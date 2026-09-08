#!/usr/bin/env python3
"""Exercise delayed child discovery and tools with a local response fixture."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shlex
import shutil
import subprocess
import threading
import time

import benchmark_codex as B
import benchmark_runner as R


def run(args, output):
	Root = Path(args.root).resolve()
	Manifest = R.read_json(Root / "control/manifest.json")
	Base, Home, Work = B.arm_paths(Root, args.task, args.arm)
	ProbeHome = output / "home"
	ProbeHome.mkdir(parents=True)
	shutil.copytree(Home / "plugins", ProbeHome / "plugins")
	shutil.copyfile(Home / "auth.json", ProbeHome / "auth.json")
	(ProbeHome / "auth.json").chmod(0o600)
	Config = (Home / "config.toml").read_text().replace(str(Home), str(ProbeHome))
	Probe = max(Base.glob("preflight-*/sandbox_probe.py"), key=lambda P: P.stat().st_mtime)
	Functional = Work / "child_functional_probe.py"
	ResultFile = Work / "child-functional-result.json"
	B.write_text(Functional, Probe.read_text().replace(str(Home), str(ProbeHome)) +
		"\npathlib.Path('child-functional-result.json').write_text(json.dumps(Result), encoding='utf-8')\n")
	ToolInput = "text(await tools.exec_command(" + json.dumps(dict(cmd=shlex.join([Manifest["python"], str(Functional)]), workdir=str(Work), max_output_tokens=1000)) + "));"
	Requests = []
	ChildDone = threading.Event()
	RootCalls, ChildCalls = 0, 0
	class Handler(BaseHTTPRequestHandler):
		def log_message(self, *unused):
			pass

		def do_POST(self):
			nonlocal RootCalls, ChildCalls
			Body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
			Requests.append(Body)
			Number = len(Requests)
			IsChild = any(Item.get("type") == "agent_message" and Item.get("recipient") == "/root/input_probe" for Item in Body.get("input", []))
			if(IsChild):
				ChildCalls += 1
				if(ChildCalls == 1):
					Item = dict(type="custom_tool_call", id=f"ctc_{Number}", call_id=f"call_{Number}", name="exec", input=ToolInput, status="completed")
				else:
					Item = dict(type="message", id=f"msg_{Number}", role="assistant", status="completed", content=[dict(type="output_text", text="CHILD_PREFLIGHT_COMPLETE", annotations=[])])
					ChildDone.set()
			else:
				RootCalls += 1
				if(RootCalls == 1):
					time.sleep(35)
					Item = dict(type="function_call", id=f"fc_{Number}", call_id=f"call_{Number}", name="spawn_agent", namespace="collaboration", arguments=json.dumps(dict(task_name="input_probe", fork_turns="none", message="CHILD_PREFLIGHT_ONLY. Execute the local infrastructure fixture; no mathematics.")), status="completed")
				elif(not ChildDone.is_set()):
					Item = dict(type="function_call", id=f"fc_{Number}", call_id=f"call_{Number}", name="wait_agent", namespace="collaboration", arguments=json.dumps(dict(timeout_ms=10000)), status="completed")
				else:
					Item = dict(type="message", id=f"msg_{Number}", role="assistant", status="completed", content=[dict(type="output_text", text="ROOT_PREFLIGHT_COMPLETE", annotations=[])])
			self.send_response(200)
			self.send_header("Content-Type", "text/event-stream")
			self.end_headers()
			Response = dict(id=f"resp_child_fixture_{Number}", object="response", status="completed", model=Manifest["model"], output=[Item], usage=dict(input_tokens=0, output_tokens=0, total_tokens=0))
			for Event in [dict(type="response.output_item.done", output_index=0, item=Item), dict(type="response.completed", response=Response)]:
				self.wfile.write(("event: " + Event["type"] + "\ndata: " + json.dumps(Event) + "\n\n").encode())
			self.wfile.flush()
	Server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
	threading.Thread(target=Server.serve_forever, daemon=True).start()
	Config = 'model_provider = "preflight"\n' + Config
	Config += '\n[model_providers.preflight]\nname = "Local child fixture"\nbase_url = ' + json.dumps(f"http://127.0.0.1:{Server.server_port}/v1") + '\nwire_api = "responses"\nenv_key = "BENCHMARK_STUB_KEY"\nrequest_max_retries = 0\nstream_max_retries = 0\n'
	B.write_text(ProbeHome / "config.toml", Config)
	Env = B.environment(ProbeHome, Work, Manifest["python"], Manifest["proxy"])
	Env["BENCHMARK_STUB_KEY"] = "local-child-fixture-only"
	Command = [Manifest["binary"], "exec", "--strict-config", "--json", "--skip-git-repo-check", "--ignore-rules", "-C", str(Work), "ROOT_CHILD_PREFLIGHT. No mathematics."]
	try:
		Result = subprocess.run(Command, env=Env, cwd=Work, capture_output=True, stdin=subprocess.DEVNULL, timeout=85)
		(output / "stdout.jsonl").write_bytes(Result.stdout)
		(output / "stderr.txt").write_bytes(Result.stderr)
	finally:
		Server.shutdown()
		Server.server_close()
	B.write_json(output / "requests.json", Requests)
	Inventory = R.session_inventory(ProbeHome)
	B.write_json(output / "sessions.json", Inventory)
	Operational = R.read_json(ResultFile) if ResultFile.exists() else {}
	for File in [Functional, ResultFile, Work / "sandbox-write.txt"]:
		File.unlink(missing_ok=True)
	Assigned = ["math-research-workflow", "rigorous-open-math-research", "manage-math-research-program", "lean-verify"]
	SkillCounts = []
	for Request in Requests:
		Text = "\n".join(Block.get("text", "") for Item in Request.get("input", []) if Item.get("role") == "developer" for Block in Item.get("content", []))
		SkillCounts.append(sum("- " + Name + ":" in Text for Name in Assigned))
	Checks = dict(child_returned=ChildDone.is_set(), root_and_child_observed=len(Inventory) == 2,
		identity_matched=all(Item["models"] == [Manifest["model"]] and Item["efforts"] == [Manifest["effort"]] for Item in Inventory),
		forbidden_metadata_absent=all(not Item["forbidden_skill_metadata"] for Item in Inventory),
		assigned_skills_matched=bool(SkillCounts) and all(Count == (0 if args.arm == "C" else 4) for Count in SkillCounts),
		child_tools_passed=bool(Operational) and all(Operational.values()), process_returned=Result.returncode == 0)
	Summary = dict(verdict="PASS" if all(Checks.values()) else "FAIL", checks=Checks,
		operational_checks=Operational, delayed_spawn_seconds=35, requests=len(Requests),
		external_model_calls=0, account_metadata_sync_enabled=True, quota_queries=0,
		fixture_usage_not_scored=True, helper_sha256=R.file_hash(__file__),
		config_sha256=R.file_hash(Home / "config.toml"), assigned_skill_counts=SkillCounts,
		model=Manifest["model"], effort=Manifest["effort"])
	B.write_json(output / "summary.json", Summary)
	print(json.dumps(Summary))
	if(Summary["verdict"] != "PASS"):
		raise RuntimeError("delayed child input or tool isolation failed")
	return Summary

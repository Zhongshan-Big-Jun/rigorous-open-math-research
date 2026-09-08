"""Deterministic runner interruption checks; these never invoke a model."""

from datetime import datetime, timedelta, timezone
import fcntl
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import benchmark_runner as R


class RunnerTests(unittest.TestCase):
	def test_unexpected_child_skill_metadata_is_visible_to_monitor(self):
		with tempfile.TemporaryDirectory() as Directory:
			Home = Path(Directory)
			(Home / "sessions").mkdir()
			Rows = [dict(type="session_meta", payload=dict(id="synthetic-child")),
				dict(type="response_item", payload=dict(type="message", role="developer", content=[dict(type="input_text", text="- deep-research-work:deep-research: unexpected extra skill")]))]
			(Home / "sessions/child.jsonl").write_text("\n".join(json.dumps(Row) for Row in Rows))
			self.assertEqual(R.session_inventory(Home)[0]["forbidden_skill_metadata"], ["deep-research-work"])

	def test_explicit_user_disables_quota_gates_without_inventing_usage(self):
		with tempfile.TemporaryDirectory() as Directory:
			Quota = Path(Directory) / "quota.json"
			Policy = Quota.with_name("quota-policy.json")
			R.persist(Policy, dict(mode="DISABLED_BY_USER", source="USER_INSTRUCTION", instruction="Quota is sufficient; ignore quota monitoring."))
			self.assertIsNone(R.quota_reason(Quota, launching=True))
			self.assertFalse(Quota.exists())
			R.persist(Quota, dict(captured_at="2020-01-01T00:00:00+00:00", windows=[]))
			self.assertIsNone(R.quota_reason(Quota))
			Policy.unlink()
			self.assertEqual(R.quota_reason(Quota), "QUOTA_SNAPSHOT_STALE")

	def test_custom_task_registration_and_legacy_budgets(self):
		with tempfile.TemporaryDirectory() as Directory:
			Root = Path(Directory)
			Task = Root / "TASK.md"
			Task.write_text("exact frozen task")
			Spec = dict(kind="PROJECT_FRONTIER_DIAGNOSTIC", tasks=dict(q9=dict(source=str(Task),
				budget_seconds=3600, audit_budget_seconds=1200, consolidation_seconds=3000,
				audit_consolidation_seconds=960)), schedule=dict(q9=["A", "C", "B"]))
			File = Root / "spec.json"
			R.persist(File, Spec)
			self.assertEqual(R.B.load_task_spec(File, Root), Spec)
			self.assertEqual(R.B.task_budget(Spec, "q9"), 3600)
			self.assertEqual(R.B.task_budget(Spec, "q9", "audit"), 1200)
			Legacy = R.B.load_task_spec(None, Root)
			self.assertEqual(R.B.task_budget(Legacy, "t1"), 1800)
			self.assertEqual(R.B.task_budget(Legacy, "t2", "audit"), 900)
			for Key, Value in [("budget_seconds", True), ("audit_budget_seconds", 0), ("consolidation_seconds", 3600)]:
				Broken = json.loads(json.dumps(Spec))
				Broken["tasks"]["q9"][Key] = Value
				R.persist(File, Broken)
				with self.assertRaises(ValueError):
					R.B.load_task_spec(File, Root)
			Spec["schedule"]["q9"] = ["A", "A", "C"]
			R.persist(File, Spec)
			with self.assertRaises(ValueError):
				R.B.load_task_spec(File, Root)
			for TaskId in ["../q9", "q9/a", "/tmp/q9", "Q9"]:
				with self.assertRaises(ValueError):
					R.B.arm_paths(Root, TaskId, "A")

	def test_custom_budget_reaches_dispatch_and_same_session_resume(self):
		from argparse import Namespace
		with tempfile.TemporaryDirectory() as Directory:
			Root = Path(Directory)
			(Root / "control").mkdir()
			Base, Home, Work = R.B.arm_paths(Root, "q9", "A")
			Work.mkdir(parents=True)
			Home.mkdir()
			(Work / "PROMPT.md").write_text("frozen common task")
			R.persist(Root / "control/quota.json", dict(captured_at=R.utc_now(), five_hour_remaining=99, weekly_remaining=99))
			Manifest = dict(binary="/usr/bin/false", python=sys.executable, proxy="http://127.0.0.1:1",
				model="gpt-6-astra", effort="max", tasks=dict(q9=dict(budget_seconds=3600)))
			Commands = []
			def fake_supervise(Command, Cwd, Env, Output, State, Quota, Budget):
				Commands.append((Command, Budget))
				State.update(root_thread_id="retained-root", active_seconds=73, stop_reason="COORDINATOR_STOP", exit_code=-2)
				return State
			Args = Namespace(root=str(Root), task="q9", arm="A", reconcile=False, resume=False)
			with patch.object(R, "assert_sealed", return_value=(Manifest, Base, Home, Work)), patch.object(R, "supervise", side_effect=fake_supervise), patch("builtins.print"):
				R.run(Args)
				Args.resume = True
				R.run(Args)
			self.assertEqual([Budget for Command, Budget in Commands], [3600, 3600])
			self.assertEqual(Commands[1][0][-2], "retained-root")
			self.assertIn("3527 seconds", Commands[1][0][-1])

	def test_quota_exhaustion_and_staleness(self):
		with tempfile.TemporaryDirectory() as Directory:
			Path = R.Path(Directory) / "quota.json"
			Data = dict(captured_at=R.utc_now(), five_hour_remaining=1, weekly_remaining=1)
			R.persist(Path, Data)
			self.assertIsNone(R.quota_reason(Path, launching=True))
			self.assertIsNone(R.quota_reason(Path))
			Data.update(five_hour_remaining=1, weekly_remaining=0)
			R.persist(Path, Data)
			self.assertEqual(R.quota_reason(Path, launching=True), "QUOTA_EXHAUSTED")
			Data["weekly_remaining"] = 1
			R.persist(Path, Data)
			self.assertIsNone(R.quota_reason(Path, launching=True))
			Data["captured_at"] = (datetime.now(timezone.utc) - timedelta(seconds=301)).isoformat()
			R.persist(Path, Data)
			self.assertEqual(R.quota_reason(Path), "QUOTA_SNAPSHOT_STALE")

	def test_stop_retains_work_and_remaining_budget(self):
		with tempfile.TemporaryDirectory() as Directory:
			Root = Path(Directory)
			Quota = Root / "quota.json"
			R.persist(Quota, dict(captured_at=R.utc_now(), five_hour_remaining=90, weekly_remaining=90))
			Script = Root / "fake.py"
			Script.write_text("import json,pathlib,time\nprint(json.dumps({'type':'thread.started','thread_id':'synthetic-test'}),flush=True)\npathlib.Path('retained.txt').write_text('partial')\npathlib.Path('STOP').touch()\ntime.sleep(30)\n")
			State = R.supervise([sys.executable, str(Script)], Root, {}, Root, {}, Quota, 5)
			self.assertEqual(State["stop_reason"], "COORDINATOR_STOP")
			self.assertEqual(State["root_thread_id"], "synthetic-test")
			self.assertEqual((Root / "retained.txt").read_text(), "partial")
			First = State["active_seconds"]
			(Root / "STOP").unlink()
			State = R.supervise([sys.executable, "-c", "print('continued')"], Root, {}, Root, State, Quota, 5)
			self.assertGreater(State["active_seconds"], First)
			self.assertEqual(len(State["segments"]), 2)
			self.assertEqual((Root / "retained.txt").read_text(), "partial")
			self.assertTrue((Root / "segment-01/events.jsonl").exists())
			with self.assertRaises(RuntimeError):
				R.supervise([sys.executable, "-c", "pass"], Root, {}, Root, State, Quota, First)

	def test_reported_windows_support_weekly_only_quota(self):
		with tempfile.TemporaryDirectory() as Directory:
			Path = R.Path(Directory) / "quota.json"
			Data = dict(captured_at=R.utc_now(), limit_id="codex", windows=[dict(window_duration_mins=10080, remaining_percent=100)])
			R.persist(Path, Data)
			self.assertIsNone(R.quota_reason(Path, launching=True))
			Data["windows"].append(dict(window_duration_mins=300, remaining_percent=0))
			R.persist(Path, Data)
			self.assertEqual(R.quota_reason(Path), "QUOTA_EXHAUSTED")
			Data["windows"].pop()
			Data["spend_control_reached"] = True
			R.persist(Path, Data)
			self.assertEqual(R.quota_reason(Path), "QUOTA_EXHAUSTED")
			Data["spend_control_reached"] = False
			Data["captured_at"] = (datetime.now(timezone.utc) - timedelta(seconds=301)).isoformat()
			R.persist(Path, Data)
			self.assertEqual(R.quota_reason(Path), "QUOTA_SNAPSHOT_STALE")

	def test_missing_or_invalid_windows_are_unknown(self):
		with tempfile.TemporaryDirectory() as Directory:
			Path = R.Path(Directory) / "quota.json"
			Invalid = [None, [], [None], [dict(window_duration_mins=10080, remaining_percent=None)],
				[dict(window_duration_mins=0, remaining_percent=100)],
				[dict(window_duration_mins=10080, remaining_percent=True)],
				[dict(window_duration_mins=10080, remaining_percent=float("nan"))]]
			for Windows in Invalid:
				with self.subTest(windows=Windows):
					R.persist(Path, dict(captured_at=R.utc_now(), limit_id="codex", windows=Windows))
					self.assertEqual(R.quota_reason(Path), "QUOTA_UNKNOWN")
			R.persist(Path, dict(captured_at=R.utc_now(), limit_id="codex_bengalfox", windows=[dict(window_duration_mins=300, remaining_percent=100)]))
			self.assertEqual(R.quota_reason(Path), "QUOTA_UNKNOWN")

	def test_lock_excludes_duplicate_dispatch(self):
		with tempfile.TemporaryDirectory() as Directory:
			with (Path(Directory) / "lock").open("a") as First, (Path(Directory) / "lock").open("a") as Second:
				fcntl.flock(First, fcntl.LOCK_EX | fcntl.LOCK_NB)
				with self.assertRaises(BlockingIOError):
					fcntl.flock(Second, fcntl.LOCK_EX | fcntl.LOCK_NB)

	def test_missing_usage_is_unknown(self):
		with tempfile.TemporaryDirectory() as Directory:
			Root = Path(Directory)
			(Root / "sessions").mkdir()
			Rows = [dict(type="session_meta", payload=dict(id="synthetic-test", source="cli")),
				dict(type="turn_context", payload=dict(model="gpt-6-astra", effort="max")),
				dict(type="response_item", payload=dict(type="function_call", call_id="call-1"))]
			Rows.append(Rows[-1])
			(Root / "sessions/test.jsonl").write_text("\n".join(json.dumps(Row) for Row in Rows))
			Data = R.session_inventory(Root)[0]
			self.assertIsNone(Data["token_usage"])
			self.assertEqual(Data["outer_tool_calls"], 1)
			self.assertIsNone(Data["response_count"])


if(__name__ == "__main__"):
	unittest.main()

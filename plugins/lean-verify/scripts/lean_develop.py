#!/usr/bin/env python3
"""Local lemma discovery, candidate feedback and exact-root checks using existing tools.

The agent writes candidates and independent expected types. This is neither an
automatic prover nor a second verifier. Development receipts authorize a fresh
atomic save; only verify_lean_project and lean_evidence decide root closure.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid

from lean_feedback import FeedbackSession, ProtocolFailure
from lean_runtime import LeanRuntime, aggregate_results, background_options, full_output, hash_bytes, hash_json, mask_lean_source, now_iso, result_status, sha256_file, source_snapshot, tool_path, write_json
from lean_evidence import TOOL_NAMES, recheck_manifest
from lean_routes import evaluate_routes
from verify_lean_project import compile_local_tree, make_parser as verifier_parser, source_imports, valid_name, verify_project


SCRIPT_DIR = Path(__file__).resolve().parent
DEVELOP_TOOLS = tuple(dict.fromkeys(("lean_develop.py", "lean_feedback.py", "lean_routes.py", *TOOL_NAMES)))
TYPE_PRINT_OPTIONS = "Options.setBool `pp.all true |>.setBool `pp.universes true |>.setBool `pp.explicit true |>.setBool `pp.deepTerms true |>.setBool `pp.proofs true |>.set `pp.maxSteps (10000000 : Nat) |>.set `maxRecDepth (8192 : Nat)"
DECLARATION = re.compile(r"\b(theorem|lemma|def|abbrev|opaque|axiom|structure|inductive)\s+([\w.']+)", re.UNICODE)


def workflow_module():
	PathValue = SCRIPT_DIR.parents[1] / "math-research-workflow" / "scripts" / "research_state.py"
	if(not PathValue.is_file()):
		raise ValueError("workflow research_state.py is unavailable; install the existing workflow component for durable jobs")
	Spec = importlib.util.spec_from_file_location("lean_develop_research_state", PathValue)
	Module = importlib.util.module_from_spec(Spec)
	Spec.loader.exec_module(Module)
	return Module


def project_file(Root, Name):
	Root = Path(Root).resolve()
	FilePath = (Root / Name).resolve()
	if(not FilePath.is_relative_to(Root) or any(FilePath.is_relative_to(Root / Name) for Name in (".lake", ".git", ".lean-verify", "__pycache__")) or FilePath.suffix != ".lean"):
		raise ValueError("candidate destination must be a project-local Lean source outside excluded generated/package directories")
	return FilePath


def development_layout(Root, Output):
	Root, Output = Path(Root).resolve(), Path(Output).resolve()
	if(Output.is_relative_to(Root) or Root.is_relative_to(Output)):
		raise ValueError("development output must be outside the project and cannot be its ancestor; in-project output is unsupported")
	return Root, Output


def tool_hashes():
	return {Name: sha256_file(SCRIPT_DIR / Name) for Name in DEVELOP_TOOLS}


# Capture the process's code epoch, before any long-lived development session.
# A new Session in this same interpreter cannot reload changed Python modules.
LOADED_TOOL_HASHES = tool_hashes()


def has_errors(Feedback):
	return any(Item.get("severity") in (1, "error") for Item in Feedback.get("diagnostics", []))


def feedback_passed(Feedback):
	return Feedback.get("status") in ("passed", "complete") and not has_errors(Feedback)


def load_targets(Root, PathValue, TargetId=None):
	"""Adapt a nonempty independently authored root list to the existing contract."""
	PathValue = Path(PathValue).resolve()
	Raw = PathValue.read_bytes()
	Data = json.loads(Raw)
	Targets = Data.get("targets") if isinstance(Data, dict) else None
	if(not isinstance(Targets, list) or not Targets):
		raise ValueError("a nonempty targets array is required")
	Ids = set()
	Result = []
	for Item in Targets:
		if(not isinstance(Item, dict)):
			raise ValueError("each target must be an object")
		Id = Item.get("id")
		if(not isinstance(Id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", Id) or Id in Ids):
			raise ValueError("each target needs a unique ordinary id")
		Ids.add(Id)
		if(not isinstance(Item.get("expected_type"), str) or not Item["expected_type"].strip()):
			raise ValueError("each target needs an independently written nonempty expected_type")
		if(not isinstance(Item.get("file"), str)):
			raise ValueError("each target needs a source file")
		Contract = {"file": str(project_file(Root, Item["file"]).relative_to(Path(Root).resolve())), "declaration": valid_name(Item.get("declaration")), "expected_type": Item["expected_type"]}
		Universes = Item.get("universes", [])
		if(not isinstance(Universes, list)):
			raise ValueError("universes must be an array")
		Contract["universes"] = [valid_name(Name) for Name in Universes]
		for Key in ("definition_hashes", "type_sha256", "environment_sha256", "semantic_sha256", "semantic_environment_sha256", "input_file_hashes"):
			if(Key in Item):
				Contract[Key] = Item[Key]
		Result.append((Id, Contract, Item))
	if(TargetId is not None):
		Result = [Item for Item in Result if Item[0] == TargetId]
		if(not Result):
			raise ValueError("requested target id is absent")
	return Result, hash_bytes(Raw)


def declarations_in_file(FilePath):
	"""Source-location hints only; Lean probes authenticate the inferred names."""
	Code = mask_lean_source(Path(FilePath).read_text(encoding="utf-8-sig"))
	Stack = []
	Records = []
	for LineNumber, Line in enumerate(Code.splitlines(), 1):
		Namespace = re.match(r"\s*namespace\s+([\w.']+)", Line)
		Section = re.match(r"\s*(?:noncomputable\s+)?section(?:\s+([\w.']+))?\s*$", Line)
		End = re.match(r"\s*end(?:\s+([\w.']+))?\s*$", Line)
		if(Namespace):
			Stack.append(("namespace", Namespace.group(1)))
		elif(Section):
			Stack.append(("section", Section.group(1)))
		elif(End and Stack):
			Stack.pop()
		for Match in DECLARATION.finditer(Line):
			Prefix = ".".join(Value for Kind, Value in Stack if Kind == "namespace")
			Name = Match.group(2)
			Name = Name[7:] if Name.startswith("_root_.") else Prefix + "." + Name if Prefix else Name
			Records.append({"candidate_name": Name, "kind": Match.group(1), "declaration_line": LineNumber})
	return Records


def source_roots(Root):
	Roots = [("project", Root)]
	Manifest = Root / "lake-manifest.json"
	if(Manifest.is_file()):
		Data = json.loads(Manifest.read_text(encoding="utf-8-sig"))
		Package = next((Item for Item in Data.get("packages", []) if Item.get("name") == "mathlib"), None)
		if(Package):
			PackagesDir = Root / Data.get("packagesDir", ".lake/packages")
			PackageRoot = (PackagesDir / "mathlib").resolve()
			if(PackageRoot.is_dir()):
				Roots.append(("mathlib", PackageRoot))
	return Roots


def search_sources(Runtime, Query, Limit=20):
	if(not Query.strip() or Limit <= 0):
		raise ValueError("a nonempty search query and a positive limit are required")
	Rg = shutil.which("rg")
	Matches = []
	Cache = {}
	Engines = []
	Roots = source_roots(Runtime.Root)
	for RootIndex, (Scope, Root) in enumerate(Roots):
		StartCount = len(Matches)
		ScopeLimit = max(1, (Limit - StartCount) // (len(Roots) - RootIndex))
		if(Rg):
			Command = [Rg, "--json", "--no-ignore", "--hidden", "-i", "-F", "-g", "*.lean", "-g", "!**/.lake/**", "-g", "!**/.git/**", "-g", "!**/.lean-verify/**", "--", Query, "."]
			Engines.append({"scope": Scope, "cwd": str(Root), "command": Command})
			Process = subprocess.Popen(Command, cwd=Root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **background_options())
			try:
				for Raw in Process.stdout:
					Event = json.loads(Raw)
					if(Event.get("type") != "match"):
						continue
					Data = Event["data"]
					FilePath = (Root / Data["path"]["text"]).resolve()
					Matches.append(search_match(FilePath, Root, Scope, Data["line_number"], Data["lines"]["text"], Cache))
					if(len(Matches) - StartCount >= ScopeLimit):
						break
			finally:
				if(Process.poll() is None):
					Process.terminate()
				Process.communicate(timeout=10)
		else:
			Engines.append({"scope": Scope, "engine": "stdlib fallback; rg unavailable"})
			for Directory, Subdirs, Names in os.walk(Root):
				Subdirs[:] = sorted(Name for Name in Subdirs if Name not in (".lake", ".git", ".lean-verify", "__pycache__"))
				for Name in sorted(Names):
					if(not Name.endswith(".lean")):
						continue
					FilePath = Path(Directory) / Name
					for LineNumber, Line in enumerate(FilePath.read_text(encoding="utf-8-sig").splitlines(), 1):
						if(Query.lower() in Line.lower()):
							Matches.append(search_match(FilePath, Root, Scope, LineNumber, Line, Cache))
							if(len(Matches) - StartCount >= ScopeLimit):
								break
					if(len(Matches) - StartCount >= ScopeLimit):
						break
				if(len(Matches) - StartCount >= ScopeLimit):
					break
		if(len(Matches) >= Limit):
			break
	return {"status": "searched", "query": Query, "matches": Matches, "limit": Limit, "search_engines": Engines, "environment_sha256": Runtime.environment()["sha256"], "exact_root_passed": False, "scope": "source hits; inferred names require the actual-version probe"}


def search_match(FilePath, Root, Scope, LineNumber, Text, Cache):
	if(FilePath not in Cache):
		Cache[FilePath] = declarations_in_file(FilePath)
	Before = [Item for Item in Cache[FilePath] if Item["declaration_line"] <= LineNumber]
	Declaration = Before[-1] if Before else {}
	return {"file": str(FilePath), "module": ".".join(FilePath.relative_to(Root).with_suffix("").parts), "scope": Scope, "line": LineNumber, "text": Text.rstrip(), "source_sha256": sha256_file(FilePath), **Declaration}


class DevelopSession:
	def __init__(self, Runtime, Timeout=60, Backend="auto"):
		development_layout(Runtime.Root, Runtime.LogDir)
		self.LoadedToolHashes = dict(LOADED_TOOL_HASHES)
		self.require_current_tools()
		self.Runtime = Runtime
		self.Timeout = Timeout
		self.Feedback = FeedbackSession(Runtime, Timeout, Backend)
		self.ImportPreparationCache = {}

	def close(self):
		self.Feedback.close()

	def require_current_tools(self):
		if(hasattr(self, "Runtime")):
			development_layout(self.Runtime.Root, self.Runtime.LogDir)
		if(tool_hashes() != self.LoadedToolHashes):
			raise ValueError("development code changed since process load; start a new Python process (LSP restart does not reload Python)")

	def prepare_imports(self, Source, Directory):
		Discovery = self.Runtime.source_dependencies(Source, Directory, self.Timeout)
		Commands = [Discovery]
		if(result_status(Discovery) != "passed"):
			return Commands
		Imports, Sources = source_imports(Discovery, self.Runtime.Root)
		self.Runtime.Environment = None
		CacheKey = hash_json({"imports": Imports, "sources": source_snapshot(self.Runtime.Root, [self.Runtime.LogDir]), "environment": self.Runtime.environment()["sha256"]})
		Cached = self.ImportPreparationCache.get(CacheKey)
		if(Cached):
			CurrentImports = self.import_identity(Source.read_text(encoding="utf-8"))
			if(CurrentImports == Cached["inventory"] and all(Path(Name).is_file() and self.Feedback.HashCache.digest(Name) == Digest for Name, Digest in Cached["artifacts"].items())):
				for Library in Cached["libraries"]:
					if(Library not in self.Runtime.SearchPaths):
						self.Runtime.SearchPaths.insert(0, Library)
				Commands.append({"status": "passed", "exit_code": 0, "kind": "development_import_cache", "scope": "current source/environment/artifact bindings; final roots still require fresh verification", "cache_key": CacheKey})
				return Commands
		Libraries = []
		for FilePath in Sources:
			if(FilePath is not None):
				# Lean resolves one module-directory prefix in the first search root.
				# All local imports must therefore share one complete fresh library.
				Library, Compilation = compile_local_tree(self.Runtime, FilePath, Directory / "local-imports", self.Timeout)
				Commands.extend(Compilation)
				if(aggregate_results(Compilation)["status"] != "passed"):
					return Commands
				if(Library not in Libraries):
					self.Runtime.SearchPaths.insert(0, Library)
					Libraries.append(Library)
		if(Libraries):
			Artifacts = self.import_identity(Source.read_text(encoding="utf-8"))
			self.ImportPreparationCache[CacheKey] = {"libraries": Libraries, "artifacts": {Item["path"]: Item["sha256"] for Item in Artifacts.values()}, "inventory": Artifacts}
		return Commands

	def import_identity(self, Text):
		Inventory = self.Feedback.inventory(self.Feedback.import_header(Text))
		return {Name: {"path": PathValue, "sha256": self.Feedback.HashCache.digest(PathValue)} for Name, PathValue in Inventory.items()}

	def trial(self, FileName, Candidate):
		self.require_current_tools()
		FilePath = project_file(self.Runtime.Root, FileName)
		Raw = Path(Candidate).read_bytes()
		Text = Raw.decode("utf-8")
		if(not Text.strip()):
			raise ValueError("candidate source must be nonempty")
		if(Text.startswith("\ufeff")):
			raise ValueError("candidate source must be UTF-8 without BOM")
		Directory = self.Runtime.LogDir / "development" / uuid.uuid4().hex
		Directory.mkdir(parents=True)
		CandidatePath = Directory / "Candidate.lean"
		CandidatePath.write_bytes(Raw)
		Initial = source_snapshot(self.Runtime.Root, [self.Runtime.LogDir])
		DiskHash = sha256_file(FilePath) if FilePath.is_file() else None
		Commands = self.prepare_imports(CandidatePath, Directory)
		if(aggregate_results(Commands)["status"] != "passed"):
			Feedback = {"status": aggregate_results(Commands)["status"], "reason": "current local imports could not be prepared", "exact_root_passed": False}
			Imports = {}
		else:
			try:
				Imports = self.import_identity(Text)
				CurrentPaths = {Name: Item["path"] for Name, Item in Imports.items()}
				if(self.Feedback.ImportInventory and self.Feedback.ImportInventory != CurrentPaths):
					# The LSP process inherited its LEAN_PATH at launch. Replacing a
					# prepared library or adding a shadow must refresh that context.
					self.Feedback.query({"action": "restart"})
				Feedback = self.Feedback.query({"action": "diagnostics", "file": str(FilePath.relative_to(self.Runtime.Root)), "text": Text})
				if(Imports != self.import_identity(Text)):
					Feedback.update(status="stale", reason="import resolution or artifacts changed during candidate feedback")
			except (OSError, ProtocolFailure) as Error:
				Imports = {}
				Feedback = {"status": "unavailable", "reason": str(Error), "exact_root_passed": False}
		if(Initial != source_snapshot(self.Runtime.Root, [self.Runtime.LogDir]) or DiskHash != (sha256_file(FilePath) if FilePath.is_file() else None)):
			Feedback.update(status="stale", reason="current source changed during candidate feedback")
		if(tool_hashes() != self.LoadedToolHashes):
			Feedback.update(status="stale", reason="development code changed during feedback; start a new Python process")
		Receipt = {"schema": "lean-development-trial/v1", "created_at": now_iso(), "project_root": str(self.Runtime.Root), "file": str(FilePath.relative_to(self.Runtime.Root)), "candidate": str(CandidatePath), "candidate_sha256": hash_bytes(Raw), "disk_sha256": DiskHash, "input_hashes": Initial, "environment_sha256": self.Runtime.environment()["sha256"], "import_artifacts": Imports, "tool_hashes": self.LoadedToolHashes, "feedback": Feedback, "preparation_commands": Commands, "search_paths": [str(Item) for Item in self.Runtime.SearchPaths], "exact_root_passed": False}
		Receipt["receipt_sha256"] = hash_json(Receipt)
		ReceiptPath = Directory / "trial.json"
		write_json(ReceiptPath, Receipt)
		return {"status": "candidate_checked" if feedback_passed(Feedback) else "candidate_incomplete", "receipt": str(ReceiptPath), "candidate_sha256": Receipt["candidate_sha256"], "feedback": Feedback, "exact_root_passed": False}

	def save(self, ReceiptPath):
		self.require_current_tools()
		Receipt = json.loads(Path(ReceiptPath).read_text(encoding="utf-8"))
		Digest = Receipt.pop("receipt_sha256", None)
		if(Receipt.get("schema") != "lean-development-trial/v1" or hash_json(Receipt) != Digest or Receipt.get("project_root") != str(self.Runtime.Root)):
			raise ValueError("invalid development receipt or different project")
		if(not feedback_passed(Receipt["feedback"])):
			raise ValueError("incomplete or stale candidate feedback cannot authorize saving")
		Raw = Path(Receipt["candidate"]).read_bytes()
		if(hash_bytes(Raw) != Receipt["candidate_sha256"] or Receipt["tool_hashes"] != tool_hashes()):
			raise ValueError("candidate or development tools changed; run a fresh trial")
		FilePath = project_file(self.Runtime.Root, Receipt["file"])
		Workflow = workflow_module()
		with Workflow.writer_lock(self.Runtime.Root / ".lean-verify" / "development-save.lock"):
			CurrentRaw = FilePath.read_bytes() if FilePath.is_file() else None
			if((hash_bytes(CurrentRaw) if CurrentRaw is not None else None) != Receipt["disk_sha256"]):
				raise ValueError("destination changed since candidate feedback; merge and retry")
			if(source_snapshot(self.Runtime.Root, [self.Runtime.LogDir]) != Receipt["input_hashes"]):
				raise ValueError("source or configuration changed; run a fresh trial")
			self.Runtime.Environment = None
			if(self.Runtime.environment()["sha256"] != Receipt["environment_sha256"]):
				raise ValueError("runtime or pinned environment changed; run a fresh trial")
			self.Runtime.SearchPaths = [Path(Item) for Item in Receipt["search_paths"]]
			if(self.import_identity(Raw.decode("utf-8")) != Receipt["import_artifacts"]):
				raise ValueError("import resolution or artifacts changed; run a fresh trial")
			self.require_current_tools()
			# Environment and actual import queries can take time. Recheck editor
			# inputs after them, immediately before the atomic compare-and-write.
			if(source_snapshot(self.Runtime.Root, [self.Runtime.LogDir]) != Receipt["input_hashes"]):
				raise ValueError("source or configuration changed during save; run a fresh trial")
			FinalRaw = FilePath.read_bytes() if FilePath.is_file() else None
			if((hash_bytes(FinalRaw) if FinalRaw is not None else None) != Receipt["disk_sha256"]):
				raise ValueError("destination changed during save; merge and retry")
			Workflow.atomic_write(FilePath, Raw, CurrentRaw)
		Result = {"status": "saved", "file": str(FilePath), "source_sha256": sha256_file(FilePath), "trial": str(Path(ReceiptPath).resolve()), "exact_root_passed": False, "scope": "fresh candidate atomically saved; exact statement and axiom verification still required"}
		write_json(Path(ReceiptPath).with_name("save.json"), Result)
		return Result

	def probe(self, Names, Imports):
		self.require_current_tools()
		Names = [valid_name(Name) for Name in Names]
		Imports = [valid_name(Name) for Name in Imports]
		if(not Names):
			raise ValueError("probe needs at least one declaration name")
		Directory = self.Runtime.LogDir / "probes" / uuid.uuid4().hex
		Directory.mkdir(parents=True)
		Source = Directory / "Interface.lean"
		Code = "import Lean\n" + "".join("import " + Name + "\n" for Name in Imports)
		Code += "open Lean Elab Command Meta\n"
		for Name in Names:
			Code += ("run_cmd do\n  let Environment := (← getEnv).setExporting false\n  let Name := `" + Name + "\n  let some Info := Environment.checked.get.find? Name | throwError \"requested declaration is absent\"\n  let FullType ← liftTermElabM <| withOptions (fun Options => " + TYPE_PRINT_OPTIONS + ") (do\n    let Printed := (← ppExpr Info.type).pretty\n    if Printed.contains '⋯' then throwError \"type pretty-printing omitted terms; complete readable type unavailable\"\n    return Printed)\n  let Module := (Environment.getModuleIdxFor? Name).bind fun Index => Environment.header.moduleNames[Index.toNat]?\n  IO.println (\"LEAN_DEVELOP_DECL \" ++ (Json.mkObj [(\"name\", toJson Name.toString), (\"actual_type\", toJson FullType), (\"module\", toJson (Module.map Lean.Name.toString)), (\"universes\", toJson (Info.levelParams.map Lean.Name.toString))]).compress)\n")
		Source.write_text(Code, encoding="utf-8", newline="\n")
		Commands = self.prepare_imports(Source, Directory)
		if(aggregate_results(Commands)["status"] == "passed"):
			Commands.append(self.Runtime.execute([tool_path(Source, self.Runtime.Command)], self.Timeout))
		Declarations = []
		if(Commands):
			for Line in full_output(Commands[-1]).splitlines():
				if(Line.startswith("LEAN_DEVELOP_DECL ")):
					Declarations.append(json.loads(Line[len("LEAN_DEVELOP_DECL "):]))
		Readable = all(isinstance(Item.get("actual_type"), str) and Item["actual_type"].strip() and "⋯" not in Item["actual_type"] for Item in Declarations)
		Result = {"status": "checked" if aggregate_results(Commands)["status"] == "passed" and len(Declarations) == len(Names) and Readable else "incomplete", "declarations": Declarations, "probe_source": str(Source), "commands": Commands, "environment_sha256": self.Runtime.environment()["sha256"], "exact_root_passed": False, "scope": "actual installed-environment type/interface query; not a proof"}
		if(tool_hashes() != self.LoadedToolHashes):
			Result.update(status="incomplete", reason="development code changed during the interface probe; start a new Python process")
		write_json(Directory / "probe.json", Result)
		return Result


def batch_input_snapshot(Runtime, ListPath, Targets):
	"""Observed declared inputs/version, not an OS-wide filesystem transaction."""
	development_layout(Runtime.Root, Runtime.LogDir)
	Runtime.Environment = None
	Environment = Runtime.environment()
	Paths = {Path(ListPath).resolve()}
	for _, Contract, Item in Targets:
		Bindings = Contract.get("input_file_hashes", {})
		if(not isinstance(Bindings, dict)):
			raise ValueError("contract input_file_hashes must map paths to SHA-256 values")
		Paths.update((Runtime.Root / Name).resolve() for Name in Bindings)
		if(Item.get("semantic_audit")):
			Paths.add((Runtime.Root / Item["semantic_audit"]).resolve())
	Files = {str(PathValue): sha256_file(PathValue) if PathValue.is_file() else None for PathValue in sorted(Paths)}
	Sources = source_snapshot(Runtime.Root)
	return {"environment_sha256": Environment["sha256"], "bound_files": Files, "sources": Sources, "tool_hashes": tool_hashes()}


def batch_evidence_snapshot(Rows, ExtraPaths=()):
	"""Keep already listed evidence bytes stable across the terminal recheck pass."""
	Paths = {Path(Name) for Name in ExtraPaths}
	for Row in Rows:
		ManifestPath = Path(Row["manifest"])
		Paths.add(ManifestPath)
		Manifest = json.loads(ManifestPath.read_bytes())
		Evidence = Manifest.get("evidence") or {}
		Target = Manifest.get("target") or {}
		Paths.update(Path(Name) for Name in Evidence.get("compiled_artifacts") or {})
		Paths.update(Path(Item["path"]) for Item in (Target.get("import_artifacts") or {}).values())
		if(Target.get("extraction_file")):
			Paths.add(Path(Target["extraction_file"]))
		if(Evidence.get("run_directory")):
			Directory = Path(Evidence["run_directory"])
			Paths.update(Directory / Name for Name in ("input-snapshot.json", "run-manifest.json"))
			Paths.update(Directory / Name for Name in Evidence.get("generated_sources", {}))
		for Command in (Manifest.get("build") or {}).get("commands", []):
			Paths.update(Path(Command[Name]) for Name in ("job_record", "stdout_log", "stderr_log") if Command.get(Name))
	return {str(PathValue): sha256_file(PathValue) if PathValue.is_file() else None for PathValue in sorted(Paths)}


def verify_targets(Arguments):
	Root, Output = development_layout(Arguments.project, Arguments.output)
	Targets, ListHash = load_targets(Root, Arguments.targets, Arguments.target_id)
	ListPath = Path(Arguments.targets).resolve()
	Runtime = LeanRuntime(Root, Output, Arguments.lean, Arguments.lake, Arguments.direct)
	Initial = batch_input_snapshot(Runtime, ListPath, Targets)
	Results = []
	for Id, Contract, Item in Targets:
		Directory = Output / "targets" / Id
		Directory.mkdir(parents=True, exist_ok=True)
		ContractPath = Directory / "contract.json"
		# Keep the independently authored source list available to the verifier snapshot.
		Contract["input_file_hashes"] = {**Contract.get("input_file_hashes", {}), str(Path(Arguments.targets).resolve()): ListHash}
		write_json(ContractPath, Contract)
		Argv = ["--project", str(Root), "--output", str(Directory), "--contract", str(ContractPath), "--lean", Arguments.lean, "--lake", Arguments.lake, "--build-timeout", str(Arguments.timeout), "--strict-exit"]
		if(Arguments.direct):
			Argv.append("--direct")
		Audit = Item.get("semantic_audit")
		if(Audit):
			Argv += ["--semantic-audit", str((Root / Audit).resolve())]
		Manifest, ManifestPath = verify_project(verifier_parser().parse_args(Argv))
		Results.append({"id": Id, "declaration": Contract["declaration"], "manifest": str(ManifestPath), "manifest_sha256": sha256_file(ManifestPath), "exact_root_passed": False, "machine": Manifest["machine"], "root_closure": Manifest["root_closure"], "semantic": Manifest["semantic"]})
	# Earlier root checks cannot authorize the later combined result. Observe a
	# common input/version epoch on both sides of one terminal pass over all roots.
	Before = batch_input_snapshot(Runtime, ListPath, Targets)
	EvidenceBefore = batch_evidence_snapshot(Results)
	Checks = [recheck_manifest(Item["manifest"]) for Item in Results]
	EvidenceAfter = batch_evidence_snapshot(Results)
	After = batch_input_snapshot(Runtime, ListPath, Targets)
	ListCurrent = After["bound_files"].get(str(ListPath)) == ListHash
	Changed = [Key for Key in Initial if Initial[Key] != Before[Key] or Before[Key] != After[Key]]
	if(EvidenceBefore != EvidenceAfter):
		Changed.append("evidence_bytes")
	if(Initial["tool_hashes"] != LOADED_TOOL_HASHES):
		Changed.append("loaded_tools")
	if(not ListCurrent):
		Changed.append("target_list")
	BatchCurrent = not Changed
	for Item, Check in zip(Results, Checks):
		ManifestCurrent = EvidenceBefore.get(Item["manifest"]) == Item["manifest_sha256"] and Check.get("manifest_sha256") == Item["manifest_sha256"]
		Item.update(evidence_check=Check, target_list_current=ListCurrent, batch_current=BatchCurrent, manifest_current=ManifestCurrent,
			exact_root_passed=BatchCurrent and ManifestCurrent and Item["root_closure"].get("exact_root_passed") is True and Check["exact_root_passed"] is True)
	SnapshotPath = Output / "batch-inputs.json"
	write_json(SnapshotPath, {"initial": Initial, "before_terminal_rechecks": Before, "after_terminal_rechecks": After, "evidence_before": EvidenceBefore, "evidence_after": EvidenceAfter})
	Result = {"status": "verified" if all(Item["exact_root_passed"] for Item in Results) else "incomplete", "target_list": str(ListPath), "target_list_sha256": ListHash, "targets": Results, "batch": {"current": BatchCurrent, "changed": Changed, "input_snapshot": str(SnapshotPath), "input_snapshot_sha256": sha256_file(SnapshotPath), "scope": "declared inputs/version and listed evidence observed stable across terminal rechecks; no OS-wide filesystem transaction"}, "exact_root_passed": bool(Results) and all(Item["exact_root_passed"] for Item in Results), "scope": "selected nonempty exact roots checked by existing verifier and terminal evidence pass with common input/version bindings; semantic acceptance and publication separate"}
	write_json(Output / "development-result.json", Result)
	return Result


def start_verification(Arguments):
	Root, Output = development_layout(Arguments.project, Arguments.output)
	Targets, _ = load_targets(Root, Arguments.targets, Arguments.target_id)
	ListPath = Path(Arguments.targets).resolve()
	if(not ListPath.is_relative_to(Root)):
		raise ValueError("durable verification requires a project-local target list so the existing workflow can bind it")
	Command = [sys.executable, "-X", "utf8", str(Path(__file__).resolve()), "--project", str(Root), "--output", str(Output), "--lean", Arguments.lean, "--lake", Arguments.lake, "--timeout", str(Arguments.timeout)]
	if(Arguments.direct):
		Command.append("--direct")
	Command += ["verify", "--targets", str(ListPath)]
	if(Arguments.target_id):
		Command += ["--target-id", Arguments.target_id]
	Inputs = list(source_snapshot(Root)) + [str(ListPath.relative_to(Root))]
	for _, _, Item in Targets:
		if(Item.get("semantic_audit")):
			Inputs.append(Item["semantic_audit"])
	Result = workflow_module().start_job(Root, Arguments.job_id, Command, sorted(set(Inputs)), Timeout=Arguments.job_timeout)
	Result["exact_root_passed"] = False
	return Result


def verification_status(Arguments):
	Root, Output = development_layout(Arguments.project, Arguments.output)
	Workflow = workflow_module()
	Result = Workflow.job_status(Root, Arguments.job_id)
	Result["exact_root_passed"] = False
	ManifestPath = Output / "development-result.json"
	if(Result["state"] == "SUCCEEDED" and Result.get("recorded_inputs_match_current") and ManifestPath.is_file()):
		SummaryRaw = ManifestPath.read_bytes()
		Summary = json.loads(SummaryRaw)
		Command = Result.get("command", [])
		ListPath = Summary.get("target_list")
		if(ListPath and ListPath in Command and "--output" in Command and Path(Command[Command.index("--output") + 1]).resolve() == Output):
			Targets, CurrentHash = load_targets(Root, ListPath, Command[Command.index("--target-id") + 1] if "--target-id" in Command else None)
			Rows = Summary.get("targets", [])
			Runtime = LeanRuntime(Root, Output, Command[Command.index("--lean") + 1], Command[Command.index("--lake") + 1], "--direct" in Command)
			StdoutPath = Root / Result["stdout"]
			ExtraPaths = [ManifestPath, StdoutPath]
			if(Result.get("stderr")):
				ExtraPaths.append(Root / Result["stderr"])
			JobPath = Workflow.job_path(Root, Arguments.job_id)
			if(JobPath.is_file()):
				ExtraPaths.append(JobPath)
			Before = batch_input_snapshot(Runtime, ListPath, Targets)
			EvidenceBefore = batch_evidence_snapshot(Rows, ExtraPaths)
			Checks = [recheck_manifest(Item["manifest"]) for Item in Rows]
			ById = {Id: Contract for Id, Contract, _ in Targets}
			Bound = len(Rows) == len(Targets) and {Item["id"] for Item in Rows} == set(ById) and EvidenceBefore.get(str(ManifestPath)) == hash_bytes(SummaryRaw)
			for Item in Rows:
				ManifestRaw = Path(Item["manifest"]).read_bytes()
				Manifest = json.loads(ManifestRaw)
				Contract = Manifest["evidence"]["contract"]
				Bound = Bound and Item["manifest_sha256"] == hash_bytes(ManifestRaw) == EvidenceBefore.get(Item["manifest"]) and Item["id"] in ById and all(Contract.get(Key) == Value for Key, Value in ById.get(Item["id"], {}).items() if Key != "input_file_hashes") and Contract.get("input_file_hashes", {}).get(ListPath) == CurrentHash
			PrintedRaw = StdoutPath.read_bytes()
			Printed = json.loads(PrintedRaw)
			Bound = Bound and hash_bytes(PrintedRaw) == EvidenceBefore.get(str(StdoutPath)) and (not Result.get("stdout_sha256") or hash_bytes(PrintedRaw) == Result["stdout_sha256"])
			CurrentJob = Workflow.job_status(Root, Arguments.job_id)
			Bound = Bound and CurrentJob.get("recorded_inputs_match_current") and all(CurrentJob.get(Key) == Result.get(Key) for Key in ("state", "command", "inputs", "stdout_sha256", "stderr_sha256"))
			# Manifest/contract/stdout/job reads can be large. Complete them before
			# the final evidence and common-input observations, never after them.
			EvidenceAfter = batch_evidence_snapshot(Rows, ExtraPaths)
			After = batch_input_snapshot(Runtime, ListPath, Targets)
			Stable = Before == After and EvidenceBefore == EvidenceAfter and After["tool_hashes"] == LOADED_TOOL_HASHES and After["bound_files"].get(ListPath) == CurrentHash
			Result["exact_root_passed"] = bool(Rows) and Bound and Stable and Printed == Summary and CurrentHash == Summary.get("target_list_sha256") and all(Check["exact_root_passed"] is True for Check in Checks)
			Result["verification"] = {"summary": str(ManifestPath), "checks": Checks, "batch_current": Stable}
	return Result


def serve(Session):
	"""One JSON request/response per line; keep the existing feedback engine warm."""
	for Line in sys.stdin:
		try:
			Session.require_current_tools()
			Request = json.loads(Line)
			if(not isinstance(Request, dict)):
				raise ValueError("development request must be an object")
			Action = Request.get("action")
			if(Action == "close"):
				print(json.dumps({"status": "closed", "exact_root_passed": False}), flush=True)
				return 0
			if(Action == "trial"):
				Result = Session.trial(Request["file"], Request["candidate"])
			elif(Action == "save"):
				Result = Session.save(Request["receipt"])
			elif(Action == "probe"):
				Result = Session.probe(Request["names"], Request.get("imports", []))
			elif(Action == "search"):
				Result = search_sources(Session.Runtime, Request["query"], Request.get("limit", 20))
			elif(Action == "feedback"):
				Result = Session.Feedback.query(Request["request"])
			elif(Action == "restart"):
				Session.ImportPreparationCache = {}
				Session.Runtime.SearchPaths = []
				Result = Session.Feedback.query({"action": "restart"})
				Result["exact_root_passed"] = False
			else:
				raise ValueError("unknown development action; use search, probe, trial, save, feedback, restart or close")
			Session.require_current_tools()
		except (OSError, ValueError, KeyError, TypeError, ProtocolFailure, subprocess.TimeoutExpired) as Error:
			Result = {"status": "incomplete", "reason": str(Error), "exact_root_passed": False}
		print(json.dumps(Result, ensure_ascii=True), flush=True)
	return 0


def make_parser():
	Parser = argparse.ArgumentParser(description=__doc__)
	Parser.add_argument("--project", required=True)
	Parser.add_argument("--output", required=True)
	Parser.add_argument("--lean", default="lean")
	Parser.add_argument("--lake", default="lake")
	Parser.add_argument("--direct", action="store_true")
	Parser.add_argument("--timeout", type=float, default=60)
	Sub = Parser.add_subparsers(dest="action", required=True)
	Search = Sub.add_parser("search")
	Search.add_argument("--query", required=True)
	Search.add_argument("--limit", type=int, default=20)
	Search.add_argument("--probe", action="store_true")
	Probe = Sub.add_parser("probe")
	Probe.add_argument("--name", action="append", required=True)
	Probe.add_argument("--import", dest="imports", action="append", default=[])
	Trial = Sub.add_parser("trial")
	Trial.add_argument("--file", required=True)
	Trial.add_argument("--candidate", required=True)
	Trial.add_argument("--backend", choices=("auto", "cli", "lsp"), default="auto")
	Serve = Sub.add_parser("serve")
	Serve.add_argument("--backend", choices=("auto", "cli", "lsp"), default="auto")
	Save = Sub.add_parser("save")
	Save.add_argument("--receipt", required=True)
	for Name in ("verify", "start"):
		Part = Sub.add_parser(Name)
		Part.add_argument("--targets", required=True)
		Part.add_argument("--target-id")
		if(Name == "start"):
			Part.add_argument("--job-id", required=True)
			Part.add_argument("--job-timeout", type=float)
	Status = Sub.add_parser("status")
	Status.add_argument("--job-id", required=True)
	Routes = Sub.add_parser("routes")
	Routes.add_argument("--graph", required=True)
	Routes.add_argument("--root", required=True)
	Routes.add_argument("--root-manifest")
	return Parser


def main():
	Arguments = make_parser().parse_args()
	Runtime = LeanRuntime(Arguments.project, Arguments.output, Arguments.lean, Arguments.lake, Arguments.direct)
	Session = None
	try:
		if(not Runtime.Root.is_dir()):
			raise ValueError("project directory does not exist")
		Session = DevelopSession(Runtime, Arguments.timeout, getattr(Arguments, "backend", "auto"))
		if(Arguments.action == "serve"):
			return serve(Session)
		if(Arguments.action == "search"):
			Result = search_sources(Runtime, Arguments.query, Arguments.limit)
			if(Arguments.probe):
				for Item in Result["matches"]:
					if(Item.get("candidate_name")):
						Item["interface"] = Session.probe([Item["candidate_name"]], [Item["module"]])
			write_json(Runtime.LogDir / "search-result.json", Result)
		elif(Arguments.action == "probe"):
			Result = Session.probe(Arguments.name, Arguments.imports)
		elif(Arguments.action == "trial"):
			Result = Session.trial(Arguments.file, Arguments.candidate)
		elif(Arguments.action == "save"):
			Result = Session.save(Arguments.receipt)
		elif(Arguments.action == "verify"):
			Result = verify_targets(Arguments)
		elif(Arguments.action == "start"):
			Result = start_verification(Arguments)
		elif(Arguments.action == "status"):
			Result = verification_status(Arguments)
		else:
			Result = evaluate_routes(json.loads(Path(Arguments.graph).read_text(encoding="utf-8")), Arguments.root, Arguments.root_manifest)
		# ASCII JSON is portable to native Windows hosts whose stdout defaults to GBK.
		print(json.dumps(Result, ensure_ascii=True, indent="\t"))
		return 1 if Result.get("status") in ("incomplete", "candidate_incomplete") or (Arguments.action == "verify" and not Result["exact_root_passed"]) else 0
	except (OSError, ValueError, KeyError, TypeError, ProtocolFailure, subprocess.TimeoutExpired) as Error:
		print(json.dumps({"status": "incomplete", "reason": str(Error), "exact_root_passed": False}, ensure_ascii=True))
		return 2
	finally:
		if(Session is not None):
			Session.close()


if(__name__ == "__main__"):
	raise SystemExit(main())

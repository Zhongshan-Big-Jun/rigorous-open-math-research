#!/usr/bin/env python3
"""Use fresh, same-account returned service limits when desktop reads fail."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import benchmark_runner as R


def event_snapshot(row, path, line_number, line, now=None):
	Payload = row.get("payload", {})
	Limits = Payload.get("rate_limits")
	if(row.get("type") != "event_msg" or Payload.get("type") != "token_count" or not Limits or Limits.get("limit_id") != "codex"):
		return None
	Timestamp = row["timestamp"].replace("Z", "+00:00")
	Age = ((now or datetime.now(timezone.utc)) - datetime.fromisoformat(Timestamp)).total_seconds()
	if(not 0 <= Age <= 120):
		return None
	Windows = []
	for Window in [Limits.get("primary"), Limits.get("secondary")]:
		if(Window is None):
			continue
		Duration, Used = Window.get("window_minutes"), Window.get("used_percent")
		if(type(Duration) is not int or Duration <= 0 or type(Used) not in [int, float] or not 0 <= Used <= 100):
			return None
		Windows.append(dict(window_duration_mins=Duration, remaining_percent=100-Used, resets_at=Window.get("resets_at")))
	if(not Windows):
		return None
	return dict(captured_at=Timestamp, limit_id="codex", windows=Windows,
		plan_type=Limits.get("plan_type"), spend_control_reached=Limits.get("spend_control_reached"),
		source="RETURNED_CODEX_RATE_LIMIT_EVENT", source_path=str(path), source_line=line_number,
		source_line_sha256=hashlib.sha256(line.encode()).hexdigest(), desktop_same_account=True)


def refresh(campaign, base, auth_source):
	Account = R.read_json(auth_source).get("tokens", {}).get("account_id")
	Other = R.read_json(base / "home/auth.json").get("tokens", {}).get("account_id")
	if(not Account or Other != Account):
		raise RuntimeError("fallback requires confirmed same-account service events")
	Snapshots = []
	for File in (base / "home/sessions").glob("**/*.jsonl"):
		Lines = File.read_text(encoding="utf-8").splitlines()
		for Number, Line in enumerate(Lines, 1):
			try:
				Row = json.loads(Line)
			except json.JSONDecodeError:
				if(Number == len(Lines)):
					continue
				raise
			Snapshot = event_snapshot(Row, File, Number, Line)
			if(Snapshot):
				Snapshots.append(Snapshot)
	if(not Snapshots):
		raise RuntimeError("no fresh returned Codex limit event; do not extend freshness")
	Snapshot = max(Snapshots, key=lambda Item: datetime.fromisoformat(Item["captured_at"]))
	Quota = campaign / "control/quota.json"
	if(Quota.exists() and datetime.fromisoformat(R.read_json(Quota)["captured_at"]) > datetime.fromisoformat(Snapshot["captured_at"])):
		return dict(action="KEPT_NEWER_SNAPSHOT")
	R.persist(Quota, Snapshot)
	Log = campaign / "control/quota-source-events.jsonl"
	with Log.open("a", encoding="utf-8") as Stream:
		Stream.write(json.dumps(dict(observed_at=R.utc_now(), snapshot=Snapshot)) + "\n")
	return dict(action="REFRESHED_FROM_RETURNED_SERVICE_EVENT", captured_at=Snapshot["captured_at"],
		windows=Snapshot["windows"], stop_reason=R.quota_reason(Quota))


def main():
	Parser = argparse.ArgumentParser(description=__doc__)
	Parser.add_argument("--campaign", required=True, type=Path)
	Parser.add_argument("--base", required=True, type=Path)
	Parser.add_argument("--auth-source", default="/mnt/c/Users/HuangZY/.codex/auth.json", type=Path)
	Args = Parser.parse_args()
	try:
		print(json.dumps(refresh(Args.campaign, Args.base, Args.auth_source)))
	except (OSError, ValueError, KeyError, TypeError, RuntimeError) as Error:
		print(json.dumps(dict(action="NOT_REFRESHED", reason=str(Error))))
		raise SystemExit(1)


if(__name__ == "__main__"):
	main()

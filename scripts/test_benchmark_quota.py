"""Returned usage limits must keep their true timestamp and account binding."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
import tempfile
import unittest

import benchmark_quota as Q


class QuotaFeedTests(unittest.TestCase):
	def test_original_time_exhaustion_and_invalid_windows(self):
		Now = datetime.now(timezone.utc)
		Time = (Now-timedelta(seconds=119)).isoformat()
		Row = dict(type="event_msg", timestamp=Time, payload=dict(type="token_count", rate_limits=dict(
			limit_id="codex", primary=dict(window_minutes=10080, used_percent=100), secondary=None)))
		Data = Q.event_snapshot(Row, Path("event.jsonl"), 2, json.dumps(Row), Now)
		self.assertEqual(Data["captured_at"], Time)
		self.assertEqual(Data["windows"][0]["remaining_percent"], 0)
		self.assertIsNone(Q.event_snapshot(Row, Path("event.jsonl"), 2, "line", Now+timedelta(seconds=2)))
		for Value in [None, True, float("nan"), -1, 101]:
			Row["payload"]["rate_limits"]["primary"]["used_percent"] = Value
			self.assertIsNone(Q.event_snapshot(Row, Path("event.jsonl"), 2, "line", Now))
		Row["payload"]["rate_limits"]["primary"]["used_percent"] = 4
		Row["payload"]["rate_limits"]["limit_id"] = "codex_bengalfox"
		self.assertIsNone(Q.event_snapshot(Row, Path("event.jsonl"), 2, "line", Now))

	def test_different_account_cannot_refresh(self):
		with tempfile.TemporaryDirectory() as Directory:
			Root = Path(Directory)
			Base = Root / "q9/a"
			(Base / "home").mkdir(parents=True)
			Auth = Root / "desktop.json"
			Q.R.persist(Auth, dict(tokens=dict(account_id="synthetic-account-one")))
			Q.R.persist(Base / "home/auth.json", dict(tokens=dict(account_id="synthetic-account-two")))
			with self.assertRaises(RuntimeError):
				Q.refresh(Root, Base, Auth)
			self.assertFalse((Root / "control/quota.json").exists())


if(__name__ == "__main__"):
	unittest.main()

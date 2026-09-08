"""Ensure evidence tampering and unclosed audit PASS cannot be hidden."""

from pathlib import Path
import tempfile
import unittest

import benchmark_frontier_report as F


class FrontierReportTests(unittest.TestCase):
	def test_frozen_tampering_and_external_path_rejected(self):
		with tempfile.TemporaryDirectory() as Directory:
			Base = Path(Directory)
			Frozen = Base / "run/frozen-work"
			Frozen.mkdir(parents=True)
			File = Frozen / "answer.md"
			File.write_text("exact submitted proof")
			F.R.persist(Base / "run/state.json", dict(status="RETURNED_UNAUDITED"))
			F.R.persist(Base / "run/frozen-hashes.json", {"answer.md": F.R.file_hash(File)})
			self.assertEqual(F.frozen_checks(Base)["verdict"], "PASS")
			File.write_text("later repaired proof")
			with self.assertRaises(RuntimeError):
				F.frozen_checks(Base)
			F.R.persist(Base / "run/frozen-hashes.json", {"../../private.txt": "unused"})
			with self.assertRaises(RuntimeError):
				F.frozen_checks(Base)

	def test_high_score_cannot_override_open_root(self):
		Data = dict(verdict="INCONCLUSIVE", root_closed=False, target_status="PARTIAL",
			load_bearing_gaps=["unproved remaining domain"], total_score=90,
			scores=dict(correctness=40, fidelity=20, strict_progress=5, calibration=10, evidence=10, reproducibility=5))
		F.check_audit(Data)
		Data["verdict"] = "PASS"
		with self.assertRaises(RuntimeError):
			F.check_audit(Data)
		Data.update(root_closed=True, target_status="REFUTED", load_bearing_gaps=[], total_score=100)
		Data["scores"]["strict_progress"] = 15
		F.check_audit(Data)
		Data["total_score"] = 99
		with self.assertRaises(RuntimeError):
			F.check_audit(Data)


if(__name__ == "__main__"):
	unittest.main()

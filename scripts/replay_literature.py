#!/usr/bin/env python3
"""Exercise byte transport and source-bound notes on a previously downloaded paper.

This checks transport, not mathematical reading comprehension or PDF extraction fidelity.
"""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "plugins/manage-math-research-program/skills/manage-math-research-program/scripts"))
import research_library as library


def main():
	Parser = argparse.ArgumentParser(description=__doc__)
	for name in ("input", "text-file", "url", "version", "title", "output"):
		Parser.add_argument("--" + name, required=True)
	Args = Parser.parse_args()
	Project = Path(Args.output).resolve()
	Project.mkdir(parents=True, exist_ok=False)
	Source = library.capture_source(Project, Args.input, Args.url, Args.version, Args.title,
		Args.text_file, "pdftotext -layout -enc UTF-8")
	Again = library.capture_source(Project, Args.input, Args.url, Args.version, Args.title,
		Args.text_file, "pdftotext -layout -enc UTF-8")
	assert Source == Again
	Offset, Chunks, Reassembled = 0, 0, []
	while(Offset is not None):
		Passage = library.read_source(Project, Source["source_id"], MaxLines=80, StartOffset=Offset)
		assert len(Passage["content"]) <= 12000
		Reassembled.append(Passage["content"])
		Offset = Passage["next_offset"]
		Chunks += 1
	TextBytes = Path(Args.text_file).read_bytes()
	assert "".join(Reassembled).encode("utf-8") == TextBytes
	Card = Project / "tools/source-reading.md"
	Card.parent.mkdir()
	Card.write_text("---\ntitle: Source transport and extraction check\nkind: reading-note\nprovenance_maturity: LEAD\n---\n"
		f"# Reading lead\n\nSource: {Args.url}, {Args.version}.\n"
		"Byte transport checked only. Record pages actually inspected separately; transport does not certify formulas or applicability.\n",
		encoding="utf-8", newline="\n")
	ControlCount = sum(ord(Char) < 32 and Char not in "\n\r\t\f" for Char in TextBytes.decode("utf-8"))
	Note = library.annotate(Project, "tools/source-reading.md", library.digest(Card.read_bytes()),
		"maintenance-replay", "observation", "extracted text, control-character scan",
		f"Extraction contains {ControlCount} non-layout control characters. Consult original PDF before formula transcription; this is not a theorem audit.",
		Source["source_id"])
	library.make_index(Project, ["tools"], ReadmePath="tools/README.md")
	Hits = library.query_tools(Project, "transcription")
	assert len(Hits["hits"]) == 1
	assert Hits["hits"][0]["annotations"][0]["state"] == "CURRENT"
	Summary = dict(verdict="PASS", kind="REAL_PDF_TRANSPORT_AND_ANNOTATION", source=Source,
		runtime_sha256=library.digest(Path(library.__file__).read_bytes()),
		replay_script_sha256=library.digest(Path(__file__).read_bytes()),
		pdf_bytes=Path(Args.input).stat().st_size, extracted_bytes=len(TextBytes), chunks=Chunks,
		exact_reassembly=True, idempotent_capture=True, annotation_id=Note["annotation_id"],
		non_layout_control_characters=ControlCount, indexed_notes=1, model_calls_in_replay=0,
		limitation="Byte transport only; visual inspection, mathematical comprehension and formula fidelity are not certified by this script.")
	library.atomic_write(Project / "results.json", library.json_bytes(Summary))
	print(json.dumps(Summary, ensure_ascii=False))


if(__name__ == "__main__"):
	main()

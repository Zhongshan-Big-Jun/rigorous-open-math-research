# Implementation tracking: research map (研究地图)

Date: 2026-08-16
Scope: add a continuously updated, human-readable research map per project so
routes/methods, intermediate results, unexpected findings, failures, tools,
open directions, an avoid list, and human/other-agent contributions are always
collectible and readable; partial progress counts and agents avoid rabbit-holing.

## Features implemented

| # | Feature | Where |
| --- | --- | --- |
| 1 | `research_map.md` template (8 sections) | `manage-math-research-program/assets/research-map.template.md` |
| 2 | `update_research_map.py` maintenance script (init + append route/finding/failure/avoid/human) | `manage-math-research-program/scripts/update_research_map.py` |
| 3 | Manage workflow 8f: maintain the research map (mandatory) | manage SKILL.md |
| 4 | Evidence rule 16: research map is a maintained living document | manage SKILL.md |
| 5 | Stage A/B/C boundary updates the research map | `math-research-workflow` SKILL.md |
| 6 | Anti-rabbit-hole: read map routes/avoid list before deep-diving a sub-branch | `math-research-workflow` SKILL.md |
| 7 | `research_map.md` added to rigorous default artifacts + publish rule | `rigorous-open-math-research` SKILL.md |
| 8 | README (zh/en) + cachebusters + MANIFEST | repo docs + plugin.json |

## Verification performed

| Check | Result |
| --- | --- |
| `update_research_map.py` init in temp project | PASS |
| Append route/finding/failure/avoid/human in correct sections | PASS (after bug fix) |
| Parent `validate_all.py` (68 checks) | PASS |
| Parent smoke tests (7) | ALL PASS |
| Budget-state JSON parse (unchanged) | PASS (via validate_all) |

## Bugs found and fixed

1. **Section-matching bug in `update_research_map.py`**:
   - Symptom: appended entries created new duplicate unnumbered sections at the
     end instead of inserting into the numbered template sections (e.g.
     `## Routes and methods tried` instead of `## 2. Routes and methods tried`).
   - Root cause: `insert_after_section` matched exact `## <heading>` strings;
     the template used numbered headings (`## 2. ...`).
   - Fix: match a section whose displayed name **ends with** the requested
     heading (e.g. `## 2. Routes and methods tried` matches
     `Routes and methods tried`).
   - Verified: re-run in a fresh temp project shows all entries land in the
     correct sections and no duplicate headings.
2. **MANIFEST stale after script fix**:
   - Regenerated `MANIFEST.sha256` after the fix; validate_all re-passes.

## Notes

- The research map is intentionally human-readable prose/bullets/tables, not raw
  logs. The script is a helper; agents still maintain section quality.
- Human/other-agent contributions are treated as leads to verify, not proven
  facts, and are merged so future agents do not rediscover or over-optimize them
  too early.

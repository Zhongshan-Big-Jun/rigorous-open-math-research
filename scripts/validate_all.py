#!/usr/bin/env python3
"""Validate the math-research workflow-plugin repository layout.

Checks (stdlib only, no network):
  1. marketplace.json: top-level name + interface.displayName; every plugin entry
     has policy.installation / policy.authentication / category; source.path
     exists and its folder basename equals the plugin name.
  2. Every plugin: .codex-plugin/plugin.json has the required fields; the skills
     directory exists; every skill has a SKILL.md with name/description
     frontmatter; agents/openai.yaml (when present) is non-empty and declares
     interface/policy.
  3. MANIFEST.sha256 (when present in a skill dir) matches every listed file.
  4. Text files are UTF-8 without BOM.
  5. Strict parse: every JSON file parses after masking {{...}} template tokens
     (templates with placeholders are valid by design); every YAML file parses
     when PyYAML is installed (CI installs it; locally the check is skipped with a
     note if PyYAML is missing).

Usage:
    python scripts/validate_all.py [repo-root]

Exit code 0 when all checks pass, 1 otherwise.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import re

REQUIRED_PLUGIN_KEYS = frozenset(
    {"name", "version", "description", "author", "repository", "license", "skills", "interface"}
)
REQUIRED_INTERFACE_KEYS = frozenset(
    {"displayName", "shortDescription", "developerName", "category"}
)
REQUIRED_MARKETPLACE_ENTRY_KEYS = frozenset({"name", "source", "policy", "category"})
REQUIRED_POLICY_KEYS = frozenset({"installation", "authentication"})
ALLOWED_INSTALLATION = frozenset({"NOT_AVAILABLE", "AVAILABLE", "INSTALLED_BY_DEFAULT"})
ALLOWED_AUTHENTICATION = frozenset({"ON_INSTALL", "ON_USE"})
TEXT_SUFFIXES = frozenset(
    {".md", ".json", ".yaml", ".yml", ".txt", ".tex", ".lean", ".py", ".csv", ".svg", ".mmd"}
)
TEMPLATE_TOKEN_RE = re.compile(r"\{\{[^{}]+\}\}")


class Validator:
    def __init__(self, root: pathlib.Path) -> None:
        self.root = root
        self.errors: list[str] = []
        self.checks = 0

    def ok(self, message: str) -> None:
        self.checks += 1
        print(f"ok: {message}")

    def bad(self, message: str) -> None:
        self.checks += 1
        self.errors.append(message)
        print(f"FAIL: {message}")

    def check(self, condition: bool, message: str) -> None:
        if condition:
            self.ok(message)
        else:
            self.bad(message)

    def check_marketplace(self) -> None:
        path = self.root / ".agents" / "plugins" / "marketplace.json"
        self.check(path.is_file(), f"marketplace file exists: {path.relative_to(self.root)}")
        if not path.is_file():
            return
        data = json.loads(path.read_text(encoding="utf-8"))
        self.check(bool(data.get("name")), "marketplace has a top-level name")
        self.check(bool(data.get("interface", {}).get("displayName")), "marketplace has interface.displayName")
        plugins = data.get("plugins")
        self.check(isinstance(plugins, list) and len(plugins) > 0, "marketplace lists at least one plugin")
        for entry in plugins or []:
            name = entry.get("name", "<missing>")
            self.check(
                REQUIRED_MARKETPLACE_ENTRY_KEYS.issubset(entry.keys()),
                f"marketplace entry '{name}' has name/source/policy/category",
            )
            policy = entry.get("policy", {})
            self.check(
                REQUIRED_POLICY_KEYS.issubset(policy.keys()),
                f"marketplace entry '{name}' has policy.installation/authentication",
            )
            self.check(
                policy.get("installation") in ALLOWED_INSTALLATION,
                f"marketplace entry '{name}' installation is an allowed value",
            )
            self.check(
                policy.get("authentication") in ALLOWED_AUTHENTICATION,
                f"marketplace entry '{name}' authentication is an allowed value",
            )
            rel = (entry.get("source", {}) or {}).get("path", "")
            plugin_dir = (self.root / rel).resolve() if rel else None
            self.check(
                plugin_dir is not None and plugin_dir.is_dir(),
                f"marketplace entry '{name}' source path exists: {rel}",
            )
            if plugin_dir is not None and plugin_dir.is_dir():
                self.check(plugin_dir.name == name, f"marketplace entry '{name}' folder basename matches")
                self.check_plugin(plugin_dir, name)

    def check_plugin(self, plugin_dir: pathlib.Path, name: str) -> None:
        manifest = plugin_dir / ".codex-plugin" / "plugin.json"
        self.check(manifest.is_file(), f"plugin '{name}' has .codex-plugin/plugin.json")
        if not manifest.is_file():
            return
        data = json.loads(manifest.read_text(encoding="utf-8"))
        self.check(data.get("name") == name, f"plugin '{name}' manifest name matches folder")
        self.check(
            REQUIRED_PLUGIN_KEYS.issubset(data.keys()),
            f"plugin '{name}' manifest has required fields",
        )
        interface = data.get("interface", {})
        self.check(
            REQUIRED_INTERFACE_KEYS.issubset(interface.keys()),
            f"plugin '{name}' interface has displayName/shortDescription/developerName/category",
        )
        skills_dir = plugin_dir / "skills"
        self.check(skills_dir.is_dir(), f"plugin '{name}' has skills/ dir")
        if skills_dir.is_dir():
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir():
                    self.check_skill(skill_dir)
        agents = plugin_dir / "agents" / "openai.yaml"
        if agents.exists():
            text = agents.read_text(encoding="utf-8")
            self.check(
                "interface:" in text and "policy:" in text and "allow_implicit_invocation:" in text,
                f"plugin '{name}' agents/openai.yaml has interface/policy",
            )

    def check_skill(self, skill_dir: pathlib.Path) -> None:
        skill_md = skill_dir / "SKILL.md"
        self.check(skill_md.is_file(), f"skill '{skill_dir.name}' has SKILL.md")
        if not skill_md.is_file():
            return
        lines = skill_md.read_text(encoding="utf-8").splitlines()
        self.check(len(lines) >= 3 and lines[0].strip() == "---", f"skill '{skill_dir.name}' frontmatter opens with ---")
        fm: list[str] = []
        closed = False
        for line in lines[1:]:
            if line.strip() == "---":
                closed = True
                break
            fm.append(line)
        if not closed:
            self.bad(f"skill '{skill_dir.name}' frontmatter never closes")
            return
        joined = "\n".join(fm)
        self.check(
            any(line.startswith("name:") for line in fm) and "description:" in joined,
            f"skill '{skill_dir.name}' frontmatter has name/description",
        )
        manifest = skill_dir / "MANIFEST.sha256"
        if manifest.exists():
            bad = 0
            for line in manifest.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                hexdigest, rel = line.split("  ", 1)
                target = skill_dir / rel
                # Normalize CRLF so MANIFEST hashes are valid in both a
                # Windows worktree (core.autocrlf) and a Linux checkout.
                data = target.read_bytes().replace(b"\r\n", b"\n") if target.exists() else b""
                if not target.exists() or hashlib.sha256(data).hexdigest() != hexdigest:
                    bad += 1
                    self.bad(f"skill '{skill_dir.name}' MANIFEST.sha256 mismatch: {rel}")
            if bad == 0:
                self.ok(f"skill '{skill_dir.name}' MANIFEST.sha256 matches")

    def check_utf8(self) -> None:
        bad = 0
        for p in self.root.rglob("*"):
            if not p.is_file() or ".git" in p.parts:
                continue
            if p.suffix.lower() not in TEXT_SUFFIXES:
                continue
            raw = p.read_bytes()
            if raw.startswith(b"\xef\xbb\xbf"):
                bad += 1
                self.bad(f"file has UTF-8 BOM: {p.relative_to(self.root)}")
            else:
                try:
                    raw.decode("utf-8")
                except UnicodeDecodeError:
                    bad += 1
                    self.bad(f"file is not valid UTF-8: {p.relative_to(self.root)}")
        if bad == 0:
            self.ok("all text files are UTF-8 without BOM")

    def check_structured(self) -> None:
        """Strict parse of YAML (when PyYAML is available) and template-aware JSON."""
        try:
            import yaml
        except ImportError:
            yaml = None
        bad_json = 0
        bad_yaml = 0
        json_checked = 0
        yaml_checked = 0
        for p in sorted(self.root.rglob("*")):
            if not p.is_file() or ".git" in p.parts:
                continue
            suffix = p.suffix.lower()
            if suffix == ".json":
                json_checked += 1
                text = p.read_text(encoding="utf-8")
                masked = TEMPLATE_TOKEN_RE.sub('0', text)
                try:
                    json.loads(masked)
                except json.JSONDecodeError as exc:
                    bad_json += 1
                    self.bad(f"JSON parse error (after masking {{{{...}}}} templates): {p.relative_to(self.root)}: {exc}")
            elif suffix in (".yaml", ".yml") and yaml is not None:
                yaml_checked += 1
                try:
                    yaml.safe_load(p.read_text(encoding="utf-8"))
                except Exception as exc:
                    bad_yaml += 1
                    self.bad(f"YAML parse error: {p.relative_to(self.root)}: {exc}")
        if yaml is None:
            print("note: PyYAML not installed; strict YAML parse skipped")
        if bad_json == 0:
            self.ok(f"all JSON files parse after masking {{{{...}}}} templates ({json_checked} files)")
        if yaml is not None and bad_yaml == 0:
            self.ok(f"all YAML files parse ({yaml_checked} files)")

    def run(self) -> int:
        print(f"Validating repository: {self.root}")
        self.check_marketplace()
        self.check_utf8()
        self.check_structured()
        if self.errors:
            print(f"\n{len(self.errors)} problem(s) found.")
            return 1
        print(f"\nAll checks passed ({self.checks} checks).")
        return 0


def main() -> int:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    return Validator(root).run()


if __name__ == "__main__":
    sys.exit(main())

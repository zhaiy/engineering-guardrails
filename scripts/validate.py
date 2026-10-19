#!/usr/bin/env python3
"""Check package structure and local documentation links, not agent quality."""

import re
from pathlib import Path

import yaml


def main():
    root = Path(__file__).resolve().parents[1]
    skill = root / "skills" / "engineering-guardrails"
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError("SKILL.md needs YAML frontmatter")
    meta = yaml.safe_load(parts[1])
    if not isinstance(meta, dict) or meta.get("name") != skill.name:
        raise ValueError("Skill name must match its directory")
    description = meta.get("description")
    if not isinstance(description, str) or not 1 <= len(description) <= 1024:
        raise ValueError("Skill description must be a non-empty string <= 1024 characters")
    if not parts[2].strip():
        raise ValueError("Skill body is empty")
    ui = yaml.safe_load((skill / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    if "$engineering-guardrails" not in ui["interface"]["default_prompt"]:
        raise ValueError("Default prompt must name the skill")
    if ui.get("policy", {}).get("allow_implicit_invocation", True) is not True:
        raise ValueError("This package promises normal automatic discovery")
    if (skill / "LICENSE").read_bytes() != (root / "LICENSE").read_bytes():
        raise ValueError("Installable skill must carry the repository's license")
    checked = 0
    for document in root.rglob("*.md"):
        if ".git" in document.parts or ".work" in document.parts:
            continue
        for target in re.findall(r"\[[^\]\n]*\]\(([^\s)]+)\)", document.read_text(encoding="utf-8")):
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            path = target.split("#", 1)[0]
            if path and not (document.parent / path).exists():
                raise ValueError(f"Broken local link in {document.relative_to(root)}: {target}")
            checked += 1
    print(f"Package valid; {checked} local links checked. Behavioral quality is evaluated separately.")


if __name__ == "__main__":
    main()

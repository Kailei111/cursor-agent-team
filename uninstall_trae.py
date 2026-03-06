#!/usr/bin/env python3
"""uninstall_trae.py - Uninstall cursor-agent-team files for TRAE.

Usage:
  python cursor-agent-team/uninstall_trae.py [--yes]
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys

_scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_scripts")
sys.path.insert(0, _scripts_dir)
import _install_utils as u  # type: ignore


def _is_dir_empty(path: str) -> bool:
    try:
        return not any(os.scandir(path))
    except FileNotFoundError:
        return True


def _remove_path(abs_path: str) -> bool:
    if not os.path.lexists(abs_path):
        return False
    try:
        if os.path.islink(abs_path) or os.path.isfile(abs_path):
            os.remove(abs_path)
            return True
        if os.path.isdir(abs_path):
            shutil.rmtree(abs_path)
            return True
        os.remove(abs_path)
        return True
    except OSError as e:
        u.colored_print(f"Error removing {abs_path}: {e}", "red")
        return False


def _try_rmdir_if_empty(abs_dir: str, removed_items: list[str], rel_label: str) -> None:
    if os.path.isdir(abs_dir) and _is_dir_empty(abs_dir):
        try:
            os.rmdir(abs_dir)
            removed_items.append(rel_label)
        except OSError:
            pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yes", action="store_true", help="Skip confirmation prompt")
    args = ap.parse_args()

    script_path = os.path.abspath(__file__)
    project_root = u.get_project_root(script_path)

    trae_root = os.path.join(project_root, ".trae")
    trae_rules = os.path.join(trae_root, "rules")
    trae_skills = os.path.join(trae_root, "skills")

    target_rule = os.path.join(trae_rules, "project_rules.md")

    # collect skill SKILL.md under .trae/skills/skill-*/SKILL.md
    skill_files: list[str] = []
    if os.path.isdir(trae_skills):
        try:
            for name in os.listdir(trae_skills):
                if not name.startswith("skill-"):
                    continue
                p = os.path.join(trae_skills, name, "SKILL.md")
                if os.path.isfile(p) or os.path.islink(p):
                    skill_files.append(p)
        except OSError:
            pass

    if not (os.path.lexists(target_rule) or skill_files):
        u.colored_print("TRAE framework files not found.", "yellow")
        print("Nothing to uninstall.")
        return 0

    print("=" * 42)
    print("TRAE AI Agent Team Framework Uninstaller")
    print("=" * 42)
    print()
    print("This will remove:")
    print("  - .trae/rules/project_rules.md")
    print("  - .trae/skills/skill-*/SKILL.md")
    print()

    if not args.yes:
        reply = input("Are you sure you want to uninstall? (y/n) ").strip().lower()
        if reply not in {"y", "yes"}:
            print("Uninstallation cancelled.")
            return 0

    removed: list[str] = []

    if _remove_path(target_rule):
        removed.append(".trae/rules/project_rules.md")

    for abs_skill in sorted(set(skill_files)):
        if _remove_path(abs_skill):
            rel = os.path.relpath(abs_skill, project_root)
            removed.append(rel)

        # remove skill directory if empty
        skill_dir = os.path.dirname(abs_skill)
        _try_rmdir_if_empty(skill_dir, removed, os.path.relpath(skill_dir, project_root) + "/")

    _try_rmdir_if_empty(trae_rules, removed, ".trae/rules/")
    _try_rmdir_if_empty(trae_skills, removed, ".trae/skills/")
    _try_rmdir_if_empty(trae_root, removed, ".trae/")

    print()
    print("=" * 42)
    u.colored_print("Uninstallation completed!", "green")
    print("=" * 42)
    print()
    print("Removed items:")
    if removed:
        for item in removed:
            print(f"  ✅ {item}")
    else:
        print("  (none)")
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


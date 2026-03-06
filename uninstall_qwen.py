#!/usr/bin/env python3
"""uninstall_qwen.py - Uninstall Cursor AI Agent Team Framework (Qwen Code).

Usage:
  python cursor-agent-team/uninstall_qwen.py [--yes] [--remove-submodule]
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys

_scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_scripts")
sys.path.insert(0, _scripts_dir)
import _install_utils as u  # type: ignore


SUBMODULE_NAME = "cursor-agent-team"
INSTALL_INFO_REL = os.path.join(".qwen", ".qwen-agent-team-installed")


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


def _run_git(project_root: str, args: list[str]) -> tuple[bool, str]:
    try:
        p = subprocess.run(
            ["git", *args],
            cwd=project_root,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return False, "git not found"
    out = (p.stdout or "").strip()
    err = (p.stderr or "").strip()
    if p.returncode != 0:
        return False, (err or out or f"git {' '.join(args)} failed")
    return True, (out or "ok")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yes", action="store_true", help="Skip confirmation prompt")
    ap.add_argument(
        "--remove-submodule",
        action="store_true",
        help="Explicitly remove the git submodule (default: keep it)",
    )
    args = ap.parse_args()

    script_path = os.path.abspath(__file__)
    project_root = u.get_project_root(script_path)

    install_info_path = os.path.join(project_root, INSTALL_INFO_REL)

    print("=" * 42)
    print("Qwen Code AI Agent Team Framework Uninstaller")
    print("=" * 42)
    print()

    if not os.path.isfile(install_info_path):
        u.colored_print("Framework not installed or installation info missing.", "yellow")
        print("Nothing to uninstall.")
        return 0

    try:
        with open(install_info_path, encoding="utf-8") as f:
            info = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        u.colored_print(f"Error reading install record: {e}", "red")
        return 1

    version = str(info.get("version", "unknown"))
    installed_at = str(info.get("installed_at", "unknown"))
    files = info.get("files", [])
    if not isinstance(files, list):
        files = []

    print("Found installation:")
    print(f"  Version: {version}")
    print(f"  Installed at: {installed_at}")
    print()

    print("This will remove installed Qwen Code files under .qwen/.")
    print("Note: QWEN.md will NOT be removed automatically (user-owned).")
    if args.remove_submodule:
        print("It will also attempt to remove the git submodule cursor-agent-team/.")
    else:
        print("It will NOT remove the git submodule unless you pass --remove-submodule.")
    print()

    if not args.yes:
        reply = input("Are you sure you want to uninstall? (y/n) ").strip().lower()
        if reply not in {"y", "yes"}:
            print("Uninstallation cancelled.")
            return 0

    removed: list[str] = []

    for rel in files:
        if not isinstance(rel, str) or not rel:
            continue
        if os.path.normpath(rel) == "QWEN.md":
            continue
        abs_path = os.path.join(project_root, rel)
        if _remove_path(abs_path):
            removed.append(rel)

    if _remove_path(install_info_path):
        removed.append(INSTALL_INFO_REL)

    _try_rmdir_if_empty(os.path.join(project_root, ".qwen", "commands"), removed, ".qwen/commands/")
    _try_rmdir_if_empty(os.path.join(project_root, ".qwen", "context"), removed, ".qwen/context/")
    _try_rmdir_if_empty(os.path.join(project_root, ".qwen"), removed, ".qwen/")

    qwen_md = os.path.join(project_root, "QWEN.md")
    if os.path.isfile(qwen_md):
        u.colored_print("Note: QWEN.md exists but was not removed.", "yellow")

    if args.remove_submodule:
        submodule_dir = os.path.join(project_root, SUBMODULE_NAME)
        had_dir = os.path.isdir(submodule_dir)
        ok, msg = _run_git(project_root, ["submodule", "deinit", "-f", SUBMODULE_NAME])
        if ok:
            removed.append("Submodule deinitialized")
        else:
            u.colored_print(f"Warning: {msg}", "yellow")

        ok, msg = _run_git(project_root, ["rm", "-f", SUBMODULE_NAME])
        if ok:
            removed.append("Submodule removed from Git index")
            if had_dir:
                removed.append(f"Submodule directory ({SUBMODULE_NAME}/)")
        else:
            u.colored_print(f"Warning: {msg}", "yellow")

        git_modules = os.path.join(project_root, ".git", "modules", SUBMODULE_NAME)
        if os.path.isdir(git_modules):
            if _remove_path(git_modules):
                removed.append("Git internal module configuration")

        if os.path.isdir(submodule_dir):
            if _remove_path(submodule_dir):
                removed.append(f"Submodule directory ({SUBMODULE_NAME}/)")

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

    if args.remove_submodule:
        print("Note: If the submodule was removed, don't forget to commit the changes in your project repo.")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


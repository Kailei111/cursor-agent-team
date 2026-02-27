#!/usr/bin/env python3
"""install_qwen.py - Install cursor-agent-team for Qwen Code (cross-platform).

Usage:
    python cursor-agent-team/install_qwen.py

Prerequisites:
    git submodule add https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_scripts"))
import _install_utils as u

SUBMODULE_NAME = "cursor-agent-team"

COMMAND_FILES = [
    ("_qwen/commands/discuss.toml", ".qwen/commands/discuss.toml"),
    ("_qwen/commands/prompt_engineer.toml", ".qwen/commands/prompt_engineer.toml"),
    ("_qwen/commands/crew.toml", ".qwen/commands/crew.toml"),
    ("_qwen/commands/spec_translator.toml", ".qwen/commands/spec_translator.toml"),
]

CONTEXT_FILES = [
    ("_qwen/context/discussion_assistant.md", ".qwen/context/discussion_assistant.md"),
    ("_qwen/context/prompt_engineer_assistant.md", ".qwen/context/prompt_engineer_assistant.md"),
    ("_qwen/context/crew_assistant.md", ".qwen/context/crew_assistant.md"),
    ("_qwen/context/spec_translator_assistant.md", ".qwen/context/spec_translator_assistant.md"),
]

QWEN_MD_CONTENT = """\
# Qwen Code Context

This file imports all context files from the cursor-agent-team framework.

@.qwen/context/discussion_assistant.md
@.qwen/context/crew_assistant.md
@.qwen/context/prompt_engineer_assistant.md
@.qwen/context/spec_translator_assistant.md
"""


def main():
    script_path = os.path.abspath(__file__)
    submodule_dir = u.get_submodule_dir(script_path)
    project_root = u.get_project_root(script_path)

    print("=" * 42)
    print("Qwen Code AI Agent Team Framework Installer")
    print("=" * 42)
    print()

    # Step 1: Environment check
    print("Step 1: Checking environment...")
    if not os.path.isdir(submodule_dir):
        u.colored_print(f"Error: Submodule not found at {submodule_dir}", "red")
        sys.exit(1)
    if not os.path.isdir(os.path.join(project_root, ".git")):
        u.colored_print("Warning: Not in a git repository. Continuing anyway...", "yellow")
    u.colored_print("✓ Environment check passed", "green")
    print()

    # Step 2: Create directories
    print("Step 2: Creating directory structure...")
    u.ensure_dir(os.path.join(project_root, ".qwen", "commands"))
    u.ensure_dir(os.path.join(project_root, ".qwen", "context"))
    u.colored_print("✓ Directories created", "green")
    print()

    # Step 3: Copy files
    print("Step 3: Copying files...")
    all_files = COMMAND_FILES + CONTEXT_FILES
    installed, failed = u.copy_files(all_files, submodule_dir, project_root)
    if failed:
        u.colored_print(f"Error: {len(failed)} file(s) failed to copy", "red")
        sys.exit(1)
    u.colored_print("✓ Files copied", "green")
    print()

    # Step 4: Create QWEN.md
    print("Step 4: Creating main QWEN.md file...")
    qwen_md_path = os.path.join(project_root, "QWEN.md")
    if not os.path.isfile(qwen_md_path):
        with open(qwen_md_path, "w", encoding="utf-8") as f:
            f.write(QWEN_MD_CONTENT)
        installed.append("QWEN.md")
        u.colored_print("✓ Created QWEN.md with import statements", "green")
    else:
        u.colored_print("QWEN.md already exists, skipping...", "yellow")
    print()

    # Step 5: Installation record
    print("Step 5: Recording installation information...")
    version = u.get_version(submodule_dir)
    info_path = os.path.join(project_root, ".qwen", ".qwen-agent-team-installed")
    u.write_install_info(info_path, version, "qwen-code", installed)
    u.colored_print("✓ Installation information recorded", "green")
    print()

    # Step 6: Update .gitignore
    print("Step 6: Updating .gitignore...")
    u.update_gitignore(project_root, SUBMODULE_NAME)
    print()

    # Summary
    print("=" * 42)
    u.colored_print("Installation completed successfully!", "green")
    print("=" * 42)
    print()
    print("Installed items:")
    for item in installed:
        print(f"  ✅ {item}")
    print()
    print(f"Version: {version}")
    print()
    print("You can now use the following commands in Qwen Code:")
    print("  /discuss - Discussion partner")
    print("  /prompt_engineer - Prompt engineer")
    print("  /crew - Crew member")
    print("  /spec_translator - Spec-Kit translator")
    print()
    print(f"Note: The workspace at {SUBMODULE_NAME}/ai_workspace/ is SHARED")
    print("      between Cursor and Qwen Code platforms.")
    print()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""install_trae.py - Install cursor-agent-team for TRAE_CN (cross-platform).

Usage:
    python cursor-agent-team/install_trae.py

Prerequisites:
    git submodule add -f https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
"""

import glob
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_scripts"))
import _install_utils as u


def main():
    script_path = os.path.abspath(__file__)
    submodule_dir = u.get_submodule_dir(script_path)
    project_root = u.get_project_root(script_path)

    source_rules = os.path.join(submodule_dir, "_trae", "rules")
    source_skills = os.path.join(submodule_dir, "_trae", "skills")

    print("=== cursor-agent-team TRAE Installation ===")
    print()
    print(f"Project root: {project_root}")
    print(f"Source: {submodule_dir}/_trae/")
    print(f"Target: {os.path.join(project_root, '.trae')}/")
    print()

    if not os.path.isdir(source_rules) or not os.path.isdir(source_skills):
        u.colored_print("ERROR: Source _trae/ directory not found.", "red")
        sys.exit(1)

    # Step 1: Create directories
    print("[1/3] Creating .trae directories...")
    trae_rules = os.path.join(project_root, ".trae", "rules")
    trae_skills = os.path.join(project_root, ".trae", "skills")
    u.ensure_dir(trae_rules)
    u.ensure_dir(trae_skills)

    # Step 2: Copy project rules
    print("[2/3] Copying project rules...")
    src = os.path.join(source_rules, "project_rules.md")
    dst = os.path.join(trae_rules, "project_rules.md")
    u.copy_file(src, dst)
    print(f"  -> {dst}")

    # Step 3: Copy skills
    print("[3/3] Copying skills...")
    skill_dirs = sorted(glob.glob(os.path.join(source_skills, "skill-*")))
    for skill_dir in skill_dirs:
        if not os.path.isdir(skill_dir):
            continue
        skill_name = os.path.basename(skill_dir)
        skill_src = os.path.join(skill_dir, "SKILL.md")
        if not os.path.isfile(skill_src):
            continue
        skill_dst_dir = os.path.join(trae_skills, skill_name)
        u.ensure_dir(skill_dst_dir)
        skill_dst = os.path.join(skill_dst_dir, "SKILL.md")
        u.copy_file(skill_src, skill_dst)
        print(f"  -> {skill_dst}")

    print()
    print("=== Installation Complete ===")
    print()
    print("Files installed:")
    print(f"  Rules:  {os.path.join(trae_rules, 'project_rules.md')}")
    for skill_dir in skill_dirs:
        if os.path.isdir(skill_dir):
            skill_name = os.path.basename(skill_dir)
            print(f"  Skill:  {os.path.join(trae_skills, skill_name, 'SKILL.md')}")
    print()
    print("=== Manual Steps Required ===")
    print()
    print("You need to manually create 3 Agents in TRAE GUI (Settings -> Agent):")
    print()
    prompts_dir = os.path.join(submodule_dir, "_trae", "agent_prompts")
    print("  1. Discussion Partner (讨论搭档)")
    print(f"     Prompt: {os.path.join(prompts_dir, 'discussion_partner.md')}")
    print("     Tools:  File System, Terminal, Web Search")
    print()
    print("  2. Crew Member (执行组员)")
    print(f"     Prompt: {os.path.join(prompts_dir, 'crew_member.md')}")
    print("     Tools:  File System, Terminal, Web Search")
    print()
    print("  3. TRAE Prompt Engineer (提示工程师)")
    print(f"     Prompt: {os.path.join(prompts_dir, 'trae_prompt_engineer.md')}")
    print("     Tools:  File System, Terminal, Web Search")
    print()
    print("Copy each prompt file's full content into the corresponding Agent's prompt field.")
    print()
    print("Done! Use @讨论搭档, @执行组员, or @提示工程师 to start.")


if __name__ == "__main__":
    main()

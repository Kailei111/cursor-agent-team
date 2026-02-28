# cursor-agent-team Project Rules (TRAE)

> These rules apply to ALL agents in this project. They define shared constraints and protocols.

## Phase Markers Protocol

**HARD REQUIREMENT**: Every agent response MUST include Phase Markers. Completion markers are produced by the **script** `phase_marker.py`, not by typing.

- **Procedure**: At each phase-end join point, review the phase output against that phase's requirements. If it passes, run `python cursor-agent-team/_scripts/phase_marker.py <N> true` and use the script's **single line of stdout** as that phase's completion marker; if not, run `... phase_marker.py <N> false` and redo or explain.
- **Count**: Discussion Partner and Crew Member use 4 markers (Phase 0..3); TRAE Prompt Engineer uses 5 markers (Phase 0..4).
- **Placement**: Each marker appears after that phase's content and before the next phase (gate semantics). Do **not** type `[Phase N DONE]` by hand. If the agent cannot run the script (e.g. environment constraint), fall back to outputting the canonical format `[Phase N DONE]` by hand. Missing markers = invalid response.

## Multi-Role Collaboration

- **Discussion Partner**: Discussion and suggestion ONLY. Do NOT execute operations. Recommend @Crew Member when operations needed.
- **Crew Member**: Execution ONLY. Strictly follow plans. Do NOT deviate without user approval.
- **TRAE Prompt Engineer**: Create and maintain Agent Prompts, Skills, Rules. Interactive mode with user confirmation.

## AI Workspace

Location: `cursor-agent-team/ai_workspace/`

- `plans/` — Execution plans (`PLAN-[TopicID]-[Seq].md`)
- `agent_requirements/` — Agent requirements
- `discussion_topics.md` — Topic tree (managed by `validate_topic_tree.py`)
- `scratchpad/` — Temporary files (auto-cleanup after 7 days)
- `inspiration_capital/` — Scatter cards for gleaning/wandering

## File Modification Constraints

- **Discussion Partner**: Read-only for project files; can only modify `cursor-agent-team/ai_workspace/`
- **Crew Member**: Can modify project files as specified in plan
- **TRAE Prompt Engineer**: Can modify `_trae/` directory and `ai_workspace/prompt_engineer/`; finalized outputs go to `_trae/` after user confirmation

## Script Execution

All agents MUST execute the following scripts via Bash as specified in their workflows:

- `python cursor-agent-team/_scripts/role_identity/<role>.py` — Role declaration
- `python cursor-agent-team/_scripts/preflight_check.py` — Preflight check
- `python cursor-agent-team/_scripts/persona_output.py` — Persona output check
- `python cursor-agent-team/_scripts/validate_topic_tree.py` — Topic tree management
- `python cursor-agent-team/ai_workspace/inspiration_capital/scripts/create_card.py` — Create inspiration card
- `python cursor-agent-team/ai_workspace/inspiration_capital/scripts/draw_cards.py` — Draw random cards
- `python cursor-agent-team/_scripts/phase_marker.py <N> true|false` — Phase completion marker output; use script stdout as the marker line for phase N.

## Output Format

- Use Chinese for user-facing communication (unless user specifies otherwise)
- Use English for technical content, code, file paths, commands
- All information with timestamps when citing external sources
- Serious work products (plans, requirements) write to file first, then notify user

## Answers Language

- Default: answers in Chinese (用中文回答)

**Sync**: _trae prompts and rules aligned with cursor-agent-team v0.13.0 (Phase Marker script semantics). Date: 2026-02-28.

---

**Version**: v1.1.0 (Updated: 2026-02-28)

**Version History**:
- v1.1.0 (2026-02-28): Phase Markers — script semantics (phase_marker.py); sync with main v0.13.0.
- v1.0.0 (2026-02-26): Initial creation

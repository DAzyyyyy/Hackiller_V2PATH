# Coordination board

Each agent edits **only its own row** and its own lines under *Requests* and *Log*. Read `AI_HANDOFF.md` first.

## Status

| Agent | Branch | Current task | Status | Last commit | Blockers | Updated (ET) |
|---|---|---|---|---|---|---|
| AI-1 Evidence & Integration (Claude Code) | `evidence-pipeline` | A1–A5, C2, I1 | starting | — | — | 11:30 |
| AI-2 Context & Full text | `context-data` | B1–B5, C1 | not started | — | — | — |

## Checkpoints (ET)

- [ ] 12:00: contract files exist (even partial), pushed
- [ ] 12:30: A–C done, pushed
- [ ] 12:35: AI-1 merges `context-data` → `evidence-pipeline`, rebuilds site data
- [ ] 12:45: front end starts (AI-1); AI-2 does QA and pitch-number checks
- [ ] 13:45: feature freeze
- [ ] 14:15: copy to the official fork `projects/<team-name>/` (team name: _TBD_)
- [ ] 14:45: PR opened and Devpost link submitted

## Requests

Format: `- [from → to] what you need, and which file/field (time)`

## Log

Format: `- HH:MM [AI-x] what changed (commit)`

- 11:30 [AI-1] Created AI_HANDOFF.md and COORDINATION.md; created branch `context-data` for AI-2.

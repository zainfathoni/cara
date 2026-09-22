# Skill Simplification Follow-up

This records the 2026-09-11 ownership result for the GPT-6 Astra skill audit. It applies the guidance in [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) without making Cara a fork of provider- or upstream-owned skills.

## Cara-owned policy

`skills/update-upstream.sh` is the source of truth for Cara's release-pinned upstream selection. Before any cleanup or installation, it runs `skills/audit-skill-ownership.sh` against other Amp discovery roots. A tracked name backed by a competing copy, broken symlink, or different-target symlink stops the update because Cara cannot guarantee which body Amp will select. A symlink resolving to the exact authoritative skill is a valid alias and is preserved without conflict. The retired `write-a-skill` entry is reported but does not block unrelated updates. No case changes the inspected path.

This is intentionally an ownership gate, not an automatic cleanup rule. A directory outside Cara's selected install target can be hand-authored or managed by another installer. The owner must identify and remove or migrate it explicitly. Unrelated foreign skills, including HEY's provider-managed skill, remain untouched.

## Trigger acceptance examples

| Example request | Expected selection and behavior | Current result |
| --- | --- | --- |
| “Implement this approved spec using TDD.” | `tdd`; use the established interface and begin red → green without another planning approval. | The duplicate historical body was removed; the pinned upstream body is selected. Its remaining unconditional seam confirmation is blocked on upstream simplification. |
| “Add this tiny field from the approved ticket.” | Explicit `implement` only; verify at change-appropriate scope and do not add review or commit gates unless requested or required locally. | Selection is explicitly invoked, but the upstream body mandates full-suite review and commit. Blocked upstream. |
| “Create a skill for release notes.” | Amp `building-skills` for packaging and `writing-for-agents` for writing mechanics; no third automatic interview workflow. | The historical `write-a-skill` installation was removed, leaving the intended built-in and upstream skills. |
| “Show my HEY calendar tomorrow.” | `hey`; load calendar-specific detail while retaining shared account and authorization rules. | Correct provider selection, but the generated 811-line root loads every HEY workflow. Blocked on Basecamp router work. |

## Verified historical restoration

Before removal on 2026-09-12, complete path/type/mode/size/hash manifests and byte comparisons proved that both historical installations exactly matched [`mattpocock/skills@62f43a1`](https://github.com/mattpocock/skills/commit/62f43a18177be6ec82da242e59ffbc490a4c22ea):

| Removed installation | Repository restoration path | Exact Git tree |
| --- | --- | --- |
| `~/.config/agents/skills/tdd` | `skills/engineering/tdd` | `28d7822c112f22cf499099881856fdec07bc83a8` |
| `~/.config/agents/skills/write-a-skill` | `skills/productivity/write-a-skill` | `2f252b35aa238879afc5a230ac30343708dee0b3` |

To restore one, fetch that exact commit into a temporary clone and extract only its listed repository path. Before placing it, require both `[ ! -e "$target" ]` and `[ ! -L "$target" ]`; refuse restoration if either check fails so no existing installation, including a broken symlink, is overwritten. Force-add the extracted directory to a disposable Git index and require its subtree ID to equal the table before moving it into place. This tree comparison verifies every path, regular-file mode and byte, and symlink target, including hidden or extra entries.

Git does not restore local macOS metadata. The removed roots and files carried `com.apple.provenance`; ownership, creation/modification timestamps, and directory modes are also outside Git tree content. No ACLs or filesystem flags were present. Preserve those separately only when an exact filesystem-metadata replica is required; they are unnecessary for restoring the verified skill contents.

Post-removal filesystem verification found both historical paths absent, the read-only ownership audit clean, and `tdd` resolving to `~/.agents/skills/tdd`. Two `reload_skills` calls in the already-running removal thread nevertheless retained a stale `write-a-skill` registration whose reported base directory no longer exists. They also listed `tdd` twice because `~/.claude/skills` aliases the authoritative `~/.agents/skills` root, although loading `tdd` selected the intended body. Verify that a fresh thread omits `write-a-skill` before treating runtime discovery cleanup as complete; no additional installation was removed to work around in-process registry state.

## Source-owner requests

### `tdd` — mattpocock/skills

Authoritative source: [`mattpocock/skills`](https://github.com/mattpocock/skills/blob/v1.2.3/skills/engineering/tdd/SKILL.md). The historical 107-line body is also from Matt's repository, but is not the pinned version.

Request upstream:

- Treat an already-approved spec and established public interface as sufficient planning for TDD.
- Ask only when a consequential behavior, priority, interface, or test seam remains unresolved.
- Keep genuine user-requested red → green development and behavior-focused tests.
- Permit refactoring while green rather than assigning it unconditionally to a separate review workflow.

File at <https://github.com/mattpocock/skills/issues/new>. Cara should consume the result through a reviewed version bump, not an installed-file patch.

### `implement` — mattpocock/skills

Authoritative source: [`mattpocock/skills`](https://github.com/mattpocock/skills/blob/v1.2.3/skills/engineering/implement/SKILL.md).

Request upstream:

- Scale typechecking and test scope to the change and repository requirements.
- Always fix failures caused by the requested change and rerun affected checks.
- Run extra two-axis review and broader suites when risk, repository guidance, or the user calls for them, rather than on every task.
- Commit only when the invoking workflow or user requests it.

File at <https://github.com/mattpocock/skills/issues/new>. Cara will not create a local fork merely to override this itinerary.

### `write-a-skill` — historical mattpocock/skills installation

The removed 117-line body exactly matched Matt Pocock's historical `write-a-skill` at commit [`62f43a1`](https://github.com/mattpocock/skills/commit/62f43a18177be6ec82da242e59ffbc490a4c22ea). It was replaced by `writing-great-skills`, then by the pinned `writing-for-agents`; it is absent from Cara's allowlist and lock file.

The owner authorized removal from the non-authoritative discovery root after the complete upstream match was verified. Amp's built-in `building-skills` remains responsible for packaging and upstream `writing-for-agents` for writing guidance.

### `hey` — basecamp/hey-cli

Authoritative source: [`basecamp/hey-cli`](https://github.com/basecamp/hey-cli). The installed marker states that manual edits are overwritten on upgrade, and the signed `hey` binary embeds and installs the skill.

Request the HEY owner to keep the root `SKILL.md` as a short router containing shared authentication, account-selection, mutation, and output invariants, with email, contacts, calendar, todos, habits, time tracking, and journal command detail in task-specific references. Preserve provider restrictions and the current shared-data/publication boundaries. Cara must not copy or patch this generated skill.

File at <https://github.com/basecamp/hey-cli/issues/new>.

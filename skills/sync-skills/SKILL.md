---
name: sync-skills
description: Synchronizes and verifies Cara-owned and upstream skill installations. Use when explicitly asked to install, update, or audit agent skills across machines.
disable-model-invocation: true
---

# Sync Skills

Follow this process in order. Treat the repository scripts as authoritative whenever prose and implementation differ.

## 1. Locate and validate the repository

Resolve the Cara root in this order:

1. `$CARA_ROOT`, when set.
2. `~/Code/GitHub/zainfathoni/cara`.
3. A path supplied by the user.

Require readable executable files at `skills/update-upstream.sh` and `skills/install.sh`. If this skill is not installed yet on a new machine, follow [`BOOTSTRAP.md`](BOOTSTRAP.md).

**Complete when:** one root has both required scripts and its canonical path is recorded. Otherwise stop and report every lookup attempted.

## 2. Update the local skill source

Require a clean repository worktree, then fast-forward its checked-out branch from the configured upstream:

```bash
git -C "<ROOT>" status --short
git -C "<ROOT>" pull --ff-only
```

Preserve local changes and divergent history. If either is present, stop mutation and report the exact repository state rather than installing stale local skills.

**Complete when:** the worktree is clean, `git pull --ff-only` exits zero, and the checked-out commit equals its upstream branch.

## 3. Resolve upstream and local roots

Read both scripts from the updated checkout before running them. Resolve their paths using the current environment, including `HOME`, `AGENT_SKILLS_DIR`, `UPSTREAM_SKILLS_AGENTS`, `XDG_CONFIG_HOME`, `CLAUDE_CONFIG_DIR`, `CODEX_HOME`, and `XDG_STATE_HOME`. Distinguish the canonical upstream root, every configured agent destination, the local install root, and the global lock file. Preserve script defaults when overrides are absent.

**Complete when:** every destination, discovery root, and lock path used by this run is listed as an absolute path and every configured agent is accepted by the upstream script.

## 4. Update upstream skills

Run, without changing its environment or logic:

```bash
"<ROOT>/skills/update-upstream.sh"
```

The script's own order is binding: read-only ownership audit, deprecated/blocked cleanup, release-pinned upstream package install, invocation/pointer/provenance checks, then separately sourced installs and their checks. Preserve every path reported by the ownership audit. A competing copy or broken/different-target link stops mutation until the owner chooses which installation to retain; an exact alias is accepted, and a retired overlap is a non-blocking ownership warning.

**Complete when:** the script exits zero and none of its checks report an error. A nonzero exit is a discrepancy; continue only with read-only verification so the final report captures the full state.

## 5. Install local skills

Run:

```bash
"<ROOT>/skills/install.sh"
```

Allow the script to replace symlinks. If it refuses a real directory, preserve that directory and record the refusal exactly.

**Complete when:** the installer exits zero. On failure, continue only with read-only verification.

## 6. Derive expectations and verify exhaustively

Derive expectations fresh from `update-upstream.sh`, `install.sh`, and the repository filesystem; never copy their inventories into this skill.

1. Extract every active upstream, separately sourced, deprecated, and blocked skill from the script's arrays, plus configured agent destinations, package provenance, required installed files, and lock-file assertions from its executable checks.
2. Derive the selected local skills by running `skills/install.sh --list`; do not infer that every Cara-owned source should be globally installed.
3. At every destination where the scripts install upstream skills, verify each expected skill exists and resolves to a directory containing `SKILL.md`. Require each validation helper and required reference encoded by the upstream script to pass, including relative context pointers, Codex sidecars, invocation parity, and lock assertions.
4. Check every deprecated and blocked name across the canonical upstream root, local root, every configured agent root, and the explicit fallback roots used by the script. Count broken symlinks as present discrepancies.
5. In the local root, verify every selected local skill is a symlink, is not broken, and its fully resolved target equals that skill's canonical repository directory. Enumerate the root to report extra skill symlinks, wrong targets, missing links, broken links, and real directories occupying expected names. Treat unselected entries as preserved inventory, not discrepancies, unless they are broken Cara-owned links left by a migration.

**Complete when:** every derived item has an explicit expected-versus-actual result, every relevant root has been enumerated (including overlapping roots), all symlink targets have been resolved, and no check was skipped.

## 7. Report

Report `Sync complete` only when the repository fast-forwarded or was already current, both scripts exited zero, and every verification passed. Include counts for upstream, deprecated, and local skills and state that discrepancies are none.

Otherwise report `Sync incomplete`, followed by every discrepancy as an exact path or command, expected state, and actual state, including script exit failures. Never claim completion from partial checks.

**Complete when:** the report names exactly one overall state, includes every required count, and accounts for every script result and verification discrepancy.

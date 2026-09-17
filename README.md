# Cara

My ways of working with coding agents.

## What This Provides

- `setup/init.sh` - a plan-then-apply setup script for shared agent docs and labels.
- `setup/github-blockers.sh` - audits, syncs, and checks real GitHub blocked-by relationships.
- `setup/templates/*` - repo-local issue-tracker, triage, domain, and agent-instruction templates.
- `skills/*` - reusable personal skills that can be installed globally by symlink.

## Workflow Contract

Planning and triage are maintainer-initiated steps. `/prototype` is model-invoked so `/wayfinder` can use it directly.

- `/to-spec` creates spec issues.
- `/to-tickets` breaks a spec into tracer-bullet tickets with blocking edges.
- `/wayfinder` plans large work as a shared map of decision tickets on the issue tracker, resolved one at a time.
- `/prototype` answers one unclear logic or UI question with throwaway code, then retains that primary source outside main. Model-invoked so `/wayfinder` can use it directly.
- `/handoff` carries context to another harness, directory, colleague, or side task when continuing in place is not possible.
- `/triage` evaluates readiness and applies triage labels.

GitHub's issue dependency graph is the canonical blocker source. Markdown
`Blocked by:` lines are documentation and must not replace real dependency
relationships.

Reference: [Skills Changelog v1.2: /wait-what, /writing-for-agents, Claude Code Plugin, and more](https://www.aihero.dev/skills/skills-changelog-v12-wait-what-writing-for-agents-claude-code-plugin-and-more).

## Set Up A Repository

From the target repository:

```bash
~/Code/GitHub/zainfathoni/cara/setup/init.sh
```

To apply without the interactive confirmation:

```bash
~/Code/GitHub/zainfathoni/cara/setup/init.sh --yes
```

The script creates or updates repo-local issue-tracker, triage-label, and domain
docs, updates the agent-instruction skills block, and creates missing canonical
labels. It does not create execution-loop entrypoints.

## Blocked-by Relationships

Markdown `Blocked by: #123` lines are documentation only. GitHub's real issue dependency graph is the canonical blocker source. Use the helper to audit or repair repositories where markdown blockers may not have matching GitHub relationships:

```bash
~/Code/GitHub/zainfathoni/cara/setup/github-blockers.sh audit --repo OWNER/REPO --state all
~/Code/GitHub/zainfathoni/cara/setup/github-blockers.sh sync --repo OWNER/REPO --state all
```

Check whether one issue has open real blockers with:

```bash
~/Code/GitHub/zainfathoni/cara/setup/github-blockers.sh check-issue --repo OWNER/REPO --issue 168
```

## Repository Docs

Each configured repository should commit:

- `docs/agents/issue-tracker.md`
- `docs/agents/triage-labels.md`
- `docs/agents/domain.md`

These files adapt global skills to the local repository. They are not an issue tracker or backlog.

## Install Shared Skills

After cloning this repo, bootstrap the `/sync-skills` skill once:

```bash
~/Code/GitHub/zainfathoni/cara/skills/install.sh
```

Then invoke `/sync-skills` for all future updates and audits. It fast-forwards this repository, runs both scripts below, cleans up deprecated skills, and verifies the installation.

For manual control or troubleshooting, the underlying scripts are:

```bash
~/Code/GitHub/zainfathoni/cara/skills/update-upstream.sh
~/Code/GitHub/zainfathoni/cara/skills/install.sh
```

`skills/update-upstream.sh` installs a release-pinned allowlist of upstream-tracked skills, including `shadcn/improve`, `firewalker06/tycho`, and `typesafe-ai/skills`, and intentionally excludes local-owned `teach`, so pulling this repo does not depend on a human remembering which upstream skills are safe to update. Upstream `wizard` remains blocked pending local file/repository mutation hardening.

By default this symlinks the small global selection documented in
[`skills/README.md`](skills/README.md) into `~/.agents/skills`. Pass skill names
to install an explicit project-local or optional selection, and set
`AGENT_SKILLS_DIR` to install somewhere else.

Upstream skills are installed for Amp, Claude Code, and Codex by default. Set `UPSTREAM_SKILLS_AGENTS` to a space-separated subset when a machine needs fewer targets.

## Script Safety

This repo uses [destructive_command_guard](https://github.com/Dicklesworthstone/destructive_command_guard) scan config in `.dcg/hooks.toml` and CI in `.github/workflows/dcg-scan.yml` to catch destructive commands added to setup scripts, skill scripts, and workflows.

For local checks, install `dcg` through machine configuration when possible (for example, the `nix-home` Home Manager setup tracked in [nix-home#3](https://github.com/zainfathoni/nix-home/issues/3)) and run:

```bash
dcg scan --paths setup/ skills/ .github/workflows/ --fail-on error
```

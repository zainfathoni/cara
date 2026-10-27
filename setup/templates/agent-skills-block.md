## Agent skills

### Issue tracker

Issues live as GitHub issues in `{{REPO}}`. See `docs/agents/issue-tracker.md`.

### Triage labels

Canonical skills labels are mapped in `docs/agents/triage-labels.md`.

### Planning and prototypes

Use `/wayfinder` for large planning tasks that exceed one agent session — it charts a shared map of investigation tickets on the issue tracker. Use `/prototype` for throwaway spikes before committing ambiguous UI, state-machine, or integration decisions to issues; it is model-invoked so `/wayfinder` can use it directly. Use `/handoff` when a long planning, debugging, or prototyping session should continue in a fresh agent context.

### PR review dispatch

Use Cara's `team-review` for an initial PR review and `self-review` to save pending findings. Before review work, load the named skill and follow `skills/team-review/SETUP.md` in the Cara source checkout. If a named skill is unavailable, locate and read its source through the configured skill paths or known Cara checkout; if it remains unavailable, stop and report the discovery gap. Skill names are not saved prompt names. Amp's built-in `Review` prompt and generic `review` or `code-review` installations are not substitutes. If the user explicitly selects one of those workflows, report the conflict with Cara's review contract before proceeding.

### Domain docs

Domain documentation and ADR lookup rules are described in `docs/agents/domain.md`.

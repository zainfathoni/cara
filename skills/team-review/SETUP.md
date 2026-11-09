# Review Setup

Use this contract before an initial PR review in `team-review`, or when `self-review` needs new findings. Keep setup and the initial review in the thread that received the review request.

## 1. Load the requested skill

Use the skill tool for the exact skill name. If it is absent, inspect the active skill list and source paths, then the configured local discovery roots and known Cara checkout (including an attached repository). Resolve symlinks and read the source `SKILL.md` and its required references. An empty shared-skill search does not prove that a local skill is absent.

If the source is readable but not registered, follow that source and report the discovery gap. If it cannot be found, stop the review and report the missing name and searched locations. A skill name is not a saved prompt: do not send it to `load_prompt` or invent a replacement workflow. Amp's built-in `Review` prompt and other `review` or `code-review` skills are separate workflows, not aliases for Cara skills.

**Complete when:** the requested skill and required references have been read from an identified source. Otherwise, report a skill-discovery blocker before reviewing or delegating.

## 2. Establish repository access

Read repository and environment guidance for credential routes. Inspect available environment variable **names only** (for example, `compgen -e` in Bash); never print tokens, dump secret files, enable shell tracing, or use authentication debug output. Test read access to the exact repository and PR, not only a public repository or the account endpoint.

A failed default credential or a private-repository 404 is not proof that the source is unavailable. Check the documented alternatives already available for that repository. GitHub CLI gives `GH_TOKEN` precedence over `GITHUB_TOKEN` and saved credentials; enterprise hosts use their enterprise variables. Use command-scoped overrides. For example, only when repository guidance identifies `BTA_GITHUB_TOKEN` as the intended credential:

```bash
GH_TOKEN="$BTA_GITHUB_TOKEN" gh api repos/OWNER/REPO/pulls/NUMBER --jq '{number, head: .head.sha, base: .base.sha}'
GH_TOKEN="$BTA_GITHUB_TOKEN" gh api user --jq .login
```

To test a documented saved account on github.com, use `env -u GH_TOKEN -u GITHUB_TOKEN gh ...` for that command only. Use the verified credential route consistently for metadata, Git fetch, and later review operations. For HTTPS Git, a command-local `-c credential.helper= -c 'credential.helper=!gh auth git-credential'` can use the same scoped environment without changing saved helpers. Keep tokens out of remote URLs and command arguments. Do not run `gh auth login`, `gh auth switch`, or `gh auth setup-git` to replace saved account state as a workaround.

**Complete when:** the exact PR is readable and the authenticated login is known. Otherwise, report which documented routes were tested by name and which access is missing. Keep initial-review ownership here; an access failure is not permission to create a runner reviewer.

## 3. Check out the exact PR head

Record the canonical repository, PR number, head repository and branch, full head SHA, base branch, and full base SHA from fresh PR metadata. Use the current thread's attached checkout so Amp can show its changes. Check `git status --porcelain=v1 --untracked-files=all`, the current branch, and local commits before changing refs.

- If there are unrelated staged, unstaged, or untracked changes, stop before checkout. Preserve them and report the blocking paths. Do not stash, reset, clean, force checkout, or move the initial review to a child thread. Ask for a safe checkout location if this thread cannot use the current one.
- In a clean checkout, automatically run `gh pr checkout NUMBER --repo OWNER/REPO`. Preserve existing local branches and commits: if the target branch already exists, use an unused local review branch with `--branch` rather than reset it. Record its mapping to the PR head branch. Never use `--force`.
- Fetch the recorded base revision with the verified credential route. Compare `git rev-parse HEAD` with the recorded full head SHA. Resolve `git merge-base BASE_SHA HEAD`, then inspect `git diff BASE_SHA...HEAD`. Fetch missing history if needed; a missing merge base is not an empty diff.
- Re-read PR metadata after checkout. If head or base changed, repeat setup against the new revisions before reviewing. A checkout command's zero exit, a matching branch name, `gh pr diff`, a downloaded patch, or `git apply --check` alone is not proof of exact-head checkout.

**Complete when:** this thread's attached checkout has the verified PR head at `HEAD`, the recorded base comparison resolves, and the worktree is clean. Report the local branch, head SHA, base SHA, and diff summary. If the ref is inaccessible or only a patch is available, report incomplete checkout; do not claim a completed initial review or save new findings from a substitute revision.

## 4. Keep initial review and second opinions distinct

Do the initial review yourself in this thread. Do not replace it with child-thread or subagent aggregation. A generic skill that requires parallel initial reviewers does not satisfy this contract.

Record the known models used for the original work and initial findings; effort labels such as `medium` and `high` do not identify those models. Honor an explicit user model choice; disclose if it repeats an originating model. Otherwise, offer Claude Code with Opus 5.5. If Opus is unavailable or was involved, offer Astra, then Sol if Astra is unavailable or already involved. Skip models already involved. If provenance is unknown or no different model is available, state that limit with the proposed choices rather than claiming cross-model independence, and ask the user to choose.

Resolve available named-model routes before starting. Verify the configured model through thread creation/status or the consultant's report; report any mismatch or unverified provider identity. Report the selected model and any fallback. An explicit second-opinion request authorizes this model selection, not automatic consultation on every review.

Use a separate reviewer thread only for a requested second opinion. Preserve its scope. Give it the reviewed revisions and a way to obtain the exact code; a branch name or commit ID alone does not transfer local work. That reviewer must verify its own checkout or state its evidence limits. Keep the initial checkout here and assess its findings against the same revision before combining results.

Reuse a suitable same-PR consultant only when its model also meets the selection above. For a new consultant, use a safe existing application checkout as the thread's working directory and verify its ownership before use. Require the consultant to verify the reviewed revision from its checkout or transferred snapshot, and state any evidence limits. Follow repository executor rules. If no suitable location is available, ask for a location decision; do not create an unnecessary worktree or start at a parent directory containing unrelated repositories.

**Complete when:** initial-review ownership remains here, and every second opinion has explicit user intent, identified revisions, and stated evidence limits. For revision checks before saving, pending-review identity, concurrent edits, and submission, follow `self-review`; setup does not authorize publication.

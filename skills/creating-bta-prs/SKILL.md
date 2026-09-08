---
name: creating-bta-prs
description: Prepares focused BookThatApp branches and pull requests. Use when asked to turn an existing BTA issue worktree into a GitHub PR.
---

# Creating BTA PRs

Turn an existing BTA issue worktree into one focused, convention-following branch and, when explicitly authorized, a GitHub pull request.

## Safety contract

- Anchor every Git command to the resolved worktree and leave unrelated changes untouched.
- Treat push, PR creation, draft/ready toggles, metadata writes, and review requests as shared mutations. Perform only the actions explicitly requested.
- Never infer that a branch is safe to rename, overwrite an existing local or remote branch, invent PR metadata, or claim a check ran when it did not.
- Assign an authorized new PR to the authenticated user and apply the evidenced `bug`, `feature`, or `chore` label. Ask when classification is ambiguous.
- Keep review submission and teammate review requests separate from PR creation. Do not request `unrooty` without explicit approval.

## Workflow

Use the [operational reference](REFERENCE.md) for commands, completion gates, and reporting evidence. Follow only the sections needed by the request, in order:

1. Establish the target, requested outcome, current status, and mutation authority.
2. Derive the branch convention from actual local and remote names; stop on collisions.
3. Review, stage, validate, and commit only intended paths.
4. If PR creation is authorized, discover repository metadata and fill its PR template with observed facts.
5. Push and create the PR only within that authorization.
6. Apply and verify standard BTA assignee and issue-type metadata.
7. Trigger missing stacked-PR CI only when explicitly authorized and safe for current review state.
8. Request external review only after separate explicit approval.
9. Verify and report final local and GitHub state.

The task is complete only when the reference’s gate for every attempted section passes, or the exact partial state and blocker are reported.

---
name: managing-dev-environments
description: Prepares, checks, and releases development runtimes and task-owned browser sessions. Use for development-runtime setup, read-only status, or explicitly authorized runtime/browser teardown.
---

# Managing Development Environments

Manage the runtime around a development task. Here, **release** means relinquish runtime and browser resources, not deploy software.

## 1. Establish scope and ownership

Read the repository's agent guidance and environment contract, plus lifecycle commands and troubleshooting docs needed for the requested resources. Inspect the command implementation before executing it. Keep repository-specific hosts, Compose names, authentication rules, and recovery procedures in those docs rather than copying them into this skill.

Resolve the requested operation: setup, status, or release. Status is read-only. Evidence collection alone does not authorize shutdown of a shared stack; carry forward an explicit setup/teardown instruction without asking again. Ask before uncovered shared-resource changes, deployments, data deletion, or authentication changes.

Inspect and record the following for resource types present and relevant to the request; container, worker, and mount checks apply only when those resources exist:

- Exact repository/worktree, revision and dirty state, target environment, and intended browser surface.
- Existing runtime services, actual source mounts (including workers), ports, and persistent volumes.
- Host-side servers such as Storybook or Vite, with their owning task and service/process identity.
- Task-owned browser pages or isolated profiles, and any other active consumers of the runtime.
- Which resources predated this task, which it creates, and which must remain running.

A worktree is not proof of runtime isolation. Before switching source or stopping services, check their shared resources; for Compose, include project identity, databases, volumes, ports, and mounts. If ownership or another consumer's need is unresolved, inspect safely and ask before disrupting it.

**Complete when:** the operation, allowed effects, resource ownership, and lifecycle commands needed for the requested resource types are known. For status-only requests, report the inventory and stop here.

## 2. Prepare and verify (setup only)

Reuse a healthy runtime serving the intended source. Otherwise run the documented startup command within the authorized scope, from the exact workdir and with the correct project configuration. Preserve existing data and unrelated services.

For a bind, dependency, or readiness failure, follow the repository's bounded recovery procedure. Obtain approval for any uncovered network or shared-service impact. Record prior state before temporary changes, restore it even if startup fails, and verify restoration. Do not introduce a second database/runtime or reset volumes as a convenient workaround.

Verify the actual source path (including application and worker mounts where present), revision/dirty changes, service health, and browser-visible asset readiness. Check the exact route and access context; a running container or HTTP 200 alone does not prove the candidate is ready. Keep component previews, full local application composition, and externally embedded storefronts as distinct surfaces. Leave login/MFA to the user unless applicable guidance and explicit authorization permit otherwise.

**Complete when:** the intended surface serves the intended source with working required services, or a specific blocker is reported. Return readiness or the blocker to the calling workflow. If browser evidence is in scope, continue with `/pr-e2e-evidence` only after readiness is verified; runtime readiness is not E2E proof.

## 3. Release and verify (release only)

Re-inspect live resources before mutation, especially when resuming after another thread or task. Use prior task records to identify ownership, not stale process or browser-page IDs.

Perform only actions for resources included in the authorized release scope. Skip absent or out-of-scope resource types; they are not cleanup blockers.

1. Preserve required evidence and identify remaining task-created fixtures/settings. Restore only changes covered by the cleanup authorization; report anything requiring separate data or external-action approval.
2. Run the repo's non-destructive shutdown command for the authorized stack. Preserve persistent volumes and unrelated stacks. Inspect its effects first: a command named `down` is not automatically safe. Never substitute destroy, volume removal, or global pruning for ordinary release.
3. Account separately for host-side servers: Compose shutdown does not stop Storybook or other host processes. Stop only resources included in the release scope, using their supported service control or exact owned process mechanism. Follow the executor tool's stopping constraints; do not misuse a hung-process kill tool for a healthy long-running server. Report a remaining process if no permitted stop mechanism is available.
4. List browser pages and close only task-owned pages included in the release scope. If the browser tool requires one page to remain and that last page is in scope, navigate it to `about:blank`. Preserve unrelated tabs, shared Chrome, and the shared DevTools connection. Quit a dedicated task-owned browser/profile only when its ownership and release scope are established.
5. Independently verify the scoped stack is stopped (and containers removed when the command promises removal), persistent volumes remain, scoped host servers are stopped, and scoped task pages are closed or blank. Verify temporary network changes are restored. Do not require a shared port to be globally unused when another legitimate service owns it.

**Complete when:** each scoped resource is verified released or explicitly reported as retained/blocked, with its reason. Partial cleanup is not a successful full release.

## 4. Report

Report the operation and outcome, exact runtime/workdir, source readiness for setup, services stopped or retained for release, persistent-data preservation, browser state, and any remaining host processes or blockers. Distinguish browser-page cleanup from terminating a browser or disconnecting DevTools. Never describe runtime shutdown as a deployment.

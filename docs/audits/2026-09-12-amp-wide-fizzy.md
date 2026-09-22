# Amp-wide Fizzy rollout

Owner scope: all Amp projects through personal hosted skills and user-level secrets. Red Alert operates on Work; Wheeljack operates on other boards. Cara owns the shared runtime. The earlier Amux project-local hook approach is superseded. Its introduced hooks and files have been removed from Amux, whose worktree is now clean; the prototype is archived under `~/.local/state/fizzy-upgrade-20260912/amux-prototype/`.

## Provisioned

- Amp user-level secrets `FIZZY_REDALERT_TOKEN` and `FIZZY_WHEELJACK_TOKEN` were saved through stdin from the existing trusted local credential source. Values were not printed or placed in arguments, files, repositories, or prompts. Both names and secret kinds were read back from Amp metadata.
- Live Fizzy identity checks verified Red Alert as `03fj2nej4tfeyw5paunpl06i3` and Wheeljack as `03fipgbrb5fhrokehz4plyjht`, both in account `6104728`. The Red Alert ID in older fleet scripts was stale; the heartbeat check now uses the verified ID.
- A fresh [Cara Orb](https://ampcode.com/threads/T-01a09453-2a74-723c-8589-2ec7453a58c5) verified that both user-level secrets are injected, with no project-specific secret setup. Its personal-skills checkout is `/home/user/workspace/fizzy-user-skills`; Thread Creator signing is configured as `Zain Fathoni <zain.fathoni@gmail.com>` via `amp-sign-commit`.

## Shared mechanism

The personal hosted skill carries the pinned installer and scoped command runner. Installation happens on demand from skill files, not repository setup/resume hooks. Each upstream invocation uses isolated config state, a fixed account/HTTPS endpoint, one selected credential, and actor validation. Card/board operations verify board scope before mutation. Secrets are runtime-only.

- Work board `03fj2n6bhaen2sq6jb9zs1eon` → Red Alert.
- Other accessible boards → Wheeljack.
- Mixed requests are split by board/scope; the current Amp project does not choose the actor.
- The runtime enforces JSON envelopes and supports a bounded documented command set. Unsupported operations fail rather than falling back to a raw mutation.

## Live local validation

- Work scope: correct Red Alert actor, one visible Work board, seven open cards, existing-card read, opposite-scope rejection.
- Personal scope: correct Wheeljack actor, four visible non-Work boards, Projects card listing, Work-board rejection.
- Red Alert standalone self-check: six assigned open cards; heartbeat read succeeds.

Wheeljack currently has access to Autobots, Career, Homeschooling, and Projects. Family, Finance, and Studio exclude Wheeljack. The routing rule applies to all non-Work boards, but it does not grant missing Fizzy permissions. A separate owner question is pending about those three existing access restrictions; publication does not depend on changing them.

## Delivery status

The Cara runtime passed 20 tests, including real CLI loopback checks and both live identities. The reviewed 14-file hosted payload has ZIP SHA-256 `d51adadd2ddb8f486d02378156f8ec185200b6b4e4b5c11c722e4313acd031c4`. Published to personal hosted skills `main` at commit `2c5faed5cfd5de32789bce5fb49473a7ce0fb749`. The remote accepted the Amp SSH-signed commit; independent local fetch confirmed its embedded signature and all 14 file contents match the reviewed archive. The publishing Linux Orb passed both identities, board filtering, Work card 430 read, personal closed card 334 read, and personal-to-Work rejection. A fresh [Homeschooling Orb](https://ampcode.com/threads/T-01a09470-b661-7790-bab5-77a3ba2092aa) started after publication passed automatic global discovery and live operation without copied source or project hooks. Its repository remained clean. It loaded `/home/user/.cache/amp/global-skills/ampcode.com/user/fizzy@966c71218189d25b`, received both user secrets, installed the initially absent Linux binary on demand, and passed archive/executable hash and exact-version checks. Work identity/list returned the expected actor, one Work board and seven open cards; personal identity/list returned Wheeljack and four non-Work boards; Projects open-card list succeeded with zero cards; personal access to Work was rejected. Final installer `--check` succeeded. A separate [Fleet Orb](https://ampcode.com/threads/T-01a0946b-92d9-719b-a55b-1276a6b4fb25) also loaded the global cache and passed the same live route checks. No per-project Amp settings need modification.

## Sources

- [Amp global plugins and skills](https://ampcode.com/news/global-plugins-and-skills)
- [Hosted personal skill workflow](https://ampcode.com/docs/customize/global-plugins-and-skills)
- [User-level Orb secrets](https://ampcode.com/docs/orbs/handling-secrets)
- [Documented Orb CLI execution](https://ampcode.com/docs/cli/spawning-orbs)
- [Fizzy board access model](https://github.com/basecamp/fizzy/blob/main/docs/api/sections/boards.md)

## Operational notes

- Publication is complete in [personal hosted skills](https://ampcode.com/git/@zainfathoni/-/skills); start a new Amp thread to load the published skill reliably.
- Cara and OpenClaw source changes remain local and uncommitted. The hosted skill itself is durably committed and pushed.
- No board memberships changed. Family, Finance and Studio remain unavailable to Wheeljack until the owner chooses to grant access.
- Native Orb smoke tests were read-only. Local CLI upgrade validation separately completed a temporary-card create/edit/comment/step/status lifecycle and deleted its test card.
- Amp file transfer requires an existing destination parent directory; uploading to the workspace root succeeded. CLI continuations sent during an active Orb turn did not appear in its transcript; native `send_thread_message` successfully delivered the recovery instruction.

## Final HQ reconciliation

Both managed implementation agents are terminal and succeeded: Cara completed two runs; the superseded Amux prototype completed three. Fleet’s final independent global-skill verification passed, including the exact Linux executable digest and a clean project worktree. No implementation agent remains active.

Correction to the Fleet agent narrative: its first capture parser tried to parse `boundary.json` from stdout even though scoped runtime rejection envelopes are emitted on stderr. The published runner’s installer does not print a first-install status line. The corrected capture combined the streams and verified the rejection. This was a verification-harness error, not a runtime installation defect. Consumers should inspect the exit status and parse success JSON from stdout or failure JSON from stderr.

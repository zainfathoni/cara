# Fizzy runtime and upgrades

Cara owns the Fizzy skill because it adds relationship-link, HTML-preservation, account-context, and read-after-write rules. Upstream owns the binary and command surface: [Fizzy CLI](https://github.com/basecamp/fizzy-cli). This skill and `setup/fizzy-wrapper.sh` are validated against **4.0.1**.

## macOS

Install the official `basecamp/tap/fizzy` Homebrew cask. When migrating from the old `fizzy-cli` formula, unlink that formula before installing the cask. Retain the old keg until smoke tests pass. Homebrew may require trusting the Basecamp tap before tapping it.

The local `~/.local/bin/fizzy` adapter is copied from `setup/fizzy-wrapper.sh`. It loads the working directory's direnv context, maps legacy `FIZZY_ACCOUNT` to `FIZZY_PROFILE` only when the latter is absent, and delegates directly to the Homebrew binary. `FIZZY_TOKEN` passes through unchanged. An explicitly empty token stops with exit 3 instead of falling back to personal saved credentials. The adapter requires direnv, including the existing Nix path fallback for restricted scheduler PATHs. The adapter checks the exact validated CLI version before dispatch, so a later package upgrade stops for a coordinated skill review.

Fizzy 4 converts Markdown itself; the adapter no longer invokes `fizzy-md`. Existing direct `fizzy-md` callers should move to `fizzy`, using `--description_file` / `--body_file` for file input. Explicit HTML remains Cara's convention for card descriptions.

## Preserve the local-owned skill on upgrades

Fizzy 4.0.1 automatically overwrites installed global `SKILL.md` files after the first successful command at a new version. It follows symlinks into source repositories. `fizzy skill install` also replaces customized instructions.

Before executing a newly installed CLI:

1. Back up the current adapter and review the Cara skill diff. Confirm the new binary using **`--version`**, whose Cobra flag bypasses the post-run refresh hook; the `version` subcommand does not.
2. Review upstream release notes and embedded skill in an isolated checkout. Port changed commands and schemas into Cara, preserving its local conventions.
3. Write the reviewed version (currently `4.0.1`) to `.last-run-version` beside the active global Fizzy config. The CLI prefers `~/.config/fizzy/config.yaml`, then `~/.fizzy/config.yaml`; if neither exists it uses `~/.config/fizzy/`. This is an upstream 4.0.1 sentinel, not a supported opt-out flag: recheck the source on future upgrades.
4. Update the validated version in this reference, `skills/fizzy/.installed-version`, and `setup/fizzy-wrapper.sh`. Install the adapter with `install -m 755 setup/fizzy-wrapper.sh ~/.local/bin/fizzy`, and the skill with `skills/install.sh fizzy`.
5. Run `fizzy doctor --json`, then the smoke test below. Confirm the Cara skill did not change after CLI execution. Remove the old keg only after dependent scripts have been migrated.

The `.installed-version` file records compatibility for `doctor`; it does not prevent auto-refresh. The version-checking adapter protects routine invocation after an unexpected binary upgrade. Direct binary and `fizzy-md` calls bypass that check.

## Credentials and Orbs

For Amp, use [Amp-wide identities](amp-wide.md): Red Alert operates on Work; Wheeljack operates on other boards. The personal hosted skill carries its installer and runner, and user-level Amp secrets supply both credentials. No project-specific hooks are needed.

The local macOS adapter retains the existing per-directory direnv mechanism for non-Amp consumers. In Amp, use the explicit scope runner so the chosen board determines the identity even when a repository's direnv configuration names another agent.

## Repeatable smoke tests

From the Cara checkout, choose a board accessible to the intended identity:

```bash
python3 setup/tests/fizzy-smoke.py --board BOARD_ID
```

This verifies identity, board/card reads, complete open/closed/postponed listings, and the JSON envelope. To explicitly test writes:

```bash
python3 setup/tests/fizzy-smoke.py --board BOARD_ID --write
```

The write test creates one uniquely marked card, checks native Markdown and HTML preservation, comments, steps, close/reopen, and filtered search, then deletes only that test card and verifies not-found. If interrupted before cleanup, use the printed card number and marker to identify the fixture; inspect it before deleting. Existing cards are only read. It does not test board migration, webhooks, or every account.

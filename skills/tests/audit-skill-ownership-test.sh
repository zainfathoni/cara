#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
AUDITOR="$SKILLS_ROOT/audit-skill-ownership.sh"
TMP_ROOT=$(mktemp -d)
trap 'rm -rf "$TMP_ROOT"' EXIT

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

authoritative_root="$TMP_ROOT/authoritative"
config_root="$TMP_ROOT/config"
compat_root="$TMP_ROOT/compat"
mkdir -p "$authoritative_root/tdd" "$authoritative_root/writing-for-agents"
mkdir -p "$config_root/foreign-skill" "$compat_root/hey"
printf 'preserve\n' > "$config_root/foreign-skill/marker"
printf 'managed by provider\n' > "$compat_root/hey/marker"
ln -s "$authoritative_root/tdd" "$compat_root/tdd"

roots="$config_root:$compat_root"
SKILL_DISCOVERY_ROOTS="$roots" "$AUDITOR" "$authoritative_root" tdd writing-for-agents >/dev/null
SKILL_DISCOVERY_ROOTS="$roots" "$AUDITOR" "$authoritative_root" tdd writing-for-agents >/dev/null
[ "$(cat "$config_root/foreign-skill/marker")" = preserve ] || fail "foreign skill changed"
[ "$(cat "$compat_root/hey/marker")" = 'managed by provider' ] || fail "provider-managed skill changed"
[ "$(readlink "$compat_root/tdd")" = "$authoritative_root/tdd" ] || fail "same-target alias changed"

mkdir -p "$config_root/tdd"
printf 'historical tdd\n' > "$config_root/tdd/marker"
if SKILL_DISCOVERY_ROOTS="$roots" "$AUDITOR" "$authoritative_root" tdd writing-for-agents >"$TMP_ROOT/duplicate.out" 2>&1; then
  fail "duplicate tracked skill was accepted"
fi
grep -F "Skill ownership conflict: $config_root/tdd" "$TMP_ROOT/duplicate.out" >/dev/null ||
  fail "duplicate report omitted the conflicting path"
grep -F "Authoritative source: $authoritative_root/tdd" "$TMP_ROOT/duplicate.out" >/dev/null ||
  fail "duplicate report omitted the authoritative source"
grep -F "Ownership audit found 1 conflict(s)" "$TMP_ROOT/duplicate.out" >/dev/null ||
  fail "same-target alias was counted as a conflict"
[ "$(cat "$config_root/tdd/marker")" = 'historical tdd' ] || fail "duplicate skill changed"

rm -r "$config_root/tdd"
ln -s "$TMP_ROOT/missing-tdd" "$config_root/tdd"
if SKILL_DISCOVERY_ROOTS="$roots" "$AUDITOR" "$authoritative_root" tdd writing-for-agents >/dev/null 2>&1; then
  fail "broken tracked-name symlink was accepted"
fi
rm "$config_root/tdd"
mkdir -p "$TMP_ROOT/different-tdd"
ln -s "$TMP_ROOT/different-tdd" "$config_root/tdd"
if SKILL_DISCOVERY_ROOTS="$roots" "$AUDITOR" "$authoritative_root" tdd writing-for-agents >/dev/null 2>&1; then
  fail "different-target tracked-name symlink was accepted"
fi
rm "$config_root/tdd"

mkdir -p "$config_root/write-a-skill"
printf 'historical writer\n' > "$config_root/write-a-skill/marker"
SKILL_DISCOVERY_ROOTS="$roots" "$AUDITOR" "$authoritative_root" tdd writing-for-agents >"$TMP_ROOT/retired.out" 2>&1 ||
  fail "preserved retired overlap blocked unrelated updates"
grep -F "Retired overlapping skill requires owner review: $config_root/write-a-skill" "$TMP_ROOT/retired.out" >/dev/null ||
  fail "retired overlap report omitted the installed path"
[ "$(cat "$config_root/write-a-skill/marker")" = 'historical writer' ] || fail "retired skill changed"

# Integration: update-upstream must audit before invoking any package manager.
fake_home="$TMP_ROOT/home"
fake_bin="$TMP_ROOT/bin"
mkdir -p "$fake_home/.config/agents/skills/tdd" "$fake_bin"
printf 'preserve duplicate\n' > "$fake_home/.config/agents/skills/tdd/marker"
cat > "$fake_bin/npx" <<EOF
#!/usr/bin/env bash
touch "$TMP_ROOT/npx-called"
EOF
chmod +x "$fake_bin/npx"
if HOME="$fake_home" XDG_CONFIG_HOME="$fake_home/.config" PATH="$fake_bin:$PATH" \
  UPSTREAM_SKILLS_AGENTS=amp "$SKILLS_ROOT/update-upstream.sh" >"$TMP_ROOT/update.out" 2>&1; then
  fail "upstream update continued through a tracked-name conflict"
fi
[ ! -e "$TMP_ROOT/npx-called" ] || fail "package manager ran before ownership audit"
[ "$(cat "$fake_home/.config/agents/skills/tdd/marker")" = 'preserve duplicate' ] ||
  fail "conflicting installation changed"

printf 'PASS: source selection, same-target alias, repeat audit, foreign preservation, conflicting copy/link, retired-overlap, and pre-mutation cases\n'

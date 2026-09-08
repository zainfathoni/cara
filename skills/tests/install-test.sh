#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
INSTALLER="$SKILLS_ROOT/install.sh"
TMP_ROOT=$(mktemp -d)
trap 'rm -rf "$TMP_ROOT"' EXIT

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

assert_link() {
  local name="$1"
  local target_root="$2"
  local link="$target_root/$name"

  [ -L "$link" ] || fail "$name was not installed as a symlink"
  [ "$(cd "$(dirname "$(readlink "$link")")" && pwd)/$(basename "$(readlink "$link")")" = "$SKILLS_ROOT/$name" ] ||
    fail "$name points at the wrong source"
}

default_root="$TMP_ROOT/default"
AGENT_SKILLS_DIR="$default_root" "$INSTALLER" >/dev/null

"$INSTALLER" --list | sort > "$TMP_ROOT/expected-defaults"
find "$default_root" -mindepth 1 -maxdepth 1 -type l -exec basename {} \; | sort > "$TMP_ROOT/actual-defaults"
diff -u "$TMP_ROOT/expected-defaults" "$TMP_ROOT/actual-defaults" || fail "default install did not match --list"
while IFS= read -r skill; do
  assert_link "$skill" "$default_root"
done < "$TMP_ROOT/expected-defaults"
[ ! -e "$default_root/checking-bta-dev-health" ] || fail "BTA-only skill was globally installed"
[ ! -e "$default_root/teach" ] || fail "optional skill was globally installed"

selected_root="$TMP_ROOT/selected"
mkdir -p "$selected_root"
foreign_source="$TMP_ROOT/foreign-source"
mkdir -p "$foreign_source"
ln -s "$foreign_source" "$selected_root/foreign-skill"
AGENT_SKILLS_DIR="$selected_root" "$INSTALLER" checking-bta-dev-health teach >/dev/null
assert_link checking-bta-dev-health "$selected_root"
assert_link teach "$selected_root"
[ "$(readlink "$selected_root/foreign-skill")" = "$foreign_source" ] || fail "foreign symlink was changed"

# A default sync must not restore every Cara source or remove explicit and
# foreign-owned selections that already exist in the same root.
AGENT_SKILLS_DIR="$selected_root" "$INSTALLER" >/dev/null
assert_link checking-bta-dev-health "$selected_root"
assert_link teach "$selected_root"
[ "$(readlink "$selected_root/foreign-skill")" = "$foreign_source" ] || fail "default sync changed foreign symlink"
[ ! -e "$selected_root/show-me" ] || fail "default sync restored an unselected skill"

if AGENT_SKILLS_DIR="$TMP_ROOT/unknown" "$INSTALLER" not-a-skill >/dev/null 2>&1; then
  fail "unknown skill was accepted"
fi

occupied_root="$TMP_ROOT/occupied"
mkdir -p "$occupied_root/fizzy"
if AGENT_SKILLS_DIR="$occupied_root" "$INSTALLER" fizzy >/dev/null 2>&1; then
  fail "real target directory was overwritten"
fi
[ -d "$occupied_root/fizzy" ] || fail "real target directory was removed"

traversal_root="$TMP_ROOT/custom"
traversal_sibling="$TMP_ROOT/skills"
traversal_source="$TMP_ROOT/traversal-source"
mkdir -p "$traversal_root" "$traversal_sibling" "$traversal_source"
ln -s "$traversal_source" "$traversal_sibling/fizzy"
if AGENT_SKILLS_DIR="$traversal_root" "$INSTALLER" ../skills/fizzy >/dev/null 2>&1; then
  fail "path-shaped skill selection was accepted"
fi
[ "$(readlink "$traversal_sibling/fizzy")" = "$traversal_source" ] ||
  fail "path-shaped selection changed a target outside the install root"

printf 'PASS: default, explicit, foreign-owned, unknown, and occupied-target installation cases\n'

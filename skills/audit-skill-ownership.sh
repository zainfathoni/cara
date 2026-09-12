#!/usr/bin/env bash
# Report skill-name conflicts without changing any installation.

set -euo pipefail

if [ "$#" -lt 2 ]; then
  printf 'Usage: skills/audit-skill-ownership.sh AUTHORITATIVE_ROOT SKILL...\n' >&2
  exit 2
fi

authoritative_root="$1"
shift
tracked_skills=("$@")

if [ "${SKILL_DISCOVERY_ROOTS+x}" = x ]; then
  discovery_roots_value=$SKILL_DISCOVERY_ROOTS
else
  discovery_roots_value="${XDG_CONFIG_HOME:-$HOME/.config}/agents/skills:${XDG_CONFIG_HOME:-$HOME/.config}/amp/skills"
fi

canonical_path() {
  local path="$1"

  if [ -d "$path" ]; then
    (cd "$path" && pwd -P)
  else
    printf '%s\n' "$path"
  fi
}

authoritative_path=$(canonical_path "$authoritative_root")
conflicts=0
warnings=0
old_ifs=$IFS
IFS=:
read -r -a discovery_roots <<< "$discovery_roots_value"
IFS=$old_ifs

for root in ${discovery_roots[@]+"${discovery_roots[@]}"}; do
  [ -n "$root" ] || continue
  [ "$(canonical_path "$root")" != "$authoritative_path" ] || continue

  for skill in "${tracked_skills[@]}"; do
    target="$root/$skill"
    if [ -e "$target" ] || [ -L "$target" ]; then
      authoritative_target=$(canonical_path "$authoritative_root/$skill")
      if [ -L "$target" ] && [ "$(canonical_path "$target")" = "$authoritative_target" ]; then
        continue
      fi

      printf 'Skill ownership conflict: %s\n' "$target" >&2
      printf '  Authoritative source: %s/%s\n' "$authoritative_root" "$skill" >&2
      conflicts=$((conflicts + 1))
    fi
  done

  # write-a-skill is a retired Matt Pocock skill whose broad trigger overlaps
  # its writing-for-agents successor and Amp's built-in building-skills skill.
  # Its provenance may predate the lock file, so preserve it for owner review.
  retired_target="$root/write-a-skill"
  if [ -e "$retired_target" ] || [ -L "$retired_target" ]; then
    printf 'Retired overlapping skill requires owner review: %s\n' "$retired_target" >&2
    printf '  Successor: %s/writing-for-agents\n' "$authoritative_root" >&2
    warnings=$((warnings + 1))
  fi
done

if [ "$conflicts" -ne 0 ]; then
  printf 'Ownership audit found %s conflict(s); no files were changed.\n' "$conflicts" >&2
  exit 1
fi

printf 'Skill ownership audit passed: %s tracked skill(s), %s preserved retired overlap(s), no conflicting tracked names.\n' "${#tracked_skills[@]}" "$warnings"

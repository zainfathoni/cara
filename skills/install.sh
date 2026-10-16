#!/usr/bin/env bash
# Symlink an explicit selection of Cara-owned skills into an agent skills directory.

set -euo pipefail

SKILLS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_ROOT=${AGENT_SKILLS_DIR:-$HOME/.agents/skills}

# Keep the default deliberately small. Project-specific and occasional skills
# remain available by passing their names as arguments.
DEFAULT_SKILLS=(
  fizzy
  log-fleet
  managing-dev-environments
  pr-e2e-evidence
  review-address
  review-clear
  review-verify
  self-review
  sync-skills
  team-review
  team-review-resolve
)

# Retired local-owned skills. Remove only exact-source links or marked managed
# copies; leave other similarly named installations untouched.
RETIRED_LOCAL_SKILLS=(
  tycho-video-explainer
)

usage() {
  printf 'Usage: skills/install.sh [--list] [SKILL...]\n'
  printf '\n'
  printf 'With no SKILL arguments, installs the default global selection.\n'
  printf 'Pass skill names to install only that explicit selection.\n'
  printf -- '--list prints the selected names without changing the target.\n'
  printf '\n'
  printf 'Environment:\n'
  printf '  AGENT_SKILLS_DIR   default: ~/.agents/skills\n'
}

list_only=false
case "${1:-}" in
  -h|--help)
    usage
    exit 0
    ;;
  --list)
    list_only=true
    shift
    ;;
esac

if [ "$#" -eq 0 ]; then
  selected_skills=("${DEFAULT_SKILLS[@]}")
else
  selected_skills=("$@")
fi

validated_skills=()
for skill_name in "${selected_skills[@]}"; do
  case "$skill_name" in
    ''|.|..|*/*)
      printf 'Skill selection must be a single directory name: %s\n' "$skill_name" >&2
      exit 1
      ;;
  esac

  for previous_skill in ${validated_skills[@]+"${validated_skills[@]}"}; do
    if [ "$skill_name" = "$previous_skill" ]; then
      printf 'Duplicate skill selection: %s\n' "$skill_name" >&2
      exit 1
    fi
  done
  validated_skills+=("$skill_name")

  if [ ! -f "$SKILLS_ROOT/$skill_name/SKILL.md" ]; then
    printf 'Unknown Cara skill: %s\n' "$skill_name" >&2
    exit 1
  fi
done

if [ "$list_only" = true ]; then
  printf '%s\n' "${selected_skills[@]}"
  exit 0
fi

mkdir -p "$TARGET_ROOT"

for skill_name in "${RETIRED_LOCAL_SKILLS[@]}"; do
  target="$TARGET_ROOT/$skill_name"
  source="$SKILLS_ROOT/$skill_name"
  if [ -L "$target" ] && [ "$(readlink "$target")" = "$source" ]; then
    rm -- "$target"
    printf 'Removed retired Cara skill link: %s\n' "$target"
  elif [ -d "$target" ] &&
    [ ! -L "$target" ] &&
    [ -f "$target/.amp-installed-skill" ] &&
    [ ! -L "$target/.amp-installed-skill" ] &&
    [ -f "$target/SKILL.md" ] &&
    grep -Fxq "name: $skill_name" "$target/SKILL.md"; then
    rm -r -- "$target"
    printf 'Removed retired Cara skill copy: %s\n' "$target"
  fi
done

for skill_name in "${selected_skills[@]}"; do
  if [ "$skill_name" = log-fleet ] &&
    [ -L "$TARGET_ROOT/log-notes" ] &&
    [ "$(readlink "$TARGET_ROOT/log-notes")" = "$SKILLS_ROOT/log-notes" ]; then
    rm "$TARGET_ROOT/log-notes"
    printf 'Removed renamed skill link: %s\n' "$TARGET_ROOT/log-notes"
  fi
done

installed=0

for skill_name in "${selected_skills[@]}"; do
  skill_dir="$SKILLS_ROOT/$skill_name"

  target="$TARGET_ROOT/$skill_name"

  if [ -L "$target" ]; then
    rm "$target"
  elif [ -e "$target" ]; then
    printf 'Refusing to overwrite non-symlink skill target: %s\n' "$target" >&2
    printf 'Move it aside or remove it, then rerun the installer.\n' >&2
    exit 1
  fi

  ln -s "$skill_dir" "$target"
  printf 'Installed %s -> %s\n' "$skill_name" "$skill_dir"
  installed=$((installed + 1))
done

printf 'Installed %s Cara skill(s) into %s\n' "$installed" "$TARGET_ROOT"

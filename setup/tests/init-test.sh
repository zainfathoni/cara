#!/usr/bin/env bash

set -euo pipefail

SETUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_ROOT=$(mktemp -d)
trap 'rm -rf "$TMP_ROOT"' EXIT

workspace="$TMP_ROOT/project"
fake_bin="$TMP_ROOT/bin"
mkdir -p "$workspace" "$fake_bin"
git -C "$workspace" init --quiet
printf '# Existing instructions\n' > "$workspace/AGENTS.md"

cat > "$fake_bin/gh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
case "$1 $2" in
  'auth status') exit 0 ;;
  'repo view')
    if [ "${3:-}" = '--json' ]; then
      printf 'owner/project\n'
    else
      printf 'main\n'
    fi
    ;;
  'label list')
    printf '%s\n' bug enhancement needs-triage ready-for-agent-triage needs-info ready-for-agent ready-for-human wontfix
    ;;
  *) printf 'Unexpected gh invocation: %s\n' "$*" >&2; exit 1 ;;
esac
SH
chmod +x "$fake_bin/gh"

PATH="$fake_bin:$PATH" "$SETUP_DIR/init.sh" --yes --workspace "$workspace" >/dev/null

test -f "$workspace/docs/agents/issue-tracker.md"
test -f "$workspace/docs/agents/triage-labels.md"
test -f "$workspace/docs/agents/domain.md"
test ! -e "$workspace/docs/agents/ralph.md"
test ! -e "$workspace/ralph.sh"
test ! -e "$workspace/PROMPT.md"
test ! -e "$workspace/.ralph"
grep -q 'Issues live as GitHub issues in `owner/project`' "$workspace/AGENTS.md"
if rg -n 'Ralph|ralph' "$workspace/AGENTS.md" "$workspace/docs/agents" >/dev/null; then
  printf 'Retired Ralph guidance was generated\n' >&2
  exit 1
fi

printf 'PASS: setup generates shared docs and labels without Ralph entrypoints\n'

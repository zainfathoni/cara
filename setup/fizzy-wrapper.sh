#!/bin/sh
# Local macOS adapter. Orbs use the upstream Linux binary and injected env directly.
set -eu

fizzy_binary=/opt/homebrew/bin/fizzy
if [ ! -x "$fizzy_binary" ]; then
  fizzy_binary=/usr/local/bin/fizzy
fi
if [ ! -x "$fizzy_binary" ]; then
  echo 'Install basecamp/tap/fizzy before using the Cara adapter.' >&2
  exit 1
fi
# --version is Cobra's flag: unlike the version subcommand, it has no post-run hook.
if [ "$("$fizzy_binary" --version)" != 'fizzy version 4.0.1' ]; then
  echo 'Fizzy version changed. Review and upgrade the Cara skill and adapter together.' >&2
  exit 1
fi

fizzy_dispatch='
  set -eu
  if [ "${FIZZY_TOKEN+x}" = x ] && [ -z "$FIZZY_TOKEN" ]; then
    echo "FIZZY_TOKEN is empty in this context; load the intended agent credential before calling Fizzy." >&2
    exit 3
  fi
  if [ -z "${FIZZY_PROFILE:-}" ] && [ -n "${FIZZY_ACCOUNT:-}" ]; then
    export FIZZY_PROFILE="$FIZZY_ACCOUNT"
  fi
  unset FIZZY_ACCOUNT
  exec "$@"
'
fizzy_direnv=$(command -v direnv || true)
if [ -z "$fizzy_direnv" ] && [ -x /etc/profiles/per-user/zain/bin/direnv ]; then
  fizzy_direnv=/etc/profiles/per-user/zain/bin/direnv
fi
if [ -z "$fizzy_direnv" ]; then
  echo 'The local Fizzy adapter requires direnv to select the intended identity.' >&2
  exit 3
fi
exec "$fizzy_direnv" exec "$PWD" sh -c "$fizzy_dispatch" fizzy "$fizzy_binary" "$@"

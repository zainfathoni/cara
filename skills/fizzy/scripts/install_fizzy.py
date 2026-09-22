#!/usr/bin/env python3
"""Install/check the private Linux pin or locate existing macOS Homebrew Fizzy."""

import argparse
import sys

sys.dont_write_bytecode = True
from fizzy_runtime import RuntimeErrorSafe, ensure_binary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify only; never download")
    args = parser.parse_args()
    try:
        print(ensure_binary(check=args.check))
        return 0
    except RuntimeErrorSafe as error:
        print(str(error), file=sys.stderr)
        return 1
    except OSError:
        print("Cannot access the Fizzy installation.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

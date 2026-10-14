#!/usr/bin/env bash
# NoseClicker AI Runner script (Linux & macOS)

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

if command -v python3 >/dev/null 2>&1; then
    exec python3 main.py "$@"
elif command -v python >/dev/null 2>&1; then
    exec python main.py "$@"
else
    python3 main.py "$@" || python main.py "$@"
fi

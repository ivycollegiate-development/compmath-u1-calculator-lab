#!/usr/bin/env bash
# setup.sh — verify you're in the right place, then clone or pull YOUR repo.
# Run this once per lab, at the START of every session, from your home directory.
#
#   bash setup.sh [folder-name]
#
# Optional argument: the local folder name to clone into. Defaults to the
# repo name. Use it when your lesson says to clone into a specific folder,
# e.g.  bash setup.sh compmath-lab
#
# It refuses to do anything unless your current directory is your home directory.
# Cloning into the wrong folder scatters your work where you can't find it.

set -euo pipefail

REPO="compmath-u1-calculator-lab"   # <- the lesson script rewrites this line
FOLDER="${1:-}"

die() { printf '\n[STOP] %s\n\n' "$1" >&2; exit 1; }

# ---- 1. Verify we are in the home directory -----------------------------------
HOME_DIR="$(cd ~ && pwd)"
CWD="$(pwd)"

if [ "$CWD" != "$HOME_DIR" ]; then
  die "You are in $CWD
     You must run this from your home directory ($HOME_DIR).
     Fix it with:  cd ~"
fi

printf 'Location OK: %s\n' "$CWD"
printf 'Your userid: %s\n\n' "$(whoami)"

# ---- 2. Work out your own repo name ------------------------------------------
# Repo names are <base>-<userid>_student : dash before the userid, underscore
# before "student". $(whoami) inserts your userid, so this is the same for everyone.
MY_REPO="${REPO}-$(whoami)_student"
[ -n "$FOLDER" ] || FOLDER="$MY_REPO"
DIR="$HOME_DIR/$FOLDER"
URL="https://github.com/ivycollegiate-development/${MY_REPO}.git"

# ---- 3. Clone if missing, otherwise pull -------------------------------------
if [ -d "$DIR/.git" ]; then
  printf 'Repo found: %s\n' "$DIR"
  printf 'Pulling any changes I pushed since last class...\n\n'
  cd "$DIR"
  git config pull.rebase false
  git pull
  printf '\n[OK] You are up to date. Open the files and start working.\n'
else
  printf 'Repo not found yet. Cloning it now...\n\n'
  printf '  %s\n\n' "$URL"
  # git clone names the folder after the URL, so pass the folder explicitly
  git clone "$URL" "$FOLDER" || die "Clone failed.
     If it asked for a username/password: use your GitHub username and a
     Personal Access Token (PAT) — never your GitHub password.
     If it says repository not found, check the exact URL in your lesson."

  cd "$DIR"
  printf '\n[OK] Cloned into %s\n' "$DIR"
fi

# ---- 4. Prove we landed in the right place -----------------------------------
ACTUAL="$(basename "$(pwd)")"
[ "$ACTUAL" = "$FOLDER" ] || die "Wrong folder: you are in $(pwd), expected $FOLDER"

git config pull.rebase false
printf '[OK] Verified: %s\n' "$ACTUAL"
printf '     Remote: %s\n' "$(git remote get-url origin)"
printf '\nOpen a file in the editor:  code .\n'

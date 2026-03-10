#!/bin/bash
# deploy.sh — copy a downloaded file into the AIStudio repo, commit, push,
#             and sync the run environment.
#
# Usage:
#   ./deploy.sh <source_file> <repo_destination> "<commit_message>"
#
# Examples:
#   ./deploy.sh ~/Downloads/api.py src/local_llm_bot/app/api.py "fix: corpus create endpoint"
#   ./deploy.sh ~/Downloads/dependencies.md docs/dependencies.md "docs: add dependencies rationale"
#   ./deploy.sh ~/Downloads/README.md README.md "docs: update README for alpha"
#
# What it does:
#   1. Copies the downloaded file to the correct location in ~/code/AIStudio
#   2. Stages the file with git add
#   3. Commits with your message
#   4. Pushes to GitHub
#   5. Pulls the change into ~/Developer/AIStudio (your run environment)

# ─── Argument validation ────────────────────────────────────────────────────

# $# = number of arguments passed to the script
# If not exactly 3 arguments, print usage instructions and exit
if [ "$#" -ne 3 ]; then
    echo "Usage: ./deploy.sh <source_file> <repo_destination> \"<commit_message>\""
    echo ""
    echo "Examples:"
    echo "  ./deploy.sh ~/Downloads/api.py src/local_llm_bot/app/api.py \"fix: corpus create\""
    echo "  ./deploy.sh ~/Downloads/dependencies.md docs/dependencies.md \"docs: add dependencies\""
    exit 1
    # exit 1 = exit with error code 1 (non-zero = something went wrong)
fi

# Assign the three arguments to named variables for readability
# $1, $2, $3 = first, second, third argument
SOURCE=$1
DEST=$2
MESSAGE=$3

# ─── Config ─────────────────────────────────────────────────────────────────

DEV_REPO=~/code/AIStudio        # where you develop and commit
RUN_REPO=~/Developer/AIStudio   # where you run and test

# ─── Step 1: Copy the file ──────────────────────────────────────────────────

echo "→ Copying $SOURCE to $DEV_REPO/$DEST"

# dirname = extract the folder path from a full file path
# e.g. dirname "docs/dependencies.md" returns "docs"
# mkdir -p creates the folder if it doesn't exist yet
mkdir -p "$DEV_REPO/$(dirname $DEST)"

# cp = copy. -f = force overwrite if file already exists
cp -f "$SOURCE" "$DEV_REPO/$DEST"

# Check if the copy succeeded ($? = exit code of last command, 0 = success)
if [ $? -ne 0 ]; then
    echo "✗ Copy failed. Does the source file exist?"
    exit 1
fi

# ─── Step 2: Commit and push from dev repo ──────────────────────────────────

echo "→ Committing and pushing from $DEV_REPO"

# cd = change directory into the dev repo
cd "$DEV_REPO"

# git add = stage the specific file for commit
git add "$DEST"

# git commit -m = commit with the message you passed as argument 3
git commit -m "$MESSAGE"

# git push = send the commit to GitHub
git push

if [ $? -ne 0 ]; then
    echo "✗ Push failed. Try: cd $DEV_REPO && git pull --rebase && git push"
    exit 1
fi

# ─── Step 3: Sync the run environment ───────────────────────────────────────

echo "→ Syncing $RUN_REPO"

cd "$RUN_REPO"

# git pull --rebase = fetch from GitHub and replay any local commits on top
# keeps history linear, correct default for solo developer workflow
git pull --rebase

if [ $? -ne 0 ]; then
    echo "✗ Pull failed. You may have a conflict in $RUN_REPO"
    echo "  Run: cd $RUN_REPO && git status"
    exit 1
fi

# ─── Done ───────────────────────────────────────────────────────────────────

echo ""
echo "✓ Done: $DEST committed, pushed, and synced to run environment"

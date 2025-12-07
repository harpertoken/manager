#!/bin/bash

# SPDX-License-Identifier: MIT

# Script to rewrite commit messages for conventional commits
# Makes first line lowercase and truncates to 40 chars if needed

if [ $# -ne 1 ]; then
    echo "Usage: $0 <commit-hash>"
    exit 1
fi

COMMIT=$1

# Get current message
MSG=$(git log --format=%B -n 1 $COMMIT)

# Process first line
FIRST_LINE=$(echo "$MSG" | head -1 | tr '[:upper:]' '[:lower:]')
if [ ${#FIRST_LINE} -gt 40 ]; then
    FIRST_LINE="${FIRST_LINE:0:40}"
fi

# Reconstruct message
NEW_MSG="$FIRST_LINE
$(echo "$MSG" | tail -n +2)"

# Rewrite commit
git filter-branch --msg-filter "echo \"$NEW_MSG\"" -- $COMMIT^..$COMMIT

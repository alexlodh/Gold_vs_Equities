#!/usr/bin/env zsh
set -e                           # exit on any error

# get timestamp in YYYYMMDD:HHMM
timestamp=$(date +%Y%m%d:%H%M)

# sync with remote main
git pull origin main

# stage everything
git add .

# commit with timestamp
git commit -m "${timestamp}"

# push to branch (default main)
branch=${1:-main}
git push -u origin "${branch}"
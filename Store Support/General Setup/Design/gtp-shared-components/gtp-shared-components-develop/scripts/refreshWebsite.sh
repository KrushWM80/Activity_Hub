#! /usr/bin/env bash

# shellcheck disable=SC2086
# shellcheck disable=SC1091

HEADER=$(cat<<'EOH'
#=====================================================================
# refreshWebsite.sh
#=====================================================================
# DESCRIPTION
#   This script copies the the .md files to the website/docs directory,
#   to be used in preparation for a new build
#
#- OPTIONS
#-    -h, --help                Print detail help (this HEADER)
#-
#=====================================================================
EOH
:)

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WEBSITE_DIR="$PROJECT_DIR/website"
STYLEGUIDIST_DIR="$PROJECT_DIR/website"
SCRIPTS_DIR="$PROJECT_DIR/scripts"
DOCS_DIR="$WEBSITE_DIR/docs/introduction"

# shellcheck source=$SCRIPTS_DIR/common.sh
source $SCRIPTS_DIR/common.sh
SELF=$(basename "$0")

#=====================================================================
# Functions
#=====================================================================
usage()         { echo "$HEADER"|grep -e "^#[%+-]" | sed -e "s/^#[%+-]//g" -e "s/\$0/$SELF/g"; }
showHelp()      { echo; echo "$HEADER"|grep -e "^#" | sed -e "s/^#[%+-]*//g" -e "s/\$0/$SELF/g"; echo; exit 0; }

#=====================================================================
# Get input parameters
#=====================================================================
(( $# != 0 && $# != 1 )) && \
  bailWithUsage "garbled command options"
while [ $# -gt 0 ]; do
  # echo "$#, $*"
  case $1 in
  (-h|--help)     showHelp;;
  (-*)  bailWithUsage "$1: unknown option"; break;;
  (*) break;;
  esac
done

step="Ensure the correct node version..."
echo $step
expected_version=$(cat "$PROJECT_DIR"/.nvmrc) && \
current_version=$(node -v | tr -d "v")
if [[ "$current_version" != "$expected_version" ]]; then
  errorHandler 101 "Node version mismatch: expected $expected_version, got $current_version\nRun nvm install"
fi

step="Copy .md files to website/docs..."
echo $step
cp "$PROJECT_DIR"/CHANGELOG.md "$DOCS_DIR" && \
cp "$PROJECT_DIR"/README.dependencies.md "$DOCS_DIR"
errorHandler $? "Something went wrong while performing: $step"

# for f in "${PROJECT_DIR:?}"/*.md; do
#   echo "$f"
#   cp "$f" "${DOCS_DIR:?}"
# done

step="Remove REPO ONLY content from CHANGELOG ..."
echo $step
awk '/REPO ONLY START/{f=1; next} /REPO ONLY END/{f=0; next} !f' "$DOCS_DIR"/CHANGELOG.md > /tmp/CHANGELOG.md && mv /tmp/CHANGELOG.md "$DOCS_DIR"/CHANGELOG.md
errorHandler $? "Something went wrong while performing: $step"

step="Add front matter to CHANGELOG ..."
echo $step
(cat << EOF
---
sidebar_position: 5
---

EOF
cat "$DOCS_DIR"/CHANGELOG.md) > /tmp/CHANGELOG.md && mv /tmp/CHANGELOG.md "$DOCS_DIR"/CHANGELOG.md
errorHandler $? "Something went wrong while performing: $step"

step="Remove REPO ONLY content from README.dependencies.md ..."
echo $step
awk '/REPO ONLY START/{f=1; next} /REPO ONLY END/{f=0; next} !f' "$DOCS_DIR"/README.dependencies.md > /tmp/README.dependencies.md && mv /tmp/README.dependencies.md "$DOCS_DIR"/README.dependencies.md
errorHandler $? "Something went wrong while performing: $step"

step="Add front matter to README.dependencies.md ..."
echo $step
(cat << EOF
---
sidebar_position: 4
---

EOF
cat "$DOCS_DIR"/README.dependencies.md) > /tmp/README.dependencies.md && mv /tmp/README.dependencies.md "$DOCS_DIR"/README.dependencies.md
errorHandler $? "Something went wrong while performing: $step"
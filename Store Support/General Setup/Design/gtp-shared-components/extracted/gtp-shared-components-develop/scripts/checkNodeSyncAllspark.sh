#! /usr/bin/env bash

# shellcheck disable=SC2086
# shellcheck disable=SC1091

HEADER=$(cat<<'EOH'
#=====================================================================
# checkNodeSyncAllspark.sh
#=====================================================================
# DESCRIPTION
#   This script compares the nodejs version from allspark-cicd-template
#   and the current nodejs version from our .nvmrc
#
#- OPTIONS
#-    -h, --help                Print detail help (this HEADER)
#-    -t, --token <git-token>   Run the script using the given git token (uses GITHUB_ACCESS_TOKEN in Looper)
#-
#=====================================================================
EOH
:)

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$PROJECT_DIR/scripts"

#=====================================================================
# Functions
#=====================================================================
# shellcheck source=$SCRIPTS_DIR/common.sh
source $SCRIPTS_DIR/common.sh

SELF=$(basename "$0")
usage()         { echo "$HEADER"|grep -e "^#[%+-]" | sed -e "s/^#[%+-]//g" -e "s/\$0/$SELF/g"; }
showHelp()      { echo; echo "$HEADER"|grep -e "^#" | sed -e "s/^#[%+-]*//g" -e "s/\$0/$SELF/g"; echo; exit 0; }
mkTempFile()    { echo "/tmp/${SELF}.${RANDOM}.txt"; }

#=====================================================================
# Get input parameters
#=====================================================================
(( $# != 0 && $# != 1 && $# != 2 )) && \
  bailWithUsage "garbled command options"
while [ $# -gt 0 ]; do
  # echo "$#, $*"
  case $1 in
  (-h|--help)     showHelp;;
  (-t|--token)    shift; setParam git_token "$1"; shift;;
  (-*)  bailWithUsage "$1: unknown option"; break;;
  (*) break;;
  esac
done

if [ -z "$git_token" ]; then
  bailWithUsage "Error: you need to provide the git token"
fi

TEMPLATE_FILE="https://gecgithub01.walmart.com/raw/allspark/allspark-cicd-template/main/.looper-allspark-template.yml?token=$git_token"

cd "$PROJECT_DIR" || exit 102
step="Getting the version of nodejs from allspark-cicd-template"
ALLSPARK_VERSION=$(curl --silent $TEMPLATE_FILE | \
grep nodejs | \
awk '{print $2}')
errorHandler $? "something went wrong during step: $step." silent

step="Getting the version of nodejs from our .nvmrc"
NVMRC_VERSION=$(cat .nvmrc)
errorHandler $? "something went wrong during step: $step." silent

step="Comparing .nvmrc nodejs version with allspark ..."
echo $step
if [[ "$ALLSPARK_VERSION" != "$NVMRC_VERSION" ]]; then
  echo "           👉 Warning: the .nvmrc nodejs version: $NVMRC_VERSION is not in sync with allspark: $ALLSPARK_VERSION"
else
  echo "✅ OK"
fi

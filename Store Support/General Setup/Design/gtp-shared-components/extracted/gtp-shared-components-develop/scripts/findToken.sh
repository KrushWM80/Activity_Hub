#! /usr/bin/env bash
# shellcheck disable=SC2086
# shellcheck disable=SC1091

HEADER=$(cat<<'EOH'
#=====================================================================
# findToken.sh
#=====================================================================
# DESCRIPTION
#     This script is a helper for the process of upgrading tokens to a new version
#     It is used to look up tokens
#     If you pass the '--next true' parameter, it will look for tokens in the 'tokens-next' package
#     NOTE: if you haven't installed the 'tokens-next' package, you will get an error. Run diffTokens.sh first to install it
#
# USAGE:
#     $0 -t <token_name> [--next true]
#
#- OPTIONS
#-    -h, --help                Print detail help (this HEADER)
#-    -t, --token <token_name>  The token name to find (it can be a regular expression)
#-    -n, --next true           (optional) look for the given token in the 'tokens-next' package
#
# EXAMPLES:
#     $0 -t componentProgressTrackerIndicatorVariantErrorBackgroundColor  # <-- find one token
#     $0 -t ProgressTracker                                               # <-- find all tokens that contain 'ProgressTracker'
#     $0 -t "componentProgressTracker..*Background"                       # <-- find all tokens which conform to this regular expression
#     $0 -t "componentSelectValueTextColorDisabled" --next true           # <-- find one token in the `tokens-next` package
#=====================================================================
EOH
:)

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$PROJECT_DIR/scripts"
LD_PREFIX="./node_modules/@livingdesign"
LD_SUFFIX="dist/react-native/light/regular"
TOKENS_DIR="$LD_PREFIX/tokens/$LD_SUFFIX"
TOKENS_NEXT_DIR="$LD_PREFIX/tokens-next/$LD_SUFFIX"

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
(( $# != 1 && $# != 2 && $# != 4 )) && \
  bailWithUsage "garbled command options"
while [ $# -gt 0 ]; do
  # echo "$#, $*"
  case $1 in
  (-h|--help)       showHelp;;
  (-t|--token)    shift; setParam token_name "$1"; shift;;
  (-n|--next)     shift; setParam next "$1"; shift;;
  (-*)  bailWithUsage "$1: unknown option"; break;;
  (*) break;;
  esac
done

if [ -z "$token_name" ]; then
  bailWithUsage "Error: you need to provide the token name you are looking for"
fi

TDIR=$TOKENS_DIR
if [ -n "$next" ] && [ "$next" == "true" ]; then
  TDIR=$TOKENS_NEXT_DIR
  if [ ! -d "$TDIR" ]; then
    errorHandler 1 "Error: the 'tokens-next' package is not installed. Run diffTokens.sh first"
  fi
fi

find $TDIR/components \
  -name "*.js" \
  -exec egrep -e "$token_name" {}  \;

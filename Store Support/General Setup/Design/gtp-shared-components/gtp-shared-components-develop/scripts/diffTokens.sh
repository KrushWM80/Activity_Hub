#! /usr/bin/env bash
# shellcheck disable=SC2086
# shellcheck disable=SC1091

HEADER=$(cat<<'EOH'
#=====================================================================
# diffTokens.sh
#=====================================================================
# DESCRIPTION
#     This script is a helper for the process of upgrading tokens to a new version
#     It peforms the following:
#       - adds "@livingdesign/tokens-next": "@livingdesign/tokens@0.61.0" to package.json
#       - identifies the tokens that are different
#       - displays the differences
#     NOTE: after you run the script, you will see package.json and yarn.lock modified
#     You will need to revert those changes when you see fit.
#
# USAGE:
#   $0 -v <new-tokens-version> [-c <component>]
#
#- OPTIONS
#-    -h, --help                        Print detail help (this HEADER)
#-    -v, --version <version_number>    The new tokens version
#-    -c, --component <component_name>  The component you are interested in
#
# EXAMPLES:
#   $0 -v 0.74.0 -c globals     <-- displays diffs for global tokens
#   $0 -v 0.74.0 -c BottomSheet <-- displays diffs for BottomSheet
#=====================================================================
EOH
:)

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$PROJECT_DIR/scripts"
LD_PREFIX="./node_modules/@livingdesign"
LD_SUFFIX="dist/react-native/light/regular"
TOKENS_DIR="$LD_PREFIX/tokens/$LD_SUFFIX"
TOKENS_NEXT_DIR="$LD_PREFIX/tokens-next/$LD_SUFFIX"
TMP_LIST="/tmp/components_list.txt"

#=====================================================================
# Functions
#=====================================================================
# shellcheck source=$SCRIPTS_DIR/common.sh
source $SCRIPTS_DIR/common.sh

SELF=$(basename "$0")
usage()         { echo "$HEADER"|grep -e "^#[%+-]" | sed -e "s/^#[%+-]//g" -e "s/\$0/$SELF/g"; }
showHelp()      { echo; echo "$HEADER"|grep -e "^#" | sed -e "s/^#[%+-]*//g" -e "s/\$0/$SELF/g"; echo; exit 0; }
mkTempFile()    { echo "/tmp/${SELF}.${RANDOM}.txt"; }

isTokenDeprecated () {
  local token="$1"
  local file="$2"
  local line_nr

  line_nr=$(isTokenPresent "$token" "$file")

  if (( line_nr != 0)); then
    # find the second previous line above this
    dep_line=$(sed -n "$((line_nr - 2))p" "$file")

    # if $dep_line contains 'deprecated' return 'true'
    if [[ -n "$dep_line" ]]; then
      if [[ "$dep_line" == *"deprecated"* ]]; then
        echo 1
      else
        echo 0
      fi
    else
      echo 0
    fi
  else
    echo 0
  fi
}

isTokenPresent () {
  local token="$1"
  local file="$2"

  local line_nr

  line_nr=$(grep -n "\b${token}\b" "$file" | cut -d':' -f1)

  if [ -n "$line_nr" ]; then
    echo "$line_nr"
  else
    echo 0
  fi
}

getTokenValue () {
  local token="$1"
  local file="$2"

  val=$(grep "\b${token}\b" "$file" | sed -e 's/^[^:][^:]*:\(..*$\)/\1/g')
  echo "$val"
}

performDiff () {
  local component="$1"
  local token="$2"
  local components_dir

  if [[ "$component" != "globals" ]]; then
    components_dir="components"
  fi

  presentInOldVersion=$(isTokenPresent "$token" "$TOKENS_DIR/$components_dir/$component.js")
  presentInNewVersion=$(isTokenPresent "$token" "$TOKENS_NEXT_DIR/$components_dir/$component.js")

  deprecatedInOldVersion=$(isTokenDeprecated "$token" "$TOKENS_DIR/$components_dir/$component.js")
  deprecatedInNewVersion=$(isTokenDeprecated "$token" "$TOKENS_NEXT_DIR/$components_dir/$component.js")

  valueInOldVersion=$(getTokenValue "$token" "$TOKENS_DIR/$components_dir/$component.js")
  valueInNewVersion=$(getTokenValue "$token" "$TOKENS_NEXT_DIR/$components_dir/$component.js")

  # in old version and not in new version - deleted
  if (( presentInOldVersion != 0 )) && (( ! presentInNewVersion != 0  )) ; then
    echo "$token deleted"
  fi

  # in new version and not in old version - added
  if (( ! presentInOldVersion != 0 )) && (( presentInNewVersion != 0 )) ; then
    echo "$token added"
  fi

  # in current version and in next version
  if (( presentInOldVersion != 0 )) && (( presentInNewVersion != 0 )) ; then

    # deperecated in new version but not in old version - deprecated
    if (( deprecatedInNewVersion != 0 )) && (( ! deprecatedInOldVersion != 0 )) ; then
      echo "$token deprecated"
    fi

    # deprecated in both versions
    if (( deprecatedInNewVersion != 0 )) && (( deprecatedInOldVersion != 0)) ; then

      # values are different- modified
      if [[ "$valueInNewVersion" != "$valueInOldVersion" ]] ; then
        echo "$token modified"
      else
        # values are identical - ignored
        echo "$token ignored"
      fi
    fi

    # not deprecated in either version
    if (( ! deprecatedInOldVersion != 0 )) && (( ! deprecatedInNewVersion != 0 )) ; then
      # values are different- modified
        if [[ "$valueInNewVersion" != "$valueInOldVersion" ]] ; then
        echo "$token modified"
      else
        # values are identical - ignored
        echo "$token ignored"
      fi
    fi
  fi
}


#=====================================================================
# Get input parameters
#=====================================================================
(( $# != 1 && $# != 2 && $# != 4 )) && \
  bailWithUsage "garbled command options"
while [ $# -gt 0 ]; do
  # echo "$#, $*"
  case $1 in
  (-h|--help)       showHelp;;
  (-v|--version)    shift; setParam next_version "$1"; shift;;
  (-c|--component)  shift; setParam component "$1"; shift;;
  (-*)  bailWithUsage "$1: unknown option"; break;;
  (*) break;;
  esac
done

if [ -z "$next_version" ]; then
  bailWithUsage "you need to provide the tokens version you are upgrading to"
fi

if [ -z "$component" ]; then
  bailWithUsage "you need to provide the commponent"
fi

cd "$PROJECT_DIR" || exit 101

step="Setup nvm ..."
echo "----------------------------------------------"
echo "$step"
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
errorHandler $? "Something went wrong during $step"

step="Point to the correct node version ..."
echo "----------------------------------------------"
echo "$step"
nvm install
errorHandler $? "Something went wrong during $step"
nvm list |grep "\->"|head -1

packageFound=$(grep -Ec "@livingdesign/tokens-next..*$next_version\"," "$PROJECT_DIR"/package.json)
if (( packageFound != 1 )); then
  step="First run, installing @livingdesign/tokens-next ..."
  echo "----------------------------------------------"
  echo "$step"
  yarn add @livingdesign/tokens-next@npm:@livingdesign/tokens@"$next_version"
fi

cd $TOKENS_DIR/components || exit 102
# shellcheck disable=SC2012
ls -1 ./*.js | sed -e 's/\.\///g' > $TMP_LIST

cd "$PROJECT_DIR" || exit 102

isValidComponent=$(grep -c "$component".js $TMP_LIST)
if (( ! isValidComponent )); then
  if [[ "$component" != "globals" ]]; then
    errorHandler 101 "Component '$component' cannot be found in the tokens dist"
  fi
fi

if [[ "$component" != "globals" ]]; then
  comp_dir="components"
else
  comp_dir=
fi

hasDiffs=$(diff \
<(grep -ve "^..*Generated on" $TOKENS_DIR/$comp_dir/$component.js) \
<(grep -ve "^..*Generated on" $TOKENS_NEXT_DIR/$comp_dir/$component.js) \
> /dev/null 2>&1; echo $?)

echo "-------------------------------------------------"
echo "$component"
echo "-------------------------------------------------"
if (( hasDiffs )); then

  # use old version as driver
  while read -r line; do
    if [[ "$line" == "" || "$line" == "/**"* || "$line" == "*"* || "$line" == "*/" || "$line" == "};" || "$line" == "module.exports"* ]]; then
      continue
    fi
    # shellcheck disable=SC2001
    tok=$(echo "$line" | sed -e 's/"//g' -e 's/\([^:][^:]*\):..*/\1/')
    gl_diff_old=$(performDiff "$component" "$tok")
    if [[ "$gl_diff_old" != "$tok ignored" ]]; then
      echo "$gl_diff_old"
    fi
  done < $TOKENS_DIR/$comp_dir/$component.js > /tmp/${component}_diff.txt

  # use new version as driver
  while read -r line; do
    if [[ "$line" == "" || "$line" == "/**"* || "$line" == "*"* || "$line" == "*/" || "$line" == "};" || "$line" == "module.exports"* ]]; then
      continue
    fi
    # shellcheck disable=SC2001
    tok=$(echo "$line" | sed -e 's/"//g' -e 's/\([^:][^:]*\):..*/\1/')
    gl_diff_new=$(performDiff "$component" "$tok")
    if [[ "$gl_diff_new" != "$tok ignored" ]]; then
      echo "$gl_diff_new"
    fi
  done < $TOKENS_NEXT_DIR/$comp_dir/$component.js >> /tmp/${component}_diff.txt

  sort /tmp/${component}_diff.txt | uniq

else
  echo "No differences"
fi

#!/usr/bin/env bash

# shellcheck disable=SC2009
# shellcheck disable=SC2086
# shellcheck disable=SC2164
# shellcheck disable=SC1091

HEADER=$(cat<<'EOH'
#=====================================================================
# refreshIcons.sh
#=====================================================================
# DESCRIPTION
#    This script handles the automated pipeline for creating icon .png and *.tsx files
#    - source vector icons are tracked in images/icons/
#    - it downloads all icons in SVG format from the Living Design 3 repository
#    - it selectively generates color and size variant .pngs using svgexport via a specifier data structure
#    - it generates icon components via the generated .pngs
#    - it resolves deprecated icons
#
#- OPTIONS
#-    -h, --help                Print detail help (this HEADER)
#-    -v, --version             version of the livingdesign/icons to pull from
#- EXAMPLE
#-    $0 --version 0.4.43       refresh icons using version v0.4.43 of the livingdesign/icon as source
#-
#=====================================================================
EOH
:)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$PROJECT_DIR/scripts"
ICONS_DIR="$PROJECT_DIR/src/icons"
TMP_DIR="$PROJECT_DIR/.tmp"
#LD_SVGS_SOURCE="https://gecgithub01.walmart.com/walmart-web/walmart/tree/main/libs/ui/icons/icons/svg"
LD_SVGS_SOURCE_REPO="https://gecgithub01.walmart.com/livingdesign/icons"
LS_SVGS_SOURCE_DIR="icons/icons/svg"

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
  (-h|--help)     showHelp; break;;
  (-v|--version) shift; setParam version "v$1"; shift;;
  (-*)  bailWithUsage "$1: unknown option"; break;;
  (*) break;;
  esac
done

if [ -z $version ]; then
  bailWithUsage "ERROR: you need to pass version (-v or --version) of livingdesign/icons you want to pull from" 101
fi

cd $PROJECT_DIR

step="    Removing current .svg files ... "
echo "$step"
rm -f images/icons/*
errorHandler $? "something went wrong during step: $step."

step="     'making temp directory' ... "
echo "$step"
mkdir -p $TMP_DIR
errorHandler $? "something went wrong during step: $step."

step="     'rm -f assets/images/icons/* src/icons/*con.tsx src/icons/*con.md' ... "
echo "$step"
rm -f assets/images/icons/* src/icons/*con.tsx src/icons/*con.md
errorHandler $? "something went wrong during step: $step."

step="    Pulling from LivingDesign/icons repo ... "
echo "$step"
cd $TMP_DIR
if [[ -d icons ]]; then
  cd icons && \
  git checkout main && \
  git pull --all && \
  git checkout $version
else
  git clone $LD_SVGS_SOURCE_REPO && \
  git checkout $version
fi
errorHandler $? "something went wrong during step: $step."

step="    Extracting LivingDesign Icons version ... "
echo "$step"
ldIconsVersion=$(grep '^[ ][ ]*"version": "' $TMP_DIR/icons/package.json | sed -e 's/^[ ][ ]*"version": "\(..*\)",/\1/g')
errorHandler $? "something went wrong during step: $step."

echo "version = $ldIconsVersion"

step="    Updating LivingDesign Icons version in README... "
echo "$step"
cat $PROJECT_DIR/README.md | sed -e "s/Conforms to \`LivingDesign Icons\` version:..*/Conforms to \`LivingDesign Icons\` version: $ldIconsVersion/g" > $TMP_DIR/README.md && \
cp $TMP_DIR/README.md $PROJECT_DIR/README.md
errorHandler $? "something went wrong during step: $step."

step="    Copying .tmp/icons/icons/svg/* to images/icons ... "
echo "$step"
cd $PROJECT_DIR
cp $TMP_DIR/icons/icons/svg/* ./images/icons
errorHandler $? "something went wrong during step: $step."

step="    Generating pngs ..."
echo "$step"
echo "    this will take a few minutes ..."
npx node $SCRIPTS_DIR/generatePngs.js
errorHandler $? "something went wrong during step: $step."

step="    Minifying pngs ... "
echo "$step"
npx tsx $SCRIPTS_DIR/minifyPngs.ts
errorHandler $? "something went wrong during step: $step."

step="    Generating icons ... "
echo "$step"
npx node $SCRIPTS_DIR/generateIcons.js
errorHandler $? "something went wrong during step: $step."

step="    Generating icons json file... "
echo "$step"
npx node $SCRIPTS_DIR/generateIconsJson.js
errorHandler $? "something went wrong during step: $step."

step="    Linting newly generated files ... "
echo "$step"
yarn lint:icons
errorHandler $? "something went wrong during step: $step."

# For backwards compatibility we want to keep any icons that were
# deleted from the LD source repo
# So we restore all deleted *.png, *.svg, *.md, *.tsx files
# and then move the .tsx and .md to src/icons/deprecated
step="    List deleted icons, if any ... "
echo "$step"
git ls-files -d | grep svg | sed -e 's/^images\/icons\/\(..*\).svg$/\1/g' > $TMP_DIR/deleted.txt
cat $TMP_DIR/deleted.txt
errorHandler $? "something went wrong during step: $step."

nrDeletedIcons=$(cat $TMP_DIR/deleted.txt | wc -l)

if (( nrDeletedIcons )); then
  step="    Restoring deleted icons (for backwards compatibility) ... "
  echo "$step"
  git ls-files -z -d | xargs -0 git checkout --
  errorHandler $? "something went wrong during step: $step."

  step="    Moving deleted icons to icons/deprecated ... "
  echo "$step"
  while read -r file; do
    $SCRIPTS_DIR/deprecateIcon.sh --icon $file
  done < $TMP_DIR/deleted.txt
  errorHandler $? "something went wrong during step: $step."
fi

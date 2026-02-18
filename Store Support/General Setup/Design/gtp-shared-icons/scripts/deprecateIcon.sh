#!/usr/bin/env bash

# shellcheck disable=SC2009
# shellcheck disable=SC2086
# shellcheck disable=SC2164
# shellcheck disable=SC1091

HEADER=$(cat<<'EOH'
#=====================================================================
# deprecateIcon.sh
#=====================================================================
# DESCRIPTION
#    This script will move a given icon to the deprecated dir
#      - move .tsx and .md files
#      - edit .tsx file and fix the imports
#      - add the icon to the deprecated/index.ts file
#
#- OPTIONS
#-    -h, --help                Print detail help (this HEADER)
#-    -i, --icon                the name of the icon to be deprecated
#-
#=====================================================================
EOH
:)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$PROJECT_DIR/scripts"
ICONS_DIR="$PROJECT_DIR/src/icons"
TMP_DIR="$PROJECT_DIR/.tmp"

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
  (-i|--icon)     shift; setParam icon "$1"; shift;;
  (-*)  bailWithUsage "$1: unknown option"; break;;
  (*) break;;
  esac
done

cd $PROJECT_DIR

if [ -f $ICONS_DIR/$icon.tsx ]; then
  step="    Move $icon.tsx to icons/deprecated ... "
  echo "$step"
  mv $ICONS_DIR/$icon.tsx $ICONS_DIR/deprecated/
  errorHandler $? "something went wrong during step: $step."

  step="    Move $icon.md to icons/deprecated ... "
  echo "$step"
  mv $ICONS_DIR/$icon.md $ICONS_DIR/deprecated/
  errorHandler $? "something went wrong during step: $step."

  step="    Add $icon to icons/deprecated/index ... "
  echo "$step"
  echo "export {$icon} from './$icon';" >> $ICONS_DIR/deprecated/index.ts
  errorHandler $? "something went wrong during step: $step."

  step="    Fix imports of assets in $icon.tsx ... "
  echo "$step"
  sed -i '' 's/\.\.\/\.\.\/assets/..\/..\/..\/assets/g' $ICONS_DIR/deprecated/$icon.tsx
  errorHandler $? "something went wrong during step: $step."

  step="    Fix imports of utils in $icon.tsx ... "
  echo "$step"
  sed -i '' 's/\.\.\/utils/..\/..\/utils/g' $ICONS_DIR/deprecated/$icon.tsx
  errorHandler $? "something went wrong during step: $step."

  step="    Append 'dep' to displayName in $icon.tsx ... "
  echo "$step"
  sed -i '' "s/displayName = ..*$/displayName = '${icon}.dep';/g" $ICONS_DIR/deprecated/$icon.tsx
  errorHandler $? "something went wrong during step: $step."

  step="    Remove export from src/icons/index ... "
  echo "$step"
  grep  -ve "export {$icon} from './$icon'" $ICONS_DIR/index.tsx > $TMP_DIR/src_icons_index.tsx
  mv $TMP_DIR/src_icons_index.tsx $ICONS_DIR/index.tsx
  errorHandler $? "something went wrong during step: $step."


  step="    Add console.log warning in $icon.tsx ... "
  echo "$step"
  cat<<EOF > $TMP_DIR/icon.tsx
  $(head -49 $ICONS_DIR/deprecated/$icon.tsx)
  // eslint-disable-next-line no-console
  $(echo "console.log('---- ⚠️  WARNING: $icon is deprecated!')")
  $(tail -22 $ICONS_DIR/deprecated/$icon.tsx)
EOF
  errorHandler $? "something went wrong during step: $step."

  step="    Ovewrite $icon.tsx ... "
  echo "$step"
  mv $TMP_DIR/icon.tsx $ICONS_DIR/deprecated/$icon.tsx && \
  yarn prettier --write $ICONS_DIR/deprecated/$icon.tsx
  errorHandler $? "something went wrong during step: $step."

fi
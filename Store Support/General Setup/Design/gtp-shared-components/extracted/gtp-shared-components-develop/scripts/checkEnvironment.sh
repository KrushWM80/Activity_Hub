#!/usr/bin/env bash

# shellcheck disable=SC2034
# shellcheck disable=SC1091
. "$HOME"/.bashrc

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$PROJECT_DIR/scripts"

# Versions of packages/tools that need to be installed
nvm_expected="0.39.0"
npx_expected="8.15.0"
node_expected="v23.1.0"
yarn_expected="4.4.1"
watchman_expected="2024.05.06.00"
pod_expected="1.14.3"
xcode_expected="15.3"
svn_expected="1.14.1"
shellcheck_expected="0.9.0"
java_expected="openjdk version \"17.0.9\" 2023-10-17 LTS"

step="Checking Xcode ..."
echo "----------------------------------------------"
echo "$step"
XC_VERSION=$(xcodebuild -version 2>/dev/null|head -1|sed -e 's/Xcode //g')
XC_VERSION=${XC_VERSION:-"none"}
if [[ "$XC_VERSION" != "$xcode_expected" ]]; then
  echo "️           👉 Warning: expected: $xcode_expected, found: $XC_VERSION"
else
  echo "✅ OK"
fi

step="Checking Java ..."
echo "----------------------------------------------"
echo "$step"
java_version=$(java -version 2>&1|head -1|sed -e "s/^..*version \"\(..*\)\"$/\1/g")
java_version=${java_version:-"none"}
if [[ "$java_version" != "$java_expected" ]]; then
  echo "️           👉 Warning: expected: $java_expected, found: $java_version"
else
  echo "✅ OK"
fi

# Check if the version of a particular package is found.
checkTool () {
  local tool="$1"
  local expected="$2"
  TOOL=$(command -v "$tool")
  TOOL_VERSION=$($TOOL --version 2>/dev/null | head -2 | grep -E -o 'v?((\d+\.)?\d+\.\d+\.\d+-?\w*)' | head -1)
  TOOL_VERSION=${TOOL_VERSION:-"none"}
  if [[ "$TOOL_VERSION" != "$expected" ]]; then
    echo "           👉 Warning: expected: $expected, found: $TOOL_VERSION"
  else
    echo "✅ OK"
  fi
}

for tool in nvm npx yarn watchman pod shellcheck node; do
  step="Checking $tool ..."
  echo "----------------------------------------------"
  echo "$step"
  exp=${tool/-/_}_expected
  checkTool $tool "${!exp}"
done

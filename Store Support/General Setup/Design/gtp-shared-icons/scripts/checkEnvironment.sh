#!/usr/bin/env bash

# Versions of packages that need to be installed
npx_expected="8.1.2"
node_expected="v16.13.2"
yarn_expected="1.22.19"
watchman_expected="2022.03.14.00"
pod_expected="1.11.3"
xcode_expected="13.2.1"
shellcheck_expected="0.8.0"
java_expected="1.8.0_322"
rsvg_convert_expected="2.52.7"       # librsvg
convert_expected="7.1.0-27" # imagemagick

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
  TOOL_VERSION=$($TOOL --version 2>/dev/null | head -2 | egrep -o 'v?((\d+\.)?\d+\.\d+\.\d+-?\w*)' | head -1)
  TOOL_VERSION=${TOOL_VERSION:-"none"}
  if [[ "$TOOL_VERSION" != "$expected" ]]; then
    echo "           👉 Warning: expected: $expected, found: $TOOL_VERSION"
  else
    echo "✅ OK"
  fi
}

for tool in npx node yarn watchman pod shellcheck rsvg-convert convert; do
  step="Checking $tool ..."
  echo "----------------------------------------------"
  echo "$step"
  exp=${tool/-/_}_expected
  checkTool $tool ${!exp}
done

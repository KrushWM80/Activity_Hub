#! /usr/bin/env bash

# This script checks if there are any spaces left at the end of lines
# and if every file has an empty line at the end.
# run with --watch if you want it run in a loop (useful while doing development)
RES="/tmp/spaces.txt"

checkSp () {
  git -c core.whitespace=fix,-indent-with-non-tab,trailing-space,cr-at-eol diff --check HEAD~1 > $RES
  res=$(cat $RES|wc -l)
  if (( res != 0 )); then
    echo "🚫 Found issues"
    echo
    cat $RES
  else
    git -c core.whitespace=fix,-indent-with-non-tab,trailing-space,cr-at-eol diff --check HEAD~2 > $RES
    res=$(cat $RES|wc -l)
    if (( res != 0 )); then
      echo "🚫 Found issues"
      echo
      cat $RES
    else
      echo "✅ OK - All tickety-boo!"
    fi
  fi
}

if [[ "$1" = "--watch" || "$1" = "-w" ]]; then
  while true; do
    clear
    checkSp
    sleep 60
  done
else
  checkSp
fi
# shellcheck disable=SC2148
# Common functions for shell scripts
bail () {
  exit 0;
}

bailWithError () {
  echo; echo "ERROR: $1"; echo; exit "${2-1}";
}

bailWithUsage () {
  echo; echo "ERROR: $1"; usage; exit "${2-1}";
}

errorHandler () {
  local ret="$1"
  local message="$2"
  local silent="$3"
  if (( ret )); then
    echo "🚫 ERROR: $message"
    exit 101
  else
    if [[ -z "$silent" ]]; then
      echo "✅ OK"
    fi
  fi
}

setParam () {
  # shellcheck disable=SC2086
  {
    local var="$1"
    local val=${2-"##undef##"}
    eval $var=$val
    [[ ${!var} == -* ]] && eval $var="##undef##"
    #echo "val: ${!var}"
  }
}

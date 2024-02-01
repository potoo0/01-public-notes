#!/usr/bin/env bash
GLOBAL_LEVEL='INFO'

# $1 message
# $2 log level, default is DEBUG, eg: INFO
log() {
  declare -A LOG_LEVEL=(
    [DEBUG]=3
    [INFO]=2
    [WARN]=1
    [ERROR]=0
  )
  declare -A LOG_COLOR=(
    [DEBUG]='\033[34m'  # Blue
    [INFO]='\033[32m'   # Green
    [WARN]='\033[33m'   # Yellow
    [ERROR]='\033[31m'  # Red
  )

  local msg level
  msg=$1
  level=$([ -n "$2" ] && echo "${2^^}" || echo 'DEBUG')

  if [ "${LOG_LEVEL[${level}]:-3}" -gt "${LOG_LEVEL[${GLOBAL_LEVEL^^}]:-3}" ] ; then
    return 0
  fi

  local DEFAULT='\033[32m'
  local NC='\033[0m'
  printf "$(date --iso-8601=seconds) ${LOG_COLOR[$level]:-$DEFAULT}>>> %-7s: ${NC}%s\n" "$level" "$msg"
}

GLOBAL_LEVEL=${1:-$GLOBAL_LEVEL}

log 'debug msg'
log 'info msg' info
log 'error msg' error

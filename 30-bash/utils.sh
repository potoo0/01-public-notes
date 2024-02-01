#!/usr/bin/env bash

# sh/zsh not support `${a,,}` or `${a^^}`, use `tr` instead
# usage: `echo aBa | lower` or `lower 'Qwe'`
lower() { echo "${*:-$(</dev/stdin)}" | tr '[:upper:]' '[:lower:]'; }
# usage: `echo aBa | upper` or `upper 'Qwe'`
upper() { echo "${*:-$(</dev/stdin)}" | tr '[:lower:]' '[:upper:]'; }


packzip() {
  ROOT=$(realpath "$1")
  if [ ! -d "$ROOT" ]; then
    echo "$ROOT not valid directory!"
    exit 1
  fi
  FILE_NAME="$(basename "$ROOT").zip"

  echo ">>>>>>>> pack $ROOT to $FILE_NAME >>>>>>>>"
  IGNORES=('*.java' '*.log' '**/__pycache__/*' '**/node_modules/*')
  FULL_CMD="zip -r $FILE_NAME $ROOT $(printf " -x %s" "${IGNORES[@]}")"
  echo "full cmd: " "$FULL_CMD"

  # need to to parent dir, otherwise IGNORES may not work.
  cd "$(dirname "$ROOT")" || exit 1
  sh -c "rm -f $FILE_NAME"
  sh -c "$FULL_CMD"
}

# foreach string with space
str_arr=('1 2' 'a b' 'c')
for str in "${str_arr[@]}"; do
  echo "str: $str"
done

# foreach from ls
for d in /tmp/*; do
  echo "item: $d"
  if [ -d "$d" ]; then
    echo "item is folder"
  fi
done

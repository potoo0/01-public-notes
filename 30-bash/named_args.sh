#!/bin/bash
# declare -A: associative arrays, just like dict in python
declare -A ARGS
for arg in "$@";do
  echo "arg: $arg"
  key=${arg%=*}
  value=${arg#*=}
  ARGS[$key]=$value
done

# print array type and element with index
declare -p ARGS

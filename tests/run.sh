#!/bin/bash

# parse arguments
rebuild=false
codeqc=false
test_filter=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --rebuild)
      rebuild=true
      shift
      ;;
    --codeqc)
      codeqc=true
      shift
      ;;
    *)
      test_filter="$1"
      shift
      ;;
  esac
done

# test all or specific tests
if [ "$test_filter" == "" ]; then
  cmd=""
else
  cmd="-k $test_filter"
fi

clear

# rebuild
if [ "$rebuild" = true ]; then
  docker compose build
fi

# check code quality
if [ "$codeqc" = true ]; then
  docker compose run --remove-orphans test_runner bash src/codeqc.sh
fi

# run pytest (by default)
docker compose run --remove-orphans test_runner pytest tests/ $cmd
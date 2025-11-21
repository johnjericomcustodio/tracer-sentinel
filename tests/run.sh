#!/bin/bash

set -euo pipefail

# parse arguments
build=false
cleanup=false
test=false
test_filter=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --build)
      build=true
      shift
      ;;
    --cleanup)
      cleanup=true
      shift
      ;;
    --test)
      test=true
      shift
      ;;
    *)
      test_filter="$1"
      shift
      ;;
  esac
done

# cleanup previous results
if [[ "$cleanup" == true ]]; then
  echo "Cleaning up previous test results..."
  find data/scenarios -type f -name "test_results*" -delete
fi

# build container + code quality checks
if [[ "$build" == true ]]; then
  echo "Building Docker container..."
  docker compose build
  echo "Running code quality checks..."
  docker compose run --remove-orphans  test_runner bash qa/codeqc.sh  
fi

# run pytest
if [[ "$test" == true ]] || [[ -n "$test_filter" ]]; then
  echo "Running tests..."
  cmd_args=()
  [[ -n "$test_filter" ]] && cmd_args+=(-k "$test_filter")
  docker compose run --remove-orphans  test_runner pytest tests/ "${cmd_args[@]}" -s -v
fi
#!/bin/bash

# exit immediately at a non-zero status
set -euo pipefail

echo "--- Running Code Quality Checks ---"

src_dirs=("src" "tests")

echo "1. Formatting checks..."
black --check --diff "${src_dirs[@]}"

echo "2. Linting..."
flake8 "${src_dirs[@]}"
pylint "${src_dirs[@]}"

echo "3. Type checking..."
mypy "${src_dirs[@]}"

echo "--- All Code Quality Checks Passed Successfully ---"
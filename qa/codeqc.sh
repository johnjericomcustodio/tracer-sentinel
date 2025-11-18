#!/bin/bash

# exit immediately at a non-zero status
set -euo pipefail

echo "--- Running Code Quality Checks ---"

src_dirs=("src" "tests")

echo "1. Formatting checks..."
black --check --diff "${src_dirs[@]}"
isort --check-only --diff "${src_dirs[@]}"

echo "2. Linting..."
flake8 "${src_dirs[@]}"
pylint "${src_dirs[@]}"

echo "3. Type checking..."
mypy "${src_dirs[@]}"

echo "4. Security scanning..."
bandit -r "${src_dirs[0]}/" -ll

echo "5. Running tests with coverage..."
pytest --cov="${src_dirs[0]}" --cov-report=term-missing --cov-fail-under=80 "${src_dirs[1]}"/

echo "--- All Code Quality Checks Passed Successfully ---"
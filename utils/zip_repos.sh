#!/usr/bin/env sh

# This script is used to zip all the repository test cases
# It requires the `zip` command to be installed

# It receives the zip filename as an argument

set -e

# Get the current directory
DIR="$(cd "$(dirname "$0")" && pwd)"

# Get the test cases directory
TEST_CASES_DIR="$DIR/../tests/repo_test_cases"

PREV_PATH=$(pwd)
# Move to the test cases directory
cd "$TEST_CASES_DIR"

# Zip all the repositories into a single file, in the original directory
zip -r "$PREV_PATH/$1" .

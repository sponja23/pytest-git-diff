#!/usr/bin/env sh

# This script is used to unzip all the repository test cases
# It requires the `unzip` command to be installed

# It receives the zip file as an argument

set -e

# Get the current directory
DIR="$(cd "$(dirname "$0")" && pwd)"

# Get the test cases directory
TEST_CASES_DIR="$DIR/../tests/repo_test_cases"

# Get the zip file
ZIP_FILE="$1"

# Unzip the file into the test cases directory
unzip -d "$TEST_CASES_DIR" "$ZIP_FILE"

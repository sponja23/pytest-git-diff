#!/usr/bin/env sh

# This script is used to zip all the repository test cases
# It requires the `zip` command to be installed

# It receives the zip filename as an argument

set -e

# Get the script's directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Get the test cases directory
TEST_CASES_DIR="$SCRIPT_DIR/../tests/repo_test_cases"

# Store the output path
OUTPUT_PATH=$(realpath "$1")

# Move to the test cases directory
cd "$TEST_CASES_DIR"

# Zip all the repositories into a single file, in the original directory
zip -r "$OUTPUT_PATH" .

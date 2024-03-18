#!/usr/bin/env sh

# This script is used to unzip all the repository test cases
# It requires the `unzip` command to be installed

# It receives the zip file as an argument

set -e

# Get the script's directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Get the test cases directory
TEST_CASES_DIR="$SCRIPT_DIR/../tests/repo_test_cases"

# Create the test cases directory if it doesn't exist
mkdir -p "$TEST_CASES_DIR"

# Get the zip file
ZIP_FILE="$1"

# Unzip the file into the test cases directory
unzip -d "$TEST_CASES_DIR" "$ZIP_FILE"

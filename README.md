# pytest-git-diff

![Test Workflow Status](https://img.shields.io/github/actions/workflow/status/sponja23/pytest-git-diff/testing.yml)
![PyPI Version](https://img.shields.io/pypi/v/pytest-git-diff)

Pytest plugin that allows the user to select the tests *affected* by a given range of git commits. A file is considered affected when:
- It was added/modified in between the commits.
- It imports another affected file.

## Installation

```bash
pip install pytest-git-diff
```

## Usage

This plugin adds 2 options to the `pytest` CLI:
- `--only-affected-by`: filters the collected tests, keeping only those affected by the given commit range. This range should be in the format `FROM_REV..TO_REV`. If `TO_REV` is omitted, it defaults to 'HEAD'.
- `--only-affected-last-commit`: has the same effect as `--only-affected-by=HEAD~1..HEAD`.

## Limitations

The main limitation in this plugin is that file paths must be valid Python identifier names (in particular, they can't contain dashes). That applies to every part of the path up to the working directory in which `pytest` was invoked.

This issue stems from a problem in the `pydeps` dependency. See https://github.com/thebjorn/pydeps/issues/24.

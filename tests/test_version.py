import sys
from pathlib import Path

from pytest_git_diff._version import VERSION

if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib


def test_versions_match():
    pyproject = Path().absolute() / "pyproject.toml"
    with open(pyproject, "rb") as f:
        data = tomllib.load(f)
        pyproject_version = data["tool"]["poetry"]["version"]

    assert VERSION == pyproject_version

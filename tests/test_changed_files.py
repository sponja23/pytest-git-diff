import json
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import List, Set

import pytest

from pytest_git_diff.changed_files import get_changed_files

from .utils import TEST_DIRECTORY, TEST_RUN_DIRECTORY


@dataclass
class ChangedFilesTestCase:
    """
    A test case consisting of a repository with multiple commits, along with the expected changes
    between some commits.
    """

    repo_path: Path
    """The path of the repository, relative to the directory where the tests are run."""

    from_rev: str
    """The revision to compare from."""

    to_rev: str
    """The revision to compare to."""

    changed_files: Set[Path]
    """The files that changed between the two revisions."""

    @staticmethod
    def from_path(path: Path) -> List["ChangedFilesTestCase"]:
        """
        Create a list of RepoTestCase objects from a path.

        Args:
            path: The path to the test case directory. It should contain a repository with the same
                name as the directory, and a file called `changed_files.json` which contains a list of
                revision ranges along with the expected changed files between them.

        Returns:
            A list of RepoTestCase objects, as many as there are entries in the `changed_files.json`
        """
        changed_files_path = path / "changed_files.json"

        # If there is no changed_files.json file, skip this test case
        if not changed_files_path.exists():
            return []

        with open(changed_files_path) as f:
            test_cases = json.load(f)

        return [
            ChangedFilesTestCase(
                repo_path=(path / path.name).relative_to(TEST_RUN_DIRECTORY),
                from_rev=case["from_rev"],
                to_rev=case["to_rev"],
                changed_files={Path(p) for p in case["changed_files"]},
            )
            for case in test_cases
        ]


changed_files_test_cases = chain.from_iterable(
    ChangedFilesTestCase.from_path(p) for p in (TEST_DIRECTORY / "repo_test_cases").iterdir()
)


@pytest.mark.parametrize(
    "test_case",
    changed_files_test_cases,
    ids=lambda p: f"{p.repo_path.name}-{p.from_rev}-{p.to_rev}",
)
def test_get_changed_files(test_case: ChangedFilesTestCase) -> None:
    assert (
        get_changed_files(test_case.repo_path, test_case.from_rev, test_case.to_rev)
        == test_case.changed_files
    )

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import pytest

from pytest_git_diff.dependencies import ModuleDependencyInfo, get_dependencies

from .utils import TEST_DIRECTORY, TEST_RUN_DIRECTORY


@dataclass
class PackageTestCase:
    """
    A test case consisting of a package with multiple files, along with the dependencies between
    the files.
    """

    package_path: Path
    """The path of the package, relative to the directory where the tests are run."""

    expected_dependencies: Dict[str, ModuleDependencyInfo]
    """The expected dependencies of the package.

    The keys are the names of the modules, and the values are the expected dependencies of
    each module.
    """

    @staticmethod
    def from_path(path: Path) -> "PackageTestCase":
        """
        Create a PackageTestCase from a path.

        Args:
            path: The path to the test case directory. It should contain a package with the same name
                as the directory, and a file called `expected_dependencies.json` which contains the
                expected dependencies of the package.

        Returns:
            A PackageTestCase object.
        """
        with open(path / "expected_dependencies.json") as f:
            expected_dependencies: Dict[str, Any] = json.load(f)

        for name, properties in expected_dependencies.items():
            # The name is not stored in the JSON file, so we add it here
            properties["name"] = name
            # The path should be a Path object, not a string
            properties["path"] = Path(properties["path"])

        return PackageTestCase(
            package_path=(path / path.name).relative_to(TEST_RUN_DIRECTORY),
            expected_dependencies={
                name: ModuleDependencyInfo(**properties)
                for name, properties in expected_dependencies.items()
            },
        )


package_test_cases = [
    PackageTestCase.from_path(path) for path in (TEST_DIRECTORY / "package_test_cases").iterdir()
]


@pytest.mark.parametrize("test_case", package_test_cases, ids=lambda p: p.package_path.name)
def test_get_dependencies(test_case: PackageTestCase) -> None:
    assert get_dependencies(test_case.package_path) == test_case.expected_dependencies

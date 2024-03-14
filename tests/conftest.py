import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import pytest

from pytest_git_diff.dependency_graph.dependencies import ModuleDependencyInfo

TEST_DIRECTORY = Path(os.path.dirname(os.path.realpath(__file__)))

TEST_RUN_DIRECTORY = Path(os.getcwd())

package_test_case_paths = list((TEST_DIRECTORY / "package_test_cases").iterdir())


@dataclass
class PackageTestCase:
    """
    A test case consisting of a package with multiple files.
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


@pytest.fixture(params=package_test_case_paths, scope="session", ids=lambda p: p.name)
def package_test_case(
    request: pytest.FixtureRequest,
) -> PackageTestCase:
    test_case_path: Path = request.param

    return PackageTestCase.from_path(test_case_path)

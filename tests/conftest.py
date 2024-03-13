import json
import os
from pathlib import Path
from typing import Any, Tuple

import pytest

from pytest_git_diff.dependency_graph.dependencies import ModuleDependencyInfo

TEST_DIRECTORY = Path(os.path.dirname(os.path.realpath(__file__)))

TEST_RUN_DIRECTORY = Path(os.getcwd())

package_test_case_paths = list((TEST_DIRECTORY / "package_test_cases").iterdir())


@pytest.fixture(params=package_test_case_paths, scope="session", ids=lambda p: p.name)
def package_test_case(
    request: pytest.FixtureRequest,
) -> Tuple[Path, dict[str, ModuleDependencyInfo]]:
    test_case_path = request.param

    # The actual package is in a subdirectory of the test case directory with the same name
    test_case_package_path = (test_case_path / test_case_path.name).relative_to(TEST_RUN_DIRECTORY)

    # Along with the package, there is a file called `expected_dependencies.json` which
    # contains the expected dependencies of the package
    with open(test_case_path / "expected_dependencies.json") as f:
        expected_dependencies: dict[str, Any] = json.load(f)

    for name, properties in expected_dependencies.items():
        # The name is not stored in the JSON file, so we add it here
        properties["name"] = name
        # The path should be a Path object, not a string
        properties["path"] = Path(properties["path"])

    return test_case_package_path, {
        name: ModuleDependencyInfo(**properties)
        for name, properties in expected_dependencies.items()
    }

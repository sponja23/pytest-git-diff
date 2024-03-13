from pathlib import Path
from typing import Tuple

from pytest_git_diff.dependency_graph.dependencies import ModuleDependencyInfo, get_dependencies


def test_get_dependencies(package_test_case: Tuple[Path, dict[str, ModuleDependencyInfo]]) -> None:
    test_case_package_path, expected_dependencies = package_test_case
    assert get_dependencies(test_case_package_path) == expected_dependencies

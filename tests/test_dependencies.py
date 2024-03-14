from pytest_git_diff.dependency_graph.dependencies import get_dependencies

from .conftest import PackageTestCase


def test_get_dependencies(package_test_case: PackageTestCase) -> None:
    assert (
        get_dependencies(package_test_case.package_path) == package_test_case.expected_dependencies
    )

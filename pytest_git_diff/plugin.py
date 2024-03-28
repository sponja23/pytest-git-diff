from typing import List

import pytest

from .affected_files import get_affected_files


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("collection")

    group.addoption(
        "--only-affected-by",
        action="store",
        default=None,
        type=str,
        help="Filter the collected tests, keeping only those affected by the given revision",
    )


def pytest_collection_modifyitems(
    session: pytest.Session,
    config: pytest.Config,
    items: List[pytest.Item],
) -> None:
    only_affected_by = config.getoption("--only-affected-by")
    if only_affected_by is None:
        return

    if ".." not in only_affected_by:
        from_rev = only_affected_by
        to_rev = "HEAD"
    else:
        from_rev, to_rev = only_affected_by.split("..")

    affected_files = get_affected_files(session.startpath, from_rev, to_rev)

    items[:] = [
        item
        for item in items
        if item.reportinfo()[0].relative_to(session.startpath) in affected_files  # type: ignore
    ]

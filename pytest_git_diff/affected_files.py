"""
Find the files that were *affected* between two revisions in a git repository.

Here, a file is considered affected if it was changed in the given revisions, or if it
depends on a file that was changed.
"""

from pathlib import Path
from typing import Optional, Set

from .changed_files import get_changed_files
from .dependencies import get_dependencies


def get_affected_files(
    repo_path: Path,
    from_rev: str,
    to_rev: Optional[str],
) -> Set[Path]:
    """
    Get the files affected in the repository between two revisions.

    Args:
        repo_path: The path to the repository
        from_rev: The revision to compare from
        to_rev: The revision to compare to. If None, compare to the working directory.
        files: A list of files to consider. If None, consider all files in the repository.

    Returns:
        A list of paths to the affected files relative to the repository root
    """
    # Get the dependencies of the repository files
    dependency_infos = get_dependencies(repo_path)

    print(dependency_infos)

    # Get the files changed in the repository between the two revisions
    changed_files = get_changed_files(repo_path, from_rev, to_rev)

    affected_files: Set[Path] = set()
    stack = list(changed_files)

    while stack:
        file = stack.pop()
        if file in affected_files:
            continue

        affected_files.add(file)
        stack.extend(dependency_infos[file].dependents)

    return affected_files

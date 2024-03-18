import subprocess
from pathlib import Path
from typing import List, Optional


def call_git_command(repo_path: Path, command: str) -> str:
    """
    Call a git command and return the output.

    **WARNING**: The `command` string is split by spaces, with no regard for quoting or
    escaping. This means that commands with spaces or other special characters will not
    work as expected.

    Args:
        repo_path: The path to the repository
        command: The command to run

    Returns:
        The output of the command
    """
    try:
        return subprocess.run(
            ["git", "-C", str(repo_path), *command.split()],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error running git command: {e.stderr}") from e


def get_changed_files(repo_path: Path, from_rev: str, to_rev: Optional[str]) -> List[Path]:
    """
    Get the files changed in the repository between two revisions.

    Args:
        repo_path: The path to the repository
        from_rev: The revision to compare from
        to_rev: The revision to compare to. If None, compare to the working directory.

    Returns:
        A list of paths to the changed files relative to the repository root
    """
    # If to_rev is None, then we are comparing against the working directory
    if to_rev is None:
        to_rev = "HEAD"

    # Get the output of the git command
    output = call_git_command(repo_path, f"diff --name-status {to_rev} {from_rev}")

    return [
        Path(path_str)
        for status, path_str in map(lambda line: line.split("\t"), output.splitlines())
        if status in {"A", "M"}
    ]

"""
Read the dependencies of the project

This is done using the `pydeps` package. It doesn't have a direct API, so
we use the command line interface.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Dict, List

from pydeps import cli
from pydeps.pydeps import pydeps


def pydeps_dependency_dict(path: Path) -> Dict[str, Any]:
    """
    Get the dependency dict output of pydeps for a given path

    Args:
        path: The path to the root of the project

    Returns:
        A dictionary of the form:
        {
            "module_name": {
                "imports"?: List[str],
                "name": str,
                "path": str,
                "imported_by"?: List[str],
            }
        }
    """
    # Use a temporary file to store the output of the `pydeps` command, since there is
    # no way to get the output directly
    with NamedTemporaryFile() as f:
        # Call pydeps with
        # - `--no-output` to suppress the graph picture
        # - `--show-deps` to output the dependencies
        # - `--deps-output` to specify the file to output the dependencies to
        # - `root_path` to specify the root of the project
        pydeps(
            **cli.parse_args(
                [
                    "--no-output",
                    f"--only={path.resolve().name}",
                    "--show-deps",
                    f"--deps-output={f.name}",
                    str(path),
                ]
            )
        )

        f.seek(0)
        return json.load(f)


@dataclass
class ModuleDependencyInfo:
    dependencies: List[Path]
    dependents: List[Path]


def get_dependencies(project_root: Path) -> Dict[Path, ModuleDependencyInfo]:
    """
    Get the dependencies of the project

    Args:
        project_root: The path to the root of the project

    Returns:
        A dictionary mapping module paths to their dependency information
    """
    dependency_dict = pydeps_dependency_dict(project_root)

    absolute_project_root = project_root.resolve()

    name_to_path = {
        entry["name"]: Path(entry["path"]).relative_to(absolute_project_root)
        for entry in dependency_dict.values()
    }

    dependency_info = {
        name_to_path[name]: ModuleDependencyInfo(
            dependencies=[name_to_path[dep] for dep in entry.get("imports", [])],
            dependents=[
                name_to_path[dep] for dep in entry.get("imported_by", []) if dep in name_to_path
            ],
        )
        for name, entry in dependency_dict.items()
    }

    return dependency_info

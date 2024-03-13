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
        root_path: The path to the root of the project

    Returns:
        A dictionary of the form:
        {
            "module_name": {
                "bacon": int,
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
    name: str
    path: Path
    dependencies: List[str]
    dependents: List[str]

    @staticmethod
    def from_pydeps_dict_entry(
        entry: Dict[str, Any],
        *,
        project_root: Path,
    ) -> "ModuleDependencyInfo":
        """
        Parse a single entry from the pydeps dependency dictionary

        Args:
            entry: A single entry from the pydeps dependency dictionary

        Returns:
            A dictionary with the following keys:
            - "name": The name of the module
            - "path": The path to the module, relative to the root of the project
            - "imports": A list of the modules that the module imports
            - "imported_by": A list of the modules that import the module
        """
        return ModuleDependencyInfo(
            name=entry["name"],
            # Convert the path to be relative to the root of the project
            path=Path(entry["path"]).relative_to(project_root),
            dependencies=entry.get("imports", []),
            dependents=entry.get("imported_by", []),
        )


def get_dependencies(project_root: Path) -> Dict[str, ModuleDependencyInfo]:
    """
    Get the dependencies of the project

    Args:
        project_root: The path to the root of the project

    Returns:
        A dictionary mapping module names to their dependency information
    """
    dependency_dict = pydeps_dependency_dict(project_root)
    return {
        module_name: ModuleDependencyInfo.from_pydeps_dict_entry(
            entry,
            project_root=project_root,
        )
        for module_name, entry in dependency_dict.items()
    }

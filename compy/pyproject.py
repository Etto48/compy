import os
from typing import Optional
import toml
import subprocess

def generate_pyproject(project_name: str, author: str, email: Optional[str], version: str = "0.1.0", description: str = "A Python project") -> dict:
    ret = {
        "project": {
            "name": project_name,
            "authors": [{
                "name": author,
            }],
            "version": version,
            "description": description,
            "license": {
                "file": "LICENSE",
            },
            "dependencies": [],
        },
        "build-system": {
            "requires": ["setuptools >= 61.0"],
            "build-backend": "setuptools.build_meta",
        },
        "tool": {
            "setuptools": {
                "package-dir": {
                    project_name: project_name,
                }
            }
        }
    }
    if email:
        ret["project"]["authors"][0]["email"] = email
    return ret

def load_pyproject(pyproject_path: str) -> dict:
    with open(pyproject_path, "r") as f:
        return toml.load(f)
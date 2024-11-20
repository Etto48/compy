import argparse
import os
import subprocess
from typing import Optional
import toml

from compy.git_tool import default_gitignore, init_repo
from compy.pyproject import generate_pyproject, load_pyproject
from compy.venv import create_venv, install_dependencies, install_project
from compy.licenses.mit import get_license
from compy.logger import log_debug, log_info, log_warning, log_error
from compy.touch import touch

def init_project(project_path: str, project_name: Optional[str], author: Optional[str]):
    project_path = os.path.abspath(project_path)
    if not project_name:
        project_name = os.path.basename(project_path)
    if not author:
        author = os.getenv("USER", "Unknown")

    log_info(f"Initializing project: {project_name}")
    os.makedirs(project_path, exist_ok=True)
    pyproject_path = os.path.join(project_path, "pyproject.toml")
    if not os.path.exists(pyproject_path):
        pyproject = generate_pyproject(project_name, author)
        with open(os.path.join(project_path, "pyproject.toml"), "w") as f:
            toml.dump(pyproject, f)
    else:
        log_warning("pyproject.toml already exists")

    log_info("Creating project structure")
    os.makedirs(os.path.join(project_path, project_name), exist_ok=True)
    touch(os.path.join(project_path, project_name, "__init__.py"))

    log_info("Creating README")
    readme_path = os.path.join(project_path, "README.md")
    if not os.path.exists(readme_path):
        with open(readme_path, "w") as f:
            f.write(f"# {project_name}\n")
    else:
        log_warning("README already exists")
    
    log_info("Creating LICENSE")
    license_path = os.path.join(project_path, "LICENSE")
    if not os.path.exists(license_path):
        license_text = get_license(author)
        with open(license_path, "w") as f:
            f.write(license_text)
    else:
        log_warning("LICENSE already exists")

    log_info("Creating virtual environment")
    venv_dir = os.path.join(project_path, ".venv")
    if not os.path.exists(venv_dir):
        create_venv(venv_dir)
    else:
        log_warning("Virtual environment already exists")
    install_project(venv_dir, project_path)

    log_info("Initializing Git repository")
    gitignore_path = os.path.join(project_path, ".gitignore")
    if not os.path.exists(gitignore_path):
        with open(gitignore_path, "w") as f:
            f.write(default_gitignore())
    else:
        log_warning(".gitignore already exists")
    if not os.path.exists(os.path.join(project_path, ".git")):
        init_repo(project_path)
    else:
        log_warning("Git repository already initialized")

    log_info("Project initialized successfully")

def add_dependency(project_path: str, dependencies: list[str]):
    project_path = os.path.abspath(project_path)
    pyproject_path = os.path.join(project_path, "pyproject.toml")
    try:
        pyproject = load_pyproject(pyproject_path)
    except FileNotFoundError:
        log_error("pyproject.toml not found")
        return
    log_info(f"Adding dependencies: {' '.join(dependencies)}")
    pyproject["project"]["dependencies"].extend(dependencies)
    
    venv_path = os.path.join(project_path, ".venv")
    if not os.path.exists(venv_path):
        log_warning("Virtual environment not found, skipping installation")
    else:
        try:
            install_dependencies(venv_path, dependencies)
        except subprocess.CalledProcessError:
            log_error(f"Failed to install dependencies")
            return

    with open(pyproject_path, "w") as f:
        toml.dump(pyproject, f)
    
    log_info("Dependency added successfully")
    

def main():
    parser = argparse.ArgumentParser(
        description="Automatic Python project initialization"
    )
    subparsers = parser.add_subparsers(dest="subcommand")
    subparsers.required = True

    init_parser = subparsers.add_parser("init", help="Initialize a new Python project")
    add_parser = subparsers.add_parser("add", help="Add a new dependency to the project")

    init_parser.add_argument("project_path", help="Path to the project directory", type=str, default=".")
    init_parser.add_argument("-p", "--project-name", help="Name of the project", type=str)
    init_parser.add_argument("-a", "--author", help="Author of the project", type=str)

    add_parser.add_argument("dependencies", help="Name of the dependency to add, also version requirements are allowed", type=str, nargs="+")
    add_parser.add_argument("-p", "--project-path", help="Path to the project directory", type=str, default=".")

    args = parser.parse_args()

    match args.subcommand:
        case "init":
            init_project(args.project_path, args.project_name, args.author)
        case "add":
            add_dependency(args.project_path, args.dependencies)

    

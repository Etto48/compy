import json
import subprocess

def create_venv(venv_dir: str, python_executable: str = "python3"):
    subprocess.run(
        [
            python_executable,
            "-m",
            "venv",
            venv_dir,
        ],
        check=True,
    )

def install_project(venv_dir: str, project_path: str):
    subprocess.run(
        [
            f"{venv_dir}/bin/pip",
            "install",
            "-e",
            project_path,
        ],
        check=True,
    )

def install_dependencies(venv_dir: str, dependencies: list[str]):
    subprocess.run(
        [
            f"{venv_dir}/bin/pip",
            "install",
            *dependencies,
        ],
        check=True,
    )

def uninstall_dependencies(venv_dir: str, dependencies: list[str]):
    subprocess.run(
        [
            f"{venv_dir}/bin/pip",
            "uninstall",
            "-y",
            *dependencies,
        ],
        check=True,
    )

def get_package_distributions(venv_dir: str) -> dict[str, list[str]]:
    result = subprocess.run(
        [
            f"{venv_dir}/bin/python3",
            "-c",
            """import importlib.metadata as im;\
            import json;\
            print(json.dumps(im.packages_distributions()))""",
        ],
        check=True,
        capture_output=True,
    )
    package_distributions = json.loads(result.stdout)
    return package_distributions
    
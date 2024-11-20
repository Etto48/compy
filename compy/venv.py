import venv
import subprocess

def create_venv(venv_dir: str):
    venv.create(venv_dir, with_pip=True)

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
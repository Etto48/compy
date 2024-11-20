import git

def default_gitignore() -> str:
    return \
"""
**/__pycache__/
.venv/
.vscode/
*.egg-info/
"""

def init_repo(project_path: str):
    git.Repo.init(project_path)
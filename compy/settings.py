from dataclasses import dataclass
import os
from typing import Literal, Optional

import toml


@dataclass
class Settings:
    name: Optional[str] = None
    email: Optional[str] = None
    version: str = "0.1.0"
    description: str = "A Python project"
    license: Literal["MIT", "GPL3"] = "MIT"
    python_executable: str = "python3"
    
    @staticmethod
    def load(path: str):
        d = toml.load(open(path))
        return Settings(**d)

    @staticmethod
    def autoload():
        paths = [
            "~/.config/compy/compy.toml",
            "~/.config/compy.toml",
        ]
        for path in paths:
            try:
                return Settings.load(os.path.expanduser(path))
            except FileNotFoundError:
                pass
        return Settings()

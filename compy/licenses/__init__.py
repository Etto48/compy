import os
import time
from typing import Literal

def load_template(template: str, **kwargs):
    licenses_dir = os.path.dirname(__file__)
    path = os.path.join(licenses_dir, f"{template}.txt")
    with open(path, "r") as f:
        license_text = f.read()
    for k, v in kwargs.items():
        license_text = license_text.replace(f"<{k.upper()}>", str(v))
    return license_text

def get_license(author: str, license: Literal["MIT", "GPL3"]):
    kwargs = {
        "COPYRIGHT HOLDER": author,
        "YEAR": time.localtime().tm_year,
    }
    return load_template(license, **kwargs)

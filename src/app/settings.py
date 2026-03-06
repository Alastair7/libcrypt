from ast import Dict
import pathlib
import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from utils.get_root_path import get_app_root_path

ROOT_DIR = get_app_root_path()
APPCONFIG_DIR = ROOT_DIR / "appconfig.yml"


@dataclass
class Settings:
    scripts_path: Path
    current_environment: str
    environment_variables: dict[str, Any]

    @classmethod
    def load_settings(cls):
        data = yaml.safe_load(APPCONFIG_DIR.read_text())

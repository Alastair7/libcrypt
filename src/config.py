import yaml
from constants import APPCONFIG_PATH


class AppConfig:
    def __init__(self):
        cfg = yaml.safe_load((APPCONFIG_PATH).read_text())
        self.scripts_path: str = cfg["scripts_path"]

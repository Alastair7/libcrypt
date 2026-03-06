import os
from typing import Any
import yaml

from constants import ROOT_PATH


APPCONFIG_PATH = ROOT_PATH / "appconfig.yml"


def load_environment_variables(environment: str) -> None:
    appconfig = yaml.safe_load((ROOT_PATH / "appconfig.yml").read_text())
    variables: dict[str, Any] = appconfig["environment_variables"][environment.lower()]

    for key, val in variables.items():
        os.environ[key] = val

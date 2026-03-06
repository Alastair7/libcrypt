import os
from typing import Any
import yaml

from constants import APPCONFIG_PATH


def load_environment_variables(environment: str) -> None:
    appconfig = yaml.safe_load((APPCONFIG_PATH).read_text())
    variables: dict[str, Any] = appconfig["environment_variables"][environment.lower()]

    for key, val in variables.items():
        os.environ[key] = val

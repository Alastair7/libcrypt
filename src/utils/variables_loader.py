import os
import subprocess


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "..", "scripts", "load_variables_by_environment.sh")
)


def load_environment_variables(environment: str) -> bool:
    result = subprocess.run(
        [SCRIPT_PATH, environment], capture_output=True, text=True, check=True
    )

    if result.returncode != 0:
        return False

    for line in result.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            os.environ[key] = value

    return True

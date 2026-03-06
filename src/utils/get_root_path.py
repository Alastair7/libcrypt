from pathlib import Path


def get_app_root_path() -> Path:
    "Gets the root path of LibCrypt App"

    current_file = Path(__file__).resolve()

    for parent in current_file.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise FileNotFoundError("Project root with pyproject.toml not found")

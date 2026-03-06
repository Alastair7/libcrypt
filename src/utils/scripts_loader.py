from pathlib import Path
import re


def load_scripts(scripts_path: Path) -> list[Path]:
    files = [file for file in scripts_path.expanduser().rglob("*.py")]

    click_commands = [file for file in files if validate_script(file) is not None]

    return click_commands


def validate_script(file: Path) -> Path | None:
    default_pattern = re.compile(r'if\s+__name__\s*==\s*["\']__main__["\']\s*:')
    click_pattern = re.compile(r"@click.")

    content = file.read_text("utf-8")

    if click_pattern.search(content):
        return file

    if default_pattern.search(content):
        return file

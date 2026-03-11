import inspect
import importlib.util
import re
from pathlib import Path
from dataclasses import dataclass

from utils.scripts_loader import validate_script


@dataclass
class ScriptParam:
    name: str
    param_type: str
    default: str | None
    help_text: str


def parse_script(path: Path) -> tuple[str, list[ScriptParam]]:
    """Analyzes a script and returns the function name and its parameters."""
    content = path.read_text("utf-8")

    # Check if it's a Click script

    if "@click" in content:
        return _parse_click(content, path)

    # Normal function: import and inspect
    return _parse_normal(path)


def _parse_normal(path: Path) -> tuple[str, list[ScriptParam]]:
    """Imports the module dynamically and inspects the main function."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if not spec or not spec.loader:
        return ("script", [])

    module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)
    except Exception:
        return ("script", [])

    # Find callable functions (exclude private ones)
    functions = {
        name: func
        for name, func in inspect.getmembers(module, inspect.isfunction)
        if not name.startswith("_")
    }

    if not functions:
        return ("script", [])

    # Pick the first public function
    func_name, func = next(iter(functions.items()))

    params: list[ScriptParam] = []
    sig = inspect.signature(func)

    for param_name, param in sig.parameters.items():
        param_type = "str"
        if param.annotation != inspect.Parameter.empty:
            param_type = param.annotation.__name__.lower()

        default = None
        if param.default != inspect.Parameter.empty:
            default = str(param.default)

        params.append(ScriptParam(param_name, param_type, default, ""))

    return func_name, params


def _parse_click(content: str, path: Path) -> tuple[str, list[ScriptParam]]:
    """Extracts parameters from Click decorators using regex."""
    params: list[ScriptParam] = []

    click_pattern = re.compile(r"@\w+\.command\(([^)]*)\)")

    script_commands = click_pattern.findall(content)
    commands = [cmd.strip('"') for cmd in script_commands]

    print("COMMANDS", commands)

    option_pattern = re.compile(
        r'@click\.option\s*\(\s*["\']--(\w+)["\']'
        r"(?:.*?type\s*=\s*(\w+))?"
        r"(?:.*?default\s*=\s*([^,\)]+))?"
        r'(?:.*?help\s*=\s*["\']([^"\']*)["\'])?',
        re.DOTALL,
    )

    argument_pattern = re.compile(
        r'@click\.argument\s*\(\s*["\'](\w+)["\']'
        r"(?:.*?type\s*=\s*(\w+))?",
        re.DOTALL,
    )

    for match in option_pattern.finditer(content):
        name = match.group(1)
        param_type = (match.group(2) or "str").lower().strip()
        default = match.group(3).strip() if match.group(3) else None
        help_text = match.group(4) or ""
        type_map = {"int": "int", "float": "float", "bool": "bool", "integer": "int"}
        params.append(
            ScriptParam(name, type_map.get(param_type, "str"), default, help_text)
        )

    for match in argument_pattern.finditer(content):
        name = match.group(1)
        param_type = (match.group(2) or "str").lower().strip()
        type_map = {"int": "int", "float": "float", "bool": "bool", "integer": "int"}
        params.append(ScriptParam(name, type_map.get(param_type, "str"), None, ""))

    func_match = re.search(r"@click\.command.*?\ndef\s+(\w+)", content, re.DOTALL)
    func_name = func_match.group(1) if func_match else path.stem

    return func_name, params


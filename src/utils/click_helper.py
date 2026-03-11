import re

from core.click_parser import ClickCommandArgument


def extract_commands(script_body: str) -> list[str]:
    """Returns a list of commands from the script body"""
    commands_pattern = re.compile(r"@\w+\.command\(([^)]*)\)")
    commands: list[str] = commands_pattern.findall(script_body)

    return [command.strip('"') for command in commands]


def extract_arguments(
    script_body: str, command_name: str
) -> list[ClickCommandArgument]:
    """Returns the arguments of a command."""
    command_pattern = re.compile(rf"@\w+\.command\(['\"]{command_name}['\"]\)")
    function_pattern = re.compile(r"def\s+\w+([^\)]*)\)")

    command = command_pattern.search(script_body)

    if not command:
        raise ValueError("Command not found")

    start_pos = command.end()
    func_match = function_pattern.search(script_body[start_pos:])

    if not func_match:
        raise ValueError("Function not found")

    end_pos = start_pos + func_match.start()

    command_section = script_body[start_pos:end_pos]

    arguments_pattern = re.compile(r"@click\.argument\(([^\)]*)\)")
    arguments: list[str] = arguments_pattern.findall(command_section)

    function_args = _extract_function_types(script_body, func_match, start_pos)

    return [
        ClickCommandArgument(
            name=arg.strip('"'), arg_type=function_args[arg.strip('"')]
        )
        for arg in arguments
        if arg.strip('"') in function_args
    ]


def _extract_function_types(
    script_body: str, func_match: re.Match[str], start_pos: int
) -> dict[str, str]:
    func_start = start_pos + func_match.start()
    func_end = start_pos + func_match.end()

    result: dict[str, str] = {}
    func_args_pattern = re.compile(r"def\s+\w+\(([^\)]*)\)")

    function_body = script_body[func_start:func_end]

    func_args_result = func_args_pattern.search(function_body)

    if not func_args_result:
        raise ValueError("Match error")

    args_group = func_args_result.group(1)
    args = args_group.strip().split(",")

    for arg in args:
        key = arg.split(":")[0].strip()
        value = arg.split(":")[1].strip()

        result[key] = value

    return result

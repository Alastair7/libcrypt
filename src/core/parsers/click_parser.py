from core.models.click_models import ClickCommand
from utils.click_helper import extract_arguments, extract_commands, extract_options


class ClickScriptParser:
    def __init__(self, content: str):
        self.content: str = content

    def get_commands(self) -> list[ClickCommand]:
        commands = extract_commands(self.content)
        results: list[ClickCommand] = []

        for command in commands:
            args = extract_arguments(self.content, command)
            options = extract_options(self.content, command)
            result = ClickCommand(name=command, args=args, options=options)
            results.append(result)

        return results

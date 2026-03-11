from dataclasses import dataclass


@dataclass
class ClickCommandOption:
    name: str
    default: str
    help: str


@dataclass
class ClickCommandArgument:
    name: str
    arg_type: str


@dataclass()
class ClickCommand:
    name: str
    args: list[ClickCommandArgument]
    options: list[ClickCommandOption]


class ClickScriptParser:
    def __init__(self, content: str):
        self.content: str = content

    def extract_commands(self) -> list[ClickCommand]:
        # command name
        # arguments
        # options
        return []

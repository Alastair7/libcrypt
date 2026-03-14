from dataclasses import dataclass


@dataclass
class ClickCommandOption:
    name: str
    default: str | None = None
    help: str | None = None
    required: bool = False


@dataclass
class ClickCommandArgument:
    name: str
    arg_type: str


@dataclass()
class ClickCommand:
    name: str
    args: list[ClickCommandArgument]
    options: list[ClickCommandOption]

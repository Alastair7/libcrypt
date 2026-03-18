import pytest

from core.models.click_models import ClickCommandArgument, ClickCommandOption
from utils.click_helper import extract_arguments, extract_commands, extract_options


@pytest.fixture
def fake_click_script() -> str:
    return """\
import click


@click.group()
def main():
    pass


@main.command("test")
@click.argument("text")
@click.option("--hello", default="Hey!", required=True)
def test_script(text: str, hello: str):
    click.echo(f"{hello} {text}")


@main.command("random")
def random_script():
    click.echo(f"Hello random")


if __name__ == "__main__":
    main()
"""


@pytest.fixture
def fake_normal_script() -> str:
    return """\


def main():
    pass


def test_script(text: str):
    click.echo(f"Hello {text}")


def random_script():
    click.echo(f"Hello random")


if __name__ == "__main__":
    main()

"""


def test_extract_commands_should_return_empty_when_no_click_commands_found(
    fake_normal_script: str,
):
    assert extract_commands(fake_normal_script) == []


def test_extract_commands_should_return_command_names(fake_click_script: str):
    assert extract_commands(fake_click_script) == ["test", "random"]


def test_extract_arguments_command_not_found(fake_click_script: str):
    with pytest.raises(ValueError, match="Command not found"):
        _ = extract_arguments(
            script_body=fake_click_script, command_name="unknown_command"
        )


def test_extract_arguments_from_command(fake_click_script: str):
    arguments = extract_arguments(script_body=fake_click_script, command_name="test")

    assert arguments == [ClickCommandArgument("text", "str")]


def test_extract_options_from_command(fake_click_script: str):
    options = extract_options(script_body=fake_click_script, command_name="test")

    print("OPTIONS", options)

    assert options == [
        ClickCommandOption(name="--hello", default="Hey!", required=True, help=None)
    ]

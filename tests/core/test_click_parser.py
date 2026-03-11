from core.click_parser import ClickCommand, ClickCommandArgument, ClickScriptParser
import pytest


@pytest.fixture
def fake_click_script() -> str:
    return """\
import click


@click.group()
def main():
    pass


@main.command("test")
@click.argument("text")
def test_script(text: str):
    click.echo(f"Hello {text}")


@main.command("random")
def random_script():
    click.echo(f"Hello random")


if __name__ == "__main__":
    main()

"""


def test_parse_script_should_return_empty(fake_click_script: str):
    parser = ClickScriptParser(fake_click_script)

    commands = parser.extract_commands()

    assert commands == []


def test_parse_script_should_return_existing_commands(fake_click_script: str):
    parser = ClickScriptParser(fake_click_script)

    commands = parser.extract_commands()

    assert commands == [
        ClickCommand(
            name="test",
            args=[
                ClickCommandArgument(name="text", arg_type="str"),
            ],
            options=[],
        ),
        ClickCommand(
            name="random",
            args=[],
            options=[],
        ),
    ]

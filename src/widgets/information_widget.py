from typing import override

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import RadioButton, RadioSet, Static


class EnvironmentRadioButton(Widget):
    DEFAULT_CSS = """
    EnvironmentRadioButton {
            height: auto;
            max-width: 20;
            }
    """

    @override
    def compose(self) -> ComposeResult:
        with RadioSet(id="env"):
            yield RadioButton("DEV", value=True)
            yield RadioButton("NP")
            yield RadioButton("PROD")

    def on_mount(self) -> None:
        self.query_one(RadioSet).focus()  # pyright: ignore[reportUnusedCallResult]


class CurrentBranchName(Static):
    def on_mount(self) -> None:
        self.update("Test")


class InformationPane(Widget):
    DEFAULT_CSS = """
    InformationPane > Horizontal > Static {
            max-width: 32;
            border: solid green;
            }
    .logo {
            width:20;
            height: 10;
            border: solid blue;
            }
    """

    @override
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Static("App Logo", classes="logo")
            yield Static("branch_name_to_do", expand=True)
            yield EnvironmentRadioButton()

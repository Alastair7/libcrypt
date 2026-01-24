from typing import override

from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widget import Widget
from textual.widgets import RadioButton, RadioSet, Static


class EnvironmentRadioButton(Widget):
    DEFAULT_CSS = """
    EnvironmentRadioButton {
            height: 10;
            max-width: 32;
            }
    EnvironmentRadioButton > RadioSet {
            layout: horizontal;
            width: auto;
            }
    #radioset-border {
            border: solid white;
            height: auto;
            }
    """

    @override
    def compose(self) -> ComposeResult:
        with Container(id="radioset-border"):
            with RadioSet(id="env"):
                yield RadioButton("DEV", value=True)
                yield RadioButton("NP")
                yield RadioButton("PROD")

    def on_mount(self) -> None:
        container = self.query_one("#radioset-border", Container)
        container.border_title = "Environments"


class CurrentBranchName(Static):
    def on_mount(self) -> None:
        self.update("Test")


class InformationPane(Widget):
    DEFAULT_CSS = """
    InformationPane {
            border: solid red;
            height: 12;
            }
    InformationPane > Horizontal > Static {
            max-width: 32;
            border: solid green;
            }
    .logo {
            max-width:20;
            height: 10;
            border: solid blue;
            }
    """

    @override
    def compose(self) -> ComposeResult:
        self.branch = Static("branch_name_to_do", expand=True)

        with Horizontal():
            yield Static("App Logo", classes="logo", expand=True)
            yield self.branch
            yield EnvironmentRadioButton()

    def on_mount(self) -> None:
        self.branch.border_title = "Current Branch"

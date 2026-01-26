from typing import override

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Static
from widgets.environment_selector import EnvrionmentSelector


class InformationPane(Widget):
    DEFAULT_CSS = """
    InformationPane {
            border: #2a4f2c;
            height: 25;
            }
    InformationPane > Horizontal > Static {
            width: 11;
            border: solid red;
            align:center top;
            }
    .logo {
            max-width:19;
            height: 9;
            border: red;
            }
    """

    @override
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Static("Test")
            yield EnvrionmentSelector()
            yield EnvrionmentSelector()

    def on_mount(self) -> None:
        pass

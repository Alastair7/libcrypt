from typing import override

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Static
from widgets.environment_selector import EnvrionmentSelector


class InformationPane(Widget):
    @override
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Static("Test")
            yield EnvrionmentSelector()

    def on_mount(self) -> None:
        pass

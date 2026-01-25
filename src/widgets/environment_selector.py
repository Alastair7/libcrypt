from typing import override
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import RadioButton, RadioSet


class EnvrionmentSelector(Widget):
    @override
    def compose(self) -> ComposeResult:
        with RadioSet():
            yield RadioButton("DEV", value=True)
            yield RadioButton("NP")
            yield RadioButton("PROD")

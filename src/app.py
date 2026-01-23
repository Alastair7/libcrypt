from typing import override
from textual.app import App
from textual.widgets import Header

from src.widgets.InformationWidget import InformationPane


class LibcryptApp(App):  # pyright: ignore[reportMissingTypeArgument]
    @override
    def compose(self):
        yield Header(name="Test", show_clock=True)
        yield InformationPane()

from typing import override

from textual.app import App, ComposeResult

from src.widgets.information_widget import InformationPane


class LibcryptApp(App):  # pyright: ignore[reportMissingTypeArgument]
    @override
    def compose(self) -> ComposeResult:
        yield InformationPane()

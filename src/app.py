from typing import override

from textual.app import App, ComposeResult

from panes.info_pane import InformationPane


class LibcryptApp(App):  # pyright: ignore[reportMissingTypeArgument]
    CSS = """
    Screen {
        background: #191a1c; /* Un gris azulado oscuro (estilo Tokyo Night) */
    }
    """

    @override
    def compose(self) -> ComposeResult:
        yield InformationPane()

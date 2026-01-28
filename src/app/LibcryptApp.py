from typing import override

from textual.app import App, ComposeResult

from panes.info_pane import InformationPane
from panes.tree_pane import TreePane
from widgets.directory_tree import CategoriesTree


class LibcryptApp(App):  # pyright: ignore[reportMissingTypeArgument]
    CSS = """
    Screen {
        background: #191a1c;
        overflow-y: hidden;
    }
    """

    @override
    def compose(self) -> ComposeResult:
        yield InformationPane()
        yield TreePane()

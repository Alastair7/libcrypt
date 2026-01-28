from typing import override
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Static

from widgets.directory_tree import CategoriesTree


class TreePane(Widget):
    DEFAULT_CSS = """
    Horizontal {
            layout: horizontal;
            height: 70%;
            }
    #tree-container {
            dock: left;
            width: 35;
            height: auto;
            border: panel brown;
            }
    #content {
            width: 1fr;
            padding: 1;
            border: solid red;
            }
    """

    @override
    def compose(self) -> ComposeResult:
        with Horizontal(id="horizontal"):
            yield CategoriesTree(id="tree-container")
            with Vertical(id="content"):
                yield Static("TODO: Scripts Panel Here")

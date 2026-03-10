from pathlib import Path
from typing import override

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import DirectoryTree

from widgets.directory_tree import CategoriesTree
from widgets.ScriptsPanel import ScriptsPanel


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
        height: 100%;
        padding: 1;
        border: solid red;
    }
    """

    @override
    def compose(self) -> ComposeResult:
        with Horizontal(id="horizontal"):
            yield CategoriesTree(id="tree-container")
            yield ScriptsPanel(id="content")

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        path = Path(str(event.path))
        if path.suffix == ".py":
            panel = self.query_one(ScriptsPanel)
            panel.show_script(path)
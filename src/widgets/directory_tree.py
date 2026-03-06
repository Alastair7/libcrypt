import os
from typing import override
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import DirectoryTree


class CategoriesTree(Container):
    @override
    def compose(self) -> ComposeResult:
        scripts_path: str = os.environ.get("", "./")
        yield DirectoryTree(path=scripts_path)

from typing import override
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import DirectoryTree

from config import AppConfig


class CategoriesTree(Container):
    @override
    def compose(self) -> ComposeResult:
        config = AppConfig()

        scripts_path: str = config.scripts_path

        yield DirectoryTree(path=scripts_path)

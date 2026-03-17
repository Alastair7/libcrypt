from pathlib import Path
from typing import override

from textual.app import ComposeResult
from textual.containers import Container, Vertical, VerticalScroll
from textual.widgets import Button, RichLog, Static

from core.models.click_models import ClickCommand
from core.parsers.click_parser import ClickScriptParser


class ScriptPanel(Container):
    def __init__(self, selected_script: Path):
        self.selected_script = selected_script
        super().__init__()

    @override
    def compose(self) -> ComposeResult:
        yield Static("Select a script from the tree", id="script-info")
        with Vertical():
            yield Static("", id="func-name")
            yield VerticalScroll(id="params-container")
            yield Button("Run Script", id="run-btn")
            yield Static("-- Output --", id="output-label")
            yield RichLog(id="output-log", highlight=True, markup=True)

    def show_script(self):
        script_details = self.query_one("#script-info", Static)
        script_details.update(f"Script: {self.selected_script.name}")

        script_commands = self._load_script()

        # TODO: Show each command of the script

        # TODO: Show each command params.

        # TODO: Execute the command using subprocess

    def _load_script(self) -> list[ClickCommand]:
        script_content = self.selected_script.read_text(encoding="utf-8")

        if not script_content:
            raise ValueError("Script is empty and content is required")

        parser = ClickScriptParser(script_content)

        return parser.get_commands()

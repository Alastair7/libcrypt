from pathlib import Path
import subprocess
import sys
from typing import override

from textual.app import ComposeResult
from textual.containers import Container, Vertical, VerticalScroll
from textual.widgets import Button, Input, RichLog, Select, Static

from core.models.click_models import ClickCommandArgument, ClickCommandOption
from utils.click_helper import extract_arguments, extract_commands, extract_options


class ScriptPanel(Container):
    can_focus_children = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_script: Path | None = None
        self.script_body: str = ""
        self.selected_command: str | None = None
        self.current_arguments: list[ClickCommandArgument] = []
        self.current_options: list[ClickCommandOption] = []

    @override
    def compose(self) -> ComposeResult:
        yield Static("Script: none", id="script-info")
        yield Select[str](options=[], prompt="Select command", id="command-select")
        yield VerticalScroll(Vertical(id="params-container"), id="params-scroll")
        yield Button("Run", id="run-btn")
        yield RichLog(id="output-log")

    def show_script(self, script_path: Path) -> None:
        self.selected_script = script_path
        self.script_body = script_path.read_text(encoding="utf-8")
        self.query_one("#script-info", Static).update(f"Script: {script_path.name}")

        commands = extract_commands(self.script_body)
        command_select = self.query_one("#command-select", Select)

        if not commands:
            command_select.set_options([])
            self.selected_command = None
            self._render_params([], [])
            return

        command_select.set_options([(cmd, cmd) for cmd in commands])
        self.selected_command = commands[0]
        command_select.value = commands[0]
        self._render_current_command()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id != "command-select" or event.value == Select.BLANK:
            return

        new_command = str(event.value)
        if new_command == self.selected_command:
            return

        self.selected_command = new_command
        self._render_current_command()

    def _render_current_command(self) -> None:
        if not self.selected_command:
            self.current_arguments = []
            self.current_options = []
            self._render_params([], [])
            return

        args = extract_arguments(self.script_body, self.selected_command)
        opts = extract_options(self.script_body, self.selected_command)

        self.current_arguments = args
        self.current_options = opts
        self._render_params(args, opts)

    def _render_params(
        self,
        arguments: list[ClickCommandArgument],
        options: list[ClickCommandOption],
    ) -> None:
        container = self.query_one("#params-container", Vertical)
        container.remove_children()

        if not arguments and not options:
            container.mount(Static("No parameters required"))
            return

        for arg in arguments:
            container.mount(Input(placeholder=f"arg: {arg.name}", id=f"arg-{arg.name}"))

        for opt in options:
            default = getattr(opt, "default", None)
            value = "" if default is None else str(default)
            container.mount(
                Input(
                    placeholder=f"option:{opt.name}",
                    value=value,
                    id=f"opt-{opt.name}",
                )
            )

        first_input = container.query(Input).first()
        if first_input:
            self.call_after_refresh(first_input.focus)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "run-btn" or not self.selected_script:
            return

        cmd = [sys.executable, str(self.selected_script)]
        if self.selected_command:
            cmd.append(self.selected_command)

        container = self.query_one("#params-container", Vertical)

        # options
        for opt in self.current_options:
            widget = container.query_one(f"#opt-{opt.name}", Input)
            value = widget.value.strip() if widget else ""
            if value:
                cmd.extend([f"{opt.name}", value])

        # arguments
        for arg in self.current_arguments:
            widget = container.query_one(f"#arg-{arg.name}", Input)
            value = widget.value.strip() if widget else ""
            if not value:
                self.query_one("#output-log", RichLog).write(
                    f"[red]Missing value for argument: {arg.name}[/red]"
                )
                return
            cmd.append(value)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(self.selected_script.parent),
        )

        log = self.query_one("#output-log", RichLog)
        log.clear()
        if result.stdout:
            log.write(result.stdout)
        if result.stderr:
            log.write(f"[red]{result.stderr}[/red]")

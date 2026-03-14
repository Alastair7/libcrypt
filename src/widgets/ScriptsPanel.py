from typing import override
from pathlib import Path
import subprocess
import sys

from textual.app import ComposeResult
from textual.containers import Container, Vertical, VerticalScroll
from textual.widgets import Static, Button, RichLog, Input, Label

from utils.scripts_parser import parse_script, ScriptParam


class ParamInput(Container):
    """Widget for an individual parameter."""

    DEFAULT_CSS = """
    ParamInput {
        height: auto;
        margin: 0 0 1 0;
        layout: horizontal;
    }

    ParamInput Label {
        width: 20;
        height: 1;
        padding: 1 1 0 0;
        color: #7aa2f7;
    }

    ParamInput Input {
        width: 1fr;
        height: 3;
        border: tall #3b4261;
        background: #1a1b26;
        color: #c0caf5;
    }

    ParamInput Input:focus {
        border: tall #7aa2f7;
    }
    """

    def __init__(self, param: ScriptParam) -> None:
        super().__init__()
        self.param = param

    @override
    def compose(self) -> ComposeResult:
        type_hint = f" ({self.param.param_type})" if self.param.param_type != "str" else ""

        yield Label(f"{self.param.name}{type_hint}:")
        yield Input(
            placeholder=f"{self.param.help_text or self.param.name}"
            + (f" [default: {self.param.default}]" if self.param.default else ""),
            value=self.param.default or "",
            id=f"param-{self.param.name}",
        )


class ScriptsPanel(Container):
    DEFAULT_CSS = """
    ScriptsPanel {
        width: 1fr;
        height: 100%;
        padding: 0;
    }

    #script-info {
        height: 3;
        padding: 0 1;
        color: #7aa2f7;
        text-style: bold;
    }

    #func-name {
        height: 2;
        padding: 0 1;
        color: #bb9af7;
        text-style: bold;
    }

    #params-container {
        height: auto;
        max-height: 50%;
        padding: 1;
        border: solid #3b4261;
    }

    #no-params {
        height: 3;
        padding: 1;
        color: #565f89;
        text-style: italic;
    }

    #run-btn {
        width: 100%;
        margin: 1 0 0 0;
        background: #1a1b26;
        color: #9ece6a;
        border: tall #9ece6a;
        text-style: bold;
        display: none;
    }

    #run-btn:hover {
        background: #9ece6a;
        color: #1a1b26;
    }

    #output-label {
        height: 1;
        color: #e0af68;
        text-style: bold;
        padding: 0 1;
        display: none;
    }

    #output-log {
        height: 1fr;
        border: solid #3b4261;
        padding: 1;
        display: none;
    }
    """

    selected_script: Path | None = None
    script_params: list[ScriptParam] = []
    is_click: bool = False

    @override
    def compose(self) -> ComposeResult:
        yield Static("Select a script from the tree", id="script-info")
        with Vertical():
            yield Static("", id="func-name")
            yield VerticalScroll(id="params-container")
            yield Button("Run Script", id="run-btn")
            yield Static("-- Output --", id="output-label")
            yield RichLog(id="output-log", highlight=True, markup=True)

    def show_script(self, path: Path) -> None:
        self.selected_script = path

        info = self.query_one("#script-info", Static)
        info.update(f"Script: {path.name}")

        # Parse the script
        func_name, params = parse_script(path)
        self.script_params = params

        # Detect if it is Click
        try:
            content = path.read_text("utf-8")
            self.is_click = "@click.command" in content
        except Exception:
            self.is_click = False

        # Show function name
        func_label = self.query_one("#func-name", Static)
        script_type = "Click" if self.is_click else "Function"
        func_label.update(f"[{script_type}] {func_name}()")

        # Clear and show parameters
        params_container = self.query_one("#params-container", VerticalScroll)
        params_container.remove_children()

        if params:
            for param in params:
                params_container.mount(ParamInput(param))
        else:
            params_container.mount(Static("No parameters needed", id="no-params"))

        self.query_one("#run-btn", Button).display = True
        self.query_one("#output-label", Static).display = False
        self.query_one("#output-log", RichLog).display = False

    def _get_param_values(self) -> dict[str, str]:
        """Gets the values from the input fields."""
        values: dict[str, str] = {}
        for param_input in self.query(ParamInput):
            input_widget = param_input.query_one(Input)
            values[param_input.param.name] = input_widget.value
        return values

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run-btn" and self.selected_script:
            self._run_script(self.selected_script)

    def _run_script(self, path: Path) -> None:
        output_label = self.query_one("#output-label", Static)
        output_log = self.query_one("#output-log", RichLog)

        output_label.display = True
        output_log.display = True
        output_log.clear()

        param_values = self._get_param_values()

        # Build the command
        cmd = [sys.executable, str(path)]

        if self.is_click:
            # Click: pass as --name value
            for name, value in param_values.items():
                if value:
                    cmd.extend([f"--{name}", value])
        else:
            # Normal function: create a wrapper that calls the function with the args
            args_str = ", ".join(
                self._cast_value(param, param_values.get(param.name, ""))
                for param in self.script_params
                if param_values.get(param.name, "")
            )

            if self.script_params:
                content = path.read_text("utf-8")
                func_name = content.split("def ")[1].split("(")[0] if "def " in content else ""

                if func_name:
                    wrapper = (
                        f"import sys; sys.path.insert(0, r'{path.parent}'); "
                        f"from {path.stem} import {func_name}; "
                        f"result = {func_name}({args_str}); "
                        f"print(result) if result is not None else None"
                    )
                    cmd = [sys.executable, "-c", wrapper]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(path.parent),
            )

            if result.stdout:
                output_log.write(result.stdout)

            if result.stderr:
                output_log.write(f"[red]{result.stderr}[/red]")

            if result.returncode == 0:
                self.notify("Script executed successfully", severity="information")
            else:
                self.notify(
                    f"Script exited with code {result.returncode}", severity="error"
                )

        except subprocess.TimeoutExpired:
            output_log.write("[red]Script timed out after 30 seconds[/red]")
            self.notify("Script timed out", severity="error")
        except Exception as e:
            output_log.write(f"[red]Error: {e}[/red]")
            self.notify(f"Error: {e}", severity="error")

    @staticmethod
    def _cast_value(param: ScriptParam, value: str) -> str:
        if not value:
            return "''"
        if param.param_type == "int":
            return value
        elif param.param_type == "float":
            return value
        elif param.param_type == "bool":
            return value.capitalize()
        else:
            return f"'{value}'"
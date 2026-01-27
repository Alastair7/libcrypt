import subprocess
from typing import override

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Label, Static

from widgets.environment_selector import EnvironmentSelector


class InformationPane(Widget):
    DEFAULT_CSS = """
    InformationPane {
        border: #2a4f2c;
        max-height: 12;
    }

    #vertical {
        width: 30;
        border: solid red;
    }

    #test {
        border: solid blue;
        text-align: center;
        width: 1fr;
        height: 3;
        content-align: center middle;
    }

    InformationPane Horizontal Vertical > Static {
        border: solid cyan;
    }

    #selector {
        width: 20;
    }

    #logo {
        width: 30;
        height: 10;
        content-align: center middle;
        border: solid yellow;
    }
    """

    @override
    def compose(self) -> ComposeResult:
        with Horizontal(id="horizontal"):
            yield Static("[LOGO]", id="logo")
            yield Label("TEST", id="test")
            with Vertical(id="vertical"):
                yield EnvironmentSelector(id="selector")
                yield Static(self.get_git_branch())

    def on_mount(self) -> None:
        # Actualiza al montar
        self.update_branch()
        # Actualiza cada 5 segundos
        self.set_interval(5.0, self.update_branch)

    def update_branch(self) -> None:
        branch = self.get_git_branch()
        self.border_subtitle = f"🌿 {branch}"

    def get_git_branch(self) -> str:
        try:
            return subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                text=True,
            ).strip()
        except Exception:
            return "no-git"

from typing import override

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Static
from widgets.environment_selector import EnvironmentSelector


class InformationPane(Widget):
    DEFAULT_CSS = """
    InformationPane {
            border: #2a4f2c;
            max-height: 12;
            }

    InformationPane Horizontal {
            align: right bottom;
            }

    InformationPane Vertical {
            border: solid white;
            max-width: 50;
            }

    InformationPane Horizontal Vertical>Static {
            border: solid cyan;
            }
    #selector {
            width: 30;
            }
    """

    @override
    def compose(self) -> ComposeResult:
        with Horizontal(id="horizontal"):
            with Vertical(id="vertical"):
                yield EnvironmentSelector(id="selector")
                yield Static("testai-9999_this_is_a_test_branch")

    def on_mount(self) -> None:
        pass

from typing import override
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Select


class EnvironmentSelector(Container):
    DEFAULT_CSS = """
    EnvironmentSelector {
        width: 25;
        height: auto;
        align: right middle;
    }
       EnvironmentSelector #env-select SelectCurrent {
        width: 1fr;
        background: transparent;
        border: solid yellow;
    }

    EnvironmentSelector #env-select.dev SelectCurrent {
        width: 1fr;
        border: solid purple;
    }

    EnvironmentSelector #env-select.np SelectCurrent {
        width:1fr;
        border: solid orange;
    }

    EnvironmentSelector #env-select.prod SelectCurrent {
        width: 1fr;
        border: solid pink;
    }

    """

    @override
    def compose(self) -> ComposeResult:
        yield Select(
            options=[
                ("DEV", "dev"),
                ("NP", "np"),
                ("PROD", "prod"),
            ],
            value="dev",
            prompt="Chose an enviroment",
            id="env-select",
        )

    def on_select_changed(self, event: Select.Changed) -> None:
        select = event.select
        _ = select.remove_class("dev", "np", "prod")

        if event.value == "dev":
            _ = select.add_class("dev")
        elif event.value == "np":
            _ = select.add_class("np")
        elif event.value == "prod":
            _ = select.add_class("prod")

    def on_mount(self) -> None:
        select = self.query_one("#env-select", Select)  # pyright: ignore[reportUnknownVariableType]
        select.add_class("dev")  # pyright: ignore[reportUnusedCallResult]

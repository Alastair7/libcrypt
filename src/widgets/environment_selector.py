from typing import override
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Select


class EnvironmentSelector(Container):
    DEFAULT_CSS = """
    EnvironmentSelector {
        width: 26;
        height: auto;
        align: right middle;
    }

    EnvironmentSelector Select {
        border: none;
    }

    EnvironmentSelector SelectCurrent {
        background: #16161e;
        border: tall #3b4261;
        color: white;
    }

    EnvironmentSelector #env-select.dev SelectCurrent {
        border: tall #9ece6a; /* Verde para desarrollo */
        color: #9ece6a;
    }

    EnvironmentSelector #env-select.np SelectCurrent {
        border: tall #e0af68; /* Naranja para No-Prod */
        color: #e0af68;
    }

    EnvironmentSelector #env-select.prod SelectCurrent {
        border: tall #f7768e; /* Rojo/Rosa para Producción */
        color: #f7768e;
        text-style: bold;
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
            prompt="Environment",
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

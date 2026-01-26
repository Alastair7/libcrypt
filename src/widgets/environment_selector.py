from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Select


class EnvrionmentSelector(Container):
    DEFAULT_CSS = """
    EnvrionmentSelector {
        width: 1fr;
        height: 12;
        padding: 1 2;
        align: right middle;
        border: solid orange;
    }

    EnvrionmentSelector #env-select {
        width: 1fr;
        height: 12;
        border: solid yellow;
    }

    EnvrionmentSelector #env-select.dev {
        width: 1fr;
        height: 12;
        border: solid purple;
    }

    EnvrionmentSelector #env-select.np{
        width:1fr;
        height: 12;
        border: solid orange;
    }

    EnvrionmentSelector #env-select.prod {
        width: 1fr;
        height: 12;
        border: solid pink;
    }

    """

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
        select.remove_class("dev", "np", "prod")

        if event.value == "dev":
            select.add_class("dev")
        elif event.value == "np":
            select.add_class("np")
        elif event.value == "prod":
            select.add_class("prod")

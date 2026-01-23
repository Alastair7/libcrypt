from typing import override
from textual import events
from textual.content import Content
from textual.widgets import Static


class InformationPane(Static):
    @override
    def _on_mount(self, event: events.Mount) -> None:
        Content("Test")

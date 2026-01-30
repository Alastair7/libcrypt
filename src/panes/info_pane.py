from typing import override

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.geometry import Offset
from textual.widget import Widget
from textual.widgets import Label, Static
from pyfiglet import Figlet, FigletString

from utils.get_git_current_branch import get_git_branch
from widgets.environment_selector import EnvironmentSelector

APP_LOGO: str = """          @@@@@          
       @@       @@       
     @@   </>   @@     
   @@@   .py~~   @@@   
   @@@   .sh~~   @@@   
     @@   ~~~   @@     
       @@       @@       
          @@@@@          
"""


class InformationPane(Widget):
    DEFAULT_CSS = """
    InformationPane {
        border: #605f61;
        max-height: 12;
    }

    #vertical {
        width: 25;
        height:100%;
        content-align:right middle;
    }
    #horizontal{
    width:100%;
    }
    #test {
        text-style: bold;
    color: #71529c;
    height: auto;
    width: 1fr;
    content-align: center middle;    }

    InformationPane Horizontal Vertical > Static {
        border: solid cyan;
    }

    #selector {
        width: 20;
        height:16;
    }

    #logo {
        width: 30;
        color: white;
        height: 10;
        content-align: center middle;
        border: round gray;
    }
    """
    figlet: Figlet = Figlet(font="big")
    title: FigletString = figlet.renderText("LIBCRYPT")

    @override
    def compose(self) -> ComposeResult:
        with Horizontal(id="horizontal"):
            yield Static(id="logo", content=APP_LOGO)
            yield Label(self.title, id="test")
            with Vertical(id="vertical"):
                yield EnvironmentSelector(id="selector")

    def on_mount(self) -> None:
        self.update_branch()
        _ = self.set_interval(5.0, self.update_branch)

    def update_branch(self) -> None:
        current_git_branch: str = get_git_branch()
        self.border_subtitle: str = f"🌿 {current_git_branch}"

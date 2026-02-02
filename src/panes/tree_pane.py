from typing import override
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widget import Widget
from textual.widgets import DirectoryTree, Static, OptionList
from textual.widgets.option_list import Option
import os
import stat
import re
from pathlib import Path
from widgets.directory_tree import CategoriesTree


class TreePane(Widget):
    DEFAULT_CSS = """
    Horizontal {
            layout: horizontal;
            height: 70%;
            }
    #tree-container {
            dock: left;
            width: 35;
            height: auto;
            border: panel brown;
            }
    #content {
            width: 1fr;
            padding: 1;
            border: solid red;
            }
    #scripts-panel {
        height: 50%;
        border: solid blue;
        padding: 1;
    }
    
    #output-panel {
        height: 50%;
        border: solid green;
        padding: 1;
    }
    
    #scripts-list {
        width: 100%;
        height: 1fr;
    }
    
    #output-content {
        width: 100%;
        height: 100%;
    }
    
    .panel-title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_scripts = []

    def is_script(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read(1000)
            has_shebang = content.startswith("#!")
            pattern = r'if\s+__name__\s*==\s*["\']__main__["\']'
            has_main = bool(re.search(pattern, content))
            try:
                st = os.stat(filepath)
                is_executable = bool(st.st_mode & stat.S_IXUSR)
            except:
                is_executable = False
            return has_shebang or has_main or is_executable
        except Exception:
            return False

    def filter_paths(self, paths):
        filtered = []
        for path in paths:
            if path.is_dir():
                filtered.append(path)
        return filtered

    def get_scripts_from_directory(self, directory_path):
        scripts = []
        try:
            for item in Path(directory_path).iterdir():
                if item.is_file():
                    if (
                        item.suffix == ".py" and self.is_script(item)
                    ) or item.suffix == ".sh":
                        scripts.append(item)
        except Exception:
            pass
        return scripts

    def update_scripts_list(self, directory_path="."):
        self.current_scripts = self.get_scripts_from_directory(directory_path)

        option_list = self.query_one("#scripts-list", OptionList)
        option_list.clear_options()

        if self.current_scripts:
            for script in self.current_scripts:
                # Show just the filename, store the full path
                option_list.add_option(Option(script.name, id=str(script)))
        else:
            option_list.add_option(Option("No scripts found", id=None, disabled=True))

    @override
    def compose(self) -> ComposeResult:
        # Create DirectoryTree inline with filter
        tree = DirectoryTree("./", id="tree-container")
        # Override the filter_paths method
        tree.filter_paths = lambda paths: self.filter_paths(paths)

        with Horizontal(id="horizontal"):
            yield tree
            with Vertical(id="content"):
                # Upper panel for scripts
                with Vertical(id="scripts-panel"):
                    yield Static("Available Scripts", classes="panel-title")
                    yield OptionList(id="scripts-list")

                # Lower panel for output
                with VerticalScroll(id="output-panel"):
                    yield Static("Output", classes="panel-title")
                    yield Static("", id="output-content")

    def on_mount(self):
        """Called when widget is mounted"""
        self.update_scripts_list("./")

    def on_directory_tree_directory_selected2(
        self, event: DirectoryTree.DirectorySelected
    ):
        """Handles directory selection - update script list"""
        directory_path = str(event.path)
        self.update_scripts_list(directory_path)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        """Handles script selection from the list"""
        if event.option.id is not None:
            script_path = event.option.id

            # Update output panel
            self.query_one("#output-content", Static).update(
                f"Selected script:\n{script_path}\n"
            )

    def on_directory_tree_directory_selected(
        self, event: DirectoryTree.DirectorySelected
    ):
        """Handles directory selection - update script list"""
        directory_path = str(event.path)
        self.update_scripts_list(directory_path)

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected):
        """Handles script selection"""
        script_path = str(event.path)

        # Update scripts panel with information about selected script
        self.query_one("#scripts-list", Static).update(
            f"Selected script:\n{script_path}\n"
        )

import os
import platform
import subprocess
import webbrowser
from pathlib import Path
from typing import Union

class FileExplorerLauncher:

    def __init__(self, path: Union[str, Path]) -> None:
        self._path = path
        self._system_to_methods = {
            "Darwin" : self.open_in_macos,
            "Windows": self.open_in_windows,
            "Linux": self.open_in_linux,
        }
        
    def start(self):
        current_system = platform.system()
        func = self._system_to_methods.get(current_system, self.open_in_browser)
        return func()

    def open_in_browser(self):
        if "://" in self._path:
            return webbrowser.open(self._path)

    def open_in_macos(self):
        return subprocess.call(("open", self._path))

    def open_in_windows(self):
        return os.startfile(self._path)

    def open_in_linux(self):
        return subprocess.call(("xdg-open", self._path))
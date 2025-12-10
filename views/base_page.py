"""
Base Page class for all views
"""

import tkinter as tk
from utils.config import BG


class Page(tk.Frame):
    """Base page class that all views inherit from"""
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app

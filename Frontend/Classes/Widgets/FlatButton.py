import tkinter as tk
from tkinter import ttk

from Frontend.Classes.Components.DarkModeInterface import DarkMode


class FlatButton(ttk.Label, DarkMode):
    def __init__(self, master: tk.Misc | None, dark_mode=False, font=("Segoe UI Symbol", 10),
                 cursor="hand2", padding=(10, 5, 10, 5), command=None, **kwargs):
        ttk.Label.__init__(self, master, font=font, cursor=cursor, padding=padding, **kwargs)
        self.bind("<Button-1>", lambda _: self._execute(command))
        if "style" in kwargs.keys():
            self.style = kwargs["style"]
        else:
            self.style = "TLabel"
        self.dark_mode = dark_mode
        if dark_mode:
            ttk.Style().configure("flatbuttonactive.TLabel", background="#34373b")
        else:
            ttk.Style().configure("flatbuttonactive.TLabel", background="#DDDDDD")

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            ttk.Style().configure("flatbuttonactive.TLabel", background="#34373b")
        else:
            ttk.Style().configure("flatbuttonactive.TLabel", background="#DDDDDD")

    def _execute(self, command):
        self._sim_button()
        if command:
            command()

    def _sim_button(self):
        self.configure(style="flatbuttonactive.TLabel")
        self.after(125, func=lambda: self.configure(style=self.style))

import tkinter as tk
from tkinter import ttk
from typing import Literal


class FlatButton(ttk.Label):
    def __init__(self, master: tk.Misc | None, dark_mode=False, font=("Segoe UI Symbol", 10),
                 cursor="hand2", padding=(10, 5, 10, 5), image=None, text: float | str = "",
                 textvariable: tk.Variable = None, width: int | Literal[""] = "", wraplength=1000, command=None):
        if image:
            if width != "":
                super().__init__(master, font=font, cursor=cursor, padding=padding, image=image,
                         width=width, wraplength=wraplength)
            else:
                super().__init__(master, font=font, cursor=cursor, padding=padding, image=image, wraplength=wraplength)
        elif textvariable:
            if width != "":
                super().__init__(master, font=font, cursor=cursor, padding=padding, textvariable=textvariable,
                         width=width, wraplength=wraplength)
            else:
                super().__init__(master, font=font, cursor=cursor, padding=padding, textvariable=textvariable,
                                 wraplength=wraplength)
        else:
            if width != "":
                super().__init__(master, font=font, cursor=cursor, padding=padding, text=text,
                         width=width, wraplength=wraplength)
            else:
                super().__init__(master, font=font, cursor=cursor, padding=padding, text=text, wraplength=wraplength)
        self.bind("<Button-1>", lambda _: self._execute(command))
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
        self.after(125, func=lambda: self.configure(style="TLabel"))

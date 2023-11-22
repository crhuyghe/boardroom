import asyncio
import tkinter as tk
from tkinter import ttk
from math import ceil


class ResizingText(ttk.Frame):
    def __init__(self, master: tk.Misc | None, text: str = "", cnf: dict = None, width: int = 100, font=None,
                 dark_mode: bool = False, alt_color=False, text_padding=0, **kwargs):
        super().__init__(master, **kwargs)
        self.dark_mode = dark_mode
        self.editing_enabled = False
        self._width = width
        if type(text_padding) == int or type(text_padding) == float:
            text_padding = (text_padding, text_padding)
        if not font:
            font = ('Segoe UI Symbol', 16)
        if dark_mode:
            if alt_color:
                bg = "#292c30"
            else:
                bg = "#24272b"
            fg = "#b6bfcc"
            ins_bg = "#b6bfcc"
        else:
            if alt_color:
                bg = "#EEEEEE"
            else:
                bg = "#FFFFFF"
            fg = "#000000"
            ins_bg = "#000000"
        self.scrollbar = ttk.Scrollbar(self, orient="vertical")
        if cnf:
            if "font" in cnf.keys():
                self.text_widget = tk.Text(self, cnf=cnf, wrap="word", undo=True, maxundo=-1, bd=0, width=width, bg=bg,
                                           fg=fg, insertbackground=ins_bg, yscrollcommand=self.scrollbar.set,
                                           padx=text_padding[0], pady=text_padding[1])
            else:
                self.text_widget = tk.Text(self, cnf=cnf, wrap="word", undo=True, maxundo=-1, bd=0, width=width,
                                font=font, bg=bg, fg=fg, insertbackground=ins_bg, yscrollcommand=self.scrollbar.set,
                                padx=text_padding[0], pady=text_padding[1])
        else:
            self.text_widget = tk.Text(self, wrap="word", undo=True, maxundo=-1, bd=0, width=width, font=font, bg=bg,
                                       fg=fg, insertbackground=ins_bg, yscrollcommand=self.scrollbar.set,
                                       padx=text_padding[0], pady=text_padding[1])

        self.scrollbar.configure(command=self.text_widget.yview)

        self.text_widget.insert(1.0, text)
        height = self.text_widget.count(1.0, "end", "update", "displaylines")

        self.text_widget.configure(state="disabled", height=ceil((height/self._width)))
        self.text_widget.pack(side="left", expand=1, fill="x")

        self.after(10, self.update_size)

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            bg = "#24272b"
            fg = "#b6bfcc"
            ins_bg = "#b6bfcc"
        else:
            bg = "#FFFFFF"
            fg = "#000000"
            ins_bg = "#000000"
        self.text_widget.configure(bg=bg, fg=fg, insertbackground=ins_bg)

    def get_text(self):
        return self.text_widget.get(1.0, "end")

    def change_text(self, text):
        self.text_widget.configure(state="normal")
        self.text_widget.delete(1.0, "end")
        self.text_widget.insert(1.0, text)
        height = self.text_widget.count(1.0, "end", "update", "displaylines")
        self.text_widget.configure(height=height, state="disabled")

    def toggle_modification(self):
        self.editing_enabled = not self.editing_enabled
        if self.editing_enabled:
            self.scrollbar.pack(side="right", expand=1, fill="y")
            self.text_widget.configure(state="normal", bd=1)
            self.text_widget.focus()
        else:
            self.text_widget.configure(state="disabled", bd=0)
            self.scrollbar.pack_forget()
            self.update_size()

    def update_size(self):
        self.update_idletasks()
        height = self.text_widget.count(1.0, "end", "update", "displaylines")
        print(height, len(self.get_text().replace(" ", "")) - 1)
        if len(self.get_text().replace(" ", "")) - 1 != height or self.get_text().replace("\n", "") == "":
            self.text_widget.configure(height=height)
        else:
            self.after(10, self.update_size)


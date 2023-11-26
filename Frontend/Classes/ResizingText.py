import asyncio
import tkinter as tk
from tkinter import ttk
from math import ceil


class ResizingText(ttk.Frame):
    def __init__(self, master: tk.Misc | None, text: str = "", cnf: dict = None, width: int = 100, font=None,
                 dark_mode: bool = False, alt_color=False, dynamic=False, text_padding=0, display_text="", **kwargs):
        super().__init__(master, **kwargs)
        self.dark_mode = dark_mode
        self.alt_color = alt_color
        self.editing_enabled = False
        self.display_text = display_text
        self._dynamic = dynamic
        self._width = width

        if len(text) == 0:
            self._empty = True
        else:
            self._empty = False

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
        if cnf:
            if "font" in cnf.keys():
                self.text_widget = tk.Text(self, cnf=cnf, wrap="word", undo=True, maxundo=-1, bd=0, width=width, bg=bg,
                                           fg=fg, insertbackground=ins_bg, padx=text_padding[0], pady=text_padding[1])
            else:
                self.text_widget = tk.Text(self, cnf=cnf, wrap="word", undo=True, maxundo=-1, bd=0, width=width,
                                           font=font, bg=bg, fg=fg, insertbackground=ins_bg,
                                           padx=text_padding[0], pady=text_padding[1])
        else:
            self.text_widget = tk.Text(self, wrap="word", undo=True, maxundo=-1, bd=0, width=width, font=font, bg=bg,
                                       fg=fg, insertbackground=ins_bg, padx=text_padding[0], pady=text_padding[1])

        if dynamic:
            self.text_widget.bind("<Key>", lambda _: self._update_size())
            self.text_widget.bind("<KeyRelease>", lambda _: self._update_size())
        else:
            self.scrollbar = ttk.Scrollbar(self, orient="vertical")
            self.scrollbar.configure(command=self.text_widget.yview)
            self.text_widget.configure(yscrollcommand=self.scrollbar.set)

        self.text_widget.bind("<FocusIn>", lambda _: self.hide_display_text())
        self.text_widget.bind("<FocusOut>", lambda _: self.check_display_text())

        self.text_widget.insert(1.0, text)
        height = self.text_widget.count(1.0, "end", "update", "displaylines")
        self._height = height

        self.text_widget.configure(state="disabled", height=ceil((height / self._width)))
        self.text_widget.pack(side="left", expand=1, fill="x")

        self.text_widget.bind("<Visibility>", lambda _: self._update_size())
        self.text_widget.bind("<Configure>", lambda _: self._update_size())

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        self.hide_display_text()
        if self.dark_mode:
            if self.alt_color:
                bg = "#292c30"
            else:
                bg = "#24272b"
            fg = "#b6bfcc"
            ins_bg = "#b6bfcc"
        else:
            if self.alt_color:
                bg = "#EEEEEE"
            else:
                bg = "#FFFFFF"
            fg = "#000000"
            ins_bg = "#000000"
        self.text_widget.configure(bg=bg, fg=fg, insertbackground=ins_bg)
        self.check_display_text()

    def get_text(self):
        fg = self.text_widget.cget("foreground")
        if self._empty or fg == "#888888" or fg == "#666666":
            return ""
        else:
            return self.text_widget.get(1.0, "end")

    def change_text(self, text):
        self.text_widget.configure(state="normal")
        self.text_widget.delete(1.0, "end")
        self.text_widget.insert(1.0, text)
        height = self.text_widget.count(1.0, "end", "update", "displaylines")
        self.text_widget.configure(height=height, state="disabled")
        if len(text) == 0:
            self._empty = True
            if self.editing_enabled:
                self.check_display_text()
        else:
            self._empty = False

    def toggle_modification(self):
        self.editing_enabled = not self.editing_enabled
        if self.dark_mode:
            if self.alt_color:
                bg = "#292c30"
                alt_bg = "#24272b"
            else:
                bg = "#24272b"
                alt_bg = "#292c30"
            fg = "#b6bfcc"
        else:
            if self.alt_color:
                bg = "#EEEEEE"
                alt_bg = "#FFFFFF"
            else:
                bg = "#FFFFFF"
                alt_bg = "#EEEEEE"
            fg = "#000000"
        if self.editing_enabled:
            if not self._dynamic:
                self.scrollbar.pack(side="right", expand=1, fill="y")
                self._update_size(6)
            self.text_widget.configure(state="normal", bg=alt_bg)
            self.check_display_text()
        else:
            if not self._dynamic:
                self.scrollbar.pack_forget()
            if self._empty:
                self.change_text("")
                self.text_widget.configure(foreground=fg)
            self.text_widget.configure(state="disabled", bg=bg)
            self._update_size()

    def check_display_text(self):
        if self.editing_enabled and self.text_widget.get(1.0, "end") == "\n" and self.focus_get() != self.text_widget:
            if self.dark_mode:
                self.text_widget.configure(foreground="#888888")
            else:
                self.text_widget.configure(foreground="#666666")
            self.text_widget.insert(1.0, self.display_text)

    def hide_display_text(self):
        fg = self.text_widget.cget("foreground")
        if self.editing_enabled and (self._empty or fg == "#888888" or fg == "#666666"):
            self.text_widget.delete(1.0, "end")
            if self.dark_mode:
                self.text_widget.configure(foreground="#b6bfcc")
            else:
                self.text_widget.configure(foreground="#000000")

    def _update_size(self, min_size=0):
        self.update_idletasks()
        height = self.text_widget.count(1.0, "end", "update", "displaylines")
        self._empty = self.text_widget.get(1.0, "end").replace("\n", "") == ""
        if height != self._height:
            if (len(self.get_text().replace(" ", "")) - 1 != height or self._empty):
                self.text_widget.configure(height=max(height, min_size))
                self._height = height
            else:
                self.after(10, self._update_size)

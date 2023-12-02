import tkinter as tk
from tkinter import ttk
from datetime import datetime

from Frontend.Classes.Components.DarkModeInterface import DarkMode
from Frontend.Classes.Widgets.FlatButton import FlatButton
from Frontend.Classes.Widgets.ResizingText import ResizingText


class MessageFrame(ttk.Frame, DarkMode):
    def __init__(self, master, text, poster, message_id, edit_command, delete_command, post_time="", show_header=True, is_owned=False, is_edited=False, dark_mode=False, width=70, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)
        self.dark_mode = dark_mode
        self.show_header = show_header
        self.is_owned = is_owned
        self.message_id = message_id
        self.poster = poster
        self._text = text

        if dark_mode:
            time_color = "#999999"
            name_color = "#DDDDDD"
            menu_colors = ("#1f2226", "#b6bfcc")
        else:
            time_color = "#222222"
            name_color = "#444444"
            menu_colors = ("#eeeeee", "#000000")

        self.text_label = ResizingText(self, text, width=width, font=("Segoe UI Symbol", 10), dark_mode=dark_mode,
                                       padding=[25, 0, 0, 0])

        self.edited_label = ttk.Label(self, text="(edited)", foreground="#AAAAAA", font=("Segoe UI Symbol", 8))
        if is_edited:
            self.edited_label.grid(row=6, column=28)

        self.rc_menu = tk.Menu(self, tearoff=0, background=menu_colors[0], foreground=menu_colors[1])
        self.rc_menu.add_command(label="Copy", command=self._copy_text)
        if is_owned:
            self.rc_menu.add_command(label="Edit", command=self._enable_editing)
            self.del_menu = tk.Menu(self, tearoff=0, background=menu_colors[0], foreground=menu_colors[1])
            self.del_menu.add_command(label="Yes", command=delete_command)
            self.del_menu.add_command(label="No")
            self.rc_menu.add_cascade(label="Delete", menu=self.del_menu)

            self.cancel_edit_button = FlatButton(self, text="Cancel", dark_mode=dark_mode,
                                                 command=self._disable_editing)
            self.submit_edit_button = FlatButton(self, text="Submit Edits", dark_mode=dark_mode,
                                                 command=lambda: self._execute_edit_command(edit_command))
        self.text_label.text_widget.bind("<Button-3>", lambda e: self._popup_menu(e))

        if show_header:
            self.header_frame = ttk.Frame(self)
            post_time = datetime.strptime(post_time, '%Y-%m-%d %X.%f').strftime("%b %d, %Y at %I:%M %p")
            if post_time[16] == "0":
                post_time = post_time[:16] + post_time[17:]
            if post_time[4] == "0":
                post_time = post_time[:4] + post_time[5:]
            self.time_label = ttk.Label(self.header_frame, text=post_time, font=("Segoe UI Symbol", 10),
                                        foreground=time_color, padding=[10, 2, 0, 0])
            self.name_label = ttk.Label(self.header_frame, text=poster.name, font=("Segoe UI Bold", 12),
                                        foreground=name_color)

            self.name_label.grid(row=0, column=0, sticky="w")
            self.time_label.grid(row=0, column=1, sticky="w")
            self.header_frame.grid(row=0, column=0, columnspan=30, sticky="w")

        self.text_label.grid(row=1, column=0, rowspan=5, columnspan=30)
        self.grid_columnconfigure("all", weight=1)
        self.grid_rowconfigure("all", weight=1)

    def _execute_edit_command(self, edit_command):
        text = self.text_label.get_text()
        if len(text.replace(" ", "").replace("\n", "")) > 0 and text != self._text:
            edit_command(text)

    def _enable_editing(self):
        self.rc_menu.entryconfig("Edit", state="disabled")
        self.cancel_edit_button.grid(row=6, column=22)
        self.submit_edit_button.grid(row=6, column=23)
        self.text_label.toggle_modification()

    def _disable_editing(self):
        self.rc_menu.entryconfig("Edit", state="normal")
        self.cancel_edit_button.grid_forget()
        self.submit_edit_button.grid_forget()
        self.text_label.toggle_modification()
        self.text_label.change_text(self._text)

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            if self.show_header:
                self.time_label.configure(foreground="#999999")
                self.name_label.configure(foreground="#DDDDDD")
            self.rc_menu.configure(background="#1f2226", foreground="#b6bfcc")
            if self.is_owned:
                self.del_menu.configure(background="#1f2226", foreground="#b6bfcc")
        else:
            if self.show_header:
                self.time_label.configure(foreground="#222222")
                self.name_label.configure(foreground="#444444")
            self.rc_menu.configure(background="#eeeeee", foreground="#000000")
            if self.is_owned:
                self.del_menu.configure(background="#eeeeee", foreground="#000000")
        self.text_label.swap_mode()
        if self.is_owned:
            self.submit_edit_button.swap_mode()
            self.cancel_edit_button.swap_mode()

    def _popup_menu(self, event):
        try:
            self.rc_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.rc_menu.grab_release()

    def _copy_text(self):
        text = self.text_label.get_text()
        self.clipboard_clear()
        self.clipboard_append(text)

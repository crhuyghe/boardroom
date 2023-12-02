import asyncio
import tkinter as tk
from tkinter import ttk, StringVar
from datetime import datetime

from Frontend.Classes.Components.DarkModeInterface import DarkMode
from Frontend.Classes.Widgets.FlatButton import FlatButton
from Frontend.Classes.Widgets.ResizingText import ResizingText
from Frontend.Classes.Components.UserFrame import UserFrame


class BoardroomFrame(ttk.Frame, DarkMode):
    def __init__(self, master, title, text, like_command, edit_command, delete_command, reply_command, view_count, like_count, poster, post_time, post_id, is_edited=False, is_owned=False, is_liked=False, dark_mode=False, width=60, **kwargs):
        """Holds the original post from a boardroom discussion"""
        ttk.Frame.__init__(self, master, **kwargs)
        self.post_id = post_id
        self.poster = poster
        self.is_liked = is_liked
        self.is_edited = is_edited
        self.is_owned = is_owned
        self.dark_mode = dark_mode
        self._text = text

        if dark_mode:
            time_foreground = "#a6afbc"
            self.liked_image = tk.PhotoImage(file="Assets/liked_dark.png")
            self.not_liked_image = tk.PhotoImage(file="Assets/not_liked_dark.png")
            menu_colors = ("#1f2226", "#b6bfcc")
        else:
            time_foreground = "#222222"
            self.liked_image = tk.PhotoImage(file="Assets/liked_light.png")
            self.not_liked_image = tk.PhotoImage(file="Assets/not_liked_light.png")
            menu_colors = ("#eeeeee", "#000000")

        self.title_label = ResizingText(self, title, dark_mode=dark_mode, width=width, font=("Segoe UI Historic", 24),
                                        padding=[0, 0, 0, 5], text_padding=(10, 5), alt_color=True)

        self.text_label = ResizingText(self, text=text, dark_mode=dark_mode, width=int(width*(5/6)),
                                       padding=[30, 5, 0, 10])

        self.rc_menu = tk.Menu(self, tearoff=0, background=menu_colors[0], foreground=menu_colors[1])
        self.rc_menu.add_command(label="Copy", command=lambda: self._copy_text())
        if is_owned:
            self.rc_menu.add_command(label="Edit", command=lambda: self._enable_editing(edit_command))
            self.del_menu = tk.Menu(self, tearoff=0, background=menu_colors[0], foreground=menu_colors[1])
            self.del_menu.add_command(label="Yes", command=lambda: delete_command(post_id))
            self.del_menu.add_command(label="No")
            self.rc_menu.add_cascade(label="Delete", menu=self.del_menu)
        self.text_label.text_widget.bind("<Button-3>", lambda e: self._popup_menu(e))

        self.like_button = ttk.Label(self, padding=0, cursor="hand2")
        self.like_button.bind("<Button-1>", lambda x: self._execute_like_command(like_command))

        if is_liked:
            self.like_button.configure(image=self.liked_image)
        else:
            self.like_button.configure(image=self.not_liked_image)

        self.like_count = StringVar()
        self.like_count.set(str(like_count))
        self.like_count_label = ttk.Label(self, textvariable=self.like_count, padding=5, font=("Segoe UI Historic", 8))

        self.view_count = StringVar()
        self.view_count.set(str(view_count) + " views")
        self.view_count_label = ttk.Label(self, textvariable=self.view_count, padding=5, font=("Segoe UI Historic", 8))

        if is_owned:
            self.edit_text = StringVar()
            self.edit_text.set("Edit Post")
            self.edit_button = FlatButton(self, textvariable=self.edit_text, dark_mode=dark_mode,
                                          command=lambda: self._enable_editing(edit_command))
            self.delete_text = StringVar()
            self.delete_text.set("Delete Post")
            self.delete_button = FlatButton(self, textvariable=self.delete_text, dark_mode=dark_mode,
                                            command=lambda: self._execute_delete_command(delete_command))

            self.cancel_edit_button = FlatButton(self, text="Cancel", dark_mode=dark_mode,
                                                 command=lambda: self._disable_editing(edit_command))

            self.edit_button.grid(row=6, column=23)
            self.delete_button.grid(row=6, column=24)

        self.edited_label = ttk.Label(self, text="(edited)", foreground="#AAAAAA", font=("Segoe UI Symbol", 8))
        if is_edited:
            self.edited_label.grid(row=6, column=27, columnspan=3)

        post_time = datetime.strptime(post_time, '%Y-%m-%d %X.%f').strftime("%b %d, %Y at %I:%M %p")
        if post_time[16] == "0":
            post_time = post_time[:16] + post_time[17:]
        if post_time[4] == "0":
            post_time = post_time[:4] + post_time[5:]
        self.time_label = ttk.Label(self, text=post_time, font=("Segoe UI Symbol", 8), foreground=time_foreground)
        self.time_label.grid(row=6, column=26)

        self.reply_button = FlatButton(self, text="Reply", dark_mode=dark_mode, command=reply_command)
        self.reply_button.grid(row=6, column=25)

        self.user_frame = UserFrame(self, poster)

        self.like_button.grid(row=2, column=0, sticky="s")
        self.like_count_label.grid(row=3, column=0, sticky="n")
        self.view_count_label.grid(row=1, column=0, sticky="n")
        self.title_label.grid(row=0, column=0, columnspan=30, sticky="nsew")
        self.text_label.grid(row=1, column=1, rowspan=5, columnspan=29, sticky="nsew")
        self.user_frame.grid(row=6, column=0, columnspan=3)
        self.grid_columnconfigure("all", weight=1)
        self.grid_rowconfigure("all", weight=1)

    def _execute_like_command(self, like_command):
        self.is_liked = not self.is_liked
        if self.is_liked:
            self.like_button.configure(image=self.liked_image)
            self.like_count.set(str(int(self.like_count.get()) + 1))
        else:
            self.like_button.configure(image=self.not_liked_image)
            self.like_count.set(str(int(self.like_count.get()) - 1))
        like_command(self.post_id)

    def _execute_delete_command(self, delete_command):
        self.delete_text.set("Are you sure?")
        self.delete_button.configure(foreground="red")
        self.delete_button.change_command(lambda: delete_command(self.post_id))
        self.delete_button.after(5000, lambda: self._reset_delete_button(delete_command))

    def _reset_delete_button(self, delete_command):
        self.delete_text.set("Delete Post")
        if self.dark_mode:
            self.delete_button.configure(foreground="#b6bfcc")
        else:
            self.delete_button.configure(foreground="#000000")
        self.delete_button.change_command(lambda: self._execute_delete_command(delete_command))

    def _execute_edit_command(self, edit_command):
        text = self.text_label.get_text()
        if len(text.replace(" ", "").replace("\n", "")) > 0 and text != self._text:
            edit_command(text, self.post_id)

    def _enable_editing(self, edit_command):
        self.edit_text.set("Submit Edits")
        self.rc_menu.entryconfig("Edit", state="disabled")
        self.edit_button.change_command(lambda: self._execute_edit_command(edit_command))
        self.cancel_edit_button.grid(row=6, column=22)
        self.text_label.toggle_modification()

    def _disable_editing(self, edit_command):
        self.edit_text.set("Edit Post")
        self.rc_menu.entryconfig("Edit", state="normal")
        self.edit_button.change_command(lambda: self._enable_editing(edit_command))
        self.cancel_edit_button.grid_forget()
        self.text_label.toggle_modification()
        self.text_label.change_text(self._text)

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.liked_image.configure(file="Assets/liked_dark.png")
            self.not_liked_image.configure(file="Assets/not_liked_dark.png")
            self.time_label.configure(foreground="#a6afbc")
            self.rc_menu.configure(background="#1f2226", foreground="#b6bfcc")
            ttk.Style().configure("title.TLabel", background="#292c30")
            if self.is_owned:
                self.del_menu.configure(background="#1f2226", foreground="#b6bfcc")
        else:
            self.liked_image.configure(file="Assets/liked_light.png")
            self.not_liked_image.configure(file="Assets/not_liked_light.png")
            self.time_label.configure(foreground="#222222")
            self.rc_menu.configure(background="#eeeeee", foreground="#000000")
            ttk.Style().configure("title.TLabel", background="#EEEEEE")
            if self.is_owned:
                self.del_menu.configure(background="#eeeeee", foreground="#000000")
        if self.is_liked:
            self.like_button.configure(image=self.liked_image)
        else:
            self.like_button.configure(image=self.not_liked_image)
        self.title_label.swap_mode()
        self.text_label.swap_mode()
        self.reply_button.swap_mode()
        if self.is_owned:
            self.edit_button.swap_mode()
            self.delete_button.swap_mode()
            self.cancel_edit_button.swap_mode()

    def tag_edited(self):
        if not self.is_edited:
            self.is_edited = True
            self.edited_label.grid(row=6, column=27)

    def _popup_menu(self, event):
        try:
            self.rc_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.rc_menu.grab_release()

    def _copy_text(self):
        text = self.text_label.get_text()
        self.clipboard_clear()
        self.clipboard_append(text)

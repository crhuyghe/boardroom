import asyncio
import tkinter as tk
from tkinter import ttk, StringVar
from datetime import datetime

from Frontend.Classes.FlatButton import FlatButton
from Frontend.Classes.ResizingText import ResizingText
from Frontend.Classes.UserFrame import UserFrame
from boardroomApp import AsyncGUI


class BoardroomFrame(ttk.Frame):
    def __init__(self, master, title, text, like_command, edit_command, delete_command, reply_command, like_count, poster, post_time, post_id, is_edited=False, is_owned=False, is_liked=False, dark_mode=False, width=60):
        super().__init__(master)
        self.post_id = post_id
        self.poster = poster
        self.is_liked = is_liked
        self.is_edited = is_edited
        self.is_owned = is_owned
        self.dark_mode = dark_mode

        if dark_mode:
            time_foreground = "#a6afbc"
            self.liked_image = tk.PhotoImage(file="Frontend/Assets/liked_dark.png")
            self.not_liked_image = tk.PhotoImage(file="Frontend/Assets/not_liked_dark.png")
        else:
            time_foreground = "#222222"
            self.liked_image = tk.PhotoImage(file="Frontend/Assets/liked_light.png")
            self.not_liked_image = tk.PhotoImage(file="Frontend/Assets/not_liked_light.png")

        self.title_label = ResizingText(self, title, dark_mode=dark_mode, width=width, font=("Segoe UI Historic", 24),
                                        padding=[0, 0, 0, 5], text_padding=(10, 5), alt_color=True)

        self.text_label = ResizingText(self, text=text, dark_mode=dark_mode, width=int(width*(5/6)),
                                       padding=[30, 5, 0, 10])

        self.like_button = ttk.Label(self, padding=0, cursor="hand2")
        self.like_button.bind("<Button-1>", lambda x: self.execute_like_command(like_command))

        if is_liked:
            self.like_button.configure(image=self.liked_image)
        else:
            self.like_button.configure(image=self.not_liked_image)

        self.like_count = StringVar()
        self.like_count.set(str(like_count))
        self.like_count_label = ttk.Label(self, textvariable=self.like_count, padding=5,
                                          font=("Segoe UI Historic", 8))

        if is_owned:
            self.edit_button = FlatButton(self, text="Edit Post", dark_mode=dark_mode, command=edit_command)
            self.delete_button = FlatButton(self, text="Delete Post", dark_mode=dark_mode, command=delete_command)

            self.edit_button.grid(row=6, column=23)
            self.delete_button.grid(row=6, column=24)

        self.edited_label = ttk.Label(self, text="(edited)", foreground="#AAAAAA", font=("Segoe UI Symbol", 8))
        if is_edited:
            self.edited_label.grid(row=6, column=27)

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
        self.title_label.grid(row=0, column=0, columnspan=30, sticky="nsew")
        self.text_label.grid(row=1, column=1, rowspan=5, columnspan=29, sticky="nsew")
        self.user_frame.grid(row=6, column=0, columnspan=3)
        self.grid_columnconfigure("all", weight=1)
        self.grid_rowconfigure("all", weight=1)

    def execute_like_command(self, like_command):
        self.is_liked = not self.is_liked
        if self.is_liked:
            self.like_button.configure(image=self.liked_image)
            self.like_count.set(str(int(self.like_count.get()) + 1))
        else:
            self.like_button.configure(image=self.not_liked_image)
            self.like_count.set(str(int(self.like_count.get()) - 1))
        like_command()

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.liked_image.configure(file="Frontend/Assets/liked_dark.png")
            self.not_liked_image.configure(file="Frontend/Assets/not_liked_dark.png")
            self.time_label.configure(foreground="#a6afbc")
            ttk.Style().configure("title.TLabel", background="#292c30")
        else:
            self.liked_image.configure(file="Frontend/Assets/liked_light.png")
            self.not_liked_image.configure(file="Frontend/Assets/not_liked_light.png")
            self.time_label.configure(foreground="#222222")
            ttk.Style().configure("title.TLabel", background="#EEEEEE")
        if self.is_liked:
            self.like_button.configure(image=self.liked_image)
        else:
            self.like_button.configure(image=self.not_liked_image)
        self.text_label.swap_mode()
        self.reply_button.swap_mode()
        if self.is_owned:
            self.edit_button.swap_mode()
            self.delete_button.swap_mode()

    def tag_edited(self):
        if not self.is_edited:
            self.is_edited = True
            self.edited_label.grid(row=6, column=27)

    def _run_as_task(self, func, *args):
        loop = asyncio.get_event_loop()
        task = loop.create_task(func(*args))
        AsyncGUI.tasks.add(task)
        task.add_done_callback(AsyncGUI.tasks.discard)

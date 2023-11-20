import asyncio
import tkinter as tk
from tkinter import ttk, StringVar
from datetime import datetime

from Frontend.Classes.UserFrame import UserFrame

class ReplyFrame(ttk.Frame):
    def __init__(self, master, text, like_command, edit_command, delete_command, run_as_task, like_count, poster,
                 post_time, reply_id,
                 is_edited=False, is_owned=False, is_liked=False, dark_mode=False, text_width=850):
        super().__init__(master)
        self.reply_id = reply_id
        self.poster = poster
        self.is_liked = is_liked
        self.is_edited = is_edited
        self.dark_mode = dark_mode
        self.run_as_task = run_as_task

        self.label_text = StringVar()
        self.label_text.set(text)

        self.text_label = ttk.Label(self, textvariable=self.label_text, padding=[25, 0, 0, 0], wraplength=text_width,
                                    font=("Segoe UI Symbol", 14))
        if dark_mode:
            button_background = "#34373b"
            time_foreground = "#a6afbc"
            self.liked_image = tk.PhotoImage(file="Frontend/Assets/liked_dark.png")
            self.liked_image = self.liked_image.subsample(4)
            self.not_liked_image = tk.PhotoImage(file="Frontend/Assets/not_liked_dark.png")
            self.not_liked_image = self.not_liked_image.subsample(4)
        else:
            button_background = "#DDDDDD"
            time_foreground = "#222222"
            self.liked_image = tk.PhotoImage(file="Frontend/Assets/liked_light.png")
            self.liked_image = self.liked_image.subsample(4)
            self.not_liked_image = tk.PhotoImage(file="Frontend/Assets/not_liked_light.png")
            self.not_liked_image = self.not_liked_image.subsample(4)

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

        ttk.Style().configure("postbottom.TLabel", font=("Segoe UI Symbol", 10), padding=[10, 5, 10, 5])
        ttk.Style().configure("postbottomactive.TLabel", font=("Segoe UI Symbol", 10), padding=[10, 5, 10, 5],
                              background=button_background)
        if is_owned:
            self.edit_button = ttk.Label(self, text="Edit Reply", style="postbottom.TLabel", cursor="hand2")
            self.edit_button.bind("<Button-1>", lambda x: self.execute_button_command(self.edit_button, edit_command))

            self.delete_button = ttk.Label(self, text="Delete Reply", style="postbottom.TLabel", cursor="hand2")
            self.delete_button.bind("<Button-1>", lambda x: self.execute_button_command(self.delete_button, delete_command))

            self.edit_button.grid(row=6, column=24)
            self.delete_button.grid(row=6, column=25)

        if is_edited:
            self.edited_label = ttk.Label(self, text="(edited)", foreground="#AAAAAA", font=("Segoe UI Symbol", 8))
            self.edited_label.grid(row=6, column=27)

        post_time = datetime.strptime(str(post_time), '%Y-%m-%d %X.%f').strftime("%b %d, %Y at %I:%M %p")
        if post_time[16] == "0":
            post_time = post_time[:16] + post_time[17:]
        if post_time[4] == "0":
            post_time = post_time[:4] + post_time[5:]
        self.time_label = ttk.Label(self, text=post_time, font=("Segoe UI Symbol", 8), foreground="#222222")
        self.time_label.grid(row=6, column=26)

        self.user_frame = UserFrame(self, poster)

        self.like_button.grid(row=1, column=0, sticky="s")
        self.like_count_label.grid(row=2, column=0, sticky="n")
        self.text_label.grid(row=1, column=1, rowspan=5, columnspan=29, sticky="nsew")
        self.user_frame.grid(row=6, column=0, columnspan=3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def execute_like_command(self, like_command):
        self.is_liked = not self.is_liked
        if self.is_liked:
            self.like_button.configure(image=self.liked_image)
            self.like_count.set(str(int(self.like_count.get()) + 1))
        else:
            self.like_button.configure(image=self.not_liked_image)
            self.like_count.set(str(int(self.like_count.get()) - 1))
        like_command()

    def execute_button_command(self, button, command):
        self.run_as_task(self.sim_button, button)
        command()

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.liked_image.configure(file="Frontend/Assets/liked_dark.png")
            self.liked_image = self.liked_image.subsample(4)
            self.not_liked_image.configure(file="Frontend/Assets/not_liked_dark.png")
            self.not_liked_image = self.not_liked_image.subsample(4)
            self.time_label.configure(foreground="#a6afbc")
            ttk.Style().configure("postbottomactive.TLabel", background="#34373b")
        else:
            self.liked_image.configure(file="Frontend/Assets/liked_light.png")
            self.liked_image = self.liked_image.subsample(4)
            self.not_liked_image.configure(file="Frontend/Assets/not_liked_light.png")
            self.not_liked_image = self.not_liked_image.subsample(4)
            self.time_label.configure(foreground="#222222")
            ttk.Style().configure("postbottomactive.TLabel", background="#DDDDDD")
        if self.is_liked:
            self.like_button.configure(image=self.liked_image)
        else:
            self.like_button.configure(image=self.not_liked_image)

    def modify_text(self, text):
        self.label_text.set(text)
        if not self.is_edited:
            self.is_edited = True
            self.edited_label.grid(row=6, column=27)

    async def sim_button(self, button: ttk.Button):
        button.configure(style="postbottomactive.TLabel")
        await asyncio.sleep(.125)
        button.configure(style="postbottom.TLabel")

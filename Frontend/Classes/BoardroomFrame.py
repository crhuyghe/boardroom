import asyncio
import tkinter as tk
from tkinter import ttk, StringVar
from datetime import datetime

from Frontend.Classes.UserFrame import UserFrame


class BoardroomFrame(ttk.Frame):
    def __init__(self, master, title, text, like_command, edit_command, delete_command, reply_command, run_as_task, like_count, poster, post_time, post_id, is_edited=False, is_owned=False, is_liked=False, dark_mode=False, width=1200):
        super().__init__(master)
        self.post_id = post_id
        self.poster = poster
        self.is_liked = is_liked
        self.is_edited = is_edited
        self.dark_mode = dark_mode
        self.run_as_task = run_as_task

        self.label_text = StringVar()
        self.label_text.set(text)

        if dark_mode:
            title_background = "#292c30"
            button_background = "#34373b"
            time_foreground = "#a6afbc"
            self.liked_image = tk.PhotoImage(file="Frontend/Assets/liked_dark.png")
            self.liked_image = self.liked_image.subsample(4)
            self.not_liked_image = tk.PhotoImage(file="Frontend/Assets/not_liked_dark.png")
            self.not_liked_image = self.not_liked_image.subsample(4)
        else:
            title_background = "#EEEEEE"
            button_background = "#DDDDDD"
            time_foreground = "#222222"
            self.liked_image = tk.PhotoImage(file="Frontend/Assets/liked_light.png")
            self.liked_image = self.liked_image.subsample(4)
            self.not_liked_image = tk.PhotoImage(file="Frontend/Assets/not_liked_light.png")
            self.not_liked_image = self.not_liked_image.subsample(4)

        ttk.Style().configure("title.TLabel", font=("Segoe UI Historic", 24), background=title_background)
        self.title_frame = ttk.Frame(self, padding=[0, 0, 0, 5])
        self.title_label = ttk.Label(self.title_frame, text=title, justify="left", style="title.TLabel",
                                     padding=[10, 0, 0, 5], wraplength=width)

        self.text_label = ttk.Label(self, textvariable=self.label_text, padding=[25, 0, 0, 0], wraplength=int(width*(5/6)))

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
            self.edit_button = ttk.Label(self, text="Edit Post", style="postbottom.TLabel", cursor="hand2")
            self.edit_button.bind("<Button-1>", lambda x: self.execute_button_command(self.edit_button, edit_command))

            self.delete_button = ttk.Label(self, text="Delete Post", style="postbottom.TLabel", cursor="hand2")
            self.delete_button.bind("<Button-1>", lambda x: self.execute_button_command(self.delete_button, delete_command))

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

        self.reply_button = ttk.Label(self, text="Reply", style="postbottom.TLabel", cursor="hand2")
        self.reply_button.bind("<Button-1>", lambda x: self.execute_button_command(self.reply_button, reply_command))
        self.reply_button.grid(row=6, column=25)

        self.user_frame = UserFrame(self, poster)

        self.like_button.grid(row=2, column=0, sticky="n")
        self.like_count_label.grid(row=2, column=0, sticky="s")
        self.title_frame.grid(row=0, column=0, columnspan=30, sticky="nsew")
        self.title_label.pack(anchor="w", fill="x", expand=1)
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
            ttk.Style().configure("title.TLabel", background="#292c30")
        else:
            self.liked_image.configure(file="Frontend/Assets/liked_light.png")
            self.liked_image = self.liked_image.subsample(4)
            self.not_liked_image.configure(file="Frontend/Assets/not_liked_light.png")
            self.not_liked_image = self.not_liked_image.subsample(4)
            self.time_label.configure(foreground="#222222")
            ttk.Style().configure("postbottomactive.TLabel", background="#DDDDDD")
            ttk.Style().configure("title.TLabel", background="#EEEEEE")
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


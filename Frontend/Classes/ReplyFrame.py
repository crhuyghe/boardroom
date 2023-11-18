import tkinter as tk
from tkinter import ttk, StringVar
from datetime import datetime

from Frontend.Classes.UserFrame import UserFrame


def __init__(self, master, text, like_command, edit_command, delete_command, like_count, poster, post_time, reply_id,
             is_edited=False, is_owned=False, is_liked=False, text_width=850):
    super().__init__(master)
    self.reply_id = reply_id
    self.poster = poster
    self.is_liked = is_liked
    self.is_edited = is_edited

    self.label_text = StringVar()
    self.label_text.set(text)

    self.text_label = ttk.Label(self, textvariable=self.label_text, padding=[25, 0, 0, 0], wraplength=text_width,
                                font=("Segoe UI Symbol", 14))

    self.liked_image = tk.PhotoImage(file="Frontend/Assets/liked.png")
    self.liked_image = self.liked_image.subsample(2)
    self.not_liked_image = tk.PhotoImage(file="Frontend/Assets/not_liked.png")
    self.not_liked_image = self.not_liked_image.subsample(2)

    self.like_button = self.like_button = ttk.Button(self, style="like.TButton",
                                                     command=lambda: self.execute_like_command(like_command),
                                                     padding=0)
    if is_liked:
        self.like_button.configure(image=self.liked_image)
    else:
        self.like_button.configure(image=self.not_liked_image)

    self.like_count = StringVar()
    self.like_count.set(str(like_count))
    self.like_count_label = ttk.Label(self, textvariable=self.like_count, padding=5,
                                      font=("Segoe UI Historic", 8))

    ttk.Style().configure("postbottom.TButton", font=("Segoe UI Symbol", 10), padding=0)
    if is_owned:
        self.edit_button = ttk.Button(self, text="Edit Reply", command=edit_command, style="postbottom.TButton")
        self.delete_button = ttk.Button(self, text="Delete Reply", command=delete_command,
                                        style="postbottom.TButton")
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

    self.like_button.grid(row=1, column=0)
    self.like_count_label.grid(row=2, column=0)
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

    def modify_text(self, text):
        self.label_text.set(text)
        if not self.is_edited:
            self.is_edited = True
            self.edited_label.grid(row=6, column=27)

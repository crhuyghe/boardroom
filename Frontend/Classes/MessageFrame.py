from tkinter import ttk, StringVar
from datetime import datetime

from Frontend.Classes.ResizingText import ResizingText


class MessageFrame(ttk.Frame):
    def __init__(self, master, text, poster, message_id, post_time="", show_header=True, dark_mode=False, width=70, padding=0):
        super().__init__(master, padding=padding)
        self.dark_mode = dark_mode
        self.message_id = message_id
        self.poster = poster

        self.text_label = ResizingText(self, text, width=width, font=("Segoe UI Symbol", 10), dark_mode=True,
                                       padding=[25, 0, 0, 0])

        if show_header:
            self.header_frame = ttk.Frame(self)
            post_time = datetime.strptime(post_time, '%Y-%m-%d %X.%f').strftime("%b %d, %Y at %I:%M %p")
            if post_time[16] == "0":
                post_time = post_time[:16] + post_time[17:]
            if post_time[4] == "0":
                post_time = post_time[:4] + post_time[5:]
            if dark_mode:
                self.time_label = ttk.Label(self.header_frame, text=post_time, font=("Segoe UI Symbol", 10),
                                            foreground="#999999", padding=[10, 2, 0, 0])
                self.name_label = ttk.Label(self.header_frame, text=poster.name, font=("Segoe UI Bold", 12),
                                            foreground="#DDDDDD")
            else:
                self.time_label = ttk.Label(self.header_frame, text=post_time, font=("Segoe UI Symbol", 10), foreground="#222222", padding=[10,2, 0, 0])
                self.name_label = ttk.Label(self.header_frame, text=poster.name, font=("Segoe UI Bold", 12), foreground="#444444")

            self.name_label.grid(row=0, column=0, sticky="w")
            self.time_label.grid(row=0, column=1, sticky="w")
            self.header_frame.grid(row=0, column=0, columnspan=30, sticky="w")

        self.text_label.grid(row=1, column=0, rowspan=5, columnspan=30)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.time_label.configure(foreground="#999999")
            self.name_label.configure(foreground="#DDDDDD")
        else:
            self.time_label.configure(foreground="#222222")
            self.name_label.configure(foreground="#444444")
        self.text_label.swap_mode()

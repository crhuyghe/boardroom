from tkinter import ttk, StringVar
from datetime import datetime

class MessageFrame(ttk.Frame):
    def __init__(self, master, text, poster, message_id, post_time="", show_header=True, text_width=700):
        super().__init__(master)
        self.message_id = message_id
        self.poster = poster

        self.label_text = StringVar()
        self.label_text.set(text)

        self.text_label = ttk.Label(self, textvariable=self.label_text, padding=[25, 0, 0, 0], wraplength=text_width,
                                    font=("Segoe UI Symbol", 10))

        if show_header:
            self.header_frame = ttk.Frame(self)
            post_time = datetime.strptime(post_time, '%Y-%m-%d %X.%f').strftime("%b %d, %Y at %I:%M %p")
            if post_time[16] == "0":
                post_time = post_time[:16] + post_time[17:]
            if post_time[4] == "0":
                post_time = post_time[:4] + post_time[5:]
            self.time_label = ttk.Label(self.header_frame, text=post_time, font=("Segoe UI Symbol", 10), foreground="#222222", padding=[10,2, 0, 0])
            self.name_label = ttk.Label(self.header_frame, text=poster.name, font=("Segoe UI Bold", 12))

            self.name_label.grid(row=0, column=0, sticky="w")
            self.time_label.grid(row=0, column=1, sticky="w")
            self.header_frame.grid(row=0, column=0, columnspan=30, sticky="w")

        self.text_label.grid(row=1, column=0, rowspan=5, columnspan=30)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

from datetime import datetime
from tkinter import ttk

from Frontend.Classes.Components.DarkModeInterface import DarkMode
from Frontend.Classes.Components.UserFrame import UserFrame


class ResultFrame(ttk.Frame, DarkMode):

    def __init__(self, master, title, text, tags, view_count, like_count, reply_count, poster, post_id, post_time,
                 open_command=None, dark_mode=False, width=120, **kwargs):
        if dark_mode:
            stat_fg = "#a6afbc"
            ttk.Style().configure(f"tagframe{post_id}.TFrame", background="#34373b")
            ttk.Style().configure(f"tag{post_id}.TLabel", background="#2f3236")
            ttk.Style().configure(f"result{post_id}.TFrame", background="#24272b")
            ttk.Style().configure(f"result{post_id}.TLabel", background="#24272b", foreground="#b6bfcc")
        else:
            stat_fg = "#222222"
            ttk.Style().configure(f"tagframe{post_id}.TFrame", background="#DDDDDD")
            ttk.Style().configure(f"tag{post_id}.TLabel", background="#E2E2E2")
            ttk.Style().configure(f"result{post_id}.TFrame", background="#EEEEEE")
            ttk.Style().configure(f"result{post_id}.TLabel", background="#EEEEEE", foreground="#000000")
        ttk.Frame.__init__(self, master, style=f"result{post_id}.TFrame", **kwargs)

        self.dark_mode = dark_mode
        self.poster = poster
        self.post_id = post_id

        self.title_label = ttk.Label(self, text=title, style=f"result{post_id}.TLabel", font=("Segoe UI Symbol", 18))

        if len(text) > width * 4:
            try:
                last_word = text.rindex(" ", 0, width * 4),
            except ValueError:
                last_word = (width * 4,)
            text = text[:last_word[0]] + "..."

        self.text_label = ttk.Label(self, text=text, wraplength=width * 8, font=("Segoe UI Symbol", 10),
                                    padding=[25, 0, 0, 20], style=f"result{post_id}.TLabel")

        post_time = datetime.strptime(post_time, '%Y-%m-%d %X.%f').strftime("%b %d, %Y at %I:%M %p")
        if post_time[16] == "0":
            post_time = post_time[:16] + post_time[17:]
        if post_time[4] == "0":
            post_time = post_time[:4] + post_time[5:]
        self.time_label = ttk.Label(self, text=post_time, font=("Segoe UI Symbol", 10), foreground=stat_fg,
                                    style=f"result{post_id}.TLabel")

        self.view_count_label = ttk.Label(self, text=str(view_count) + " views", font=("Segoe UI Symbol", 10),
                                          foreground=stat_fg, style=f"result{post_id}.TLabel")
        self.like_count_label = ttk.Label(self, text=str(like_count) + " likes", font=("Segoe UI Symbol", 10),
                                          foreground=stat_fg, style=f"result{post_id}.TLabel")
        self.reply_count_label = ttk.Label(self, text=str(reply_count) + " replies", font=("Segoe UI Symbol", 10),
                                          foreground=stat_fg, style=f"result{post_id}.TLabel")

        self.poster_frame = UserFrame(self, poster, style=f"result{post_id}.TFrame", padding=[0, 0, 0, 10])
        self.poster_frame.name_label.configure(style=f"result{post_id}.TLabel")
        self.poster_frame.email_label.configure(style=f"result{post_id}.TLabel")

        self.tag_frame = ttk.Frame(self, padding=[10, 5, 0, 5], style=f"tagframe{post_id}.TFrame")
        self.tag_list = []
        for tag in tags:
            tag_label = ttk.Label(self.tag_frame, style=f"tag{post_id}.TLabel", text=tag, padding=5,
                                  font=("Segoe UI Symbol", 8))
            tag_label.pack(side="left", padx=(0, 10))
            self.tag_list.append(tag_label)

        self.title_label.grid(row=0, column=0, columnspan=30, sticky="w")
        self.text_label.grid(row=1, column=0, columnspan=30, sticky="nw")
        self.time_label.grid(row=2, column=27, columnspan=3)
        self.reply_count_label.grid(row=2, column=24, columnspan=3, sticky="w")
        self.like_count_label.grid(row=2, column=21, columnspan=3)
        self.view_count_label.grid(row=2, column=18, columnspan=3, sticky="e")
        self.poster_frame.grid(row=2, column=0, columnspan=3)
        self.tag_frame.grid(row=3, column=0, columnspan=30, sticky="nswe")

        self.grid_columnconfigure("all", weight=1)
        # self.grid_rowconfigure("all", weight=1)

        self.bind("<Button-1>", lambda _: self._execute(open_command))
        self.title_label.bind("<Button-1>", lambda _: self._execute(open_command))
        self.text_label.bind("<Button-1>", lambda _: self._execute(open_command))
        self.poster_frame.bind("<Button-1>", lambda _: self._execute(open_command))
        self.view_count_label.bind("<Button-1>", lambda _: self._execute(open_command))
        self.like_count_label.bind("<Button-1>", lambda _: self._execute(open_command))
        self.reply_count_label.bind("<Button-1>", lambda _: self._execute(open_command))
        self.time_label.bind("<Button-1>", lambda _: self._execute(open_command))
        self.tag_frame.bind("<Button-1>", lambda _: self._execute(open_command))
        for tag_label in self.tag_list:
            tag_label.bind("<Button-1>", lambda _: self._execute(open_command))

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            stat_fg = "#a6afbc"
            ttk.Style().configure(f"tagframe{self.post_id}.TFrame", background="#34373b")
            ttk.Style().configure(f"tag{self.post_id}.TLabel", background="#2f3236")
            ttk.Style().configure(f"result{self.post_id}.TFrame", background="#24272b")
            ttk.Style().configure(f"result{self.post_id}.TLabel", background="#24272b", foreground="#b6bfcc")
        else:
            stat_fg = "#222222"
            ttk.Style().configure(f"tagframe{self.post_id}.TFrame", background="#DDDDDD")
            ttk.Style().configure(f"tag{self.post_id}.TLabel", background="#E2E2E2")
            ttk.Style().configure(f"result{self.post_id}.TFrame", background="#EEEEEE")
            ttk.Style().configure(f"result{self.post_id}.TLabel", background="#EEEEEE", foreground="#000000")
        self.view_count_label.configure(foreground=stat_fg)
        self.like_count_label.configure(foreground=stat_fg)
        self.reply_count_label.configure(foreground=stat_fg)
        self.time_label.configure(foreground=stat_fg)

    def _execute(self, command):
        self._sim_button()
        if command:
            command(self.post_id)

    def _sim_button(self):
        if self.dark_mode:
            ttk.Style().configure(f"tagframe{self.post_id}.TFrame", background="#44474b")
            ttk.Style().configure(f"tag{self.post_id}.TLabel", background="#3f4246")
            ttk.Style().configure(f"result{self.post_id}.TFrame", background="#34373b")
            ttk.Style().configure(f"result{self.post_id}.TLabel", background="#34373b")

            self.after(125, func=lambda: ttk.Style().configure(f"tagframe{self.post_id}.TFrame", background="#34373b"))
            self.after(125, func=lambda: ttk.Style().configure(f"tag{self.post_id}.TLabel", background="#2f3236"))
            self.after(125, func=lambda: ttk.Style().configure(f"result{self.post_id}.TFrame", background="#24272b"))
            self.after(125, func=lambda: ttk.Style().configure(f"result{self.post_id}.TLabel", background="#24272b"))
        else:
            ttk.Style().configure(f"tagframe{self.post_id}.TFrame", background="#CCCCCC")
            ttk.Style().configure(f"tag{self.post_id}.TLabel", background="#D3D3D3")
            ttk.Style().configure(f"result{self.post_id}.TFrame", background="#DDDDDD")
            ttk.Style().configure(f"result{self.post_id}.TLabel", background="#DDDDDD")

            self.after(125, func=lambda: ttk.Style().configure(f"tagframe{self.post_id}.TFrame", background="#DDDDDD"))
            self.after(125, func=lambda: ttk.Style().configure(f"tag{self.post_id}.TLabel", background="#E2E2E2"))
            self.after(125, func=lambda: ttk.Style().configure(f"result{self.post_id}.TFrame", background="#EEEEEE"))
            self.after(125, func=lambda: ttk.Style().configure(f"result{self.post_id}.TLabel", background="#EEEEEE"))

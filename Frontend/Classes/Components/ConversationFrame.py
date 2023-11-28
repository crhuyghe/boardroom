from datetime import datetime
from tkinter import ttk


class ConversationFrame(ttk.Frame):
    def __init__(self, master, recipient, last_message: str, open_command=None, message_time="", dark_mode=False, width=60, **kwargs):
        if dark_mode:
            time_color = "#999999"
            name_color = "#DDDDDD"
            ttk.Style().configure("conversation.TFrame", background="#1f2226")
            ttk.Style().configure("conversationactive.TFrame", background="#2f3236")
            ttk.Style().configure("conversation.TLabel", background="#1f2226", foreground="#b6bfcc")
            ttk.Style().configure("conversationactive.TLabel", background="#2f3236", foreground="#b6bfcc")
            email_color = "#969fac"
        else:
            ttk.Style().configure("conversation.TFrame", background="#DDDDDD")
            ttk.Style().configure("conversationactive.TFrame", background="#BBBBBB")
            ttk.Style().configure("conversation.TLabel", background="#DDDDDD", foreground="#000000")
            ttk.Style().configure("conversationactive.TLabel", background="#BBBBBB", foreground="#000000")
            time_color = "#222222"
            name_color = "#444444"
            email_color = "#666666"

        super().__init__(master, style="conversation.TFrame", **kwargs)

        self.dark_mode = dark_mode
        self.recipient = recipient

        self.header_frame = ttk.Frame(self, padding=[0, 5, 0, 5], style="conversation.TFrame")
        self.name_label = ttk.Label(self.header_frame, text=recipient.name, font=("Segoe UI Bold", 20),
                                    foreground=name_color, style="conversation.TLabel")
        self.email_label = ttk.Label(self.header_frame, text="(" + recipient.email + ")", font=("Segoe UI Bold", 12),
                                    foreground=email_color, style="conversation.TLabel", padding=[20, 5, 0, 5])

        message_time = datetime.strptime(message_time, '%Y-%m-%d %X.%f').strftime("%m/%d/%Y\n%I:%M %p")
        if message_time[11] == "0":
            message_time = message_time[:11] + message_time[12:]
        if message_time[3] == "0":
            message_time = message_time[:3] + message_time[4:]
        if message_time[0] == "0":
            message_time = message_time[1:]
        self.time_label = ttk.Label(self, text=message_time, font=("Segoe UI Symbol", 10), foreground=time_color,
                                    style="conversation.TLabel", padding=[20, 0, 0, 40], justify="center")

        if len(last_message) > width*2:
            try:
                last_word = last_message.rindex(" ", 0, width*2),
            except ValueError:
                last_word = (width*2, )
            last_message = last_message[:last_word[0]] + "..."

        # self.text_label = ResizingText(self, last_message, width=width, font=("Segoe UI Symbol", 10),
        #                                dark_mode=dark_mode, padding=[25, 0, 0, 0])
        self.text_label = ttk.Label(self, text=last_message, wraplength=width*8, font=("Segoe UI Symbol", 10),
                                    style="conversation.TLabel", padding=[25, 0, 0, 0])

        self.name_label.grid(row=0, column=0, sticky="sw")
        self.email_label.grid(row=0, column=1, sticky="s")
        self.header_frame.grid(row=0, column=0, columnspan=30, sticky="w")

        self.text_label.grid(row=1, column=0, columnspan=30, sticky="n")
        self.time_label.grid(row=1, column=30, sticky="n")

        # self.grid_columnconfigure("all", weight=1)
        # self.grid_rowconfigure("all", weight=1)
        self.bind("<Button-1>", lambda _: self._execute(open_command))
        self.header_frame.bind("<Button-1>", lambda _: self._execute(open_command))
        self.text_label.bind("<Button-1>", lambda _: self._execute(open_command))
        self.time_label.bind("<Button-1>", lambda _: self._execute(open_command))
        self.name_label.bind("<Button-1>", lambda _: self._execute(open_command))
        self.email_label.bind("<Button-1>", lambda _: self._execute(open_command))

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.time_label.configure(foreground="#999999")
            self.name_label.configure(foreground="#DDDDDD")
            self.email_label.configure(foreground="#969fac")
            ttk.Style().configure("conversation.TFrame", background="#1f2226")
            ttk.Style().configure("conversationactive.TFrame", background="#2f3236")
            ttk.Style().configure("conversation.TLabel", background="#1f2226", foreground="#b6bfcc")
            ttk.Style().configure("conversationactive.TLabel", background="#2f3236", foreground="#b6bfcc")
            ttk.Style().configure("border.TFrame", background="#969fac")
        else:
            self.time_label.configure(foreground="#222222")
            self.name_label.configure(foreground="#444444")
            self.email_label.configure(foreground="#666666")
            ttk.Style().configure("conversation.TFrame", background="#DDDDDD")
            ttk.Style().configure("conversationactive.TFrame", background="#BBBBBB")
            ttk.Style().configure("conversation.TLabel", background="#DDDDDD", foreground="#000000")
            ttk.Style().configure("conversationactive.TLabel", background="#BBBBBB", foreground="#000000")
            ttk.Style().configure("border.TFrame", background="#666666")

    def _execute(self, command):
        self._sim_button()
        if command:
            command(self.recipient.id)

    def _sim_button(self):
        self.configure(style="conversationactive.TFrame")
        self.header_frame.configure(style="conversationactive.TFrame")
        self.name_label.configure(style="conversationactive.TLabel")
        self.email_label.configure(style="conversationactive.TLabel")
        self.time_label.configure(style="conversationactive.TLabel")
        self.text_label.configure(style="conversationactive.TLabel")
        self.after(125, func=lambda: self.configure(style="conversation.TFrame"))
        self.after(125, func=lambda: self.header_frame.configure(style="conversation.TFrame"))
        self.after(125, func=lambda: self.name_label.configure(style="conversation.TLabel"))
        self.after(125, func=lambda: self.email_label.configure(style="conversation.TLabel"))
        self.after(125, func=lambda: self.time_label.configure(style="conversation.TLabel"))
        self.after(125, func=lambda: self.text_label.configure(style="conversation.TLabel"))

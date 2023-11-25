import tkinter as tk
import asyncio
from datetime import datetime, timedelta
from tkinter import ttk, StringVar
from ttkthemes import ThemedTk
import pandas as pd

from Classes.Models.User import User
from Frontend.Classes.FlatButton import FlatButton
from Frontend.Classes.MessageFrame import MessageFrame
from Frontend.Classes.ResizingText import ResizingText
from Frontend.Classes.UserFrame import UserFrame
from boardroomApp import AsyncGUI


class DirectMessagesFrame(ttk.Frame):
    def __init__(self, master, database_response, current_user, edit_command, delete_command, dark_mode=False):
        super().__init__(master)
        self.dark_mode = dark_mode
        self.current_user = current_user
        self.recipient = database_response["recipient"]
        self.recipient = User(self.recipient["id"], self.recipient["email"], self.recipient["name"])

        self.messages = database_response["messages"]
        self.message_frames = []

        if self.dark_mode:
            ttk.Style().configure("headerfooter.TFrame", background="#1f2226")
            ttk.Style().configure("headerfooter.TLabel", background="#1f2226")
            name_fg = "#DDDDDD"
            email_fg = "#AAAAAA"
        else:
            ttk.Style().configure("headerfooter.TFrame", background="#DDDDDD")
            ttk.Style().configure("headerfooter.TLabel", background="#DDDDDD")
            name_fg = "#111111"
            email_fg = "#AAAAAA"

        # Displays current conversation and edit/delete buttons
        self.header_frame = ttk.Frame(self, style="headerfooter.TFrame", padding=20)

        # Displays current messages
        self.messages_frame = ttk.Frame(self, padding=[0, 0, 0, 20])

        # Displays input
        self.footer_frame = ttk.Frame(self, style="headerfooter.TFrame", padding=20)

        self.user_label = ttk.Frame(self.header_frame, style="headerfooter.TFrame")
        name = ttk.Label(self.user_label, text=self.recipient.name, font=("Segoe UI Historic", 22),
                         foreground=name_fg, style="headerfooter.TLabel")
        email = ttk.Label(self.user_label, text=self.recipient.email, font=("Segoe UI Historic", 12),
                        foreground=email_fg, style="headerfooter.TLabel")
        name.pack(side="top", anchor="w")
        email.pack(side="top")

        self.user_label.pack(side="left")

        for i in range(len(self.messages)-1, -1, -1):
            if self.messages[i]["sender_message"]:
                sender = self.current_user
            else:
                sender = self.recipient

            if i > 0 and self.messages[i-1]["id"] == sender.id:
                prev_time = datetime.strptime(self.messages[i-1]["time"], '%Y-%m-%d %X.%f')
                curr_time = datetime.strptime(self.messages[i]["time"], '%Y-%m-%d %X.%f')
                if prev_time + timedelta(minutes=2) > curr_time:
                    header = False
                    post_time = ""
                    padding = [0, 5, 0, 0]
                else:
                    header = True
                    post_time = self.messages[i]["time"]
                    padding = [0, 10, 0, 0]
            else:
                header = True
                post_time = self.messages[i]["time"]
                padding = [0, 10, 0, 0]

            message = MessageFrame(self.messages_frame, self.messages[i]["text"], sender, self.messages[i]["id"],
                                   edit_command, delete_command, post_time, header, self.messages[i]["sender_message"],
                                   self.messages[i]["message_is_edited"], dark_mode, padding=padding)

            message.pack(side="bottom", fill="x")
            self.message_frames.append(message)

        self.send_box = ResizingText(self.footer_frame, padding=5, width=50, dark_mode=dark_mode,
                                     text_padding=(5, 5), dynamic=True, display_text=f"Send to {self.recipient.name}")
        self.send_box.toggle_modification()

        # self.send_button =
        self.send_box.pack(side="left", fill="x", expand=True)

        self.header_frame.grid(row=0, column=0, sticky="nswe")
        self.messages_frame.grid(row=1, column=0, sticky="s")
        self.footer_frame.grid(row=2, column=0, sticky="nswe")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # self.header_frame.pack(side="top", expand=1, fill="x", anchor="n")
        # self.footer_frame.pack(side="bottom", expand=1, fill="x")
        # self.messages_frame.pack(side="bottom", expand=1, fill="y")

    def swap_mode(self):
        for frame in self.message_frames:
            frame.swap_mode()


loop = asyncio.get_event_loop()
window = AsyncGUI(loop)
s = ttk.Style()
s.configure('.', font=('Segoe UI Symbol', 16), background="#24272b", foreground="#b6bfcc")
# s.configure('.', font=('Segoe UI Symbol', 16))
func = lambda: print("hi")
func2 = lambda _: print("hi")
format = lambda x: x.strftime('%Y-%m-%d %X.%f')
user = User(0, "cave.johnson@aperture.com", "Cave Johnson")
time = datetime.strptime(str(pd.Timestamp.now()), '%Y-%m-%d %X.%f')
text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
response = {"success": True, "recipient": {"name": "Caroline", "email": "caroline@aperture.com", "picture": False,
            "id": 2}, "messages": [
            {"sender_message": True, "text": text, "message_is_edited": False, "id": 0, "time": format(time+timedelta(minutes=0))},
            {"sender_message": False, "text": text, "message_is_edited": False, "id": 0, "time": format(time+timedelta(minutes=5))},
            {"sender_message": False, "text": text, "message_is_edited": True, "id": 0, "time": format(time+timedelta(minutes=6))},
            {"sender_message": True, "text": text, "message_is_edited": False, "id": 0, "time": format(time+timedelta(minutes=7))},
            {"sender_message": True, "text": text, "message_is_edited": False, "id": 0, "time": format(time+timedelta(minutes=16))}
            ]}
new_frame = DirectMessagesFrame(window, response, user, func2, func2, True)
# new_frame = BoardroomFrame(window, "This is a title. Deal with it.", text, func2, func2, func2, func2, 1337, user,
#                            str(pd.Timestamp.now()), 0, True, True, True, True)
# new_frame = ReplyFrame(window, text, func, func, func, 1337, user, str(pd.Timestamp.now()), 0, 0, True, True, True, True)
# new_frame = MessageFrame(window, text, user, 0, func2, func2, str(pd.Timestamp.now()), True, True, True, True)

# new_frame.swap_mode()

new_frame.pack(expand=1, fill="both")

# text_box = ResizingText(window, dynamic=True, display_text="Message Cave Johnson", dark_mode=True, width=30)
# text_box2 = ResizingText(window, dynamic=True, text=text, display_text="This is a test", dark_mode=False, width=30)
#
# text_box.after(1000, text_box.toggle_modification)
# # text_box.after(20000, text_box.toggle_modification)
#
# text_box.pack(side="top")
# text_box2.pack(side="bottom")

loop.run_forever()
loop.close()

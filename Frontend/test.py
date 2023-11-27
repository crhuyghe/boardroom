import asyncio
from datetime import datetime, timedelta
from tkinter import ttk
import pandas as pd

from Backend.Classes.Models.User import User
from Frontend.Classes.Widgets.FlatButton import FlatButton
from Frontend.Classes.Components.MessageFrame import MessageFrame
from Frontend.Classes.Widgets.ResizingText import ResizingText
from Frontend.Classes.Widgets.ScrollFrame import ScrollFrame
from Frontend.boardroomApp import AsyncGUI


class DirectMessagesFrame(ttk.Frame):
    def __init__(self, master, database_response, current_user, edit_command, delete_command, send_command,
                 dark_mode=False):
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
        self.message_list = ScrollFrame(self, dark_mode)

        # Displays input
        self.footer_frame = ttk.Frame(self, style="headerfooter.TFrame", padding=20)

        self.user_label = ttk.Frame(self.header_frame, style="headerfooter.TFrame")
        self.name_label = ttk.Label(self.user_label, text=self.recipient.name, font=("Segoe UI Historic", 22),
                         foreground=name_fg, style="headerfooter.TLabel")
        self.email_label = ttk.Label(self.user_label, text=self.recipient.email, font=("Segoe UI Historic", 12),
                        foreground=email_fg, style="headerfooter.TLabel")
        self.name_label.pack(side="top", anchor="w")
        self.email_label.pack(side="top")

        self.user_label.pack(side="left")

        for i in range(len(self.messages)):
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

            message = MessageFrame(self.message_list.frame, self.messages[i]["text"], sender,
                                   self.messages[i]["id"], edit_command, delete_command, post_time, header,
                                   self.messages[i]["sender_message"], self.messages[i]["message_is_edited"],
                                   dark_mode, 90, padding)

            message.pack(side="top")

            self.message_frames.append(message)
        self.message_list.canvas.update_idletasks()
        self.message_list.canvas.yview_moveto("1.0")

        self.send_box = ResizingText(self.footer_frame, padding=5, width=50, dark_mode=dark_mode, text_padding=(5, 5),
                                     dynamic=True, display_text=f"Send to {self.recipient.name}",
                                     font=("Segoe UI Symbol", 12))
        self.send_box.toggle_modification()

        self.send_button = FlatButton(self.footer_frame, dark_mode=dark_mode, text="Send",
                                      command=lambda: send_command(self.send_box.get_text(), self.recipient.id))

        self.send_button.pack(side="right", padx=(30, 0))
        self.send_box.pack(side="left", fill="x", expand=True)

        self.header_frame.grid(row=0, column=0, sticky="nswe")
        self.message_list.grid(row=1, column=0, sticky="nsew")
        self.footer_frame.grid(row=2, column=0, sticky="nswe")

        self.grid_rowconfigure(1, weight=20)
        self.grid_rowconfigure(0, weight=1)

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        for frame in self.message_frames:
            frame.swap_mode()
        self.message_list.swap_mode()
        self.send_box.swap_mode()
        self.send_button.swap_mode()
        if self.dark_mode:
            ttk.Style().configure("headerfooter.TFrame", background="#1f2226")
            ttk.Style().configure("headerfooter.TLabel", background="#1f2226")
            self.name_label.configure(foreground="#DDDDDD")
        else:
            ttk.Style().configure("headerfooter.TFrame", background="#DDDDDD")
            ttk.Style().configure("headerfooter.TLabel", background="#DDDDDD")
            self.name_label.configure(foreground="#111111")



loop = asyncio.get_event_loop()
window = AsyncGUI(loop)
# window = ThemedTk(theme="adapta")
s = ttk.Style()
# s.configure('.', font=('Segoe UI Symbol', 16), background="#24272b", foreground="#b6bfcc")
s.configure('.', font=('Segoe UI Symbol', 16))
func = lambda: print("hi")
func2 = lambda _: print("hi")
func3 = lambda _, __=None: print("hi")
format = lambda x: x.strftime('%Y-%m-%d %X.%f')
user = User(0, "cave.johnson@aperture.com", "Cave Johnson")
time = datetime.strptime(str(pd.Timestamp.now()), '%Y-%m-%d %X.%f')
text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
response = {"success": True, "recipient": {"name": "Caroline", "email": "caroline@aperture.com", "picture": False,
            "id": 2}, "messages": [
            {"sender_message": True, "text": text, "message_is_edited": False, "id": 0, "time": format(time+timedelta(minutes=0))},
            {"sender_message": False, "text": text, "message_is_edited": False, "id": 1, "time": format(time+timedelta(minutes=5))},
            {"sender_message": False, "text": text, "message_is_edited": True, "id": 2, "time": format(time+timedelta(minutes=6))},
            {"sender_message": True, "text": text, "message_is_edited": False, "id": 3, "time": format(time+timedelta(minutes=7))},
            {"sender_message": True, "text": text, "message_is_edited": False, "id": 4, "time": format(time+timedelta(minutes=16))},
            {"sender_message": True, "text": text, "message_is_edited": False, "id": 5, "time": format(time+timedelta(minutes=17))},
            {"sender_message": True, "text": text, "message_is_edited": False, "id": 6, "time": format(time+timedelta(minutes=18))},
            {"sender_message": True, "text": text, "message_is_edited": False, "id": 7, "time": format(time+timedelta(minutes=19))},
            ]}
# response = {"success": True, "post_title": "On lemons: a memoir by Cave Johnson", "post_id": 0,
#             "post_creator": {"name": "Cave Johnson", "email": "cave.johnson@aperture.com", "picture": False, "id": 0},
#             "post_likes": 243694, "post_views": 999999, "post_text": text, "post_tags": ["lemons", "aperture"],
#             "post_time": format(time+timedelta(minutes=0)), "post_is_liked": False, "post_is_edited": True,
#             "post_replies": [
#                 {"reply_likes": 596, "reply_text": text, "reply_is_liked": True, "reply_is_edited": False,
#                  "reply_id": 0,
#                  "reply_creator": {"name": "Caroline", "email": "caroline@aperture.com", "picture": False, "id": 2},
#                  "reply_time": format(time+timedelta(days=3))},
#                 {"reply_likes": 596, "reply_text": text, "reply_is_liked": False, "reply_is_edited": False,
#                  "reply_id": 0,
#                  "reply_creator": {"name": "Bill Cipher", "email": "bcipher@gmail.com", "picture": False, "id": 3},
#                  "reply_time": format(time+timedelta(days=3))},
#                 {"reply_likes": 596, "reply_text": text, "reply_is_liked": True, "reply_is_edited": True,
#                  "reply_id": 0,
#                  "reply_creator": {"name": "Bill Cipher", "email": "bcipher@gmail.com", "picture": False, "id": 3},
#                  "reply_time": format(time+timedelta(days=3))},
#                 {"reply_likes": 596, "reply_text": text, "reply_is_liked": False, "reply_is_edited": True,
#                  "reply_id": 0,
#                  "reply_creator": {"name": "Cave Johnson", "email": "cave.johnson@aperture.com", "picture": False, "id": 0},
#                  "reply_time": format(time+timedelta(days=3))},
#             ]}
new_frame = DirectMessagesFrame(window, response, user, func2, func2, func3, False)
# new_frame = BoardroomFrame(window, "This is a title. Deal with it.", text, func2, func2, func2, func2, 5, 1337, user,
#                            str(pd.Timestamp.now()), 0, True, True, True, True)
# new_frame = ReplyFrame(window, text, func, func, func, 1337, user, str(pd.Timestamp.now()), 0, 0, True, True, True, True)
# new_frame = MessageFrame(window, text, user, 0, func2, func2, str(pd.Timestamp.now()), True, True, True, True)
# new_frame = FullPostFrame(window, response, user, func3, func3, func3, func3, False)

# new_frame.swap_mode()

new_frame.pack(expand=1, fill="both")
# new_frame.after(3000, new_frame.swap_mode)
# new_frame.after(3000, lambda: s.configure('.', font=('Segoe UI Symbol', 16), background="#24272b", foreground="#b6bfcc"))
#
# new_frame.after(5000, new_frame.destroy)

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
# window.mainloop()

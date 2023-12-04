import asyncio
from datetime import datetime, timedelta
from tkinter import ttk, BooleanVar, StringVar
import pandas as pd
import tkinter as tk

from Backend.Classes.Models.User import User
from Frontend.Classes.Components.BoardroomFrame import BoardroomFrame
from Frontend.Classes.Components.ConversationFrame import ConversationFrame
from Frontend.Classes.Components.DarkModeInterface import DarkMode
from Frontend.Classes.Components.ReplyFrame import ReplyFrame
from Frontend.Classes.Components.ResultFrame import ResultFrame
from Frontend.Classes.Components.UserFrame import UserFrame
# from Frontend.Classes.Screens.HeaderFrame import HeaderFrame
from Frontend.Classes.Widgets.FlatButton import FlatButton
from Frontend.Classes.Components.MessageFrame import MessageFrame
from Frontend.Classes.Widgets.ResizingText import ResizingText
from Frontend.Classes.Widgets.ScrollFrame import ScrollFrame
from Frontend.boardroomApp import AsyncGUI

class FullPostFrame(ttk.Frame, DarkMode):
    def __init__(self, master, database_response, current_user, like_command, edit_command, delete_command,
                 reply_command, dark_mode=False, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)
        self.dark_mode = dark_mode

        if dark_mode:
            ttk.Style().configure("replybar.TFrame", background="#1f2226")
            ttk.Style().configure("replybar.TLabel", background="#1f2226", foreground="#b6bfcc")
        else:
            ttk.Style().configure("replybar.TFrame", background="#DDDDDD")
            ttk.Style().configure("replybar.TLabel", background="#DDDDDD", foreground="#000000")

        self.scrollframe = ScrollFrame(self, dark_mode)

        poster = database_response["post_creator"]
        poster = User(poster["id"], poster["email"], poster["name"])
        self.boardroom_frame = BoardroomFrame(self.scrollframe.frame, database_response["post_title"],
                                              database_response["post_text"], like_command, edit_command,
                                              delete_command, self._show_reply_box, database_response["post_views"],
                                              database_response["post_likes"], poster, database_response["post_time"],
                                              database_response["post_id"], database_response["post_is_edited"],
                                              current_user.id == poster.id, database_response["post_is_liked"],
                                              dark_mode, padding=[0, 0, 0, 50])

        self.reply_list = []

        self.boardroom_frame.pack(side="top", fill="x", expand=1, padx=(100, 50))
        for reply in database_response["post_replies"]:
            replier = reply["reply_creator"]
            replier = User(replier["id"], replier["email"], replier["name"])
            reply_frame = ReplyFrame(self.scrollframe.frame, reply["reply_text"], like_command, edit_command,
                                     delete_command, reply["reply_likes"], replier, reply["reply_time"],
                                     reply["reply_id"], self.boardroom_frame.post_id, reply["reply_is_edited"],
                                     current_user.id == replier.id, reply["reply_is_liked"], dark_mode, padding=10)
            reply_frame.pack(side="top", fill="x", expand=1, padx=(200, 100))
            self.reply_list.append(reply_frame)

        self.scrollframe.grid(row=0, column=0, sticky="nswe")

        self.reply_frame = ttk.Frame(self, style="replybar.TFrame", padding=20)

        self.reply_label = ttk.Label(self.reply_frame, text="Enter your reply in the box below",
                                      font=("Segoe UI Bold", 18), style="replybar.TLabel")
        self.reply_entry = ResizingText(self.reply_frame, dark_mode=dark_mode, text_padding=(5, 5),
                                        padding=5, display_text="Enter some reply text...\n\n", width=100,
                                        font=("Segoe UI Symbol", 12), min_height=5)
        self.submit_reply_button = FlatButton(self.reply_frame, dark_mode=dark_mode, text="Send Reply",
                                              command=lambda: self._execute_reply_command(reply_command))
        self.hide_reply_button = FlatButton(self.reply_frame, dark_mode=dark_mode, text="X", foreground="#AAAAAA",
                                            command=self._hide_reply_box)

        self.reply_entry.toggle_modification()

        self.reply_label.grid(row=0, column=1)
        self.reply_entry.grid(row=1, column=1, pady=(20, 20))
        self.submit_reply_button.grid(row=2, column=1)
        self.hide_reply_button.grid(row=0, column=2, sticky="ne", padx=(20, 20), pady=(20, 20))
        self.reply_frame.grid_columnconfigure(0, weight=1)
        self.reply_frame.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _execute_reply_command(self, reply_command):
        text = self.reply_entry.get_text()
        if len(text.replace(" ", "").replace("\n", "")) > 0:
            reply_command(self.boardroom_frame.post_id, text)

    def _show_reply_box(self):
        self.reply_frame.grid(row=1, column=0, sticky="sew")

    def _hide_reply_box(self):
        self.reply_frame.grid_forget()

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            ttk.Style().configure("replybar.TFrame", background="#1f2226")
            ttk.Style().configure("replybar.TLabel", background="#1f2226", foreground="#b6bfcc")
        else:
            ttk.Style().configure("replybar.TFrame", background="#DDDDDD")
            ttk.Style().configure("replybar.TLabel", background="#DDDDDD", foreground="#000000")
        self.scrollframe.swap_mode()
        self.boardroom_frame.swap_mode()
        self.reply_entry.swap_mode()
        self.submit_reply_button.swap_mode()
        self.hide_reply_button.swap_mode()
        for reply_frame in self.reply_list:
            reply_frame.swap_mode()



loop = asyncio.get_event_loop()
window = AsyncGUI(loop)
# window = ThemedTk(theme="adapta")
s = ttk.Style()
# s.configure('.', font=('Segoe UI Symbol', 16), background="#24272b", foreground="#b6bfcc")
s.configure('.', font=('Segoe UI Symbol', 16))
func = lambda: print("hi")
func2 = lambda _: print("hi")
func3 = lambda _, __=None, ___=None: print("hi")
format = lambda x: x.strftime('%Y-%m-%d %X.%f')
user = User(0, "cave.johnson@aperture.com", "Cave Johnson")
time = datetime.strptime(str(pd.Timestamp.now()), '%Y-%m-%d %X.%f')
# text = "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
# Direct Message test
# response = {"success": True, "recipient": {"name": "Caroline", "email": "caroline@aperture.com", "picture": False,
#             "id": 2}, "messages": [
#             {"sender_message": True, "text": text, "message_is_edited": False, "id": 0, "time": format(time+timedelta(minutes=0))},
#             {"sender_message": False, "text": text, "message_is_edited": False, "id": 1, "time": format(time+timedelta(minutes=5))},
#             {"sender_message": False, "text": text, "message_is_edited": True, "id": 2, "time": format(time+timedelta(minutes=6))},
#             {"sender_message": True, "text": text, "message_is_edited": False, "id": 3, "time": format(time+timedelta(minutes=7))},
#             {"sender_message": True, "text": text, "message_is_edited": False, "id": 4, "time": format(time+timedelta(minutes=16))},
#             {"sender_message": True, "text": text, "message_is_edited": False, "id": 5, "time": format(time+timedelta(minutes=17))},
#             {"sender_message": True, "text": text, "message_is_edited": False, "id": 6, "time": format(time+timedelta(minutes=18))},
#             {"sender_message": True, "text": text, "message_is_edited": False, "id": 7, "time": format(time+timedelta(minutes=19))},
#             ]}

# Boardroom + Reply test
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

# Conversations test
# response = {"success": True, "conversations": [
#     {"recipient": {"name": "Caroline", "email": "caroline@aperture.com", "picture": False, "id": 2}, "last_message": text, "last_message_time": format(time+timedelta(minutes=0))},
#     {"recipient": {"name": "Bill Cipher", "email": "bcipher@gmail", "picture": False, "id": 3}, "last_message": text, "last_message_time": format(time-timedelta(days=76))},
#     {"recipient": {"name": "Chell", "email": "chell@aperture.com", "picture": False, "id": 4}, "last_message": text, "last_message_time": format(time-timedelta(days=98))},
#     {"recipient": {"name": "Wheatley", "email": "wheatley@aperture.com", "picture": False, "id": 5}, "last_message": text, "last_message_time": format(time-timedelta(weeks=57))},
#     {"recipient": {"name": "Batman", "email": "bwayne@gmail.com", "picture": False, "id": 6}, "last_message": text, "last_message_time": format(time-timedelta(weeks=157))},
#     {"recipient": {"name": "Steve Jobs", "email": "sjobs@apple.com", "picture": False, "id": 7}, "last_message": text, "last_message_time": format(time-timedelta(weeks=257))},
#             ]}
# response = {"success": True, "conversations": []}

response = {"success": True, "post_title": "Post Title", "post_id": 0, "post_creator": {"name": "Cave Johnson", "email": "cave.johnson@aperture.com", "picture": False, "id": 0}, "post_likes": 1, "post_views": 7, "post_text": "When life gives you lemons, don't make lemonade! Get mad!", "post_tags": ["test", "post", "test2"], "post_time": "2023-11-03 13:11:32.541756", "post_is_liked": False, "post_is_edited": True, "post_replies": [{"reply_likes": 1, "reply_text": "You tell 'em Cave!", "reply_is_liked": True, "reply_is_edited": False, "reply_id": 0, "reply_creator": {"name": "Cave Johnson", "email": "cave.johnson@aperture.com", "picture": False, "id": 0}, "reply_time": "2023-11-04 11:23:24.469726"}, {"reply_likes": 0, "reply_text": "No lemonade here!", "reply_is_liked": False, "reply_is_edited": False, "reply_id": 1, "reply_creator": {"name": "Cave Johnson", "email": "cave.johnson@aperture.com", "picture": False, "id": 0}, "reply_time": "2023-11-04 13:21:46.511837"}, {"reply_likes": 1, "reply_text": "This post sucks", "reply_is_liked": True, "reply_is_edited": False, "reply_id": 2, "reply_creator": {"name": "Cave Johnson", "email": "cave.johnson@aperture.com", "picture": False, "id": 0}, "reply_time": "2023-11-16 14:12:22.695086"}]}

# Search Results test
# response = {'success': True, 'posts': [{'post_title': 'Post Title', 'post_text': "When life gives you lemons, don't make lemonade! Get mad!", 'post_creator': {'name': 'Cave Johnson', 'email': 'cave.johnson@aperture.com', 'picture': False, 'id': 0}, 'post_id': 0, 'post_likes': 1, 'post_views': 7, 'post_time': '2023-11-03 13:11:32.541756', 'post_replies': 3, 'post_tags': ['test', 'post', 'test2']}, {'post_title': 'test post', 'post_text': 'Insert text here', 'post_creator': {'name': 'Test Testington', 'email': 'test@test.com', 'picture': False, 'id': 1}, 'post_id': 2, 'post_likes': 0, 'post_views': 0, 'post_time': '2023-11-06 14:15:56.022726', 'post_replies': 0, 'post_tags': ['test', 'post']}, {'post_title': 'Post Title 2', 'post_text': 'post text', 'post_creator': {'name': 'Cave Johnson', 'email': 'cave.johnson@aperture.com', 'picture': False, 'id': 0}, 'post_id': 1, 'post_likes': 1, 'post_views': 0, 'post_time': '2023-11-03 13:12:31.812848', 'post_replies': 0, 'post_tags': ['post', 'title', 'post-title', 'post-title2']}]}
# response = {"success": True, "posts": []}

# new_frame = DirectMessagesFrame(window, response, user, func3, func3, func3, False)
# new_frame = BoardroomFrame(window, "This is a title. Deal with it.", text, func2, func3, func2, func2, 5, 1337, user,
#                            str(pd.Timestamp.now()), 0, True, True, True, False)
# new_frame = ReplyFrame(window, text, func2, func3, func3, 1337, user, str(pd.Timestamp.now()), 0, 0, True, True, True)
# new_frame = MessageFrame(window, text, user, 0, func, func, str(pd.Timestamp.now()), True, True, True)
new_frame = FullPostFrame(window, response, user, func3, func3, func3, func3, )
# new_frame = ConversationFrame(window, user, text, func2, str(pd.Timestamp.now()), False)
# new_frame = ConversationSidebarFrame(window, response, func3, func3, False)
# new_frame = HomeFrame(window, True)
# new_frame = CreateAccountFrame(window)
# new_frame = HeaderFrame(window, user, func, func3, func, func3, func)
# new_frame = ResultFrame(window, "Lemons are bad", text, ["lemons", "Cave-Johnson", "aperture"], 345678, 79876, 432, user, 0, str(pd.Timestamp.now()), func2, False)
# new_frame = SearchResultsFrame(window, response, func2, False)
# new_frame = WelcomeFrame(window, user, func, False)
# new_frame = CreatePostFrame(window, func3, False)

# new_frame.swap_mode()

new_frame.pack(expand=1, fill="both")

new_frame.after(3000, new_frame.swap_mode)
new_frame.after(3000, lambda: s.configure('.', font=('Segoe UI Symbol', 16), background="#24272b", foreground="#b6bfcc"))
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

from tkinter import ttk

from Backend.Classes.Models.User import User
from Frontend.Classes.Components.BoardroomFrame import BoardroomFrame
from Frontend.Classes.Components.DarkModeInterface import DarkMode
from Frontend.Classes.Components.ReplyFrame import ReplyFrame
from Frontend.Classes.Widgets.FlatButton import FlatButton
from Frontend.Classes.Widgets.ResizingText import ResizingText
from Frontend.Classes.Widgets.ScrollFrame import ScrollFrame


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

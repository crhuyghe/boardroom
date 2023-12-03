from datetime import datetime, timedelta
from tkinter import ttk

from Backend.Classes.Models.User import User
from Frontend.Classes.Components.DarkModeInterface import DarkMode
from Frontend.Classes.Widgets.FlatButton import FlatButton
from Frontend.Classes.Components.MessageFrame import MessageFrame
from Frontend.Classes.Widgets.ResizingText import ResizingText
from Frontend.Classes.Widgets.ScrollFrame import ScrollFrame


class DirectMessagesFrame(ttk.Frame, DarkMode):
    def __init__(self, master, database_response, current_user, edit_command, delete_command, send_command,
                 dark_mode=False):
        ttk.Frame.__init__(self, master)
        self.dark_mode = dark_mode
        self.current_user = current_user
        self.recipient = database_response["recipient"]
        self.recipient = User(self.recipient["id"], self.recipient["email"], self.recipient["name"])
        self._edit = edit_command
        self._delete = delete_command

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
        self.message_scrollframe = ScrollFrame(self, dark_mode)

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

            if i > 0 and self.messages[i-1]["sender_message"] == self.messages[i]["sender_message"]:
                prev_time = datetime.strptime(self.messages[i-1]["time"], '%Y-%m-%d %X.%f')
                curr_time = datetime.strptime(self.messages[i]["time"], '%Y-%m-%d %X.%f')
                if prev_time + timedelta(minutes=2) > curr_time:
                    header = False
                    post_time = ""
                    padding = [0, 5, 0, 0]
                else:
                    header = True
                    post_time = self.messages[i]["time"]
                    padding = [0, 30, 0, 0]
            else:
                header = True
                post_time = self.messages[i]["time"]
                padding = [0, 30, 0, 0]
            message = MessageFrame(self.message_scrollframe.frame, self.messages[i]["text"], sender,
                                   self.messages[i]["id"],
                                   lambda mid, text: edit_command(self.recipient.id, mid, text),
                                   lambda mid: delete_command(self.recipient.id, mid), post_time,
                                   header, self.messages[i]["sender_message"], self.messages[i]["message_is_edited"],
                                   dark_mode, 90, padding=padding)

            message.pack(side="top")

            self.message_frames.append(message)
        self.message_scrollframe.canvas.update_idletasks()
        self.message_scrollframe.canvas.yview_moveto("1.0")

        self.send_box = ResizingText(self.footer_frame, padding=5, width=50, dark_mode=dark_mode, text_padding=(5, 5),
                                     dynamic=True, display_text=f"Send to {self.recipient.name}",
                                     font=("Segoe UI Symbol", 12))
        self.send_box.toggle_modification()

        self.send_button = FlatButton(self.footer_frame, dark_mode=dark_mode, text="Send",
                                      command=lambda: self._execute_send_command(send_command))

        self.send_button.pack(side="right", padx=(30, 0))
        self.send_box.pack(side="left", fill="x", expand=True)

        self.header_frame.grid(row=0, column=0, sticky="nswe")
        self.message_scrollframe.grid(row=1, column=0, sticky="nsew")
        self.footer_frame.grid(row=2, column=0, sticky="nswe")

        self.grid_rowconfigure(1, weight=20)
        self.grid_rowconfigure(0, weight=1)

    def _execute_send_command(self, send_command):
        if len(self.send_box.get_text().replace(" ", "").replace("\n", "")) > 0:
            send_command(self.recipient.email, self.send_box.get_text())
            self.send_box.change_text("")

    def delete_message_widget(self, message_id):
        for i in range(len(self.message_frames)-1, -1, -1):
            if self.message_frames[i].message_id == message_id:
                self.message_frames[i].destroy()
                self.message_frames.remove(self.message_frames[i])
                self.messages.remove(self.messages[i])

    def edit_message_record(self, message_id, text):
        for i in range(len(self.messages)):
            print(self.messages[i]["id"])
            if int(self.messages[i]["id"]) == message_id:
                self.messages[i]["text"] = text
                self.messages[i]["message_is_edited"] = True

    def flush_messages(self, database_response):
        for message_frame in self.message_frames:
            message_frame.destroy()
        self.message_frames = []
        self.messages = database_response["messages"]
        for i in range(len(self.messages)):
            if self.messages[i]["sender_message"]:
                sender = self.current_user
            else:
                sender = self.recipient

            if i > 0 and self.messages[i-1]["sender_message"] == self.messages[i]["sender_message"]:
                prev_time = datetime.strptime(self.messages[i-1]["time"], '%Y-%m-%d %X.%f')
                curr_time = datetime.strptime(self.messages[i]["time"], '%Y-%m-%d %X.%f')
                if prev_time + timedelta(minutes=2) > curr_time:
                    header = False
                    post_time = ""
                    padding = [0, 5, 0, 0]
                else:
                    header = True
                    post_time = self.messages[i]["time"]
                    padding = [0, 30, 0, 0]
            else:
                header = True
                post_time = self.messages[i]["time"]
                padding = [0, 30, 0, 0]
            message = MessageFrame(self.message_scrollframe.frame, self.messages[i]["text"], sender,
                                   self.messages[i]["id"],
                                   lambda mid, text: self._edit(self.recipient.id, mid, text),
                                   lambda mid: self._delete(self.recipient.id, mid), post_time,
                                   header, self.messages[i]["sender_message"], self.messages[i]["message_is_edited"],
                                   self.dark_mode, 90, padding=padding)

            message.pack(side="top")

            self.message_frames.append(message)
        self.message_scrollframe.canvas.update_idletasks()
        self.message_scrollframe.canvas.yview_moveto("1.0")


    def append_message(self, message):
        if message["sender_message"]:
            sender = self.current_user
        else:
            sender = self.recipient

        if len(self.messages) > 0 and self.messages[-1]["sender_message"] == message["sender_message"]:
            prev_time = datetime.strptime(self.messages[-1]["time"], '%Y-%m-%d %X.%f')
            curr_time = datetime.strptime(message["time"], '%Y-%m-%d %X.%f')
            if prev_time + timedelta(minutes=2) > curr_time:
                header = False
                post_time = ""
                padding = [0, 5, 0, 0]
            else:
                header = True
                post_time = message["time"]
                padding = [0, 30, 0, 0]
        else:
            header = True
            post_time = message["time"]
            padding = [0, 30, 0, 0]
        new_message = MessageFrame(self.message_scrollframe.frame, message["text"], sender,
                                   message["id"],
                                   lambda mid, text: self._edit(self.recipient.id, mid, text),
                                   lambda mid: self._delete(self.recipient.id, mid), post_time,
                                   header, message["sender_message"], message["message_is_edited"],
                                   self.dark_mode, 90, padding=padding)
        new_message.pack(side="top")
        self.message_frames.append(new_message)
        self.messages.append(message)
        self.message_scrollframe.canvas.update_idletasks()
        self.message_scrollframe.canvas.yview_moveto("1.0")

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        for frame in self.message_frames:
            frame.swap_mode()
        self.message_scrollframe.swap_mode()
        self.send_box.swap_mode()
        self.send_button.swap_mode()
        if self.dark_mode:
            ttk.Style().configure("headerfooter.TFrame", background="#1f2226")
            ttk.Style().configure("headerfooter.TLabel", background="#1f2226", foreground="#b6bfcc")
            self.name_label.configure(foreground="#DDDDDD")
        else:
            ttk.Style().configure("headerfooter.TFrame", background="#DDDDDD")
            ttk.Style().configure("headerfooter.TLabel", background="#DDDDDD", foreground="#000000")
            self.name_label.configure(foreground="#111111")

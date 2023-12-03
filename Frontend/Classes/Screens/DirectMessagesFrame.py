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
            message = MessageFrame(self.message_list.frame, self.messages[i]["text"], sender,
                                   self.messages[i]["id"],
                                   lambda text: edit_command(self.recipient.id, self.messages[i]["id"], text),
                                   lambda: delete_command(self.recipient.id, self.messages[i]["id"]), post_time,
                                   header, self.messages[i]["sender_message"], self.messages[i]["message_is_edited"],
                                   dark_mode, 90, padding=padding)

            message.pack(side="top")

            self.message_frames.append(message)
        self.message_list.canvas.update_idletasks()
        self.message_list.canvas.yview_moveto("1.0")

        self.send_box = ResizingText(self.footer_frame, padding=5, width=50, dark_mode=dark_mode, text_padding=(5, 5),
                                     dynamic=True, display_text=f"Send to {self.recipient.name}",
                                     font=("Segoe UI Symbol", 12))
        self.send_box.toggle_modification()

        self.send_button = FlatButton(self.footer_frame, dark_mode=dark_mode, text="Send",
                                      command=lambda: self._execute_send_command(send_command))

        self.send_button.pack(side="right", padx=(30, 0))
        self.send_box.pack(side="left", fill="x", expand=True)

        self.header_frame.grid(row=0, column=0, sticky="nswe")
        self.message_list.grid(row=1, column=0, sticky="nsew")
        self.footer_frame.grid(row=2, column=0, sticky="nswe")

        self.grid_rowconfigure(1, weight=20)
        self.grid_rowconfigure(0, weight=1)

    def _execute_send_command(self, send_command):
        if len(self.send_box.get_text().replace(" ", "").replace("\n", "")) > 0:
            send_command(self.recipient.email, self.send_box.get_text())
            self.send_box.change_text("")

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        for frame in self.message_frames:
            frame.swap_mode()
        self.message_list.swap_mode()
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

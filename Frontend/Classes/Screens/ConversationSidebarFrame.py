from datetime import datetime
from tkinter import ttk

from Backend.Classes.Models.User import User
from Frontend.Classes.Components.ConversationFrame import ConversationFrame
from Frontend.Classes.Components.DarkModeInterface import DarkMode
from Frontend.Classes.Widgets.ResizingText import ResizingText
from Frontend.Classes.Widgets.ScrollFrame import ScrollFrame


class ConversationSidebarFrame(ttk.Frame, DarkMode):
    def __init__(self, master, database_response, open_command, dark_mode=False, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)
        self.dark_mode = dark_mode
        if dark_mode:
            ttk.Style().configure("border.TFrame", background="#969fac")
            ttk.Style().configure("send.TFrame", background="#1f2226")
            ttk.Style().configure("send.TLabel", background="#1f2226", foreground="#b6bfcc")
        else:
            ttk.Style().configure("border.TFrame", background="#666666")
            ttk.Style().configure("send.TFrame", background="#DDDDDD")
            ttk.Style().configure("send.TLabel", background="#DDDDDD", foreground="#000000")

        self.border_list = []

        self.send_frame = ttk.Frame(self, style="send.TFrame")


        self.send_label = ttk.Label(self.send_frame, style="send.TLabel", text="Start a conversation",
                                    font=('Segoe UI Symbol', 20))
        self.recipient_entry = ResizingText(self.send_frame, dark_mode=dark_mode, dynamic=True,
                                          font=('Segoe UI Symbol', 10), display_text="Enter the recipient email...",
                                          text_padding=(5, 5), width=80, padding=10)
        self.message_entry = ResizingText(self.send_frame, dark_mode=dark_mode, dynamic=True,
                                          font=('Segoe UI Symbol', 10), display_text="Enter a message...",
                                          text_padding=(5, 5), width=80, padding=10)
        self.recipient_entry.toggle_modification()
        self.message_entry.toggle_modification()
        self.send_label.grid(row=0, column=0, padx=30, pady=10)
        self.recipient_entry.grid(row=1, column=0, padx=30, pady=10)
        self.message_entry.grid(row=2, column=0, padx=30, pady=10)

        send_border_horizontal = ttk.Frame(self.send_frame, height=3, style="border.TFrame")
        send_border_vertical_r = ttk.Frame(self.send_frame, width=3, style="border.TFrame")
        send_border_vertical_l = ttk.Frame(self.send_frame, width=3, style="border.TFrame")
        send_border_horizontal.grid(row=0, column=0, sticky="new")
        send_border_vertical_r.grid(row=0, rowspan=3, column=0, sticky="nes")
        send_border_vertical_l.grid(row=0, rowspan=3, column=0, sticky="nws")
        self.border_list.append(send_border_horizontal)
        self.border_list.append(send_border_vertical_r)
        self.border_list.append(send_border_vertical_l)

        self.conversation_list = []

        database_response["conversations"].sort(key=lambda x: datetime.strptime(x["last_message_time"],
                                                                                '%Y-%m-%d %X.%f'), reverse=True)

        if len(database_response["conversations"]) > 0:
            self.conversations_frame = ScrollFrame(self, dark_mode, True)
            for conversation in database_response["conversations"]:
                recipient = conversation["recipient"]
                recipient = User(recipient["id"], recipient["email"], recipient["name"])

                conversation_frame = ConversationFrame(self.conversations_frame.frame, recipient,
                                                       conversation["last_message"], open_command,
                                                       conversation["last_message_time"], dark_mode, padding=20)
                conversation_frame.pack(side="top", fill="x", expand=1)

                border = ttk.Frame(self.conversations_frame.frame, height=1, style="border.TFrame")
                border.pack(side="top", fill="x", expand=1)

                self.border_list.append(border)
                self.conversation_list.append(conversation_frame)
            self.conversations_frame.grid(row=0, column=0, sticky="nsew")
        else:
            self.no_conversations_frame = ttk.Frame(self, style="send.TFrame")
            self.no_conversations_label = ttk.Label(self.no_conversations_frame,
                                                    text="No messages yet!\nSend one to one of\nyour friends!",
                                                    font=("Segoe UI", 20), style="send.TLabel", justify="center",
                                                    padding=[0, 50, 0, 0])
            self.no_conversations_label.grid(column=1)
            self.no_conversations_frame.grid_columnconfigure(0, weight=1)
            self.no_conversations_frame.grid_columnconfigure(2, weight=1)
            self.no_conversations_frame.grid(row=0, column=0, sticky="nsew")

        self.send_frame.grid(row=1, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if len(self.conversation_list) > 0:
            self.conversations_frame.swap_mode()
        if self.dark_mode:
            ttk.Style().configure("border.TFrame", background="#969fac")
            ttk.Style().configure("send.TFrame", background="#1f2226")
            ttk.Style().configure("send.TLabel", background="#1f2226", foreground="#b6bfcc")
        else:
            ttk.Style().configure("border.TFrame", background="#666666")
            ttk.Style().configure("send.TFrame", background="#DDDDDD")
            ttk.Style().configure("send.TLabel", background="#DDDDDD", foreground="#000000")

        self.recipient_entry.swap_mode()
        self.message_entry.swap_mode()

        for conversation_frame in self.conversation_list:
            conversation_frame.swap_mode()

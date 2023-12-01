from tkinter import ttk

from Frontend.Classes.Widgets.FlatButton import FlatButton


class WelcomeFrame(ttk.Frame):
    def __init__(self, master, current_user, create_post_command, dark_mode=False, **kwargs):
        super().__init__(master, **kwargs)
        self.dark_mode = dark_mode
        if dark_mode:
            ttk.Style().configure("create.TLabel", background="#1f2226", foreground="#b6bfcc")
        else:
            ttk.Style().configure("create.TLabel", background="#DDDDDD", foreground="#000000")

        name = current_user.name.split()
        self.welcome_name_label = ttk.Label(self, text=f"Welcome, {name[0]}!", font=("Segoe UI Bold", 30),
                                            justify="center")
        self.welcome_text_label = ttk.Label(self,
                                            text="Message your friends,\nsearch for boardrooms,\nor create your own!",
                                            font=("Segoe UI Bold", 20), justify="center")

        self.create_post_button = FlatButton(self, dark_mode, text="Create Post", command=lambda: create_post_command,
                                             style="create.TLabel", font=("Segoe UI Bold", 20))
        self.welcome_name_label.grid(row=1, column=1, sticky="s")
        self.welcome_text_label.grid(row=2, column=1, sticky="n")
        self.create_post_button.grid(row=3, column=1, pady=50)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)


    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            ttk.Style().configure("create.TLabel", background="#1f2226", foreground="#b6bfcc")
        else:
            ttk.Style().configure("create.TLabel", background="#DDDDDD", foreground="#000000")
        self.create_post_button.swap_mode()

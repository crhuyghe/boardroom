import asyncio
import tkinter as tk
from tkinter import ttk, StringVar

from Frontend.Classes.FlatButton import FlatButton

class LoginFrame(ttk.Frame):
    def __init__(self, master=None, dark_mode=False):
        super().__init__(master)
        self.dark_mode = dark_mode

        # Set default font for new objects
        default_font = ("Segoe UI Symbol", 12)
        self.master.option_add("*TButton*Font", default_font)
        self.master.option_add("*TLabel*Font", default_font)
        self.master.option_add("*TEntry*Font", default_font)

        # Title
        title_label = ttk.Label(self.master, text="Log Into Your Account", font=("Segoe UI Symbol", 16))
        title_label.pack(pady=20)

        # Style for login frame objects. Only changes background color.
        s_login = ttk.Style()
        s_login.configure("new.TFrame", background="#cccccc")

        # Login frame that holds text fields and buttons.
        login_frame = ttk.Frame(self.master, style="new.TFrame", padding=(20, 10), relief="solid", borderwidth=1)
        login_frame.pack(pady=20)

        # Username entry field.
        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, sticky="w")
        username_entry = ttk.Entry(login_frame)
        username_entry.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

        # Password entry field. Hides user input with "*".
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky="w")
        password_entry = ttk.Entry(login_frame, show="*")
        password_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        # Clickable link for "Create Account" text.
        create_account_label = ttk.Label(login_frame, text="Don't have an account? Create one!", cursor="hand2",
                                         font=default_font)
        create_account_label.grid(row=2, column=0, columnspan=2, pady=5, padx=5, sticky="ew")
        create_account_label.bind("<Button-1>", self.create_account)
        create_account_label.bind("<Enter>",
                                  lambda event: create_account_label.config(font=("Segoe UI Symbol", 12, "underline")))
        create_account_label.bind("<Leave>", lambda event: create_account_label.config(font=("Segoe UI Symbol", 12)))

        # Login button.
        login_button = FlatButton(login_frame, dark_mode=False, text="Login", font=default_font,
                                  command=lambda: self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=10)

    def create_account(self, event):
        # Handles clicking "Create Account" text link
        print("Create an account!")
        # Do something

    def login(self):
        # Handles clicking "Login" button
        print("Logging in...")
        # Do something

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            ttk.Style().configure("title.TLabel", background="#292c30")
        else:
            ttk.Style().configure("title.TLabel", background="#EEEEEE")

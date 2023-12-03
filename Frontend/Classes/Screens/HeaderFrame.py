import tkinter as tk
from tkinter import ttk, BooleanVar, StringVar

from Frontend.Classes.Components.DarkModeInterface import DarkMode
from Frontend.Classes.Components.UserFrame import UserFrame
from Frontend.Classes.Widgets.FlatButton import FlatButton
from Frontend.Classes.Widgets.ResizingText import ResizingText


class HeaderFrame(ttk.Frame, DarkMode):
    def __init__(self, master, current_user, home_command, search_command, logout_command, delete_account_command,
                 mode_command, dark_mode=False, **kwargs):
        ttk.Frame.__init__(self, master, style="headerbar.TFrame", **kwargs)
        self.dark_mode = dark_mode
        if dark_mode:
            ttk.Style().configure("border.TFrame", background="#969fac")
            ttk.Style().configure("headerbar.TFrame", background="#1d2024")
            ttk.Style().configure("headerbar.TLabel", background="#1d2024", foreground="#b6bfcc")
            ttk.Style().configure("header.TCheckbutton", background="#1d2024", foreground="#b6bfcc",
                                  font=('Segoe UI Symbol', 8))
            self.search_image = tk.PhotoImage(file="Assets/search_dark.png")
            menu_colors = ("#1f2226", "#b6bfcc")
            home_fg = "#84e0e8"
            email_fg = "#AAAAAA"
        else:
            ttk.Style().configure("border.TFrame", background="#666666")
            ttk.Style().configure("headerbar.TFrame", background="#BBBBBB")
            ttk.Style().configure("headerbar.TLabel", background="#BBBBBB", foreground="#000000")
            ttk.Style().configure("header.TCheckbutton", background="#BBBBBB", foreground="#000000",
                                  font=('Segoe UI Symbol', 8))
            self.search_image = tk.PhotoImage(file="Assets/search_light.png")
            menu_colors = ("#eeeeee", "#000000")
            home_fg = "#ab0323"
            email_fg = "#777777"

        self.left_frame = ttk.Frame(self, style="headerbar.TFrame")

        self.search_frame = ttk.Frame(self, style="headerbar.TFrame")

        self.right_frame = ttk.Frame(self, style="headerbar.TFrame")

        self.home_button = FlatButton(self.left_frame, dark_mode, style="headerbar.TLabel",
                                      font=("Franklin Gothic Heavy", 25, "bold"),
                                      text="Boardroom", foreground=home_fg, command=home_command)
        self.home_button.grid(padx=15, pady=(15, 18))

        self.searchbox = ResizingText(self.search_frame, dark_mode=dark_mode, dynamic=True,
                                      font=('Segoe UI Symbol', 10), display_text="Search for Boardrooms...",
                                      text_padding=(5, 5), width=60, padding=5)
        self.tag_searchbox = ResizingText(self.search_frame, dark_mode=dark_mode, dynamic=True,
                                          font=('Segoe UI Symbol', 8), display_text="Enter tags to search by...",
                                          text_padding=(5, 5), width=10, padding=5)
        self.searchbox.toggle_modification()
        self.tag_searchbox.toggle_modification()
        self.search_button = FlatButton(self.search_frame, dark_mode, image=self.search_image, padding=5,
                                        style="headerbar.TLabel", command=lambda:
            self._execute_search_command(search_command))

        self.searchbox.grid(row=1, column=0, columnspan=4, padx=30, pady=8, sticky="ew")
        self.tag_searchbox.grid(row=0, column=0, padx=30, pady=5, sticky="ew")
        self.search_button.grid(row=0, rowspan=2, column=4, sticky="e", padx=(0, 20))
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_frame.grid_columnconfigure(1, weight=1)

        self.dark_mode_var = BooleanVar()
        self.dark_mode_var.set(dark_mode)
        self.dark_mode_button = ttk.Checkbutton(self.right_frame, text="Dark Mode", variable=self.dark_mode_var,
                                                onvalue=True, offvalue=False, style="header.TCheckbutton",
                                                command=mode_command)

        self.user_label = UserFrame(self.right_frame, current_user, style="headerbar.TFrame",
                                    label_style="headerbar.TLabel")
        self.user_label.bind("<Button-1>", self._popup_menu)

        self.user_menu = tk.Menu(self, tearoff=0, background=menu_colors[0], foreground=menu_colors[1])
        self.user_menu.add_command(label="Logout", command=logout_command)
        self.user_menu.add_command(label="Delete Account", command=self._show_password_input)

        self.password_frame = ttk.Frame(self.right_frame, style="headerbar.TFrame")
        self.password_label = ttk.Label(self.password_frame, style="headerbar.TLabel", font=('Segoe UI Symbol', 10),
                                        text="Enter password to confirm deletion")
        self.password = StringVar()
        self.password_entry = ttk.Entry(self.password_frame, show="*", textvariable=self.password,
                                        font=('Segoe UI Symbol', 10), foreground="#000000")
        self.cancel_button = FlatButton(self.password_frame, dark_mode, text="Cancel",
                                        command=self._hide_password_input)
        self.confirm_button = FlatButton(self.password_frame, dark_mode, text="Confirm",
                                         command=lambda: self._execute_delete_account_command(delete_account_command))
        self.error_label = ttk.Label(self.password_frame, style="headerbar.TLabel", foreground="red",
                                     font=('Segoe UI Symbol', 10), text="Incorrect password")

        self.password_label.grid(row=0, column=0, columnspan=2)
        self.password_entry.grid(row=1, column=0, columnspan=2)
        self.cancel_button.grid(row=2, column=0, padx=(0, 5), pady=5, sticky="e")
        self.confirm_button.grid(row=2, column=1, padx=(5, 0), pady=5, sticky="w")

        self.user_label.pack(fill="y", expand=1, side="right")
        self.user_label.email_label.configure(foreground=email_fg)

        self.dark_mode_button.pack(fill="y", expand=1, side="left")

        border_horizontal = ttk.Frame(self, height=3, style="border.TFrame")
        border_horizontal.grid(row=0, column=0, columnspan=3, sticky="sew")

        self.left_frame.grid(row=0, column=0, sticky="w")
        self.search_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.grid(row=0, column=2, sticky="we")

        # self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure("all", weight=1, uniform="header")

    def _show_password_input(self):
        self.password_frame.pack(side="right")
    def _hide_password_input(self):
        self.password_frame.pack_forget()
        self.error_label.grid_forget()

    def _execute_delete_account_command(self, delete_command):
        password = self.password.get()
        if len(password) > 0:
            delete_command(password)

    def _execute_search_command(self, search_command):
        if len(self.searchbox.get_text()) > 0 or len(self.tag_searchbox.get_text()) > 0:
            search_command(self.searchbox.get_text(), self.tag_searchbox.get_text().split())

    def show_error(self):
        self.error_label.grid(row=3, column=0, columnspan=2)

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            ttk.Style().configure("border.TFrame", background="#969fac")
            ttk.Style().configure("headerbar.TFrame", background="#1d2024")
            ttk.Style().configure("headerbar.TLabel", background="#1d2024", foreground="#b6bfcc")
            ttk.Style().configure("header.TCheckbutton", background="#1d2024", foreground="#b6bfcc")
            self.search_image.configure(file="Assets/search_dark.png")
            self.user_menu.configure(background="#1f2226", foreground="#b6bfcc")
            self.user_label.email_label.configure(foreground="#AAAAAA")
            self.home_button.configure(foreground="#84e0e8")
        else:
            ttk.Style().configure("border.TFrame", background="#666666")
            ttk.Style().configure("headerbar.TFrame", background="#BBBBBB")
            ttk.Style().configure("headerbar.TLabel", background="#BBBBBB", foreground="#000000")
            ttk.Style().configure("header.TCheckbutton", background="#BBBBBB", foreground="#000000")
            self.search_image.configure(file="Assets/search_light.png")
            self.user_menu.configure(background="#eeeeee", foreground="#000000")
            self.user_label.email_label.configure(foreground="#777777")
            self.home_button.configure(foreground="#ab0323")
        self.searchbox.swap_mode()
        self.tag_searchbox.swap_mode()
        self.search_button.swap_mode()
        self.confirm_button.swap_mode()
        self.cancel_button.swap_mode()

    def _popup_menu(self, event):
        try:
            self.user_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.user_menu.grab_release()

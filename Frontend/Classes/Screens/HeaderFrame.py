import tkinter as tk
from tkinter import ttk, BooleanVar

from Frontend.Classes.Components.UserFrame import UserFrame
from Frontend.Classes.Widgets.FlatButton import FlatButton
from Frontend.Classes.Widgets.ResizingText import ResizingText


class HeaderFrame(ttk.Frame):

    def __init__(self, master, current_user, home_command, search_command, logout_command, delete_account_command, mode_command, dark_mode=False, **kwargs):
        super().__init__(master, style="headerbar.TFrame", **kwargs)
        self.dark_mode = dark_mode
        if dark_mode:
            ttk.Style().configure("border.TFrame", background="#969fac")
            ttk.Style().configure("headerbar.TFrame", background="#1d2024")
            ttk.Style().configure("headerbar.TLabel", background="#1d2024", foreground="#b6bfcc")
            ttk.Style().configure("header.TCheckbutton", background="#1d2024", foreground="#b6bfcc",
                                  font=('Segoe UI Symbol', 8))
            self.search_image = tk.PhotoImage(file="Frontend/Assets/search_dark.png")
            menu_colors = ("#1f2226", "#b6bfcc")
            home_fg = "#84e0e8"
        else:
            ttk.Style().configure("border.TFrame", background="#666666")
            ttk.Style().configure("headerbar.TFrame", background="#BBBBBB")
            ttk.Style().configure("headerbar.TLabel", background="#BBBBBB", foreground="#000000")
            ttk.Style().configure("header.TCheckbutton", background="#BBBBBB", foreground="#000000",
                                  font=('Segoe UI Symbol', 8))
            self.search_image = tk.PhotoImage(file="Frontend/Assets/search_light.png")
            menu_colors = ("#eeeeee", "#000000")
            home_fg = "#ab0323"

        self.left_frame = ttk.Frame(self, style="headerbar.TFrame")

        self.search_frame = ttk.Frame(self, style="headerbar.TFrame")

        self.right_frame = ttk.Frame(self, style="headerbar.TFrame")

        self.home_button = FlatButton(self.left_frame, style="headerbar.TLabel", font=("Franklin Gothic Heavy", 25, "bold"),
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
            search_command(self.tag_searchbox.get_text(), self.searchbox.get_text()))

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
        self.user_label.name_label.bind("<Button-1>", self._popup_menu)
        self.user_label.email_label.bind("<Button-1>", self._popup_menu)

        self.user_menu = tk.Menu(self, tearoff=0, background=menu_colors[0], foreground=menu_colors[1])
        self.user_menu.add_command(label="Logout", command=logout_command)
        self.user_menu.add_command(label="Delete Account", command=delete_account_command)

        self.user_label.pack(fill="y", expand=1, side="right")

        self.dark_mode_button.pack(fill="y", expand=1, side="left")

        border_horizontal = ttk.Frame(self, height=3, style="border.TFrame")
        # border_vertical = ttk.Frame(self.search_frame, width=3, style="border.TFrame")
        border_horizontal.grid(row=0, column=0, columnspan=3, sticky="sew")

        self.left_frame.grid(row=0, column=0, sticky="w")
        self.search_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.grid(row=0, column=2, sticky="we")

        # self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure("all", weight=1, uniform="header")



    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            ttk.Style().configure("border.TFrame", background="#969fac")
            ttk.Style().configure("headerbar.TFrame", background="#1d2024")
            ttk.Style().configure("headerbar.TLabel", background="#1d2024", foreground="#b6bfcc")
            ttk.Style().configure("header.TCheckbutton", background="#1d2024", foreground="#b6bfcc")
            self.search_image.configure(file="Frontend/Assets/search_dark.png")
            self.user_menu.configure(background="#1f2226", foreground="#b6bfcc")
            self.home_button.configure(foreground="#84e0e8")
        else:
            ttk.Style().configure("border.TFrame", background="#666666")
            ttk.Style().configure("headerbar.TFrame", background="#BBBBBB")
            ttk.Style().configure("headerbar.TLabel", background="#BBBBBB", foreground="#000000")
            ttk.Style().configure("header.TCheckbutton", background="#BBBBBB", foreground="#000000")
            self.search_image.configure(file="Frontend/Assets/search_light.png")
            self.user_menu.configure(background="#eeeeee", foreground="#000000")
            self.home_button.configure(foreground="#ab0323")

    def _popup_menu(self, event):
        try:
            self.user_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.user_menu.grab_release()

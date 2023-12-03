from tkinter import ttk, StringVar, PhotoImage

from Frontend.Classes.Components.DarkModeInterface import DarkMode
from Frontend.Classes.Widgets.FlatButton import FlatButton

class LoginFrame(ttk.Frame):
    def __init__(self, master, login_command, create_account_command):
        ttk.Frame.__init__(self, master)

        # Style for login frame objects. Only changes background color.
        s_login = ttk.Style()
        s_login.configure("login.TFrame", background="#cccccc", foreground="#000000")
        s_login.configure("login.TLabel", background="#cccccc", foreground="#000000")
        s_login.configure("login_button.TLabel", background="#EEEEEE", foreground="#000000")

        # Login frame that holds text fields and buttons.
        self.login_frame = ttk.Frame(self, style="login.TFrame", padding=(20, 10), relief="solid", borderwidth=1)
        self.login_frame.grid(row=1, column=1, pady=20)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Title
        self.title_label = ttk.Label(self.login_frame, style="login.TLabel", text="Log Into Your Account",
                                font=("Segoe UI Symbol", 16))
        self.title_label.pack(pady=20)
        self.title_label.grid(row=0, column=1, pady=5, sticky="ew")

        # Email entry field.
        ttk.Label(self.login_frame, style="login.TLabel", text="Email:", font=("Segoe UI Symbol", 12)).grid(row=1, column=0, sticky="w")
        self.email_text = StringVar()
        self.email_entry = ttk.Entry(self.login_frame, textvariable=self.email_text, foreground="#000000", font=("Segoe UI Symbol", 12))
        self.email_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        # Password entry field. Hides user input with "*".
        self.visibility_image = PhotoImage(file="Assets/visibility_toggle.png")
        ttk.Label(self.login_frame, style="login.TLabel", text="Password:", font=("Segoe UI Symbol", 12)).grid(row=2, column=0, sticky="w")
        self.password_text = StringVar()
        self.password_entry = ttk.Entry(self.login_frame, textvariable=self.password_text, show="*", foreground="#000000", font=("Segoe UI Symbol", 12))
        self.password_entry.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        self.view_button_1 = FlatButton(self.login_frame, style="login.TLabel", image=self.visibility_image,
                                        command=lambda: self.password_entry.configure(show="") if
                                        self.password_entry.cget("show") == "*" else
                                        self.password_entry.configure(show="*"), padding=0)
        self.view_button_1.grid(row=2, column=2)

        # Clickable link for "Create Account" text.
        self.create_account_label = ttk.Label(self.login_frame, style="login.TLabel", text="Don't have an account? Create one!", cursor="hand2",
                                         font=("Segoe UI Symbol", 12), foreground="blue")
        self.create_account_label.grid(row=3, column=0, columnspan=2, pady=5, padx=5, sticky="ew")
        self.create_account_label.bind("<Button-1>", lambda e=None: create_account_command() if e else None)
        self.create_account_label.bind("<Enter>",
                                  lambda event: self.create_account_label.config(font=("Segoe UI Symbol", 12, "underline"), foreground="blue"))
        self.create_account_label.bind("<Leave>", lambda event: self.create_account_label.config(font=("Segoe UI Symbol", 12)))

        # Login button.
        self.login_button = FlatButton(self.login_frame, text="Login", font=("Segoe UI Symbol", 12),
                                  command=lambda: self._execute_login_command(login_command),
                                       style="login_button.TLabel")
        self.login_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.warning_text = StringVar()
        self.warning_label = ttk.Label(self.login_frame, style="login.TLabel", foreground="red",
                                       font=("Segoe UI Symbol", 10), textvariable=self.warning_text)

    def show_warning_label(self, warning):
        self.warning_text.set(warning)
        self.warning_label.grid(row=5, column=0, columnspan=2, pady=10)

    def _execute_login_command(self, login_command):
        # Handles clicking "Login" button
        email = self.email_text.get()
        password = self.password_text.get()
        if len(email) > 0 and len(password) > 0:
            self.password_text.set("")
            login_command(email, password)

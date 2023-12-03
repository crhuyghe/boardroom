from tkinter import ttk, StringVar, PhotoImage

from Frontend.Classes.Components.DarkModeInterface import DarkMode
from Frontend.Classes.Widgets.FlatButton import FlatButton

class CreateAccountFrame(ttk.Frame):

    def __init__(self, master, login_command, create_account_command):
        ttk.Frame.__init__(self, master)

        # Style for login frame objects. Only changes background color.
        s_createAccount = ttk.Style()
        s_createAccount.configure("create_account.TFrame", background="#cccccc", foreground="#000000")
        s_createAccount.configure("create_account.TLabel", background="#cccccc", foreground="#000000", font=("Segoe UI Symbol", 12))
        s_createAccount.configure("ca_button.TLabel", background="#EEEEEE", foreground="#000000")

        # Login frame that holds text fields and buttons.
        self.createAccount_frame = ttk.Frame(self, style="create_account.TFrame", padding=(20, 10), relief="solid", borderwidth=1)
        self.createAccount_frame.grid(row=1, column=1, pady=20)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Title
        self.title_label = ttk.Label(self.createAccount_frame, style="create_account.TLabel", text="Create An Account",
                                font=("Segoe UI Symbol", 16))
        self.title_label.pack(pady=20)
        self.title_label.grid(row=0, column=1, pady=5, sticky="ew")

        # Username entry field.
        ttk.Label(self.createAccount_frame, style="create_account.TLabel", text="Email:").grid(row=1, column=0, sticky="w")
        self.email_text = StringVar()
        self.email_entry = ttk.Entry(self.createAccount_frame, foreground="#000000", font=("Segoe UI Symbol", 12),
                                     textvariable=self.email_text)
        self.email_entry.grid(row=1, column=1, sticky="ew")

        # Password entry field. Hides user input with "*".
        self.visibility_image = PhotoImage(file="Assets/visibility_toggle.png")

        ttk.Label(self.createAccount_frame, style="create_account.TLabel", text="Password:").grid(row=2, column=0, sticky="w")
        self.password_text1 = StringVar()
        self.password_entry1 = ttk.Entry(self.createAccount_frame, show="*", foreground="#000000",
                                         font=("Segoe UI Symbol", 12), textvariable=self.password_text1)
        self.password_entry1.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        self.view_button_1 = FlatButton(self.createAccount_frame, style="create_account.TLabel", image=self.visibility_image,
                                        command=lambda: self.password_entry1.configure(show="") if
                                        self.password_entry1.cget("show") == "*" else
                                        self.password_entry1.configure(show="*"), padding=0)
        self.view_button_1.grid(row=2, column=2)

        ttk.Label(self.createAccount_frame, style="create_account.TLabel", text="Confirm Password:").grid(row=3, column=0, sticky="w")
        self.password_text2 = StringVar()
        self. password_entry2 = ttk.Entry(self.createAccount_frame, show="*", foreground="#000000",
                                         font=("Segoe UI Symbol", 12), textvariable=self.password_text2)
        self.password_entry2.grid(row=3, column=1, pady=5, padx=5, sticky="ew")

        self.view_button_2 = FlatButton(self.createAccount_frame, style="create_account.TLabel", image=self.visibility_image,
                                        command=lambda: self.password_entry2.configure(show="") if
                                        self.password_entry2.cget("show") == "*" else
                                        self.password_entry2.configure(show="*"), padding=0)
        self.view_button_2.grid(row=3, column=2, pady=5, padx=5)

        # First and last name entry field.
        ttk.Label(self.createAccount_frame, style="create_account.TLabel", text="First & Last Name:").grid(row=4, column=0, sticky="w")
        self.name_text = StringVar()
        self.name_entry = ttk.Entry(self.createAccount_frame, foreground="#000000", font=("Segoe UI Symbol", 12),
                                    textvariable=self.name_text)
        self.name_entry.grid(row=4, column=1, pady=5, padx=5, sticky="ew")

        # Clickable link for "Login" text.
        self.login_label = ttk.Label(self.createAccount_frame, style="create_account.TLabel", text="Already have an account? Log in!", cursor="hand2",
                                         font=("Segoe UI Symbol", 12), foreground="blue")
        self.login_label.grid(row=5, column=0, columnspan=2, pady=5, padx=5, sticky="ew")
        self.login_label.bind("<Button-1>", lambda e=None: login_command() if e else None)
        self.login_label.bind("<Enter>",
                                  lambda event: self.login_label.config(font=("Segoe UI Symbol", 12, "underline"), foreground="blue"))
        self.login_label.bind("<Leave>", lambda event: self.login_label.config(font=("Segoe UI Symbol", 12)))

        # Create account button.
        self.create_account_button = FlatButton(self.createAccount_frame, dark_mode=False, text="Create My Account!", font=("Segoe UI Symbol", 12),
                                                command=lambda: self._execute_create_account_command(create_account_command), style="ca_button.TLabel")
        self.create_account_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.warning_text = StringVar()
        self.warning_label = ttk.Label(self.createAccount_frame, style="create_account.TLabel", foreground="red",
                                       font=("Segoe UI Symbol", 10), textvariable=self.warning_text)

    def show_warning_label(self, warning):
        self.warning_text.set(warning)
        self.warning_label.grid(row=7, column=0, columnspan=2, pady=10)

    def _execute_create_account_command(self, create_account_command):
        # Handles clicking "Create Account" button
        email = self.email_text.get()
        name = self.name_text.get()
        pass1 = self.password_text1.get()
        pass2 = self.password_text2.get()

        if len(email) > 0 and len(name) > 0 and len(pass1) > 0 and len(pass2) > 0:
            if "@" not in email or "." not in email:
                self.show_warning_label("Please fill out a valid email")
            elif pass1 != pass2:
                self.show_warning_label("Passwords do not match")
            else:
                create_account_command(email, name, pass1)

from tkinter import ttk

from Frontend.Classes.Components.DarkModeInterface import DarkMode
from Frontend.Classes.Widgets.FlatButton import FlatButton

class CreateAccountFrame(ttk.Frame, DarkMode):

    def __init__(self, master=None, dark_mode=False):
        ttk.Frame.__init__(self, master)
        self.dark_mode = dark_mode

        # Set default font for new objects
        # default_font = ("Segoe UI Symbol", 12)
        # self.master.option_add("*TButton*Font", default_font)
        # self.master.option_add("*TLabel*Font", default_font)
        # self.master.option_add("*TEntry*Font", default_font)

        # Style for login frame objects. Only changes background color.
        s_createAccount = ttk.Style()
        s_createAccount.configure("new.TFrame", background="#cccccc")
        s_createAccount.configure("new.TLabel", background="#cccccc", font=("Segoe UI Symbol", 12))

        # Login frame that holds text fields and buttons.
        createAccount_frame = ttk.Frame(self, style="new.TFrame", padding=(20, 10), relief="solid", borderwidth=1)
        createAccount_frame.pack(pady=20)

        # Title
        title_label = ttk.Label(createAccount_frame, style="new.TLabel", text="Create An Account",
                                font=("Segoe UI Symbol", 16))
        title_label.pack(pady=20)
        title_label.grid(row=0, column=1, pady=5, sticky="ew")

        # Username entry field.
        ttk.Label(createAccount_frame, style="new.TLabel", text="Email:").grid(row=1, column=0, sticky="w")
        email_entry = ttk.Entry(createAccount_frame)
        email_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        # Password entry field. Hides user input with "*".
        ttk.Label(createAccount_frame, style="new.TLabel", text="Password:").grid(row=2, column=0, sticky="w")
        password_entry = ttk.Entry(createAccount_frame, show="*")
        password_entry.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        # First and last name entry field.
        ttk.Label(createAccount_frame, style="new.TLabel", text="First & Last Name:").grid(row=3, column=0, sticky="w")
        password_entry = ttk.Entry(createAccount_frame)
        password_entry.grid(row=3, column=1, pady=5, padx=5, sticky="ew")

        # Create account button.
        login_button = FlatButton(createAccount_frame, dark_mode=False, text="Create My Account!", font=("Segoe UI Symbol", 12),
                                  command=lambda: self.create_account)
        login_button.grid(row=4, column=0, columnspan=2, pady=10)


    def create_account(self):
        # Handles clicking "Create Account" button
        print("Account created!")
        # Do something

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            ttk.Style().configure("title.TLabel", background="#292c30")
        else:
            ttk.Style().configure("title.TLabel", background="#EEEEEE")

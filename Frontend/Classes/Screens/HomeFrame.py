from tkinter import ttk

from Frontend.Classes.Widgets.FlatButton import FlatButton

class HomeFrame(ttk.Frame):

    def __init__(self, master=None, dark_mode=False):
        super().__init__(master)
        self.dark_mode = dark_mode

        # Set default font for new objects
        # default_font = ("Segoe UI Symbol", 12)

        # Create and pack the search bar and search button side by side
        search_frame = ttk.Frame(self, borderwidth=2, relief="solid")
        search_frame.grid(row=0, column=0, sticky="ew")

        search_entry = ttk.Entry(search_frame, font=("Segoe UI", 12), width=100)
        search_entry.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        # The above search_entry code works. ResizingText keeps making it disappear.

        # search_entry = self.text_label = ResizingText(self, text, width=70, font=("Segoe UI Symbol", 10), dark_mode=dark_mode,
        #                              padding=[25, 0, 0, 0])
        # search_entry.grid(row=0, column=0, sticky="ew")

        search_button = FlatButton(search_frame, dark_mode=False, text="Search", font=("Segoe UI Symbol", 12),
                                   command=lambda: self.search)
        search_button.grid(row=0, column=1, sticky="ew")

        # Create and pack the right column
        right_column_frame = ttk.Frame(self, width=self.master.winfo_screenwidth() // 4,
                                       borderwidth=2, relief="solid", height=self.master.winfo_screenheight())
        right_column_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Create and pack the logout button in the right column
        logout_button = FlatButton(right_column_frame, dark_mode=False, text="Logout", font=("Segoe UI Symbol", 12),
                                   command=lambda: self.logout)
        logout_button.grid(row=0, column=0, sticky="e")

        # Create and pack the welcome frame
        welcome_frame = ttk.Frame(self, borderwidth="20", relief="solid")
        welcome_frame.grid(row=1, column=0, sticky="nsew")

        welcome_label = ttk.Label(welcome_frame, text="Welcome to Boardroom, User!", font=("Segoe UI", 32))
        welcome_label.pack(expand=True, fill="both", anchor="center")

        # Configure row and column weights to make the layout resizable
        self.columnconfigure(0, weight=3)  # 75% screen width
        self.columnconfigure(1, weight=1)  # 25% screen width
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

    def search(self):
        # Functionality for the search button
        # search_query = search_entry.get()
        # You can implement your search logic here
        print(f"Searching...")

    def logout(self):
        # Functionality for the login button
        print("Logout button clicked")

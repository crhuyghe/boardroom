from tkinter import ttk

class UserFrame(ttk.Frame):
    def __init__(self, master, user):
        super().__init__(master)

        self.name_label = ttk.Label(self, text=user.name, font=("Segoe UI Symbol", 10))
        self.email_label = ttk.Label(self, text=user.email, font=("Segoe UI Symbol", 7), foreground="#AAAAAA")

        self.name_label.grid(row=0)
        self.email_label.grid(row=1)

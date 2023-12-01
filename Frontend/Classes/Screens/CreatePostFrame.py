from tkinter import ttk

from Frontend.Classes.Widgets.FlatButton import FlatButton
from Frontend.Classes.Widgets.ResizingText import ResizingText


class CreatePostFrame(ttk.Frame):
    def __init__(self, master, current_user, create_command, dark_mode=False, **kwargs):
        super().__init__(master, **kwargs)
        self.dark_mode = dark_mode
        if dark_mode:
            ttk.Style().configure("create.TLabel", background="#1f2226", foreground="#b6bfcc")
        else:
            ttk.Style().configure("create.TLabel", background="#DDDDDD", foreground="#000000")

        name = current_user.name.split()

        self.creation_frame = ttk.Frame(self)
        self.prompt_label = ttk.Label(self.creation_frame, text="Enter a title, text, and tags for your new boardroom",
                                      font=("Segoe UI Bold", 18))
        self.title_label = ttk.Label(self.creation_frame, text="Title:")
        self.text_label = ttk.Label(self.creation_frame, text="Text:")
        self.tag_label = ttk.Label(self.creation_frame, text="Tags:")
        self.tag_warning_label = ttk.Label(self.creation_frame, text="(Tags should be separated by a single space)",
                                     font=("Segoe UI Symbol", 10), foreground="#AAAAAA")
        self.warning_label = ttk.Label(self.creation_frame, text="*Please fill out all fields.", foreground="red",
                                     font=("Segoe UI Symbol", 12))

        self.title_entry = ResizingText(self.creation_frame, dark_mode=dark_mode, dynamic=True, text_padding=(5, 5),
                                        padding=5, display_text="Enter a title for your boardroom...", width=80)
        self.text_entry = ResizingText(self.creation_frame, dark_mode=dark_mode, text_padding=(5, 5),
                                        padding=5, display_text="Enter some post text...\n\n", width=100,
                                        font=("Segoe UI Symbol", 12), min_height=5)
        self.tag_entry = ResizingText(self.creation_frame, dark_mode=dark_mode, dynamic=True, text_padding=(5, 5),
                                        padding=5, display_text="Enter your tags here...",
                                        font=("Segoe UI Symbol", 10))

        self.title_entry.toggle_modification()
        self.text_entry.toggle_modification()
        self.tag_entry.toggle_modification()

        self.submit_button = FlatButton(self.creation_frame, dark_mode, text="Create Boardroom",
                                        command=lambda: self._execute_create_command(create_command),
                                        style="create.TLabel", font=("Segoe UI Bold", 15))

        self.prompt_label.grid(row=0, column=0, columnspan=2)
        self.title_label.grid(row=1, column=0, columnspan=2, sticky="w")
        self.title_entry.grid(row=2, column=0, columnspan=2, sticky="we")
        self.text_label.grid(row=3, column=0, columnspan=2, sticky="w")
        self.text_entry.grid(row=4, column=0, columnspan=2, sticky="we")
        self.tag_label.grid(row=5, column=0, columnspan=2, sticky="w")
        self.tag_entry.grid(row=6, column=0, columnspan=2, sticky="we")
        self.tag_warning_label.grid(row=7, column=0, columnspan=2, sticky="w")
        self.submit_button.grid(row=8, column=1, sticky="e")

        self.creation_frame.grid(row=1, column=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def _execute_create_command(self, create_command):
        title = self.title_entry.get_text()
        text = self.text_entry.get_text()
        tags = self.tag_entry.get_text().split()

        if len(title.replace(" ", "").replace("\n", "")) == 0 or len(text.replace(" ", "").replace("\n", "")) == 0 or len(tags) == 0:
            self.warning_label.grid(row=8, column=0)
        else:
            self.warning_label.grid_forget()
            create_command(title, text, tags)

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            ttk.Style().configure("create.TLabel", background="#1f2226", foreground="#b6bfcc")
        else:
            ttk.Style().configure("create.TLabel", background="#DDDDDD", foreground="#000000")
        self.tag_entry.swap_mode()
        self.text_entry.swap_mode()
        self.title_entry.swap_mode()
        self.submit_button.swap_mode()

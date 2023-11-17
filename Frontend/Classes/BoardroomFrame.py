class BoardroomFrame(ttk.Frame):
    def __init__(self, master, title, text, like_command, edit_command, delete_command, reply_command, like_count, poster, is_owned=False, is_liked=False):
        super().__init__(master)
        self.is_liked = is_liked

        self.label_text = StringVar()
        self.label_text.set(text)

        ttk.Style().configure("title.TLabel", font=("Segoe UI Historic", 28), relief="flat")
        self.title_label = ttk.Label(self, text=title, justify="left", style="title.TLabel", padding=10)

        self.text_label = ttk.Label(self, textvariable=self.label_text, padding=[25, 0, 0, 0])


        self.liked_image = tk.PhotoImage(file="Frontend/Assets/liked.png")
        self.liked_image = self.liked_image.subsample(2)
        self.not_liked_image = tk.PhotoImage(file="Frontend/Assets/not_liked.png")
        self.not_liked_image = self.not_liked_image.subsample(2)

        self.like_button = self.like_button = ttk.Button(self, style="like.TButton",
                                      command=lambda: self.execute_like_command(like_command), padding=0)
        if is_liked:
            self.like_button.configure(image=self.liked_image)
        else:
            self.like_button.configure(image=self.not_liked_image)

        self.like_count = StringVar()
        self.like_count.set(str(like_count))
        self.like_count_label = ttk.Label(self, textvariable=self.like_count, padding=5,
                                          font=("Segoe UI Historic", 8))

        ttk.Style().configure("postbottom.TButton", font=("Segoe UI Symbol", 10), padding=0)
        if is_owned:
            self.edit_button = ttk.Button(self, text="Edit Post", command=edit_command, style="postbottom.TButton")
            self.delete_button = ttk.Button(self, text="Delete Post", command=delete_command,
                                            style="postbottom.TButton")
            self.edit_button.grid(row=6, column=26)
            self.delete_button.grid(row=6, column=27)

        self.reply_button = ttk.Button(self, text="Reply", command=reply_command, style="postbottom.TButton")
        self.reply_button.grid(row=6, column=28)
        self.user_frame = UserFrame(self, user)

        self.like_button.grid(row=1, column=0)
        self.like_count_label.grid(row=2, column=0)
        self.title_label.grid(row=0, column=0, columnspan=30, sticky="w")
        self.text_label.grid(row=1, column=1, rowspan=5, columnspan=29, sticky="w")
        self.user_frame.grid(row=6, column=0)

    def execute_like_command(self, like_command):
        self.is_liked = not self.is_liked
        if self.is_liked:
            self.like_button.configure(image=self.liked_image)
            self.like_count.set(str(int(self.like_count.get()) + 1))
        else:
            self.like_button.configure(image=self.not_liked_image)
            self.like_count.set(str(int(self.like_count.get()) - 1))
        like_command()

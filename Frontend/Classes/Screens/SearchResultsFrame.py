from tkinter import ttk

from Backend.Classes.Models.User import User
from Frontend.Classes.Components.ResultFrame import ResultFrame
from Frontend.Classes.Widgets.ScrollFrame import ScrollFrame


class SearchResultsFrame(ttk.Frame):
    def __init__(self, master, database_response, open_command, dark_mode=False, **kwargs):
        super().__init__(master, **kwargs)
        self.dark_mode = dark_mode
        if dark_mode:
            ttk.Style().configure("border.TFrame", background="#969fac")
        else:
            ttk.Style().configure("border.TFrame", background="#666666")


        self.border_list = []

        self.result_list = []

        if len(database_response["posts"]):
            self.results = ScrollFrame(self, dark_mode)
            for post in database_response["posts"]:
                border = ttk.Frame(self.results.frame, height=1, style="border.TFrame")
                border.pack(side="top", fill="x", expand=1)

                poster = post["post_creator"]
                poster = User(poster["id"], poster["email"], poster["name"])

                result_frame = ResultFrame(self.results.frame, post["post_title"], post["post_text"], post["post_tags"],
                                           post["post_views"], post["post_likes"], post["post_replies"], poster,
                                           post["post_id"], post["post_time"], open_command, dark_mode)
                result_frame.pack(side="top", fill="x", expand=1)


                self.border_list.append(border)
                self.result_list.append(result_frame)
            self.results.pack(fill="both", expand=1)
        else:
            self.no_results_label = ttk.Label(self, text="Sorry, but it looks like nothing matched your search.\n"
                                                         "How about searching something else?", font=("Segoe UI", 30),
                                              justify="center", padding=[0, 50, 0, 0])
            self.no_results_label.grid(column=1)
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(2, weight=1)

    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if len(self.result_list) > 0:
            self.results.swap_mode()
        if self.dark_mode:
            ttk.Style().configure("border.TFrame", background="#969fac")
        else:
            ttk.Style().configure("border.TFrame", background="#666666")

        for result_frame in self.result_list:
            result_frame.swap_mode()

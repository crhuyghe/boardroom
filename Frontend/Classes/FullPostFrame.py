from Classes.Models.User import User
from Frontend.Classes.BoardroomFrame import BoardroomFrame
from Frontend.Classes.ReplyFrame import ReplyFrame
from Frontend.Classes.ScrollFrame import ScrollFrame


class FullPostFrame(ScrollFrame):
    def __init__(self, master, database_response, current_user, like_command, edit_command, delete_command,
                 reply_command, dark_mode=False, **kwargs):
        super().__init__(master, dark_mode, **kwargs)
        poster = database_response["post_creator"]
        poster = User(poster["id"], poster["email"], poster["name"])
        self.boardroom_frame = BoardroomFrame(self.frame, database_response["post_title"],
                                              database_response["post_text"], lambda pid: like_command(pid, None),
                                              lambda pid: edit_command(pid, None),
                                              lambda pid: delete_command(pid, None),
                                              lambda pid: reply_command(pid, None), database_response["post_views"],
                                              database_response["post_likes"], poster, database_response["post_time"],
                                              database_response["post_id"], database_response["post_is_edited"],
                                              current_user.id == poster.id, database_response["post_is_liked"],
                                              dark_mode, padding=[0, 0, 0, 50])

        self.reply_list = []

        self.boardroom_frame.pack(side="top", fill="x", expand=1, padx=(100, 50))
        for reply in database_response["post_replies"]:
            replier = reply["reply_creator"]
            replier = User(replier["id"], replier["email"], replier["name"])
            reply_frame = ReplyFrame(self.frame, reply["reply_text"], lambda pid, rid: like_command(pid, rid),
                                     lambda pid, rid: edit_command(pid, rid),
                                     lambda pid, rid: delete_command(pid, rid), reply["reply_likes"], replier,
                                     reply["reply_time"], reply["reply_id"], self.boardroom_frame.post_id,
                                     reply["reply_is_edited"], current_user.id == replier.id, reply["reply_is_liked"],
                                     dark_mode, padding=10)
            reply_frame.pack(side="top", fill="x", expand=1, padx=(200, 100))
            self.reply_list.append(reply_frame)

    def swap_mode(self):
        super().swap_mode()
        self.boardroom_frame.swap_mode()
        for reply_frame in self.reply_list:
            reply_frame.swap_mode()

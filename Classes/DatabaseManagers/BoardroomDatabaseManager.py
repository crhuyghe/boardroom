import pandas as pd
from Classes.Models.Boardroom import Boardroom
from Classes.Models.Message import Message
from Classes.Models.User import User


class BoardroomDatabaseManager:
    wd = __file__[:str(__file__).rindex("\\")][:__file__[:str(__file__).rindex("\\")].rindex("\\")][
         :__file__[:str(__file__).rindex("\\")][:__file__[:str(__file__).rindex("\\")].rindex("\\")].rindex("\\")]
    df = None
    df_file = ""
    reply_df = None
    reply_df_file = ""
    tag_df = None
    tag_df_file = ""
    post_tag_df = None
    post_tag_df_file = ""

    def __init__(self):
        """Controls functionality for reading the boardroom databases."""
        self.df_file = f"{self.wd}\\Database\\Boardrooms.csv"
        self.reply_df_file = f"{self.wd}\\Database\\Replies.csv"
        self.tag_df_file = f"{self.wd}\\Database\\Tags.csv"
        self.post_tag_df_file = f"{self.wd}\\Database\\PostsToTags.csv"
        self.df = pd.read_csv(self.df_file)
        self.reply_df = pd.read_csv(self.reply_df_file)
        self.tag_df = pd.read_csv(self.tag_df_file)
        self.post_tag_df = pd.read_csv(self.post_tag_df_file)

    def get_post(self, post_id, userDB):
        """Takes arguments to locate a specified entry in the database"""
        if len(self.df) > post_id and self.df.iloc[post_id].title != "###DELETED###":
            post = self.df.iloc[post_id]
            search_row = userDB.search("id", post.poster_id)
            post_creator = User(search_row.id.values[0], search_row.email.values[0], search_row.name.values[0])
            if str(search_row.picture_link.values[0]) != "nan":
                post_creator.picture = search_row.picture_link.values[0]
            else:
                post_creator.picture = False
            return Boardroom(post.id, post_creator, post.title, self.get_post_tags(post.id), post.text,
                             post.view_count, post.like_count, post.is_edited), post.post_time
        else:
            raise ValueError

    def get_post_replies(self, post_id, userDB) -> list[tuple[Message, int, pd.Timestamp]]:
        replies = []

        rows = self.reply_df.loc[self.reply_df["post_id"] == post_id]

        for i in range(len(rows)):
            row = rows.iloc[i]
            search_row = userDB.search("id", row.poster_id)
            reply_creator = User(search_row.id.values[0], search_row.email.values[0], search_row.name.values[0])
            if str(search_row.picture_link.values[0]) != "nan":
                reply_creator.picture = search_row.picture_link.values[0]
            else:
                reply_creator.picture = False
            replies.append((Message(row.reply_id, reply_creator, post_id, row.text, row.is_edited),
                            int(row.like_count), row.post_time))

        return replies

    def write_post(self, title, tags: list, text, current_user):
        """Takes a title, tags, and text as well as the current user in order to add a new post to the database"""
        tag_ids = self.find_tags(tags)
        if len(self.df) == 0:
            new_boardroom = Boardroom(0, current_user, title, tag_ids, text, 0, 0, False)
            self.df = pd.DataFrame([new_boardroom.format_for_dataframe()])
        else:
            new_boardroom = Boardroom(self.df["id"].iloc[-1] + 1, current_user, title, tag_ids, text, 0, 0, False)
            self.df = pd.concat((self.df, pd.DataFrame([new_boardroom.format_for_dataframe()])), ignore_index=False)
        self.link_tags(tag_ids, new_boardroom.id)
        self.__update_posts()
        return new_boardroom

    def write_post_reply(self, post_id, text, current_user):
        if len(self.df) > post_id and self.df.iloc[post_id].title != "###DELETED###":
            rows = self.reply_df.loc[self.reply_df["post_id"] == post_id].reply_id.values
            if len(rows) != 0:
                reply_id = rows[-1] + 1
            else:
                reply_id = 0
            new_reply = Message(reply_id, current_user, post_id, text, False)
            new_row = pd.DataFrame([new_reply.format_for_reply_dataframe()])
            if len(self.reply_df) == 0:
                self.reply_df = new_row
            else:
                self.reply_df = pd.concat((self.reply_df, new_row), ignore_index=False)
            self.__update_replies()
        else:
            raise ValueError

    def get_post_tags(self, post_id):
        linked_rows = self.post_tag_df.loc[self.post_tag_df["post_id"] == post_id]
        tag_ids = []
        tags = []
        for i in range(len(linked_rows)):
            tag_ids.append(linked_rows.tag_id.values[i])
        for tag_id in tag_ids:
            tags.append(self.tag_df.iloc[tag_id].tag)
        return tags

    def find_tags(self, tags):
        """returns a list of ids for the input list of tags; adds tags to database if not already present."""
        tag_ids = []
        if len(self.tag_df) == 0:
            new_index = 0
            new_tags = []
            for tag in tags:
                tag_ids.append(new_index)
                new_tags.append({"id": new_index, "tag": tag})
                new_index += 1
            self.tag_df = pd.DataFrame(new_tags)
        else:
            new_index = self.tag_df["id"].iloc[-1] + 1
            for tag in tags:
                row = self.tag_df.loc[self.tag_df['tag'] == tag, "id"].values
                if len(row) == 0:
                    tag_ids.append(new_index)
                    self.tag_df = pd.concat((self.tag_df, pd.DataFrame([{"id": new_index, "tag": tag}])),
                                            ignore_index=False)
                    new_index += 1
                else:
                    tag_ids.append(row[0])
        self.__update_tags()
        return tag_ids

    def link_tags(self, tag_ids, post_id):
        new_entries = []
        for tag_id in tag_ids:
            new_entries.append({"tag_id": tag_id, "post_id": post_id})
        if len(self.post_tag_df) == 0:
            self.post_tag_df = pd.DataFrame([new_entries[0]])
            self.post_tag_df = pd.concat((self.post_tag_df, pd.DataFrame(new_entries[1:])), ignore_index=False)
        else:
            self.post_tag_df = pd.concat((self.post_tag_df, pd.DataFrame(new_entries)), ignore_index=False)
        self.post_tag_df.to_csv(self.post_tag_df_file, index=False)

    def modify_entry(self):
        """Takes arguments to modify an entry in the database"""
        print("hi")

    def delete_entry(self):
        print("hi")

    def __update_posts(self):
        """Writes current post database to file"""
        self.df.to_csv(self.df_file, index=False)

    def __update_replies(self):
        """Writes current reply database to file"""
        self.reply_df.to_csv(self.reply_df_file, index=False)

    def __update_tags(self):
        """Writes current tag database to file"""
        self.tag_df.to_csv(self.tag_df_file, index=False)

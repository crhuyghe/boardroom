import pandas as pd
from numpy import nan
import heapq
import re

from Classes.Models.Boardroom import Boardroom
from Classes.Models.Message import Message
from Classes.Models.User import User


class BoardroomDatabaseManager:
    wd = __file__[:str(__file__).rindex("\\")][:__file__[:str(__file__).rindex("\\")].rindex("\\")][
         :__file__[:str(__file__).rindex("\\")][:__file__[:str(__file__).rindex("\\")].rindex("\\")].rindex("\\")]

    def __init__(self):
        """Controls functionality for reading the boardroom databases."""
        self.df_file = f"{self.wd}\\Database\\Boardrooms.csv"
        self.reply_df_file = f"{self.wd}\\Database\\Replies.csv"
        self.tag_df_file = f"{self.wd}\\Database\\Tags.csv"
        self.post_tag_df_file = f"{self.wd}\\Database\\PostsToTags.csv"
        self.like_df_file = f"{self.wd}\\Database\\Likes.csv"
        self.df = pd.read_csv(self.df_file, dtype={"poster_id": "Int64", "view_count": "Int64"})
        self.reply_df = pd.read_csv(self.reply_df_file, dtype={"poster_id": "Int64"})
        self.tag_df = pd.read_csv(self.tag_df_file)
        self.post_tag_df = pd.read_csv(self.post_tag_df_file)
        self.like_df = pd.read_csv(self.like_df_file)

    def search_posts(self, keywords: str, tags: list):
        weights = []
        tag_ids = []
        keywords = keywords.split(" ")
        if '' in keywords:
            keywords.remove('')
        if '' in tags:
            tags.remove('')
        for i in range(len(self.df)):
            weights.append([i, 0])
        for tag in tags:
            tag_ids.append(self.tag_df.loc[self.tag_df["tag"] == tag, "id"].values[0])
        for tag_id in tag_ids:
            matches = self.post_tag_df.loc[self.post_tag_df["tag_id"] == tag_id, "post_id"].values
            for match in matches:
                weights[match][1] += 10
        for word in keywords:
            for index, row in self.df.iterrows():
                if not pd.isna(row.title):
                    weights[int(row.id)][1] += str(row.title).count(word) * 5 + str(row.text).count(word) * 2
        closest_matches = heapq.nlargest(min(20, len(self.df)), weights, key=lambda x: x[1])
        index = 0
        while index < len(closest_matches) and closest_matches[index][1] != 0:
            index += 1
        print(weights, closest_matches)
        closest_matches = closest_matches[:index]
        print(closest_matches)
        results = []

        for i in range(len(closest_matches)):
            row = self.df.iloc[i]
            results.append((row.title, int(row.poster_id), int(row.id),
                            len(self.like_df.loc[
                                    (self.like_df["post_id"] == int(row.id)) & (self.like_df["reply_id"] == -1)]),
                            int(row.view_count), str(row.post_time),
                            len(self.reply_df.loc[self.reply_df["post_id"] == int(row.id)])))
        return results


    def get_post(self, post_id, current_user):
        """Takes arguments to locate a specified entry in the database"""
        if len(self.df) > post_id and not pd.isna(self.df.iloc[post_id].title):
            post = self.df.iloc[post_id]
            if current_user.id != int(post.poster_id):
                self.df.loc[self.df['id'] == post_id, "view_count"] += 1
                post = self.df.iloc[post_id]
                self.__update_posts()
            likes, is_liked = self.get_likes(current_user, post_id)
            return Boardroom(post.id, int(post.poster_id), post.title, self.get_post_tags(post.id), post.text,
                             post.view_count, likes, post.is_edited), post.post_time, is_liked
        else:
            raise ValueError

    def get_post_replies(self, post_id, current_user) -> list[tuple[Message, int, pd.Timestamp, bool]]:
        replies = []

        rows = self.reply_df.loc[self.reply_df["post_id"] == post_id]

        for i in range(len(rows)):
            row = rows.iloc[i]
            if not pd.isna(row.poster_id):
                likes, is_liked = self.get_likes(current_user, post_id, i)
                replies.append((Message(row.reply_id, int(row.poster_id), post_id, row.text, row.is_edited),
                                likes, row.post_time, is_liked))

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

    def modify_post(self, post_id, modifications, user_id):
        if len(self.df) <= post_id or pd.isna(self.df.iloc[post_id].title):
            raise ValueError
        if self.df.iloc[post_id, 2] == user_id:
            if modifications["text"] is not False:
                self.df.iloc[post_id, 3] = modifications["text"]
                self.df.iloc[post_id, 6] = True
                self.__update_posts()
            if modifications["tags"] is not False:
                self.post_tag_df.drop(self.post_tag_df[self.post_tag_df["post_id"] == post_id].index, inplace=True)
                self.link_tags(self.find_tags(modifications["tags"]), post_id)
        else:
            raise KeyError

    def modify_post_reply(self, post_id, reply_id, new_text, user_id):
        post_nonexistent = len(self.df) <= post_id or pd.isna(self.df.iloc[post_id].title) or \
                           len(self.reply_df.loc[(self.reply_df["post_id"] == post_id) &
                                                 (self.reply_df["reply_id"] == reply_id)]) == 0 or \
                           pd.isna(self.reply_df.loc[(self.reply_df["post_id"] == post_id) &
                                                     (self.reply_df["reply_id"] == reply_id), "poster_id"].values[0])
        if post_nonexistent:
            raise ValueError
        if self.reply_df.loc[(self.reply_df["post_id"] == post_id) & (self.reply_df["reply_id"] == reply_id),
                             "poster_id"].values[0] == user_id:
            self.reply_df.loc[(self.reply_df["post_id"] == post_id) & (self.reply_df["reply_id"] == reply_id),
                              "text"] = new_text
            self.reply_df.loc[(self.reply_df["post_id"] == post_id) & (self.reply_df["reply_id"] == reply_id),
                              "is_edited"] = True

            self.__update_replies()
        else:
            raise KeyError

    def delete_post(self, post_id, user_id):
        if len(self.df) <= post_id or pd.isna(self.df.iloc[post_id].title):
            raise ValueError
        if self.df.iloc[post_id, 2] == user_id:
            self.df.iloc[post_id, 1] = nan
            self.df.iloc[post_id, 2] = nan
            self.df.iloc[post_id, 3] = nan
            self.df.iloc[post_id, 4] = nan
            self.df.iloc[post_id, 5] = nan
            self.df.iloc[post_id, 6] = False

            self.reply_df.drop(self.reply_df[self.reply_df["post_id"] == post_id].index, inplace=True)
            self.like_df.drop(self.like_df[self.like_df["post_id"] == post_id].index, inplace=True)
            self.post_tag_df.drop(self.post_tag_df[self.post_tag_df["post_id"] == post_id].index, inplace=True)

            self.__update_posts()
            self.__update_replies()
            self.__update_likes()
            self.__update_post_tags()
        else:
            raise KeyError

    def delete_post_reply(self, post_id, reply_id, user_id):
        post_nonexistent = len(self.df) <= post_id or pd.isna(self.df.iloc[post_id].title) or \
                           len(self.reply_df.loc[(self.reply_df["post_id"] == post_id) &
                                                 (self.reply_df["reply_id"] == reply_id)]) == 0 or \
                           pd.isna(self.reply_df.loc[(self.reply_df["post_id"] == post_id) &
                                                     (self.reply_df["reply_id"] == reply_id), "poster_id"].values[0])
        if post_nonexistent:
            raise ValueError
        if self.reply_df.loc[(self.reply_df["post_id"] == post_id) & (self.reply_df["reply_id"] == reply_id),
                          "poster_id"].values[0] == user_id:
            self.reply_df.loc[(self.reply_df["post_id"] == post_id) & (self.reply_df["reply_id"] == reply_id),
                              "poster_id"] = nan
            self.reply_df.loc[(self.reply_df["post_id"] == post_id) & (self.reply_df["reply_id"] == reply_id),
                              "text"] = nan
            self.reply_df.loc[(self.reply_df["post_id"] == post_id) & (self.reply_df["reply_id"] == reply_id),
                              "post_time"] = nan
            self.reply_df.loc[(self.reply_df["post_id"] == post_id) & (self.reply_df["reply_id"] == reply_id),
                              "is_edited"] = False
            self.like_df.drop(self.like_df[(self.like_df["post_id"] == post_id) &
                                           (self.like_df["reply_id"] == reply_id)].index, inplace=True)

            self.__update_replies()
            self.__update_likes()
        else:
            raise KeyError

    def toggle_like(self, current_user, post_id, reply_id=-1):
        """Increases the like count of a post or reply if the user has not already liked it, and decreases it
        otherwise."""
        post_nonexistent = len(self.df) <= post_id or pd.isna(self.df.iloc[post_id].title) or (reply_id != -1 and
            (len(self.reply_df.loc[(self.reply_df["post_id"] == post_id) & (self.reply_df["reply_id"] == reply_id)]) ==
             0 or pd.isna(self.reply_df.loc[(self.reply_df["post_id"] == post_id) & (self.reply_df["reply_id"] ==
                                                                                reply_id), "poster_id"].values[0])))
        if post_nonexistent:
            raise ValueError
        if len(self.like_df.loc[(self.like_df["user_id"] == current_user.id) & (self.like_df["post_id"] == post_id) &
                                (self.like_df["reply_id"] == reply_id)]) == 0:
            if len(self.like_df) == 0:
                self.like_df = pd.DataFrame([{"user_id": current_user.id, "post_id": post_id, "reply_id": reply_id}])
            else:
                self.like_df = pd.concat((self.like_df, pd.DataFrame([{"user_id": current_user.id, "post_id": post_id,
                                                                       "reply_id": reply_id}])), ignore_index=False)
            self.__update_likes()
        else:
            self.like_df.drop(self.like_df[(self.like_df["user_id"] == current_user.id) &
                                           (self.like_df["post_id"] == post_id) &
                                           (self.like_df["reply_id"] == reply_id)].index, inplace=True)
            self.__update_likes()

    def get_likes(self, current_user, post_id, reply_id=-1):
        """Detects how many likes a given post or reply has along with whether the current user has liked it"""
        rows = self.like_df.loc[(self.like_df["post_id"] == post_id) & (self.like_df["reply_id"] == reply_id)]
        return len(rows), len(rows.loc[rows["user_id"] == current_user.id]) == 1

    def clear_activity(self, user_id):
        """Clears the activity of a given user"""
        for post_id in self.df.loc[self.df["poster_id"] == user_id, "id"].values:
            self.delete_post(post_id, user_id)
        for index, row in self.reply_df.loc[self.reply_df["poster_id"] == user_id].iterrows():
            self.delete_post_reply(row.post_id, row.reply_id, user_id)

        self.like_df.drop(self.like_df[self.like_df["user_id"] == user_id].index, inplace=True)

        self.__update_posts()
        self.__update_replies()
        self.__update_likes()

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
        self.__update_post_tags()

    def __update_posts(self):
        """Writes current post database to file"""
        self.df.to_csv(self.df_file, index=False)

    def __update_replies(self):
        """Writes current reply database to file"""
        self.reply_df.to_csv(self.reply_df_file, index=False)

    def __update_tags(self):
        """Writes current tag database to file"""
        self.tag_df.to_csv(self.tag_df_file, index=False)

    def __update_post_tags(self):
        """Writes current post-tag database to file"""
        self.post_tag_df.to_csv(self.post_tag_df_file, index=False)

    def __update_likes(self):
        """Writes current like database to file"""
        self.like_df.to_csv(self.like_df_file, index=False)

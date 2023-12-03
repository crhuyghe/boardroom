import pandas as pd
import numpy as np

from Backend.Classes.Models.Message import Message


class MessageDatabaseManager:
    wd = __file__[:str(__file__).rindex("\\")][:__file__[:str(__file__).rindex("\\")].rindex("\\")][
         :__file__[:str(__file__).rindex("\\")][:__file__[:str(__file__).rindex("\\")].rindex("\\")].rindex("\\")]

    def __init__(self):
        """Controls functionality for reading the message database."""
        self.df_file = f"{self.wd}\\Database\\Messages.csv"
        self.df = pd.read_csv(self.df_file, dtype={"user1_id": "Int64", "user2_id": "Int64"})

    def get_messages(self, participant_id, user_id):
        """Gets a list of messages exchanged between two users"""
        rows = self.df.loc[((self.df["receiver_id"] == participant_id) & (self.df["sender_id"] == user_id)) |
                           ((self.df["receiver_id"] == user_id) & (self.df["sender_id"] == participant_id))]
        message_list = []
        for i in range(len(rows)):
            current_row = rows.iloc[i]
            if not pd.isna(current_row.text):
                current_message = Message(int(current_row.id), int(current_row.sender_id), int(current_row.receiver_id),
                                          current_row.text, bool(current_row.is_edited))
                message_list.append((current_message, str(current_row.post_time)))
        return message_list

    def get_conversations(self, user_id):
        """Gets a list of conversations between users"""
        rows = self.df.loc[(self.df["sender_id"] == user_id) | (self.df["receiver_id"] == user_id)]
        logged_conversations = set()
        conversations = []
        for i in range(len(rows)):
            row = rows.iloc[len(rows)-1-i]
            if not pd.isna(row.text):
                s_id = int(row.sender_id)
                r_id = int(row.receiver_id)
                if (min(s_id, r_id), max(s_id, r_id)) not in logged_conversations:
                    if user_id != s_id:
                        participant_id = s_id
                    else:
                        participant_id = r_id
                    logged_conversations.add((min(s_id, r_id), max(s_id, r_id)))
                    conversations.append((participant_id, row.text, str(row.post_time)))
        return [conversations[len(conversations)-1-i] for i in range(len(conversations))]

    def write_message(self, recipient_id, text, user_id):
        """Takes arguments to write a new entry into the database"""
        if len(self.df) == 0:
            new_message = Message(0, user_id, recipient_id, text, False)
            self.df = pd.DataFrame([new_message.format_for_message_dataframe()])
        else:
            new_id = 0
            id_values = self.df.loc[((self.df["receiver_id"] == recipient_id) & (self.df["sender_id"] == user_id)) |
                                    ((self.df["receiver_id"] == user_id) & (self.df["sender_id"] == recipient_id)),
                                    "id"].values
            if len(id_values) != 0:
                new_id = id_values[-1] + 1
            new_message = Message(new_id, user_id, recipient_id, text, False)
            self.df = pd.concat((self.df, pd.DataFrame([new_message.format_for_message_dataframe()])),
                                ignore_index=True)
        self.__updateDF()
        return new_message

    def edit_message(self, user_id, recipient_id, message_id, text):
        """Edits a specified message in the database"""
        row = self.df.loc[((self.df["sender_id"] == user_id) & (self.df["receiver_id"] == recipient_id) |
                           (self.df["sender_id"] == recipient_id) & (self.df["receiver_id"] == user_id)) &
                          (self.df["id"] == message_id)]
        if len(row) > 0 and not pd.isna(row.text.values[0]):
            if int(row.sender_id.values[0]) == user_id:
                self.df.loc[(self.df["sender_id"] == user_id) & (self.df["receiver_id"] == recipient_id) &
                            (self.df["id"] == message_id), "text"] = text
                self.df.loc[(self.df["sender_id"] == user_id) & (self.df["receiver_id"] == recipient_id) &
                            (self.df["id"] == message_id), "is_edited"] = True
                self.__updateDF()
            else:
                raise KeyError
        else:
            raise ValueError

    def delete_message(self, user_id, recipient_id, message_id):
        """Deletes a specified message from the database"""
        row = self.df.loc[((self.df["sender_id"] == user_id) & (self.df["receiver_id"] == recipient_id) |
                           (self.df["sender_id"] == recipient_id) & (self.df["receiver_id"] == user_id)) &
                          (self.df["id"] == message_id)]
        if len(row) > 0 and not pd.isna(row.text.values[0]):
            if int(row.sender_id.values[0]) == user_id:
                self.df.loc[(self.df["sender_id"] == user_id) & (self.df["receiver_id"] == recipient_id) &
                            (self.df["id"] == message_id), "text"] = np.nan
                self.df.loc[(self.df["sender_id"] == user_id) & (self.df["receiver_id"] == recipient_id) &
                            (self.df["id"] == message_id), "post_time"] = np.nan
                self.df.loc[(self.df["sender_id"] == user_id) & (self.df["receiver_id"] == recipient_id) &
                            (self.df["id"] == message_id), "is_edited"] = False
                self.__updateDF()
            else:
                raise KeyError
        else:
            raise ValueError

    def clear_activity(self, user_id):
        """Clears all conversations involving a specific user"""
        self.df.drop(self.df[(self.df["sender_id"] == user_id) | (self.df["receiver_id"] == user_id)].index,
                     inplace=True)
        self.__updateDF()

    def __updateDF(self):
        """Writes current databases to file"""
        self.df.to_csv(self.df_file, index=False)

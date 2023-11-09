import pandas as pd

from Classes.Models.Message import Message


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
            current_message = Message(int(current_row.id), int(current_row.sender_id), int(current_row.receiver_id),
                                      current_row.text, bool(current_row.is_edited))
            message_list.append((current_message, str(current_row.post_time)))
        return message_list


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
                                ignore_index=False)
        self.__updateDF()

    def modify_entry(self):
        """Takes arguments to modify an entry in the database"""
        print("hi")

    def delete_entry(self):
        print("hi")

    def __updateDF(self):
        """Writes current databases to file"""
        self.df.to_csv(self.df_file, index=False)

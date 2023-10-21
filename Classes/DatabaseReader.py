import json
import pandas as pd
from Classes.User import User
from Classes.Boardroom import Boardroom
from Classes.Message import Message

class DatabaseReader:
    wd = __file__[:str(__file__[:str(__file__).rindex("\\")]).rindex("\\")]
    mode = ""
    df = None
    df_file = ""
    reply_df = None
    reply_df_file = ""

    def __init__(self, mode: str):
        """Controls functionality for reading databases.\nAcceptable modes are:
        'boardroom'\n\n'message'\n\n'user'"""
        self.mode = mode
        if mode == "boardroom":
            self.df_file = f"{self.wd}\\Database\\Boardrooms.csv"
            self.reply_df_file = f"{self.wd}\\Database\\Replies.csv"
            self.df = pd.read_csv(self.df_file)
            self.reply_df = pd.read_csv(self.reply_df_file)
        elif mode == "message":
            self.df_file = f"{self.wd}\\Database\\Messages.csv"
            self.df = pd.read_csv(self.df_file)
        elif mode == "user":
            self.df_file = f"{self.wd}\\Database\\Users.csv"
            self.df = pd.read_csv(self.df_file)
        else:
            raise ValueError

    def readEntry(self, *args):
        """Takes arguments to locate a specified entry in the database"""
        print("hi")

    def writeEntry(self, *args):
        """Takes arguments to write a new entry into the database"""
        if self.mode == "boardroom":
            print("hi")
        elif self.mode == "user":
            if args[0] in self.df["email"].tolist():
                raise ValueError
            if len(self.df) == 0:
                new_user = User(0, args[0], args[1])
                self.df = pd.DataFrame([new_user.format_with_password(self.decrypt(args[2]))])
            else:
                new_user = User(self.df["id"].iloc[-1] + 1, args[0], args[1])
                self.df = pd.concat((self.df,
                    pd.DataFrame([new_user.format_with_password(self.decrypt(args[2]))])), ignore_index=False)
            print(self.df)
            self.df.to_csv(self.df_file, index=False)
            return new_user
        else:
            print("hi")

    def modifyEntry(self, *args):
        """Takes arguments to modify an entry in the database"""
        print("hi")

    def deleteEntry(self, *args):
        """Takes arguments to delete an entry in the database"""
        print("hi")

    def search(self, *args):
        """For user and boardroom databases; Allows searching for users/boardrooms"""
        if self.mode == "boardroom":
            print("hi")
        elif self.mode == "user":
            row = self.df.loc[self.df["email"] == args[0]]
            # return User(self.df)
        else:
            raise Exception("search not supported on message database")

    @staticmethod
    def decrypt(password: str) -> str:
        return password

import json
import pandas as pd
from Classes.User import User
from Classes.Boardroom import Boardroom
from Classes.Message import Message
from Classes.Errors import IncorrectPasswordError, AccountLockoutError

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
        if self.mode == "boardroom":
            print("hi")
        if self.mode == "user":
            row = self.search("email", args[0])
            if len(row) == 0:
                raise KeyError
            self.__check_lockout(row.id.values[0])
            if self.__decrypt(args[1]) == row.password.values[0]:
                return User(row.id.values[0], row.email.values[0], row.name.values[0])
            else:
                self.__increment_lockout_counter(row.id.values[0])
        else:
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
                self.df = pd.DataFrame([new_user.format_with_password(self.__decrypt(args[2]))])
            else:
                new_user = User(self.df["id"].iloc[-1] + 1, args[0], args[1])
                self.df = pd.concat((self.df,
                    pd.DataFrame([new_user.format_with_password(self.__decrypt(args[2]))])), ignore_index=False)
            self.__updateDF()
            return new_user
        else:
            print("hi")

    def modifyEntry(self, *args):
        """Takes arguments to modify an entry in the database"""
        if self.mode == "boardroom":
            print("hi")
        elif self.mode == "user":
            row = self.search("id", args[0].id)
            self.__check_lockout(row.id.values[0])
            if self.__decrypt(args[1]) == row.password.values[0]:
                if args[2]["picture"] is not False:
                    self.df.loc[self.df['id'] == args[0].id, "picture_link"] = args[2]["picture"]
                if args[2]["email"] is not False:
                    self.df.loc[self.df['id'] == args[0].id, "email"] = args[2]["email"]
                if args[2]["password"] is not False:
                    self.df.loc[self.df['id'] == args[0].id, "password"] = args[2]["password"]
                if args[2]["name"] is not False:
                    self.df.loc[self.df['id'] == args[0].id, "name"] = args[2]["name"]
                self.__updateDF()

                row = self.search("id", args[0].id)
                return User(row.id.values[0], row.email.values[0], row.name.values[0])
            else:
                self.__increment_lockout_counter(row.id.values[0])
        else:
            print("hi")

                # self.df.drop(self.df[self.df["id"] == args[0].id].index, inplace=True)
                # self.__updateDF()
    def deleteEntry(self, *args):
        """Takes arguments to delete an entry in the database"""
        if self.mode == "boardroom":
            print("hi")
        elif self.mode == "user":
            row = self.search("id", args[0].id)
            self.__check_lockout(row.id.values[0])
            if self.__decrypt(args[1]) == row.password.values[0]:
                self.df.drop(self.df[self.df["id"] == args[0].id].index, inplace=True)
                self.__updateDF()
            else:
                self.__increment_lockout_counter(row.id.values[0])
        else:
            print("hi")

    def search(self, *args):
        """For user and boardroom databases; Allows searching for users/boardrooms"""
        if self.mode == "boardroom":
            print("hi")
        elif self.mode == "user":
            if args[0] == "email":
                return self.df.loc[self.df["email"] == args[1]]
            elif args[0] == "id":
                return self.df.loc[self.df["id"] == args[1]]
        else:
            raise Exception("search not supported on message database")

    def __updateDF(self):
        """Writes current databases to file"""
        self.df.to_csv(self.df_file, index=False)
        if self.mode == "boardroom":
            self.reply_df.to_csv(self.reply_df_file, index=False)

    def __increment_lockout_counter(self, user_id):
        """Increments login attempt counter on entries and raises appropriate error"""
        self.df.loc[self.df['id'] == user_id, "login_attempts"] += 1
        self.__updateDF()
        self.__check_lockout(user_id)
        raise IncorrectPasswordError

    def __check_lockout(self, user_id):
        if self.search("id", user_id).login_attempts.values[0] == 3:
            raise AccountLockoutError

    @staticmethod
    def __decrypt(password: str) -> str:
        return password

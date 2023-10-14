import json
import pandas as pd
from Classes.User import User
from Classes.Boardroom import Boardroom
from Classes.Message import Message

class DatabaseReader:
    wd = __file__[:str(__file__[:str(__file__).rindex("\\")]).rindex("\\")]
    mode = ""
    df = None

    def __init__(self, mode: str):
        """Controls functionality for reading databases.\nAcceptable modes are:
        'boardroom'\n\n'message'\n\n'user'"""
        self.mode = mode
        if mode == "boardroom":
            df = pd.read_csv(f"{self.wd}\\Database\\Boardrooms.csv")
        elif mode == "message":
            df = pd.read_csv(f"{self.wd}\\Database\\Messages.csv")
        elif mode == "user":
            df = pd.read_csv(f"{self.wd}\\Database\\Users.csv")
        else:
            raise ValueError

    def readEntry(self, *args):
        """Takes arguments to locate a specified entry in the database"""
        print("hi")

    def writeEntry(self, *args):
        """Takes arguments to write a new entry into the database"""
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
            print("hi")
        else:
            raise Exception("search not supported on message database")

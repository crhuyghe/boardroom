import pandas as pd


class MessageDatabaseManager:
    wd = __file__[:str(__file__).rindex("\\")][:__file__[:str(__file__).rindex("\\")].rindex("\\")][
         :__file__[:str(__file__).rindex("\\")][:__file__[:str(__file__).rindex("\\")].rindex("\\")].rindex("\\")]
    df = None
    df_file = ""

    def __init__(self):
        """Controls functionality for reading the message database."""
        self.df_file = f"{self.wd}\\Database\\Messages.csv"
        self.df = pd.read_csv(self.df_file)

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
        print("hi")

    def __updateDF(self):
        """Writes current databases to file"""
        self.df.to_csv(self.df_file, index=False)

import pandas as pd
from Classes.Models.User import User
from Classes.Errors import IncorrectPasswordError, AccountLockoutError

class UserDatabaseManager:
    wd = __file__[:str(__file__).rindex("\\")][:__file__[:str(__file__).rindex("\\")].rindex("\\")][
         :__file__[:str(__file__).rindex("\\")][:__file__[:str(__file__).rindex("\\")].rindex("\\")].rindex("\\")]
    df = None
    df_file = ""

    def __init__(self):
        """Controls functionality for reading the user database."""
        self.df_file = f"{self.wd}\\Database\\Users.csv"
        self.df = pd.read_csv(self.df_file)

    def login_account(self, email, password):
        """Takes the email and password for an account. Checks for the existence of account, and verifies the\nvalidity
        of the password. Returns the account if the password is correct, increments lockout counter otherwise."""
        row = self.search("email", email)
        if len(row) == 0:
            raise KeyError
        self.__check_lockout(row.id.values[0])
        if self.__decrypt(password) == row.password.values[0]:
            if self.df.loc[self.df['id'] == row.id.values[0], "login_attempts"].values[0] != 0:
                self.df.loc[self.df['id'] == row.id.values[0], "login_attempts"] = 0
                self.__updateDF()
            return User(row.id.values[0], row.email.values[0], row.name.values[0])
        else:
            self.__increment_lockout_counter(row.id.values[0])


    def create_account(self, email, name, password):
        """Creates a new account in the database from a given email, name, and password. Raises an error if the\n
        account already exists. Returns the new account entry"""
        if email in self.df["email"].tolist():
            raise ValueError
        if len(self.df) == 0:
            new_user = User(0, email, name)
            self.df = pd.DataFrame([new_user.format_with_password(self.__decrypt(password))])
        else:
            new_user = User(self.df["id"].iloc[-1] + 1, email, name)
            self.df = pd.concat((self.df,
                pd.DataFrame([new_user.format_with_password(self.__decrypt(password))])), ignore_index=False)
        self.__updateDF()
        return new_user

    def modify_account(self, user_id, password, modifications):
        """Takes a user_id, password, and a list of modifications. Verifies password, and makes necessary changes to\n
        the database."""
        row = self.search("id", user_id)
        self.__check_lockout(row.id.values[0])
        if self.__decrypt(password) == row.password.values[0]:
            if modifications["picture"] is not False:
                self.df.loc[self.df['id'] == user_id, "picture_link"] = modifications["picture"]
            if modifications["email"] is not False:
                self.df.loc[self.df['id'] == user_id, "email"] = modifications["email"]
            if modifications["password"] is not False:
                self.df.loc[self.df['id'] == user_id, "password"] = modifications["password"]
            if modifications["name"] is not False:
                self.df.loc[self.df['id'] == user_id, "name"] = modifications["name"]
            self.__updateDF()

            row = self.search("id", user_id)
            return User(row.id.values[0], row.email.values[0], row.name.values[0])
        else:
            self.__increment_lockout_counter(row.id.values[0])

    def delete_account(self, user_id, password):
        """Takes a user id and password and deletes the account, if the password is correct."""
        row = self.search("id", user_id)
        self.__check_lockout(row.id.values[0])
        if self.__decrypt(password) == row.password.values[0]:
            self.df.drop(self.df[self.df["id"] == user_id].index, inplace=True)
            self.__updateDF()
        else:
            self.__increment_lockout_counter(row.id.values[0])

    def search(self, column, search_term):
        """Allows searching for users based on a given database value. Email and ID are always unique"""
        return self.df.loc[self.df[column] == search_term]

    def __updateDF(self):
        """Writes current database to file"""
        self.df.to_csv(self.df_file, index=False)

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
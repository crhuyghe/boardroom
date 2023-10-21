import pandas as pd

class User:
    id = -1
    email = ""
    name = ""
    picture = ""

    def __init__(self, user_id, email, name):
        self.id = user_id
        self.email = email
        self.name = name

    def format_with_password(self, password, time_created=pd.Timestamp.now()):
        return {"id": self.id, "email": self.email, "name": self.name, "password": password,
                "time_created": time_created, "picture_link": self.picture}

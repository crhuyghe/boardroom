import pandas as pd

class User:
    def __init__(self, user_id: int, email: str, name: str):
        self.id = int(user_id)
        self.email = email
        self.name = name
        self.picture = ""

    def format_for_response(self):
        return {"name": self.name, "email": self.email, "picture": self.picture, "id": self.id}

    def format_with_password(self, password, time_created=None, login_attempts=0):
        if time_created is None:
            time_created = pd.Timestamp.now()
        return {"id": self.id, "email": self.email, "name": self.name, "password": password,
                "time_created": time_created, "picture_link": self.picture,
                "login_attempts": int(login_attempts)}

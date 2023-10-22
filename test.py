import pandas as pd
import json

from Classes.DatabaseReader import DatabaseReader
from Classes.User import User
from Classes.Errors import IncorrectPasswordError, AccountLockoutError

boardroomDB = DatabaseReader("boardroom")
userDB = DatabaseReader("user")
messageDB = DatabaseReader("message")

decoder = json.JSONDecoder()
encoder = json.JSONEncoder()


def respond(message: dict):
    current_user = User(0, "cave.johnson@aperture.com", "Cave Johnson")
    response = {}

    if message["action"] == 1:  # Access Account
        try:
            current_user = userDB.readEntry(message["email"], message["password"])
            response["success"] = True
        except KeyError:
            response["success"] = False
            response["message"] = "Incorrect email or password"
            response["account_found"] = False
            response["lockout"] = False
        except IncorrectPasswordError:
            response["success"] = False
            response["message"] = "Incorrect email or password"
            response["account_found"] = True
            response["lockout"] = False
        except AccountLockoutError:
            response["success"] = False
            response["message"] = "Exceeded maximum login attempts. Account is locked until tomorrow."
            response["lockout"] = True

    elif message["action"] == 2:  # Create Account
        try:
            current_user = userDB.writeEntry(message["email"], message["name"], message["password"])
            response["success"] = True
        except ValueError:
            response["success"] = False
            response["message"] = "AccountExistsError"
        # finally:
        #     await websocket.send(encoder.encode(response))
    elif message["action"] == 3:
        print("CreatePost")
    elif message["action"] == 4:  # Delete Account
        try:
            userDB.deleteEntry(current_user, message["password"])
            current_user = None
        except IncorrectPasswordError:
            response["success"] = False
            response["message"] = "TempWrongPasswordError"
        # finally:
        #     await websocket.send(encoder.encode(response))
    elif message["action"] == 5:
        print("DeleteMessage")
    elif message["action"] == 6:
        print("EditMessage")
    elif message["action"] == 7:
        print("GetPost")
    elif message["action"] == 8:
        print("LikePost")
    elif message["action"] == 9:
        print("LikePostReply")
    elif message["action"] == 10:
        print("LogoutAccount")
    elif message["action"] == 11:
        print("ModifyAccount")
    elif message["action"] == 12:
        print("ModifyPost")
    elif message["action"] == 13:
        print("ModifyPostReply")
    elif message["action"] == 14:
        print("Refresh")
    elif message["action"] == 15:
        print("ReplyPost")
    elif message["action"] == 16:
        print("SearchPosts")
    elif message["action"] == 17:
        print("DeletePostReply")
    elif message["action"] == 18:
        print("DeletePost")
    elif message["action"] == 19:
        print("SendMessage")

    print(response)


# curr_message = {
#     "action": 2,
#     "email": "test@test.com",
#     "name": "test",
#     "password": "test"
# }
curr_message = {
    "action": 1,
    "email": "cave.johnson@aperture.com",
    "password": "IH8Lemons"
}
respond(curr_message)

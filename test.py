import json

from Classes.DatabaseManagers.BoardroomDatabaseManager import BoardroomDatabaseManager
from Classes.DatabaseManagers.MessageDatabaseManager import MessageDatabaseManager
from Classes.DatabaseManagers.UserDatabaseManager import UserDatabaseManager
from Classes.Models.User import User
from Classes.Errors import IncorrectPasswordError, AccountLockoutError

boardroomDB = BoardroomDatabaseManager()
userDB = UserDatabaseManager()
messageDB = MessageDatabaseManager()

decoder = json.JSONDecoder()
encoder = json.JSONEncoder()


def respond(message: dict):
    # current_user = User(0, "cave.johnson@aperture.com", "Cave Johnson")
    current_user = User(1, "test@test.com", "test")
    response = {}

    if message["action"] == 1:  # Access Account
        try:
            current_user = userDB.login_account(message["email"], message["password"])
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
            current_user = userDB.create_account(message["email"], message["name"], message["password"])
            response["success"] = True
        except ValueError:
            response["success"] = False
            response["message"] = "AccountExistsError"

    elif message["action"] == 3:
        print("CreatePost")

    elif message["action"] == 4:  # Delete Account
        try:
            userDB.delete_account(current_user.id, message["password"])
            current_user = None
            response["success"] = True
        except IncorrectPasswordError:
            response["success"] = False
            response["message"] = "Incorrect email or password"
            response["account_found"] = True
            response["lockout"] = False
        except AccountLockoutError:
            response["success"] = False
            response["message"] = "Exceeded maximum login attempts. Account is locked until tomorrow."
            response["lockout"] = True

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

    elif message["action"] == 10:  # Logout Account
        current_user = None
        response["success"] = True

    elif message["action"] == 11:  # Modify Account
        try:
            current_user = userDB.modify_account(current_user, message["password"], message["modifications"])
        except IncorrectPasswordError:
            response["success"] = False
            response["message"] = "Incorrect email or password"
            response["account_found"] = True
            response["lockout"] = False
        except AccountLockoutError:
            response["success"] = False
            response["message"] = "Exceeded maximum login attempts. Account is locked until tomorrow."
            response["lockout"] = True

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
#     "name": "Test Testington",
#     "password": "test"
# }
curr_message = {
    "action": 1,
    "email": "cave.johnson@aperture.com",
    "password": "IH8Lemons"
}

respond(curr_message)

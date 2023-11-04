import asyncio
import json
import websockets as ws
from websockets import server

from Classes.DatabaseManagers.BoardroomDatabaseManager import BoardroomDatabaseManager
from Classes.DatabaseManagers.MessageDatabaseManager import MessageDatabaseManager
from Classes.DatabaseManagers.UserDatabaseManager import UserDatabaseManager
from Classes.Errors import IncorrectPasswordError, AccountLockoutError

boardroomDB = BoardroomDatabaseManager()
userDB = UserDatabaseManager()
messageDB = MessageDatabaseManager()

decoder = json.JSONDecoder()
encoder = json.JSONEncoder()

# In the current state, hosts a localhost websocket on port 8765.
# This connection accepts messages from the client and echoes them back.
async def connection(websocket: server.WebSocketServerProtocol):
    try:
        print("New Connection:", websocket.id)
        current_user = None
        while True:
            message = decoder.decode(await websocket.recv())
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


            elif message["action"] == 3:  # Create Post
                boardroomDB.write_post(message["title"], message["tags"], message["text"], current_user)
                response["success"] = True

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

            elif message["action"] == 7:  # Get Post
                try:
                    post, post_time = boardroomDB.get_post(int(message["post_id"]), userDB)
                    response["success"] = True
                    response["post_title"] = post.title
                    response["post_id"] = post.id
                    response["post_creator"] = post.poster.format_for_response()
                    response["post_likes"] = post.likes
                    response["post_views"] = post.views
                    response["post_text"] = post.text
                    response["post_tags"] = post.tags
                    response["post_time"] = str(post_time)
                    response["post_is_edited"] = post.edited
                    response["post_replies"] = []
                    for reply, like_count, reply_time in boardroomDB.get_post_replies(post.id, userDB):
                        formatted_reply = {"reply_likes": like_count,
                                           "reply_text": reply.text,
                                           "reply_is_edited": reply.edited,
                                           "reply_id": reply.id,
                                           "reply_creator": reply.sender.format_for_response(),
                                           "reply_time": str(reply_time)}
                        response["post_replies"].append(formatted_reply)
                except ValueError:
                    response["success"] = False
                    response["message"] = "Post not found"

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


            elif message["action"] == 15:  # Reply Post
                try:
                    boardroomDB.write_post_reply(int(message["post_id"]), message["text"], current_user)
                    response["success"] = True
                except ValueError:
                    response["success"] = False
                    response["message"] = "Post does not exist"

            elif message["action"] == 16:
                print("SearchPosts")

            elif message["action"] == 17:
                print("DeletePostReply")

            elif message["action"] == 18:
                print("DeletePost")

            elif message["action"] == 19:
                print("SendMessage")

            print(message)
            await websocket.send(encoder.encode(response))

    except ws.ConnectionClosedOK:
        print("Client disconnected:", websocket.id)

    except ConnectionError:
        print("Client disconnected with error:", websocket.id)

async def main():
    async with ws.serve(connection, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    print("Launching server...")
    asyncio.run(main())

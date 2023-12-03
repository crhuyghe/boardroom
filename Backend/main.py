import asyncio
import json
import pandas as pd
import websockets as ws
from websockets import server

from Backend.Classes.DatabaseManagers.BoardroomDatabaseManager import BoardroomDatabaseManager
from Backend.Classes.DatabaseManagers.MessageDatabaseManager import MessageDatabaseManager
from Backend.Classes.DatabaseManagers.UserDatabaseManager import UserDatabaseManager
from Backend.Classes.Errors import IncorrectPasswordError, AccountLockoutError

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

            if current_user is None and (message["action"] != 1 and message["action"] != 2):
                message["action"] = -1
                response["success"] = False
                response["message"] = "Must log in before other requests may be sent"

            if message["action"] == 1:  # Access Account
                try:
                    current_user = userDB.login_account(message["email"], message["password"])
                    response["success"] = True
                    response["id"] = current_user.id
                    response["email"] = current_user.email
                    response["name"] = current_user.name
                    response["picture"] = False
                except KeyError:
                    response["success"] = False
                    response["message"] = "Incorrect email"
                    response["account_found"] = False
                    response["lockout"] = False
                except IncorrectPasswordError:
                    response["success"] = False
                    response["message"] = "Incorrect password"
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
                    response["id"] = current_user.id
                    response["email"] = current_user.email
                    response["name"] = current_user.name
                    response["picture"] = False
                except ValueError:
                    response["success"] = False
                    response["message"] = "An account with this email already exists"

            elif message["action"] == 3:  # Create Post
                new_post = boardroomDB.write_post(message["title"], message["tags"], message["text"], current_user)
                post, post_time, is_liked = boardroomDB.get_post(new_post.id, current_user)
                post.poster = userDB.get_user_by_id(post.poster)
                response["success"] = True
                response["post_title"] = post.title
                response["post_id"] = post.id
                response["post_creator"] = post.poster.format_for_response()
                response["post_likes"] = post.likes
                response["post_views"] = post.views
                response["post_text"] = post.text
                response["post_tags"] = post.tags
                response["post_time"] = str(post_time)
                response["post_is_liked"] = is_liked
                response["post_is_edited"] = post.edited
                response["post_replies"] = []

            elif message["action"] == 4:  # Delete Account
                try:
                    userDB.delete_account(current_user.id, message["password"])
                    boardroomDB.clear_activity(current_user.id)
                    messageDB.clear_activity(current_user.id)
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

            elif message["action"] == 5:  # Delete Message
                try:
                    messageDB.delete_message(current_user.id, int(message["recipient"]), int(message["message_id"]))
                    response["success"] = True
                except KeyError:
                    response["success"] = False
                    response["message"] = "Can only delete own messages"
                except ValueError:
                    response["success"] = False
                    response["message"] = "Message does not exist"

            elif message["action"] == 6:  # Edit Message
                try:
                    messageDB.edit_message(current_user.id, int(message["recipient"]), int(message["message_id"]),
                                           message["text"])
                    response["success"] = True
                except KeyError:
                    response["success"] = False
                    response["message"] = "Can only edit own messages"
                except ValueError:
                    response["success"] = False
                    response["message"] = "Message does not exist"

            elif message["action"] == 7:  # Get Post
                try:
                    post, post_time, is_liked = boardroomDB.get_post(int(message["post_id"]), current_user)
                    post.poster = userDB.get_user_by_id(post.poster)
                    response["success"] = True
                    response["post_title"] = post.title
                    response["post_id"] = post.id
                    response["post_creator"] = post.poster.format_for_response()
                    response["post_likes"] = post.likes
                    response["post_views"] = post.views
                    response["post_text"] = post.text
                    response["post_tags"] = post.tags
                    response["post_time"] = str(post_time)
                    response["post_is_liked"] = is_liked
                    response["post_is_edited"] = post.edited
                    response["post_replies"] = []
                    for reply, like_count, reply_time, is_liked in boardroomDB.get_post_replies(post.id, current_user):
                        reply.sender = userDB.get_user_by_id(reply.sender)
                        formatted_reply = {"reply_likes": like_count,
                                           "reply_text": reply.text,
                                           "reply_is_liked": is_liked,
                                           "reply_is_edited": reply.edited,
                                           "reply_id": reply.id,
                                           "reply_creator": reply.sender.format_for_response(),
                                           "reply_time": str(reply_time)}
                        response["post_replies"].append(formatted_reply)
                except ValueError:
                    response["success"] = False
                    response["message"] = "Post not found"

            elif message["action"] == 8:  # like post
                try:
                    boardroomDB.toggle_like(current_user, int(message["post_id"]))
                    response["success"] = True
                except ValueError:
                    response["success"] = False
                    response["message"] = "Post does not exist"

            elif message["action"] == 9:  # like post reply
                try:
                    boardroomDB.toggle_like(current_user, int(message["post_id"]), int(message["reply_id"]))
                    response["success"] = True
                except ValueError:
                    response["success"] = False
                    response["message"] = "Reply does not exist"

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

            elif message["action"] == 12:  # Modify Post
                try:
                    boardroomDB.modify_post(int(message["post_id"]), message["modifications"], current_user.id)
                    response["success"] = True
                except ValueError:
                    response["success"] = False
                    response["message"] = "Post does not exist"
                except KeyError:
                    response["success"] = False
                    response["message"] = "Current user does not have permission to modify this post"

            elif message["action"] == 13:  # Modify Post Reply
                try:
                    boardroomDB.modify_post_reply(int(message["post_id"]), int(message["reply_id"]), message["text"],
                                                  current_user.id)
                    response["success"] = True
                except ValueError:
                    response["success"] = False
                    response["message"] = "Reply does not exist"
                except KeyError:
                    response["success"] = False
                    response["message"] = "Current user does not have permission to modify this reply"

            elif message["action"] == 14:
                print("Refresh")

            elif message["action"] == 15:  # Reply Post
                try:
                    boardroomDB.write_post_reply(int(message["post_id"]), message["text"], current_user)
                    response["success"] = True
                except ValueError:
                    response["success"] = False
                    response["message"] = "Post does not exist"

            elif message["action"] == 16:  # Search Posts
                results = boardroomDB.search_posts(message["keywords"], message["tags"])
                response["success"] = True
                response["posts"] = []
                for vals in results:
                    formatted_post = {"post_title": vals[0], "post_text": vals[1],
                                  "post_creator": userDB.get_user_by_id(vals[2]).format_for_response(), "post_id": vals[3],
                                  "post_likes": vals[4], "post_views": vals[5], "post_time": vals[6],
                                  "post_replies": vals[7], "post_tags": vals[8]}
                    response["posts"].append(formatted_post)

            elif message["action"] == 17:  # Delete Post Reply
                try:
                    boardroomDB.delete_post_reply(int(message["post_id"]), int(message["reply_id"]), current_user.id)
                    response["success"] = True
                except ValueError:
                    response["success"] = False
                    response["message"] = "Reply does not exist"
                except KeyError:
                    response["success"] = False
                    response["message"] = "Current user does not have permission to delete this reply"

            elif message["action"] == 18:  # Delete Post
                try:
                    boardroomDB.delete_post(int(message["post_id"]), current_user.id)
                    response["success"] = True
                except ValueError:
                    response["success"] = False
                    response["message"] = "Post does not exist"
                except KeyError:
                    response["success"] = False
                    response["message"] = "Current user does not have permission to delete this post"

            elif message["action"] == 19:  # Send Message
                recipient = userDB.search("email", message["recipient"])
                if len(recipient) == 1:
                    messageDB.write_message(int(recipient.id.values[0]), message["text"], current_user.id)
                    participant = userDB.get_user_by_id(int(recipient.id.values[0]))
                    direct_messages = messageDB.get_messages(participant.id, current_user.id)

                    response["success"] = True
                    response["recipient"] = participant.format_for_response()
                    response["messages"] = []
                    for message, post_time in direct_messages:
                        response["messages"].append({"sender_message": message.sender == current_user.id,
                                                     "text": message.text, "message_is_edited": message.edited,
                                                     "id": message.id, "time": post_time})
                else:
                    response["success"] = False
                    response["message"] = "User does not exist"

            elif message["action"] == 20:  # Get Messages
                participant = userDB.search("id", message["participant_id"])
                if not pd.isna(participant.email):
                    participant = userDB.get_user_by_id(int(participant.id))
                    direct_messages = messageDB.get_messages(participant.id, current_user.id)

                    response["success"] = True
                    response["recipient"] = participant.format_for_response()
                    response["messages"] = []
                    for message, post_time in direct_messages:
                        response["messages"].append({"sender_message": message.sender == current_user.id,
                                                     "text": message.text, "message_is_edited": message.edited,
                                                     "id": message.id, "time": post_time})
                else:
                    response["success"] = False
                    response["message"] = "User does not exist"

            elif message["action"] == 21:  # Get Conversations
                response["success"] = True
                response["conversations"] = []
                for receiver_id, text, time in messageDB.get_conversations(current_user.id):
                    receiver = userDB.get_user_by_id(receiver_id)
                    response["conversations"].append(
                        {"recipient": receiver.format_for_response(), "last_message": text,
                         "last_message_time": time})

            await websocket.send(encoder.encode(response))

    except ws.ConnectionClosedOK:
        print("Client disconnected:", websocket.id)

    except ws.ConnectionClosedError:
        print("Client disconnected with error:", websocket.id)

    except ConnectionError:
        print("Client disconnected with error:", websocket.id)

async def main():
    # Swap "localhost" with server IP
    async with ws.serve(connection, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    print("Launching server...")
    asyncio.run(main())

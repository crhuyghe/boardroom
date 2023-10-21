import asyncio
import json
import websockets as ws
from websockets import server
from Classes.DatabaseReader import DatabaseReader

boardroomDB = DatabaseReader("boardroom")
userDB = DatabaseReader("user")
messageDB = DatabaseReader("message")

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

            if message["action"] == 1:
                print("AccessAccount")
            elif message["action"] == 2:  # Create Account
                response = {}
                try:
                    current_user = userDB.writeEntry(message["email"], message["name"], message["password"])
                    response["success"] = True
                except ValueError:
                    response["success"] = False
                    response["message"] = "AccountExistsError"
                finally:
                    await websocket.send(encoder.encode(response))
            elif message["action"] == 3:
                print("CreatePost")
            elif message["action"] == 4:
                print("DeleteAccount")
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

            print(message)
            await websocket.send(message)

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

import asyncio
import json
import websockets as ws
from websockets import server
# from Classes.DatabaseReader import DatabaseReader

# BoardroomDB = DatabaseReader("boardroom")
# UserDB = DatabaseReader("user")
# MessageDB = DatabaseReader("message")

decoder = json.JSONDecoder()

# In the current state, hosts a localhost websocket on port 8765.
# This connection accepts messages from the client and echoes them back.
async def connection(websocket: server.WebSocketServerProtocol):
    try:
        print("New Connection:", websocket.id)
        while True:
            message = decoder.decode(await websocket.recv())

            if message["action"] == 0:
                print("AccessAccount")
            elif message["action"] == 1:
                print("CreateAccount")
            elif message["action"] == 2:
                print("CreatePost")
            elif message["action"] == 3:
                print("DeleteAccount")
            elif message["action"] == 4:
                print("DeleteMessage")
            elif message["action"] == 5:
                print("EditMessage")
            elif message["action"] == 6:
                print("GetPost")
            elif message["action"] == 7:
                print("LikePost")
            elif message["action"] == 8:
                print("LikePostReply")
            elif message["action"] == 9:
                print("LogoutAccount")
            elif message["action"] == 10:
                print("ModifyAccount")
            elif message["action"] == 11:
                print("ModifyPost")
            elif message["action"] == 12:
                print("ModifyPostReply")
            elif message["action"] == 13:
                print("Refresh")
            elif message["action"] == 14:
                print("ReplyPost")
            elif message["action"] == 15:
                print("SearchPosts")
            elif message["action"] == 16:
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

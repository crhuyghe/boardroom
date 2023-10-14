import asyncio
import websockets as ws
from websockets import server
from Classes.DatabaseReader import DatabaseReader

BoardroomDB = DatabaseReader("boardroom")
UserDB = DatabaseReader("user")
MessageDB = DatabaseReader("message")

# In the current state, hosts a localhost websocket on port 8765.
# This connection accepts messages from the client and echoes them back.
async def connection(websocket: server.WebSocketServerProtocol):
    try:
        print("New Connection:", websocket.id)
        while True:
            message = await websocket.recv()

            if message == 0:
                print("AccessAccount")
            elif message == 1:
                print("CreateAccount")
            elif message == 2:
                print("CreatePost")
            elif message == 3:
                print("DeleteAccount")
            elif message == 4:
                print("DeleteMessage")
            elif message == 5:
                print("EditMessage")
            elif message == 6:
                print("GetPost")
            elif message == 7:
                print("LikePost")
            elif message == 8:
                print("LikePostReply")
            elif message == 9:
                print("LogoutAccount")
            elif message == 10:
                print("ModifyAccount")
            elif message == 11:
                print("ModifyPost")
            elif message == 12:
                print("ModifyPostReply")
            elif message == 13:
                print("Refresh")
            elif message == 14:
                print("ReplyPost")
            elif message == 15:
                print("SearchPosts")
            elif message == 16:
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

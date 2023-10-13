import asyncio
import websockets as ws
from websockets import server

async def connection(websocket: server.WebSocketServerProtocol):
    try:
        print("New Connection:", websocket.id)
        while True:
            message = await websocket.recv()
            print(message)
            await websocket.send(message)
    except ws.ConnectionClosedOK:
        print("Client disconnected")

async def main():
    async with ws.serve(connection, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())

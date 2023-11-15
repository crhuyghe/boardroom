import tkinter as tk
import asyncio
import json
import websockets as ws
from tkinter import ttk
from ttkthemes import ThemedTk
from websockets.exceptions import ConnectionClosedError

class AsyncGUI(ThemedTk):
    def __init__(self, main_loop: asyncio.AbstractEventLoop):
        super().__init__(theme="adapta")

        # These lines are necessary for running asyncio with tkinter
        self.loop = main_loop
        self.interval = 1 / 120
        self.protocol("WM_DELETE_WINDOW", self._close)
        self.tasks = set()
        self.tasks.add(self.loop.create_task(self._updater()))  # Window update loop
        connection = self.loop.create_task(self._connection_handler())  # Websocket Connection
        self.tasks.add(connection)
        connection.add_done_callback(self.tasks.discard)

        # DO NOT TOUCH THESE VARIABLES. Use the send_message function to send and receive messages.
        self._outgoing_message = None
        self._outgoing_message_flag = asyncio.Event()
        self._incoming_message = None
        self._incoming_message_flag = asyncio.Event()
        self._connected = asyncio.Event()  # Check for connection with line "self._connected.is_set()"

        # Set this equal to the user's login request if it is successful
        self.login = None
        self.logged_in = False

        # Add your GUI elements here
        self.title("Boardroom")
        self.frame = ttk.Frame()
        test_message = {"action": 1, "email": "cave.johnson@aperture.com", "password": "IH8Lemons"}
        self.test_button = ttk.Button(self.frame, text="Test Button",
                                      command=lambda: self.run_as_task(self.send_message, test_message))
        self.test_button.pack(side="top")

        self.frame.pack(fill="both", expand=1)


    def run_as_task(self, func, *args):
        print(func)

        task = self.loop.create_task(func(*args))
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)

    @staticmethod
    def is_successful(response):
        if type(response) == dict:
            return response["success"]
        else:
            return False

    async def send_message(self, message: dict) -> dict:
        message = json.JSONEncoder().encode(message)
        self._outgoing_message_flag.set()
        self._outgoing_message = message
        await self._incoming_message_flag.wait()
        self._incoming_message_flag.clear()

        return json.JSONDecoder().decode(self._incoming_message)

    async def _connection_handler(self, reconnecting=False):
        try:
            async with ws.connect("ws://localhost:8765") as websocket:
                self._connected.set()
                if self.login:
                    await websocket.send(self.login)
                    self.logged_in = self.is_successful(await websocket.recv())

                reconnecting = False
                while True:
                    await self._outgoing_message_flag.wait()
                    await websocket.send(self._outgoing_message)
                    self._outgoing_message_flag.clear()
                    self._outgoing_message = None
                    self._incoming_message = await websocket.recv()
                    self._incoming_message_flag.set()
        except ConnectionClosedError as e:
            self._connected.clear()
            print(type(e), "\nAttempting reconnection...")
            if not reconnecting:
                reconnect = self.loop.create_task(self._reconnect())
                self.tasks.add(reconnect)
                reconnect.add_done_callback(self.tasks.discard)

    async def _reconnect(self):
        task = None
        while not self._connected.is_set():
            task = self.loop.create_task(self._connection_handler(True))
            await asyncio.sleep(3)
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)

    async def _updater(self):
        """Updates the GUI"""
        while True:
            self.update()
            await asyncio.sleep(self.interval)

    def _close(self):
        """Allows the window to close properly"""
        for task in self.tasks:
            if task:
                task.cancel(msg=None)
        self.loop.stop()
        self.destroy()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = AsyncGUI(loop)
    loop.run_forever()
    loop.close()


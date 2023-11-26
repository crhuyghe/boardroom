import tkinter as tk
import asyncio
import json
import websockets as ws
from tkinter import ttk
from ttkthemes import ThemedTk
from websockets.exceptions import ConnectionClosedError

class AsyncGUI(ThemedTk):
    tasks = set()

    def __init__(self, main_loop: asyncio.AbstractEventLoop):
        super().__init__(theme="adapta")

        # These lines are necessary for running asyncio with tkinter
        self.loop = main_loop
        self.interval = 1 / 120
        self.protocol("WM_DELETE_WINDOW", lambda: self.run_as_task(self._close))
        self.run_as_task(self._updater)
        self.run_as_task(self._connection_handler)
        self._updater_closed = asyncio.Event()

        # DO NOT TOUCH THESE VARIABLES. Use the send_message function to send and receive messages.
        self._outgoing_message = None
        self._outgoing_message_flag = asyncio.Event()
        self._incoming_message = None
        self._incoming_message_flag = asyncio.Event()
        self._connected = asyncio.Event()  # Check for connection with line "self._connected.is_set()"
        self._closing = False
        self._connection_closed = asyncio.Event()

        # Set this equal to the user's login request if it is successful
        self.login = None
        self.logged_in = False

        # Add your GUI elements here
        self.title("Boardroom")
        ttk.Style().configure('.', font=('Segoe UI Symbol', 16))
        # self.frame = ttk.Frame()
        test_message = {"action": 1, "email": "cave.johnson@aperture.com", "password": "IH8Lemons"}
        # self.test_button = ttk.Button(self.frame, text="Test Button",
        #                               command=lambda: self.run_as_task(self.send_message, test_message))
        # self.test_button.pack(side="top")

        # self.frame.pack(fill="both", expand=1)

    def run_as_task(self, func, *args):
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
        print(self._incoming_message)

        return json.JSONDecoder().decode(self._incoming_message)

    async def _connection_handler(self, reconnecting=False):
        try:
            async with ws.connect("ws://localhost:8765") as websocket:
                self._connection_closed.clear()
                self.websocket = websocket
                self._connected.set()
                if self.login:
                    await websocket.send(self.login)
                    self.logged_in = self.is_successful(await websocket.recv())

                print("Connection successful")
                while not self._closing:
                    await self._outgoing_message_flag.wait()
                    if not self._closing:
                        await websocket.send(self._outgoing_message)
                        self._outgoing_message_flag.clear()
                        self._outgoing_message = None
                        self._incoming_message = await websocket.recv()
                        self._incoming_message_flag.set()
            self._connection_closed.set()
        except ConnectionClosedError:
            self._connected.clear()
            self._connection_closed.set()
            self.logged_in = False
            print("Connection error. attempting reconnection...")
            self.run_as_task(self._reconnect)
        except ConnectionRefusedError or asyncio.TimeoutError:
            print("Connection attempt failed. Retrying...")
            self._connection_closed.set()
            if not reconnecting:
                self.run_as_task(self._reconnect)

    async def _reconnect(self):
        task = None
        while not self._connected.is_set() and not self._closing:
            self._connection_closed.clear()
            task = self.loop.create_task(self._connection_handler(True))
            await asyncio.sleep(3)
            await self._connection_closed.wait()
        if task:
            self.tasks.add(task)
            task.add_done_callback(self.tasks.discard)

    async def _updater(self):
        """Updates the GUI"""
        while not self._closing:
            self.update()
            await asyncio.sleep(self.interval)
        self._updater_closed.set()

    async def _close(self):
        """Allows the window to close properly"""
        self._closing = True
        self._outgoing_message_flag.set()
        self._incoming_message = '{"success": false}'
        self._incoming_message_flag.set()
        await asyncio.wait_for(self._connection_closed.wait(), 4)
        await asyncio.wait_for(self._updater_closed.wait(), 3)
        for task in self.tasks:
            if task and "AsyncGUI._close" not in str(task.get_coro()):
                task.cancel(msg=None)
        self.loop.stop()
        self.destroy()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = AsyncGUI(loop)
    loop.run_forever()
    loop.close()


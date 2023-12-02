import tkinter as tk
import asyncio
import json
import websockets as ws
from tkinter import ttk
from websockets.exceptions import ConnectionClosedError

from Backend.Classes.Models.User import User
from Frontend.Classes.Components.DarkModeInterface import DarkMode
from Frontend.Classes.Screens.ConversationSidebarFrame import ConversationSidebarFrame
from Frontend.Classes.Screens.CreateAccountFrame import CreateAccountFrame
from Frontend.Classes.Screens.CreatePostFrame import CreatePostFrame
from Frontend.Classes.Screens.DirectMessagesFrame import DirectMessagesFrame
from Frontend.Classes.Screens.FullPostFrame import FullPostFrame
from Frontend.Classes.Screens.HeaderFrame import HeaderFrame
from Frontend.Classes.Screens.LoginFrame import LoginFrame
from Frontend.Classes.Screens.SearchResultsFrame import SearchResultsFrame
from Frontend.Classes.Screens.WelcomeFrame import WelcomeFrame

class AsyncGUI(tk.Tk, DarkMode):
    tasks = set()

    def __init__(self, main_loop: asyncio.AbstractEventLoop):
        tk.Tk.__init__(self)

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
        # self.user = None
        self.user = User(0, "cave.johnson@aperture.com", "Cave Johnson")

        # Add your GUI elements here
        self.title("Boardroom")
        ttk.Style().configure('.', font=('Segoe UI Symbol', 16))
        self.configure(background="#EEEEEE")
        self._dark_mode = False
        # self.swap_mode()
        # self.state('zoomed')
        # self.grid_rowconfigure(1, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        self.headerbar = None
        self.welcome_frame = None
        self.conversations_sidebar = None
        self.post_creation = None

        # self.run_as_task(self.launch_homepage)

    def swap_mode(self):
        self._dark_mode = not self._dark_mode
        if self._dark_mode:
            ttk.Style().configure('.', background="#24272b", foreground="#b6bfcc")
            self.configure(background="#24272b")
        else:
            ttk.Style().configure('.', background="#EEEEEE", foreground="#000000")
            self.configure(background="#EEEEEE")
        for widget in self.winfo_children():
            if isinstance(widget, DarkMode):
                widget.swap_mode()

    def clear_window(self, destroy=True, clear_header=False):
        if destroy:
            for widget in self.winfo_children():
                if type(widget) != HeaderFrame or clear_header:
                    widget.destroy()
        else:
            for widget in self.winfo_children():
                if type(widget) != HeaderFrame or clear_header:
                    widget.grid_forget()

    async def launch_homepage(self):
        self.clear_window()

        self.welcome_frame = WelcomeFrame(self, self.user, self.show_post_creation, self._dark_mode)
        self.conversations_sidebar = ConversationSidebarFrame(self, await self.get_conversations(),
                                                         lambda rid: self.run_as_task(self.show_direct_messages, rid),
                                                         lambda remail, txt: self.run_as_task(self, remail, txt),
                                                         self._dark_mode)

        if self.headerbar is None:
            self.headerbar = HeaderFrame(self, self.user, lambda: self.run_as_task(self.launch_homepage),
                                         lambda text, tags: self.run_as_task(self.search_posts, text, tags),
                                         lambda: self.run_as_task(self.logout),
                                         lambda: self.run_as_task(self.delete_account),
                                         self.swap_mode, self._dark_mode)
            self.headerbar.grid(row=0, column=0, columnspan=2, sticky="new")

        self.welcome_frame.grid(row=1, column=0, sticky="nsew")
        self.conversations_sidebar.grid(row=1, column=1, sticky="nsew")

    def show_post_creation(self):
        print("hi")
        self.welcome_frame.destroy()

        self.post_creation = CreatePostFrame(self,
                                             lambda title, text, tags: self.run_as_task(self.create_post, title, text,
                                                                                        tags), self._dark_mode)
        self.post_creation.grid(row=1, column=0, sticky="nsew")

    async def create_post(self, title, text, tags):
        pass

    async def get_conversations(self):
        from datetime import datetime, timedelta
        import pandas as pd
        time = datetime.strptime(str(pd.Timestamp.now()), '%Y-%m-%d %X.%f')
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        return {"success": True, "conversations": [
            {"recipient": {"name": "Caroline", "email": "caroline@aperture.com", "picture": False, "id": 2},
             "last_message": text, "last_message_time": format(time + timedelta(minutes=0))},
            {"recipient": {"name": "Bill Cipher", "email": "bcipher@gmail", "picture": False, "id": 3},
             "last_message": text, "last_message_time": format(time - timedelta(days=76))},
            {"recipient": {"name": "Chell", "email": "chell@aperture.com", "picture": False, "id": 4},
             "last_message": text, "last_message_time": format(time - timedelta(days=98))},
            {"recipient": {"name": "Wheatley", "email": "wheatley@aperture.com", "picture": False, "id": 5},
             "last_message": text, "last_message_time": format(time - timedelta(weeks=57))},
            {"recipient": {"name": "Batman", "email": "bwayne@gmail.com", "picture": False, "id": 6},
             "last_message": text, "last_message_time": format(time - timedelta(weeks=157))},
            {"recipient": {"name": "Steve Jobs", "email": "sjobs@apple.com", "picture": False, "id": 7},
             "last_message": text, "last_message_time": format(time - timedelta(weeks=257))},
        ]}

    async def show_direct_messages(self, rid):
        pass

    async def get_direct_messages(self):
        pass
        # from datetime import datetime, timedelta
        # import pandas as pd
        # time = datetime.strptime(str(pd.Timestamp.now()), '%Y-%m-%d %X.%f')
        # text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        # return {"success": True, "conversations": [
        #         {"recipient": {"name": "Caroline", "email": "caroline@aperture.com", "picture": False, "id": 2}, "last_message": text, "last_message_time": format(time+timedelta(minutes=0))},
        #         {"recipient": {"name": "Bill Cipher", "email": "bcipher@gmail", "picture": False, "id": 3}, "last_message": text, "last_message_time": format(time-timedelta(days=76))},
        #         {"recipient": {"name": "Chell", "email": "chell@aperture.com", "picture": False, "id": 4}, "last_message": text, "last_message_time": format(time-timedelta(days=98))},
        #         {"recipient": {"name": "Wheatley", "email": "wheatley@aperture.com", "picture": False, "id": 5}, "last_message": text, "last_message_time": format(time-timedelta(weeks=57))},
        #         {"recipient": {"name": "Batman", "email": "bwayne@gmail.com", "picture": False, "id": 6}, "last_message": text, "last_message_time": format(time-timedelta(weeks=157))},
        #         {"recipient": {"name": "Steve Jobs", "email": "sjobs@apple.com", "picture": False, "id": 7}, "last_message": text, "last_message_time": format(time-timedelta(weeks=257))},
        #         ]}

    async def send_user_message(self, recipient_id, text):
        pass

    async def edit_message(self, recipient_id, message_id, text):
        pass

    async def delete_message(self, recipient_id, message_id):
        pass

    async def search_posts(self, text, tags):
        pass

    async def logout(self):
        pass

    async def delete_account(self):
        pass

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

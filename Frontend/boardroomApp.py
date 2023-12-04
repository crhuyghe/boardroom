import contextlib
import tkinter as tk
import asyncio
import json
import websockets as ws
from collections import deque
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
        self.run_as_task(self._send_queue_handler)
        self._updater_closed = asyncio.Event()

        # DO NOT TOUCH THESE VARIABLES. Use the send_message function to send and receive messages.
        self._outgoing_message = None
        self._outgoing_message_flag = asyncio.Event()
        self._incoming_message = None
        self._incoming_message_flag = asyncio.Event()
        self._connected = asyncio.Event()  # Check for connection with line "self._connected.is_set()"
        self._closing = False
        self._connection_closed = asyncio.Event()
        self._send_queue = deque()
        self._send_queue_has_element = asyncio.Event()
        self._send_queue_closed = asyncio.Event()
        self._conv_update_closed = asyncio.Event()
        self._dm_update_closed = asyncio.Event()

        # Set this equal to the user's login request if it is successful
        self.login = None
        self.logged_in = False
        self.user = None

        # Add your GUI elements here
        self.title("Boardroom")
        ttk.Style().configure('.', font=('Segoe UI Symbol', 16))
        self.configure(background="#EEEEEE")
        self._dark_mode = False
        self.swap_mode()

        # Initialize all the GUI elements to None
        self.headerbar = None
        self.welcome_frame = None
        self.conversations_sidebar = None
        self.post_creation = None
        self.search_results_frame = None
        self.full_boardroom = None
        self.direct_message_window = None
        self.login_page = None
        self.create_account_page = None

        # Update cycle for direct messages and conversations
        self.run_as_task(self._conversation_update_handler)
        self.run_as_task(self._dm_update_handler)

        # Start the app on the login page
        self.run_as_task(self.show_login)

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
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        if destroy:
            for widget in self.winfo_children():
                if type(widget) != HeaderFrame or clear_header:
                    widget.destroy()
            if clear_header:
                self.headerbar = None
            self.welcome_frame = None
            self.conversations_sidebar = None
            self.post_creation = None
            self.search_results_frame = None
            self.full_boardroom = None
            self.direct_message_window = None
            self.login_page = None
            self.create_account_page = None
        else:
            for widget in self.winfo_children():
                if type(widget) != HeaderFrame or clear_header:
                    widget.grid_forget()

    async def launch_homepage(self):
        self.clear_window()
        self.welcome_frame = WelcomeFrame(self, self.user, self.show_post_creation, self._dark_mode)
        self.conversations_sidebar = ConversationSidebarFrame(self, await self.get_conversations(),
                                                         lambda rid: self.run_as_task(self.show_direct_messages, rid),
                                    lambda remail, txt: self.run_as_task(self.send_user_message, remail, txt, True),
                                                         self._dark_mode)
        if self.headerbar is None:
            self.headerbar = HeaderFrame(self, self.user, lambda: self.run_as_task(self.launch_homepage),
                                         lambda text, tags: self.run_as_task(self.show_search_results, text, tags),
                                         lambda: self.run_as_task(self.account_logout),
                                         lambda password: self.run_as_task(self.delete_account, password),
                                         self.swap_mode, dark_mode=self._dark_mode)
            self.headerbar.grid(row=0, column=0, columnspan=2, sticky="new")

        self.welcome_frame.grid(row=1, column=0, sticky="nsew")
        self.conversations_sidebar.grid(row=1, column=1, sticky="nsew")


    def show_post_creation(self):
        self.welcome_frame.destroy()

        self.post_creation = CreatePostFrame(self, lambda title, text, tags: self.run_as_task(self.create_post, title, text, tags), self._dark_mode)
        self.post_creation.grid(row=1, column=0, sticky="nsew")


    async def create_post(self, title, text, tags):
        message = {"action": 3, "title": title, "tags": tags, "text": text}

        response = await self.send_message(message)
        if response["success"]:
            self.clear_window()
            self.full_boardroom = FullPostFrame(self, response, self.user,
                                                lambda pid, rid=None: self.run_as_task(self.like_post_or_reply, pid,
                                                                                       rid),
                                                lambda txt, pid, rid=None: self.run_as_task(self.edit_post_or_reply,
                                                                                            txt, pid, rid),
                                                lambda pid, rid=None: self.run_as_task(self.delete_post_or_reply, pid,
                                                                                       rid),
                                                lambda pid, txt: self.run_as_task(self.reply_to_post, pid, txt),
                                                self._dark_mode)
            self.full_boardroom.grid(row=1, column=0, columnspan=2, sticky="nswe")

    async def get_conversations(self):
        message = {"action": 21}
        response = await self.send_message(message)

        if response["success"]:
            return response

    async def show_direct_messages(self, recipient_id):
        try:
            dms = await self.get_direct_messages(recipient_id)

            self.clear_window()
            self.direct_message_window = DirectMessagesFrame(self, dms, self.user,
                                            lambda rid, mid, txt: self.run_as_task(self.edit_message, rid, mid, txt),
                                            lambda rid, mid: self.run_as_task(self.delete_message, rid, mid),
                                                lambda rem, txt: self.run_as_task(self.send_user_message, rem, txt),
                                                             self._dark_mode)

            self.conversations_sidebar = ConversationSidebarFrame(self, await self.get_conversations(),
                                                                  lambda rid: self.run_as_task(
                                                                      self.show_direct_messages, rid),
                                    lambda remail, txt: self.run_as_task(self.send_user_message, remail, txt, True),
                                                                  self._dark_mode)
            self.conversations_sidebar.grid(row=1, column=0, sticky="nswe")
            self.direct_message_window.grid(row=1, column=1, sticky="nswe")
            self.grid_columnconfigure(0, weight=0)
            self.grid_columnconfigure(1, weight=1)
        except ValueError as e:
            print(e)
            await self.launch_homepage()

    async def get_direct_messages(self, recipient_id):
        message = {"action": 20, "participant_id": recipient_id}

        response = await self.send_message(message)
        if response["success"]:
            return response
        elif "does not exist" in response["message"]:
            raise ValueError

    async def send_user_message(self, recipient_email, text, new_conversation=False):
        message = {"action": 19, "recipient": recipient_email, "text": text}

        response = await self.send_message(message)
        if response["success"]:
            if new_conversation:
                if self.conversations_sidebar and self.conversations_sidebar.error_active:
                    self.conversations_sidebar.hide_error()
                await self.show_direct_messages(response["recipient"]["id"])
            else:
                if self.direct_message_window:
                    self.direct_message_window.append_message(response["messages"][-1])
                    if not response["messages"] == self.direct_message_window.messages:
                        self.direct_message_window.flush_messages(response)
                        await self.show_direct_messages(response["recipient"]["id"])
        elif "does not exist" in response["message"]:
            if new_conversation:
                if self.conversations_sidebar:
                    self.conversations_sidebar.show_error()
            else:
                await self.launch_homepage()

    async def edit_message(self, recipient_id, message_id, text):
        message = {"action": 6, "recipient": recipient_id, "message_id": message_id, "text": text}
        print(message)
        response = await self.send_message(message)
        if response["success"]:
            if self.direct_message_window:
                self.direct_message_window.edit_message_record(message_id, text)
        elif "does not exist" in response["message"]:
            await self.launch_homepage()
        elif "own messages" in response["message"]:
            print("Button misfire detected")

    async def delete_message(self, recipient_id, message_id):
        message = {"action": 5, "recipient": recipient_id, "message_id": message_id}

        response = await self.send_message(message)
        if response["success"]:
            if self.direct_message_window:
                self.direct_message_window.delete_message_widget(message_id)
        elif "does not exist" in response["message"]:
            await self.launch_homepage()
        elif "own messages" in response["message"]:
            print("Button misfire detected")

    async def show_search_results(self, keywords, tags):
        results = await self.search_posts(keywords, tags)

        self.clear_window()
        self.search_results_frame = SearchResultsFrame(self, results,
                                                       lambda pid: self.run_as_task(self.show_boardroom, pid),
                                                       self._dark_mode)
        self.search_results_frame.grid(row=1, column=0, columnspan=2, sticky="nswe")

    async def search_posts(self, keywords, tags):
        message = {"action": 16, "keywords": keywords, "tags": tags}

        response = await self.send_message(message)

        if response["success"]:
            return response

    async def show_boardroom(self, post_id):
        try:
            post = await self.get_post(post_id)
            self.clear_window()

            self.full_boardroom = FullPostFrame(self, post, self.user,
                                            lambda pid, rid=None: self.run_as_task(self.like_post_or_reply, pid, rid),
                                lambda txt, pid, rid=None: self.run_as_task(self.edit_post_or_reply,txt, pid, rid),
                                        lambda pid, rid=None: self.run_as_task(self.delete_post_or_reply, pid, rid),
                                                lambda pid, txt: self.run_as_task(self.reply_to_post, pid, txt),
                                                self._dark_mode)
            self.full_boardroom.grid(row=1, column=0, columnspan=2, sticky="nswe")
        except ValueError:
            await self.launch_homepage()

    async def get_post(self, post_id):
        message = {"action": 7, "post_id": post_id}

        response = await self.send_message(message)
        if response["success"]:
            return response
        elif response["message"] == "Post not found":
            raise ValueError

    async def edit_post_or_reply(self, text, post_id, reply_id):
        if reply_id is not None:
            message = {"action": 13, "post_id": post_id, "reply_id": reply_id, "text": text}
        else:
            message = {"action": 12, "post_id": post_id, "modifications": {"text": text, "tags": False}}

        response = await self.send_message(message)
        if response["success"]:
            await self.show_boardroom(post_id)
        elif "does not exist" in response["message"]:
            print(response["message"])

    async def delete_post_or_reply(self, post_id, reply_id=None):
        if reply_id is not None:
            message = {"action": 17, "post_id": post_id, "reply_id": reply_id}
        else:
            message = {"action": 18, "post_id": post_id}

        response = await self.send_message(message)
        if response["success"]:
            if reply_id:
                await self.show_boardroom(post_id)
            else:
                await self.launch_homepage()
        elif "does not exist" in response["message"]:
            print(response["message"])

    async def reply_to_post(self, post_id, text):
        message = {"action": 15, "post_id": post_id, "text": text}

        response = await self.send_message(message)
        if response["success"]:
            await self.show_boardroom(post_id)
        elif "post does not exist" in response["message"]:
            print(response["message"])
            await self.launch_homepage()

    async def like_post_or_reply(self, post_id, reply_id=None):
        if reply_id is not None:
            message = {"action": 9, "post_id": post_id, "reply_id": reply_id}
        else:
            message = {"action": 8, "post_id": post_id}

        response = await self.send_message(message)
        if response["success"]:
            return response
        elif "does not exist" in response["message"]:
            print(response["message"])

    async def show_login(self):
        self.clear_window(clear_header=True)
        self.state("normal")
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.login_page = LoginFrame(self, lambda email, password: self.run_as_task(self.account_login, email, password),
                                     lambda: self.run_as_task(self.show_create_account))
        self.login_page.grid(row=0, column=0, sticky="nswe")

    async def show_create_account(self):
        self.clear_window(clear_header=True)
        self.state("normal")
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.create_account_page = CreateAccountFrame(self, lambda: self.run_as_task(self.show_login),
                            lambda email, name, password: self.run_as_task(self.create_account, email, name, password))
        self.create_account_page.grid(row=0, column=0, sticky="nswe")

    async def account_login(self, email, password):
        message = {"action": 1, "email": email, "password": password}

        response = await self.send_message(message)
        if response["success"]:
            self.user = User(response["id"], response["email"], response["name"])
            self.login = message
            self.logged_in = True
            await self.launch_homepage()
            self.state("zoomed")
        elif response["lockout"]:
            if self.login_page:
                self.login_page.show_warning_label("This account is locked out until tomorrow")
        else:
            if self.login_page:
                self.login_page.show_warning_label("Incorrect email or password")

    async def account_logout(self):
        message = {"action": 10}

        response = await self.send_message(message)
        if response["success"]:
            self.login = None
            self.user = None
            self.logged_in = False
            await self.show_login()

    async def create_account(self, email, name, password):
        message = {"action": 2, "email": email, "name": name, "password": password}

        response = await self.send_message(message)
        if response["success"]:
            self.user = User(response["id"], response["email"], response["name"])
            self.login = {"action": 1, "email": email, "password": password}
            self.logged_in = True
            await self.launch_homepage()
            self.state("zoomed")
        elif "exists" in response["message"]:
            self.create_account_page.show_warning_label("An account with this email already exists")

    async def delete_account(self, password):
        message = {"action": 4, "password": password}

        response = await self.send_message(message)
        if response["success"]:
            self.login = None
            self.user = None
            self.logged_in = False
            await self.show_login()
        elif response["lockout"]:
            await self.account_logout()
        else:
            self.headerbar.show_error()


    async def modify_account(self, email, password, name):
        pass  # Possibly replace welcome frame with modify account frame?

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
        flags = (asyncio.Event(), asyncio.Event())
        self._send_queue.append(flags)
        if not self._send_queue_has_element.is_set():
            self._send_queue_has_element.set()
        print(message)
        message = json.JSONEncoder().encode(message)


        await flags[0].wait()

        self._outgoing_message_flag.set()
        self._outgoing_message = message
        await self._incoming_message_flag.wait()
        self._incoming_message_flag.clear()

        flags[1].set()
        print(self._incoming_message)

        return json.JSONDecoder().decode(self._incoming_message)

    async def _send_queue_handler(self):
        while not self._closing or len(self._send_queue) != 0:
            if len(self._send_queue) == 0:
                self._send_queue_has_element.clear()
            await self._send_queue_has_element.wait()
            if len(self._send_queue) != 0:
                active_send = self._send_queue.popleft()
                active_send[0].set()
                await active_send[1].wait()
            else:
                self._send_queue_closed.set()
        self._send_queue_closed.set()

    async def _conversation_update_handler(self):
        while not self._closing:
            if self.conversations_sidebar:
                await asyncio.sleep(3)
                try:
                    conversations = (await self.get_conversations())

                    if self.conversations_sidebar and conversations["conversations"] != self.conversations_sidebar.conversations:
                        self.conversations_sidebar.flush_conversations(conversations)
                except AttributeError:
                    continue
            else:
                await asyncio.sleep(1)
        self._conv_update_closed.set()


    async def _dm_update_handler(self):
        while not self._closing:
            if self.direct_message_window:
                await asyncio.sleep(2)
                try:
                    response = (await self.get_direct_messages(self.direct_message_window.recipient.id))

                    if self.direct_message_window and len(response["messages"]) > len(self.direct_message_window.messages):
                        for new_message in response["messages"][len(self.direct_message_window.messages):]:
                            self.direct_message_window.append_message(new_message)
                    if self.direct_message_window and response["messages"] != self.direct_message_window.messages:
                        self.direct_message_window.flush_messages(response)
                except ValueError:
                    await self.launch_homepage()
                except AttributeError:
                    continue
            else:
                await asyncio.sleep(1)
        self._dm_update_closed.set()

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
        self._send_queue_has_element.set()
        try:
            await asyncio.wait_for(self._send_queue_closed.wait(), 3)
            await asyncio.wait_for(self._connection_closed.wait(), 4)
            await asyncio.wait_for(self._updater_closed.wait(), 3)
        except asyncio.TimeoutError as e:
            print(e)
        for task in self.tasks:
            with contextlib.suppress(asyncio.CancelledError):
                if task and "AsyncGUI._close" not in str(task.get_coro()):
                    task.cancel(msg=None)
        self.loop.stop()
        self.destroy()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = AsyncGUI(loop)
    loop.run_forever()
    loop.close()

import asyncio
import pathlib
import websockets
import tkinter as tk
from tkinter import *
from ttkthemes import ThemedTk
import os

localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")

# This function doesn't work
async def connection():
    uri = "wss://localhost:8765"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f">>> {name}")


class App(ThemedTk):

    def __init__(self):
        super().__init__(theme="adapta")

        # Create window
        self.title("Boardroom")
        self.geometry('600x400')


def main():
    # asyncio.run(connection()) This doesn't work
    app = App()
    app.mainloop()


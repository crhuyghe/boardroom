import tkinter as tk
import json
from tkinter import ttk, StringVar
from ttkthemes import ThemedTk

from Classes.Errors import IncorrectPasswordError, AccountLockoutError
from Classes.DatabaseManagers.UserDatabaseManager import UserDatabaseManager
from Classes.DatabaseManagers.BoardroomDatabaseManager import BoardroomDatabaseManager
from Classes.DatabaseManagers.MessageDatabaseManager import MessageDatabaseManager

class App(ThemedTk):

    def __init__(self):
        super().__init__(theme="adapta")

        self.title("Boardroom Test App")

        self.actions = {1: ["cave.johnson@aperture.com", "IH8Lemons"], 2: ["", "", ""], 3: ["", "", ""], 4: [""],
                        5: ["", ""], 6: ["", "", ""], 7: [""], 8: [""], 9: ["", ""], 10: [], 11: ["", "", "", "", ""],
                        12: ["", "", ""], 13: ["", "", ""], 14: [], 15: ["", ""], 16: ["", ""], 17: ["", ""], 18: [""],
                        19: ["", ""]}
        self.string_vars = [StringVar(value=""), StringVar(value=""), StringVar(value=""), StringVar(value=""),
                            StringVar(value="")]
        self.text_fields = []

        self.current_user = None
        self.current_action = 1
        self.frame = ttk.Frame(self, padding=25)

        self.argument_frame = ttk.Frame(self.frame)
        self.simulate_button = ttk.Button(self.frame, text="Simulate Send", padding=5,
                                          command=lambda: self.run_action())

        self.user_label_text = StringVar()
        self.user_label_text.set("No User Logged In")
        self.user_label = ttk.Label(self.frame, textvariable=self.user_label_text)

        self.response_label_text = StringVar()
        self.response_label = ttk.Label(self.frame, textvariable=self.response_label_text)

        self.mode_menu = tk.Menu(self.frame)
        self.mode_dropdown = ttk.Menubutton(self.frame, name="command menu", text="Choose a command",
                                            menu=self.mode_menu)

        self.mode_menu.add_command(label="Access Account", command=lambda: self.update_text_fields(1))
        self.mode_menu.add_command(label="Create Account", command=lambda: self.update_text_fields(2))
        self.mode_menu.add_command(label="Create Post", command=lambda: self.update_text_fields(3))
        self.mode_menu.add_command(label="Delete Account", command=lambda: self.update_text_fields(4))
        self.mode_menu.add_command(label="Delete Message", command=lambda: self.update_text_fields(5))
        self.mode_menu.add_command(label="Edit Message", command=lambda: self.update_text_fields(6))
        self.mode_menu.add_command(label="Get Post", command=lambda: self.update_text_fields(7))
        self.mode_menu.add_command(label="Like Post", command=lambda: self.update_text_fields(8))
        self.mode_menu.add_command(label="Like Post Reply", command=lambda: self.update_text_fields(9))
        self.mode_menu.add_command(label="Logout Account", command=lambda: self.update_text_fields(10))
        self.mode_menu.add_command(label="Modify Account", command=lambda: self.update_text_fields(11))
        self.mode_menu.add_command(label="Modify Post", command=lambda: self.update_text_fields(12))
        self.mode_menu.add_command(label="Modify Post Reply", command=lambda: self.update_text_fields(13))
        self.mode_menu.add_command(label="Refresh", command=lambda: self.update_text_fields(14))
        self.mode_menu.add_command(label="Reply Post", command=lambda: self.update_text_fields(15))
        self.mode_menu.add_command(label="Search Posts", command=lambda: self.update_text_fields(16))
        self.mode_menu.add_command(label="Delete Post Reply", command=lambda: self.update_text_fields(17))
        self.mode_menu.add_command(label="Delete Post", command=lambda: self.update_text_fields(18))
        self.mode_menu.add_command(label="Send Message", command=lambda: self.update_text_fields(19))

        self.user_label.pack(side="top")
        self.mode_dropdown.pack(side="top")
        self.response_label.pack(side="bottom")
        self.simulate_button.pack(side="bottom")
        self.argument_frame.pack(side="bottom")

        self.frame.pack(fill="both", expand=1)
        self.update_text_fields(action=1)

    def run_action(self):
        message = self.map_action_message()
        response = {}

        boardroomDB = BoardroomDatabaseManager()
        userDB = UserDatabaseManager()
        messageDB = MessageDatabaseManager()

        encoder = json.JSONEncoder()

        current_user = self.current_user

        if message["action"] == 1:  # Access Account
            try:
                current_user = userDB.login_account(message["email"], message["password"])
                response["success"] = True
            except KeyError:
                response["success"] = False
                response["message"] = "Incorrect email or password"
                response["account_found"] = False
                response["lockout"] = False
            except IncorrectPasswordError:
                response["success"] = False
                response["message"] = "Incorrect email or password"
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
            except ValueError:
                response["success"] = False
                response["message"] = "AccountExistsError"

        elif message["action"] == 3:  # Create Post
            boardroomDB.write_post(message["title"], message["tags"], message["text"], current_user)
            response["success"] = True

        elif message["action"] == 4:  # Delete Account
            try:
                userDB.delete_account(current_user.id, message["password"])
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

        self.current_user = current_user
        if self.current_user:
            self.user_label_text.set(self.current_user.name)
        else:
            self.user_label_text.set("No User Logged In")

        self.response_label_text.set(encoder.encode(response))



    def map_action_message(self):
        for i in range(len(self.actions[self.current_action])):
            self.actions[self.current_action][i] = self.string_vars[i].get()
        message = {"action": self.current_action}

        if self.current_action == 1:
            message["email"] = self.string_vars[0].get()
            message["password"] = self.__encrypt(self.string_vars[1].get())
        elif self.current_action == 2:
            message["email"] = self.string_vars[0].get()
            message["name"] = self.string_vars[1].get()
            message["password"] = self.__encrypt(self.string_vars[2].get())
        elif self.current_action == 3:
            message["title"] = self.string_vars[0].get()
            message["tags"] = self.extract_tags(self.string_vars[1].get())
            message["text"] = self.string_vars[2].get()
        elif self.current_action == 4:
            message["password"] = self.__encrypt(self.string_vars[0].get())
        elif self.current_action == 5:
            message["recipient"] = self.string_vars[0].get()
            message["message_id"] = self.string_vars[1].get()
        elif self.current_action == 6:
            message["recipient"] = self.string_vars[0].get()
            message["message_id"] = self.string_vars[1].get()
            message["text"] = self.string_vars[2].get()
        elif self.current_action == 7:
            message["post_id"] = self.string_vars[0].get()
        elif self.current_action == 8:
            message["post_id"] = self.string_vars[0].get()
        elif self.current_action == 9:
            message["post_id"] = self.string_vars[0].get()
            message["reply_id"] = self.string_vars[1].get()
        elif self.current_action == 11:
            message["current_password"] = self.string_vars[0].get()
            if self.string_vars[1].get() == "":
                picture = False
            else:
                picture = self.string_vars[1].get()
            if self.string_vars[2].get() == "":
                email = False
            else:
                email = self.string_vars[2].get()
            if self.string_vars[3].get() == "":
                password = False
            else:
                password = self.__encrypt(self.string_vars[3].get())
            if self.string_vars[4].get() == "":
                name = False
            else:
                name = self.string_vars[4].get()

            message["modifications"] = {"picture": picture, "email": email, "password": password, "name": name}
        elif self.current_action == 12:
            message["post_id"] = self.string_vars[0].get()

            if self.string_vars[1].get() == "":
                text = False
            else:
                text = self.string_vars[1].get()
            if self.string_vars[2].get() == "":
                tags = False
            else:
                tags = self.extract_tags(self.string_vars[2].get())

            message["modifications"] = {"text": text, "tags": tags}
        elif self.current_action == 13:
            message["post_id"] = self.string_vars[0].get()
            message["reply_id"] = self.string_vars[1].get()
            message["text"] = self.string_vars[2].get()
        elif self.current_action == 15:
            message["post_id"] = self.string_vars[0].get()
            message["text"] = self.string_vars[1].get()
        elif self.current_action == 16:
            message["keywords"] = self.string_vars[0].get()
            message["tags"] = self.extract_tags(self.string_vars[1].get())
        elif self.current_action == 17:
            message["post_id"] = self.string_vars[0].get()
            message["reply_id"] = self.string_vars[1].get()
        elif self.current_action == 18:
            message["post_id"] = self.string_vars[0].get()
        elif self.current_action == 19:
            message["recipient"] = self.string_vars[0].get()
            message["text"] = self.string_vars[1].get()

        return message

    @staticmethod
    def extract_tags(tag_string: str):
        tags = tag_string.split(" ")
        return tags

    def update_text_fields(self, action):
        self.current_action = action

        for label, box in self.text_fields:
            label.destroy()
            box.destroy()
        self.text_fields = []

        for var in self.string_vars:
            var.set("")

        if action == 1:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Email"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Password"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[1])))
        elif action == 2:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Email"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Name"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[1])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Password"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[2])))
        elif action == 3:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Title"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Tags"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[1])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Text"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[2])))
        elif action == 4:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Password"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
        elif action == 5:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Recipient"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Message ID"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[1])))
        elif action == 6:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Recipient"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Message ID"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[1])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Text"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[2])))
        elif action == 7:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Post ID"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
        elif action == 8:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Post ID"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
        elif action == 9:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Post ID"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Reply ID"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[1])))
        elif action == 11:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Current Password"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Picture"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[1])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Email"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[2])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Password"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[3])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Name"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[4])))
        elif action == 12:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Post ID"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Text"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[1])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Tags"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[2])))
        elif action == 13:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Post ID"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Reply ID"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[1])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Text"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[2])))
        elif action == 15:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Post ID"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Text"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[1])))
        elif action == 16:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Keywords"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Tags"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[1])))
        elif action == 17:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Post ID"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Reply ID"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[1])))
        elif action == 18:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Post ID"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
        elif action == 19:
            self.text_fields.append((ttk.Label(self.argument_frame, text="Recipient"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[0])))
            self.text_fields.append((ttk.Label(self.argument_frame, text="Text"),
                                     ttk.Entry(self.argument_frame, textvariable=self.string_vars[1])))

        for i in range(len(self.text_fields)):
            self.text_fields[i][0].grid(row=i, column=0, sticky='E')
            self.text_fields[i][1].grid(row=i, column=1, sticky='W')

        for i in range(len(self.actions[action])):
            self.string_vars[i].set(str(self.actions[action][i]))

    @staticmethod
    def __encrypt(password: str) -> str:
        return password


if __name__ == '__main__':
    app = App()
    app.mainloop()
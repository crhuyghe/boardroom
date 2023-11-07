import pandas as pd

# Class for direct messages and possibly for boardroom replies
class Message:
    id = -1
    sender = None
    destination = None
    text = ""
    edited = False

    def __init__(self, message_id: int, sender, destination, text, edited: bool):
        self.id = int(message_id)
        self.sender = sender
        self.destination = destination
        self.text = text
        self.edited = bool(edited)

    def format_for_reply_dataframe(self, time_created=None):
        if time_created is None:
            time_created = pd.Timestamp.now()
        return {"reply_id": self.id, "post_id": self.destination, "poster_id": self.sender.id, "text": self.text,
                "post_time": time_created, "is_edited": self.edited}

    def format_for_message_dataframe(self, time_created=None):
        if time_created is None:
            time_created = pd.Timestamp.now()
        if self.sender > self.destination:
            return {"sender_id": self.sender, "receiver_id": self.destination, "id": self.id, "text": self.text,
                    "post_time": time_created, "is_edited": self.edited}

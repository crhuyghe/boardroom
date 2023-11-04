import pandas as pd

# Discussion board
class Boardroom:
    def __init__(self, post_id: int, poster, title: str, tags: list, text: str, views: int, likes: int, edited: bool):
        self.id = int(post_id)
        self.poster = poster
        self.title = title
        self.tags = tags
        self.text = text
        self.views = int(views)
        self.likes = int(likes)
        self.edited = bool(edited)

    def format_for_dataframe(self, time_created=None):
        if time_created is None:
            time_created = pd.Timestamp.now()
        return {"id": self.id, "title": self.title, "poster_id": self.poster.id, "text": self.text,
                "like_count": self.likes, "view_count": self.views, "post_time": time_created,
                "is_edited": self.edited}


from .database import RUNNING_DB


class AppEngine:
    def __init__(self):
        self.db_instance = RUNNING_DB


import sqlite3
import os

from Logger import *

class DatabaseManager:
    def __init__(self, db_path="bausteine.db"):
        if os.path.exists(db_path):
            self.db_path = db_path
            self.db_connection = sqlite3.connect(db_path)
        else:
            log(f"Database file {db_path} does not exist.", LogLevel.ERROR)
            log("Failed to connect to the database.", LogLevel.NOTIFICATION)
            self.db_connection = None
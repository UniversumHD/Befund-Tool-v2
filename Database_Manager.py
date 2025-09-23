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

    def execute_query(self, query, params=()):
        if self.db_connection:
            cursor = self.db_connection.cursor()
            try:
                cursor.execute(query, params)
                self.db_connection.commit()
                return cursor.fetchall()
            except sqlite3.Error as e:
                log(f"Database query error: {e}", LogLevel.ERROR)
                return None
        else:
            log("No database connection available.", LogLevel.ERROR)
            return None
        
    def close_connection(self):
        if self.db_connection:
            self.db_connection.close()
            log("Database connection closed.", LogLevel.INFO)
    
    def __del__(self):
        self.close_connection()
            
    def get_available_kuerzel(self):
        query = "SELECT kuerzel FROM bausteine"
        results = self.execute_query(query)
        if results is not None:
            return [row[0] for row in results]
        return []
    
    def append_to_history(self, name, geburtsdatum, befund):
        query = "INSERT INTO befundverlauf (name, geburtsdatum, befund) VALUES (?, ?, ?)"
        self.execute_query(query, (name, geburtsdatum, befund))
        log(f"Appended to history: {name}, {geburtsdatum}, {befund}", LogLevel.INFO)
        
    def get_history(self, limit=10):
        query = """ SELECT id, name
                        FROM befundverlauf
                        WHERE id IN (
                            SELECT MAX(id)
                            FROM befundverlauf
                            GROUP BY name
                        )
                        ORDER BY id DESC LIMIT ?;
                        """
        results = self.execute_query(query, (limit,))
        if results is not None:
            return results
        return []
    
    def get_history_entry(self, id):
        query = "SELECT name, geburtsdatum, befund FROM befundverlauf WHERE id = ?"
        results = self.execute_query(query, (id,))
        if results:
            return results[0]
        return None
    
    def get_bausteine(self):
        query = "SELECT * FROM bausteine"
        results = self.execute_query(query)
        if results is not None:
            return results
        return []
    
    def get_kategorien(self):
        query = "SELECT * FROM kategorien"
        results = self.execute_query(query)
        if results is not None:
            return results
        return []
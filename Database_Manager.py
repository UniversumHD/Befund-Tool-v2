import sqlite3
import os
import sys
from Logger import *

class DatabaseManager:
    def __init__(self, db_path="bausteine.db"):
        if os.path.exists(db_path):
            self.db_path = db_path
            self.db_connection = sqlite3.connect(db_path)
        else:
            log(f"Database file {db_path} does not exist.", LogLevel.WARNING)
            self.create_database(self.get_resource_path("schema.sql"), db_path)
            self.db_path = db_path
            self.db_connection = sqlite3.connect(db_path)
            
    def create_database(self, schema_path, db_path="bausteine.db"):
        try:
            with open(schema_path, 'r') as f:
                schema = f.read()
            self.db_connection = sqlite3.connect(db_path)
            cursor = self.db_connection.cursor()
            cursor.executescript(schema)
            self.db_connection.commit()
            log(f"Database created at {db_path} using schema {schema_path}", LogLevel.INFO)
        except Exception as e:
            log(f"Failed to create database: {e}", LogLevel.ERROR)
            log("Fehler beim Erstellen der Datenbank. Siehe Log für Details.", LogLevel.NOTIFICATION)
    
    def get_resource_path(self, relative_path):
        """Gibt den absoluten Pfad zur Ressource zurück, funktioniert für dev und PyInstaller."""
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller: Ressource ist im temporären Verzeichnis
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            # Entwicklungsumgebung: Ressource ist im aktuellen Verzeichnis
            return os.path.abspath(relative_path)

        
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
        query = "SELECT * FROM bausteine ORDER BY kuerzel"
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
    
    def update_baustein(self, baustein_id, kuerzel, text, kategorie_id):
        query = "UPDATE bausteine SET kuerzel = ?, text = ?, kategorie = ? WHERE id = ?"
        self.execute_query(query, (kuerzel, text, kategorie_id, baustein_id))
        log(f"Updated baustein ID {baustein_id}: {kuerzel}", LogLevel.NOTIFICATION)
        
    def add_baustein(self, kuerzel, text, kategorie_name):
        # Get or create category
        query = "SELECT id FROM kategorien WHERE name = ?"
        results = self.execute_query(query, (kategorie_name,))
        if results:
            kategorie_id = results[0][0]
        else:
            log(f"Category '{kategorie_name}' not found.", LogLevel.NOTIFICATION)
            return
        
        # Insert baustein
        insert_baustein_query = "INSERT INTO bausteine (kuerzel, text, kategorie) VALUES (?, ?, ?)"
        self.execute_query(insert_baustein_query, (kuerzel, text, kategorie_id))
        log(f"Added new Baustein: {kuerzel}", LogLevel.NOTIFICATION)
        
    def kategorie_to_id(self, kategorie_name):
        query = "SELECT id FROM kategorien WHERE name = ?"
        results = self.execute_query(query, (kategorie_name,))
        if results:
            return results[0][0]
        return 0
    
    def delete_baustein(self, baustein_id):
        query = "DELETE FROM bausteine WHERE id = ?"
        self.execute_query(query, (baustein_id,))
        log(f"Deleted baustein ID {baustein_id}", LogLevel.NOTIFICATION)
        
    def create_backup(self, backup_path):
        try:
            if self.db_connection:
                self.db_connection.commit()  # Ensure all changes are saved
                self.db_connection.close()   # Close the connection to avoid locks
            import shutil
            shutil.copyfile(self.db_path, backup_path + f"/bausteine_backup.db")
            log(f"Database backup created at {backup_path}", LogLevel.NOTIFICATION)
            # Reopen the connection
            self.db_connection = sqlite3.connect(self.db_path)
        except Exception as e:
            log(f"Failed to create database backup: {e}", LogLevel.ERROR)
            log("Fehler beim Erstellen des Backups. Siehe Log für Details.", LogLevel.NOTIFICATION)
            
    
    def add_kategorie(self, name):
        query = "INSERT INTO kategorien (name) VALUES (?)"
        self.execute_query(query, (name,))
        log(f"Added new Kategorie: {name}", LogLevel.NOTIFICATION)
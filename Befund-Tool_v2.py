import sys, os

from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget

from MainWindow import MainWindow
from EditorTab import EditorTab
from Logger import *
from Database_Manager import DatabaseManager
from Baustein_Table_Tab import BausteinTableTab

def main():
    
    db_path = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Befund-Tool", "bausteine.db")
    
    db_manager = DatabaseManager(db_path)
    db_connection = db_manager.db_connection
    if db_connection is None:
        log("Exiting application due to database connection failure.", LogLevel.ERROR)
        sys.exit(1)
    
    app = QApplication(sys.argv)
    window = MainWindow(db_manager)
    setup_ui(window, db_manager)
    
    set_log_level(LogLevel.DEBUG)
    log("Application started", LogLevel.INFO)
    
    window.show()
    sys.exit(app.exec_())
    
    

def setup_ui(window, db_manager):
    editor_tab = EditorTab(db_manager)
    baustein_tabelle_tab = BausteinTableTab(db_manager)
    
    editor_widget = QWidget()
    editor_widget.setLayout(editor_tab)
    baustein_tabelle_widget = QWidget()
    baustein_tabelle_widget.setLayout(baustein_tabelle_tab)
    
    tabs = QTabWidget()
    tabs.addTab(editor_widget, "Editor")
    tabs.addTab(baustein_tabelle_widget, "Bausteine verwalten")
    
    window.setCentralWidget(tabs)
    return window



if __name__ == "__main__":
    main()
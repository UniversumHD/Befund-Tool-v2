import sys, os

from PyQt5.QtWidgets import QApplication, QWidget

from MainWindow import MainWindow
from EditorTab import EditorTab
from Logger import *
from Database_Manager import DatabaseManager

def main():
    app = QApplication(sys.argv)
    window = MainWindow(sys.argv)
    
    db_path = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Befund-Tool", "bausteine.db")
    
    db_manager = DatabaseManager(db_path)
    db_connection = db_manager.db_connection
    if db_connection is None:
        log("Exiting application due to database connection failure.", LogLevel.ERROR)
        sys.exit(1)
    
    setup_ui(window)
    
    set_log_level(LogLevel.DEBUG)
    log("Application started", LogLevel.INFO)
    
    window.show()
    sys.exit(app.exec_())
    
    

def setup_ui(window):
    editor_tab = EditorTab()
    
    widget = QWidget()
    widget.setLayout(editor_tab)
    window.setCentralWidget(widget)
    return window



if __name__ == "__main__":
    main()
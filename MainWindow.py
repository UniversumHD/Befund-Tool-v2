from PyQt5.QtWidgets import QMainWindow, QApplication, QAction
from Logger import *


class MainWindow(QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.configure_menu_bar()
        self.setWindowTitle("Befund-Tool v2.2.3")
        self.setGeometry(100, 100, 800, 600)
        
        
    def configure_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Datei")
        
        backup_action = QAction("Backup erstellen", self)
        backup_action.triggered.connect(self.create_backup)

        file_menu.addAction(backup_action)
        
    def create_backup(self):
        dir = self.choose_directory()
        self.db_manager.create_backup(dir)
        pass
    
    def choose_directory(self):
        from PyQt5.QtWidgets import QFileDialog
        if hasattr(self, 'prev_path'):
            directory = QFileDialog.getExistingDirectory(self.parent(), "Verzeichnis auswählen", self.prev_path)
        else:
            directory = QFileDialog.getExistingDirectory(self.parent(), "Verzeichnis auswählen")
            self.prev_path = directory
        return directory
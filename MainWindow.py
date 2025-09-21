from PyQt5.QtWidgets import QMainWindow, QApplication

class MainWindow(QMainWindow):
    def __init__(self, db_connection):
        super().__init__()
        self.setWindowTitle("Befund-Tool v2")
        self.setGeometry(100, 100, 800, 600)
        
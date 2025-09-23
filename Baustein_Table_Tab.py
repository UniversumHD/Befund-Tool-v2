from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QDialog, QLabel, QLineEdit, QTextEdit
)
from Logger import *

class BausteinTableTab(QVBoxLayout):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Kürzel", "Text", "Kategorie"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.cellClicked.connect(self.on_cell_clicked)

        self.add_button = QPushButton("Baustein hinzufügen")
        self.add_button.clicked.connect(self.add_baustein)

        self.edit_button = QPushButton("Baustein bearbeiten")
        self.edit_button.clicked.connect(self.edit_baustein)
        self.edit_button.setEnabled(False)

        self.delete_button = QPushButton("Baustein löschen")
        self.delete_button.clicked.connect(self.delete_baustein)
        self.delete_button.setEnabled(False)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        self.addWidget(self.table)
        self.addLayout(button_layout)

        self.load_bausteine()

    def load_bausteine(self):
        bausteine = self.db_manager.get_bausteine()
        kategorien = self.db_manager.get_kategorien()
        self.table.setRowCount(0)
        for baustein in bausteine:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(baustein[3]))
            self.table.setItem(row_position, 1, QTableWidgetItem(baustein[2]))
            self.table.setItem(row_position, 2, QTableWidgetItem(kategorien[baustein[1]][1]))

    def on_cell_clicked(self, row, column):
        if row >= 0:
            self.edit_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        else:
            self.edit_button.setEnabled(False)
            self.delete_button.setEnabled(False)
    def add_baustein(self):
        log("Not implemented yet", LogLevel.WARNING)
        log("Not implemented yet", LogLevel.NOTIFICATION)
        pass
    def edit_baustein(self):
        log("Not implemented yet", LogLevel.WARNING)
        log("Not implemented yet", LogLevel.NOTIFICATION)
        pass
    def delete_baustein(self):
        log("Not implemented yet", LogLevel.WARNING)
        log("Not implemented yet", LogLevel.NOTIFICATION)
        pass
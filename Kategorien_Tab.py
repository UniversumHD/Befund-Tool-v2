from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QDialog, QLabel, QLineEdit, QTextEdit
)
from Logger import *
from Input_Dialog import InputDialog
from Confirm_Dialog import ConfirmDialog

class KategorienTab(QVBoxLayout):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Name"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.cellClicked.connect(self.on_cell_clicked)

        self.add_button = QPushButton("Kategorie hinzufügen")
        self.add_button.clicked.connect(self.add_kategorie)

        self.edit_button = QPushButton("Kategorie bearbeiten")
        self.edit_button.clicked.connect(self.edit_kategorie)
        self.edit_button.setEnabled(False)

        self.delete_button = QPushButton("Kategorie löschen")
        self.delete_button.clicked.connect(self.delete_kategorie)
        self.delete_button.setEnabled(False)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        self.addWidget(self.table)
        self.addLayout(button_layout)

        self.load_bausteine()

    def load_bausteine(self):
        kategorien = self.db_manager.get_kategorien()
        log(f"{kategorien}")
        self.table.setRowCount(0)
        for kat in kategorien:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            log(f"Loading kategorie: {kat}", LogLevel.DEBUG)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(kat[0])))
            self.table.setItem(row_position, 1, QTableWidgetItem(kat[1]))
        # for baustein in bausteine:
        #     row_position = self.table.rowCount()
        #     self.table.insertRow(row_position)
        #     log(f"Loading baustein: {baustein}", LogLevel.DEBUG)
        #     self.table.setItem(row_position, 0, QTableWidgetItem(str(baustein[0])))
        #     self.table.setItem(row_position, 1, QTableWidgetItem(baustein[3]))
        #     self.table.setItem(row_position, 2, QTableWidgetItem(baustein[2]))
        #     self.table.setItem(row_position, 3, QTableWidgetItem(kategorien[baustein[1]][1]))

    def on_cell_clicked(self, row, column):
        if row >= 0:
            self.edit_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        else:
            self.edit_button.setEnabled(False)
            self.delete_button.setEnabled(False)

            
            
    def add_kategorie(self):
        log("Not yet implemented: add_kategorie", LogLevel.NOTIFICATION)
        
    def edit_kategorie(self):
        log("Not yet implemented: edit_kategorie", LogLevel.NOTIFICATION)
        
    def delete_kategorie(self):
        log("Not yet implemented: delete_kategorie", LogLevel.NOTIFICATION)
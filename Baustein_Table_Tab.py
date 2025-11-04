from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QDialog, QLabel, QLineEdit, QTextEdit
)
from Logger import *
from Input_Dialog import InputDialog
from Confirm_Dialog import ConfirmDialog

class BausteinTableTab(QVBoxLayout):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Kürzel", "Text", "Kategorie"])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.cellClicked.connect(self.on_cell_clicked)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

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
        log(f"{kategorien}")
        self.table.setRowCount(0)
        for baustein in bausteine:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            log(f"Loading baustein: {baustein}", LogLevel.DEBUG)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(baustein[0])))
            self.table.setItem(row_position, 1, QTableWidgetItem(baustein[3]))
            self.table.setItem(row_position, 2, QTableWidgetItem(baustein[2]))
            self.table.setItem(row_position, 3, QTableWidgetItem(kategorien[baustein[1]][1]))

    def on_cell_clicked(self, row, column):
        if row >= 0:
            self.edit_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        else:
            self.edit_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            
    def get_contents_from_row(self, row):
        if row < 0 or row >= self.table.rowCount():
            return None
        kuerzel = self.table.item(row, 1).text()
        text = self.table.item(row, 2).text()
        kategorie = self.table.item(row, 3).text()
        id = self.table.item(row, 0).text()
        return (id, kuerzel, text, kategorie)
            
    def add_baustein(self, values = None):
        self.dialog = InputDialog("Baustein hinzufügen", ["ID:", "Kürzel:", "Text:", "Kategorie:"], values)
        if self.dialog.exec_() == QDialog.Accepted:
            kuerzel = self.db_manager.get_available_kuerzel()
            if self.dialog.inputs[0].text() in kuerzel:
                log("Kürzel bereits vorhanden!", LogLevel.NOTIFICATION)
                self.add_baustein(self.dialog.get_inputs())
                return
            inputs = self.dialog.get_inputs()[1:]  # Skip ID field
            log(f"User inputs: {inputs}", LogLevel.DEBUG)
            self.db_manager.add_baustein(inputs[0], inputs[1], inputs[2])
        
            self.load_bausteine()
            
    def edit_baustein(self):
        row = self.table.currentRow()
        if row < 0 or row >= self.table.rowCount():
            log("No row selected for editing", LogLevel.WARNING)
            log("Please select a row to edit.", LogLevel.NOTIFICATION)
            return
        current_values = self.get_contents_from_row(row)
        if current_values is None:
            log("Failed to retrieve current values for editing", LogLevel.ERROR)
            return
        self.dialog = InputDialog("Baustein bearbeiten", ["ID:", "Kürzel:", "Text:", "Kategorie:"], current_values)
        if self.dialog.exec_() == QDialog.Accepted:
            inputs = self.dialog.get_inputs()
            kuerzels = self.db_manager.get_available_kuerzel()
            log(f"User inputs for editing: {inputs}", LogLevel.DEBUG)
            baustein_id = int(inputs[0])
            kuerzel = inputs[1]
            text = inputs[2]
            kategorie = inputs[3]
            kategorie = self.db_manager.kategorie_to_id(kategorie)
            
            self.db_manager.update_baustein(baustein_id, kuerzel, text, kategorie)
            self.load_bausteine()
        
    def delete_baustein(self):
        row = self.table.currentRow()
        if row < 0 or row >= self.table.rowCount():
            log("No row selected for deletion", LogLevel.WARNING)
            log("Please select a row to delete.", LogLevel.NOTIFICATION)
            return
        id = int(self.table.item(row, 0).text())
        self.dialog = ConfirmDialog("Baustein löschen", f"Sind Sie sicher, dass Sie den Baustein mit ID {id} löschen möchten?")
        if self.dialog.exec_() == QDialog.Accepted:
            self.db_manager.delete_baustein(id)
            self.load_bausteine()
        
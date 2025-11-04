from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QDialog, QLabel, QLineEdit, QTextEdit
)
from Logger import *
from Kategorie_Input_Dialog import KategoieInputDialog
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

        self.load_kategorie()

    def load_kategorie(self):
        kategorien = self.db_manager.get_kategorien()
        log(f"{kategorien}")
        self.table.setRowCount(0)
        for kat in kategorien:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            log(f"Loading kategorie: {kat}", LogLevel.DEBUG)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(kat[0])))
            self.table.setItem(row_position, 1, QTableWidgetItem(kat[1]))


    def on_cell_clicked(self, row, column):
        if row >= 0:
            self.edit_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        else:
            self.edit_button.setEnabled(False)
            self.delete_button.setEnabled(False)

            
            
    def add_kategorie(self):
        dialog = KategoieInputDialog("Kategorie hinzufügen", ["ID:", "Name:"])
        if dialog.exec_() == QDialog.Accepted:
            inputs = dialog.get_inputs()
            self.db_manager.add_kategorie(inputs[1])
            self.load_kategorie()
        
        
    def edit_kategorie(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            return
        
        kat_id = self.table.item(selected_row, 0).text()
        kat_name = self.table.item(selected_row, 1).text()
        
        dialog = KategoieInputDialog("Kategorie bearbeiten", ["ID:", "Name:"], [kat_id, kat_name])
        if dialog.exec_() == QDialog.Accepted:
            inputs = dialog.get_inputs()
            # Update the category in the database
            query = "UPDATE kategorien SET name = ? WHERE id = ?"
            self.db_manager.execute_query(query, (inputs[1], inputs[0]))
            log(f"Updated Kategorie ID {inputs[0]} to Name: {inputs[1]}", LogLevel.NOTIFICATION)
            self.load_kategorie()
        
        
    def delete_kategorie(self):
        selected_row = self.table.currentRow()
        if selected_row <= 0:
            return
        
        kat_id = self.table.item(selected_row, 0).text()
        kat_name = self.table.item(selected_row, 1).text()
        
        confirm_dialog = ConfirmDialog("Kategorie löschen", f"Sind Sie sicher, dass Sie die Kategorie '{kat_name}' löschen möchten? \nDie Bausteine, die dieser Kategorie zugeordnet sind, werden nicht gelöscht, aber ihre Kategorie wird auf 'Unkategorisiert' gesetzt.")
        if confirm_dialog.exec_() == QDialog.Accepted:
            query = "DELETE FROM kategorien WHERE id = ?"
            self.db_manager.execute_query(query, (kat_id,))
            log(f"Deleted Kategorie ID {kat_id}", LogLevel.NOTIFICATION)
            self.recategorize_bausteine(kat_id, 0)  # Assuming 0 is the ID for 'Unkategorisiert'
            self.load_kategorie()
            
    def recategorize_bausteine(self, old_kat_id, new_kat_id):
        query = "UPDATE bausteine SET kategorie = ? WHERE kategorie = ?"
        self.db_manager.execute_query(query, (new_kat_id, old_kat_id))
        log(f"Re-categorized bausteine from Kategorie ID {old_kat_id} to {new_kat_id}", LogLevel.NOTIFICATION)
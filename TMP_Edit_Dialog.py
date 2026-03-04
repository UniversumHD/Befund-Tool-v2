from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QDialog, QLabel, QLineEdit, QTextEdit, QComboBox
)

class TmpEditDialog(QDialog):
    def __init__(self, title, label, default_value=None):
        super().__init__()
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        self.input = None
        
        # Text
        text_layout = QHBoxLayout()
        text_layout.addWidget(QLabel(label))
        text = QTextEdit()
        text.setPlainText(default_value)
        text_layout.addWidget(text)
        self.input = text
        self.layout.addLayout(text_layout)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Abbrechen")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def get_input(self):
        return self.input.toPlainText()
    

# Example usage:
# dialog = InputDialog("Baustein bearbeiten", ["Kürzel:", "Text:", "Kategorie:"], ["KZ1", "Beispieltext", "Kategorie1"])
# if dialog.exec_() == QDialog.Accepted:
#     inputs = dialog.get_inputs()
#     print(inputs)
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QDialog, QLabel, QLineEdit, QTextEdit
)

class KategoieInputDialog(QDialog):
    def __init__(self, title, labels, default_values=None):
        super().__init__()
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        
        if default_values is None:
            default_values = [""] * len(labels)

        hlayout_id = QHBoxLayout()
        hlayout_id.addWidget(QLabel(labels[0]))
        self.id_label = QLabel()
        self.id_label.setText(default_values[0])
        hlayout_id.addWidget(self.id_label)
        self.layout.addLayout(hlayout_id)
        
        hlayout_name = QHBoxLayout()
        hlayout_name.addWidget(QLabel(labels[1]))
        self.name_input = QLineEdit()
        self.name_input.setText(default_values[1])
        hlayout_name.addWidget(self.name_input)
        self.layout.addLayout(hlayout_name)
        

        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Abbrechen")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def get_inputs(self):
        return [self.id_label.text(), self.name_input.text()]
    

# Example usage:
# dialog = InputDialog("Baustein bearbeiten", ["Kürzel:", "Text:", "Kategorie:"], ["KZ1", "Beispieltext", "Kategorie1"])
# if dialog.exec_() == QDialog.Accepted:
#     inputs = dialog.get_inputs()
#     print(inputs)
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QDialog, QLabel, QLineEdit, QTextEdit
)

class InputDialog(QDialog):
    def __init__(self, title, labels, default_values=None):
        super().__init__()
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()

        self.inputs = []
        for i, label in enumerate(labels):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel(label))
            if i == 0:
                line_edit = QLabel()  # Read-only label for ID
                if default_values and i < len(default_values):
                    line_edit.setText(default_values[i])
            elif i == 2:
                line_edit = QTextEdit()
                if default_values and i < len(default_values):
                    line_edit.setPlainText(default_values[i])
            else:
                line_edit = QLineEdit()
                if default_values and i < len(default_values):
                    line_edit.setText(default_values[i])
            hlayout.addWidget(line_edit)
            self.inputs.append(line_edit)
            self.layout.addLayout(hlayout)

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
        inputs = []
        for i, input_widget in enumerate(self.inputs):
            if i == 0:
                inputs.append(input_widget.text())  # ID from QLabel
            elif i == 2:
                inputs.append(input_widget.toPlainText())  # Text from QTextEdit
            else:
                inputs.append(input_widget.text())  # Text from QLineEdit
        return inputs

# Example usage:
# dialog = InputDialog("Baustein bearbeiten", ["Kürzel:", "Text:", "Kategorie:"], ["KZ1", "Beispieltext", "Kategorie1"])
# if dialog.exec_() == QDialog.Accepted:
#     inputs = dialog.get_inputs()
#     print(inputs)
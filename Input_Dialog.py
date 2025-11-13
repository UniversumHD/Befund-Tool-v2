from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QDialog, QLabel, QLineEdit, QTextEdit, QComboBox
)

class InputDialog(QDialog):
    def __init__(self, title, labels, categories, default_values=None):
        super().__init__()
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        self.inputs = []
        
        
        # ID
        id_layout = QHBoxLayout()
        id_layout.addWidget(QLabel(labels[0]))
        id = QLabel()  # Read-only label for ID
        if default_values and 0 < len(default_values):
            id.setText(default_values[0])
        id_layout.addWidget(id)
        self.inputs.append(id)
        self.layout.addLayout(id_layout)

        # Kürzel
        kuerzel_layout = QHBoxLayout()
        kuerzel_layout.addWidget(QLabel(labels[1]))
        kuerzel = QLineEdit()
        if default_values and 1 < len(default_values):
            kuerzel.setText(default_values[1])
        kuerzel_layout.addWidget(kuerzel)
        self.inputs.append(kuerzel)
        self.layout.addLayout(kuerzel_layout)

        # Text
        text_layout = QHBoxLayout()
        text_layout.addWidget(QLabel(labels[2]))
        text = QTextEdit()
        if default_values and 2 < len(default_values):
            text.setPlainText(default_values[2])
        text_layout.addWidget(text)
        self.inputs.append(text)
        self.layout.addLayout(text_layout)

        # Category
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel(labels[3]))
        category = QComboBox()
        
        # Populate the QComboBox with items from getKategorien()

        category.addItems(categories)
        
        # Set the selected item based on default_values[3]
        if default_values and 3 < len(default_values):
            if default_values[3] in categories:
                category.setCurrentText(default_values[3])
        
        category_layout.addWidget(category)
        self.inputs.append(category)
        self.layout.addLayout(category_layout)


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
                inputs.append(input_widget.currentText() if isinstance(input_widget, QComboBox) else input_widget.text())
        return inputs
    

# Example usage:
# dialog = InputDialog("Baustein bearbeiten", ["Kürzel:", "Text:", "Kategorie:"], ["KZ1", "Beispieltext", "Kategorie1"])
# if dialog.exec_() == QDialog.Accepted:
#     inputs = dialog.get_inputs()
#     print(inputs)
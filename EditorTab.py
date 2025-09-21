from PyQt5.QtWidgets import (QVBoxLayout, QLineEdit, QComboBox, QPlainTextEdit, 
                             QPushButton, QLabel, QHBoxLayout)
from BefundEditor import BefundEditor

from Logger import *

class EditorTab(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
        
    def setup_ui(self):
        self.namensfeld = QLineEdit()
        self.namensfeld.setPlaceholderText("Name Patient")

        self.dropdown = QComboBox()
        self.dropdown.setToolTip("Wählen Sie einen Patienten aus dem Verlauf")
        self.dropdown.currentIndexChanged.connect(self.placeholder)

        self.geburtstagsfeld = QLineEdit()
        self.geburtstagsfeld.setPlaceholderText("Geburtsdatum")

        self.current_suggestion = ""
        self.befundfeld = BefundEditor(self.current_suggestion)
        self.befundfeld.setPlaceholderText("Befunde (Kürzel mit Komma getrennt)")
        self.befundfeld.resize(200, 200)  # Größe des dritten Textfeldes anpassen
        self.befundfeld.textChanged.connect(self.placeholder)

        self.suchzeile_layout = QHBoxLayout()

        self.kuerzelfeld = QLineEdit()
        self.kuerzelfeld.setPlaceholderText("Kürzel")
        self.kuerzelfeld.textChanged.connect(self.placeholder)

        self.uebernehmen_button = QPushButton("Übernehmen")
        self.uebernehmen_button.setToolTip("Übernimmt den aktuellen Baustein")
        self.uebernehmen_button.clicked.connect(self.placeholder)
        self.uebernehmen_button.setDisabled(True)

        self.befundfeld_neu = QPlainTextEdit()
        self.befundfeld_neu.setPlaceholderText("Befund neu")
        self.befundfeld_neu.resize(200, 200)  # Größe des neuen Textfeldes anpassen

        self.vorschlagfeld = QLabel()
        self.vorschlagfeld.setText("Vorschläge: ")
        self.vorschlagfeld.setWordWrap(True)

        self.erstellen_button = QPushButton("Erstellen")
        self.erstellen_button.setToolTip("Erstellt einen neuen Befund")
        self.erstellen_button.clicked.connect(self.placeholder)

        self.clear_button = QPushButton("Felder leeren")
        self.clear_button.setToolTip("Leert die Eingabefelder")
        self.clear_button.clicked.connect(self.placeholder)
        
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.namensfeld)
        top_layout.addWidget(self.geburtstagsfeld)

        topleft_layout = QVBoxLayout()
        topleft_layout.addWidget(self.dropdown) 
        topleft_layout.addLayout(top_layout)
        topleft_layout.addWidget(self.befundfeld)
        topleft_layout.addWidget(self.vorschlagfeld)
        topleft_layout.addWidget(self.erstellen_button)
        topleft_layout.addWidget(self.clear_button)

        self.addLayout(topleft_layout)

    def placeholder(self):
        log("Placeholder function called", LogLevel.DEBUG)
        pass
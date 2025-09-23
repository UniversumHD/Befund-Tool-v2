from PyQt5.QtWidgets import (QVBoxLayout, QLineEdit, QComboBox, QPlainTextEdit, QPushButton, QLabel, QHBoxLayout)
from BefundEditor import BefundEditor

from Logger import *

class EditorTab(QVBoxLayout):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        
        
    def setup_ui(self):
        self.namensfeld = QLineEdit()
        self.namensfeld.setPlaceholderText("Name Patient")

        self.dropdown = QComboBox()
        self.dropdown.setToolTip("Wählen Sie einen Patienten aus dem Verlauf")
        self.fill_dropdown()

        self.geburtstagsfeld = QLineEdit()
        self.geburtstagsfeld.setPlaceholderText("Geburtsdatum")

        self.current_suggestion = ""
        self.befundfeld = BefundEditor(self.current_suggestion)
        self.befundfeld.setPlaceholderText("Befunde (Kürzel mit Komma getrennt)")
        self.befundfeld.resize(200, 200)  # Größe des dritten Textfeldes anpassen

        self.vorschlagfeld = QLabel()
        self.vorschlagfeld.setText("Gib was ein um Vorschläge zu sehen")
        self.vorschlagfeld.setWordWrap(True)

        self.erstellen_button = QPushButton("Erstellen")
        self.erstellen_button.setToolTip("Erstellt einen neuen Befund")

        self.clear_button = QPushButton("Felder leeren")
        self.clear_button.setToolTip("Leert die Eingabefelder")
        
        self.dropdown.currentIndexChanged.connect(self.on_dropdown_changed)
        self.befundfeld.textChanged.connect(self.on_text_changed)
        self.erstellen_button.clicked.connect(self.create_befund)
        self.clear_button.clicked.connect(self.clear_fields)
        
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
    
    def create_befund(self):
        available_kuerzel = self.db_manager.get_available_kuerzel()
        # log(f"Available Kürzel: {available_kuerzel}", LogLevel.DEBUG)
        
        text = self.befundfeld.toPlainText()
        kuerzel_list = [k.strip() for k in text.split(",") if k.strip()]
        
        # log(str(kuerzel_list), LogLevel.DEBUG)
        
        if not kuerzel_list:
            log("Bitte gültige Kürzel eingeben", LogLevel.NOTIFICATION)
            return
        
        for kuerzel in kuerzel_list:
            if kuerzel not in available_kuerzel:
                log(f"Kürzel '{kuerzel}' not found in database.", LogLevel.WARNING)
                log(f"'{kuerzel}' ist kein gültiges Kürzel", LogLevel.NOTIFICATION)
                return
        
        name = self.namensfeld.text().strip()
        geburtsdatum = self.geburtstagsfeld.text().strip()
        
        if not name or not geburtsdatum:
            log("Name und Geburtsdatum müssen ausgefüllt sein", LogLevel.NOTIFICATION)
            return
        
        self.db_manager.append_to_history(name, geburtsdatum, text)
        self.fill_dropdown()
        self.namensfeld.clear()
        self.geburtstagsfeld.clear()
        self.befundfeld.clear()
        
        log(f"Das Erstellen Feature is not fully implemented yet.", LogLevel.WARNING)
        log(f"Das Erstellen Feature is not fully implemented yet.", LogLevel.NOTIFICATION)
        
    def fill_dropdown(self):
        history = self.db_manager.get_history()
        self.dropdown.clear()
        self.dropdown.addItem("---", 0)  # Default item
        for entry in history:
            self.dropdown.addItem(entry[1], entry[0])  # Display name, store id
    
    def on_dropdown_changed(self, index):
        if index == -1:
            return
        id = self.dropdown.itemData(index)
        if id == 0:
            self.clear_fields()
            return
        log(f"Selected index from dropdown: {index}", LogLevel.DEBUG)
        log(f"Selected ID from dropdown: {id}", LogLevel.DEBUG)
        entry = self.db_manager.get_history_entry(id)
        log(str(entry), LogLevel.DEBUG)
        self.namensfeld.setText(entry[0])
        self.geburtstagsfeld.setText(entry[1])
        self.befundfeld.setPlainText(entry[2])
        log(f"Loaded history of Patient {entry[0]}", LogLevel.INFO)
        
    def clear_fields(self):
        self.namensfeld.clear()
        self.geburtstagsfeld.clear()
        self.befundfeld.clear()
        log("Cleared input fields", LogLevel.INFO)
        
    def on_text_changed(self):
        text = self.befundfeld.toPlainText().lower()
        if not text:
            self.current_suggestion = ""
            self.befundfeld.set_current_suggestion(self.current_suggestion)
            self.vorschlagfeld.setText("Gib was ein um Vorschläge zu sehen")
            return
        kuerzel_list = [k.strip() for k in text.split(",") if k.strip()]
        available_kuerzel = self.db_manager.get_available_kuerzel()
        suggestions = []
        for kuerzel in available_kuerzel:
            if kuerzel.lower().startswith(kuerzel_list[-1]) and kuerzel not in kuerzel_list:
                suggestions.append(kuerzel)
        suggestions = suggestions[:9]  # nur die ersten 5 Vorschläge nehmen
        suggestion = ", ".join(suggestions)
        self.current_suggestion = suggestion
        self.befundfeld.set_current_suggestion(self.current_suggestion)
        self.vorschlagfeld.setText(f"{self.current_suggestion}")
        
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtCore, QtWidgets

from Logger import *

class BefundEditor(QPlainTextEdit):

    def __init__(self, current_suggestions):
        super().__init__()
        self.current_suggestions = current_suggestions

    def set_current_suggestions(self, suggestions):
        self.current_suggestions = suggestions

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            event.ignore()
            return
        # Filter out Shift+Number keys
        if event.text() and event.text() in "!\"§$%&/()":
            # get index of the number pressed
            index = "!\"§$%&/()".index(event.text())
            log(f"Index of suggestion to insert: {index+1}", LogLevel.DEBUG)
            
            self.insert_suggestion(index)  # Convert to 0-based index
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.insert_suggestion(0)  # Insert the first suggestion
        else:
            super().keyPressEvent(event)
            
    def insert_suggestion(self, index):
        if 0 <= index < len(self.current_suggestions):
            suggestion = self.current_suggestions[index]
            cursor = self.textCursor()
            text = self.toPlainText()
            last_comma = text.rfind(',')
            if last_comma == -1:
                new_text = suggestion + ", "
            else:
                new_text = text[:last_comma + 1] + " " + suggestion + ", "
            self.setPlainText(new_text)
            cursor.setPosition(len(new_text))
            self.setTextCursor(cursor)
            log(f"Inserted suggestion: {suggestion}", LogLevel.INFO)
        else:
            log(f"Invalid suggestion index: {index}", LogLevel.WARNING)
        
        #trigger text changed event
        self.textChanged.emit()
        
        
    def get_currently_marked_kuerzel(self):
        ## return the kuerzel that the cursor is currently on
        cursor = self.textCursor()
        text = self.toPlainText()
        pos = cursor.position()
        
        kuerzel = text.split(", ")
        length = 0
        for k in kuerzel:
            k = k.strip()
            length += len(k)
            if length >= pos:
                return k
            length += 2 # for the comma and space
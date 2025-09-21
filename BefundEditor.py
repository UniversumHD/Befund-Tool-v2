from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor

class BefundEditor(QPlainTextEdit):

    def __init__(self, current_suggestion):
        super().__init__()
        self.current_suggestion = current_suggestion

    def set_current_suggestion(self, suggestion):
        self.current_suggestion = suggestion

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Aktuelles Wort austauschen
            suggestion = self.current_suggestion
            cursor = self.textCursor()
            cursor.select(QTextCursor.WordUnderCursor)
            current_word = cursor.selectedText()
            if len(current_word) == 0:
                return
            
            cursor.removeSelectedText()
                
            
            cursor.insertText(suggestion + ", ")

        else:
            super().keyPressEvent(event)  # alle anderen Tasten norma
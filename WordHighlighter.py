from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegularExpression, QRegExp

class WordHighlighter(QSyntaxHighlighter):
    def __init__(self, parent, green_words):
        super().__init__(parent)
        self.green_words = green_words

        # Format für grüne Wörter
        self.greenFormat = QTextCharFormat()
        self.greenFormat.setForeground(QColor("green"))

        # Format für rote Wörter (alles andere)
        self.redFormat = QTextCharFormat()
        self.redFormat.setForeground(QColor("red"))

        # Format für schwarze Kommas
        self.commaFormat = QTextCharFormat()
        self.commaFormat.setForeground(QColor("black"))

        #print(green_words)

    def highlightBlock(self, text):
        # alles standardmäßig rot
        self.setFormat(0, len(text), self.redFormat)

        # Kommas schwarz färben
        comma_pattern = QRegExp(",")
        index = comma_pattern.indexIn(text)
        while index >= 0:
            self.setFormat(index, 1, self.commaFormat)
            index = comma_pattern.indexIn(text, index + 1)
        
        # grüne Wörter
        for word in self.green_words:

            pattern = QRegExp(QRegExp.escape(word))

            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, self.greenFormat)
                index = pattern.indexIn(text, index + length)

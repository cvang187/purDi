from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt, QStringListModel
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QPlainTextEdit, QCompleter

from gui.modules import util


class PurDiPromptCompleter(QCompleter):
    """
    Custom QCompleter for QPromptSuggestion. Takes a list() and converts it
    into a QStringListModel.
    """

    insertText = QtCore.Signal(str)

    def __init__(self, prompt_list: list, parent=None):
        QCompleter.__init__(self, prompt_list, parent)
        self.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setWrapAround(False)

        self.model = QStringListModel(prompt_list, self)
        self.setModel(self.model)

        self.highlighted.connect(self.set_highlighted)
        self.last_selected = None

    def set_highlighted(self, text):
        self.last_selected = text

    def get_selected(self):
        return self.last_selected


class PurDiPromptSuggestion(QPlainTextEdit):
    """Text autocompletion class that is inherited by the QTabWidget prompt field.
    Takes a words.txt file split by line and processes it for the QCompleter
    and allows prompt suggestion in real time
    """

    def __init__(self, parent=None):
        super(PurDiPromptSuggestion, self).__init__(parent)
        self.prompt_list = []
        self.num_char_before_word_suggestion = 1
        word_list = util.working_directory("../../configs/prompts/words.txt")

        try:
            with open(word_list, "r") as file:
                for line in file:
                    line = line.strip("\n")
                    self.prompt_list.append(line)
        except FileNotFoundError:
            print(f"{word_list} is invalid or words.txt does not exist")

        self.completer = PurDiPromptCompleter(prompt_list=self.prompt_list)
        self.completer.setWidget(self)
        self.completer.insertText.connect(self.insert_completion)

    def insert_completion(self, completion):
        text_cursor = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        text_cursor.movePosition(QTextCursor.Left)
        text_cursor.movePosition(QTextCursor.EndOfWord)
        text_cursor.insertText(completion[-extra:])
        self.setTextCursor(text_cursor)
        self.completer.popup().hide()

    def focusInEvent(self, event: QtGui.QFocusEvent) -> None:
        if self.completer:
            self.completer.setWidget(self)
        QPlainTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Text auto complete is handled by Tab key and fires when more than
        self.num_char_before_prompt_suggestion which is by default 2.
        :param event:
        :return:
        """
        text_cursor = self.textCursor()
        if event.key() == Qt.Key_Tab and self.completer.popup().isVisible():
            self.completer.insertText.emit(self.completer.get_selected())
            self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
            return

        QPlainTextEdit.keyPressEvent(self, event)
        text_cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        cursor_rect = self.cursorRect()

        if len(text_cursor.selectedText()) > self.num_char_before_word_suggestion:
            self.completer.setCompletionPrefix(text_cursor.selectedText())
            popup = self.completer.popup()
            popup.setCurrentIndex(self.completer.completionModel().index(0, 0))

            cursor_rect.setWidth(
                self.completer.popup().sizeHintForColumn(0)
                + self.completer.popup().verticalScrollBar().sizeHint().width()
                + 50
            )
            self.completer.complete(cursor_rect)
        else:
            self.completer.popup().hide()

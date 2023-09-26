import sys

from PyQt6.QtWidgets import QApplication

from src.bloc_note import BlocNoteWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BlocNoteWindow()
    window.show()
    sys.exit(app.exec())

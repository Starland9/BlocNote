from PyQt6.QtWidgets import QMainWindow, QMessageBox, QFileDialog

from ui import main_window


class BlocNoteWindow(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.current_file = None
        self.old_content = None
        self.current_content = None

        self.connect_all_actions()

    def connect_menu_actions(self):
        self.actionNouveau.triggered.connect(self.new_file)
        self.actionOuvrir.triggered.connect(self.open_file)
        self.actionEnregistrer.triggered.connect(self.save_file)
        self.actionEnregistrer_sous.triggered.connect(self.save_file_as)
        self.actionQuitter.triggered.connect(self.exit)

        self.actionCopier.triggered.connect(self.textEdit.copy)
        self.actionColler.triggered.connect(self.textEdit.paste)
        self.actionRetour.triggered.connect(self.textEdit.undo)
        self.actionAvancer.triggered.connect(self.textEdit.redo)
        self.actionCouper.triggered.connect(self.textEdit.cut)
        self.actionSelectionner_tout.triggered.connect(self.textEdit.selectAll)

        self.actionA_Propos.triggered.connect(self.show_about)
        self.actionA_Propos_de_Qt.triggered.connect(self.show_qt_about)

    def connect_content_action(self):
        self.textEdit.textChanged.connect(self.on_text_edit_changed)

    def connect_all_actions(self):
        self.connect_menu_actions()
        self.connect_content_action()

    def new_file(self):
        if not self.is_saved():
            self.show_save_demand()

        self.textEdit.clear()

    def open_file(self):
        self.current_file, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "./")
        if self.current_file:
            with open(self.current_file, "r") as file:
                text = file.read()
                self.textEdit.setPlainText(text)
                self.current_content = text
                self.old_content = text

            self.upgrade_content()

    def save_file(self):
        if self.current_file is not None:
            with open(self.current_file, "w") as file:
                file.write(self.textEdit.toPlainText())

            self.upgrade_content()

        else:
            self.save_file_as()

    def save_file_as(self):
        self.current_file, _ = QFileDialog.getSaveFileName(self, "Sauvegarder le fichier", "./", )
        if self.current_file:
            self.save_file()

    def exit(self):
        if not self.is_saved():
            self.show_save_demand()
        self.close()

    def on_text_edit_changed(self):
        self.current_content = self.textEdit.toPlainText()
        self.update_title()

    def update_title(self):
        if not self.is_saved():
            self.setWindowTitle("BlocNote *")
        else:
            self.setWindowTitle("BlocNote")

        if self.is_saved() and self.current_file:
            self.setWindowTitle(f"BlocNote {self.get_file_name()}")

    def is_saved(self):
        return self.current_content and self.current_content == self.old_content

    def upgrade_content(self):
        self.old_content = self.current_content
        self.update_title()

    def show_save_demand(self):
        response = QMessageBox.information(
            self, "Information", "Votre document n'a pas ete sauvegarde.",
            QMessageBox.StandardButton.Save, QMessageBox.StandardButton.Cancel
        )
        if response is QMessageBox.StandardButton.Save:
            self.save_file()

    def get_file_name(self):
        if self.current_file:
            return "/" + str(self.current_file).split("/")[-1]

    def show_about(self):
        QMessageBox.about(self, "A propos de BlocNote", "Par Landry Simo")

    def show_qt_about(self):
        QMessageBox.aboutQt(self, "A propos de Qt")

from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QFontDialog, QColorDialog

from src.config import Config
from ui import main_window


class BlocNoteWindow(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        """
        Initializes the class and sets up the user interface.

        Parameters:
            None

        Returns:
            None
        """
        super().__init__()
        self.setupUi(self)

        self.current_file = None
        self.old_content = None
        self.current_content = None
        self.current_font = QFont()
        self.background_color = QColor()
        self.foreground_color = QColor()

        self.connect_all_actions()

    def connect_menu_actions(self):
        """
        Connects the menu actions to their respective functions.

        This function connects the menu actions of the application's menu bar to their corresponding functions. The menu actions include options like "New File", "Open File", "Save File", and "Exit". When a menu action is triggered, the corresponding function is called to perform the desired action.

        Parameters:
        - None

        Returns:
        - None
        """
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

        self.actionPolice_de_caractere.triggered.connect(self.choose_font_size)
        self.actionCouleur_de_fond.triggered.connect(self.choose_background_color)
        self.actionCouleur_du_texte.triggered.connect(self.choose_foreground_color)
        self.actionLecture_seule.triggered.connect(self.toggle_readonly)

        self.actionA_Propos.triggered.connect(self.show_about)
        self.actionA_Propos_de_Qt.triggered.connect(self.show_qt_about)

        self.destroyed.connect(self.exit)

    def connect_content_action(self):
        """
        Connects the `textChanged` signal of the `textEdit` widget to the `on_text_edit_changed` slot.
        """
        self.textEdit.textChanged.connect(self.on_text_edit_changed)

    def connect_all_actions(self):
        """
        Connects all the actions in the class.
        """
        self.connect_menu_actions()
        self.connect_content_action()

    def new_file(self):
        """
        Clears the text in the textEdit widget.

        Parameters:
            None

        Returns:
            None
        """
        if not self.is_saved():
            self.show_save_demand()

        self.textEdit.clear()

    def open_file(self):
        """
        Opens a file dialog to allow the user to select a file. If a file is selected, it reads the contents of the file and sets the text in the textEdit widget to the file contents. It also updates the current_content and old_content variables with the file contents. Finally, it calls the upgrade_content() method.
        """
        self.current_file, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "./")
        if self.current_file:
            with open(self.current_file, "r") as file:
                text = file.read()
                self.textEdit.setPlainText(text)
                self.current_content = text
                self.old_content = text

            self.upgrade_content()

    def save_file(self):
        """
        Saves the contents of the current file to disk.

        This method checks if a current file is set. If so, it opens the file in write mode and writes the contents of the textEdit widget to the file. After saving the file, it calls the `upgrade_content()` method to perform any necessary upgrades to the saved content.

        If no current file is set, it calls the `save_file_as()` method to prompt the user to save the file with a new name.
        """
        if self.current_file is not None:
            with open(self.current_file, "w") as file:
                file.write(self.textEdit.toPlainText())

            self.upgrade_content()

        else:
            self.save_file_as()

    def save_file_as(self):
        """
        Save the current file as a new file.

        Parameters:
            None

        Returns:
            None
        """
        self.current_file, _ = QFileDialog.getSaveFileName(self, "Sauvegarder le fichier", "./", )
        if self.current_file:
            self.save_file()

    def exit(self):
        """
        Exit the program.
        """
        if not self.is_saved():
            self.show_save_demand()
        self.close()

    def close(self) -> bool:
        Config(self).store_config()
        return True

    def on_text_edit_changed(self):
        """
        Updates the current content of the text edit and calls the `update_title` method.

        Parameters:
            None

        Returns:
            None
        """
        self.current_content = self.textEdit.toPlainText()
        self.update_title()

    def update_title(self):
        """
        Updates the title of the BlocNote window based on the current state of the application.

        This function checks if the document has been saved or not. If it has not been saved, 
        the window title is set to "BlocNote *", indicating that there are unsaved changes. 
        Otherwise, the title is set to "BlocNote".

        Additionally, if the document has been saved and there is a current file, the title 
        is updated to include the name of the file, formatted as "BlocNote <filename>".

        Parameters:
            self (BlocNote): The instance of the BlocNote class.

        Returns:
            None
        """
        if not self.is_saved():
            self.setWindowTitle("BlocNote *")
        else:
            self.setWindowTitle("BlocNote")

        if self.is_saved() and self.current_file:
            self.setWindowTitle(f"BlocNote {self.get_file_name()}")

    def is_saved(self):
        """
        Check if the current content is saved.

        Returns:
            bool: True if the current content is saved, False otherwise.
        """
        return self.current_content and self.current_content == self.old_content

    def upgrade_content(self):
        """
        Upgrade the content of the object.

        This function updates the old_content attribute by assigning the current_content value to it. It then calls the update_title() method.

        Parameters:
            None

        Returns:
            None
        """
        self.old_content = self.current_content
        self.update_title()

    def show_save_demand(self):
        """
        Show a message box to inform the user that their document has not been saved and provide options to save or cancel.

        Parameters:
            self: The current instance of the class.
        
        Returns:
            None
        """
        response = QMessageBox.information(
            self, "Information", "Votre document n'a pas ete sauvegarde.",
            QMessageBox.StandardButton.Save, QMessageBox.StandardButton.Cancel
        )
        if response is QMessageBox.StandardButton.Save:
            self.save_file()

    def get_file_name(self):
        """
        Returns the filename of the current file.

        :param self: The current instance of the class.
        :return: A string representing the filename of the current file.
        """
        if self.current_file:
            return "/" + str(self.current_file).split("/")[-1]

    def show_about(self):
        """
        Displays a message box with information about the application.

        Parameters:
            self (object): The instance of the class.
        
        Returns:
            None
        """
        QMessageBox.about(self, "A propos de BlocNote", "Par Landry Simo")

    def show_qt_about(self):
        QMessageBox.aboutQt(self, "A propos de Qt")

    def choose_font_size(self):
        """
        Prompts the user to select a font size and sets it as the current font for the text editor.

        Returns:
            None.
        """
        self.current_font, selected = QFontDialog.getFont(self.current_font, self, "Choisir la police de caractere")
        if selected:
            self.textEdit.setFont(self.current_font)

    def choose_background_color(self):
        self.background_color = QColorDialog.getColor(
            self.background_color, self, "Choisir la couleur de fond"
        )
        if self.background_color:
            self.textEdit.setTextBackgroundColor(self.background_color)

    def choose_foreground_color(self):
        self.foreground_color = QColorDialog.getColor(
            self.background_color, self, "Choisir la couleur du texte"
        )
        if self.foreground_color:
            self.textEdit.setTextColor(self.foreground_color)

    def toggle_readonly(self):
        self.textEdit.setReadOnly(self.actionLecture_seule.isChecked())

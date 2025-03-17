from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QDialogButtonBox
from PyQt5.QtCore import Qt

class EditDialog(QDialog):

    def __init__(self, parent=None, main_window=None, item=None):
        super().__init__(None, Qt.Dialog)

        # region Janela - Editar Descrição

        # Lá embaixo, no open dialog, eu passei a janela principal MainWindow, pra conseguir usar as funções dela
        self.main_window = main_window
        # No open dialog eu também passei o self.current_item pra ser esse 'item'.
        self.item = item

        # Definindo atributos da window
        self.setWindowTitle(f"Editar descrição de '{item}'")
        self.setGeometry(200, 200, 400, 300)

        mainlayout = QVBoxLayout(self)

        # Definindo Título (da label)
        self.labeltitulo = QLabel(f"Aqui você pode editar a descrição de sua atividade como quiser.")
        mainlayout.addWidget(self.labeltitulo)

        # Definindo descrição a ser editada
        # Criaremos uma QTextEdit
        self.text_edit = QTextEdit(self)
        # Criamos uma variavel descrição, que vai usar a função da mainwindow get_description
        descricao = self.main_window.get_description()
        # Setamos o texto da QTextEdit como a descrição que a função da mainwindow pegou
        self.text_edit.setText(descricao)
        # Adicionamos o QTextEdit pro mainlayout
        mainlayout.addWidget(self.text_edit)

        # Botões de save e cancel
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.save_description)
        self.button_box.rejected.connect(self.reject)
        mainlayout.addWidget(self.button_box)
        # endregion

    def save_description(self):
        novadesc = self.text_edit.toPlainText()

        for habito in self.main_window.habitos:
            if habito["name"] == self.item:
                habito["description"] = novadesc
                break
        self.main_window.model.layoutChanged.emit()

        itens_lista = self.main_window.lista.findItems(self.item, Qt.MatchExactly)
        if itens_lista:
            self.main_window.get_title_name(itens_lista[0])

        self.accept()
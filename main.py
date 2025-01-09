import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QListWidget, QVBoxLayout,
                             QWidget, QHBoxLayout, QLineEdit, QPushButton, QGridLayout, QLabel, QListView,
                             QAbstractItemView, QMessageBox, QDialog, QDialogButtonBox, QTextEdit)
from PyQt5.QtCore import Qt, QTimer, QAbstractListModel, QModelIndex
from bs4 import BeautifulSoup

# Cria uma subclasse de QAbstractListModel, pra criar um modelo totalmente personalizado pra mostrar na seção da direita
# PS: rowCount e data são nomes necessários para que o QAbstractListModel funcione.
class ListViewModel(QAbstractListModel):


    def __init__(self, habitos = None):
        super().__init__()
        self.habitos = habitos or []


    # Função necessária para exibir os dados numa célula da lista QListView
    # É passado 2 parametros, index (posição), e role (um tipo de dado).
    # Se o dado for um Qt.DisplayRole, dará continuidade...
    def data(self, index, role):

        if role == Qt.DisplayRole:
            # Ferramenta que acessa self.habitos (um dicionário), checando cada index e pegando ele.
            habito = self.habitos[index.row()]
            # O valor do dicionário que a função hábito pegou será retornado neste formato abaixo
            # E aí o hábito será exibido
            return (f"{habito['name']}\n"
                    f"Estado: {habito['status']}\n"
                    f"Tempo em andamento: {habito['actual_time']}s\n"
                    f"Tempo total: {habito['total_time']}s")

    # Apenas diz ao PyQt5 quantas linhas estão presentes
    def rowCount(self, index=QModelIndex()):
        return len(self.habitos)

class EditDialog(QDialog):

    def __init__(self, parent=None, main_window =None, item=None):
        super().__init__(parent)

        # region Janela - Editar Descrição

        # Lá embaixo, no open dialog, eu passei a janela principal MainWindow, pra conseguir usar as funções dela
        self.main_window = main_window
        # No open dialog eu também passei o self.current_item pra ser esse 'item'.
        self.item = item

        # Definindo atributos da window
        self.setWindowTitle(f"Editar descrição de '{item}'")
        self.setGeometry(200,200,400,300)

        mainlayout = QVBoxLayout(self)

        # Definindo Título (da label)
        self.labeltitulo = QLabel(f"Aqui você pode editar a descrição de sua atividade como quiser.")
        mainlayout.addWidget(self.labeltitulo)

        # Definindo descrição a ser editada
        self.text_edit = QTextEdit(self)
        descricao = self.main_window.get_description()
        self.text_edit.setText(descricao)
        mainlayout.addWidget(self.text_edit)

        # Botões de save e cancel
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        mainlayout.addWidget(self.button_box)

        # endregion



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Habit Tracker")
        self.setGeometry(100, 150, 900, 600)


        #region Criando itens (Labels | Lists | Buttons)

        self.labelprincipal = QLabel("Aqui ficará as atividades", self)
        self.listatexto = QLineEdit(self)
        self.lista = QListWidget(self)
        self.lista2 = QListView(self)
        self.botaoadicionar = QPushButton("Adicionar...")
        self.botaodeletar = QPushButton("Deletar...")
        self.botaoiniciar = QPushButton("Iniciar")
        self.botaopausar = QPushButton("Pausar")
        self.botaoreiniciar = QPushButton("Reiniciar")
        self.botaoparar = QPushButton("Parar / Zerar")
        self.botaoeditdesc = QPushButton("Editar descrição...")

        #endregion

        #region TEMPORARIO = Itens teste da lista 1

        # Adicionando itens à lista 1
        self.lista.addItem("Teste #1")
        self.lista.addItem("Teste #2")
        self.lista.addItem("Teste #3")
        self.lista.addItem("LAYANINHA")

        #endregion

        # region Criando self.habitos

        # Criando self.hábitos, que será usado no listviewmodel. Valores padrões passados como teste.
        self.habitos = [
            {"name": "Teste #4",
             "status": "INATIVO",
             "seconds_elapsed": 0,
             "running": False,
             "actual_time": 0,
             "total_time": 0},

            {"name": "Teste #5",
             "status": "INATIVO",
             "seconds_elapsed": 0,
             "actual_time": 0,
             "running": False,
             "total_time": 10},

            {"name": "LAYANINHA",
             "status": "INATIVO",
             "seconds_elapsed": 0,
             "actual_time": 0,
             "running": False,
             "total_time": 0}
        ]

        # endregion

        # region Lista 2 --> ListViewModel

        # Setando o modelo da lista 2: O modelo é um listviewmodel, usando self.habitos
        self.model = ListViewModel(self.habitos)
        self.lista2.setModel(self.model)

        # endregion

        # region Definindo os tamanhos dos botoes

        # Setando size de todos
        self.botaoadicionar.setFixedSize(150,25)
        self.botaodeletar.setFixedSize(150,25)

        self.botaoiniciar.setFixedSize(170,50)
        self.botaopausar.setFixedSize(170, 50)
        self.botaoreiniciar.setFixedSize(170,50)
        self.botaoparar.setFixedSize(170, 50)
        self.botaoeditdesc.setFixedSize(100, 50)

        self.lista.setFixedWidth(150)
        self.lista2.setFixedWidth(300)
        self.listatexto.setFixedSize(150, 30)
        self.labelprincipal.setFixedWidth(self.width())

        # endregion

        # region Funções do timer

        # Criando funções para o timer
        self.current_item = None                        # Armazena o nome da atividade atual
        self.timer = QTimer()                           # Dispara a cada 1s (Configurado mais adiante)
        self.timer.timeout.connect(self.update_timer)   # Quando o timer atingir o tempo configurado, executa a função

        # endregion

        self.initUI()


    def initUI(self):

        # region Cleanar seleções

        # Definindo funções ao mudar uma seleção de uma lista
        self.lista.selectionModel().selectionChanged.connect(self.lista2_selecao_clear)
        self.lista2.selectionModel().selectionChanged.connect(self.lista_selecao_clear)

        # endregion

        # region Funções de botões e double click

        # Definindo funções aos double-click da lista, e ao click dos botões
        self.lista.itemDoubleClicked.connect(self.get_title_name)
        self.botaoadicionar.clicked.connect(self.addlistaitem)
        self.botaodeletar.clicked.connect(self.deletelistaitem)
        self.botaoiniciar.clicked.connect(self.start_timer)
        self.botaopausar.clicked.connect(self.stop_timer)
        self.botaoreiniciar.clicked.connect(self.reset_timer)
        self.botaoparar.clicked.connect(self.fullstop)
        self.botaoeditdesc.clicked.connect(self.open_edit_dialog)

        # endregion

        # region Texto padrão da label + Estilo

        # Style da Label
        self.labelprincipal.setStyleSheet("""
            background-color: white;
            color: black;
            border: 2px solid black;
            border-radius: 5px;
            font-size: 20px;
            font-weight: bold; 
            word-wrap: break-word;        
        """)


        # Texto padrão da label
        textopadrao = f"""
        <p style=
        "font-size: 24px; 
        font-weight: bold; 
        color: black;">
        Exemplo de título
        </p>
        <br>
        <p style=
        "font-size: 16px; 
        color: lightgray;
        text-align: left;
        margin: 10px;">
        Exemplo de descrição
        </p>
        """

        # Setando texto da label padrão.
        self.labelprincipal.setText(textopadrao)
        self.labelprincipal.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.labelprincipal.setWordWrap(True)

        #endregion

        #region Manipulação de layouts

        # Criando layout de botões
        layoutbotoes = QHBoxLayout()
        layoutbotoes.addWidget(self.botaoiniciar)
        layoutbotoes.addWidget(self.botaopausar)
        layoutbotoes.addWidget(self.botaoreiniciar)
        layoutbotoes.addWidget(self.botaoparar)
        layoutbotoes.addWidget(self.botaoeditdesc)


        # Criando layout da esquerda
        layoutesquerda = QVBoxLayout()
        layoutesquerda.addWidget(self.lista)
        layoutesquerda.addWidget(self.listatexto)
        layoutesquerda.addWidget(self.botaoadicionar)
        layoutesquerda.addWidget(self.botaodeletar)

        # Criando layout da direita
        layoutdireita = QVBoxLayout()   # Define o layout da direita como um VBOX
        layoutdireita.addWidget(self.lista2)   # Adiciona uma lista no layout da direita


        # Criando layout central
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.labelprincipal)
        central_layout.addLayout(layoutbotoes)


        # Criando layout que vai conter todos os outros
        layoutzao = QHBoxLayout()
        layoutzao.addLayout(layoutesquerda)
        layoutzao.addStretch(0)
        layoutzao.addLayout(central_layout)
        layoutzao.addStretch(0)
        layoutzao.addLayout(layoutdireita)

        # Criando o widget que vai conter o layout, já que anexar um layout a uma janela é impossível
        widgetcentral = QWidget(self)
        widgetcentral.setLayout(layoutzao)
        self.setCentralWidget(widgetcentral)

        #endregion



    # region Todas as funções do programa




    # region Manipulação da label

    # Toda vez que houver um double-clique na lista à esquerda, essa função será executada..
    def get_title_name(self, item):

        # Pega o nome do que foi double clickado
        nomeatividade = item.text()

        # Printa oque foi double clicado
        print(f"{nomeatividade}")

        # Faz um novo título com oque foi double clickado
        updatetitulo = f"""
        <p style=
        "font-size: 24px; 
        font-weight: bold; 
        color: black;">
        {nomeatividade}
        </p>
        <br>
        <p style=
        "font-size: 16px; 
        color: lightgray;
        text-align: left;
        margin: 10px;">
        O título e a descrição foram atualizados.
        </p>
        """

        # Atualiza o título da label pro que foi double-clickado
        self.labelprincipal.setText(updatetitulo)

        # Armazena o nome do item que foi double clicado nesse "Current item"
        self.current_item = nomeatividade

    def get_description(self):
        descricao_html = self.labelprincipal.text()

        soup = BeautifulSoup(descricao_html, "html.parser")

        descricao_tag = soup.find_all("p")[1]

        if descricao_tag:
            descricao_texto = descricao_tag.get_text(strip=True)
            print(f"Descrição: {descricao_texto}")
            return descricao_texto
        else:
            print("Nada mano. Foi mal")


    # endregion

    # region Funções caixa de texto

    # Toda vez que houver um clique no botão adicionar, essa função será executada.
    def addlistaitem(self):


        # Pega o texto que o usuário digitou na caixa de texto. Strip apaga os espaços
        texto = self.listatexto.text().strip()
        # Se houver algum texto digitado...
        if texto:
            # Adiciona o texto na lista da esquerda
            self.lista.addItem(texto)
            # Adiciona o texto no dicionário self.habitos, que por sua vez é automaticamente adicionado na lista
            # por conta da função data
            self.habitos.append(
                {"name": texto,
                 "status": "INATIVO",
                 "seconds_elapsed": 0,
                 "running": False,
                 "actual_time": 0,
                 "total_time":0}
            )
            # Notifica ao PyQt que algo mudou, fazendo-o atualizar a lista
            self.model.layoutChanged.emit()
            # Limpa a caixa de texto que foi digitado
            self.listatexto.clear()

            print(self.habitos)

    # Toda vez que houver um clique no botão deletar, essa função será executada.
    def deletelistaitem(self):

        # Vê se tem algo selecionado na lista 1
        item = self.lista.currentItem()
        # Se tiver
        if item:
            # Pegar o nome do item selecionado na lista 1
            nome_item_lista1 = item.text()
            # Veja todos os itens da lista 2
            for i, habito in enumerate(self.habitos):
                # Se na lista 2 tiver algo idêntico a lista 1
                if habito["name"] == nome_item_lista1:
                    if habito["running"]:
                        habito["running"] = False
                        habito["status"] = "INATIVO"
                        self.timer.stop()
                        print("A atividade estava ativa antes de deletá-la.\nParando o timer antes do delete...")
                    # Deleta da lista 2
                    del self.habitos[i]
                    self.model.layoutChanged.emit()
                    break
            # Pega a row lááá do primeiro item selecionado (na lista 1)
            linhalista1 = self.lista.row(item)
            # Deleta também
            self.lista.takeItem(linhalista1)

    # endregion

    #region Funções botões timers

    # Ao clicar iniciar, essa função é executada
    def start_timer(self):
        # Se o item selecionado for válido
        if self.current_item:
            for habito in self.habitos:
                # Se algum hábito tiver rodando: running definido como false, status definido como inativo
                if habito["running"] == True:
                    habito["running"] = False
                    habito["status"] = "INATIVO"
                # Se tiver algum hábito com o mesmo nome do selecionado
                if habito["name"] == self.current_item:
                    # Seta running como true e status como ativo, indicando que está rodando
                    habito["running"] = True
                    habito["status"] = "ATIVO"
                    # Começa o timer
                    self.timer.start(1000)
                    # Timer iniciado
                    print(f"Timer iniciado para: {self.current_item}")
                    break
        else:
            print("O item selecionado não é válido")

    # Essa função é executada a cada 1 segundo após o timer ser ligado
    def update_timer(self):
        for habito in self.habitos:
            # Se tiver algum hábito rodando
            if habito["running"] == True:
                # Aumenta 1s dos seconds_elapsed dele
                habito["seconds_elapsed"] += 1
                # Atualiza o "total_time" dele pra seconds_elapsed
                habito["total_time"] = habito["seconds_elapsed"]
                # Aumenta o "actual_time" em 1s
                habito["actual_time"] += 1
                # Atualiza a lista
                self.model.layoutChanged.emit()
                break

    # Essa função é executada sempre que o botão Pausar ser clicado
    def stop_timer(self):

        # Se não houver algo selecionado
        if not self.current_item:
            # Mensagem de aviso
            self.warningwrongselec("Nenhum hábito válido selecionado.")
        else:
            # Define habit found e wrong selection
            habit_found = False
            wrong_selection = False
            # Loopa
            for habito in self.habitos:
                # Se tiver algum hábito rodando, prossegue
                if habito["running"]:
                    # Se não tiver nenhum hábito com o nome do que tá selecionado
                    if habito["name"] != self.current_item:
                        # Seleção errada é true
                        wrong_selection = True
                    else:
                        # Se tiver algo rodando, e o nome for igual, vai pausar o hábito normalmente
                        habito["running"] = False
                        self.timer.stop()
                        print(f"Timer pausado para: {self.current_item}")
                        habito["status"] = "INATIVO"
                        habit_found = True

                        break
            # Se apenas for seleção errada, mas achar um hábito
            if wrong_selection and not habit_found:
                self.warningwrongselec("Por favor, selecione o hábito corretamente")

            # Se não achar um hábito, e nem uma seleção errada
            if not habit_found and not wrong_selection:
                self.warningwrongselec("Não parece ter um hábito ativo...")

            # Atualiza o modelo
            self.model.layoutChanged.emit()

    # Essa função é executada sempre que o botão Reiniciar ser clicado
    def reset_timer(self):
        wrong_selection = False

        for habito in self.habitos:
            # Se tiver algum hábito com o tempo em andamento maior que um, prossegue
            if habito["actual_time"] >= 1:
                # Se não tiver nenhum hábito com o nome do que tá selecionado
                if habito["name"] != self.current_item:
                    # Seleção errada é true
                    wrong_selection = True
                else:
                    # Atualiza o actual time dele pra 0
                    habito["actual_time"] = 0
                    # Printa isso
                    print("Timer zerado monstramente.")
                    # Atualiza o modelo
                    self.model.layoutChanged.emit()
                    break

        # Se apenas for seleção errada, mas achar um hábito
        if wrong_selection:
            self.warningwrongselec("Por favor, selecione o hábito corretamente")

    # Essa função é executada sempre que o botão Parar/Zerar ser clicado
    def fullstop(self):
        for habito in self.habitos:
            # Se não tiver nenhum hábito com o nome do que tá selecionado
            if habito["name"] == self.current_item:
                # Performa essas mudanças e para o timer
                habito["running"] = False
                habito["status"] = "INATIVO"
                habito["actual_time"] = 0
                print("ZERADO")
                self.model.layoutChanged.emit()
                break
            if habito["name"] == self.current_item and habito["running"]:
                self.timer.stop()

    # endregion

    # region Função pop-up editar descrição
    def open_edit_dialog(self):
        item = self.current_item
        if item == None:
            self.warningwrongselec("Por favor, selecione um item corretamente antes de editá-lo.")
        else:
            dialog = EditDialog(self, self, item)
            dialog.exec_()
    # end region

    # region Função caixa de aviso

    # Mensagem de aviso genérica. . .
    def warningwrongselec(self, text):

        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setWindowTitle("Aviso")
        msgbox.setText(text)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.exec_()

    # endregion

    # region Funções cleanar seleção

    # Toda vez que algo for selecionado na lista 1, vai limpar na lista 2
    def lista_selecao_clear(self):
        if self.lista2.selectedIndexes():
            self.lista.selectionModel().clearSelection()

    # Toda vez que algo for selecionado na lista 2, vai limpar na lista 1
    def lista2_selecao_clear(self):
        if self.lista.selectedIndexes():
            self.lista2.selectionModel().clearSelection()

    # endregion




    # endregion



    #endregion

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

    # def resizeEvent(self, event):   # Caso o usuário maximize a tela, vai ter a altura da tela
    #     self.lista.setGeometry(0, 0, 150, self.height())
    #     self.lista2.setGeometry(self.width() - 150, 0, 150, self.height())
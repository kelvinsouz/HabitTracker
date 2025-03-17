from PyQt5.QtWidgets import QMainWindow, QLabel, QListWidget, QListView, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QApplication, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFontDatabase
from models import ListViewModel
from habit_manager import load, save
from dialogs import EditDialog
from bs4 import BeautifulSoup

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Habit Tracker")
        self.setGeometry(100, 150, 900, 600)

        self.habitos = load()
        self.model = ListViewModel(self.habitos)

        self.current_item = None                        # Armazena o nome da atividade atual
        self.timer = QTimer()                           # Dispara a cada 1s (Configurado mais adiante)
        self.timer.timeout.connect(self.update_timer)   # Quando o timer atingir o tempo configurado, executa a função

        self.initUI()

    def initUI(self):

        # region Criando listas e botões, setando sizes

        self.labelprincipal = QLabel(self)
        self.listatexto = QLineEdit(self)
        self.lista = QListWidget(self)
        self.lista2 = QListView(self)
        self.lista2.setModel(self.model)
        self.botaoadicionar = QPushButton("Adicionar...")
        self.botaodeletar = QPushButton("Deletar...")
        self.botaoiniciar = QPushButton("Iniciar")
        self.botaopausar = QPushButton("Pausar")
        self.botaoreiniciar = QPushButton("Reiniciar")
        self.botaoparar = QPushButton("Parar / Zerar")
        self.botaoeditdesc = QPushButton("Editar descrição...")

        self.botaoadicionar.setFixedSize(175,25)
        self.botaodeletar.setFixedSize(175,25)

        self.botaoiniciar.setFixedSize(170,50)
        self.botaopausar.setFixedSize(170, 50)
        self.botaoreiniciar.setFixedSize(170,50)
        self.botaoparar.setFixedSize(170, 50)
        self.botaoeditdesc.setFixedSize(100, 50)

        self.lista.setFixedWidth(175)
        self.lista2.setFixedWidth(250)
        self.listatexto.setFixedSize(175, 30)
        self.labelprincipal.setFixedWidth(self.width())

        # endregion

        # region Definindo função dos botões e listas

        self.lista.itemDoubleClicked.connect(self.get_title_name)
        self.botaoadicionar.clicked.connect(self.addlistaitem)
        self.botaodeletar.clicked.connect(self.deletelistaitem)
        self.botaoiniciar.clicked.connect(self.start_timer)
        self.botaopausar.clicked.connect(self.stop_timer)
        self.botaoreiniciar.clicked.connect(self.reset_timer)
        self.botaoparar.clicked.connect(self.fullstop)
        self.botaoeditdesc.clicked.connect(self.open_edit_dialog)

        self.lista.clear()
        for habito in self.habitos:
            self.lista.addItem(habito["name"])

        # endregion

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

        # region Cleanar seleções

        # Definindo funções ao mudar uma seleção de uma lista
        self.lista.selectionModel().selectionChanged.connect(self.lista2_selecao_clear)
        self.lista2.selectionModel().selectionChanged.connect(self.lista_selecao_clear)

        # endregion

        # region Personalização de cores e estilos do programa
        QApplication.instance().setStyleSheet("""
            QMainWindow{
            background-color: #263238;
            }

            QMainWindow QLabel {
            background-color: white;
            border: 1px solid white;
            border-radius: 6px;
            font-weight: bold; 
            word-wrap: break-word;    
            }

            QMainWindow QPushButton{
            background-color: #00897B;
            color: #FFFFFF;
            font-family: Calibri;
            font-size: 14px;
            border: 1px solid #02756a; 
            border-radius: 6px;
            padding: 2px;
            }

            QMainWindow QPushButton:hover{
            background-color: #006359;
            }

            QMainWindow QPushButton:pressed{
            background-color: #013d37
            }

            QLineEdit {
            font-family: Calibri;
            font-size: 14px;
            border: 1px solid white; 
            border-radius: 6px;
            padding: 2px;
            }

            QListView {
            font-family: Calibri;
            font-size: 14px;
            border: 1px solid white; 
            border-radius: 3px
            }      

        """)

        self.botaoeditdesc.setStyleSheet("""
        font-size: 12px;        
        """)

        self.labelprincipal.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.labelprincipal.setWordWrap(True)
        self.resetlabel()

        #endregion


    # region Todas as funções do programa

    # region Manipulação da label

    # Toda vez que houver um double-clique na lista à esquerda, essa função será executada..
    def get_title_name(self, item):

        font_path = "Inter-VariableFont_opsz,wght.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            interfont = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            interfont = "Arial"

        descricaohabito = None

        # Pega o nome do que foi double clickado
        nomeatividade = item.text()

        # Loopa, se tiver um habito com o nome do que ta selecionado, muda a descricao pra descricao local dele
        for habito in self.habitos:
            if habito["name"] == nomeatividade:
                descricaohabito = habito["description"]

        # Faz um novo título com oque foi double clickado
        updatetitulo = f"""
        <p style=
        "font-size: 24px; 
        font-weight: 600; 
        font-family: {interfont};
        color: black;">
        {nomeatividade}
        </p>
        <br>
        <p style=
        "font-size: 20px; 
        font-weight: 200;
        font-family: {interfont};
        color: #212121;
        text-align: left;
        margin: 10px;">
        {descricaohabito}
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
            return descricao_texto
        else:
            print("Nenhuma descrição encontrada")

    def resetlabel(self):
        # Texto padrão da label

        font_path = "Inter-VariableFont_opsz,wght.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            interfont = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            interfont = "Arial"

        textopadrao = f"""
        <p style=
        "font-size: 24px; 
        font-weight: 600;
        font-family: {interfont}; 
        color: black;">
        Bem-vindo ao HabitTracker!
        </p>
        <br>
        <p style=
        "font-size: 20px; 
        font-weight: 200;
        color: #424242;
        font-family: {interfont};
        text-align: left;
        margin: 10px;">
        Esse programa tem a finalidade de ajudar você a acompanhar, gerenciar e melhorar seus hábitos diários, 
        tornando sua rotina mais produtiva. <br>
        Defina seus hábitos, acompanhe seu progresso, e o tempo que você investiu neles! <br><br>
        Vamos começar? <br><br>
        Para adicionar um hábito, digite o nome desejado na caixa de texto ao canto inferior esquerdo da tela.
        Após isso, clique em "Adicionar", e ele será adicionado automaticamente à lista de hábitos.
        </p>
        """
        # Setando texto da label padrão.
        self.labelprincipal.setText(textopadrao)

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
            # Adiciona o texto no dicionário self.habitos, que também vai pra lista2.
            self.habitos.append(
                {
                    "name": texto,
                    "status": "INATIVO",
                    "seconds_elapsed": 0,
                    "running": False,
                    "actual_time": 0,
                    "total_time": 0,
                    "description": "Atualmente não há uma descrição para essa tarefa.\nVocê pode customizar isso clicando no botão 'Editar Descrição' no canto inferior direito."
                }
            )
            # Se após adicionar esse hábito, o tamanho de self.habitos for 1, significa que esse é o
            # primeiro item da lista.
            if len(self.habitos) == 1:
                # Então ele vai criar esse modelo novo, e colocar na lista 2
                # atualizando a lista 2, QAbstractListView
                self.model = ListViewModel(self.habitos)
                self.lista2.setModel(self.model)
            else:
                # Se tiver mais de 1 item, só precisa atualizar mesmo
                self.model.layoutChanged.emit()
            self.listatexto.clear()

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
                    # Deleta da lista 2
                    del self.habitos[i]
                    self.model.layoutChanged.emit()
                    break
            # Pega a row lááá do primeiro item selecionado (na lista 1)
            linhalista1 = self.lista.row(item)
            # Deleta também
            self.lista.takeItem(linhalista1)
            self.resetlabel()

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
        found = False # Variável auxiliar pra ajudar a encontrar o hábito correto

        for habito in self.habitos:
            # Se tiver algum hábito com o tempo em andamento maior que um, prossegue
            if habito["actual_time"] >= 1:
                # Se tiver algum hábito com o nome do que tá selecionado
                if habito["name"] == self.current_item:
                    # Atualiza o actual time dele pra 0
                    habito["actual_time"] = 0
                    # Printa isso
                    print("Timer zerado monstramente.")
                    # Atualiza o modelo
                    self.model.layoutChanged.emit()
                    found = True
                    break
        # Se apenas for seleção errada, mas achar um hábito
        if found == False:
            self.warningwrongselec("Por favor, selecione o hábito corretamente")

    # Essa função é executada sempre que o botão Parar/Zerar ser clicado
    def fullstop(self):
        for habito in self.habitos:
            # Se tiver um hábito com o nome do que tá selecionado
             if habito["name"] == self.current_item:
                if self.warningconditional("Tem certeza que deseja zerar esse hábito?\nEssa ação não pode ser desfeita!"):
                    # Performa essas mudanças e para o timer
                    habito["running"] = False
                    habito["status"] = "INATIVO"
                    habito["actual_time"] = 0
                    habito["total_time"] = 0
                    habito["seconds_elapsed"] = 0
                    print("ZERADO")
                    self.model.layoutChanged.emit()
                    print(self.habitos)
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
    # endregion

    # region Função caixa de aviso

    # Mensagem de aviso genérica. . .
    def warningwrongselec(self, text):

        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setWindowTitle("Aviso")
        msgbox.setText(text)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.exec_()

    # Mensagem de aviso condicional
    def warningconditional(self, text):
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setWindowTitle("Aviso")
        msgbox.setText(text)
        msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resposta = msgbox.exec_()
        if resposta == QMessageBox.Yes:
            return True
        else:
            return False

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

    # region Função fechar
    def closeEvent(self, event):
        save(self.habitos)
        event.accept()
    # endregion


    # endregion
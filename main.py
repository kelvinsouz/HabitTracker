import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QListWidget, QVBoxLayout,
                             QWidget, QHBoxLayout, QLineEdit, QPushButton, QGridLayout, QLabel, QListView,
                             QAbstractItemView)
from PyQt5.QtCore import Qt, QTimer, QAbstractListModel, QModelIndex


# Cria uma subclasse de QAbstractListModel, pra criar um modelo totalmente personalizado pra mostrar na seção da direita
# PS: rowCount e data são nomes necessários para que o QAbstractListModel funcione.
class listviewmodel(QAbstractListModel):


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
            return f"{habito['name']}\nEstado: {habito['status']}\nTempo total: {habito['total_time']}s"

    # Apenas diz ao PyQt5 quantas linhas estão presentes
    def rowCount(self, index=QModelIndex()):
        return len(self.habitos)


class MainWindow(QMainWindow):


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Janela teste")
        self.setGeometry(100, 150, 900, 600)


        # Criando itens (Label, lista 1/2, caixa de texto, botões)
        self.labelprincipal = QLabel("Aqui ficará as atividades", self)
        self.listatexto = QLineEdit(self)
        self.lista = QListWidget(self)
        self.lista2 = QListView(self)
        self.botaoadicionar = QPushButton("Adicionar...")
        self.botaodeletar = QPushButton("Deletar...")
        self.botaoiniciar = QPushButton("Iniciar")
        self.botaoparar = QPushButton("Parar")
        self.botaoreiniciar = QPushButton("Reiniciar")
        self.botaozerar = QPushButton("Zerar")


        # Adicionando itens à lista 1
        self.lista.addItem("Teste #1")
        self.lista.addItem("Teste #2")
        self.lista.addItem("Teste #3")

        # Criando self.hábitos, que será usado no listviewmodel. Valores padrões passados como teste.
        self.habitos = [
            {"name": "Teste #4", "status": "INATIVO", "total_time": 0},
            {"name": "Teste #5", "status": "INATIVO", "total_time": 10}
        ]

        # Setando o modelo da lista 2: O modelo é um listviewmodel, usando self.habitos
        self.model = listviewmodel(self.habitos)
        self.lista2.setModel(self.model)


        # Setando size de todos
        self.botaoadicionar.setFixedSize(150,25)
        self.botaodeletar.setFixedSize(150,25)

        self.botaoiniciar.setFixedSize(200,50)
        self.botaoparar.setFixedSize(200,50)
        self.botaoreiniciar.setFixedSize(200,50)
        self.botaozerar.setFixedSize(200,50)

        self.lista.setFixedWidth(150)
        self.lista2.setFixedWidth(300)
        self.listatexto.setFixedSize(150, 30)
        self.labelprincipal.setFixedWidth(self.width())


        # Criando funções para o timer
        self.current_item = None                        # Armazena o nome da atividade atual
        self.timer = QTimer()                           # Dispara a cada 1s (Configurado mais adiante)
        self.timer.timeout.connect(self.update_timer)   # Quando o timer atingir o tempo configurado, executa a função
        self.seconds_elapsed = 0                        # Variável que armazena o tempo passado

        print(self.habitos)
        self.initUI()


    def initUI(self):

        # Definindo funções ao mudar uma seleção de uma lista
        self.lista.selectionModel().selectionChanged.connect(self.lista2_selecao_clear)
        self.lista2.selectionModel().selectionChanged.connect(self.lista_selecao_clear)

        # Definindo funções aos double-click da lista, e ao click dos botões
        self.lista.itemDoubleClicked.connect(self.get_title_name)
        self.botaoadicionar.clicked.connect(self.addlistaitem)
        self.botaodeletar.clicked.connect(self.deletelistaitem)
        self.botaoiniciar.clicked.connect(self.start_timer)

        # region Style de labels

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
        layoutbotoes.addWidget(self.botaoparar)
        layoutbotoes.addWidget(self.botaoreiniciar)
        layoutbotoes.addWidget(self.botaozerar)


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

        # Toda vez que houver um double click na lista1, o timer será resetado nessa função "Reset timer"
        self.reset_timer()



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
            self.habitos.append({"name": texto, "status": "INATIVO", "total_time":0})
            # Notifica ao PyQt que algo mudou, fazendo-o atualizar a lista
            self.model.layoutChanged.emit()
            # Limpa a caixa de texto que foi digitado
            self.listatexto.clear()

            print(self.habitos)


    # Toda vez que houver um clique no botão deletar, essa função será executada.
    def deletelistaitem(self):
        item = self.lista.currentItem()
        if item:
            linhalista1 = self.lista.row(item)
            self.lista.takeItem(linhalista1)
        else:
            selected_index = self.lista2.selectionModel().currentIndex()
            if selected_index.isValid():
                linhalista2 = selected_index.row()
                del self.habitos[linhalista2]
                self.model.layoutChanged.emit()



        # Pega o que tá selecionado
        # Se oque tiver selecionado for realmente um item, pega a linha desse item e deleta
        # item = self.lista.currentItem()
        # if item:
        #     linha = self.lista.row(item)
        #     self.lista.takeItem(linha)

    def start_timer(self):
        if self.current_item:
            self.seconds_elapsed = 0
            self.timer.start(1000)
            print(f"Timer iniciado para: {self.current_item}")

    def update_timer(self):
        self.seconds_elapsed += 1
        print(f"{self.current_item}: {self.seconds_elapsed} segundos.")

    def reset_timer(self):
        self.timer.stop()
        self.seconds_elapsed = 0
        print("Timer zerado monstramente.")

    def lista2_selecao_clear(self):
        # Limpa a seleção na lista2 se algo for selecionado na lista1
        if self.lista.selectedIndexes():
            self.lista2.selectionModel().clearSelection()

    def lista_selecao_clear(self):
        # Limpa a seleção na lista1 se algo for selecionado na lista2
        if self.lista2.selectedIndexes():
            self.lista.selectionModel().clearSelection()

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
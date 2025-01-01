import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QListWidget, QVBoxLayout,
                             QWidget, QHBoxLayout, QLineEdit, QPushButton, QGridLayout, QLabel)
from PyQt5.QtCore import Qt, QTimer


class MainWindow(QMainWindow):


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Janela teste")
        self.setGeometry(100, 150, 900, 600)


        # Criando itens (Label, lista 1/2, caixa de texto, botões)
        self.labelprincipal = QLabel("Aqui ficará as atividades", self)
        self.listatexto = QLineEdit(self)
        self.lista = QListWidget(self)
        self.lista2 = QListWidget(self)
        self.lista2.setDragDropMode(QListWidget.InternalMove)
        self.botaoadicionar = QPushButton("Adicionar...")
        self.botaodeletar = QPushButton("Deletar...")
        self.botaoiniciar = QPushButton("Iniciar")
        self.botaoparar = QPushButton("Parar")
        self.botaoreiniciar = QPushButton("Reiniciar")
        self.botaozerar = QPushButton("Zerar")


        # Adicionando itens as listas
        self.lista.addItem("Teste #1")
        self.lista.addItem("Teste #2")
        self.lista.addItem("Teste #3")
        self.lista2.addItem("Teste #4")
        self.lista2.addItem("Teste #5")


        # Setando size de todos
        self.botaoadicionar.setFixedSize(150,25)
        self.botaodeletar.setFixedSize(150,25)

        self.botaoiniciar.setFixedSize(200,50)
        self.botaoparar.setFixedSize(200,50)
        self.botaoreiniciar.setFixedSize(200,50)
        self.botaozerar.setFixedSize(200,50)

        self.lista.setFixedWidth(150)
        self.lista2.setFixedWidth(150)
        self.listatexto.setFixedSize(150, 30)
        self.labelprincipal.setFixedWidth(self.width())

        self.current_item = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.seconds_elapsed = 0


        self.initUI()


    def initUI(self):

        # Definindo funções aos botões, e double click na lista.
        self.lista.itemDoubleClicked.connect(self.get_title_name)
        self.botaoadicionar.clicked.connect(self.addlistaitem)
        self.botaodeletar.clicked.connect(self.deletelistaitem)
        self.botaoiniciar.clicked.connect(self.start_timer)


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
        Desc example
        </p>
        """


        self.labelprincipal.setText(textopadrao)
        self.labelprincipal.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.labelprincipal.setWordWrap(True)


        #region

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


    def get_title_name(self, item):
        # Pega o nome do que foi double clickado
        # Coloca o título da atividade double clickada na label
        # Por fim, seta o texto atualizado pra label
        nomeatividade = item.text()
        print(f"{nomeatividade}")

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
        ...
        </p>
        """
        self.labelprincipal.setText(updatetitulo)
        self.current_item = nomeatividade

        self.reset_timer()


    # Função adicionar lista
    def addlistaitem(self):
        # Pega o texto que tá na caixa de texto. Strip apaga espaços.
        # Quando a função for chamada, irá adicionar o texto a lista
        # Por fim, limpa a caixa de texto
        texto = self.listatexto.text().strip()
        if texto:
            self.lista.addItem(texto)
            self.listatexto.clear()


    # Função deletar item da lista
    def deletelistaitem(self):
        # Pega o que tá selecionado
        # Se oque tiver selecionado for realmente um item, pega a linha desse item e deleta
        item = self.lista.currentItem()
        if item:
            linha = self.lista.row(item)
            self.lista.takeItem(linha)

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
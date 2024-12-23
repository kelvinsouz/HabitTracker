import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QListWidget, QVBoxLayout,
                             QWidget, QHBoxLayout, QLineEdit, QPushButton, QGridLayout, QLabel)
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Janela teste")
        self.setGeometry(180, 150, 900, 600)


        # Criando itens (Label, lista 1/2, caixa de texto, botão)
        self.labeltitulo = QLabel("Olá", self)
        self.listatexto = QLineEdit(self)
        self.lista = QListWidget(self)
        self.lista2 = QListWidget(self)
        self.botaoadicionar = QPushButton("Adicionar...")
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
        self.botaoadicionar.setFixedSize(150,50)
        self.botaoiniciar.setFixedSize(200,50)
        self.botaoparar.setFixedSize(200,50)
        self.botaoreiniciar.setFixedSize(200,50)
        self.botaozerar.setFixedSize(200,50)
        self.lista.setFixedWidth(150)  # Largura da lista fixa de 150
        self.lista2.setFixedWidth(150)  # Largura da lista fixa de 150
        self.listatexto.setFixedSize(150, 30) # Largura da caixa de texto
        self.labeltitulo.setFixedWidth(self.width())

        self.initUI()


    def initUI(self):   # UI stuff


        self.labeltitulo.setStyleSheet("""
            background-color: white;
            color: black;
            border: 2px solid black;
            border-radius: 10px;
            font-size: 20px;
            font-weight: bold;         
        """)


        layoutzao = QHBoxLayout()   # Adiciona um layout horizontal, que vai ter o esquerda direita e central

        layoutbotoes = QHBoxLayout()
        layoutbotoes.addWidget(self.botaoiniciar)
        layoutbotoes.addWidget(self.botaoparar)
        layoutbotoes.addWidget(self.botaoreiniciar)
        layoutbotoes.addWidget(self.botaozerar)


        layoutesquerda = QVBoxLayout()   # Define o layout da esquerda como um VBOX
        layoutesquerda.addWidget(self.lista)   # Adiciona a lista no layout da esquerda
        layoutesquerda.addWidget(self.listatexto)  # Adiciona a caixa de texto no layout da esquerda
        layoutesquerda.addWidget(self.botaoadicionar)


        layoutdireita = QVBoxLayout()   # Define o layout da direita como um VBOX
        layoutdireita.addWidget(self.lista2)   # Adiciona uma lista no layout da direita

        central_layout = QVBoxLayout()
        central_layout.addWidget(self.labeltitulo)
        central_layout.addLayout(layoutbotoes)


        layoutzao.addLayout(layoutesquerda)
        layoutzao.addStretch(0)
        layoutzao.addLayout(central_layout)
        layoutzao.addStretch(0)
        layoutzao.addLayout(layoutdireita)

        widgetcentral = QWidget(self)
        widgetcentral.setLayout(layoutzao)
        self.setCentralWidget(widgetcentral)


    # def resizeEvent(self, event):   # Caso o usuário maximize a tela, vai ter a altura da tela
    #     self.lista.setGeometry(0, 0, 150, self.height())
    #     self.lista2.setGeometry(self.width() - 150, 0, 150, self.height())


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
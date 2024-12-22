import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QListWidget, QVBoxLayout,
                             QWidget, QHBoxLayout, QLineEdit, QPushButton, QGridLayout)
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Janela teste")
        self.setGeometry(280, 150, 900, 600)


        self.listatexto = QLineEdit(self)   # Criando LineEdit
        self.lista = QListWidget(self)  # Criando lista.
        self.lista2 = QListWidget(self)   # Criando caixa de texto da lista


        self.lista.addItem("Teste #1")  # Adicionando itens a lista 1
        self.lista.addItem("Teste #2")
        self.lista.addItem("Teste #3")
        self.lista2.addItem("Teste #4")   # Adicionando itens a lista 2
        self.lista2.addItem("Teste #5")

        self.lista.setFixedWidth(150)  # Largura da lista fixa de 150
        self.lista2.setFixedWidth(150)  # Largura da lista fixa de 150
        self.listatexto.setFixedSize(50, 50) # Largura da caixa de texto

        self.botao1 = QPushButton("#1")
        self.botao2 = QPushButton("#2")
        self.botao3 = QPushButton("#3")
        self.botao4 = QPushButton("#4")
        self.botao5 = QPushButton("#5")
        self.botao6 = QPushButton("#6")
        self.botao7 = QPushButton("#7")
        self.botao8 = QPushButton("#8")
        self.botao9 = QPushButton("#9")

        self.initUI()


    def initUI(self):   # UI stuff

        layoutzao = QHBoxLayout()   # Adiciona um layout horizontal, que vai ter o esquerda direita e central

        layoutesquerda = QVBoxLayout()   # Define o layout da esquerda como um VBOX
        layoutesquerda.addWidget(self.lista)   # Adiciona a lista no layout da esquerda
        layoutesquerda.addWidget(self.listatexto)  # Adiciona a caixa de texto no layout da esquerda


        layoutdireita = QVBoxLayout()   # Define o layout da direita como um VBOX
        layoutdireita.addWidget(self.lista2)   # Adiciona uma lista no layout da direita

        layoutgrid = QGridLayout()   # Cria um layout grid
        layoutgrid.addWidget(self.botao1, 0, 0) # Adicionando botões ao layout grid
        layoutgrid.addWidget(self.botao2, 0, 1)
        layoutgrid.addWidget(self.botao3, 0, 2)
        layoutgrid.addWidget(self.botao4, 1, 0)
        layoutgrid.addWidget(self.botao5, 1, 1)
        layoutgrid.addWidget(self.botao6, 1, 2)
        layoutgrid.addWidget(self.botao7, 2, 0)
        layoutgrid.addWidget(self.botao8, 2, 1)
        layoutgrid.addWidget(self.botao9, 2, 2)

        # Obs: Nenhum deles é visível ainda

        central_layout = QVBoxLayout() # VBOX pro widget central
        central_layout.addLayout(layoutgrid) # Adicionar um layout dentro de outro layout (Grid dentro do VBOX)

        layoutzao.addLayout(layoutesquerda)
        layoutzao.addStretch()
        layoutzao.addLayout(central_layout)
        layoutzao.addStretch()
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
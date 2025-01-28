import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JANELA MANEIRA")  # Define um título
        self.setGeometry(625, 350, 200, 200)  # Posição do X, Posição do Y, Largura, Altura

        self.botaoadicionar = QPushButton("Adicionar...")
        self.botaoiniciar = QPushButton("Iniciar")
        self.botaoparar = QPushButton("Parar")
        self.botaoreiniciar = QPushButton("Reiniciar")
        self.botaozerar = QPushButton("Zerar")
        self.initUI()

    def initUI(self):
        layoutbotoes = QHBoxLayout()
        layoutbotoes.addWidget(self.botaoiniciar)
        layoutbotoes.addWidget(self.botaoparar)
        layoutbotoes.addWidget(self.botaoreiniciar)
        layoutbotoes.addWidget(self.botaozerar)

        layoutbotoes.setSpacing(0)  # Define o espaçamento entre os botões como 2 pixels

        widgetcentral = QWidget(self)
        widgetcentral.setLayout(layoutbotoes)
        self.setCentralWidget(widgetcentral)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

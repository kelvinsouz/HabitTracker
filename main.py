import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Janela teste")
        self.setGeometry(280, 150, 900, 600)


        self.lista = QListWidget(self)  # Criando lista. Lista é um Widget de lista, vai se comportar como um
        self.lista.addItem("Teste #1")  # Itens teste
        self.lista.addItem("Teste #2")
        self.lista.addItem("Teste #3")

        self.lista.setFixedWidth(150)

    def resizeEvent(self, event):
        self.lista.setGeometry(0, 0, 150, self.height())


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
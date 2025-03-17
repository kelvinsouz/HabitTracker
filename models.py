from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
class ListViewModel(QAbstractListModel):
    def __init__(self, habitos = None):
        super().__init__()
        self.habitos = habitos or []


    def formatar_tempo(self, segundos):
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        segundos = segundos % 60
        tempoformatado = f"{horas}h {minutos}m {segundos}s" if horas else f"{minutos}m {segundos}s" if minutos else f"{segundos}s"
        return tempoformatado


    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Ferramenta que acessa self.habitos, checando cada index e pegando ele.
            habito = self.habitos[index.row()]
            # O valor do dicionário que a função hábito pegou será retornado neste formato abaixo
            # E aí o hábito será exibido
            return (f"{habito['name']}\n"
                    f"Estado: {habito['status']}\n"
                    f"Tempo em andamento: {self.formatar_tempo(habito['actual_time'])}\n"
                    f"Tempo total: {self.formatar_tempo(habito['total_time'])}\n")


    # Apenas diz ao PyQt5 quantas linhas estão presentes
    def rowCount(self, index=QModelIndex()):
        return len(self.habitos)
"""
============================================================
  Payslip Generator
  Developed by: Raphael Soares dos Santos
  Creation Date: February 10, 2025
============================================================
"""

import os
os.environ["QT_API"] = "PyQt5"
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QSize
from src.utils import obter_pasta_temp


class FolhaA4Viewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualização da Folha A4")
        self.setAttribute(Qt.WA_DontShowOnScreen)

        """
        if not os.path.exists(self.preview_path):
            print("A imagem 'holerite_preview.png' não foi encontrada. Encerrando o programa.")
           # sys.exit()"""

        self.label_folha = QLabel(self)
        self.label_folha.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label_folha)

        #self.posicao_holerite_duplicado()
        #self.posicao_holerite_horizontal()
        #self.posicao_holerite_vertical()


    def posicao_holerite_duplicado(self):
        """
        Posiciona dois holerites dentro da folha A4.
        """
        # Obtém o caminho correto da pasta temporária
        temp_dir = obter_pasta_temp()
        # Caminho atualizado para a imagem salva na pasta TEMP
        self.preview_path = os.path.join(temp_dir, "holerite_preview.png")

        # Define o fundo branco
        self.setGeometry(100, 100, 1700, 2400)
        self.setStyleSheet("background-color: white;")

        preview_pixmap = QPixmap(self.preview_path)
        if preview_pixmap.isNull():
            print("Erro ao carregar 'holerite_preview.png'")
            return

        # Define a escala e configura o tamanho da visualização
        escala = 2.20
        holerite_size = QSize(int(700 * escala), int(550 * escala))

        # Exibe o primeiro holerite no topo da página
        self.label_top = QLabel(self)
        self.label_top.setPixmap(preview_pixmap.scaled(holerite_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.label_top.resize(self.label_top.pixmap().size())
        self.label_top.move(75, 190)
        self.label_top.show()

        # Exibe o segundo holerite na parte inferior da página
        self.label_bottom = QLabel(self)
        self.label_bottom.setPixmap(preview_pixmap.scaled(holerite_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.label_bottom.resize(self.label_bottom.pixmap().size())
        self.label_bottom.move(75, 1250)
        self.label_bottom.show()

        # Salva a imagem individualmente e reinicia a interface
        self.salvar_imagem_individual("duplicado")
        self.restart_viewer()  # Reinicia a interface antes da próxima função


    def posicao_holerite_vertical(self):
        """
        Posiciona um único holerite no centro da folha A4.
        """
        # Obtém o caminho correto da pasta temporária
        temp_dir = obter_pasta_temp()
        # Caminho atualizado para a imagem salva na pasta TEMP
        self.preview_path = os.path.join(temp_dir, "holerite_preview.png")

        # Define o fundo branco
        self.setGeometry(100, 100, 1700, 2400)
        self.setStyleSheet("background-color: white;")

        preview_pixmap = QPixmap(self.preview_path)
        if preview_pixmap.isNull():
            print("Erro ao carregar 'holerite_preview.png'")
            return

        # Define a escala e configura o tamanho da visualização
        escala = 2.20
        holerite_size = QSize(int(700 * escala), int(550 * escala))

        self.label_single = QLabel(self)
        self.label_single.setPixmap(preview_pixmap.scaled(holerite_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.label_single.resize(self.label_single.pixmap().size())
        self.label_single.move(75, 720)
        self.label_single.show()

        # Salva a imagem individualmente e reinicia a interface
        self.salvar_imagem_individual("vertical")
        self.restart_viewer()  # Reinicia a interface antes da próxima função


    def posicao_holerite_horizontal(self):
        """
        Configura a posição horizontal da pré-visualização do holerite.
        """
        # Obtém o caminho correto da pasta temporária
        temp_dir = obter_pasta_temp()
        # Caminho atualizado para a imagem salva na pasta TEMP
        self.preview_path = os.path.join(temp_dir, "holerite_preview.png")

        # Define o fundo branco
        self.setGeometry(100, 100, 2400, 1700)
        self.setStyleSheet("background-color: white;")

        preview_pixmap = QPixmap(self.preview_path)
        if preview_pixmap.isNull():
            print("Erro ao carregar 'holerite_preview.png'")
            return

        # Define a escala e configura o tamanho da visualização
        escala = 3.20
        holerite_size = QSize(int(700 * escala), int(550 * escala))

        self.label_single = QLabel(self)
        self.label_single.setPixmap(preview_pixmap.scaled(holerite_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.label_single.resize(self.label_single.pixmap().size())
        self.label_single.move(80, 145)
        self.label_single.show()

        # Salva a imagem individualmente e reinicia a interface
        self.salvar_imagem_individual("horizontal")
        self.restart_viewer()  # Reinicia a interface antes da próxima função


    def restart_viewer(self):
        """Fecha e reabre a janela para resetar totalmente o estado gráfico."""
        self.close()  # Fecha a interface para limpar memória
        self.__init__()  # Reinicia a classe do zero


    def salvar_imagem_individual(self, nome):
        """Salva a imagem atual com o nome fornecido."""
        pixmap = QPixmap(self.size())  # Captura a interface atual
        self.render(pixmap)  # Renderiza a interface em um QPixmap
        save_path = os.path.join(os.path.dirname(self.preview_path), f"holerite_{nome}.png")
        pixmap.save(save_path, "PNG")
        print(f"Imagem do 'holerite_{nome}' salva em: {save_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = FolhaA4Viewer()
    #viewer.show()
    sys.exit(app.exec_())


# Developed by Raphael Soares dos Santos - Payslip Generator

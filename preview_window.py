"""
============================================================
  Payslip Generator
  Developed by: Raphael Soares dos Santos
  Creation Date: February 10, 2025
============================================================
"""

import os
os.environ["QT_API"] = "PyQt5"
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, \
    QScrollArea, QSpacerItem, QSizePolicy, QMessageBox, QFileDialog, QWidget
from PyQt5.QtGui import QPixmap, QImageReader, QIcon
from PyQt5.QtCore import Qt, QTimer, QSize, QEvent
from src.utils import imagem_para_pdf, obter_pasta_temp, aplicar_escalonamento_dpi
from src.printer import imprimir_holerite
import sys


class PreVisualizacaoHolerite(QDialog):

    def mousePressEvent(self, event):
        """Remove o foco de qualquer campo ao clicar fora, sem travamentos."""
        foco_atual = QApplication.focusWidget()
        if foco_atual and isinstance(foco_atual, QWidget):
            foco_atual.clearFocus()  # Remove o foco imediatamente
        super().mousePressEvent(event)

    def __init__(self, parent_ui=None, funcionario="", empresa=""):
        super().__init__()
        self.fator_escala = aplicar_escalonamento_dpi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.ui = parent_ui  # Armazena o objeto principal (ui.py)
        self.funcionario = funcionario
        self.empresa = empresa

        # Caminho dinâmico para o ícone dentro de 'assets/icons'
        base_dir = os.path.abspath(os.path.dirname(__file__))  # Caminho absoluto seguro
        icon_path = os.path.join(base_dir, "assets", "icons", "Logo2_holerite_generator.ico")

        # Verifica se o ícone realmente existe
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))  # Aplica o ícone à janela principal
        else:
            print(f"⚠️ Aviso: Ícone não encontrado em {icon_path}")

        base_dir = os.path.abspath(os.path.dirname(__file__))  # Caminho absoluto seguro
        icon_print_path = os.path.join(base_dir, "assets", "templates", "img_printer.png")

        self.setWindowTitle("Pré-visualização do Holerite")

        # Define a posição e o tamanho escalonado
        largura_base = 1050
        altura_base = 885
        self.setGeometry(
            int(450 * self.fator_escala),  # Posição X
            int(80 * self.fator_escala),  # Posição Y
            int(largura_base * self.fator_escala),  # Largura
            int(altura_base * self.fator_escala)  # Altura
        )
        self.setMaximumSize(int(largura_base * self.fator_escala), int(altura_base * self.fator_escala))

        # Aqui você define o redimensionamento de acordo com o conteúdo da tela
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Permite redimensionamento

        # Obtém o caminho correto da pasta temporária
        self.assets_dir = obter_pasta_temp()

        # Lista de imagens com caminho absoluto
        self.imagens = [
            os.path.join(self.assets_dir, "holerite_duplicado.png"),
            os.path.join(self.assets_dir, "holerite_horizontal.png"),
            os.path.join(self.assets_dir, "holerite_vertical.png")
        ]
        self.imagem_atual = 0
        self.zoom_factor = 0.3 * self.fator_escala

        self.caminho_pdf = os.path.join(os.path.expanduser("~"), "Desktop")

        main_layout = QVBoxLayout()

        # Área de Visualização com Scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Aplicar escalonamento na largura e altura da área de scroll
        largura_base = 920  # Largura base
        altura_base = 750  # Altura base

        self.scroll_area.setFixedSize(
            int(largura_base * self.fator_escala),
            int(altura_base * self.fator_escala)
        )
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(f"border: {int(2 * self.fator_escala)}px solid #888;")  # Borda também escalonada

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.carregar_imagem(self.imagens[self.imagem_atual])
        self.scroll_area.setWidget(self.image_label)

        # Layout para centralizar
        center_layout = QVBoxLayout()
        center_layout.addWidget(self.scroll_area, alignment=Qt.AlignCenter)
        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)
        center_layout.insertItem(0, spacer)  # Insere acima da scroll_area

        # Layout dos botões de zoom
        zoom_side_layout = QVBoxLayout()
        zoom_side_layout.setContentsMargins(
            0, int(300 * self.fator_escala), 0, 0
        )  # Move os botões para cima proporcionalmente

        # Botão de zoom in
        self.botao_zoom_in = QPushButton("🔍+")
        self.botao_zoom_in.setToolTip("Aproxima a visualização do holerite.")
        self.botao_zoom_in.setFixedSize(
            int(50 * self.fator_escala), int(50 * self.fator_escala)
        )  # Aplica a escala ao tamanho
        self.botao_zoom_in.clicked.connect(self.zoom_in)

        # Botão de zoom out
        self.botao_zoom_out = QPushButton("🔍-")
        self.botao_zoom_out.setToolTip("Afasta a visualização do holerite.")
        self.botao_zoom_out.setFixedSize(
            int(50 * self.fator_escala), int(50 * self.fator_escala)
        )  # Aplica a escala ao tamanho
        self.botao_zoom_out.clicked.connect(self.zoom_out)

        # Adicionar botões ao layout lateral
        zoom_side_layout.addWidget(self.botao_zoom_in)
        zoom_side_layout.addWidget(self.botao_zoom_out)
        zoom_side_layout.addStretch()

        # Área central com botões de zoom à direita
        center_with_zoom_layout = QHBoxLayout()
        center_with_zoom_layout.addWidget(self.scroll_area)
        center_with_zoom_layout.addLayout(zoom_side_layout)

        main_layout.addLayout(center_with_zoom_layout)

        # Navegação de Imagens
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(int(0 * self.fator_escala))  # Ajusta espaçamento conforme o DPI
        nav_layout.setContentsMargins(0, 0, 0, 0)

        # Botão Anterior
        self.botao_anterior = QPushButton("<")
        self.botao_anterior.setToolTip("Escolha o formato do holerite antes de gerar ou imprimir.")
        self.botao_anterior.setFixedSize(
            int(50 * self.fator_escala), int(25 * self.fator_escala)
        )  # Aplica escala no tamanho
        self.botao_anterior.clicked.connect(self.imagem_anterior)

        # Label do Tipo de Holerite
        self.label_tipo = QLineEdit("Holerite Duplicado")
        self.label_tipo.setAlignment(Qt.AlignCenter)
        self.label_tipo.setReadOnly(True)
        self.label_tipo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.label_tipo.setFixedSize(
            int(250 * self.fator_escala), int(25 * self.fator_escala)
        )  # Aplica a escala corretamente
        self.label_tipo.setStyleSheet("background-color: white; border: 1px solid #ccc;")

        # Botão Próximo
        self.botao_proximo = QPushButton(">")
        self.botao_proximo.setToolTip("Escolha o formato do holerite antes de gerar ou imprimir.")
        self.botao_proximo.setFixedSize(
            int(50 * self.fator_escala), int(25 * self.fator_escala)
        )  # Aplica escala no tamanho
        self.botao_proximo.clicked.connect(self.imagem_proxima)

        # Espaçadores ajustados para escalonamento
        spacer_esquerda = QSpacerItem(
            int(310 * self.fator_escala), int(30 * self.fator_escala), QSizePolicy.Fixed, QSizePolicy.Minimum
        )
        spacer_direita = QSpacerItem(
            int(310 * self.fator_escala), int(30 * self.fator_escala), QSizePolicy.Fixed, QSizePolicy.Minimum
        )

        nav_layout.addItem(spacer_esquerda)  # Controla a posição do botão esquerdo
        nav_layout.addWidget(self.botao_anterior)
        nav_layout.addWidget(self.label_tipo)
        nav_layout.addWidget(self.botao_proximo)
        nav_layout.addItem(spacer_direita)  # Controla a posição do botão direito

        # Adicionando uma mensagem informativa
        mensagem_label = QLabel("Selecione a versão do holerite a ser gerada:")
        mensagem_label.setAlignment(Qt.AlignCenter)  # Centraliza o texto

        # Ajusta o tamanho da fonte com base no fator de escala
        mensagem_label.setStyleSheet(
            f"font-size: {int(12 * self.fator_escala)}px; font-weight: bold; color: #333;"
        )
        # Layout para a mensagem
        mensagem_layout = QVBoxLayout()
        mensagem_layout.addWidget(mensagem_label)

        main_layout.addLayout(mensagem_layout)
        main_layout.addLayout(nav_layout)

        # Botões Gerais
        botoes_layout = QHBoxLayout()

        self.botao_gerar = QPushButton("Gerar Holerite")
        self.botao_gerar.setToolTip("Gera um PDF do holerite selecionado.")

        # Ajusta o tamanho do botão com base no fator de escala
        self.botao_gerar.setFixedSize(
            int(250 * self.fator_escala), int(25 * self.fator_escala)
        )

        self.botao_gerar.clicked.connect(self.gerar_holerite_preview)

        # Criar o botão de impressão com ícone
        self.botao_imprimir = QPushButton()
        self.botao_imprimir.setToolTip("Imprime o holerite selecionado.")

        # Ajusta o tamanho do botão com base no fator de escala
        self.botao_imprimir.setFixedSize(
            int(40 * self.fator_escala), int(25 * self.fator_escala)
        )

        # Aplicar o ícone se o arquivo existir
        if os.path.exists(icon_print_path):
            self.botao_imprimir.setIcon(QIcon(icon_print_path))
            # Ajusta o tamanho do ícone proporcionalmente ao DPI
            icon_size = int(17 * self.fator_escala)
            self.botao_imprimir.setIconSize(QSize(icon_size, icon_size))
        else:
            print(f"⚠️ Aviso: Ícone de impressão não encontrado em {icon_print_path}")

        # Conectar a função de impressão
        self.botao_imprimir.clicked.connect(self.imprimir_holerite_preview_window)

        # Botão de voltar com redimensionamento
        self.botao_voltar = QPushButton("Voltar")
        self.botao_voltar.setToolTip("Retorna à tela principal.")

        # Ajusta tamanho do botão proporcionalmente ao DPI
        self.botao_voltar.setFixedSize(int(250 * self.fator_escala), int(25 * self.fator_escala))

        self.botao_voltar.clicked.connect(self.close)

        # Ajuste dos espaçadores com fator de escala
        spacer_esquerda = QSpacerItem(int(0 * self.fator_escala), int(30 * self.fator_escala), QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_direita = QSpacerItem(int(120 * self.fator_escala), int(0 * self.fator_escala), QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_entre = QSpacerItem(int(0 * self.fator_escala), int(0 * self.fator_escala), QSizePolicy.Fixed, QSizePolicy.Minimum)

        # Adiciona os elementos ao layout com os espaçadores ajustados
        botoes_layout.addItem(spacer_esquerda)  # Espaço antes
        botoes_layout.addWidget(self.botao_gerar)
        botoes_layout.addItem(spacer_entre)  # Espaço entre
        botoes_layout.addWidget(self.botao_imprimir)
        botoes_layout.addWidget(self.botao_voltar)
        botoes_layout.addItem(spacer_direita)  # Espaço depois

        self.setLayout(main_layout)
        main_layout.addLayout(botoes_layout)

        # Espaçador invisível que cresce para a esquerda, agora ajustado ao fator de escala
        espacador_invisivel = QSpacerItem(
            int(120 * self.fator_escala), int(10 * self.fator_escala),
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        # Adicionando o espaçador ao layout principal
        main_layout.addItem(espacador_invisivel)

        #main_layout.addLayout(center_layout)


    def gerar_holerite_preview(self):
        self.gerar_pdf_do_holerite_preview()


    def carregar_imagem(self, nome_imagem):
        imagem_path = os.path.join(self.assets_dir, nome_imagem)
        if os.path.exists(imagem_path):
            reader = QImageReader(imagem_path)
            reader.setAutoTransform(True)
            image = reader.read()

            if not image.isNull():
                pixmap = QPixmap.fromImage(image).scaled(
                    int(image.width() * self.zoom_factor),
                    int(image.height() * self.zoom_factor),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_label.setPixmap(pixmap)
            else:
                self.image_label.setText("Erro ao carregar a imagem.")
        else:
            self.image_label.setText("Imagem não encontrada.")

    def zoom_in(self):
        self.zoom_factor += 0.1 * self.fator_escala
        self.atualizar_previsualizacao()

    def zoom_out(self):
        self.zoom_factor = max(0.29 * self.fator_escala, self.zoom_factor - (0.1 * self.fator_escala))
        self.atualizar_previsualizacao()

    def imagem_anterior(self):
        self.imagem_atual = (self.imagem_atual - 1) % len(self.imagens)
        self.atualizar_previsualizacao()

    def imagem_proxima(self):
        self.imagem_atual = (self.imagem_atual + 1) % len(self.imagens)
        self.atualizar_previsualizacao()

    def atualizar_previsualizacao(self):
        self.carregar_imagem(self.imagens[self.imagem_atual])
        nomes = ["Holerite Duplo", "Holerite Padrão - Folha Horizontal", "Holerite Padrão - Folha Vertical"]
        self.label_tipo.setText(nomes[self.imagem_atual])

    def gerar_pdf_do_holerite_preview(self, *args, **kwargs):
        """Permite que o usuário escolha o local e nome do arquivo antes de gerar o PDF da pré-visualização."""

        # Verifica se há uma imagem selecionada
        if 0 <= self.imagem_atual < len(self.imagens):
            holerite_selecionado = os.path.basename(self.imagens[self.imagem_atual])  # Obtém apenas o nome do arquivo
        else:
            QMessageBox.warning(self, "Erro", "Nenhum holerite selecionado.")
            return

        # Obtém o caminho correto da pasta temporária
        temp_dir = obter_pasta_temp()

        # Caminho correto da imagem dentro da pasta TEMP
        imagem_path = os.path.join(temp_dir, holerite_selecionado)

        # Dados da UI principal
        funcionario = self.ui.funcionario_input.text().strip() if self.ui else "Desconhecido"
        empresa = self.ui.empresa_input.text().strip() if self.ui else "Desconhecida"

        # Define um nome padrão para o arquivo PDF
        nome_padrao = f"holerite_{funcionario}" if funcionario else (f"holerite_{empresa}" if empresa else "holerite")
        nome_padrao = nome_padrao.replace(" ", "_").replace("/", "_").replace("\\", "_") + ".pdf"

        # Abre o seletor de arquivos para o usuário escolher o nome e o local do arquivo
        pdf_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Holerite",
            os.path.join(self.caminho_pdf, nome_padrao),
            "Arquivos PDF (*.pdf)"
        )

        # Se o usuário cancelar, interrompe a função
        if not pdf_path:
            QMessageBox.warning(self, "Ação Cancelada", "A geração do PDF foi cancelada.")
            return

        # Salva o PDF somente se a imagem existir
        if os.path.exists(imagem_path):
            imagem_para_pdf(imagem_path, pdf_path)
            QMessageBox.information(self, "PDF Salvo", f"PDF salvo com sucesso em:\n{pdf_path}")
        else:
            QMessageBox.warning(self, "Erro", f"Imagem do holerite não encontrada no caminho:\n{imagem_path}")

    def imprimir_holerite_preview_window(self):
        """Imprime o holerite que está sendo exibido na pré-visualização."""

        # Pega a imagem atualmente selecionada
        if 0 <= self.imagem_atual < len(self.imagens):
            holerite_selecionado = self.imagens[self.imagem_atual]
        else:
            QMessageBox.warning(self, "Erro", "Nenhum holerite selecionado.")
            return

        # Caminho da imagem selecionada
        caminho_imagem = os.path.join(self.assets_dir, holerite_selecionado)

        # Verifica se a imagem existe antes de imprimir
        if os.path.exists(caminho_imagem):
            try:
                imprimir_holerite(caminho_imagem, parent=self)
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Falha ao imprimir o holerite: {str(e)}")
        else:
            QMessageBox.warning(self, "Erro", "A imagem do holerite não foi encontrada.")


def abrir_previsualizacao():
    app = QApplication.instance() or QApplication(sys.argv)
    window = PreVisualizacaoHolerite()
    window.show()
    return window


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PreVisualizacaoHolerite()
    window.show()
    sys.exit(app.exec_())


# Developed by Raphael Soares dos Santos - Payslip Generator

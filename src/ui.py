"""
============================================================
  Payslip Generator/Gerador de Holerites
  Developed by: Raphael Soares dos Santos
  Creation Date: February 10, 2025
============================================================
"""

#import qdarkstyle
import ctypes
import os
os.environ["QT_API"] = "PyQt5"
from PyQt5.QtGui import QKeySequence, QIcon, QPixmap, QPainter, QMovie, QPainterPath, QRegion, QFont
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot, QUrl, QSize, QRect
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QMessageBox, QPushButton, QFileDialog, QShortcut, QSplashScreen,
    QMainWindow, QSizePolicy)
from src.form_layout import criar_formulario, atualizar_ui # Importa o formulário modularizado
from src.pdf_generator import FolhaA4Viewer
from src.calculos import calcular_fgts, calcular_irrf, atualizar_totais
from src.utils import (imagem_para_pdf, criar_pasta_temp, limpar_pasta_temp, obter_pasta_temp,
                       obter_caminho_area_de_trabalho, aplicar_escalonamento_dpi)
from src.preview_window import PreVisualizacaoHolerite, abrir_previsualizacao  # Nova janela de pré-visualização
from src.printer import imprimir_holerite
from datetime import datetime
import pyqtgraph as pg
import sys
import shutil
import time
import subprocess


ctypes.windll.shcore.SetProcessDpiAwareness(2)  # 2 = Per Monitor DPI Aware
base_dir = os.path.abspath(os.path.dirname(__file__))  # Caminho absoluto seguro
video_path = os.path.join(base_dir, "assets", "templates", "intro_sist_holerite.gif")


class VideoSplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.fator_escala = aplicar_escalonamento_dpi(self, debug=True)
        # Criar a pasta temporária antes do programa carregar
        self.temp_dir = criar_pasta_temp()
        print(f"📂 Pasta temporária criada: {self.temp_dir}")  # Debug para verificar a criação

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SplashScreen)  # Remove bordas e define como splash
        self.setAttribute(Qt.WA_TranslucentBackground)  # Torna a janela transparente

        # Definir o tamanho escalonado
        largura_base = 500
        altura_base = 500
        self.setGeometry(
            int(750 * self.fator_escala),  # Posição X
            int(250 * self.fator_escala),  # Posição Y
            int(largura_base * self.fator_escala),  # Largura
            int(altura_base * self.fator_escala)  # Altura
        )
        self.setMaximumSize(int(largura_base * self.fator_escala), int(altura_base * self.fator_escala))

        # Criar um QLabel para exibir a animação
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background: transparent; border-radius: 30px;")  # Aplica bordas arredondadas no QLabel

        # Criar uma máscara para arredondar a splash screen
        path = QPainterPath()
        path.addRoundedRect(10, 10, int(largura_base * self.fator_escala), int(altura_base * self.fator_escala), 100, 100)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

        # Verifica se o GIF existe
        if not os.path.exists(video_path):
            print(f"⚠️ ERRO: Arquivo de GIF não encontrado: {video_path}")
            self.abrir_janela_principal()
            return

        # Configurar QMovie para carregar e rodar o GIF
        self.movie = QMovie(video_path)
        self.movie.setScaledSize(QSize(int(largura_base * self.fator_escala), int(altura_base * self.fator_escala)))  # Ajusta o tamanho do GIF
        self.label.setMovie(self.movie)

        # Definir o layout e adicionar o QLabel
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Conectar o sinal para fechar a splash quando o GIF acabar
        self.movie.finished.connect(self.abrir_janela_principal)

        self.show()
        self.movie.start()  # Inicia a animação


    def abrir_janela_principal(self):
        """Fecha a splash e abre a interface principal."""
        self.close()
        self.main_app = HoleriteApp()
        self.main_app.show()

    def abrir_janela_principal(self):
        """Abre a interface do sistema após a animação."""
        self.main_app = HoleriteApp()
        self.main_app.show()


class HoleriteApp(QWidget):
    sinal_atualizar_calculos = pyqtSignal()  # Sinal que será emitido pelo form_layout.py

    def mousePressEvent(self, event):
        """Remove o foco de qualquer campo ao clicar fora, sem travamentos."""
        foco_atual = QApplication.focusWidget()
        if foco_atual and isinstance(foco_atual, QWidget):
            foco_atual.clearFocus()  # Remove o foco imediatamente
        super().mousePressEvent(event)


    def obter_dados_holerite(self):
        """
        Retorna os valores atualizados dos inputs para serem passados ao HoleriteGenerator.
        """
        return {
            "empresa_input": self.empresa_input,
            "endereco_input": self.endereco_input,
            "cnpj_input": self.cnpj_input,
            "codigo_input": self.codigo_input,
            "funcionario_input": self.funcionario_input,
            "funcao_input": self.funcao_input,
            "cbo_input": self.cbo_input,
            "fl_input": self.fl_input,
            "tipo_input": self.tipo_input,
            "referencia_input": self.referencia_input,
            "salario_input": self.salario_input,
            "salario_saida_copia": self.salario_saida_copia,
            "codigo_salario_input": self.codigo_salario_input,
            "sal_contr_inss_input": self.sal_contr_inss_input,
            "base_fgts_input": self.base_fgts_input,
            "valor_fgts_input": self.valor_fgts_input,
            "base_irrf_input": self.base_irrf_input,
            "data_emissao_input": self.data_emissao_input,
            "observacoes_input": self.observacoes_input,
            "total_vencimentos_label": self.total_vencimentos_label,
            "total_descontos_label": self.total_descontos_label,
            "valor_liquido_label": self.valor_liquido_label,
        }

    def __init__(self):
        super().__init__()
        # Agora `fator_escala` pertence à instância da classe
        self.fator_escala = aplicar_escalonamento_dpi(self)  # Sempre retorna um valor válido

        # Obter o caminho da pasta TEMP criada na intro
        self.temp_dir = obter_pasta_temp()
        self.init_ui()
        from src.holerite_generator import HoleriteDesign  # Importa a classe do gerador
        self.holerite_generator = HoleriteDesign(
            self)  # Passa a própria instância da interface, garantindo a comunicação
        self.holerite_generator.show()  # Abre a interface do holerite junto com a principal
        self.sinal_atualizar_calculos.connect(self.atualizar_calculos)
        self.pdf_viewer = FolhaA4Viewer()  # Instância do pdf_generator
        self.caminho_pdf = os.path.join(os.path.expanduser("~"), "Desktop")  # Área de Trabalho padrão
        self.preview_window = PreVisualizacaoHolerite(self)
        self.dados_anteriores = {}  # Armazena os dados antes de limpar

        # Criar atalho Ctrl + Z
        self.atalho_desfazer = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.atalho_desfazer.activated.connect(self.desfazer_limpeza)

    def init_ui(self):
        # Configuração inicial da janela
        self.setWindowTitle("Gerador de Holerites")

        # Caminho dinâmico para o ícone dentro de 'assets/icons'
        base_dir = os.path.abspath(os.path.dirname(__file__))  # Caminho absoluto seguro
        icon_path = os.path.join(base_dir, "assets", "icons", "Logo2_holerite_generator.ico")

        # Verifica se o ícone realmente existe
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))  # Aplica o ícone à janela principal
        else:
            print(f"⚠️ Aviso: Ícone não encontrado em {icon_path}")

        self.setGeometry(
            int(650 * self.fator_escala),  # Posição X
            int(100 * self.fator_escala),  # Posição Y
            int(728 * self.fator_escala),  # Largura
            int(840 * self.fator_escala)  # Altura
        )
        # Travar o tamanho para não redimensionar

        self.setMaximumSize(
            int(728 * self.fator_escala),
            int(785 * self.fator_escala)
        )

        # Layout principal
        main_layout = QVBoxLayout()

        # Título
        title_label = QLabel("Preencha os dados para gerar o holerite")
        font = QFont("Roboto", int(16 * self.fator_escala))
        font.setBold(True)  # Mantém o peso da fonte
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignCenter)  # Centraliza corretamente o texto
        main_layout.addWidget(title_label)

        # Formulário modularizado
        form_layout, entradas = criar_formulario(self)
        self.atualizar_ui = atualizar_ui
        main_layout.addLayout(form_layout)

        # Integração dos campos com a classe
        self.empresa_input = entradas["empresa_input"]
        self.endereco_input = entradas["endereco_input"]
        self.cnpj_input = entradas["cnpj_input"]
        self.codigo_input = entradas["codigo_input"]
        self.funcionario_input = entradas["funcionario_input"]
        self.funcao_input = entradas["funcao_input"]
        self.cbo_input = entradas["cbo_input"]
        self.fl_input = entradas["fl_input"]
        self.tipo_input = entradas["tipo_input"]
        self.referencia_input = entradas["referencia_input"]
        self.salario_input = entradas["salario_input"]
        self.salario_saida_copia = entradas["salario_saida_copia"]
        self.codigo_salario_input = entradas["codigo_salario_input"]
        self.descontos_input = entradas["descontos_input"]
        self.descricao_desconto_input = entradas["descricao_desconto_input"]
        self.codigo_desconto_input = entradas["codigo_desconto_input"]
        self.sal_contr_inss_input = entradas["sal_contr_inss_input"]
        self.base_fgts_input = entradas["base_fgts_input"]
        self.valor_fgts_input = entradas["valor_fgts_input"]
        self.base_irrf_input = entradas["base_irrf_input"]
        self.data_emissao_input = entradas["data_emissao_input"]
        self.observacoes_input = entradas["observacoes_input"]

        self.lista_descontos = entradas["lista_descontos"]

        self.total_vencimentos_label = entradas["totais"]["vencimentos"]
        self.total_descontos_label = entradas["totais"]["descontos"]
        self.valor_liquido_label = entradas["totais"]["liquido"]

        # Botões
        self.preview_button = entradas["botoes"]["preview"]
        self.preview_button.setText("Pré-visualizar Holerite")
        self.gerar_button = entradas["botoes"]["gerar"]
        self.limpar_button = entradas["botoes"]["limpar"]
        self.imprimir_button = entradas["botoes"]["imprimir"]

        self.preview_button.clicked.connect(self.abrir_previsualizacao)
        self.gerar_button.clicked.connect(self.gerar_holerite)
        self.imprimir_button.clicked.connect(self.imprimir_holerite_preview)
        self.limpar_button.clicked.connect(self.limpar_campos)
        self.lista_descontos_espelho = self.atualizar_ui()

        # Conectar atualizações automáticas
        self.salario_input.textChanged.connect(self.atualizar_calculos)

        # Configuração final
        self.setLayout(main_layout)

        self.empresa_input.textChanged.connect(self.notificar_holerite_generator)
        self.endereco_input.textChanged.connect(self.notificar_holerite_generator)
        self.cnpj_input.textChanged.connect(self.notificar_holerite_generator)
        self.codigo_input.valueChanged.connect(self.notificar_holerite_generator)
        self.funcionario_input.textChanged.connect(self.notificar_holerite_generator)
        self.funcao_input.textChanged.connect(self.notificar_holerite_generator)
        self.cbo_input.valueChanged.connect(self.notificar_holerite_generator)
        self.fl_input.valueChanged.connect(self.notificar_holerite_generator)
        self.tipo_input.currentIndexChanged.connect(self.notificar_holerite_generator)
        self.referencia_input.textChanged.connect(self.notificar_holerite_generator)
        self.salario_input.textChanged.connect(self.notificar_holerite_generator)
        self.salario_saida_copia.textChanged.connect(self.notificar_holerite_generator)
        self.codigo_salario_input.valueChanged.connect(self.notificar_holerite_generator)
        self.sal_contr_inss_input.textChanged.connect(self.notificar_holerite_generator)
        self.base_fgts_input.textChanged.connect(self.notificar_holerite_generator)
        self.valor_fgts_input.textChanged.connect(self.notificar_holerite_generator)
        self.base_irrf_input.textChanged.connect(self.notificar_holerite_generator)
        self.data_emissao_input.textChanged.connect(self.notificar_holerite_generator)
        self.observacoes_input.textChanged.connect(self.notificar_holerite_generator)



    def atualizar_calculos(self):
        """
        Atualiza os cálculos e chama a função para atualizar os totais na interface.
        """
        try:
            salario_text = self.salario_input.text().replace('.', '').replace(',', '.')
            salario = float(salario_text) if salario_text else 0.0

            total_descontos = 0.0
            total_vencimentos = 0.0

            # Identifica descontos e vencimentos separadamente
            for i in range(self.lista_descontos.count()):
                item = self.lista_descontos.item(i)
                item_data = item.data(Qt.UserRole)


                if isinstance(item_data, float):
                    # Se for um número, assumimos que é um desconto (comportamento antigo)
                    total_descontos += item_data
                elif isinstance(item_data, dict):
                    # Se for um dicionário, usamos os valores corretos
                    desconto_valor = float(item_data.get("desconto", 0.0))
                    vencimento_valor = float(item_data.get("vencimento", 0.0))

                    if desconto_valor > 0:
                        total_descontos += desconto_valor
                    if vencimento_valor > 0:
                        total_vencimentos += vencimento_valor

            salario_base = salario
            fgts = calcular_fgts(salario)
            irrf = calcular_irrf(salario, total_descontos)
            totais = atualizar_totais(salario + total_vencimentos, total_descontos, irrf['valor_irrf'])

            self.salario_saida_copia.setText(f"{salario_base:.2f}".replace('.', ','))
            self.sal_contr_inss_input.setText(f"{salario_base:.2f}".replace('.', ','))
            self.base_fgts_input.setText(f"{fgts['base_fgts']:.2f}".replace('.', ','))
            self.valor_fgts_input.setText(f"{fgts['valor_fgts']:.2f}".replace('.', ','))
            self.base_irrf_input.setText(f"{irrf['base_irrf']:.2f}".replace('.', ','))
            self.total_vencimentos_label.setText(f"{totais['total_vencimentos']:.2f}".replace('.', ','))
            self.total_descontos_label.setText(f"{totais['total_descontos']:.2f}".replace('.', ','))
            self.valor_liquido_label.setText(f"{totais['valor_liquido']:.2f}".replace('.', ','))
        except ValueError:
            pass


    def notificar_holerite_generator(self):
        """
        Notifica o HoleriteGenerator para atualizar a exibição quando um campo for alterado.
        """
        if self.holerite_generator:
            self.holerite_generator.update()

    def salvar_estado_anterior(self):
        """Salva todos os dados atuais antes de limpar o formulário."""
        self.dados_anteriores = {
            "empresa": self.empresa_input.text(),
            "endereco": self.endereco_input.text(),
            "cnpj": self.cnpj_input.text(),
            "codigo": self.codigo_input.value(),
            "funcionario": self.funcionario_input.text(),
            "funcao": self.funcao_input.text(),
            "cbo": self.cbo_input.value(),
            "fl": self.fl_input.value(),
            "tipo": self.tipo_input.currentIndex(),
            "referencia": self.referencia_input.text(),
            "salario": self.salario_input.text(),
            "salario_saida_copia": self.salario_saida_copia.text(),
            "codigo_salario": self.codigo_salario_input.value(),
            "descontos": self.descontos_input.text(),
            "descricao_desconto": self.descricao_desconto_input.text(),
            "codigo_desconto": self.codigo_desconto_input.value(),
            "sal_contr_inss": self.sal_contr_inss_input.text(),
            "base_fgts": self.base_fgts_input.text(),
            "valor_fgts": self.valor_fgts_input.text(),
            "base_irrf": self.base_irrf_input.text(),
            "data_emissao": self.data_emissao_input.text(),
            "observacoes": self.observacoes_input.toPlainText(),
            "total_vencimentos": self.total_vencimentos_label.text(),
            "total_descontos": self.total_descontos_label.text(),
            "valor_liquido": self.valor_liquido_label.text()
        }

    def limpar_campos(self):
        """Exibe um alerta antes de apagar os dados do formulário."""
        resposta = QMessageBox.question(
            self, "Confirmação",
            "Você tem certeza que deseja limpar todos os campos?\nEssa ação não pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            self.salvar_estado_anterior()  # Salva os dados antes de limpar
            self.empresa_input.clear()
            self.endereco_input.clear()
            self.cnpj_input.clear()
            self.funcionario_input.clear()
            self.funcao_input.clear()
            self.cbo_input.setValue(0)
            self.fl_input.setValue(0)
            self.tipo_input.setCurrentIndex(0)
            self.codigo_input.setValue(0)
            self.referencia_input.clear()
            self.salario_input.clear()
            self.salario_saida_copia.clear()
            self.codigo_salario_input.setValue(0)
            self.descontos_input.clear()
            self.descricao_desconto_input.clear()
            self.codigo_desconto_input.setValue(0)
            self.lista_descontos.clear()
            self.sal_contr_inss_input.clear()
            self.base_fgts_input.clear()
            self.valor_fgts_input.clear()
            self.base_irrf_input.clear()
            self.data_emissao_input.setText(datetime.now().strftime("%d/%m/%Y"))
            self.observacoes_input.clear()
            self.total_vencimentos_label.setText("0.00")
            self.total_descontos_label.setText("0.00")
            self.valor_liquido_label.setText("0.00")
        else:
            # Se o usuário clicar em "Não", não faz nada
            return

    def desfazer_limpeza(self):
        """Restaura os valores antes da limpeza."""
        if not self.dados_anteriores:
            QMessageBox.warning(self, "Erro", "Nenhum dado para restaurar.")
            return

        self.empresa_input.setText(self.dados_anteriores["empresa"])
        self.endereco_input.setText(self.dados_anteriores["endereco"])
        self.cnpj_input.setText(self.dados_anteriores["cnpj"])
        self.codigo_input.setValue(self.dados_anteriores["codigo"])
        self.funcionario_input.setText(self.dados_anteriores["funcionario"])
        self.funcao_input.setText(self.dados_anteriores["funcao"])
        self.cbo_input.setValue(self.dados_anteriores["cbo"])
        self.fl_input.setValue(self.dados_anteriores["fl"])
        self.tipo_input.setCurrentIndex(self.dados_anteriores["tipo"])
        self.referencia_input.setText(self.dados_anteriores["referencia"])
        self.salario_input.setText(self.dados_anteriores["salario"])
        self.salario_saida_copia.setText(self.dados_anteriores["salario_saida_copia"])
        self.codigo_salario_input.setValue(self.dados_anteriores["codigo_salario"])
        self.descontos_input.setText(self.dados_anteriores["descontos"])
        self.descricao_desconto_input.setText(self.dados_anteriores["descricao_desconto"])
        self.codigo_desconto_input.setValue(self.dados_anteriores["codigo_desconto"])
        self.sal_contr_inss_input.setText(self.dados_anteriores["sal_contr_inss"])
        self.base_fgts_input.setText(self.dados_anteriores["base_fgts"])
        self.valor_fgts_input.setText(self.dados_anteriores["valor_fgts"])
        self.base_irrf_input.setText(self.dados_anteriores["base_irrf"])
        self.data_emissao_input.setText(self.dados_anteriores["data_emissao"])
        self.observacoes_input.setPlainText(self.dados_anteriores["observacoes"])
        self.total_vencimentos_label.setText(self.dados_anteriores["total_vencimentos"])
        self.total_descontos_label.setText(self.dados_anteriores["total_descontos"])
        self.valor_liquido_label.setText(self.dados_anteriores["valor_liquido"])

        QMessageBox.information(self, "Restaurado", "Os dados foram restaurados com sucesso!")

    def gerar_holerite(self):
        if self.holerite_generator:
            # Atualiza a pré-visualização do holerite
            self.holerite_generator.update()
            # Aciona a função de salvar imagem do holerite
            self.holerite_generator.salvar_como_imagem()
            self.pdf_viewer.posicao_holerite_duplicado()
            self.gerar_pdf_do_holerite()

    def abrir_previsualizacao(self):
        """
        Ativa a funcionalidade do botão de pré-visualizar holerite,
        chamando a função de salvar imagem da interface do HoleriteGenerator.
        """
        if self.holerite_generator:
            self.holerite_generator.update()
            self.holerite_generator.salvar_como_imagem()
            self.pdf_viewer.posicao_holerite_duplicado()
            self.pdf_viewer.posicao_holerite_horizontal()
            self.pdf_viewer.posicao_holerite_vertical()

        # Obtém o caminho correto da pasta temporária
        temp_dir = obter_pasta_temp()

        """ Abre a janela de pré-visualização apenas se os arquivos existirem. """
        arquivos_necessarios = [
            "holerite_duplicado.png",
            "holerite_horizontal.png",
            "holerite_vertical.png"
        ]
        for arquivo in arquivos_necessarios:
            caminho = os.path.join(temp_dir, arquivo)  # Caminho atualizado
            if not os.path.exists(caminho):
                QMessageBox.warning(self, "Erro", f"O arquivo {arquivo} não foi gerado corretamente.")
                return  # Impede a abertura da janela se um arquivo estiver faltando

        """ Ativa a funcionalidade do botão de pré-visualizar holerite. """
        if hasattr(self, 'preview_window') and self.preview_window is not None:
            self.preview_window.close()
            QTimer.singleShot(200,
                              self.preview_window.deleteLater)  # Garante que a janela antiga foi apagada antes de abrir uma nova

        self.preview_window = PreVisualizacaoHolerite(
            parent_ui=self,
            funcionario=self.funcionario_input.text().strip(),
            empresa=self.empresa_input.text().strip()
        )
        self.preview_window.show()

    def gerar_pdf_do_holerite(self, *args, **kwargs):
        """Gera o PDF e permite que o usuário escolha o nome e local de salvamento."""

        # Obtém o caminho correto da pasta temporária
        temp_dir = obter_pasta_temp()
        # Caminho atualizado para a imagem do holerite
        imagem_path = os.path.join(temp_dir, "holerite_duplicado.png")
        # Caminho da Area de trabalho
        local_area = obter_caminho_area_de_trabalho()

        # Obtém os nomes do funcionário e empresa, se existirem
        funcionario = self.funcionario_input.text().strip()
        empresa = self.empresa_input.text().strip()

        # Define um nome padrão para o arquivo
        if funcionario:
            nome_padrao = f"holerite_{funcionario}"
        elif empresa:
            nome_padrao = f"holerite_{empresa}"
        else:
            nome_padrao = "holerite"

        # Substitui caracteres problemáticos no nome do arquivo
        nome_padrao = nome_padrao.replace(" ", "_").replace("/", "-").replace("\\", "-") + ".pdf"

        # Abre o seletor de arquivos para o usuário escolher onde salvar o PDF
        pdf_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Holerite",
            os.path.join(local_area, nome_padrao),
            "Arquivos PDF (*.pdf)"
        )

        # Se o usuário cancelar, interrompe a função
        if not pdf_path:
            QMessageBox.warning(self, "Ação Cancelada", "A geração do PDF foi cancelada.")
            return

        # Se a imagem do holerite existir, gera o PDF
        if os.path.exists(imagem_path):
            imagem_para_pdf(imagem_path, pdf_path)
            QMessageBox.information(self, "PDF Salvo", f"PDF salvo com sucesso em:\n{pdf_path}")
        else:
            QMessageBox.warning(self, "Erro", "Imagem do holerite não encontrada.")

    def imprimir_holerite_preview(self):
        """Envia o holerite duplicado para a impressora."""

        if self.holerite_generator:
            self.holerite_generator.update()
            self.holerite_generator.salvar_como_imagem()
            self.pdf_viewer.posicao_holerite_duplicado()

        # Obtém o caminho da pasta temporária
        temp_dir = obter_pasta_temp()

        # Atualiza o caminho da imagem para a pasta temp
        caminho_imagem = os.path.join(temp_dir, "holerite_duplicado.png")

        # Aguarda um curto intervalo para garantir que o arquivo foi salvo antes de imprimir
        QTimer.singleShot(500, lambda: (
            imprimir_holerite(caminho_imagem, parent=self)
            if os.path.exists(caminho_imagem)
            else QMessageBox.warning(self, "Erro", "A imagem do holerite não foi gerada corretamente.")
        ))


    def closeEvent(self, event):
        if hasattr(self, 'holerite_generator') and self.holerite_generator:
            self.holerite_generator.close()
            # Apagar a pasta TEMP ao sair
            limpar_pasta_temp()
            print(f"🗑️ Pasta temporária removida com sucesso: {self.temp_dir}")
            event.accept()

    '''
    def abrir_teste_previsualizacao(self):
        if not hasattr(self, 'preview_window') or self.preview_window is None:
            self.preview_window = abrir_previsualizacao()
            self.preview_window.show()
          '''


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    #window = HoleriteApp()
    #window.show()
    import os
    import shutil

    # Obtém o diretório base do script, compatível com .py e .exe
    base_dir = os.path.abspath(os.path.dirname(__file__))  # Caminho absoluto seguro
    video_path = os.path.join(base_dir, "assets", "templates", "intro_sist_holerite.gif")

    # Exibe a animação antes do sistema iniciar
    splash = VideoSplashScreen()
    splash.show()

    # Espera um tempo fixo antes de abrir a aplicação principal (ajustável)
    QTimer.singleShot(2300, splash.close)  # Fecha a splash após 3 segundos

    # Inicia a aplicação principal após o GIF
    QTimer.singleShot(2300, lambda: HoleriteApp().show())

    #app.aboutToQuit.connect(remover_imagens_preview)
    sys.exit(app.exec_())


# Developed by Raphael Soares dos Santos - Payslip Generator

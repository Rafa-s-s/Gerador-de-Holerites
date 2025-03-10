"""
============================================================
  Payslip Generator
  Developed by: Raphael Soares dos Santos
  Creation Date: February 10, 2025
============================================================
"""

import os
os.environ["QT_API"] = "PyQt5"
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QTimer
import sys
import tempfile
import re
from src.utils import (formatar_data_emissao, formatar_valor, quebrar_texto, formatar_cnpj, ajustar_texto_e_fonte,
                       formatar_valor_lista, obter_pasta_temp)
from src.form_layout import atualizar_ui
from src.ui import HoleriteApp  # Importando a classe correta


class HoleriteDesign(QMainWindow):

    def __init__(self, entradas):
        super().__init__()
        self.entradas = entradas
        self.initUI()
        self.lista_itens = self.obter_itens_lista_espelho()
        #print(f'lista {self.lista_itens}')

        # Parâmetros para controle do grupo mestre
        self.grupo_x = -55
        self.grupo_y = -695
        self.grupo_escala = 2.4

    def initUI(self):
        self.setWindowTitle("Pré-visualização do Holerite")
        self.setGeometry(100, 27, 1542, 979)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.template_label = QLabel(self)
        self.template_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.template_label)

        # Obtém o diretório base do script
        base_dir = os.path.abspath(os.path.dirname(__file__))
        # Caminho absoluto para a imagem da pré-visualização
        template_path = os.path.join(base_dir, "assets", "templates", "um_holerite_horizontal.png")

        self.pixmap = QPixmap(template_path)
        if self.pixmap.isNull():
            print(f"Erro: Não foi possível carregar a imagem no caminho: {template_path}")
        else:
            self.pixmap = self.pixmap.scaled(1549, 979, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.setCentralWidget(central_widget)
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_DontShowOnScreen)
        # QTimer.singleShot(500, self.salvar_como_imagem)  # Aguarda a interface carregar antes de salvar

    def obter_itens_lista_espelho(self):
        """
        Converte os itens da lista espelho em um dicionário estruturado,
        aplicando a formatação diretamente para exibição.
        """
        itens = []
        lista_espelho = atualizar_ui()  # Obtém a lista espelho atualizada

        for item_texto in lista_espelho:
            dicionario = {
                "codigo": "",
                "descricao": "",
                "desconto": "0,00",  # String formatada desde o início
                "vencimento": "0,00"  # String formatada desde o início
            }

            partes = item_texto.split(" | ")

            for parte in partes:
                chave_valor = parte.split(": ", 1)
                if len(chave_valor) == 2:
                    chave = chave_valor[0].strip()
                    valor = chave_valor[1].strip()

                    if chave == "Desconto":
                        try:
                            dicionario["desconto"] = formatar_valor_lista(valor.replace(',', '.'))
                        except ValueError:
                            print(f"Erro: Desconto inválido ({valor})")
                    elif chave == "Vencimento":
                        try:
                            dicionario["vencimento"] = formatar_valor_lista(valor.replace(',', '.'))
                        except ValueError:
                            print(f"Erro: Vencimento inválido ({valor})")
                    elif chave == "Descrição":
                        dicionario["descricao"] = valor
                    elif chave == "Código":
                        dicionario["codigo"] = int(valor) if valor.isdigit() else valor

            itens.append(dicionario)

        return itens


    def salvar_como_imagem(self):
        """
        Salva a interface do holerite como uma imagem PNG dentro da pasta temp.
        """
        # Obtém o caminho correto da pasta temporária
        temp_dir = obter_pasta_temp()

        # Caminho onde a imagem será salva
        save_path = os.path.join(temp_dir, "holerite_preview.png")

        # Renderiza e salva a imagem
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        pixmap.save(save_path, "PNG")

        # Verifica se a imagem foi salva corretamente
        if os.path.exists(save_path):
            print(f"✅ Holerite 'Preview' salvo com sucesso: {save_path}")
        else:
            print(f"⚠️ Erro: Não foi possível salvar a imagem em {save_path}")

        return save_path  # Retorna o caminho correto para outras funções usarem


    def paintEvent(self, event):
        #print("[Depuração] Executando paintEvent...")
        self.lista_itens = self.obter_itens_lista_espelho()
        #print("[Depuração] Lista de itens recebida:", self.lista_itens)  # Verifica a lista antes de usar
        self.update()  # Atualiza a interface sempre que um dado for modificado
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.drawPixmap(0, 0, self.pixmap)

        # Atualiza os dados ANTES de desenhar no holerite
        dados_atualizados = self.entradas.obter_dados_holerite()

        painter.setFont(QFont("Roboto", 7, QFont.Medium))
        painter.setPen(Qt.black)

        painter.translate(self.grupo_x, self.grupo_y)
        painter.scale(self.grupo_escala, self.grupo_escala)

        cnpj_text = formatar_cnpj(dados_atualizados["cnpj_input"].text().strip())
        cnpj_x, cnpj_y = 32, 308
        painter.drawText(cnpj_x, cnpj_y, cnpj_text.upper())

        empresa_text = dados_atualizados["empresa_input"].text().strip()
        empresa_x, empresa_y = 32, 321
        painter.drawText(empresa_x, empresa_y, empresa_text.upper())

        endereco_text = dados_atualizados["endereco_input"].text().strip()
        endereco_x, endereco_y = 32, 335
        painter.drawText(endereco_x, endereco_y, endereco_text.upper())

        data_emissao_text = formatar_data_emissao(dados_atualizados["data_emissao_input"].text().strip())
        data_emissao_x, data_emissao_y, data_width = 352, 315, 200
        painter.setFont(QFont("Roboto", 7, QFont.Bold))
        painter.drawText(data_emissao_x, data_emissao_y, data_width, 50, Qt.AlignRight, data_emissao_text.upper())

        codigo_text = str(dados_atualizados["codigo_input"].value()) if dados_atualizados[
                                                                            "codigo_input"].value() != 0 else ""
        codigo_x, codigo_y = 32, 367
        painter.setFont(QFont("Roboto", 7, QFont.Medium))
        painter.drawText(codigo_x, codigo_y, codigo_text.upper())

        nome_funcionario_text = dados_atualizados["funcionario_input"].text().strip()
        nome_funcionario_x, nome_funcionario_y = 67, 367
        painter.drawText(nome_funcionario_x, nome_funcionario_y, nome_funcionario_text.upper())

        # Obtém o texto da função
        funcao_text = dados_atualizados["funcao_input"].text().strip()
        funcao_x, funcao_y_base = 346, 372
        largura_maxima_funcao = 100  # Define a largura máxima disponível

        # Obtém as linhas ajustadas, tamanho da fonte e deslocamento vertical
        linhas_funcao, tamanho_fonte_ajustado, deslocamento_vertical = ajustar_texto_e_fonte(
            painter, funcao_text, largura_maxima_funcao
        )

        # Define a fonte ajustada para a função
        painter.setFont(QFont("Roboto", tamanho_fonte_ajustado, QFont.Medium))

        # Ajusta a posição inicial para expandir para cima e para baixo
        funcao_y = funcao_y_base - deslocamento_vertical

        # Desenha as linhas ajustadas
        for i, linha in enumerate(linhas_funcao):
            painter.drawText(funcao_x, funcao_y + (i * 7), linha.upper())

        # RESTAURA A FONTE ORIGINAL para não afetar outros campos
        painter.setFont(QFont("Roboto", 7, QFont.Medium))

        # Obtém o texto da opção selecionada
        tipo_text = dados_atualizados["tipo_input"].currentText()

        # Define as coordenadas padrão (adicione as posições desejadas)
        tipo_x, tipo_y = 477, 367  # Substitua com as coordenadas corretas

        # Se for 'N/A', deixa vazio (invisível no holerite)
        tipo_text = "" if tipo_text == "N/A" else tipo_text

        # Desenha o texto (apenas se não for vazio)
        if tipo_text:
            painter.drawText(tipo_x, tipo_y, tipo_text.upper())

        # Ajustando a posição do CBO para crescer para os dois lados
        cbo_text = str(dados_atualizados["cbo_input"].value()) if dados_atualizados["cbo_input"].value() != 0 else ""
        painter.setFont(QFont("Roboto", 7, QFont.Medium))

        # Calcula a largura real do texto
        metrics = QFontMetrics(painter.font())
        largura_texto_cbo = metrics.width(cbo_text)

        # Define a posição centralizada
        cbo_x_centro = 515  # Posição central original
        cbo_x = cbo_x_centro - (largura_texto_cbo // 2)  # Ajuste para centralizar
        cbo_y = 367

        painter.drawText(cbo_x, cbo_y, cbo_text.upper())

        # Ajustando a posição do FL para crescer para os dois lados
        fl_text = str(dados_atualizados["fl_input"].value()) if dados_atualizados["fl_input"].value() != 0 else ""
        painter.setFont(QFont("Roboto", 7, QFont.Medium))

        # Calcula a largura real do texto
        metrics = QFontMetrics(painter.font())
        largura_texto_fl = metrics.width(fl_text)

        # Define a posição centralizada
        fl_x_centro = 548  # Posição central original
        fl_x = fl_x_centro - (largura_texto_fl // 2)  # Ajuste para centralizar
        fl_y = 367

        painter.drawText(fl_x, fl_y, fl_text.upper())

        salario_base_text = formatar_valor(dados_atualizados["salario_saida_copia"].text().strip())
        salario_base_x, salario_base_y = 50, 689
        painter.drawText(salario_base_x, salario_base_y, salario_base_text.upper())

        if salario_base_text:
            salario_base_venc_x, salario_base_venc_y = 368, 412
            painter.drawText(salario_base_venc_x, salario_base_venc_y, salario_base_text.upper())

            codigo_salario_base = str(dados_atualizados["codigo_salario_input"].value()) if dados_atualizados[
                                                                                                "codigo_salario_input"].value() != 0 else ""
            codigo_salario_x, codigo_salario_y = 28, 412
            painter.drawText(codigo_salario_x, codigo_salario_y, codigo_salario_base.upper())

            descricao_salario_base = "SALÁRIO BASE"
            descricao_salario_x, descricao_salario_y = 63, 412
            painter.drawText(descricao_salario_x, descricao_salario_y, descricao_salario_base.upper())

        referencia_text = dados_atualizados["referencia_input"].text().strip()
        referencia_x, referencia_y = 313, 412
        painter.drawText(referencia_x, referencia_y, referencia_text.upper())

        item_y_base = 424

        for item in self.lista_itens:
            try:
                codigo = str(item.get("codigo", "")).upper()
                descricao = item.get("descricao", "").upper()

                desconto = formatar_valor_lista(item.get("desconto", ""))
                vencimento = formatar_valor_lista(item.get("vencimento", ""))

                codigo_x, codigo_y = 28, item_y_base
                descricao_x, descricao_y = 64, item_y_base
                desconto_x, desconto_y = 465, item_y_base
                vencimento_x, vencimento_y = 368, item_y_base

                painter.drawText(codigo_x, codigo_y, codigo)
                painter.drawText(descricao_x, descricao_y, descricao)
                painter.drawText(vencimento_x, vencimento_y, vencimento)
                painter.drawText(desconto_x, desconto_y, desconto)

                item_y_base += 12
            except ValueError as e:
                print(f"Erro ao processar item: {e} (valor inválido)")
            except Exception as e:
                print(f"Erro inesperado ao processar item: {e}")


        total_venc_text = formatar_valor(dados_atualizados["total_vencimentos_label"].text().strip())

        painter.setFont(QFont("Roboto", 7, QFont.Medium))
        metrics = QFontMetrics(painter.font())
        largura_texto_venc = metrics.width(total_venc_text)

        venc_x_centro = 411
        total_venc_x = venc_x_centro - (largura_texto_venc // 2)  # Ajuste para centralizar
        total_venc_y = 624

        painter.drawText(total_venc_x, total_venc_y, total_venc_text.upper())

        total_desc_text = formatar_valor(dados_atualizados["total_descontos_label"].text().strip())

        painter.setFont(QFont("Roboto", 7, QFont.Medium))
        metrics = QFontMetrics(painter.font())
        largura_texto_desc = metrics.width(total_desc_text)

        desc_x_centro = 510
        total_desc_x = desc_x_centro - (largura_texto_desc // 2)  # Ajuste para centralizar
        total_desc_y = 624

        painter.drawText(total_desc_x, total_desc_y, total_desc_text.upper())

        inss_text = formatar_valor(dados_atualizados["sal_contr_inss_input"].text().strip())  # <--- Sal.contr. INSS
        inss_x, inss_y = 162, 689
        painter.drawText(inss_x, inss_y, inss_text.upper())

        fgts_calc_text = formatar_valor(dados_atualizados["base_fgts_input"].text().strip())
        fgts_calc_x, fgts_calc_y = 275, 689
        painter.drawText(fgts_calc_x, fgts_calc_y, fgts_calc_text.upper())

        fgts_mes_text = formatar_valor(dados_atualizados["valor_fgts_input"].text().strip())
        fgts_mes_x, fgts_mes_y = 390, 689
        painter.drawText(fgts_mes_x, fgts_mes_y, fgts_mes_text.upper())

        # Ajustando a posição da Base de Cálculo IRRF para crescer para os dois lados
        irrf_text = formatar_valor(dados_atualizados["base_irrf_input"].text().strip())
        painter.setFont(QFont("Roboto", 7, QFont.Medium))

        # Calcula a largura real do texto
        metrics = QFontMetrics(painter.font())
        largura_texto_irrf = metrics.width(irrf_text)

        # Define a posição centralizada
        irrf_x_centro = 515  # Posição central original
        irrf_x = irrf_x_centro - (largura_texto_irrf // 2)  # Ajuste para centralizar
        irrf_y = 689

        painter.drawText(irrf_x, irrf_y, irrf_text.upper())

        observacoes_text = dados_atualizados[
            "observacoes_input"].toPlainText().strip() if self.entradas.observacoes_input.toPlainText() else ""
        observacoes_x, observacoes_y = 29, 613
        linhas_observacoes = quebrar_texto(observacoes_text, 200)  # Ajuste a largura conforme necessário
        for i, linha in enumerate(linhas_observacoes):
            painter.drawText(observacoes_x, observacoes_y + (i * 12), linha.upper())

        # Ajustando a posição do valor líquido para crescer para os dois lados
        valor_liquido_text = formatar_valor(dados_atualizados["valor_liquido_label"].text())
        painter.setFont(QFont("Roboto", 9, QFont.Bold))

        # Calcula a largura real do texto
        metrics = QFontMetrics(painter.font())
        largura_texto = metrics.width(valor_liquido_text)

        # Define a posição centralizada
        valor_liquido_x_centro = 510  # Posição central original
        valor_liquido_x = valor_liquido_x_centro - (largura_texto // 2)  # Ajuste para centralizar
        valor_liquido_y = 654

        painter.drawText(valor_liquido_x, valor_liquido_y, valor_liquido_text.upper())

        painter.end()


    # def mousePressEvent(self, event):
    #    x, y = event.x(), event.y()
    #    print(f"Coordenadas do clique: x={x}, y={y}")


def main():
    app = QApplication(sys.argv)
    app_instance = HoleriteApp()
    main_window = HoleriteDesign(app_instance)
    #main_window.show()
    sys.exit(app.exec_())  # Garante que a aplicação continue rodando


if __name__ == '__main__':
    main()


# Developed by Raphael Soares dos Santos - Payslip Generator

"""
============================================================
  Payslip Generator
  Developed by: Raphael Soares dos Santos
  Creation Date: February 10, 2025
============================================================
"""

import os
os.environ["QT_API"] = "PyQt5"

from datetime import datetime
from PyQt5.QtWidgets import QWidget


def formatar_data_emissao(data):
    """
    Formata a data de emissão para o formato "MÊS / ANO" se for uma string de data válida.
    Caso contrário, retorna a string diretamente.
    """
    meses = [
        "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO",
        "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"
    ]
    try:
        # Tenta converter para o formato desejado
        dt = datetime.strptime(data, "%d/%m/%Y")
        return f"{meses[dt.month - 1]} / {dt.year}"
    except ValueError:
        # Se não for possível converter, retorna a string como está
        return data



import re

def formatar_valor_lista(valor: str) -> str:
    try:
        # Remove caracteres inválidos
        valor = re.sub(r'[^\d.,]', '', valor).strip()

        # Caso especial: Permitir livre entrada até formar milhar ('1.0' => '1.0', mas '1.000' => '1.000,00')
        if re.match(r'^\d+\.\d*$', valor) and len(valor.split('.')[1]) < 3:
            return valor.replace('.', ',')

        # Quando atingir milhar ('1.000'), aplica formatação
        if re.match(r'^\d{1,3}\.\d{3}$', valor):
            numero = float(valor.replace('.', ''))
            return f"{numero:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

        # Ajuste para múltiplos pontos ('1.00000', '1.000.00')
        if valor.count('.') > 1:
            partes = valor.split('.')
            if all(len(p) == 3 for p in partes[1:-1]):
                valor = valor.replace('.', '', len(partes) - 2)
            else:
                return "Inválido"

        # Validação para múltiplos pontos em posições erradas
        if re.search(r'\d+\.\d+\.\d+', valor) and ',' not in valor:
            return "Inválido"

        # Tratamento padrão brasileiro (milhar com ponto, decimal com vírgula)
        if ',' in valor and '.' in valor:
            if valor.rfind(',') > valor.rfind('.'):
                valor = valor.replace('.', '').replace(',', '.')
            else:
                return "Inválido"
        elif ',' in valor:
            valor = valor.replace(',', '.')

        # Conversão e formatação padrão brasileiro
        numero = float(valor) if valor else 0.0
        return f"{numero:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if numero != 0 else ""
    except ValueError:
        return "Inválido"



import re

def formatar_valor(valor: str) -> str:
    try:
        # Remove caracteres inválidos
        valor = re.sub(r'[^\d.,-]', '', valor).strip()

        # Permite exibir livremente até formar milhar, incluindo zero ('0.0' => '0,0')
        if re.match(r'^-?\d+\.\d*$', valor) and len(valor.split('.')[1]) < 3:
            return valor.replace('.', ',')

        # Aceita valores negativos e exibe zero corretamente
        if re.match(r'^-?\d{1,3}(\.\d{3})*$', valor):
            numero = float(valor.replace('.', '').replace(',', '.'))
            return f"{numero:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

        # Ajuste para múltiplos pontos ('-1.00000')
        if valor.count('.') > 1:
            partes = valor.split('.')
            if all(len(p) == 3 for p in partes[1:-1]):
                valor = valor.replace('.', '', len(partes) - 2)
            else:
                return "Inválido"

        # Tratamento padrão brasileiro (milhar com ponto, decimal com vírgula)
        if ',' in valor and '.' in valor:
            if valor.rfind(',') > valor.rfind('.'):
                valor = valor.replace('.', '').replace(',', '.')
            else:
                return "Inválido"
        elif ',' in valor:
            valor = valor.replace(',', '.')

        # Conversão e formatação padrão brasileiro com preservação de zero
        numero = float(valor) if valor else 0.0
        return f"{numero:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except ValueError:
        return "Inválido"


#print(f"Teste M (100000,00): {formatar_valor('100000,00')} - Esperado: 100.000,00")



from PyQt5.QtGui import QFont, QFontMetrics


def quebrar_texto(texto, largura_maxima, fonte=QFont("Roboto", 7, QFont.Medium)):
    """
    Quebra o texto em várias linhas de acordo com a largura real das palavras.

    Parâmetros:
        - texto: str -> O texto que será quebrado em múltiplas linhas.
        - largura_maxima: int -> A largura máxima permitida antes da quebra de linha.
        - fonte: QFont -> Fonte usada para medir o tamanho das palavras.

    Retorna:
        - list[str] -> Lista de linhas ajustadas ao limite de largura.
    """
    if not texto:
        return [""]

    metrics = QFontMetrics(fonte)
    palavras = texto.split()
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        largura_linha_atual = metrics.width(linha_atual + " " + palavra) if linha_atual else metrics.width(palavra)

        if largura_linha_atual <= largura_maxima:
            linha_atual += (" " if linha_atual else "") + palavra
        else:
            linhas.append(linha_atual)
            linha_atual = palavra

    if linha_atual:
        linhas.append(linha_atual)

    return linhas


import random

def calcular_identificador_aleatorio(dados):
    """
    Algoritmo dinâmico para validação de registros criptográficos.
     Utiliza transformações matemáticas para evitar corrupção de dados.

    Parâmetros:
    - dados (str): Entrada de dados a ser analisada.

     Retorna:
     - int: Identificador gerado dinamicamente com base no conjunto de entrada.
     """
    ruido = ["0xFA", "0x2B", "0x91", "0x7C", str(random.randint(100, 999))]
    return sum(ord(c) for c in dados + "".join(ruido)) % 512


from PyQt5.QtGui import QFontMetrics, QFont

def ajustar_texto_e_fonte(painter, texto, largura_maxima, font_size_inicial=7, min_font_size=5):
    """
    Ajusta dinamicamente o tamanho da fonte e quebra linhas conforme necessário para caber no espaço disponível.
    Agora também ajusta a posição vertical do texto para expandir para cima e para baixo ao mesmo tempo.

    :param painter: Objeto QPainter usado para medir o texto.
    :param texto: String do texto a ser ajustado.
    :param largura_maxima: Largura máxima disponível para desenhar o texto.
    :param font_size_inicial: Tamanho inicial da fonte.
    :param min_font_size: Tamanho mínimo permitido para a fonte.
    :return: Lista de linhas formatadas, tamanho de fonte ajustado e deslocamento vertical.
    """
    font = painter.font()
    font.setPointSize(font_size_inicial)
    painter.setFont(font)
    metrics = QFontMetrics(font)

    # Tenta ajustar a fonte reduzindo até que caiba na largura máxima
    while metrics.width(texto) > largura_maxima and font.pointSize() > min_font_size:
        font.setPointSize(font.pointSize() - 1)
        painter.setFont(font)
        metrics = QFontMetrics(font)

    # Agora faz a quebra de linha conforme o novo tamanho da fonte
    palavras = texto.split()
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        if metrics.width(linha_atual + " " + palavra) <= largura_maxima:
            linha_atual += (" " if linha_atual else "") + palavra
        else:
            linhas.append(linha_atual)
            linha_atual = palavra

    if linha_atual:
        linhas.append(linha_atual)

    # Calcula o deslocamento vertical para expandir para cima e para baixo
    altura_total_texto = len(linhas) * metrics.height()
    deslocamento_vertical = altura_total_texto // 2  # Centraliza o texto verticalmente

    return linhas, font.pointSize(), deslocamento_vertical


CONFIG = {
    "version": "1.0.0",
    "author": "5261706861656c20536f6172657320646f732053616e746f73"
}

def aplicar_zoom(widget: QWidget, valor_zoom: int):
    """
    Aplica zoom em um widget redimensionando sua escala com base no valor de zoom.
    O valor de zoom varia de 50 (50%) a 200 (200%).
    """
    escala = valor_zoom / 100.0
    largura_original = 800  # Defina o tamanho base da interface
    altura_original = 600
    nova_largura = int(largura_original * escala)
    nova_altura = int(altura_original * escala)
    widget.setFixedSize(nova_largura, nova_altura)



import re

def formatar_cnpj(cnpj):
    """
    Formata um CNPJ inserido pelo usuário para o formato correto XX.XXX.XXX/XXXX-XX.
    Remove caracteres inválidos, permite a visualização progressiva do CNPJ e mantém a formatação parcial.
    """
    # Remover todos os caracteres que não são números
    cnpj_limpo = re.sub(r"\D", "", cnpj)

    # Aplicando formatação progressiva
    if len(cnpj_limpo) >= 3:
        cnpj_formatado = f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}"
    else:
        cnpj_formatado = cnpj_limpo[:2]

    if len(cnpj_limpo) >= 6:
        cnpj_formatado += f".{cnpj_limpo[5:8]}"
    if len(cnpj_limpo) >= 9:
        cnpj_formatado += f"/{cnpj_limpo[8:12]}"
    if len(cnpj_limpo) >= 13:
        cnpj_formatado += f"-{cnpj_limpo[12:14]}"

    return cnpj_formatado



from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import sys
import platform
import shutil

def obter_caminho_area_de_trabalho():
    """Retorna o caminho da Área de Trabalho do usuário, compatível com Windows, Linux e macOS."""
    sistema = platform.system()

    if sistema == "Windows":
        return os.path.join(os.path.expanduser("~"), "Desktop")
    elif sistema == "Darwin":  # macOS
        return os.path.join(os.path.expanduser("~"), "Desktop")
    elif sistema == "Linux":
        return os.path.join(os.path.expanduser("~"), "Área de Trabalho")  # Linux em português
    else:
        return os.path.expanduser("~")  # Caso não reconheça o SO, salva na home do usuário



from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
import os
from PIL import Image

def imagem_para_pdf(imagem_path, pdf_path):
    """
    Converte uma imagem em um arquivo PDF em alta qualidade,
    com ajuste automático para paisagem ou retrato.
    """
    try:
        if not pdf_path:
            print("Operação cancelada. PDF não foi gerado.")
            return

        with Image.open(imagem_path) as img:
            img = img.convert('RGB')  # Remove canais alfa para evitar erros
            img_largura, img_altura = img.size

            # Ajuste da qualidade de renderização (Redimensionamento otimizado)
            if img_largura > 3508 or img_altura > 2480:  # Maior que A4 em pixels a 300dpi
                img = img.resize((3508, 2480), Image.Resampling.LANCZOS)

            # Define a orientação da página (paisagem ou retrato)
            pagina = landscape(A4) if img_largura > img_altura else A4
            largura, altura = pagina

            proporcao = min(largura / img_largura, altura / img_altura)
            nova_largura = img_largura * proporcao
            nova_altura = img_altura * proporcao

            # Centraliza
            x = (largura - nova_largura) / 2
            y = (altura - nova_altura) / 2

            c = canvas.Canvas(pdf_path, pagesize=pagina)
            c.drawImage(
                imagem_path, x, y,
                width=nova_largura, height=nova_altura,
                preserveAspectRatio=True,
                mask='auto'
            )
            c.showPage()
            c.save()

        print(f"PDF salvo com sucesso em: {pdf_path}")
    except Exception as e:
        print(f"Erro ao gerar o PDF: {e}")


import os
import tempfile
import shutil
import uuid

# Criar um nome único para a pasta TEMP do sistema
TEMP_DIR = os.path.join(tempfile.gettempdir(), f"holerite_{uuid.uuid4().hex[:8]}")

def criar_pasta_temp():
    """Cria a pasta temporária se ela ainda não existir e retorna o caminho."""
    os.makedirs(TEMP_DIR, exist_ok=True)
    return TEMP_DIR

def obter_pasta_temp():
    """Retorna o caminho da pasta temporária"""
    return TEMP_DIR

def limpar_pasta_temp():
    """Remove a pasta temporária e todo o seu conteúdo."""
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR, ignore_errors=True)


import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QSpinBox, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Habilita o escalonamento global do PyQt5 baseado no DPI do sistema
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

def is_notebook():
    """Verifica se o dispositivo é um notebook baseado na presença de bateria."""
    battery = psutil.sensors_battery()
    return battery is not None  # Se houver bateria, é um notebook

def aplicar_escalonamento_dpi(janela, debug=False):
    """
    Aplica um escalonamento global à interface com base no DPI do monitor.
    - Se for um notebook, ajusta a escala para evitar interfaces gigantes.
    - Mantém o DPI mínimo em 70, mas sem limite superior.
    - Se DPI < 75, a fonte não reduz além do tamanho de 75 DPI para evitar ilegibilidade.
    - Se houver erro, define o DPI como 80.
    """
    try:
        screen = QApplication.primaryScreen()
        dpi = screen.physicalDotsPerInch()
        #dpi = 70

        # Se o DPI for inválido (None ou zero), define 80
        if dpi is None or dpi == 0:
            raise ValueError("DPI inválido detectado")

    except Exception as e:
        dpi = 80  # Define 80 se houver erro
        if debug:
            print(f"⚠️ Erro ao obter DPI: {e}. Aplicando valor padrão: {dpi}")

    # Ajuste especial para notebooks (simula DPI menor para evitar exageros)
    if is_notebook():
        dpi = max(70, dpi * (70 / 105))  # Considera 105 DPI como 70 DPI para notebooks

    else:
        dpi = max(70, dpi)  # Mantém o DPI normal para PCs, sem limite superior

    fator_escala = dpi / 96  # Fator de escala final

    # GARANTIA DE FONTE LEGÍVEL: Se DPI < 75, usa o fator de 75 para fontes
    fator_fonte = max(75 / 96, fator_escala)  # Fonte nunca será menor que a de 75 DPI

    # Exibe apenas se debug=True
    if debug:
        print(f"🖥️ Notebook: {is_notebook()}, DPI ajustado: {dpi:.2f}, "
              f"Fator de escala: {fator_escala:.3f}, Fator de fonte: {fator_fonte:.3f}")

    # Ajuste global de fonte
    def ajustar_fonte(tamanho):
        return QFont("Roboto", int(tamanho * fator_fonte))  # Usa fator de fonte ajustado

    janela.setFont(ajustar_fonte(9.5))

    # Ajusta o tamanho e fonte dos widgets corretamente
    for widget in janela.findChildren(QWidget):
        font = widget.font()
        font.setPointSizeF(font.pointSizeF() * fator_fonte)  # Usa fator de fonte para manter legibilidade
        widget.setFont(font)

        # Ajusta os botões internos do QSpinBox e QComboBox
        if isinstance(widget, (QSpinBox, QComboBox)):
            widget.setFixedHeight(int(30 * fator_escala))
            widget.setStyleSheet(f"""
                {widget.__class__.__name__} {{
                    height: {int(30 * fator_escala)}px;
                    font-size: {int(10 * fator_fonte)}px; /* Usa fator de fonte */
                }}
            """)

    # Exibe apenas se debug=True
    if debug:
        print("✅ Escala aplicada com sucesso.")

    return fator_escala


# Developed by Raphael Soares dos Santos - Payslip Generator

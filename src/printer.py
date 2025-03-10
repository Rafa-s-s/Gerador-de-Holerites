"""
============================================================
  Payslip Generator
  Developed by: Raphael Soares dos Santos
  Creation Date: February 10, 2025
============================================================
"""

import os
os.environ["QT_API"] = "PyQt5"
from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QPainter, QPixmap, QTransform
from PyQt5.QtWidgets import QMessageBox
from PIL import Image

def imprimir_holerite(caminho_imagem, parent=None):
    """
    Função para imprimir a imagem do holerite com qualidade máxima.
    Caso a imagem esteja na horizontal, ela será rotacionada para impressão.

    :param caminho_imagem: Caminho da imagem do holerite gerado.
    :param parent: Janela principal que chama a função (para exibir diálogos).
    """
    printer = QPrinter(QPrinter.HighResolution)
    printer.setPageSize(QPrinter.A4)

    # Permitir que o usuário escolha a impressora
    dialog = QPrintDialog(printer, parent)
    if dialog.exec_() != QPrintDialog.Accepted:
        return  # Usuário cancelou a impressão

    # Criar um pintor para desenhar no documento de impressão
    painter = QPainter(printer)
    pixmap = QPixmap(caminho_imagem)

    if pixmap.isNull():
        QMessageBox.warning(parent, "Erro", "Não foi possível carregar a imagem para impressão.")
        return

    # Obtém as dimensões reais da imagem
    with Image.open(caminho_imagem) as img:
        img_largura, img_altura = img.size

    # Dimensões da página
    largura_pagina = printer.pageRect().width()
    altura_pagina = printer.pageRect().height()

    # Se a imagem for mais larga que alta (modo paisagem), rotaciona
    if img_largura > img_altura:
        transform = QTransform()
        transform.rotate(90)  # Gira a imagem 90 graus para impressão correta
        pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)

    # Ajustar a imagem para preencher a página corretamente
    proporcao = min(largura_pagina / pixmap.width(), altura_pagina / pixmap.height())
    nova_largura = int(pixmap.width() * proporcao)
    nova_altura = int(pixmap.height() * proporcao)

    # Centraliza a imagem na folha
    x = (largura_pagina - nova_largura) // 2
    y = (altura_pagina - nova_altura) // 2

    # Desenha a imagem na folha
    painter.drawPixmap(x, y, nova_largura, nova_altura, pixmap)
    painter.end()  # Finaliza a impressão


# Developed by Raphael Soares dos Santos - Payslip Generator

"""
============================================================
  Payslip Generator
  Developed by: Raphael Soares dos Santos
  Creation Date: February 10, 2025
============================================================
"""
# P1--------------------------------------------------------------------------------
import os
os.environ["QT_API"] = "PyQt5"
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QHBoxLayout, QLabel, QSpinBox, QComboBox, QTextEdit, QVBoxLayout, \
    QPushButton, QFrame, QListWidget, QListWidgetItem, QWidget, QMessageBox, QSpacerItem, QSizePolicy, \
    QAbstractItemView, QApplication, QStyle
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QPalette, QIcon, QFont
from datetime import datetime
from src.utils import aplicar_escalonamento_dpi  # Importa a função de escalonamento


def criar_formulario(app_ref):
    """
    Função para criar o layout do formulário de entrada de dados.
    Retorna o layout do formulário e os widgets associados.
    """
    fator_escala = app_ref.fator_escala  # Obtém o fator de escala da aplicação principal

    global lista_descontos_espelho
    global lista_descontos

    # Definir o caminho do ícone da impressora
    base_dir = os.path.abspath(os.path.dirname(__file__))  # Caminho absoluto seguro
    icon_print_path = os.path.join(base_dir, "assets", "templates", "img_printer.png")

    form_layout = QFormLayout()

    # Informações da Empresa
    empresa_input = QLineEdit()
    empresa_input.setFixedWidth(int(580 * fator_escala))  # largura
    empresa_input.setFixedHeight(int(22 * fator_escala))  # altura
    empresa_input.setPlaceholderText("Ex: Empresa XYZ Ltda")
    empresa_input.setMaxLength(50)  # Limite de 50 caracteres

    endereco_input = QLineEdit()
    endereco_input.setFixedWidth(int(580 * fator_escala))  # largura
    endereco_input.setFixedHeight(int(22 * fator_escala))  # altura
    endereco_input.setPlaceholderText("Ex: Rua das Flores, 123")
    endereco_input.setMaxLength(80)  # Limite de 70 caracteres

    cnpj_input = QLineEdit()
    cnpj_input.setFixedWidth(int(180 * fator_escala))  # largura
    cnpj_input.setFixedHeight(int(22 * fator_escala))  # altura
    cnpj_input.setPlaceholderText("Ex: 00.000.000/0000-00")
    cnpj_input.setMaxLength(18)  # O formato correto do CNPJ tem 18 caracteres

    form_layout.addRow("Nome da Empresa:", empresa_input)
    form_layout.addRow("Endereço da Empresa:", endereco_input)
    form_layout.addRow("CNPJ:", cnpj_input)

    # Informações do Funcionário
    codigo_input = QSpinBox()
    codigo_input.setSpecialValueText(" ")  # Faz com que 0 pareça vazio
    codigo_input.setRange(0, 999999)  # Permite valores de 0 a 99999
    codigo_input.setFixedWidth(int(80 * fator_escala))  # largura
    codigo_input.setFixedHeight(int(22 * fator_escala))  # altura
    codigo_hint = QLabel("Código (ID) do Funcionário.")

    funcionario_input = QLineEdit()
    funcionario_input.setFixedWidth(int(180 * fator_escala))  # largura
    funcionario_input.setFixedHeight(int(22 * fator_escala))  # altura
    funcionario_input.setPlaceholderText("Ex: João da Silva")
    funcionario_input.setMaxLength(40)  # Nome do funcionário limitado a 40 caracteres

    funcao_input = QLineEdit()
    funcao_input.setFixedWidth(int(180 * fator_escala))  # largura
    funcao_input.setFixedHeight(int(22 * fator_escala))  # altura
    funcao_input.setPlaceholderText("Ex: Analista de Sistemas")
    funcao_input.setMaxLength(40)  # Limite da função para 40 caracteres

    cbo_input = QSpinBox()
    cbo_input.setSpecialValueText(" ")  # Faz com que 0 pareça vazio
    cbo_input.setRange(0, 999999)
    cbo_input.setSpecialValueText(" ")  # Faz com que 0 pareça vazio
    cbo_input.setFixedWidth(int(80 * fator_escala))  # largura
    cbo_input.setFixedHeight(int(22 * fator_escala))  # altura
    cbo_hint = QLabel("(CBO) Código Brasileiro de Ocupações.")

    fl_input = QSpinBox()
    fl_input.setSpecialValueText(" ")  # Faz com que 0 pareça vazio
    fl_input.setRange(0, 9999)
    fl_input.setSpecialValueText(" ")  # Faz com que 0 pareça vazio
    fl_input.setFixedWidth(int(80 * fator_escala))  # largura
    fl_input.setFixedHeight(int(22 * fator_escala))  # altura
    fl_hint = QLabel("(Fl) Numeração da Folha.")



    tipo_input = QComboBox()
    tipo_input.addItems(["M", "F", "N/A"])
    tipo_input.setFixedWidth(int(80 * fator_escala))  # largura
    tipo_input.setFixedHeight(int(22 * fator_escala))  # altura
    tipo_hint = QLabel("(M) para Masculino, (F) para Feminino.")

    # Layouts para campos compactos
    '''
    codigo_layout = QHBoxLayout()
    codigo_layout.addWidget(codigo_input)
    codigo_layout.addWidget(codigo_hint)'''


    cbo_fl_layout = QHBoxLayout()
    cbo_fl_layout.addWidget(cbo_input)
    cbo_fl_layout.addWidget(cbo_hint)
    # Insere um espaçador que empurra tudo para a esquerda
    espacador16 = QSpacerItem(int(20 * fator_escala), int(0 * fator_escala), QSizePolicy.Minimum, QSizePolicy.Minimum)
    cbo_fl_layout.addItem(espacador16)
    cbo_fl_layout.addWidget(fl_input)
    cbo_fl_layout.addWidget(fl_hint)
    #Insere um espaçador que empurra tudo para a esquerda
    espacador6 = QSpacerItem(int(0 * fator_escala), int(0 * fator_escala), QSizePolicy.Expanding, QSizePolicy.Minimum)
    cbo_fl_layout.addItem(espacador6)


    tipo_layout = QHBoxLayout()
    tipo_layout.addWidget(tipo_input)
    tipo_layout.addWidget(tipo_hint)

    # Criando um layout horizontal para agrupar os campos
    layout_funcionario = QHBoxLayout()
    #layout_funcionario.addWidget(QLabel("Nome do Funcionário:"))
    layout_funcionario.addWidget(funcionario_input)
    # Insere um espaçador que empurra tudo para a esquerda
    #espacador16 = QSpacerItem(int(50 * fator_escala), int(0 * fator_escala), QSizePolicy.Minimum, QSizePolicy.Minimum)
    #layout_funcionario.addItem(espacador16)
    #layout_funcionario.addWidget(QLabel("Código (ID):"))
    layout_funcionario.addWidget(codigo_input)
    layout_funcionario.addWidget(codigo_hint)
    # Insere um espaçador que empurra tudo para a esquerda
    espacador17 = QSpacerItem(int(0 * fator_escala), int(0 * fator_escala), QSizePolicy.Expanding, QSizePolicy.Minimum)
    layout_funcionario.addItem(espacador17)


    #form_layout.addRow("Código do Funcionário:", codigo_layout)
    form_layout.addRow("Nome do Funcionário:", layout_funcionario)
    form_layout.addRow("Função:", funcao_input)
    form_layout.addRow("CBO e Fl:", cbo_fl_layout)
    form_layout.addRow("Tipo:", tipo_layout)

    # Valores e Descrição de Referência
    referencia_input = QLineEdit()
    referencia_input.setPlaceholderText("Ex: 30,00 D")
    referencia_input.setMaxLength(9)  # Limite de 9 caracteres
    referencia_input.setFixedWidth(int(130 * fator_escala))  # largura
    referencia_input.setFixedHeight(int(22 * fator_escala))  # altura
    referencia_hint = QLabel("Ex: 30,00 D para 30 dias")

    referencia_layout = QHBoxLayout()
    referencia_layout.addWidget(referencia_input)
    referencia_layout.addWidget(referencia_hint)

    salario_saida_copia = QLineEdit()
    salario_saida_copia.setVisible(False)  # Torna o campo invisível

    salario_input = QLineEdit()
    salario_input.setPlaceholderText("Ex: 2500,00")
    salario_input.setMaxLength(12)  # Máximo de 12 caracteres para valores
    salario_input.setFixedWidth(int(130 * fator_escala))  # largura
    salario_input.setFixedHeight(int(22 * fator_escala))  # altura

    codigo_salario_input = QSpinBox()
    codigo_salario_input.setRange(0, 999999)
    codigo_salario_input.setSpecialValueText(" ")  # Faz com que 0 pareça vazio
    codigo_salario_input.setFixedWidth(int(80 * fator_escala))  # largura
    codigo_salario_input.setFixedHeight(int(22 * fator_escala))  # altura
    codigo_salario_hint = QLabel("Código (ID) do Salário Base.")

    salario_layout = QHBoxLayout()
    salario_layout.addWidget(salario_input)
    salario_layout.addWidget(codigo_salario_input)
    salario_layout.addWidget(codigo_salario_hint)


    # Linha de separação entre Salário Base e Descontos

    descontos_input = QLineEdit()
    descontos_input.setFixedWidth(int(80 * fator_escala))  # largura
    descontos_input.setFixedHeight(int(22 * fator_escala))  # altura
    descontos_input.setPlaceholderText("Ex: 125,00")
    descontos_hint = QLabel("Desconto:")

    descricao_desconto_input = QLineEdit()
    descricao_desconto_input.setPlaceholderText("Descrição Ex: I.N.S.S.")
    descricao_desconto_input.setMaxLength(40)  # Limite de 40 caracteres para a descrição do desconto
    descricao_desconto_input.setFixedWidth(int(180 * fator_escala))  # largura
    descricao_desconto_input.setFixedHeight(int(22 * fator_escala))  # altura

    codigo_desconto_input = QSpinBox()
    codigo_desconto_input.setRange(0, 999999)
    codigo_desconto_input.setSpecialValueText(" ")  # Faz com que 0 pareça vazio
    codigo_desconto_input.setFixedWidth(int(80 * fator_escala))  # largura
    codigo_desconto_input.setFixedHeight(int(22 * fator_escala))  # altura
    codigo_desconto_hint = QLabel("Código (ID).")

    vencimentos_input = QLineEdit()
    vencimentos_input.setFixedWidth(int(80 * fator_escala))  # largura
    vencimentos_input.setFixedHeight(int(22 * fator_escala))  # altura
    vencimentos_input.setPlaceholderText("Ex: 150,00")
    vencimentos_hint = QLabel("Vencimento:")

    descontos_layout = QHBoxLayout()
    descontos_layout.addWidget(descontos_hint)
    # Insere um espaçador que empurra tudo para a esquerda
    espacador1 = QSpacerItem(int(14 * fator_escala), int(0 * fator_escala), QSizePolicy.Minimum, QSizePolicy.Minimum)
    descontos_layout.addItem(espacador1)
    descontos_layout.addWidget(descontos_input)
    descontos_layout.addWidget(descricao_desconto_input)
    descontos_layout.addWidget(codigo_desconto_input)
    descontos_layout.addWidget(codigo_desconto_hint)
    # Insere um espaçador que empurra tudo para a esquerda
    espacador9 = QSpacerItem(int(0 * fator_escala), int(0 * fator_escala), QSizePolicy.Expanding, QSizePolicy.Minimum)
    descontos_layout.addItem(espacador9)



    adicionar_desconto_button = QPushButton("ADD+ Desc/Venc")
    adicionar_desconto_button.setToolTip("Adiciona um desconto ou vencimento à lista.")
    adicionar_desconto_button.setFixedWidth(int(120 * fator_escala))  # largura
    adicionar_desconto_button.setFixedHeight(int(22 * fator_escala))  # altura

    # Dica para o botão adicionar desconto
    adicionar_desconto_hint = QLabel("<- Clique após preencher os dados de Desc/Venc.")

    vencimentos_layout = QHBoxLayout()
    vencimentos_layout.addWidget(vencimentos_hint)
    # Insere um espaçador que empurra tudo para a esquerda
    espacador2 = QSpacerItem(int(2 * fator_escala), int(0 * fator_escala), QSizePolicy.Minimum, QSizePolicy.Minimum)
    vencimentos_layout.addItem(espacador2)
    vencimentos_layout.addWidget(vencimentos_input)
    vencimentos_layout.addWidget(adicionar_desconto_button)
    vencimentos_layout.addWidget(adicionar_desconto_hint)
    # Insere um espaçador que empurra tudo para a esquerda
    espacador8 = QSpacerItem(int(0 * fator_escala), int(0 * fator_escala), QSizePolicy.Expanding, QSizePolicy.Minimum)
    vencimentos_layout.addItem(espacador8)


    form_layout.addRow("Referência:", referencia_layout)
    form_layout.addRow("Salário Base:", salario_layout)

    #Criar um layout vertical para empilhar os dois layouts
    dv_layout = QVBoxLayout()
    dv_layout.addLayout(descontos_layout)  # Adiciona os descontos em cima
    dv_layout.addLayout(vencimentos_layout)  # Adiciona os vencimentos embaixo

    #Criar um widget contêiner para o layout vertical
    dv_container = QWidget()
    dv_container.setLayout(dv_layout)  # Aplica o layout no widget

    # Linha de separação1
    separador1 = QFrame()
    separador1.setFrameShape(QFrame.HLine)
    separador1.setFrameShadow(QFrame.Sunken)
    form_layout.addRow(separador1)

    form_layout.addRow("Adicionar D/V:", dv_container)

    # Lista de Descontos Adicionados
    lista_descontos = QListWidget()
    lista_descontos.setFixedWidth(int(580 * fator_escala))  # largura
    lista_descontos.setFixedHeight(int(100 * fator_escala))  # altura
    #lista_descontos.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Sempre mostra a barra
    #lista_descontos.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)  # Rolagem suave
    lista_descontos_espelho = []
    total_vencimentos_var = 0.0  # Variável para armazenar o total de vencimentos
    total_descontos_var = 0.0  # Variável para armazenar o total de descontos
    total_liquido_var = 0.0  # Variável para armazenar o total líquido

    lista_descontos_layout = QVBoxLayout()
    limpar_lista_button = QPushButton("Limpar Lista")
    limpar_lista_button.setToolTip("Remove todos os itens da lista.")
    limpar_lista_button.setFixedWidth(int(100 * fator_escala))  # largura
    limpar_lista_button.setFixedHeight(int(22 * fator_escala))  # altura

    # Estilizando botão de limpar lista
    #palette = limpar_lista_button.palette()
    #palette.setColor(QPalette.Button, QColor(Qt.red))
    #limpar_lista_button.setPalette(palette)

    def limpar_lista():
        nonlocal total_descontos_var, total_liquido_var, total_vencimentos_var
        lista_descontos.clear()
        lista_descontos_espelho.clear()
        atualizar_ui()  # Notifica que a lista mudou
        total_vencimentos_var = 0.0
        total_descontos_var = 0.0  # Resetar total de descontos ao limpar lista
        total_liquido_var = 0.0  # Resetar total líquido
        # Emitir o sinal para atualizar os cálculos no `ui.py`
        app_ref.sinal_atualizar_calculos.emit()

    limpar_lista_button.clicked.connect(limpar_lista)


    lista_descontos_layout.addWidget(lista_descontos)
    lista_descontos_layout.addWidget(limpar_lista_button, alignment=Qt.AlignCenter)

    form_layout.addRow("Descontos/Vencimentos:", lista_descontos_layout)

    # Linha de separação2
    separador2 = QFrame()
    separador2.setFrameShape(QFrame.HLine)
    separador2.setFrameShadow(QFrame.Sunken)
    form_layout.addRow(separador2)

    sal_contr_inss_input = QLineEdit()
    sal_contr_inss_input.setFixedWidth(int(130 * fator_escala))  # largura
    sal_contr_inss_input.setFixedHeight(int(22 * fator_escala))  # altura
    sal_contr_inss_input.setPlaceholderText("Ex: 1900,00")
    sal_contr_inss_input.setMaxLength(15)

    base_fgts_input = QLineEdit()
    base_fgts_input.setFixedWidth(int(130 * fator_escala))  # largura
    base_fgts_input.setFixedHeight(int(22 * fator_escala))  # altura
    base_fgts_input.setPlaceholderText("Ex: 2000,00")
    base_fgts_input.setMaxLength(15)

    valor_fgts_input = QLineEdit()
    valor_fgts_input.setFixedWidth(int(130 * fator_escala))  # largura
    valor_fgts_input.setFixedHeight(int(22 * fator_escala))  # altura
    valor_fgts_input.setPlaceholderText("Ex: 160,00")
    valor_fgts_input.setMaxLength(15)

    base_irrf_input = QLineEdit()
    base_irrf_input.setFixedWidth(int(130 * fator_escala))  # largura
    base_irrf_input.setFixedHeight(int(22 * fator_escala))  # altura
    base_irrf_input.setPlaceholderText("Ex: 1800,00")
    base_irrf_input.setMaxLength(15)

    # Criando os layouts horizontais para cada linha
    layout_inss_basefgts = QHBoxLayout()
    #layout_inss_fgts.addWidget(QLabel("Sal. Contr. INSS:"))
    layout_inss_basefgts.addWidget(sal_contr_inss_input)
    # Insere um espaçador que empurra tudo para a esquerda
    espacador10 = QSpacerItem(int(80 * fator_escala), int(0 * fator_escala), QSizePolicy.Minimum, QSizePolicy.Minimum)
    layout_inss_basefgts.addItem(espacador10)
    layout_inss_basefgts.addWidget(QLabel("Base de cálc. FGTS:"))
    # Insere um espaçador que empurra tudo para a esquerda
    espacador11 = QSpacerItem(int(1 * fator_escala), int(0 * fator_escala), QSizePolicy.Minimum, QSizePolicy.Minimum)
    layout_inss_basefgts.addItem(espacador11)
    layout_inss_basefgts.addWidget(base_fgts_input)
    # Insere um espaçador que empurra tudo para a esquerda
    espacador12 = QSpacerItem(int(0 * fator_escala), int(0 * fator_escala), QSizePolicy.Expanding, QSizePolicy.Minimum)
    layout_inss_basefgts.addItem(espacador12)


    layout_fgts_irrf = QHBoxLayout()
    #layout_valor_irrf.addWidget(QLabel("Valor FGTS:"))
    layout_fgts_irrf.addWidget(valor_fgts_input)
    # Insere um espaçador que empurra tudo para a esquerda
    espacador13 = QSpacerItem(int(80 * fator_escala), int(0 * fator_escala), QSizePolicy.Minimum, QSizePolicy.Minimum)
    layout_fgts_irrf.addItem(espacador13)
    layout_fgts_irrf.addWidget(QLabel("Base de cálc. IRRF:"))
    # Insere um espaçador que empurra tudo para a esquerda
    espacador14 = QSpacerItem(int(5 * fator_escala), int(0 * fator_escala), QSizePolicy.Minimum, QSizePolicy.Minimum)
    layout_fgts_irrf.addItem(espacador14)
    layout_fgts_irrf.addWidget(base_irrf_input)
    # Insere um espaçador que empurra tudo para a esquerda
    espacador15 = QSpacerItem(int(0 * fator_escala), int(0 * fator_escala), QSizePolicy.Expanding, QSizePolicy.Minimum)
    layout_fgts_irrf.addItem(espacador15)



    # Adicionando ao form_layout
    form_layout.addRow("Sal. Contr. INSS:", layout_inss_basefgts)
    form_layout.addRow("Valor FGTS:", layout_fgts_irrf)

    data_emissao_input = QLineEdit(datetime.now().strftime("%d/%m/%Y"))
    data_emissao_input.setFixedWidth(int(90 * fator_escala))  # largura
    data_emissao_input.setFixedHeight(int(22 * fator_escala))  # altura
    form_layout.addRow("Data de Emissão:", data_emissao_input)

    # Função para adicionar desconto
    def adicionar_desconto():
        nonlocal total_descontos_var, total_liquido_var, total_vencimentos_var

        # Verificar se o limite de 15 itens já foi atingido
        if lista_descontos.count() >= 15:
            QMessageBox.warning(None, "Limite atingido", "O número máximo de descontos/vencimentos permitidos é 15.")
            return  # Impede a adição de mais itens

        desconto = descontos_input.text().replace('.', '').replace(',', '.')
        vencimento = vencimentos_input.text().replace('.', '').replace(',', '.')
        descricao = descricao_desconto_input.text()
        codigo = codigo_desconto_input.value()

        # Verifica se pelo menos um dos valores foi preenchido
        if not desconto and not vencimento:
            QMessageBox.warning(None, "Erro", "É necessário inserir um valor de desconto ou vencimento!")
            return

        try:
            desconto_valor = float(desconto) if desconto else 0.0
            vencimento_valor = float(vencimento) if vencimento else 0.0
        except ValueError:
            QMessageBox.warning(None, "Erro", "Os valores de desconto e vencimento devem ser numéricos!")
            return

        # Construção dinâmica da string
        item_text = ""
        if desconto_valor > 0:
            item_text += f" Desconto: {desconto_valor:.2f} |"
            total_descontos_var += desconto_valor
        if vencimento_valor > 0:
            item_text += f" Vencimento: {vencimento_valor:.2f} |"
            total_vencimentos_var += vencimento_valor

        item_text += f" Descrição: {descricao} | Código: {codigo if codigo != 0 else ' '}"

        # Criando item da lista
        item_widget = QWidget()
        item_layout = QHBoxLayout()
        item_layout.setContentsMargins(0, 0, 0, 0)

        item_label = QLabel(item_text)
        remover_button = QPushButton("x")
        remover_button.setFixedWidth(int(20 * fator_escala))  # largura
        remover_button.setFixedHeight(int(18 * fator_escala))  # altura

        def remover_item():
            nonlocal total_descontos_var, total_liquido_var, total_vencimentos_var
            for i in range(lista_descontos.count()):
                if lista_descontos.itemWidget(lista_descontos.item(i)) == item_widget:
                    lista_descontos.takeItem(i)
                    del lista_descontos_espelho[i]
                    atualizar_ui()
                    if desconto_valor > 0:
                        total_descontos_var -= desconto_valor
                    if vencimento_valor > 0:
                        total_vencimentos_var -= vencimento_valor
                    app_ref.sinal_atualizar_calculos.emit()
                    break

        remover_button.clicked.connect(remover_item)

        item_layout.addWidget(item_label)
        item_layout.addWidget(remover_button)
        item_widget.setLayout(item_layout)

        item = QListWidgetItem()
        item.setData(Qt.UserRole, {"desconto": desconto_valor, "vencimento": vencimento_valor})
        lista_descontos.addItem(item)
        lista_descontos.setItemWidget(item, item_widget)

        # Adicionar à lista espelho
        lista_descontos_espelho.append(item_text)
        atualizar_ui()

        # Atualizar valores exibidos
        try:
            salario = float(salario_input.text().replace('.', '').replace(',', '.')) if salario_input.text() else 0.0
            total_liquido_var = salario + total_vencimentos_var - total_descontos_var
            valor_liquido_value.setText(f"{total_liquido_var:.2f}".replace('.', ','))
        except ValueError:
            valor_liquido_value.setText("0,00")

        total_descontos_value.setText(f"{total_descontos_var:.2f}".replace('.', ','))
        total_vencimentos_value.setText(f"{total_vencimentos_var:.2f}".replace('.', ','))

        # Limpar campos
        descontos_input.clear()
        vencimentos_input.clear()
        descricao_desconto_input.clear()
        codigo_desconto_input.setValue(0)
        app_ref.sinal_atualizar_calculos.emit()

    adicionar_desconto_button.clicked.connect(adicionar_desconto)

    # P1------------------------------------------------------------------------------------
    # P2------------------------------------------------------------------------------------
    # Linha de separação3
    separador3 = QFrame()
    separador3.setFrameShape(QFrame.HLine)
    separador3.setFrameShadow(QFrame.Sunken)
    form_layout.addRow(separador3)

    # Totais e Observações
    totais_layout = QVBoxLayout()

    total_vencimentos_layout = QHBoxLayout()
    total_vencimentos_layout.setSpacing(5)
    total_vencimentos_label = QLabel("Total de Vencimentos:")
    total_vencimentos_value = QLineEdit("0,00")
    total_vencimentos_value.setFixedWidth(int(125 * fator_escala))  # largura
    total_vencimentos_value.setFixedHeight(int(22 * fator_escala))  # altura
    total_vencimentos_layout.addWidget(total_vencimentos_label)
    total_vencimentos_layout.addSpacing(3)
    total_vencimentos_layout.addStretch()
    total_vencimentos_layout.addWidget(total_vencimentos_value)
    # Insere um espaçador que empurra tudo para a esquerda
    espacador3 = QSpacerItem(int(320 * fator_escala), int(20 * fator_escala), QSizePolicy.Expanding, QSizePolicy.Minimum)
    total_vencimentos_layout.addItem(espacador3)

    total_descontos_layout = QHBoxLayout()
    total_descontos_layout.setSpacing(5)
    total_descontos_label = QLabel("Total de Descontos:")
    total_descontos_value = QLineEdit("0,00")
    total_descontos_value.setFixedWidth(int(125 * fator_escala))  # largura
    total_descontos_value.setFixedHeight(int(22 * fator_escala))  # altura
    total_descontos_layout.addWidget(total_descontos_label)
    total_descontos_layout.addSpacing(3)
    total_descontos_layout.addStretch()
    total_descontos_layout.addWidget(total_descontos_value)
    # Insere um espaçador que empurra tudo para a esquerda
    espacador4 = QSpacerItem(int(320 * fator_escala), int(20 * fator_escala), QSizePolicy.Expanding,
                             QSizePolicy.Minimum)
    total_descontos_layout.addItem(espacador4)

    valor_liquido_layout = QHBoxLayout()
    valor_liquido_layout.setSpacing(5)
    valor_liquido_label = QLabel("Valor Líquido:")
    valor_liquido_value = QLineEdit("0,00")
    valor_liquido_value.setFixedWidth(int(125 * fator_escala))  # largura
    valor_liquido_value.setFixedHeight(int(22 * fator_escala))  # altura
    valor_liquido_layout.addWidget(valor_liquido_label)
    valor_liquido_layout.addSpacing(3)
    valor_liquido_layout.addStretch()
    valor_liquido_layout.addWidget(valor_liquido_value)
    # Insere um espaçador que empurra tudo para a esquerda
    espacador5 = QSpacerItem(int(320 * fator_escala), int(20 * fator_escala), QSizePolicy.Expanding,
                             QSizePolicy.Minimum)

    valor_liquido_layout.addItem(espacador5)

    totais_layout.addLayout(total_vencimentos_layout)
    totais_layout.addLayout(total_descontos_layout)
    totais_layout.addLayout(valor_liquido_layout)

    form_layout.addRow("Totais:", totais_layout)

    # Linha de separação4
    separador4 = QFrame()
    separador4.setFrameShape(QFrame.HLine)
    separador4.setFrameShadow(QFrame.Sunken)
    form_layout.addRow(separador4)

    observacoes_input = QTextEdit()
    observacoes_input.setFixedWidth(int(580 * fator_escala))  # largura
    observacoes_input.setFixedHeight(int(50 * fator_escala))  # altura
    observacoes_input.setPlaceholderText("Adicione observações, se necessário (até 125 caracteres)")

    limite_caracteres = 125  # Define o limite máximo de caracteres

    def limitar_texto():
        texto_atual = observacoes_input.toPlainText()
        if len(texto_atual) > limite_caracteres:
            observacoes_input.setPlainText(texto_atual[:limite_caracteres])
            # Move o cursor para o final para evitar comportamento estranho na digitação
            cursor = observacoes_input.textCursor()
            cursor.movePosition(cursor.End)
            observacoes_input.setTextCursor(cursor)

    observacoes_input.textChanged.connect(limitar_texto)  # Conecta o evento ao limitador

    form_layout.addRow("Observações:", observacoes_input)

    # Botões
    botoes_layout = QHBoxLayout()
    preview_button = QPushButton("Pré-visualizar PDF")
    preview_button.setToolTip("Veja como o holerite ficará antes de gerar.")
    preview_button.setFixedWidth(int(222 * fator_escala))  # largura
    preview_button.setFixedHeight(int(23 * fator_escala))  # altura

    gerar_button = QPushButton("Gerar Holerite")
    gerar_button.setToolTip("Gera um PDF com holerite duplo.")
    gerar_button.setFixedWidth(int(222 * fator_escala))  # largura
    gerar_button.setFixedHeight(int(23 * fator_escala))  # altura

    # Criar o botão de impressão com ícone
    imprimir_button = QPushButton()
    imprimir_button.setToolTip("Imprime uma folha com holerite duplo.")
    imprimir_button.setFixedWidth(int(40 * fator_escala))  # largura
    imprimir_button.setFixedHeight(int(23 * fator_escala))  # altura

    # Aplicar o ícone se o arquivo existir
    if os.path.exists(icon_print_path):
        imprimir_button.setIcon(QIcon(icon_print_path))
        imprimir_button.setIconSize(QSize(int(16 * fator_escala), int(16 * fator_escala)))
    else:
        print(f"⚠️ Aviso: Ícone de impressão não encontrado em {icon_print_path}")

    limpar_button = QPushButton("Limpar Campos")
    limpar_button.setToolTip("Apaga todos os dados preenchidos.")
    limpar_button.setFixedWidth(int(222 * fator_escala))  # largura
    limpar_button.setFixedHeight(int(23 * fator_escala))  # altura


    espacador7 = QSpacerItem(int(1 * fator_escala), int(1 * fator_escala), QSizePolicy.Expanding,
                             QSizePolicy.Minimum)
    form_layout.addItem(espacador7)
    botoes_layout.addWidget(preview_button)
    botoes_layout.addWidget(gerar_button)
    botoes_layout.addWidget(limpar_button)
    botoes_layout.addWidget(imprimir_button)

    form_layout.addRow(botoes_layout)

    # Atualização automática do valor líquido
    def atualizar_valor_liquido():
        try:
            salario = float(salario_input.text().replace(',', '.')) if salario_input.text() else 0.0
            total_liquido_var = salario - total_descontos_var
            valor_liquido_value.setText(f"{total_liquido_var:.2f}".replace('.', ','))
        except ValueError:
            valor_liquido_value.setText("0,00")

    # Conectar eventos
    #salario_input.textChanged.connect(atualizar_valor_liquido)
    lista_descontos.itemChanged.connect(atualizar_valor_liquido)

    # Integração para atualizações dinâmicas
    def atualizar_totais_interface(vencimentos, descontos, liquido):
        total_vencimentos_value.setText(f"{vencimentos:.2f}".replace('.', ','))
        total_descontos_value.setText(f"{descontos:.2f}".replace('.', ','))
        valor_liquido_value.setText(f"{liquido:.2f}".replace('.', ','))

    # Após adicionar todos os elementos, ajusta o tamanho manualmente
    #ajustar_tamanho_manual(form_layout)

    # Retornar layout e entradas para integração
    return form_layout, {
        "empresa_input": empresa_input,
        "endereco_input": endereco_input,
        "cnpj_input": cnpj_input,
        "codigo_input": codigo_input,
        "funcionario_input": funcionario_input,
        "funcao_input": funcao_input,
        "cbo_input": cbo_input,
        "fl_input": fl_input,
        "tipo_input": tipo_input,
        "referencia_input": referencia_input,
        "salario_input": salario_input,
        "salario_saida_copia": salario_saida_copia,
        "codigo_salario_input": codigo_salario_input,
        "descontos_input": descontos_input,
        "vencimentos_input": vencimentos_input,
        "descricao_desconto_input": descricao_desconto_input,
        "codigo_desconto_input": codigo_desconto_input,
        "lista_descontos": lista_descontos,
        "lista_descontos_espelho": lista_descontos_espelho,
        "atualizar_ui": atualizar_ui,  # Adiciona a função de atualização ao retorno
        "total_descontos_var": total_descontos_var,
        "total_liquido_var": total_liquido_var,
        "sal_contr_inss_input": sal_contr_inss_input,
        "base_fgts_input": base_fgts_input,
        "valor_fgts_input": valor_fgts_input,
        "base_irrf_input": base_irrf_input,
        "data_emissao_input": data_emissao_input,
        "totais": {
            "vencimentos": total_vencimentos_value,
            "descontos": total_descontos_value,
            "liquido": valor_liquido_value,
        },
        "observacoes_input": observacoes_input,
        "botoes": {
            "preview": preview_button,
            "gerar": gerar_button,
            "limpar": limpar_button,
            "imprimir": imprimir_button,
        }
    }


def atualizar_ui():
    global lista_descontos_espelho, lista_descontos

    # Se a lista de descontos principal estiver vazia, esvaziar a lista espelho também
    if lista_descontos.count() == 0:
        lista_descontos_espelho.clear()

    return lista_descontos_espelho  # Retorna a lista espelho sempre atualizada


# Developed by Raphael Soares dos Santos - Payslip Generator

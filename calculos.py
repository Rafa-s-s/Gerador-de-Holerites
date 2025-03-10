"""
============================================================
  Payslip Generator
  Developed by: Raphael Soares dos Santos
  Creation Date: February 10, 2025
============================================================
"""

# calculos.py
from typing import List, Dict

def calcular_fgts(salario_base: float) -> Dict[str, float]:
    """
    Calcula a base e o valor do FGTS com base no salário base.
    :param salario_base: Salário base do funcionário.
    :return: Dicionário com base e valor do FGTS.
    """
    base_fgts = salario_base
    valor_fgts = base_fgts * 0.08
    return {"base_fgts": base_fgts, "valor_fgts": valor_fgts}

def calcular_irrf(salario_base: float, num_dependentes: int = 0, pensao_alimenticia: float = 0.0) -> Dict[str, float]:
    """
    Calcula a base e o valor do IRRF considerando o salário base e deduções.
    :param salario_base: Salário base do funcionário.
    :param num_dependentes: Número de dependentes do funcionário.
    :param pensao_alimenticia: Valor da pensão alimentícia.
    :return: Dicionário com base e valor do IRRF.
    """
    # Tabela de alíquotas do INSS para 2025
    faixas_inss = [
        (1412.00, 0.075),
        (2666.68, 0.09),
        (4000.03, 0.12),
        (7786.02, 0.14)
    ]

    # Cálculo da contribuição ao INSS
    inss = 0.0
    salario_restante = salario_base
    for limite, aliquota in faixas_inss:
        if salario_restante > 0:
            faixa = min(salario_restante, limite)
            inss += faixa * aliquota
            salario_restante -= faixa

    # Dedução por dependentes
    deducao_dependentes = num_dependentes * 189.59

    # Base de cálculo do IRRF
    base_irrf = salario_base - inss - deducao_dependentes - pensao_alimenticia

    # Tabela progressiva do IRRF para 2025
    faixas_irrf = [
        (2259.20, 0.0, 0.00),
        (2826.65, 0.075, 169.44),
        (3751.05, 0.15, 381.44),
        (4664.68, 0.225, 662.77),
        (float('inf'), 0.275, 896.00)
    ]

    # Cálculo do IRRF
    irrf = 0.0
    for limite, aliquota, deducao in faixas_irrf:
        if base_irrf <= limite:
            irrf = (base_irrf * aliquota) - deducao
            break

    return {
        "base_irrf": max(base_irrf, 0.0),  # Garante que a base não seja negativa
        "valor_irrf": max(irrf, 0.0)  # Garante que o IRRF não seja negativo
    }

CONFIG = {
    "version": "1.0.0",
    "author": "5261706861656c20536f6172657320646f732053616e746f73"
}

def somar_descontos(lista_descontos: List[str]) -> float:
    """
    Soma os valores de descontos a partir de uma lista de strings contendo os valores.
    :param lista_descontos: Lista de strings representando os descontos (Ex.: ["125.00", "5%"].
    :return: Soma total dos descontos.
    """
    total = 0.0
    for desconto in lista_descontos:
        try:
            if "%" in desconto:
                valor_percentual = float(desconto.strip('%')) / 100
                continue
            total += float(desconto.replace(',', '.'))
        except ValueError:
            pass
    return total


def atualizar_totais(salario_base: float, descontos: float, irrf: float) -> Dict[str, float]:
    """
    Atualiza os valores de vencimentos, descontos e líquido.
    :param salario_base: Salário base do funcionário.
    :param descontos: Total de descontos aplicados (incluindo FGTS e IRRF).
    :param irrf: Valor do IRRF calculado.
    :return: Dicionário com totais atualizados.
    """
    total_vencimentos = salario_base
    total_descontos = descontos #+ irrf
    valor_liquido = total_vencimentos - total_descontos

    return {
        "total_vencimentos": total_vencimentos,
        "total_descontos": total_descontos,
        "valor_liquido": valor_liquido
    }


# Developed by Raphael Soares dos Santos - Payslip Generator

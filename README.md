# 📄 Sistema Gerador de Holerites

**Versão:** 1.0.0  
**Desenvolvido por:** Raphael Soares dos Santos  

## 📌 Descrição

O **Sistema Gerador de Holerites** é uma aplicação desenvolvida em **Python (PyQt5)** que permite a criação, pré-visualização e impressão de holerites. Ele é ideal para pequenas empresas, contadores e profissionais que precisam de um sistema simples e eficiente para gerar holerites.

---

## ⚙️ Funcionalidades

- ✅ Geração de holerites com base nos dados inseridos.
- ✅ Interface gráfica moderna e intuitiva.
- ✅ Salvar holerites como **PDF**.
- ✅ Opção de **impressão direta**.
- ✅ Suporte para **cálculos automáticos** de FGTS e IRRF.
- ✅ **Versão desktop** com instalador para Windows.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **PyQt5** (Interface gráfica)
- **ReportLab** (Geração de PDF)
- **Pillow** (Manipulação de imagens)
- **cx_Freeze** (Empacotamento para .exe)

---

## 📦 Estrutura do Projeto

```
holerite_generator/
├── src/
│   ├── main.py                     # Arquivo principal
│   ├── form_layout.py              # Layout do formulário
│   ├── ui.py                       # Interface gráfica
│   ├── preview_window.py           # Janela de pré-visualização
│   ├── holerite_generator.py       # Geração do holerite
│   ├── printer.py                  # Funções de impressão
│   ├── pdf_generator.py            # Criação de PDFs
│   ├── calculos.py                 # Cálculo de FGTS, IRRF e Totais
│   ├── utils.py                    # Funções utilitárias
│   ├── assets/
│       ├── templates/              # Modelos de holerite
│       ├── preview/                # Pré-visualizações
│       ├── icons/                  # Ícones do projeto
├── tests/
│   ├── test_holerite.py             # Testes unitários
├── README.md                        # Documentação do projeto
├── requirements.txt                 # Dependências do projeto
├── setup.py                         # Configuração do executável
└── dist/                            # Pasta onde o executável é gerado
```

---

## 🚀 Instalação

Para rodar o projeto localmente:

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/Rafa-s-s/seu-repositorio.git
cd seu-repositorio
```

### 2️⃣ Crie um ambiente virtual e instale as dependências

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3️⃣ Execute o programa

```bash
python src/main.py
```

---

## 📃 Licença

Este projeto está licenciado sob a **MIT License** – veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## ✉️ Contato

📧 **E-mail:** raphael.soaresdossantos@yahoo.com  
🌐 **GitHub:** [Rafa-s-s](https://github.com/Rafa-s-s)  

![Interface_Holerite](https://github.com/user-attachments/assets/e4837af5-e5da-4da6-8f71-73c491eeb73c)





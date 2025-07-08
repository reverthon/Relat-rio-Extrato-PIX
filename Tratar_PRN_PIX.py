import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QScrollArea, QLabel
from collections import defaultdict
import locale
import calendar
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
import os

# Definir locale para formatar os valores como Real (R$)
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')  # fallback para o padrão do sistema

# Inicializar as variáveis "ano" e "Nome"
ano = ""
Nome = ""

# Função para calcular a soma dos valores por mês
def calcular_soma_por_mes(dados):
    soma_debito = {}
    soma_credito = {}
    contagem_pix_credito = {}
    descricao_somas_meses = defaultdict(lambda: defaultdict(float))  # Dicionário aninhado para manter a soma por descrição e mês

    for linha in dados:
        data = linha['Data']
        debito = 0.0
        if linha['Debito'] and linha['Debito'].strip() != '':
            debito = float(linha['Debito'].replace('.', '').replace(',', '.').strip())
        credito = 0.0
        if linha['Credito'] and linha['Credito'].strip() != '':
            credito = float(linha['Credito'].replace('.', '').replace(',', '.').strip())
        historico = linha['Historico']

        # Verificar se o histórico começa com "DEVOLUCAO" e desconsiderar o débito
        if "DEVOLUCAO" in historico.upper():
            debito = 0.0

        mes_numero = int(data.split('/')[1])
        mes_nome = calendar.month_name[mes_numero].capitalize()  # Primeira letra maiúscula

        if mes_nome in soma_debito:
            soma_debito[mes_nome] += debito
            soma_credito[mes_nome] += credito
            if credito > 0:
                contagem_pix_credito[mes_nome] += 1
        else:
            soma_debito[mes_nome] = debito
            soma_credito[mes_nome] = credito
            if credito > 0:
                contagem_pix_credito[mes_nome] = 1
            else:
                contagem_pix_credito[mes_nome] = 0

        # Somar os valores das descrições repetidas por mês
        if credito > 0:
            descricao = historico.strip().upper()  # Extrair a descrição e converter para maiúsculas
            descricao_somas_meses[descricao][mes_nome] += credito

    # Calcular o Total PIX Crédito Geral
    total_pix_credito_geral = sum(soma_credito.values())

    return soma_debito, soma_credito, contagem_pix_credito, descricao_somas_meses,total_pix_credito_geral

def calcular_concentracao_pix_credito(dados, total_pix_credito):
    descricao_somas = {}

    for linha in dados:
        descricao = linha['Historico']
        credito_str = linha['Credito'].replace('.', '').replace(',', '').strip()

        # Verificar se o valor de crédito é válido e diferente de vazio
        if credito_str and credito_str.isdigit():
            credito = float(credito_str)
            descricao = linha['Historico'].strip().upper()  # Extrair a descrição a partir da posição 53 e converter para maiúsculas
            #print(f"Descricao:{descricao}, Crédito: {credito}")
            if descricao in descricao_somas:
                descricao_somas[descricao] += credito
            else:
                descricao_somas[descricao] = credito

    concentracao = []
    for descricao, soma in descricao_somas.items():
        percentual = (soma / total_pix_credito) * 100
        if percentual >= 30:
            concentracao.append((descricao, percentual, soma))

    return concentracao

def calcular_concentracao_geral(dados, total_pix_credito_geral):
    return calcular_concentracao_pix_credito(dados, total_pix_credito_geral)

class ResumoPIXWindow(QMainWindow):
    def __init__(self, Nome, soma_debito, soma_credito, contagem_pix_credito, descricao_somas_meses, total_pix_credito_geral):
        super().__init__()
        self.setWindowTitle("Resumo PIX")
        self.setGeometry(200, 50, 1000, 650)

        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)
        self.scroll_area = QScrollArea(self.central_widget)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        self.layout.addWidget(self.scroll_area)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        fonte_titulo = QFont("Arial", 12, QFont.Bold)  # Aumentar o tamanho e aplicar negrito ao título

        label_titulo = QLabel(f"<b>Nome do Associado:</b> {Nome}\n")  # Adicionar "Nome do Associado:" ao QLabel
        label_titulo.setFont(fonte_titulo)  # Aplicar a fonte ao título
        label_titulo.setStyleSheet("background-color: white; padding: 5px;")  # Definir fundo branco e espaçamento interno
        self.scroll_layout.addWidget(label_titulo, alignment=Qt.AlignTop)

        # Exibir o Total PIX Crédito Geral
        total_pix_credito_geral_formatado = locale.currency(total_pix_credito_geral, grouping=True, symbol="R$")
        total_pix_credito_geral_texto = f"<b>Total de Recebimento PIX:</b> {total_pix_credito_geral_formatado}<br/>"

        # Exibir o Ticket Médio Geral (Crédito)
        total_pix_credito = sum(soma_credito.values())
        total_contagem_pix_credito = sum(contagem_pix_credito.values())
        ticket_medio_geral = total_pix_credito / total_contagem_pix_credito if total_contagem_pix_credito > 0 else 0
        ticket_medio_geral_formatado = locale.currency(ticket_medio_geral, grouping=True, symbol="R$")
        ticket_medio_geral_texto = f"<b>Ticket Médio dos Recebimentos PIX:</b> {ticket_medio_geral_formatado}<br/>"

        fonte_titulo = QFont("Arial", 12, QFont.Bold)  # Aumentar o tamanho e aplicar negrito ao título
        label_titulo = QLabel(f"<b>Resumo Geral (Todo Extrato PIX):</b>\n")  # Adicionar "Nome do Associado:" ao QLabel
        label_titulo.setFont(fonte_titulo)  # Aplicar a fonte ao título
        label_titulo.setStyleSheet("background-color: white; padding: 5px;")  # Definir fundo branco e espaçamento interno
        self.scroll_layout.addWidget(label_titulo, alignment=Qt.AlignTop)

        # Concatenar as informações de "Total PIX Crédito Geral", "Ticket Médio Geral (Crédito)" e "Análise de Concentração Geral"
        resumo_texto = (
            f"<b>"
            f"</b>{total_pix_credito_geral_texto}{ticket_medio_geral_texto}</b>"
            f"<b>Concentração Geral: </b><br/>"
        )

        # Calcular a análise de concentração geral
        concentracao_geral = calcular_concentracao_geral(dados, total_pix_credito_geral)

        # Adicionar as informações da análise de concentração na mesma label
        for descricao, percentual, soma in concentracao_geral:
            if percentual >= 3000:
                percentual_formatado = f"{percentual/100:.2f}%"
                soma_formatada = locale.currency(soma/100, grouping=True, symbol="R$")
                resumo_texto += f"{descricao}: Total de transações PIX Crédito = {soma_formatada}. Concentração: {percentual_formatado}.<br/>"

        # Criar a QLabel para exibir todas as informações
        self.resumo_label = QLabel(resumo_texto)
        self.resumo_label.setFont(QFont("Arial", 12))
        self.resumo_label.setStyleSheet("background-color: white; padding: 5px;")
        self.resumo_label.setAlignment(Qt.AlignTop)
        self.scroll_layout.addWidget(self.resumo_label)  # Adicionar o QLabel no layout de rolagem

        self.setCentralWidget(self.central_widget)

        self.exibir_resumo_pix(Nome, soma_debito, soma_credito, contagem_pix_credito, descricao_somas_meses)

    def exibir_resumo_pix(self, Nome, soma_debito, soma_credito, contagem_pix_credito, descricao_somas_meses):
        fonte_dados = QFont("Arial", 12)  # Aumentar o tamanho da fonte aqui

        fonte_titulo = QFont("Arial", 12, QFont.Bold)  # Aumentar o tamanho e aplicar negrito ao título
        label_titulo = QLabel(f"<b>Resumo por mês:</b>\n")  # Adicionar "Nome do Associado:" ao QLabel
        label_titulo.setFont(fonte_titulo)  # Aplicar a fonte ao título
        label_titulo.setStyleSheet("background-color: white; padding: 5px;")  # Definir fundo branco e espaçamento interno
        self.scroll_layout.addWidget(label_titulo, alignment=Qt.AlignTop)


        for mes, valor_debito in soma_debito.items():
            valor_credito = soma_credito[mes]
            contagem_pix = contagem_pix_credito[mes]

            valor_formatado_debito = locale.currency(valor_debito, grouping=True, symbol="R$")
            valor_formatado_credito = locale.currency(valor_credito, grouping=True, symbol="R$")

            ticket_medio = valor_credito / contagem_pix if contagem_pix > 0 else 0
            ticket_medio_formatado = locale.currency(ticket_medio, grouping=True, symbol="R$")

            mes_ano = f"{mes.capitalize()}/{ano}"
            concentracao_pix = calcular_concentracao_pix_credito(dados, valor_credito)

            widget_mes = QWidget()  # Criar um novo QWidget para cada mês
            widget_mes.setStyleSheet("background-color: white;")  # Aplicar o estilo de fundo branco
            layout_mes = QVBoxLayout(widget_mes)  # Criar um QVBoxLayout para o novo QWidget


            # Formatando a string para exibir uma abaixo da outra
            label_text = (
                f"<b>{mes_ano}</b><br/>"
                f"Total de PIX Enviado: {valor_formatado_debito}<br/>"
                f"Total de Recebimento PIX {valor_formatado_credito}<br/>"
                f"Ticket Médio dos Recebimentos PIX: {ticket_medio_formatado}<br/>"
                f"Quantidade de Recebimentos PIX: {contagem_pix}<br/><br/>"
                f"<b>Concentração: </b><br/>"
            )

            if concentracao_pix:
                #label_text += "<b>Concentração:</b><br/>"
                for descricao, percentual, soma in concentracao_pix:
                    soma_mes = descricao_somas_meses[descricao][mes]  # Soma específica para o mês atual
                    percentual_mes = (soma_mes / valor_credito) * 100  # Percentual específico para o mês atual
                    if percentual_mes >= 30:
                        label_text += "</b><br/>" f"{descricao}: Total de transações PIX Crédito = {locale.currency(soma_mes, grouping=True, symbol='R$')}. Concentração: {percentual_mes:.2f}%."
                label_text += "<br/>"

            label_widget = QLabel()
            label_widget.setTextFormat(Qt.RichText)
            label_widget.setText(label_text)
            label_widget.setFont(fonte_dados)
            self.scroll_layout.addWidget(label_widget, alignment=Qt.AlignTop)

            # Adicionar o QLabel dentro do novo QWidget
            layout_mes.addWidget(label_widget, alignment=Qt.AlignTop)
            layout_mes.addStretch(1)  # Adicionar espaço entre as informações

            # Adicionar o novo QWidget no layout da janela
            self.scroll_layout.addWidget(widget_mes)

            # Aplicar a formatação em negrito para a data
            label_widget.setStyleSheet("b { font-weight: bold; }")

app = QApplication(sys.argv)

# Abrir janela de seleção de arquivo PRN
root = tk.Tk()
root.withdraw()
arquivo_prn = filedialog.askopenfilename(
    title="Selecione o arquivo baixado em PRN", filetypes=[("PRN Files", "*.PRN")]
)

if arquivo_prn:
    manipulador = open(arquivo_prn, "r")

    # Ler o arquivo PRN e obter a informação desejada
    linha_desejada = None
    for i, linha in enumerate(manipulador):
        if i == 4:  # Considerando que a linha 5 tem o índice 4
            Nome = linha[11:45].strip()
            linha_desejada = linha.rstrip()  # Remove espaços em branco no final da linha
            break

    manipulador.close()

    # Exibir a informação desejada
    if linha_desejada is not None:

        # Definir o caminho do arquivo CSV diretamente no código
        arquivo_csv = os.path.join('C:\\Temp', f"{Nome}.csv")

        if arquivo_csv:
            saida = open(arquivo_csv, "w")
            saida.write(f"Nome do Associado: {Nome}\n")
            saida.write("Data;Documento;Historico;Debito;Credito\n")
            dados = []

            # Abrir novamente o arquivo PRN
            manipulador = open(arquivo_prn, "r")
            for linha in manipulador:
                linha = linha.rstrip()
                if linha != "":
                    digito = linha[13:17]
                    if "PIX" in digito:
                        Data = linha[0:11]
                        Documento = linha[13:23]
                        Historico = linha[40:68]
                        Debito = linha[73:96]
                        Credito = linha[97:112]
                        linhafinal = f"{Data};{Documento};{Historico};{Debito};{Credito}\n"
                        saida.write(linhafinal)
                        dados.append(
                            {
                                "Data": Data,
                                "Debito": Debito,
                                "Credito": Credito,
                                "Historico": Historico,
                            }
                        )
                        if not ano:  # Atribuir o valor do ano na primeira linha válida
                            ano = Data.split("/")[2].strip()

            manipulador.close()
            saida.close()

            # Exibir uma caixa de mensagem
            messagebox.showinfo("Arquivo Salvo", f"O Extrato PIX foi salvo na pasta Temp com o nome {Nome}")


            # Calcular a soma dos valores por mês
            soma_debito, soma_credito, contagem_pix_credito, descricao_somas_meses, total_pix_credito_geral = calcular_soma_por_mes(dados)

            # Janela para exibir o resumo PIX
            resumo_pix_window = ResumoPIXWindow(Nome, soma_debito, soma_credito, contagem_pix_credito, descricao_somas_meses, total_pix_credito_geral)
            resumo_pix_window.show()

            sys.exit(app.exec_())
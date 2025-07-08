# Tratar PRN PIX

Este projeto foi desenvolvido para atender à necessidade da empresa em realizar uma análise detalhada das movimentações financeiras via PIX, tanto de pagamentos quanto de recebimentos. Como o sistema original não disponibilizava uma base específica para este tipo de análise, foi criado um script em Python capaz de processar extratos de conta corrente gerados no formato PRN, que não possuem padronização, disponibilizando as informações de forma tratada e visual em tela.

## 📌 Funcionalidades

- Leitura de arquivos `.PRN` com transações bancárias.
- Extração de dados PIX (Data, Documento, Histórico, Débito, Crédito).
- Geração de arquivo `.CSV` com os dados tratados.
- Cálculo de:
  - Total de recebimentos e envios por mês.
  - Ticket médio de recebimentos.
  - Concentração de recebimentos por origem.
- Interface gráfica com resumo analítico (PyQt5).

## 🖥️ Interface

A interface exibe:
- Nome do cliente.
- Resumo geral dos recebimentos.
- Análise por mês com concentração de PIX.

## 🛠️ Requisitos

- Python 3.8+
- PyQt5
- tkinter (incluso no Python)
- Sistema operacional com suporte a GUI (Windows recomendado)

## 📦 Instalação

```bash
pip install pyqt5


# Tratar PRN PIX

Esse projeto foi desenvolvido para atender à necessidade da empresa de realizar uma análise mais detalhada das movimentações financeiras via PIX, tanto em relação a pagamentos quanto recebimentos. Como o sistema original não disponibilizava uma base específica para esse tipo de análise, foi criado um script em Python capaz de processar o extrato de conta corrente gerado no formato PRN, sem configurações padronizadas e disponibilizar as informações em tela.

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


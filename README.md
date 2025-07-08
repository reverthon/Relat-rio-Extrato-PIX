# Tratar PRN PIX

Este projeto é uma ferramenta para leitura, extração e análise de transações PIX a partir de arquivos `.PRN` exportados do sistema XY.

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

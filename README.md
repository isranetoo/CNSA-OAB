# CNA OAB Data Extractor

Este projeto realiza a extração e processamento de dados do site [CNA OAB](https://cna.oab.org.br/). Ele automatiza a coleta de informações de advogados registrados, incluindo detalhes adicionais e imagens relacionadas. 

## Funcionalidades

- **Extração de Dados**: Realiza requisições ao sistema CNA utilizando o nome do advogado e salva os resultados.
- **Detalhes Adicionais**: Coleta informações detalhadas a partir das URLs retornadas pela consulta inicial.
- **Processamento de Arquivos**: Extrai informações relevantes dos arquivos JSON retornados.
- **Download de Imagens**: Baixa imagens relacionadas aos registros de advogados.
- **Execução de Scripts Auxiliares**: Integra outros scripts Python para etapas adicionais de processamento.

## Estrutura de Pastas

O projeto organiza os arquivos em pastas criadas automaticamente:

- `output_CNA_OAB`: Resultados da consulta inicial (dados gerais dos advogados).
- `resultados_CNA_detalhes`: Detalhes adicionais obtidos das URLs.
- `detalhes_CNA_processados`: Arquivos JSON processados.
- `imgs_CNA_OAB`: Imagens baixadas.

## Requisitos

- Python 3.8 ou superior
- Bibliotecas necessárias (instale com `pip install -r requirements.txt`):
  - `requests`

## Como Usar

1. **Crie uma lista de nomes**:
   - Crie um arquivo chamado `lista_nomes.txt` contendo os nomes dos advogados, um por linha.

2. **Execute o script principal**:
   ```bash
   python main.py

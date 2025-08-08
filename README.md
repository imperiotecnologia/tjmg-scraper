# Dashboard Precavida Brasil - Análise Comercial 2025

Este repositório contém um app em Streamlit que apresenta um dashboard interativo com os principais KPIs, gráficos e tabelas do controle comercial de 2025 da Precavida Brasil.

## Pré-requisitos
- Python 3.10+
- (Opcional) Ambiente virtual configurado

## Instalação

Sem ambiente virtual (rápido):
```bash
pip install -r requirements.txt
```

Com ambiente virtual (recomendado):
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Executar o app
```bash
streamlit run app/precavida_dashboard.py
```

O app será aberto no navegador (normalmente em `http://localhost:8501`).

## Dados
Devido a restrições de acesso, os arquivos Excel originais não estão incluídos. O app utiliza dados de 2025 embutidos (resumo executivo) para demonstração. Você pode enviar arquivos Excel usando os seletores na barra lateral para integração em uma etapa futura.

Arquivos esperados (quando disponíveis):
- Controle Comercial 2025: `xlsx/xls/xlsb`
- Ranking de Especialistas: `xlsx/xls/xlsb`
- Ranking de Negociadores: `xlsx/xls/xlsb`

## Funcionalidades
- KPIs principais com formatação compacta BRL
- Gráficos de barras, linhas e pizza (Plotly)
- Filtros por mês
- Tabelas de análise por praça e rankings
- Layout responsivo em Streamlit

## Próximos passos
- Conectar leitura dos arquivos Excel enviados (mapeamento de colunas)
- Persistir filtros e preferências do usuário
- Exportar gráficos/tabelas em PNG/CSV

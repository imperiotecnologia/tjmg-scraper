import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime


# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="Dashboard Precavida Brasil 2025",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -------------------------------
# Helpers
# -------------------------------
PT_BR_MONTHS = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]


def format_currency_brl_compact(value_brl: float) -> str:
    """
    Format numeric value (in BRL) using a compact Brazilian style, e.g.:
      49_300_000 -> 'R$ 49,3M'
      885_723   -> 'R$ 885,7K'
    """
    if value_brl is None or pd.isna(value_brl):
        return "-"

    abs_value = abs(value_brl)
    sign = "-" if value_brl < 0 else ""

    if abs_value >= 1_000_000_000:
        comp = f"{abs_value / 1_000_000_000:.1f}B".replace(".", ",")
    elif abs_value >= 1_000_000:
        comp = f"{abs_value / 1_000_000:.1f}M".replace(".", ",")
    elif abs_value >= 1_000:
        comp = f"{abs_value / 1_000:.1f}K".replace(".", ",")
    else:
        comp = f"{abs_value:,.0f}".replace(",", ".")

    return f"{sign}R$ {comp}"


def percent_str(p: float) -> str:
    if p is None or pd.isna(p):
        return "-"
    return f"{p*100:.1f}%".replace(".", ",")


# -------------------------------
# Static 2025 summary data (fallback)
# -------------------------------
TOTAL_QTD_PRECS = 351
TOTAL_VALOR_PRECS = 49_300_000.0
TOTAL_APORTE = 26_800_000.0
MAX_OPERACAO = 885_723.0

# Derived KPIs (trusting provided values, but also computing to stay consistent)
TICKET_MEDIO_PRECAT = TOTAL_VALOR_PRECS / TOTAL_QTD_PRECS if TOTAL_QTD_PRECS else np.nan
PERCENTUAL_PAGO = TOTAL_APORTE / TOTAL_VALOR_PRECS if TOTAL_VALOR_PRECS else np.nan
TICKET_MEDIO_APORTE = TOTAL_APORTE / TOTAL_QTD_PRECS if TOTAL_QTD_PRECS else np.nan

# "Praças" table (values in Millions as provided, converted to BRL)
pracas_df = pd.DataFrame(
    [
        {"Praça": "Minas Gerais", "Qtd Precatórios": 202, "Valor (M)": 32.9, "Aporte (M)": 17.9, "Participação": 0.667},
        {"Praça": "Bahia", "Qtd Precatórios": 20, "Valor (M)": 5.6, "Aporte (M)": 1.8, "Participação": 0.114},
        {"Praça": "TRF4", "Qtd Precatórios": 13, "Valor (M)": 2.3, "Aporte (M)": 1.6, "Participação": 0.047},
        {"Praça": "TRF2", "Qtd Precatórios": 18, "Valor (M)": 2.1, "Aporte (M)": 1.5, "Participação": 0.043},
        {"Praça": "TRF6", "Qtd Precatórios": 14, "Valor (M)": 1.4, "Aporte (M)": 1.0, "Participação": 0.028},
    ]
)
pracas_df["Valor BRL"] = pracas_df["Valor (M)"] * 1_000_000
pracas_df["Aporte BRL"] = pracas_df["Aporte (M)"] * 1_000_000

# "Evolução Mensal 2025"
meses_order = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho"]
evolucao_df = pd.DataFrame(
    [
        {"Mês": "Janeiro", "Qtd Precatórios": 29, "Valor Precatórios": 3_500_000, "Valor Aportado": 1_800_000},
        {"Mês": "Fevereiro", "Qtd Precatórios": 78, "Valor Precatórios": 7_700_000, "Valor Aportado": 4_100_000},
        {"Mês": "Março", "Qtd Precatórios": 55, "Valor Precatórios": 5_700_000, "Valor Aportado": 2_900_000},
        {"Mês": "Abril", "Qtd Precatórios": 59, "Valor Precatórios": 9_100_000, "Valor Aportado": 4_500_000},
        {"Mês": "Maio", "Qtd Precatórios": 72, "Valor Precatórios": 12_900_000, "Valor Aportado": 7_600_000},
        {"Mês": "Junho", "Qtd Precatórios": 54, "Valor Precatórios": 9_800_000, "Valor Aportado": 5_600_000},
        {"Mês": "Julho", "Qtd Precatórios": 4, "Valor Precatórios": 500_000, "Valor Aportado": 300_000},
    ]
)

evolucao_df["Mês"] = pd.Categorical(evolucao_df["Mês"], categories=meses_order, ordered=True)

# Performance dos Especialistas
especialistas_df = pd.DataFrame(
    [
        {"Especialista": "Regiane", "Operações": 93, "Valor (M)": 12.2, "Ticket Médio": 131_000, "Participação": 0.248},
        {"Especialista": "Breno Antunes", "Operações": 56, "Valor (M)": 10.0, "Ticket Médio": 179_000, "Participação": 0.203},
        {"Especialista": "Marcelle", "Operações": 76, "Valor (M)": 9.9, "Ticket Médio": 130_000, "Participação": 0.201},
        {"Especialista": "Isadora", "Operações": 99, "Valor (M)": 8.9, "Ticket Médio": 90_000, "Participação": 0.181},
        {"Especialista": "Ricardo", "Operações": 27, "Valor (M)": 8.3, "Ticket Médio": 307_000, "Participação": 0.168},
    ]
)
especialistas_df["Valor BRL"] = especialistas_df["Valor (M)"] * 1_000_000

# Performance dos Negociadores
negociadores_df = pd.DataFrame(
    [
        {"Negociador": "Precavida", "Operações": 139, "Valor (M)": 16.0, "Ticket Médio": 115_000, "Participação": 0.325},
        {"Negociador": "Mauricio", "Operações": 14, "Valor (M)": 6.0, "Ticket Médio": 432_000, "Participação": 0.123},
        {"Negociador": "Inova", "Operações": 9, "Valor (M)": 4.5, "Ticket Médio": 502_000, "Participação": 0.092},
        {"Negociador": "LIR", "Operações": 24, "Valor (M)": 4.0, "Ticket Médio": 168_000, "Participação": 0.082},
        {"Negociador": "Rafael Fly", "Operações": 4, "Valor (M)": 1.8, "Ticket Médio": 451_000, "Participação": 0.037},
    ]
)
negociadores_df["Valor BRL"] = negociadores_df["Valor (M)"] * 1_000_000

# Distribuição por fonte
fontes_df = pd.DataFrame(
    [
        {"Fonte": "Intermediárias", "Participação": 0.673},
        {"Fonte": "Breno Martins", "Participação": 0.141},
        {"Fonte": "Marina", "Participação": 0.132},
        {"Fonte": "Outros", "Participação": 0.054},
    ]
)


# -------------------------------
# Sidebar controls
# -------------------------------
st.sidebar.header("Filtros")
selected_year = st.sidebar.selectbox("Ano", options=[2025], index=0)
selected_months = st.sidebar.multiselect(
    "Meses",
    options=list(evolucao_df.sort_values("Mês")["Mês"].astype(str)),
    default=list(evolucao_df.sort_values("Mês")["Mês"].astype(str)),
)

st.sidebar.markdown("---")
st.sidebar.subheader("Carregar dados (opcional)")
controle_file = st.sidebar.file_uploader("Controle Comercial (Excel)", type=["xlsx", "xlsb", "xls"])
esp_file = st.sidebar.file_uploader("Ranking Especialistas (Excel)", type=["xlsx", "xlsb", "xls"])
neg_file = st.sidebar.file_uploader("Ranking Negociadores (Excel)", type=["xlsx", "xlsb", "xls"])

if controle_file or esp_file or neg_file:
    st.sidebar.info(
        "Arquivos enviados. O app usa dados embutidos como padrão; integração automática \n"
        "com arquivos enviados pode ser configurada em uma próxima etapa."
    )


# -------------------------------
# Header
# -------------------------------
st.title("Dashboard Precavida Brasil - Análise Comercial 2025")
st.caption(
    "Visão 360º das operações comerciais de 2025 com KPIs, evolução temporal, análise por praças e rankings de performance."
)


# -------------------------------
# KPI Cards
# -------------------------------
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Precatórios Comprados 📊", f"{TOTAL_QTD_PRECS}")
col2.metric("Valor Total Precatórios 💰", format_currency_brl_compact(TOTAL_VALOR_PRECS))
col3.metric("Ticket Médio Precatório 📈", format_currency_brl_compact(TICKET_MEDIO_PRECAT))
col4.metric("Percentual Pago ✅", percent_str(PERCENTUAL_PAGO))
col5.metric("Aporte Total 🤝", format_currency_brl_compact(TOTAL_APORTE))
col6.metric("Ticket Médio Aporte 🎯", format_currency_brl_compact(TICKET_MEDIO_APORTE))

st.markdown(
    f"Maior operação individual: **{format_currency_brl_compact(MAX_OPERACAO)}**"
)

st.markdown("---")


# -------------------------------
# Top Praças + Distribuição por Fonte
# -------------------------------
left, right = st.columns([2, 1])

with left:
    st.subheader("Top 5 Praças por Valor de Precatórios")
    fig_pracas = px.bar(
        pracas_df,
        x="Praça",
        y="Valor BRL",
        text=pracas_df["Valor BRL"].apply(format_currency_brl_compact),
        color="Praça",
        color_discrete_sequence=px.colors.sequential.Blues_r,
    )
    fig_pracas.update_layout(
        showlegend=False,
        yaxis_title="Valor de Precatórios (BRL)",
        xaxis_title="",
        margin=dict(l=10, r=10, t=10, b=10),
        height=380,
    )
    st.plotly_chart(fig_pracas, use_container_width=True)

with right:
    st.subheader("Distribuição por Fonte")
    fig_fontes = px.pie(
        fontes_df,
        names="Fonte",
        values="Participação",
        color_discrete_sequence=px.colors.sequential.RdBu,
        hole=0.35,
    )
    fig_fontes.update_traces(textinfo="percent+label")
    fig_fontes.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=380)
    st.plotly_chart(fig_fontes, use_container_width=True)


# -------------------------------
# Evolução Mensal 2025
# -------------------------------
if selected_months:
    evolucao_filtered = evolucao_df[evolucao_df["Mês"].astype(str).isin(selected_months)].copy()
else:
    evolucao_filtered = evolucao_df.copy()

st.subheader("Evolução Mensal 2025")
col_a, col_b = st.columns(2)

with col_a:
    fig_evol_valor = px.bar(
        evolucao_filtered.sort_values("Mês"),
        x="Mês",
        y=["Valor Precatórios", "Valor Aportado"],
        barmode="group",
        labels={"value": "Valor (BRL)", "variable": "Indicador"},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_evol_valor.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=420)
    st.plotly_chart(fig_evol_valor, use_container_width=True)

with col_b:
    fig_evol_qtd = px.line(
        evolucao_filtered.sort_values("Mês"),
        x="Mês",
        y="Qtd Precatórios",
        markers=True,
        color_discrete_sequence=["#2E86DE"],
    )
    fig_evol_qtd.update_layout(
        yaxis_title="Quantidade",
        margin=dict(l=10, r=10, t=10, b=10),
        height=420,
    )
    st.plotly_chart(fig_evol_qtd, use_container_width=True)


# -------------------------------
# Análise por Praça (tabela)
# -------------------------------
st.subheader("Análise por Praça")
pracas_display = pracas_df[["Praça", "Qtd Precatórios", "Valor (M)", "Aporte (M)", "Participação"]].copy()
pracas_display["Participação"] = pracas_display["Participação"].apply(lambda x: f"{x*100:.1f}%".replace(".", ","))
st.dataframe(
    pracas_display,
    use_container_width=True,
    hide_index=True,
)


# -------------------------------
# Performance dos Especialistas e Negociadores
# -------------------------------
st.subheader("Performance dos Especialistas")
fig_espec = px.bar(
    especialistas_df,
    x="Especialista",
    y="Valor BRL",
    text=especialistas_df["Valor BRL"].apply(format_currency_brl_compact),
    color="Especialista",
    color_discrete_sequence=px.colors.sequential.Teal_r,
)
fig_espec.update_layout(showlegend=False, yaxis_title="Valor (BRL)", xaxis_title="", height=420)
st.plotly_chart(fig_espec, use_container_width=True)

st.subheader("Performance dos Negociadores")
fig_neg = px.bar(
    negociadores_df,
    x="Negociador",
    y="Valor BRL",
    text=negociadores_df["Valor BRL"].apply(format_currency_brl_compact),
    color="Negociador",
    color_discrete_sequence=px.colors.sequential.OrRd,
)
fig_neg.update_layout(showlegend=False, yaxis_title="Valor (BRL)", xaxis_title="", height=420)
st.plotly_chart(fig_neg, use_container_width=True)


# -------------------------------
# Insights Estratégicos (static)
# -------------------------------
st.markdown("---")
st.subheader("Insights Estratégicos")

insights = [
    ("Concentração Geográfica", [
        "Minas Gerais domina com ~67% do volume total",
        "Diversificação em 16 praças oferece oportunidades de expansão",
    ]),
    ("Sazonalidade e Crescimento", [
        "Maio registrou pico com R$ 12,9M em precatórios",
        "Crescimento médio mensal de ~23% no 1º semestre",
        "Julho mostra desaceleração que requer atenção",
    ]),
    ("Eficiência Operacional", [
        f"Taxa de pagamento de {percent_str(PERCENTUAL_PAGO)} demonstra boa liquidez",
        f"Ticket médio de {format_currency_brl_compact(TICKET_MEDIO_PRECAT)} indica operações de médio porte",
        f"Maior operação individual: {format_currency_brl_compact(MAX_OPERACAO)}",
    ]),
]

for title, bullets in insights:
    st.markdown(f"**{title}**")
    for b in bullets:
        st.markdown(f"- {b}")


# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption(
    "Dashboard demonstrativo baseado no resumo executivo de 2025. Upload de arquivos Excel disponível para futura integração.")
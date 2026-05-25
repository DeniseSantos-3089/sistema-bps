import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# =========================
# CONFIGURAÇÃO
# =========================
st.set_page_config(
    page_title="Dashboard BPS",
    layout="wide"
)

# =========================
# HEADER ESTILO POWER BI
# =========================
st.markdown("""
    <div style='background-color:#1F4E79;padding:15px;border-radius:10px'>
    <h2 style='color:white;text-align:center;'>Dashboard de Performance BPS</h2>
    </div>
""", unsafe_allow_html=True)

st.write("")

# =========================
# DADOS
# =========================
data = {
    "Periodo": [1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6],
    "Equipe": [
        "Jurídico","Jurídico","Jurídico","Jurídico","Jurídico","Jurídico",
        "Telecom","Telecom","Telecom","Telecom","Telecom","Telecom",
        "Fraude","Fraude","Fraude","Fraude","Fraude","Fraude",
        "Suporte","Suporte","Suporte","Suporte","Suporte","Suporte"
    ],
    "Score": [
        0.78,0.80,0.82,0.83,0.84,0.85,
        0.70,0.72,0.75,0.76,0.77,0.78,
        0.72,0.68,0.65,0.60,0.58,0.55,
        0.80,0.85,0.88,0.90,0.92,0.95
    ]
}

df = pd.DataFrame(data)

# =========================
# FILTRO LATERAL
# =========================
st.sidebar.markdown("## Filtros")

equipe = st.sidebar.selectbox(
    "Selecione a equipe:",
    df["Equipe"].unique()
)

df_filtrado = df[df["Equipe"] == equipe]

# =========================
# KPIs (POWER BI STYLE)
# =========================
st.markdown("## Indicadores")

col1, col2, col3 = st.columns(3)

media = df_filtrado["Score"].mean()
maximo = df_filtrado["Score"].max()
minimo = df_filtrado["Score"].min()

col1.metric("Média", round(media,2))
col2.metric("Melhor", round(maximo,2))
col3.metric("Pior", round(minimo,2))

# =========================
# GRÁFICO DE LINHA
# =========================
st.markdown("## Evolução")

fig1 = px.line(
    df_filtrado,
    x="Periodo",
    y="Score",
    markers=True,
    title=f"Evolução - {equipe}"
)

fig1.update_layout(
    template="simple_white"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# COMPARAÇÃO ENTRE EQUIPES
# =========================
st.markdown("## Comparação Geral")

fig2 = px.line(
    df,
    x="Periodo",
    y="Score",
    color="Equipe",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# IA MAIS AVANÇADA (REGRESSÃO)
# =========================
st.markdown("## Previsão Inteligente")

x = df_filtrado["Periodo"]
y = df_filtrado["Score"]

coef = np.polyfit(x, y, 2)  # grau 2 (mais preciso)
modelo = np.poly1d(coef)

futuro = np.arange(max(x)+1, max(x)+4)
previsao = modelo(futuro)

for periodo, valor in zip(futuro, previsao):
    st.write(f"Período {periodo}: {round(valor,2)}")

# =========================
# GRÁFICO DA PREVISÃO
# =========================
df_prev = pd.DataFrame({
    "Periodo": list(x) + list(futuro),
    "Score": list(y) + list(previsao),
    "Tipo": ["Real"]*len(x) + ["Previsto"]*len(futuro)
})

fig3 = px.line(
    df_prev,
    x="Periodo",
    y="Score",
    color="Tipo",
    markers=True,
    title="Previsão vs Real"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# ALERTA INTELIGENTE
# =========================
st.markdown("## Alerta")

if previsao[-1] < media:
    st.error("Risco de queda de performance")
elif previsao[-1] > media:
    st.success("Tendência de crescimento")
else:
    st.warning("Estabilidade")

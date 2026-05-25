import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# =============================
# CONFIGURAÇÃO DA PÁGINA
# =============================
st.set_page_config(
    page_title="Dashboard BPS",
    layout="wide"
)

# =============================
# TÍTULO ESTILO EMPRESA
# =============================
st.markdown(
    "<h1 style='text-align: center; color: #2E86C1;'>Dashboard de Performance BPS</h1>",
    unsafe_allow_html=True
)

st.markdown("---")

# =============================
# DADOS (COM HISTÓRICO)
# =============================
data = {
    "Periodo": [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4],
    "Equipe": [
        "Jurídico","Jurídico","Jurídico","Jurídico",
        "Telecom","Telecom","Telecom","Telecom",
        "Fraude","Fraude","Fraude","Fraude",
        "Suporte","Suporte","Suporte","Suporte"
    ],
    "Score": [
        0.78,0.80,0.82,0.83,
        0.70,0.72,0.75,0.76,
        0.72,0.68,0.65,0.60,
        0.80,0.85,0.88,0.90
    ]
}

df = pd.DataFrame(data)

# =============================
# FILTRO
# =============================
st.sidebar.header("Filtro")

equipe = st.sidebar.selectbox(
    "Selecione a equipe:",
    df["Equipe"].unique()
)

df_filtrado = df[df["Equipe"] == equipe]

# =============================
# KPIs (NÍVEL EMPRESA)
# =============================
st.subheader("Indicadores")

col1, col2, col3 = st.columns(3)

media = df_filtrado["Score"].mean()
maximo = df_filtrado["Score"].max()
minimo = df_filtrado["Score"].min()

col1.metric("Média", round(media,2))
col2.metric("Melhor valor", round(maximo,2))
col3.metric("Pior valor", round(minimo,2))

# =============================
# GRÁFICO EVOLUÇÃO
# =============================
st.subheader("Evolução da Equipe")

fig1 = px.line(
    df_filtrado,
    x="Periodo",
    y="Score",
    markers=True
)

fig1.update_layout(
    plot_bgcolor="white"
)

st.plotly_chart(fig1, use_container_width=True)

# =============================
# COMPARAÇÃO ENTRE EQUIPES
# =============================
st.subheader("Comparação Geral")

fig2 = px.line(
    df,
    x="Periodo",
    y="Score",
    color="Equipe",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# =============================
# PREVISÃO COM IA
# =============================
st.subheader("Previsão de Tendência")

x = df_filtrado["Periodo"].values
y = df_filtrado["Score"].values

coef = np.polyfit(x, y, 1)
funcao = np.poly1d(coef)

futuro = [5,6,7]
previsao = funcao(futuro)

for i, valor in enumerate(previsao):
    st.write(f"Período {futuro[i]}: {round(valor,2)}")

# =============================
# ALERTA INTELIGENTE
# =============================
st.subheader("Alerta Inteligente")

if previsao[-1] < media:
    st.error("Tendência de queda")
elif previsao[-1] > media:
    st.success("Tendência de crescimento")
else:
    st.warning("Tendência estável")


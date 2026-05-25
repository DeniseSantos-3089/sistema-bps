import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAÇÃO
st.set_page_config(page_title="Sistema BPS", layout="wide")

# TÍTULO
st.title("Sistema de Performance BPS")

# DADOS COM HISTÓRICO (IMPORTANTE)
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

# ===================================
# FILTRO
# ===================================
st.sidebar.header("Filtro")

equipe = st.sidebar.selectbox(
    "Escolhe a equipe:",
    df["Equipe"].unique()
)

df_filtrado = df[df["Equipe"] == equipe]

# ===================================
# GRÁFICO DE LINHA (Evolução)
# ===================================
st.subheader("Evolução da Equipe")

fig1 = px.line(
    df_filtrado,
    x="Periodo",
    y="Score",
    markers=True
)

st.plotly_chart(fig1)

# ===================================
# GRÁFICO DE COMPARAÇÃO
# ===================================
st.subheader("Comparação entre Equipes")

fig2 = px.line(
    df,
    x="Periodo",
    y="Score",
    color="Equipe",
    markers=True
)

st.plotly_chart(fig2)

# ===================================
# ANÁLISE
# ===================================
media = df.groupby("Equipe")["Score"].mean()

melhor = media.idxmax()
pior = media.idxmin()

st.success(f"Melhor equipe: {melhor}")
st.warning(f"Ponto de atenção: {pior}")

# ===================================
# ALERTA
# ===================================
if media[pior] < 0.7:
    st.error("Existe equipe com baixo desempenho")
else:
    st.success("Tudo dentro do esperado")

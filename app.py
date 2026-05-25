import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

# =========================
# CONFIGURAÇÃO
# =========================
st.set_page_config(page_title="Painel Executivo BPS", layout="wide")

# =========================
# TÍTULO
# =========================
st.title("Painel Executivo de Performance BPS")

# =========================
# DADOS
# =========================
data = {
    "Periodo": list(range(1,11))*4,
    "Equipe": ["Jurídico"]*10 + ["Telecom"]*10 + ["Fraude"]*10 + ["Suporte"]*10,
    "Score": [
        0.78,0.80,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,
        0.70,0.72,0.75,0.76,0.77,0.78,0.79,0.80,0.81,0.82,
        0.72,0.68,0.65,0.60,0.58,0.55,0.53,0.52,0.50,0.48,
        0.80,0.85,0.88,0.90,0.92,0.94,0.95,0.96,0.97,0.98
    ]
}

df = pd.DataFrame(data)

# =========================
# FILTRO
# =========================
st.sidebar.title("Filtros")

equipe = st.sidebar.selectbox(
    "Selecione a equipe:",
    df["Equipe"].unique()
)

df_filtrado = df[df["Equipe"] == equipe]

# =========================
# KPIs
# =========================
col1, col2, col3 = st.columns(3)

media = df_filtrado["Score"].mean()
atual = df_filtrado["Score"].iloc[-1]
crescimento = atual - df_filtrado["Score"].iloc[0]

col1.metric("Média", round(media,2))
col2.metric("Atual", round(atual,2))
col3.metric("Crescimento", round(crescimento,2))

# =========================
# GRÁFICO DE LINHA
# =========================
st.subheader("Evolução da Equipe")

fig1 = px.line(
    df_filtrado,
    x="Periodo",
    y="Score",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# COMPARAÇÃO ENTRE EQUIPES
# =========================
st.subheader("Comparação Geral")

fig2 = px.line(
    df,
    x="Periodo",
    y="Score",
    color="Equipe",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# IA REAL (Machine Learning)
# =========================
st.subheader("Previsão com Inteligência Artificial")

X = df_filtrado[["Periodo"]]
y = df_filtrado["Score"]

modelo = LinearRegression()
modelo.fit(X, y)

futuro = pd.DataFrame({"Periodo":[11,12,13,14]})
previsao = modelo.predict(futuro)

for i in range(len(futuro)):
    st.write(f"Período {futuro.iloc[i,0]}: {round(previsao[i],2)}")

# =========================
# GRÁFICO PREVISÃO
# =========================
df_previsao = pd.concat([
    df_filtrado,
    pd.DataFrame({
        "Periodo": futuro["Periodo"],
        "Score": previsao,
        "Equipe": equipe
    })
])

fig3 = px.line(
    df_previsao,
    x="Periodo",
    y="Score",
    markers=True
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# ALERTA INTELIGENTE
# =========================
st.subheader("Análise")

if previsao[-1] < media:
    st.error("Risco de queda de performance")
elif previsao[-1] > media:
    st.success("Tendência de crescimento")
else:
    st.warning("Estabilidade")

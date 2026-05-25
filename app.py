import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# =========================
# CONFIGURAÇÃO
# =========================
st.set_page_config(page_title="Painel Executivo BPS", layout="wide")

# =========================
# HEADER ESTILO DIRETORIA
# =========================
st.markdown("""
<div style='background-color:#0E2A47;padding:20px;border-radius:10px'>
<h1 style='color:white;text-align:center;'>Painel Executivo BPS</h1>
</div>
""", unsafe_allow_html=True)

st.write("")

# =========================
# DADOS MAIS COMPLETOS
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
equipe = st.sidebar.selectbox("Selecione a equipe", df["Equipe"].unique())

df_filtrado = df[df["Equipe"] == equipe]

# =========================
# KPIs (ESTILO DIRETOR)
# =========================
col1, col2, col3, col4 = st.columns(4)

media = df_filtrado["Score"].mean()
crescimento = df_filtrado["Score"].iloc[-1] - df_filtrado["Score"].iloc[0]

col1.metric("Média", round(media,2))
col2.metric("Último Score", round(df_filtrado["Score"].iloc[-1],2))
col3.metric("Crescimento", round(crescimento,2))
col4.metric("Registros", len(df_filtrado))

# =========================
# GRÁFICO PRINCIPAL
# =========================
st.markdown("### Evolução de Performance")

fig = px.line(
    df_filtrado,
    x="Periodo",
    y="Score",
    markers=True
)

fig.update_layout(
    plot_bgcolor="#F4F6F6",
    paper_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# IA REAL (REGRESSÃO + TENDÊNCIA)
# =========================
st.markdown("### Inteligência Artificial (Machine Learning)")

x = df_filtrado["Periodo"].values
y = df_filtrado["Score"].values

# modelo linear + tendência
coef = np.polyfit(x, y, 2)
modelo = np.poly1d(coef)

# prever futuro
futuro = np.arange(max(x)+1, max(x)+6)
previsao = modelo(futuro)

# mostrar previsão
st.markdown("#### Previsão futura")
for p, v in zip(futuro, previsao):
    st.write(f"Período {p}: {round(v,2)}")

# =========================
# GRÁFICO PREVISÃO
# =========================
df_previsao = pd.DataFrame({
    "Periodo": list(x) + list(futuro),
    "Score": list(y) + list(previsao),
    "Tipo": ["Real"]*len(x) + ["Previsto"]*len(futuro)
})

fig2 = px.line(
    df_previsao,
    x="Periodo",
    y="Score",
    color="Tipo",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# COMPARAÇÃO GERAL
# =========================
st.markdown("### Comparação entre Equipes")

fig3 = px.line(
    df,
    x="Periodo",
    y="Score",
    color="Equipe"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# ALERTA INTELIGENTE
# =========================
st.markdown("### Insights Automáticos")

if previsao[-1] < media:
    st.error("Queda prevista: atenção necessária")
elif previsao[-1] > media + 0.05:
    st.success("Crescimento forte projetado")
else:
    st.warning("Estabilidade prevista")


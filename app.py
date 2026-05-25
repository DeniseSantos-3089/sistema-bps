import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Painel Executivo BPS", layout="wide")

# =========================
# HEADER DIRETOR
# =========================
st.markdown("""
<div style='background-color:#0B1F3A;padding:20px;border-radius:10px'>
<h1 style='color:white;text-align:center;'>Painel Executivo BPS</h1>
</div>
""", unsafe_allow_html=True)

st.write("")

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
equipe = st.sidebar.selectbox("Equipe", df["Equipe"].unique())
df_filtrado = df[df["Equipe"] == equipe]

# =========================
# KPIs DIRETORIA
# =========================
col1, col2, col3, col4 = st.columns(4)

media = df_filtrado["Score"].mean()
atual = df_filtrado["Score"].iloc[-1]
crescimento = atual - df_filtrado["Score"].iloc[0]
tendencia = "Alta" if crescimento > 0 else "Queda"

col1.metric("Média", round(media,2))
col2.metric("Atual", round(atual,2))
col3.metric("Crescimento", round(crescimento,2))
col4.metric("Tendência", tendencia)

# =========================
# GRÁFICO PRINCIPAL
# =========================
st.markdown("### Evolução")

fig1 = px.line(df_filtrado, x="Periodo", y="Score", markers=True)
st.plotly_chart(fig1, use_container_width=True)

# =========================
# IA (Machine Learning)
# =========================
st.markdown("### Previsão com IA")

X = df_filtrado[["Periodo"]]
y = df_filtrado["Score"]

modelo = LinearRegression()
modelo.fit(X, y)

futuro = pd.DataFrame({"Periodo":[11,12,13,14]})
previsao = modelo.predict(futuro)

# =========================
# GRÁFICO REAL vs PREVISÃO
# =========================
df_real = df_filtrado.copy()
df_real["Tipo"] = "Real"

df_prev = pd.DataFrame({
    "Periodo": futuro["Periodo"],
    "Score": previsao,
    "Equipe": equipe,
    "Tipo": "Previsto"
})

df_final = pd.concat([df_real, df_prev])

fig2 = px.line(
    df_final,
    x="Periodo",
    y="Score",
    color="Tipo",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# RANKING DAS EQUIPES
# =========================
st.markdown("### Ranking das Equipes")

ranking = df.groupby("Equipe")["Score"].mean().sort_values(ascending=False)
st.dataframe(ranking)

# =========================
# ALERTA ESTRATÉGICO
# =========================
st.markdown("### Insights Executivos")

if previsao[-1] < media:
    st.error("Queda prevista - intervenção necessária")
elif previsao[-1] > media:
    st.success("Crescimento sustentável identificado")
else:
    st.warning("Estabilidade - manter estratégia atual")



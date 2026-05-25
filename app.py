import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

# =========================
# CONFIGURAÇÃO
# =========================
st.set_page_config(page_title="Painel Executivo BPS", layout="wide")

# =========================
# HEADER
# =========================
st.markdown("""
<div style='background-color:#0B1F3A;padding:20px;border-radius:10px'>
<h1 style='color:white;text-align:center;'>Painel Executivo BPS</h1>
</div>
""", unsafe_allow_html=True)

st.write("")

# =========================
# UPLOAD DE EXCEL
# =========================
arquivo = st.file_uploader("Carregue seu Excel", type=["xlsx"])

if arquivo is not None:
    df = pd.read_excel(arquivo)
else:
    st.warning("Usando dados padrão")

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
# VALIDAÇÃO (IMPORTANTE)
# =========================
colunas_necessarias = ["Periodo", "Equipe", "Score"]

if not all(col in df.columns for col in colunas_necessarias):
    st.error("O Excel precisa ter as colunas: Periodo, Equipe, Score")
    st.stop()

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
# GRÁFICO REAL
# =========================
st.subheader("Evolução Real")

fig1 = px.line(
    df_filtrado,
    x="Periodo",
    y="Score",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# IA (Machine Learning)
# =========================
st.subheader("Previsão com IA")

X = df_filtrado[["Periodo"]]
y = df_filtrado["Score"]

modelo = LinearRegression()
modelo.fit(X, y)

futuro = pd.DataFrame({"Periodo": list(range(max(df_filtrado["Periodo"])+1, max(df_filtrado["Periodo"])+5))})
previsao = modelo.predict(futuro)

# =========================
# REAL + PREVISÃO
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

# =========================
# GRÁFICO FINAL
# =========================
st.subheader("Real vs Previsão")

fig2 = px.line(
    df_final,
    x="Periodo",
    y="Score",
    color="Tipo",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# COMPARAÇÃO
# =========================
st.subheader("Comparação Geral")

fig3 = px.line(
    df,
    x="Periodo",
    y="Score",
    color="Equipe"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# ALERTA
# =========================
st.subheader("Insights")

if previsao[-1] < media:
    st.error("Risco de queda futura")
elif previsao[-1] > media:
    st.success("Tendência de crescimento")
else:
    st.warning("Estabilidade")



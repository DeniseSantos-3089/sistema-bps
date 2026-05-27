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

        "Qualidade": [
            0.80,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.90,
            0.72,0.74,0.76,0.78,0.79,0.80,0.81,0.82,0.83,0.84,
            0.68,0.65,0.62,0.60,0.58,0.56,0.54,0.52,0.50,0.48,
            0.85,0.88,0.90,0.92,0.94,0.95,0.96,0.97,0.98,0.99
        ],

        "Realizado": [80]*40,
        "Meta": [100]*40
    }

    df = pd.DataFrame(data)

# =========================
# VALIDAÇÃO
# =========================
colunas = ["Periodo", "Equipe", "Qualidade", "Realizado", "Meta"]

if not all(col in df.columns for col in colunas):
    st.error("O Excel precisa ter: Periodo, Equipe, Qualidade, Realizado, Meta")
    st.stop()

if (df["Meta"] == 0).any():
    st.error("Existe meta igual a 0 no arquivo")
    st.stop()

# =========================
# CÁLCULOS AUTOMÁTICOS
# =========================
df["Volumetria"] = df["Realizado"] / df["Meta"]
df["Score"] = (df["Qualidade"] + df["Volumetria"]) / 2

# =========================
# EXPLICAÇÃO DO SCORE
# =========================
st.info("""
Score automático:

Qualidade = precisão  
Volumetria = Realizado / Meta  

Score = (Qualidade + Volumetria) / 2
""")

# =========================
# FILTRO
# =========================
st.sidebar.title("Filtros")

equipe = st.sidebar.selectbox("Equipe:", df["Equipe"].unique())
df_filtrado = df[df["Equipe"] == equipe]

# =========================
# KPIs
# =========================
col1, col2, col3, col4, col5, col6 = st.columns(6)

media = df_filtrado["Score"].mean()
atual = df_filtrado["Score"].iloc[-1]
crescimento = atual - df_filtrado["Score"].iloc[0]

qualidade_media = df_filtrado["Qualidade"].mean()
volumetria_media = df_filtrado["Volumetria"].mean()

atingiu_meta = "✅" if df_filtrado["Volumetria"].iloc[-1] >= 1 else "❌"

col1.metric("Média", round(media,2))
col2.metric("Atual", round(atual,2))
col3.metric("Crescimento", round(crescimento,2))
col4.metric("Qualidade", round(qualidade_media,2))
col5.metric("Volumetria", round(volumetria_media,2))
col6.metric("Meta", atingiu_meta)

# =========================
# GRÁFICOS
# =========================
st.subheader("Evolução")

fig1 = px.line(df_filtrado, x="Periodo", y="Score", markers=True)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Qualidade vs Volumetria")

fig2 = px.line(df_filtrado, x="Periodo", y=["Qualidade","Volumetria"], markers=True)
st.plotly_chart(fig2, use_container_width=True)

# =========================
# IA (PREVISÃO)
# =========================
X = df_filtrado[["Periodo"]]
y = df_filtrado["Score"]

modelo = LinearRegression()
modelo.fit(X, y)

futuro = pd.DataFrame({
    "Periodo": list(range(max(df_filtrado["Periodo"])+1, max(df_filtrado["Periodo"])+5))
})

previsao = modelo.predict(futuro)

df_real = df_filtrado.copy()
df_real["Tipo"] = "Real"

df_prev = pd.DataFrame({
    "Periodo": futuro["Periodo"],
    "Score": previsao,
    "Tipo": "Previsto"
})

df_final = pd.concat([df_real, df_prev])

st.subheader("Previsão")

fig3 = px.line(df_final, x="Periodo", y="Score", color="Tipo", markers=True)
st.plotly_chart(fig3, use_container_width=True)

# =========================
# RANKING
# =========================
ranking = df.groupby("Equipe")["Score"].mean().reset_index()
ranking = ranking.sort_values(by="Score", ascending=False)

st.subheader("Ranking")
st.dataframe(ranking, use_container_width=True)

# =========================
# OFENSOR
# =========================
st.subheader("Ofensor")

if qualidade_media < volumetria_media:
    st.error("Ofensor: Qualidade")
elif volumetria_media < qualidade_media:
    st.warning("Ofensor: Volumetria")
else:
    st.success("Equilíbrio")

# =========================
# INSIGHTS
# =========================
st.subheader("Insights Estratégicos")

ultimo_score = df_filtrado["Score"].iloc[-1]

if previsao[-1] > ultimo_score:
    st.success("Tendência de crescimento")
elif previsao[-1] < ultimo_score:
    st.error("Tendência de queda")
else:
    st.warning("Estabilidade")

if df_filtrado["Volumetria"].iloc[-1] >= 1:
    st.success("Meta atingida")
else:
    st.warning("Meta não atingida")

if crescimento > 0:
    st.success("Evolução positiva")
else:
    st.error("Queda de performance")






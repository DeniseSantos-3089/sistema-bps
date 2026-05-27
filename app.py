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
        ],

        "Qualidade": [
            0.80,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.90,
            0.72,0.74,0.76,0.78,0.79,0.80,0.81,0.82,0.83,0.84,
            0.68,0.65,0.62,0.60,0.58,0.56,0.54,0.52,0.50,0.48,
            0.85,0.88,0.90,0.92,0.94,0.95,0.96,0.97,0.98,0.99
        ],

        "Volumetria": [
            0.76,0.78,0.80,0.82,0.83,0.84,0.85,0.86,0.87,0.88,
            0.68,0.70,0.72,0.74,0.75,0.76,0.77,0.78,0.79,0.80,
            0.70,0.66,0.63,0.60,0.58,0.56,0.54,0.53,0.51,0.50,
            0.78,0.82,0.85,0.88,0.90,0.92,0.94,0.95,0.96,0.97
        ]
    }

    df = pd.DataFrame(data)

# =========================
# VALIDAÇÃO
# =========================
colunas_necessarias = ["Periodo", "Equipe", "Score", "Qualidade", "Volumetria"]

if not all(col in df.columns for col in colunas_necessarias):
    st.error("O Excel precisa ter: Periodo, Equipe, Score, Qualidade, Volumetria")
    st.stop()

# =========================
# FILTRO
# =========================
st.sidebar.title("Filtros")

equipe = st.sidebar.selectbox("Selecione a equipe:", df["Equipe"].unique())

df_filtrado = df[df["Equipe"] == equipe]

# =========================
# KPIs + META
# =========================
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

media = df_filtrado["Score"].mean()
atual = df_filtrado["Score"].iloc[-1]
crescimento = atual - df_filtrado["Score"].iloc[0]

qualidade_media = df_filtrado["Qualidade"].mean()
volumetria_media = df_filtrado["Volumetria"].mean()

# METAS (pode mudar depois)
meta_score = 0.95
meta_qualidade = 0.95
meta_volumetria = 0.95

# Atingimento (%)
ating_score = (media / meta_score) * 100
ating_qualidade = (qualidade_media / meta_qualidade) * 100
ating_volumetria = (volumetria_media / meta_volumetria) * 100

# KPIs
col1.metric("Média", round(media,2))
col2.metric("Atual", round(atual,2))
col3.metric("Crescimento", round(crescimento,2))
col4.metric("Qualidade", round(qualidade_media,2))
col5.metric("Volumetria", round(volumetria_media,2))

# NOVO (META)
col6.metric("Meta Score (%)", f"{round(ating_score,1)}%")
col7.metric("Meta Qualidade (%)", f"{round(ating_qualidade,1)}%")
col8.metric("Meta Volumetria (%)", f"{round(ating_volumetria,1)}%")

# =========================
# GRÁFICO REAL
# =========================
st.subheader("Evolução da Equipe")

fig1 = px.line(df_filtrado, x="Periodo", y="Score", markers=True)
st.plotly_chart(fig1, use_container_width=True)

# =========================
# QUALIDADE vs VOLUMETRIA
# =========================
st.subheader("Qualidade vs Volumetria")

fig_qv = px.line(df_filtrado, x="Periodo", y=["Qualidade","Volumetria"], markers=True)
st.plotly_chart(fig_qv, use_container_width=True)

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

# REAL + PREVISÃO
df_real = df_filtrado.copy()
df_real["Tipo"] = "Real"

df_prev = pd.DataFrame({
    "Periodo": futuro["Periodo"],
    "Score": previsao,
    "Equipe": equipe,
    "Tipo": "Previsto"
})

df_final = pd.concat([df_real, df_prev])

# GRÁFICO
st.subheader("Real vs Previsão")

fig2 = px.line(df_final, x="Periodo", y="Score", color="Tipo", markers=True)
st.plotly_chart(fig2, use_container_width=True)

# =========================
# COMPARAÇÃO GERAL
# =========================
st.subheader("Comparação entre Equipes")

fig3 = px.line(df, x="Periodo", y="Score", color="Equipe")
st.plotly_chart(fig3, use_container_width=True)

# =========================
# RANKING
# =========================
st.subheader("Ranking de Performance")

ranking = df.groupby("Equipe")["Score"].mean().reset_index()
ranking = ranking.sort_values(by="Score", ascending=False)
ranking["Posição"] = range(1, len(ranking)+1)

ranking = ranking[["Posição", "Equipe", "Score"]]

st.dataframe(ranking, use_container_width=True)

# =========================
# OFENSOR
# =========================
st.subheader("Análise de Ofensor")

if qualidade_media < volumetria_media:
    st.error("Principal ofensor: QUALIDADE")
elif volumetria_media < qualidade_media:
    st.warning("Principal ofensor: VOLUMETRIA")
else:
    st.success("Equilíbrio entre qualidade e volumetria")

# =========================
# ALERTA FINAL
# =========================
st.subheader("Insights")

if previsao[-1] < media:
    st.error("Risco de queda futura")
elif previsao[-1] > media:
    st.success("Tendência de crescimento")
else:
    st.warning("Estabilidade")







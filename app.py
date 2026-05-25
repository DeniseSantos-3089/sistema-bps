import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAÇÃO
st.set_page_config(page_title="Sistema BPS", layout="wide")

# TÍTULO
st.title("Sistema BPS - Performance de Equipes")

# DADOS
data = {
    "Equipe": ["Jurídico", "Telecom", "Fraude", "Suporte"],
    "Score": [0.82, 0.75, 0.65, 0.88]
}

df = pd.DataFrame(data)

# MOSTRAR DADOS
st.subheader("Dados das equipes")
st.dataframe(df)

# GRÁFICO
st.subheader("Ranking de Equipes")

fig = px.bar(
    df,
    x="Equipe",
    y="Score",
    color="Score"
)

st.plotly_chart(fig)

# ANÁLISE
melhor = df.loc[df["Score"].idxmax()]
pior = df.loc[df["Score"].idxmin()]

st.success(f"Melhor equipe: {melhor['Equipe']} ({melhor['Score']})")
st.warning(f"Ponto de atenção: {pior['Equipe']} ({pior['Score']})")

# ALERTA
if pior["Score"] < 0.7:
    st.error("Existe equipe com baixo desempenho")
else:
    st.success("Tudo dentro do esperado")
``

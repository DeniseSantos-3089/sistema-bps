import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Dashboard BPS", layout="wide")

st.title("Sistema BPS - Performance de Equipes")

# Criar dados simples
data = {
    "Equipe": ["Jurídico", "Telecom", "Fraude", "Suporte"],
    "Score": [0.82, 0.75, 0.65, 0.88]
}

df = pd.DataFrame(data)

# Mostrar tabela
st.subheader("📋 Dados")
st.write(df)

# Gráfico
fig = px.bar(df, x="Equipe", y="Score", color="Score")
st.plotly_chart(fig)

# Alertas
st.subheader("Alertas")

alertas = df[df["Score"] < 0.7]

if not alertas.empty:
    st.error("Equipes com performance baixa:")
    st.write(alertas)
else:
    st.success("Tudo certo")
``

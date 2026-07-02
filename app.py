import streamlit as st
import pandas as pd

# ----------------------------
# LOAD DATA
# ----------------------------
#df = pd.read_csv("data/screener.csv", sep=";")
df = pd.read_csv("data/screener.csv", sep=";", decimal=",")

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.title("Filtros")

tipo = st.sidebar.multiselect(
    "Tipo de ativo",
    df["type"].unique(),
    default=df["type"].unique()
)

min_score = st.sidebar.slider(
    "Score mínimo",
    float(df["score"].min()),
    float(df["score"].max()),
    float(df["score"].min())
)

df = df[df["type"].isin(tipo)]
df = df[df["score"] >= min_score]

# ----------------------------
# SIGNAL (COMPRA/VENDA)
# ----------------------------
def signal(score):
    if score >= 2:
        return "🟢 COMPRA FORTE"
    elif score >= 0.5:
        return "🟡 NEUTRO"
    else:
        return "🔴 EVITAR"

df["sinal"] = df["score"].apply(signal)

# ----------------------------
# RANKING
# ----------------------------
df = df.sort_values("score", ascending=False)
df["rank"] = range(1, len(df) + 1)

# ----------------------------
# UI
# ----------------------------
st.title("📊 Screener de FIIs e Ações")

st.metric("Total ativos", len(df))
st.metric("Score médio", round(df["score"].mean(), 2))

st.dataframe(
    df[[
        "rank",
        "type",
        "id",
        "name",
        "score",
        "sinal",
        "dy_avg",
        "pvp_avg"
    ]],
    use_container_width=True
)

# ----------------------------
# CHART
# ----------------------------
st.subheader("Ranking por Score")

st.bar_chart(df.set_index("name")["score"])

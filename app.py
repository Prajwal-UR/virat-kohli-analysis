import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("🏏 Virat Kohli ODI Dashboard")

# LOAD DATA
df = pd.read_csv("kohli_odi_clean_dataset.csv")
bowler = pd.read_csv("kohli_vs_bowlers_final.csv")

df['Date'] = pd.to_datetime(df['Date'])
bowler['avg_numeric'] = pd.to_numeric(bowler['batting_average'], errors='coerce')

# -----------------------------
# KPIs
# -----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Runs", int(df['Runs'].sum()))
col2.metric("Matches", df.shape[0])
col3.metric("Average", round(df['Runs'].mean(), 2))
col4.metric("Strike Rate", round(df['StrikeRate'].mean(), 2))

# -----------------------------
# RUNS TREND
# -----------------------------
st.subheader("📈 Runs Over Time")

plt.figure()
plt.plot(df['Date'], df['Runs'])
plt.xticks(rotation=45)
st.pyplot(plt)

# -----------------------------
# ROLLING FORM
# -----------------------------
st.subheader("📉 Form (Rolling Avg)")

df['rolling'] = df['Runs'].rolling(10).mean()

plt.figure()
plt.plot(df['Date'], df['rolling'])
plt.xticks(rotation=45)
st.pyplot(plt)

# -----------------------------
# OPPONENT ANALYSIS
# -----------------------------
st.subheader("🆚 Opponent Performance")

opp = df.groupby('Opponent')['Runs'].mean().sort_values(ascending=False)

plt.figure()
opp.plot(kind='bar')
plt.xticks(rotation=45)
st.pyplot(plt)

# -----------------------------
# SHOT DISTRIBUTION
# -----------------------------
st.subheader("🎯 Shot Distribution")

shots = {
    'Singles': df['Singles'].sum(),
    'Fours': df['Fours'].sum(),
    'Sixes': df['Sixes'].sum()
}

plt.figure()
plt.pie(shots.values(), labels=shots.keys(), autopct='%1.1f%%')
st.pyplot(plt)

# -----------------------------
# TOP TOUGHEST BOWLERS
# -----------------------------
st.subheader("🏏 Top 3 Toughest Bowlers")

tough = bowler[
    (bowler['balls_faced'] > 30) &
    (bowler['avg_numeric'].notna()) &
    (bowler['dismissals'] > 0)
].sort_values(by='avg_numeric').head(3)

st.dataframe(tough[['Bowler','avg_numeric','dismissals']])

# -----------------------------
# TOP DOMINATED BOWLERS
# -----------------------------
st.subheader("🔥 Top 3 Dominated Bowlers")

easy = bowler[
    (bowler['balls_faced'] > 30) &
    (bowler['avg_numeric'].notna())
].sort_values(by='avg_numeric', ascending=False).head(3)

st.dataframe(easy[['Bowler','avg_numeric','runs_scored']])

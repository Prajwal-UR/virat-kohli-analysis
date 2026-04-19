import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# TITLE
# -----------------------------
st.title("🏏 Virat Kohli ODI Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("kohli_odi_clean_dataset.csv")
bowler = pd.read_csv("kohli_vs_bowlers_final.csv")

# Convert date
df['Date'] = pd.to_datetime(df['Date'])

# -----------------------------
# BASIC CHECK
# -----------------------------
st.subheader("Dataset Preview")
st.write(df.head())

# -----------------------------
# KPIs
# -----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Runs", int(df['Runs'].sum()))
col2.metric("Matches", df.shape[0])
col3.metric("Average Runs", round(df['Runs'].mean(), 2))

# -----------------------------
# RUNS OVER TIME
# -----------------------------
st.subheader("📈 Runs Over Time")

plt.figure()
plt.plot(df['Date'], df['Runs'])
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
# BOWLER ANALYSIS
# -----------------------------
st.subheader("🏏 Top 3 Toughest Bowlers")

bowler['avg_numeric'] = pd.to_numeric(bowler['batting_average'], errors='coerce')

tough = bowler[
    (bowler['balls_faced'] > 30) &
    (bowler['avg_numeric'].notna()) &
    (bowler['dismissals'] > 0)
].sort_values(by='avg_numeric').head(3)

st.write(tough[['Bowler','avg_numeric','dismissals']])

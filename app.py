import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# -----------------------------
# HEADER (IMAGE + TITLE)
# -----------------------------
col1, col2 = st.columns([1.5, 5])

with col1:
    st.markdown("<br><br>", unsafe_allow_html=True)  # pushes image down
    st.image("virat.jpg", width=160)

with col2:
    st.title("Virat Kohli ODI Performance Dashboard 🏏")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("kohli_odi_clean_dataset.csv")
bowler = pd.read_csv("kohli_vs_bowlers_final.csv")

df['Date'] = pd.to_datetime(df['Date'])
bowler['avg_numeric'] = pd.to_numeric(bowler['batting_average'], errors='coerce')

# -----------------------------
# 🎛️ FILTERS
# -----------------------------
st.sidebar.header("Filters")

year = st.sidebar.selectbox("Select Year", ["All"] + sorted(df['Date'].dt.year.unique()))

if year != "All":
    df = df[df['Date'].dt.year == year]

# -----------------------------
# 1. OVERALL PERFORMANCE SUMMARY
# -----------------------------
st.subheader("📊 Overall Performance Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Runs", int(df['Runs'].sum()))
col2.metric("Matches Played", df.shape[0])
col3.metric("Batting Average", round(df['Runs'].mean(), 2))
col4.metric("Strike Rate", round(df['StrikeRate'].mean(), 2))

# -----------------------------
# 2. CAREER GROWTH OVER TIME
# -----------------------------
st.subheader("📈 Career Growth Over Time")

plt.figure()
plt.plot(df['Date'], df['Runs'])
plt.xticks(rotation=45)
st.pyplot(plt)

# -----------------------------
# 3. CURRENT FORM & STABILITY
# -----------------------------
st.subheader("📉 Current Form & Stability")

df['rolling_avg'] = df['Runs'].rolling(10).mean()

plt.figure()
plt.plot(df['Date'], df['rolling_avg'])
plt.xticks(rotation=45)
st.pyplot(plt)

consistency = df['Runs'].mean() / df['Runs'].std()
st.metric("Consistency Score", round(consistency, 2))

# -----------------------------
# 4. PERFORMANCE AGAINST TEAMS
# -----------------------------
st.subheader("🆚 Performance Against Different Teams")

opp = df.groupby('Opponent')['Runs'].mean().sort_values(ascending=False)

plt.figure()
opp.plot(kind='bar')
plt.xticks(rotation=45)
st.pyplot(plt)

# -----------------------------
# 5. PERFORMANCE ACROSS STADIUMS
# -----------------------------
st.subheader("🏟️ Performance Across Stadiums")

venue = df.groupby('Venue')['Runs'].mean().sort_values(ascending=False)

st.bar_chart(venue)

# -----------------------------
# 6. BATTING STYLE BREAKDOWN
# -----------------------------
st.subheader("🎯 Batting Style Breakdown")

shots = {
    'Singles': df['Singles'].sum(),
    'Fours': df['Fours'].sum(),
    'Sixes': df['Sixes'].sum()
}

plt.figure()
plt.pie(shots.values(), labels=shots.keys(), autopct='%1.1f%%')
st.pyplot(plt)

# -----------------------------
# 7. CONVERSION ABILITY
# -----------------------------
st.subheader("🎯 Ability to Convert Starts into Big Scores")

total_50s = df['50s'].sum()
total_100s = df['100s'].sum()

conversion = (total_100s / (total_50s + total_100s)) * 100 if (total_50s + total_100s) > 0 else 0

st.metric("Conversion Rate (50 → 100)", f"{conversion:.1f}%")

# -----------------------------
# 8. BOWLER MATCHUP ANALYSIS
# -----------------------------
st.subheader("🏏 Performance Against Bowlers (Key Insights)")

tough = bowler[
    (bowler['balls_faced'] > 30) &
    (bowler['avg_numeric'].notna()) &
    (bowler['dismissals'] > 0)
].sort_values(by='avg_numeric').head(3)

easy = bowler[
    (bowler['balls_faced'] > 30) &
    (bowler['avg_numeric'].notna())
].sort_values(by='avg_numeric', ascending=False).head(3)

col1, col2 = st.columns(2)

with col1:
    st.write("🔥 Toughest Bowlers")
    st.dataframe(tough[['Bowler','avg_numeric','dismissals']])

with col2:
    st.write("💪 Dominated Bowlers")
    st.dataframe(easy[['Bowler','avg_numeric','runs_scored']])

# Scatter
st.subheader("📊 Average vs Strike Rate")

plt.figure()
plt.scatter(bowler['avg_numeric'], bowler['strike_rate'])
plt.xlabel("Average")
plt.ylabel("Strike Rate")
st.pyplot(plt)

# -----------------------------
# 9. PERFORMANCE BY YEAR
# -----------------------------
st.subheader("📅 Performance by Year")

yearly = df.groupby(df['Date'].dt.year)['Runs'].sum()

st.line_chart(yearly)

# -----------------------------
# 10. BEST PERFORMANCES
# -----------------------------
st.subheader("🔥 Best Performances (Top Innings)")

top_scores = df.sort_values(by='Runs', ascending=False).head(10)

st.dataframe(top_scores[['Date','Opponent','Runs']])

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# -----------------------------
# HEADER (IMAGE + TITLE)
# -----------------------------
col1, col2 = st.columns([4, 6])   # give much more space to image

with col1:
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("virat.jpg", use_container_width=True)

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
st.subheader("📈 Career Growth(Runs Scored Over Time)")

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
st.subheader("🆚 Performance Against Different Teams(Avg Runs Scored)")

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
# -----------------------------
# -----------------------------
# 🎯 BATTING STYLE BREAKDOWN
# -----------------------------
st.subheader("🎯 Batting Style Breakdown")

# Calculate totals
singles = df['Singles'].sum()
doubles = df['Doubles'].sum()
triples = df['Triples'].sum()
fours = df['Fours'].sum()
sixes = df['Sixes'].sum()

labels = ['Singles', 'Doubles', 'Triples', 'Fours', 'Sixes']
values = [singles, doubles, triples, fours, sixes]

total_runs = sum(values)

# -----------------------------
# BAR CHART (MAIN VISUAL)
# -----------------------------
shot_df = pd.DataFrame({
    'Shot Type': labels,
    'Runs': values
})

plt.figure(figsize=(10,5))
plt.bar(shot_df['Shot Type'], shot_df['Runs'])

plt.title("Run Distribution by Shot Type")
plt.xlabel("Shot Type")
plt.ylabel("Runs")

plt.grid(axis='y', alpha=0.3)

st.pyplot(plt)

# -----------------------------
# TOTAL RUNS
# -----------------------------
st.markdown(f"**Total Runs from Shots: {total_runs}**")

# -----------------------------
# INSIGHT
# -----------------------------
top_shot = labels[values.index(max(values))]
st.info(f"Most runs are scored through: **{top_shot}**")
# 7. CONVERSION ABILITY
# -----------------------------
st.subheader("🎯 Ability to Convert Starts into Big Scores")

total_50s = df['50s'].sum()
total_100s = df['100s'].sum()

conversion = (total_100s / (total_50s + total_100s)) * 100 if (total_50s + total_100s) > 0 else 0

st.metric("Conversion Rate (50 → 100)", f"{conversion:.1f}%")

# -----------------------------
# 11. CENTURIES AGAINST OPPONENTS
# -----------------------------
st.subheader("🏏 Centuries Against Opponents")

centuries = df[df['Runs'] >= 100]

centuries_count = centuries.groupby('Opponent').size().sort_values(ascending=False)

plt.figure()
centuries_count.plot(kind='bar')
plt.xlabel("Opponent")
plt.ylabel("Number of Centuries")
plt.xticks(rotation=45)
st.pyplot(plt)

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
# -----------------------------
# 📊 SCORE DISTRIBUTION (PERFORMANCE LEVEL)
# -----------------------------
st.subheader("📊 Score Distribution by Performance Level")

# Create categories
low = df[df['Runs'] < 30].shape[0]
medium = df[(df['Runs'] >= 30) & (df['Runs'] < 50)].shape[0]
good = df[(df['Runs'] >= 50) & (df['Runs'] < 100)].shape[0]
excellent = df[df['Runs'] >= 100].shape[0]

labels = ['Low (<30)', 'Medium (30-50)', 'Good (50-100)', 'Excellent (100+)']
values = [low, medium, good, excellent]

# Plot
plt.figure(figsize=(8,5))
plt.bar(labels, values)

plt.title("Score Distribution Categories")
plt.xlabel("Performance Type")
plt.ylabel("Matches")

plt.grid(axis='y', alpha=0.3)

st.pyplot(plt)

# -----------------------------
# INSIGHT
# -----------------------------
best_category = labels[values.index(max(values))]
st.info(f"Most innings fall under: **{best_category}**")

# -----------------------------
# 9. PERFORMANCE BY YEAR
# -----------------------------
st.subheader("📅 Performance by Year")

yearly = df.groupby(df['Date'].dt.year)['Runs'].sum()

st.line_chart(yearly)

# -----------------------------
# 📅 YEAR-WISE PERFORMANCE (DETAILED)
# -----------------------------
st.subheader("📅 Year-wise Runs (Career Progression)")

yearly = df.groupby(df['Date'].dt.year)['Runs'].sum()

plt.figure(figsize=(10,5))
bars = plt.bar(yearly.index, yearly.values)

plt.title("Year-wise Runs (Career Progression)")
plt.xlabel("Year")
plt.ylabel("Total Runs")

plt.grid(axis='y', alpha=0.3)

# Add values on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 20, 
             int(height), ha='center')

st.pyplot(plt)

# -----------------------------
# INSIGHT (SMART ADDITION)
# -----------------------------
best_year = yearly.idxmax()
best_runs = yearly.max()

st.info(f"Peak performance year: **{best_year}** with **{best_runs} runs**")

# -----------------------------
# 10. BEST PERFORMANCES
# -----------------------------
st.subheader("🔥 Best Performances (Top Innings)")

top_scores = df.sort_values(by='Runs', ascending=False).head(10)

st.dataframe(top_scores[['Date','Opponent','Runs']])

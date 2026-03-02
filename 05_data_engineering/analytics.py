import pandas as pd
import plotly.express as px

# 1. The Sample Data (Simulating a CSV file)
data = {
    "Title": ["The Matrix", "Inception", "Stranger Things", "The Crown", "Interstellar", "Dark", "Avengers", "The Office"],
    "Type": ["Movie", "Movie", "TV Show", "TV Show", "Movie", "TV Show", "Movie", "TV Show"],
    "Genre": ["Sci-Fi", "Sci-Fi", "Sci-Fi", "Drama", "Sci-Fi", "Thriller", "Action", "Comedy"],
    "Release_Year": [1999, 2010, 2016, 2016, 2014, 2017, 2012, 2005],
    "Views_Millions": [45.5, 60.2, 85.0, 40.1, 70.5, 30.0, 95.2, 110.5]
}

# Load the data into a Pandas DataFrame (the core object of Pandas)
df = pd.DataFrame(data)

# --- THE PANDAS MAGIC ---

print("📊 1. Looking at the raw data:")
print(df.head()) # .head() shows the first 5 rows

print("\n📈 2. Getting quick statistics:")
print(df.describe()) # .describe() automatically calculates mean, min, max, etc. for numbers

print("\n🔍 3. Filtering Data (Only Sci-Fi):")
scifi_df = df[df["Genre"] == "Sci-Fi"]
print(scifi_df)

print("\n🧮 4. Grouping Data (Total Views by Type):")
# This is like a Pivot Table in Excel
summary = df.groupby("Type")["Views_Millions"].sum().reset_index()
print(summary)

# --- THE PLOTLY MAGIC ---
print("\n🌐 5. Opening dashboard in your browser...")

# Create an interactive Bar Chart
fig = px.bar(
    summary, 
    x="Type", 
    y="Views_Millions", 
    color="Type", 
    title="Total Views: Movies vs. TV Shows",
    text="Views_Millions" # Puts the number on top of the bar
)

# This will open a new tab in your web browser!
fig.show()
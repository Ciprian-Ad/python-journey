import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Page Configuration ---
st.set_page_config(page_title="Netflix Analytics", layout="wide")

st.title("🎬 Netflix Data Explorer")
st.markdown("Welcome to your very first Python Web Dashboard!")

# --- 2. Load the Data (The Smart Way) ---
# The @st.cache_data decorator tells Streamlit to only read the CSV once.
# This makes your dashboard lightning fast when clicking buttons!
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df["director"] = df["director"].fillna("Unknown")
    return df

df = load_data()

# --- 3. The Sidebar (Interactive Filters) ---
st.sidebar.header("🔍 Filter Options")

# Create a dropdown menu automatically populated with "Movie" and "TV Show"
selected_type = st.sidebar.selectbox("Select Media Type:", df["type"].unique())

# Create a slider for the release year
min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())
selected_year_range = st.sidebar.slider(
    "Select Release Year Range:",
    min_value=min_year,
    max_value=max_year,
    value=(2010, max_year) # Default range
)

# --- 4. Apply the Filters (Pandas) ---
# Filter by the dropdown AND the slider
filtered_df = df[
    (df["type"] == selected_type) & 
    (df["release_year"] >= selected_year_range[0]) & 
    (df["release_year"] <= selected_year_range[1])
]

# --- 5. The Dashboard UI ---
# Show a big metric number
st.metric(label=f"Total {selected_type}s Found", value=len(filtered_df))

st.write("---") # A horizontal divider line

# Reusing your Time Machine logic!
st.subheader("📈 Releases Over Time")
timeline = filtered_df.groupby("release_year").size().reset_index(name="count")
fig = px.line(timeline, x="release_year", y="count", title=f"{selected_type} Releases Trend")

# This is the magic command that puts your Plotly chart on the web page!
st.plotly_chart(fig, use_container_width=True)

st.write("---")

# Show the raw interactive data table
st.subheader("📋 Raw Data Explorer")
st.dataframe(filtered_df[["title", "director", "release_year", "listed_in"]].head(100))
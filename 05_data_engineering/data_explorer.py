import pandas as pd
import plotly.express as px

# 1 Load the data from a CSV file
df = pd.read_csv("netflix_titles.csv")

# 1.1 Print the first 10 rows of the DataFrame to see what it looks like
print("📊 1. Looking at the raw data:")
print(df.head(10)) # .head(10) shows the first 10 rows

# 1.2 Print the total number of rows and columns
print("\n📈 1.2 DataFrame shape (rows, columns):")
print(df.shape)

# 2. Filter DataFrame to show only rows where the "type" is "TV Show"
filtered_df = df[df["type"] == "TV Show"]
print("\n🔍 2. Filtered DataFrame (TV Shows only):")
print(filtered_df.head(10))

# 2.1 Get the Movie after 2020
movies_after_2020 = df[(df["type"] == "Movie") & (df["release_year"] > 2020)]
print("\n🔍 2.1 Movies released after 2020:")
print(movies_after_2020[["title", "director"]].head(10))

# 3 Most recent Movies
most_recent_movies = df[df["type"] == "Movie"].sort_values(by="release_year", ascending=False).head(10)
print("\n🔍 3. Most recent Movies:")
print(most_recent_movies[["title", "director", "release_year"]])

# 4.1 Missing value from each column
print("\n🧮 4.1 Missing values in each column:")
print(df.isna().sum())

# 4.2 Fill missing values in the "director" column with "Unknown"
df["director"] = df["director"].fillna("Unknown")
print("\n🧮 4.2 Missing values in 'director' column after filling:")
print(df["director"].isnull().sum())

# 5 Total number of Movies and TV Shows
type_counts = df["type"].value_counts().reset_index()
type_counts.columns = ["Type", "Count"]
print("\n🧮 5. Total number of Movies and TV Shows:")
print(type_counts)

# 6. Create an interactive Bar Chart using Plotly
print("\n🌐 6. Opening dashboard in your browser...")
fig = px.bar(type_counts, x="Type", y="Count", title="Number of Movies and TV Shows")
fig.show()

# 7. String cleaning - remove minutes from duration column and convert to numeric
movies = df[df["type"] == "Movie"].copy() # Create a copy to avoid SettingWithCopyWarning
movies["duration"] = movies["duration"].str.replace(" min", "") # Remove " min"
movies["duration"] = movies["duration"].astype("Int64") # Convert to integer type (allows for NaN)
print("\n🧮 7. Cleaned duration column:")
print(movies[["title", "duration"]].head(10))

# 8. The Time Machine (Grouping & Line Charts)
# Group by release year and count the number of movies released each year
movies_by_year = movies.groupby("release_year").size().reset_index(name="count")
print("\n🧮 8. Number of Movies released each year:")
print(movies_by_year.head(10))
# Create a line chart to show the trend of movie releases over time
fig = px.line(movies_by_year, x="release_year", y="count", title="Number of Movies Released Each Year")
fig.show()
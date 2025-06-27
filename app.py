import pandas as pd
import streamlit as st

# Load data
df = pd.read_csv("netflix_titles.csv")
df.fillna('', inplace=True)

# Set page config
st.set_page_config(page_title="Netflix Movie Recommender", layout="centered")

st.title("🎬 Netflix Movie Recommender")
st.markdown("Find top movies or shows based on genre, country, rating group, and release year.")

# 🎭 Simplified Genre List
custom_genres = [
    "Action", "Adventure", "Comedy", "Drama", "Horror", "Thriller", "Romance", 
    "Documentary", "Sci-Fi & Fantasy", "Children & Family", "Crime", "Mystery", 
    "Animation", "Stand-Up Comedy", "Reality"
]

# 🌍 Unique countries from data
all_countries = sorted(set(
    c.strip() for sublist in df['country'].dropna() for c in sublist.split(',')
))

# 🏷️ Simplified Ratings (Mapping real ratings to groups)
rating_map = {
    "Unrestricted": ['G', 'PG', 'TV-G', 'TV-Y', 'TV-Y7'],
    "Youth": ['PG-13', 'TV-14'],
    "Adults Only": ['R', 'NC-17', 'TV-MA']
}

# 📌 Sidebar filters
genre = st.selectbox("🎭 Choose Genre", [""] + custom_genres)
country = st.selectbox("🌍 Choose Country", [""] + all_countries)
rating_group = st.selectbox("🏷️ Rating Category", ["", "Unrestricted", "Youth", "Adults Only"])
year = st.slider("📅 Minimum Release Year", 1940, 2022, 2000)

# 👉 Button to apply filters
if st.button("🎯 Show Recommendations"):

    filtered = df.copy()

    if genre:
        filtered = filtered[filtered['listed_in'].str.contains(genre, case=False)]

    if country:
        filtered = filtered[filtered['country'].str.contains(country, case=False)]

    if rating_group:
        selected_ratings = rating_map[rating_group]
        filtered = filtered[filtered['rating'].isin(selected_ratings)]

    filtered = filtered[filtered['release_year'] >= year]

    st.subheader("🍿 Top Matches")
    if filtered.empty:
        st.warning("❌ No matches found. Try relaxing filters.")
    else:
        for _, row in filtered.sort_values(by="release_year", ascending=False).head(10).iterrows():
            st.markdown(f"**{row['title']}** ({row['release_year']})  \n*{row['listed_in']} — {row['country']}*")

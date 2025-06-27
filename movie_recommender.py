import pandas as pd

df = pd.read_csv("netflix_titles.csv")


# Clean & Fill
df.fillna('', inplace=True)

def filter_movies(genre=None, country=None, min_rating=None, year=None):
    filtered = df.copy()

    if genre:
        filtered = filtered[filtered['listed_in'].str.contains(genre, case=False)]


    if country:
        filtered = filtered[filtered['country'].str.contains(country, case=False)]

    if min_rating:
        filtered = filtered[filtered['rating'].isin(min_rating)]

    if year:
        filtered = filtered[filtered['release_year'] >= year]

    return filtered.sort_values(by="release_year", ascending=False).head(10)

def main():
    print("\n🎬 Welcome to Movie Recommender CLI!")
    while True:
        print("\nChoose filter options:")
        genre = input("Enter genre (leave blank to skip): ")
        country = input("Enter country (leave blank to skip): ")
        rating_input = input("Enter preferred ratings (like TV-14, PG, etc. comma separated, or blank to skip): ")
        min_rating = [r.strip() for r in rating_input.split(",")] if rating_input else None
        try:
            year = int(input("Enter minimum release year (or leave blank): ") or 0)
        except ValueError:
            year = 0

        results = filter_movies(genre, country, min_rating, year)

        if results.empty:
            print("\n❌ No movies found matching your filters.")
        else:
            print("\n🎯 Top Matches:\n")
            for index, row in results.iterrows():
                print(f"{row['title']} ({row['release_year']}) - {row['listed_in']} - {row['country']}")


        again = input("\nTry again? (y/n): ").lower()
        if again != 'y':
            print("\n🎉 Thanks for using Movie Recommender CLI!")
            break

if __name__ == "__main__":
    main()

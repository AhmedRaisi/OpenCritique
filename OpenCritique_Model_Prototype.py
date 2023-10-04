import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances 

# 1. Load the Data:
data_path = "/mnt/c/Users/Ahmed/Projects/OpenCritique/data/ml-100k/ml-100k/"

# Load the ratings data
column_names = ["user_id", "item_id", "rating", "timestamp"]
ratings = pd.read_csv(data_path + 'u.data', sep='\t', names=column_names)

# Load the movie information
movie_columns = ["item_id", "movie_title", "release_date", "video_release_date", "IMDb_URL", "unknown", "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]
movies = pd.read_csv(data_path + 'u.item', sep='|', names=movie_columns, encoding='latin-1')

# Load user data
user_columns = ["user_id", "age", "gender", "occupation", "zip_code"]
users = pd.read_csv(data_path + 'u.user', sep='|', names=user_columns)

# 2. Data Preprocessing:
# Checking for missing values
print(ratings.isnull().sum())
print(movies.isnull().sum())

# Creating a user-item matrix
user_item_matrix = ratings.pivot_table(index='user_id', columns='item_id', values='rating')

# Filling NaN values with 0
user_item_matrix = user_item_matrix.fillna(0)

# Calculating user-user similarity
user_similarity = 1 - pairwise_distances(user_item_matrix, metric='cosine')

# Making Predictions:
def predict(ratings, similarity):
    mean_user_rating = ratings.mean(axis=1)
    ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
    pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
    return pred

user_prediction = predict(user_item_matrix.values, user_similarity)


def describe_user(user_id):
    user = users[users['user_id'] == user_id].iloc[0]
    return f"User of age {user['age']} with occupation {user['occupation']}"


# Get movies by genre
def get_movies_by_genre(genre, num_movies=5):
    # Convert 'release_date' column to datetime format
    movies['release_date'] = pd.to_datetime(movies['release_date'], errors='coerce')

    # Filter movies based on the genre and release year
    genre_movies = movies[(movies[genre] == 1) & (movies['release_date'].dt.year >= 1990)]
    
    # If there are fewer than the required number of movies, return as many as available
    if len(genre_movies) < num_movies:
        return genre_movies['movie_title'].tolist()

    # Sort movies by release_date in descending order
    genre_movies = genre_movies.sort_values('release_date', ascending=False)
    
    # Split the movies into even intervals but prioritize recent movies
    interval_size = len(genre_movies) // (2 * num_movies)
    diverse_movies = []
    
    for i in range(num_movies):
        idx = i * interval_size
        diverse_movies.append(genre_movies.iloc[idx]['movie_title'])

    return diverse_movies

# 5. Making Recommendations:
def recommend_movies(user_id, num_recommendations=10):
    sorted_movie_indices = np.argsort(user_prediction[user_id-1])[::-1]
    recommended_movie_ids = [i for i in sorted_movie_indices if user_item_matrix.iloc[user_id-1, i] == 0]
    return movies.iloc[recommended_movie_ids]['movie_title'].head(num_recommendations)

if __name__ == "__main__":
    genre = input("Enter a genre: ").capitalize()
    print(f"\nTop 5 movies in {genre} genre:")
    genre_movies = get_movies_by_genre(genre)
    for idx, movie in enumerate(genre_movies, 1):
        print(f"{idx}. {movie}")
    
    movie_picks = list(map(int, input("\nPick 2 movies by entering their numbers (e.g. 1 3): ").split()))

    # For simplicity, picking the user that has rated these movies the highest
    chosen_movie_ids = [movies[movies['movie_title'] == genre_movies[i-1]].iloc[0]['item_id'] for i in movie_picks]
    # Users who rated the movies
    user_ids_with_ratings = ratings[ratings['item_id'].isin(chosen_movie_ids)]['user_id'].unique()
    # Randomly select a user
    user_id = np.random.choice(user_ids_with_ratings)

    user_description = describe_user(user_id)
    print(f"\nMatching critic for your choices: {user_description}")
    
    num_recs = int(input("Enter number of recommendations you want: "))
    recommended_movies = recommend_movies(user_id, num_recs)
    print("\nRecommended Movies:")
    for idx, movie in enumerate(recommended_movies, 1):
        print(f"{idx}. {movie}")


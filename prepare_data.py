# prepare_data.py
import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

print("Preparing movie recommendation data...")

# Load your movie data - adjust this based on what you found in step 1
try:
    # Try to load from movies.pkl first
    with open('movies.pkl', 'rb') as f:
        movies = pickle.load(f)
    print("Loaded movies.pkl")
except:
    try:
        # Try movie_dict.pkl as fallback
        with open('movie_dict.pkl', 'rb') as f:
            movies = pickle.load(f)
        print("Loaded movie_dict.pkl")
    except:
        print("No movie data file found!")
        exit()

# Convert to DataFrame if needed
if isinstance(movies, dict):
    # If it's a dictionary with movie details
    if 'title' in movies:
        movies_df = pd.DataFrame(movies)
    else:
        # Try to create a DataFrame from the dict
        movies_df = pd.DataFrame.from_dict(movies, orient='index')
        movies_df.reset_index(inplace=True)
        movies_df.columns = ['movie_id', 'title']  # Adjust as needed
elif isinstance(movies, list):
    # If it's just a list of titles
    movies_df = pd.DataFrame(movies, columns=['title'])
elif isinstance(movies, pd.DataFrame):
    movies_df = movies
else:
    print(f"Unexpected data type: {type(movies)}")
    exit()

print(f"Movies DataFrame shape: {movies_df.shape}")
print(f"Columns: {movies_df.columns.tolist()}")

# Ensure we have a title column
if 'title' not in movies_df.columns:
    # Use the first column as title
    first_col = movies_df.columns[0]
    movies_df['title'] = movies_df[first_col]
    print(f"Using '{first_col}' as title column")

# Create features for similarity calculation
# This depends on what data you have. Common approaches:

# Approach 1: If you have text features (overview, genres, etc.)
if 'overview' in movies_df.columns:
    print("Using overview text for similarity...")
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['overview'].fillna(''))
    similarity = linear_kernel(tfidf_matrix, tfidf_matrix)

# Approach 2: If you have genres or other categorical data
elif 'genres' in movies_df.columns:
    print("Using genres for similarity...")
    from sklearn.preprocessing import MultiLabelBinarizer
    # Assuming genres are in list format
    mlb = MultiLabelBinarizer()
    genre_matrix = mlb.fit_transform(movies_df['genres'].fillna('').apply(lambda x: x.split('|')))
    similarity = linear_kernel(genre_matrix, genre_matrix)

# Approach 3: Simple random similarity (temporary, just for testing)
else:
    print("No suitable features found. Creating random similarity matrix for testing...")
    n_movies = len(movies_df)
    similarity = np.random.rand(n_movies, n_movies)
    # Make it symmetric (similarity matrices should be symmetric)
    similarity = (similarity + similarity.T) / 2
    # Set diagonal to 1 (a movie is perfectly similar to itself)
    np.fill_diagonal(similarity, 1)

# Save the files
print("\nSaving files...")

# Save movie data
with open('movie_data.pkl', 'wb') as f:
    pickle.dump(movies_df, f)
print("Saved movie_data.pkl")

# Save similarity matrix
with open('similarity.pkl', 'wb') as f:
    pickle.dump(similarity, f)
print(f"Saved similarity.pkl with shape: {similarity.shape}")

print("\nData preparation complete!")
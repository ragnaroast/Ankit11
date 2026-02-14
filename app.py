import streamlit as st
import pickle
import pandas as pd
import os
import gdown
import subprocess

st.set_page_config(page_title="Movie Recommender", page_icon="🎬")

# =====================================================
# DOWNLOAD MODEL FILES FROM GOOGLE DRIVE IF MISSING
# =====================================================

def download_file(file_id, output):
    if not os.path.exists(output):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output, quiet=False)

# 🔥 REPLACE THESE WITH YOUR REAL FILE IDs
SIMILARITY_ID = "1tHb-psekOycvxiDe8b5h9lGqmewSOflY"
MOVIE_DATA_ID = "1TjpJ7NHWp02K5VwHVdqAvaGEtNDJ83zT"
MOVIE_DICT_ID = "1iCkIqxMRYT3ucDsxXwyCktQ-Ga_4nVHP"

download_file(SIMILARITY_ID, "similarity.pkl")
download_file(MOVIE_DATA_ID, "movie_data.pkl")
download_file(MOVIE_DICT_ID, "movie_dict.pkl")

# =====================================================
# LOAD DATA
# =====================================================

def load_data():
    """Load movies and similarity data"""
    try:
        # Try to load from the new files first
        if os.path.exists('movie_data.pkl') and os.path.exists('similarity.pkl'):
            with open('movie_data.pkl', 'rb') as f:
                movies = pickle.load(f)
            with open('similarity.pkl', 'rb') as f:
                similarity = pickle.load(f)
            st.success("Loaded data from movie_data.pkl and similarity.pkl")
            
        # Fallback to original files
        elif os.path.exists('movie_dict.pkl') and os.path.exists('similarity.pkl'):
            with open('movie_dict.pkl', 'rb') as f:
                movie_dict = pickle.load(f)
                # Convert to DataFrame
                if isinstance(movie_dict, dict):
                    movies = pd.DataFrame(movie_dict)
                else:
                    movies = movie_dict
            with open('similarity.pkl', 'rb') as f:
                similarity = pickle.load(f)
            st.success("Loaded data from movie_dict.pkl and similarity.pkl")
            
        elif os.path.exists('movies.pkl') and os.path.exists('similarity.pkl'):
            with open('movies.pkl', 'rb') as f:
                movies = pickle.load(f)
            with open('similarity.pkl', 'rb') as f:
                similarity = pickle.load(f)
            st.success("Loaded data from movies.pkl and similarity.pkl")
            
        else:
            missing_files = []
            if not os.path.exists('similarity.pkl'):
                missing_files.append('similarity.pkl')
            st.error(f"Missing required files: {', '.join(missing_files)}")
            return None, None
        
        # Ensure movies is a DataFrame
        if not isinstance(movies, pd.DataFrame):
            if isinstance(movies, list):
                movies = pd.DataFrame({'title': movies})
            elif isinstance(movies, dict):
                movies = pd.DataFrame(movies)
            else:
                st.error(f"Unexpected movies data type: {type(movies)}")
                return None, None
        
        # Ensure we have a title column
        if 'title' not in movies.columns:
            if len(movies.columns) > 0:
                movies['title'] = movies.iloc[:, 0]
            else:
                st.error("No title column found in movie data")
                return None, None
        
        return movies, similarity
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

# =====================================================
# MAIN APP
# =====================================================

st.title("🎬 Movie Recommendation System")

# Load data
with st.spinner("Loading movie data..."):
    movies, similarity = load_data()

if movies is None or similarity is None:
    st.error("Failed to load movie data. Please run prepare_data.py first.")
    
    if st.button("Run Data Preparation"):
        result = subprocess.run(['python', 'prepare_data.py'], capture_output=True, text=True)
        st.code(result.stdout)
        st.rerun()
    
    st.stop()

st.success(f"✅ Loaded {len(movies)} movies successfully!")

# Create movie selection
movie_titles = movies['title'].tolist()
selected_movie = st.selectbox(
    "Select a movie:",
    movie_titles,
    index=0
)

def get_recommendations(movie_title, movies, similarity, n_recommendations=5):
    try:
        # Find the index of the selected movie
        movie_idx = movies[movies['title'] == movie_title].index[0]
        
        # Get similarity scores
        sim_scores = list(enumerate(similarity[movie_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N similar movies (excluding itself)
        sim_scores = sim_scores[1:n_recommendations+1]
        movie_indices = [i[0] for i in sim_scores]
        
        # Return recommended movie titles
        return movies.iloc[movie_indices]['title'].tolist()
    except Exception as e:
        st.error(f"Error getting recommendations: {str(e)}")
        return []

# Recommend button
if st.button("🎯 Get Recommendations", type="primary"):
    with st.spinner("Finding similar movies..."):
        recommendations = get_recommendations(selected_movie, movies, similarity)
        
        if recommendations:
            st.subheader("🎥 Top 5 Recommendations:")
            for i, movie in enumerate(recommendations, 1):
                st.write(f"{i}. {movie}")
        else:
            st.warning("No recommendations found. The similarity matrix might need to be recalculated.")

# Show data info in sidebar
with st.sidebar:
    st.header("📊 Data Info")
    st.write(f"Total movies: {len(movies)}")
    st.write(f"Similarity matrix shape: {similarity.shape}")
    
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

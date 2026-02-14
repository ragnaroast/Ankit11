# check_data.py
import pickle
import pandas as pd

# Check movies.pkl
try:
    with open('movies.pkl', 'rb') as f:
        movies_data = pickle.load(f)
    print("=== movies.pkl ===")
    print("Type:", type(movies_data))
    if isinstance(movies_data, pd.DataFrame):
        print("Shape:", movies_data.shape)
        print("Columns:", movies_data.columns.tolist())
        print("First 5 rows:")
        print(movies_data.head())
    elif isinstance(movies_data, dict):
        print("Keys:", movies_data.keys())
        print("First few items:")
        for k, v in list(movies_data.items())[:3]:
            print(f"{k}: {type(v)} - length: {len(v) if hasattr(v, '__len__') else 'N/A'}")
    elif isinstance(movies_data, list):
        print("Length:", len(movies_data))
        print("First 5 items:", movies_data[:5])
    else:
        print("Sample:", str(movies_data)[:200])
except Exception as e:
    print("Error loading movies.pkl:", e)

print("\n" + "="*50 + "\n")

# Check movie_dict.pkl
try:
    with open('movie_dict.pkl', 'rb') as f:
        movie_dict = pickle.load(f)
    print("=== movie_dict.pkl ===")
    print("Type:", type(movie_dict))
    if isinstance(movie_dict, dict):
        print("Keys:", movie_dict.keys())
        print("First few items:")
        for k, v in list(movie_dict.items())[:3]:
            print(f"{k}: {type(v)} - length: {len(v) if hasattr(v, '__len__') else 'N/A'}")
    else:
        print("Sample:", str(movie_dict)[:200])
except Exception as e:
    print("Error loading movie_dict.pkl:", e)
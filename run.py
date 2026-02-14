# run.py
from waitress import serve
import subprocess
import sys

# This will run your Streamlit app through waitress
if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "streamlit", "run", "your_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"])
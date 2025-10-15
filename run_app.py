import os
import sys
import subprocess

# Get the folder where this script (or exe) is located
current_folder = os.path.dirname(os.path.abspath(__file__))

# Build path to the Streamlit app inside the same folder
app_path = os.path.join(current_folder, "Name_to_BIN.py")

# Run Streamlit app
subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])

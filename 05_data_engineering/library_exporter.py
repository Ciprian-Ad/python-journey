import pandas as pd
import os
from pathlib import Path

def scan_library(path):
    """
    Scans the library directory and returns a list of book metadata.
    
    Args:
        path (str): The path to the library directory.
    Returns:
        list: A list of dictionaries containing book metadata.
    """
    library_data = []
    root = Path(path)
    print(f"Scanning library at: {root}")
    for folder in root.glob('*'):
        print(f"Scanning: {folder.name}")
        stats = folder.stat()
        library_data.append({
            'Name': folder.name,
            'Type': 'Movie' if 'Movies' in str(folder) else 'TV Show',
            'Size (GB)': round(sum(f.stat().st_size for f in folder.rglob('*') if f.is_file()) / (1024**3), 2),
            "Created_Year": pd.to_datetime(stats.st_ctime, unit='s').year
        })
    # Create the DataFrame
    df = pd.DataFrame(library_data)
    # Save to CSV for our "Analytics" step
    df.to_csv("media_inventory.csv", index=False)
    print("✅ Media inventory exported to CSV!")

if __name__ == "__main__":
    library_path = "/home/ciprian/Videos"  # Update this to your library path
    scan_library(library_path)
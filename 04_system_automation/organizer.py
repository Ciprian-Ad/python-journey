import os
import shutil
from pathlib import Path
from rich.console import Console

console = Console()

def organize_folder(target_path):
    # Convert string path to a Path object for easier handling
    base_dir = Path(target_path)
    
    # Define our rules: { folder_name: [extensions] }
    file_types = {
        "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Scripts": [".py", ".sh", ".js"],
        "Archives": [".zip", ".tar", ".gz"],
        "Videos": [".mp4", ".avi", ".mkv"]
    }

    # Loop through every file in the folder
    for file_path in base_dir.iterdir():
        if file_path.is_file():
            # Get the file extension
            extension = file_path.suffix.lower()
            
            # Find which category it belongs to
            moved = False
            for folder, extensions in file_types.items():
                if extension in extensions:
                    # Create the category folder if it doesn't exist
                    dest_folder = base_dir / folder
                    dest_folder.mkdir(exist_ok=True)
                    
                    # Move the file
                    shutil.move(str(file_path), str(dest_folder / file_path.name))
                    console.print(f"[green]Moved:[/green] {file_path.name} -> {folder}")
                    moved = True
                    break
            
            if not moved:
                console.print(f"[yellow]Skipped:[/yellow] {file_path.name} (Unknown type)")

# For testing, we'll use a "test_folder" so we don't accidentally mess up your real files!
# Create a folder called 'test_folder' and put some empty .txt or .jpg files in it first.
organize_folder("./test_folder")
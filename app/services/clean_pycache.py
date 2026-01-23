import os
import shutil

def remove_pycaches_ad_pycs(directory):
    for root, dirs, files in os.walk(directory):
        if "__pycache__" in dirs:
            pycache_dir = os.path.join(root, "__pycache__")
            print(f"Removing directory: {pycache_dir}")
            shutil.rmtree(pycache_dir) # Use shutil.rmtree for directories
            
            
        for file in files:
            if file.endswith(".pyc") or file.endswith(".pyo"):
                file_path = os.path.join(root, file)
                print(f"removing file: {file_path}")
                os.remove(file_path)
                
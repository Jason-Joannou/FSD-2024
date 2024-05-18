import os
from .exceptions import DirectoryNotFound

def validate_directory(dir_path:str):
    if not os.path.isdir(dir_path):
        raise DirectoryNotFound(f"The following directory `{dir_path}` does not exist")

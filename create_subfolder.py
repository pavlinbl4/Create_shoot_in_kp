import os.path
from pathlib import Path


def create_directory(folder: str, user_folder="Documents") -> str:
    home = f'{str(Path.home())}/{user_folder}'
    folder_path = os.path.join(home, folder)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path


if __name__ == '__main__':
    print(create_directory("WWWWWWWW/dddd", user_folder='Music'))

"""
To explain:

    First we import the os, os.path and pathlib modules to work with files and paths
    We use pathlib.Path.home() to get the user's home directory path
    We define a list of subfolder names to create
    We loop through this list and construct the full path using os.path.join()
    We check if the folder already exists using os.path.exists()
    If it doesn't exist, we create it using os.makedirs()
    Finally we print out the list of created folders
"""

import os
import logging
from create_subfolder import create_directory

logger = logging.getLogger(__name__)


def create_file_if_not_exists(folder, file_name):
    folder_path = create_directory(folder, user_folder="Documents")
    # Validate inputs
    if not os.path.isdir(folder_path):
        raise ValueError(f"{folder_path} is not a valid folder")

    file_path = os.path.join(folder_path, file_name)

    # Create file if  it doesn't exist
    if not os.path.exists(file_path):
        logger.info("Creating file %s", file_path)
        with open(file_path, 'w'):
            pass

    return file_path


if __name__ == '__main__':
    created_file = create_file_if_not_exists('Kommersant/shoot_rename', 'test_file.txt')
    print(created_file)

import os
from concurrent.futures import ThreadPoolExecutor
from shutil import move
import logging
from functools import partial


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - (%(filename)s).%(funcName)s(%(lineno)d) - "
                           "[%(threadName)s] - %(message)s")


def move_files(path: str, files: dict, folder: str) -> None:
    if not os.listdir(folder):
        os.rmdir(folder)
        logging.debug(f'Видалено порожню папку: {folder}')

    for file in files[folder]:
        file_path = os.path.join(folder, file)
        extension = file.split('.')[-1]
        destination_folder: str = os.path.join(path, extension)

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        destination_path = os.path.join(destination_folder, file)
        move(file_path, destination_path)
        logging.debug(f"Файл {file} переміщено в {destination_path}")


def main():
    path = "D:\\hl"
    folder_files = {}
    for root, dirs, files in os.walk(path, topdown=False):
        folder_files[root] = files
    with ThreadPoolExecutor() as executor:
        executor.map(partial(move_files, path, folder_files), folder_files)
        # executor.map(lambda arg: move_files(path, folder_files, arg), folder_files) # так наче повільніше


if __name__ == "__main__":
    main()

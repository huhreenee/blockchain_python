import os
import io

CURRENT_DIRECTORY = os.getcwd()


def retrieve_blocks():
    block_path = os.path.join(CURRENT_DIRECTORY, 'block_file')
    if not os.path.exists(block_path):
        return
    for file in os.listdir(block_path):
        with io.open(os.path.join(block_path, file), 'rb') as f:
            print(f)


retrieve_blocks()

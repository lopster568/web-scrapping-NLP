import os
from utils import list_files, read_lines_from_file

# Path
directory_path = './stopwords'

# Get list of files
file_list = list_files(directory_path)

# Function to get the stopwords list
def list_stopwords():
    stopwords_list = set()
    # Read all files 
    for file in file_list:
        res = read_lines_from_file(os.path.join(directory_path, file))
        stopwords_list.update(res)
    return stopwords_list
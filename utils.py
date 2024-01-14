import os

def list_files(directory_path):
    files = []

    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            files.append(filename)

    return files

def read_lines_from_file(file_path):
    words = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    words.extend(line.split())
    except UnicodeDecodeError:
        # Retry with 'latin-1' encoding if UTF-8 decoding fails
        with open(file_path, 'r', encoding='latin-1') as file:
            for line in file:
                line = line.strip()
                if line:
                    words.extend(line.split())

    return words
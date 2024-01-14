from utils import read_lines_from_file

# Paths
positive_words_path = './master-dict/positive-words.txt'  
negative_words_path = "./master-dict/negative-words.txt"

# Initialize sets
positive_words = set()
negative_words = set()

# Function to get the master dictionary
def list_master_dict():
    positive_words.update(read_lines_from_file(positive_words_path))
    negative_words.update(read_lines_from_file(negative_words_path))

    master_dict = {
        "positive": positive_words,
        "negative": negative_words
    }

    return master_dict

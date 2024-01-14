import os
import pandas as pd
from nltk import sent_tokenize, word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from utils import list_files

from get_stopwords import list_stopwords
from get_masterwords import list_master_dict
from extract_articles import extract_articles
from utils import read_lines_from_file
# STEP 1: DATA EXTRACTION ----------------------------
print('Extracting articles...')
extract_articles()

# STEP 2: DATA ANALYSIS ------------------------------
print('Performing semantic analysis...')
# Load stopwords and master dictionary
master_dict = list_master_dict()
stopwords_list = list_stopwords()

# Initialize sentiment analyzer
nltk.download('vader_lexicon')
nltk.download('punkt')
sia = SentimentIntensityAnalyzer()

# Function to analyze text
def analyze_text(text):
    # Tokenize text
    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    # Clean text
    clean_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stopwords_list]

    # Calculate variables
    total_words = len(clean_words)
    total_sentences = len(sentences)
    avg_sentence_length = total_words / total_sentences
    complex_words = [word for word in clean_words if len(word) > 2]
    complex_word_count = len(complex_words)
    avg_word_length = sum(len(word) for word in clean_words) / total_words
    syllable_per_word = sum([sum(char.isdigit() for char in word) for word in complex_words]) / complex_word_count
    positive_score = sum(word.lower() in master_dict["positive"] for word in clean_words)
    negative_score = sum(word.lower() in master_dict["negative"] for word in clean_words)
    subjectivity_score = positive_score + negative_score / ((total_words) + 0.000001 )
    
    # Sentiment analysis
    compound_score = sia.polarity_scores(text)['compound']
    return [
        positive_score,
        negative_score,
        sum(compound_score > 0 for _ in sentences),
        sum(compound_score < 0 for _ in sentences),
        compound_score,
        subjectivity_score,
        avg_sentence_length,
        len(complex_words) / total_words,
        0.4 * (avg_sentence_length + len(complex_words) / total_words),
        complex_word_count,
        total_words,
        syllable_per_word,
        sum(word.lower() in ['i', 'me', 'my', 'mine', 'myself', 'we', 'us', 'our', 'ours', 'ourselves'] for word in words),
        avg_word_length
    ]

# Initialize output DataFrame
output_path = './Output.xlsx'
output_columns = ['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POSITIVE SENTENCES', 'NEGATIVE SENTENCES',
                  'POLARITY SCORE', 'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS',
                  'FOG INDEX', 'COMPLEX WORD COUNT', 'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS',
                  'AVG WORD LENGTH']
output_data = pd.DataFrame(columns=output_columns)

# Read text from the extracted articles and analyze it
articles_list = list_files('./articles')

def generate_output():
    input_data = pd.read_excel("./Input.xlsx")
    for index, row in input_data.iterrows():
        url_id = row['URL_ID']
        url = row['URL']
        file_path = os.path.join('./articles', f"{url_id}.txt") 
        
        try: 
            with open(file_path, 'r') as f:
                text = f.read()
                output_data.loc[index] = [url_id, url] + analyze_text(text)
        except FileNotFoundError:
            print(f'File {file_path} not found. Maybe the link is broken for this file?')
            output_data.loc[index] = [url_id, url] + [0] * (len(output_columns) - 2)

# Save the output to an Excel file
generate_output()
print('Saving output...')
output_data.to_excel(output_path, index=False)
print('Done!')
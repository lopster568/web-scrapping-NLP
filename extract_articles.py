import pandas as pd
from bs4 import BeautifulSoup
import requests

# Function to extract text from a given URL
def extract_text(url):
    try:
        # Making request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting article
        article_title = soup.find('title').get_text()
        article_text = soup.find('div', class_='td-post-content').get_text()

        return article_title, article_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None, None

# Paths
input_file = "Input.xlsx"
output_folder = "articles/"

# Input file
df_input = pd.read_excel(input_file)

# Function to extract articles
def extract_articles():
    for index, row in df_input.iterrows():
        # Reading data from the input file
        url_id = row['URL_ID']
        url = row['URL']

        article_title, article_text = extract_text(url)

        if article_title is not None and article_text is not None:
            print(f"{url_id} - Extracted")
            # Save extracted text in a text file
            with open(output_folder + f"{url_id}.txt", "w", encoding="utf-8") as file:
                file.write(f"{article_title}\n{article_text}")
        else:
            print(f"{url_id} - extraction error.")

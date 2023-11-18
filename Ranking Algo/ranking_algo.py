# Yelp Business Data Filter and Rank

## Overview
# This Python script processes Yelp business data to provide search results ranked by relevance based on user queries within a specified geographic radius. It allows for additional search criteria, such as minimum star ratings, minimum number of reviews, and exclusion of specific categories.

## Installation

# Before running the script, ensure that you have the required dependencies installed. You can install them using pip:
# pip install pandas numpy rank_bm25 geopy

import pandas as pd
import numpy as np
from rank_bm25 import BM25Okapi
import string
from geopy.distance import geodesic
# nltk.download('punkt')

stop_word_list = ["shop"]

# Load the first 10000 data points from the Yelp JSON dataset
file_path = 'yelp_academic_dataset_business.json'
yelp_data = pd.read_json(file_path, lines=True, chunksize=30000)
df = next(yelp_data)  # We only load the first chunk, which is 10000 entries

# Cleaning and tokenizing text without using nltk
def clean_and_tokenize(text):
    text = text.replace('&', ' and ')
    text = ' '.join(text.split()).lower().strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.split()

# Apply tokenization to the 'categories' column
df['tokens'] = df['categories'].fillna('').apply(clean_and_tokenize)

# Define a function to calculate distance between two points given their latitudes and longitudes
def calculate_distance(lat1, long1, lat2, long2):
    return geodesic((lat1, long1), (lat2, long2)).kilometers

# Function to filter the DataFrame for businesses within a 10 km radius from a given point
def filter_by_radius(df, latitude, longitude, radius=10):
    distances = df.apply(lambda row: calculate_distance(latitude, longitude, row['latitude'], row['longitude']), axis=1)
    return df[distances <= radius].copy(), distances[distances <= radius]

# Example coordinates for filtering
# example_latitude = 34.052235  # Latitude for Los Angeles
# example_longitude = -118.243683  # Longitude for Los Angeles

example_latitude = 39.925984 # Latitude for New Jersey
example_longitude = -75.034921  # Longitude for New Jersey

# Filter the DataFrame for businesses within a 10 km radius
df_filtered, distances_within_radius = filter_by_radius(df, example_latitude, example_longitude)

# Check if the filtering returned an empty DataFrame
if df_filtered.empty:
    raise ValueError("No businesses found within the specified radius. Please check your coordinates and radius.")

# Create BM25 object from the filtered tokenized 'categories'
tokenized_corpus = df_filtered['tokens'].tolist()
if not any(tokenized_corpus):  # Check if tokenized_corpus is not empty
    raise ValueError("Tokenization resulted in an empty corpus. Please check the tokenization process.")

bm25 = BM25Okapi(tokenized_corpus)

# Function to query and get top N results within the 10 km radius
def bm25_query(query, top_n=10):
    query_tokens = clean_and_tokenize(query)
    doc_scores = bm25.get_scores(query_tokens)
    top_doc_indices = (-doc_scores).argsort()[:top_n]
    results = []
    for i in top_doc_indices:
        business = df_filtered.iloc[i]
        results.append({
            "Place Name": business['name'],
            "Stars and Review counts": f"{business['stars']} stars, {business['review_count']} reviews",
            "Distance": f"{distances_within_radius.iloc[i]:.2f} km",
            "Categories": business['categories'],
            "BM25 Score": doc_scores[i]
        })
    return results

# Example query to test
test_query = "coffee tea"
test_results = bm25_query(test_query)

# Print the results in the specified format
for result in test_results:
    print(f"Place Name: {result['Place Name']}")
    print(f"Stars and Review counts: {result['Stars and Review counts']}")
    print(f"Distance from user's lat and longitude: {result['Distance']}")
    print(f"Categories: {result['Categories']}")
    print(f"BM25 Score: {result['BM25 Score']:.2f}\n")

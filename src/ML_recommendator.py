import pandas as pd
import numpy as np
from rank_bm25 import BM25Okapi
import string
from geopy.distance import geodesic
from openai import OpenAI


# Load the first 10000 data points from the Yelp JSON dataset
file_path = 'data/yelp_academic_dataset_business.json'
yelp_data = pd.read_json(file_path, lines=True, chunksize=100000)
df = next(yelp_data)

# Cleaning and tokenizing text without using nltk
def clean_and_tokenize(text):
    text = ' '.join(text.split()).lower().strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.split()

# Apply tokenization to the 'categories' column
df['tokens'] = df['categories'].fillna('').apply(clean_and_tokenize)

# Define a function to calculate distance between two points given their latitudes and longitudes
def calculate_distance(lat1, long1, lat2, long2):
    return geodesic((lat1, long1), (lat2, long2)).kilometers

# Function to filter the DataFrame for businesses within a specified radius from a given point
def filter_by_radius(df, latitude, longitude, radius = 100):
    distances = df.apply(lambda row: calculate_distance(latitude, longitude, row['latitude'], row['longitude']), axis=1)
    return df[distances <= radius].copy(), distances[distances <= radius]

# Function to filter out unwanted categories
def filter_unwanted_categories(df, categories_not_wanted):
    return df[~df['categories'].str.contains('|'.join(categories_not_wanted), case=False, na=False)]

# Function to query and get top N results within the specified radius and apply user filters
def bm25_query(bm25, df_filtered, distances_within_radius, query, top_n=10, min_stars=0, min_reviews=0, max_distance=10, categories_not_wanted=[]):
    query_tokens = clean_and_tokenize(query)
    doc_scores = bm25.get_scores(query_tokens)
    top_doc_indices = (-doc_scores).argsort()[:top_n]

    # Apply user filters
    filtered_results = []
    for i in top_doc_indices:
        business = df_filtered.iloc[i]
        if (business['stars'] >= min_stars and
            business['review_count'] >= min_reviews and
            distances_within_radius.iloc[i] <= max_distance and
            not any(unwanted in business['categories'] for unwanted in categories_not_wanted)):
            filtered_results.append({
                "PlaceName": business['name'],
                "StarsAndReviewcounts": f"{business['stars']} stars, {business['review_count']} reviews",
                "Distance": f"{distances_within_radius.iloc[i]:.2f} km",
                "Categories": business['categories'],
                "Latitude":business['latitude'],
                "Longitude": business['longitude']
            })
    return filtered_results

# def findRecommendations(latitud,longitud,words) :
#     df_filtered, distances_within_radius = filter_by_radius(df, latitud, longitud)

#     # Check if the filtering returned an empty DataFrame
#     if df_filtered.empty:
#         raise ValueError("No businesses found within the specified radius. Please check your coordinates and radius.")
    
#     tokenized_corpus = df_filtered['tokens'].tolist()
#     if not any(tokenized_corpus):  # Check if tokenized_corpus is not empty
#         raise ValueError("Tokenization resulted in an empty corpus. Please check the tokenization process.")

#     # Create BM25 object from the filtered tokenized 'categories'
#     bm25 = BM25Okapi(tokenized_corpus)

#     result = bm25_query(bm25, df_filtered, distances_within_radius, words, 10, 0, 0, 500)

#     topRecommend_df = pd.DataFrame (result)

#     # Generate the prompt for OpenAI GPT
#     places_info = "Places of Interest descriptions:\n"
#     for index, row in topRecommend_df.iterrows():
#         places_info += f"- {row['PlaceName']}: {row['StarsAndReviewcounts']} within {row['Distance']} km, Categories: {row['Categories']}\n"

#     recommendations = Data2geojson(topRecommend_df)

#     # Return both the recommendations and the formatted string
#     return recommendations, places_info

def findRecommendations(latitud, longitud, words):
    df_filtered, distances_within_radius = filter_by_radius(df, latitud, longitud)

    # Check if the filtering returned an empty DataFrame
    if df_filtered.empty:
        raise ValueError("No businesses found within the specified radius. Please check your coordinates and radius.")
    
    tokenized_corpus = df_filtered['tokens'].tolist()
    if not any(tokenized_corpus):  # Check if tokenized_corpus is not empty
        raise ValueError("Tokenization resulted in an empty corpus. Please check the tokenization process.")

    # Create BM25 object from the filtered tokenized 'categories'
    bm25 = BM25Okapi(tokenized_corpus)

    result = bm25_query(bm25, df_filtered, distances_within_radius, words, 10, 0, 0, 500)
    topRecommend_df = pd.DataFrame(result)
    recommendations = Data2geojson(topRecommend_df)

    # Generate the prompt for OpenAI GPT
    places_info = "Places of Interest descriptions:\n"
    for index, row in topRecommend_df.iterrows():
        places_info += f"- {row['PlaceName']}: {row['StarsAndReviewcounts']} within {row['Distance']} km, Categories: {row['Categories']}\n"

    # Initialize OpenAI client
    client = OpenAI()

    # Complete prompt
    complete_prompt = f"You are a trip advisor. Your client is interested in {words}. These are the top recommendations for the client. Form a small description for the client of all these places.\n\n{places_info}"

    # Call to OpenAI GPT
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=complete_prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Return both the recommendations and the generated descriptions
    return recommendations, response.text


def getDescriptionsForRecommendations(places_info):
    # Initialize OpenAI client
    client = OpenAI()

    # Complete prompt
    complete_prompt = f"You are a trip advisor. Your client is interested in {words}. These are the top recommendations for the client. Form a small description for the client of all these places.\n\n{places_info}"

    # Call to OpenAI GPT
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=complete_prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.text

import json
import geojson
from geojson import Feature, FeatureCollection, Point


def Data2geojson(df):
    features = []
    insert_features = lambda X: features.append(
                        geojson.Feature(geometry=geojson.Point((X["Longitude"],
                                                    X["Latitude"])),
                        properties=dict(name = X["PlaceName"],
                                    description = X["Categories"],
                                    rating = X['StarsAndReviewcounts']))
                    )
    df.apply(insert_features, axis=1)

    dump = geojson.dumps(geojson.FeatureCollection(features), sort_keys=True, ensure_ascii=False,indent=4)
    return dump
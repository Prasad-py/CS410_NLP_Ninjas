import pandas as pd
from Data2GeoJson import Data2geojson
import numpy as np
from rank_bm25 import BM25Okapi
import string
from geopy.distance import geodesic
import openai

# Set the API key for OpenAI (required for using GPT models)
openai.api_key = # Get your key

# Load the first 100000 data points from the Yelp JSON dataset
file_path = 'data/yelp_academic_dataset_business.json'
yelp_data = pd.read_json(file_path, lines=True, chunksize=100000)
df = next(yelp_data)

# Cleaning and tokenizing text without using nltk
def clean_and_tokenize(text):
    text = ' '.join(text.split()).lower().strip()  # Normalize and strip text
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    return text.split()  # Tokenize the text

# Apply tokenization to the 'categories' column of the dataframe
df['tokens'] = df['categories'].fillna('').apply(clean_and_tokenize)

# Function to calculate distance between two points given their latitudes and longitudes
def calculate_distance(lat1, long1, lat2, long2):
    return geodesic((lat1, long1), (lat2, long2)).kilometers

# Function to filter the DataFrame for businesses within a specified radius from a given point
def filter_by_radius(df, latitude, longitude, radius = 100):
    distances = df.apply(lambda row: calculate_distance(latitude, longitude, row['latitude'], row['longitude']), axis=1)
    return df[distances <= radius].copy(), distances[distances <= radius]

# Function to filter out unwanted categories
def filter_unwanted_categories(df, categories_not_wanted):
    return df[~df['categories'].str.contains('|'.join(categories_not_wanted), case=False, na=False)]

# Function to perform a BM25 query and get top N results within a specified radius applying user filters
def bm25_query(bm25, df_filtered, distances_within_radius, query, top_n=5, min_stars=0, min_reviews=0, max_distance=10):
    query_tokens = clean_and_tokenize(query)
    doc_scores = bm25.get_scores(query_tokens)
    top_doc_indices = (-doc_scores).argsort()[:top_n]

    # Apply user filters to the results
    filtered_results = []
    for i in top_doc_indices:
        business = df_filtered.iloc[i]
        if (business['stars'] >= min_stars and
            business['review_count'] >= min_reviews and
            distances_within_radius.iloc[i] <= max_distance):
            filtered_results.append({
                "PlaceName": business['name'],
                "StarsAndReviewcounts": f"{business['stars']} stars, {business['review_count']} reviews",
                "Distance": f"{distances_within_radius.iloc[i]:.2f} km",
                "Categories": business['categories'],
                "Latitude":business['latitude'],
                "Longitude": business['longitude']
            })
    return filtered_results

# Main function to find recommendations based on user input
def findRecommendations(latitud, longitud, words, radius, minStars):
    df_filtered, distances_within_radius = filter_by_radius(df, latitud, longitud, radius)

    # Check if any businesses were found within the specified radius
    if df_filtered.empty:
        raise ValueError("No businesses found within the specified radius. Please check your coordinates and radius.")
    
    tokenized_corpus = df_filtered['tokens'].tolist()
    if not any(tokenized_corpus):  # Ensure corpus is not empty
        raise ValueError("Tokenization resulted in an empty corpus. Please check the tokenization process.")

    bm25 = BM25Okapi(tokenized_corpus)  # Create BM25 object from the filtered tokenized 'categories'

    result = bm25_query(bm25, df_filtered, distances_within_radius, words, 5, minStars, 0, 100)
    topRecommend_df = pd.DataFrame(result)
    recommendations = Data2geojson(topRecommend_df)  # Convert data to GeoJSON for mapping

    # Prepare the prompt for GPT model
    places_info = "Places of Interest descriptions:\n"
    for index, row in topRecommend_df.iterrows():
        places_info += f"- {row['PlaceName']}: {row['StarsAndReviewcounts']} within {row['Distance']} km, Categories: {row['Categories']}\n"

    complete_prompt = f"You are a trip advisor. Your client is interested in {words}. These are the top recommendations for the client. Form a small description for the client of all these places.\n\n{places_info}"

    # Call to OpenAI GPT to generate descriptions
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=complete_prompt,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    gpt_response = response.choices[0].text
    recommendation = {}
    recommendation["mapData"] = recommendations
    recommendation["gptResponse"] = gpt_response
    return recommendation

# Yelp Business Data Filter and Rank

## Overview
This Python script processes Yelp business data to provide search results ranked by relevance based on user queries within a specified geographic radius. It allows for additional search criteria, such as minimum star ratings, minimum number of reviews, and exclusion of specific categories.

## Installation

Before running the script, ensure that you have the required dependencies installed. You can install them using pip:

```bash
pip install pandas numpy rank_bm25 geopy

# CS410 Group Project - Team MapMingle

## Project Overview
MapMingle is a dynamic nearby places recommender system that provides personalized suggestions based on user-specified latitude, longitude, and search queries. The system sorts and ranks points of interest (POIs) using user reviews and ratings, ensuring high-quality and relevant recommendations.

## Team Members
- **Rohit Pandey (Captain)** - NetID: rp23
- **Prasad Gole** - NetID: gole2
- **Asmita Chihnara** - NetID: asmitac2
- **Avinash Pathak** - NetID: apathak3
- **Surya Sindhu Mallimanugula** - NetID: ssm13

## Demo Video

Check out our demo video to see MapMingle in action:

[![MapMingle Demo Video](https://img.youtube.com/vi/wXWIm62aU9k/0.jpg)](https://youtu.be/wXWIm62aU9k)

Click on the image above to watch the video on YouTube.

### Addressing a Need
- The inception of MapMingle was driven by the growing demand for personalized and dynamic location-based services. This project aims to provide a solution that is both convenient and customizable, meeting the modern requirements of users.

### Enhancing User Experience
- Traditional location-based services often offer static and irrelevant suggestions. MapMingle revolutionizes this approach by delivering real-time, tailored recommendations, thereby enhancing user engagement and satisfaction.

### Leveraging Technology
- Utilizing advancements in spatial filtering, ranking algorithms, and mobile technology, MapMingle represents a step forward in creating an intelligent and user-friendly recommender system.

### Filling the Gap
- Despite the abundance of location-based services, there exists a gap in the market for a system that intelligently combines user preferences, location data, and real-time adaptability. MapMingle aims to bridge this gap.

### Impact and Innovation
- MapMingle has the potential to significantly impact how individuals interact with their surroundings, making the discovery of new places more intuitive, personalized, and enjoyable. It represents an opportunity for our team to apply cutting-edge technologies in data filtering and ranking algorithms to address real-world challenges.


## Dataset and Ranking Algorithm

### Yelp Academic Dataset

MapMingle utilizes the Yelp Academic Dataset, a rich collection of data from Yelp, one of the largest user-generated review platforms. This dataset is an excellent resource for location-based services and recommendation systems due to its comprehensive nature. Key features of the Yelp dataset include:

- **Business Information:** Detailed data about local businesses including location, categories, and attributes.
- **Reviews and Ratings:** Millions of user-generated reviews and ratings, offering deep insights into customer preferences and experiences.
- **User Data:** Information about the users who provide reviews and ratings, which can be used to understand demographics and user behaviors.
- **Check-in Information:** Data about user check-ins at businesses, reflecting popularity and customer visit patterns.

This dataset provides the backbone for MapMingle's recommendation system, allowing for a nuanced understanding of user preferences and business attributes.

### Ranking Algorithm - BM25

MapMingle employs the BM25 (Best Matching 25) ranking algorithm for its recommendation engine. BM25 is a probabilistic information retrieval model, widely recognized for its effectiveness in ranking documents based on their relevance to a given search query. The key aspects of BM25 in the context of MapMingle are:

- **Relevance Scoring:** BM25 calculates a score for each business in the dataset based on how closely it matches the user's search query, taking into account the frequency of query terms in each business's description and categories.
- **Term Frequency-Document Frequency:** The algorithm considers both the frequency of the query term in each document (term frequency) and the number of documents containing the term (document frequency), balancing the weight given to common and rare terms.
- **Tuning Parameters:** BM25 includes parameters like 'k1' and 'b', which can be fine-tuned to adjust the sensitivity of the model to term frequency and document length, respectively. This allows for customization based on specific use cases and datasets.

By integrating BM25, MapMingle can efficiently and effectively rank businesses based on the user's preferences and search criteria, ensuring that the recommendations are both relevant and personalized.


## How to Run

### Prerequisites
- Python installation.
- OpenAI API key for the GPT model - Put it in the file Recommender.py (line 10)

### Installation and Setup
1. **Clone the Repository:**
   - `git clone [repository-url]`
   - Navigate to the `src` folder.

2. **Prepare the Data:**
   - Place `yelp_academic_dataset_business.json` in the `data` folder.

3. **Install Python Packages:**
   - `pip install pandas numpy nltk geopy geojson rank_bm25 matplotlib seaborn scikit-learn flask`

4. **Running the Application:**
   - `python app.py`
   - Access the site at [http://127.0.0.1:5000](http://127.0.0.1:5000).

### Note
- Ensure network settings allow server access.
- Use a stable internet connection for optimal performance.

---

Enjoy exploring with MapMingle!


# CS410 Group Project - Team MapMingle

## Project Overview
MapMingle is a dynamic nearby places recommender system that provides personalized suggestions based on user-specified latitude, longitude, and search queries. The system sorts and ranks points of interest (POIs) using user reviews and ratings, ensuring high-quality and relevant recommendations.

## Team Members
- **Rohit Pandey (Captain)** - NetID: rp23
- **Prasad Gole** - NetID: gole2
- **Asmita Chihnara** - NetID: asmitac2
- **Avinash Pathak** - NetID: apathak3
- **Surya Sindhu Mallimanugula** - NetID: ssm13

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


## How to Run

### Prerequisites
- Python installation.
- OpenAI API key for the GPT model.

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


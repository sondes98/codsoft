import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
df = pd.read_csv('netflix_titles.csv')

# Fill missing values
df['director'] = df['director'].fillna('')
df['cast'] = df['cast'].fillna('')
df['country'] = df['country'].fillna('')
df['listed_in'] = df['listed_in'].fillna('')
df['description'] = df['description'].fillna('')

# Create a new column combining relevant features
df['combined_features'] = df['title'] + ' ' + df['director'] + ' ' + df['cast'] + ' ' + df['listed_in'] + ' ' + df['description']

# Convert text data into numerical vectors using TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])

# Calculate the cosine similarity between items
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_recommendations(content_type, genre, rating, cosine_sim=cosine_sim):
    filtered_df = df[(df['type'] == content_type) & 
                        (df['listed_in'].str.contains(genre, case=False, na=False)) & 
                        (df['rating'].str.contains(rating, case=False, na=False))]
    
    if filtered_df.empty:
        return "No items found for these preferences. Please try different criteria."
    
    # Avoid SettingWithCopyWarning by using .copy() method
    filtered_df = filtered_df.copy()
    
    # Get the combined features for filtered items
    filtered_df['combined_features'] = filtered_df['title'] + ' ' + filtered_df['director'] + ' ' + filtered_df['cast'] + ' ' + filtered_df['listed_in'] + ' ' + filtered_df['description']
    
    # Vectorize the filtered items
    filtered_tfidf_matrix = tfidf.transform(filtered_df['combined_features'])
    
    # Compute cosine similarity for filtered items
    filtered_cosine_sim = cosine_similarity(filtered_tfidf_matrix, tfidf_matrix)
    
    # Sum similarity scores across all items
    sim_scores = filtered_cosine_sim.mean(axis=0)
    
    # Get the indices of the top 10 most similar items
    sim_scores = list(enumerate(sim_scores))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:10]
    
    # Get the recommended movie/show indices
    show_indices = [i[0] for i in sim_scores]
    
    # Return the titles of the recommended shows/movies
    return df[['title']].iloc[show_indices]

def main():
    print("Welcome to the Netflix Recommendation System!")
    
    # User input for recommendations in a structured format
    user_input = input("Enter your recommendation request:  ").strip().lower()
    
    # Parse user input
    if "recommend" in user_input:
        # Example input: "Recommend top-rated science fiction movies"
        parts = user_input.split(' ')
        content_type = 'Movie' if 'movie' in user_input else 'TV Show' if 'show' in user_input else 'Series'
        genre = ' '.join(part for part in parts if part in ['action', 'adventure', 'anime', 'children', 'classic', 'comedies', 'cult', 'documentaries', 'dramas', 'faith', 'horror', 'independent', 'international', 'lgbtq', 'music', 'romantic', 'sci-fi', 'sports', 'stand-up', 'thrillers'])
        rating = ' '.join(part for part in parts if part in ['pg', 'pg-13', 'r', 'tv-ma', 'tv-pg'])
        
        # Get recommendations
        recommendations = get_recommendations(content_type, genre, rating)
        
        if isinstance(recommendations, str):
            print(recommendations)
        else:
            print("\nRecommended titles for you:")
            for title in recommendations['title']:
                print(f"- {title}")

if __name__ == "__main__":
    main()

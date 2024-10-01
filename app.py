import streamlit as st
import pickle
import requests

# Load the movies and similarity data
movies = pickle.load(open('movies.pkl', 'rb'))
movie_titles = movies['title'].values
movie_ids = movies['id'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to fetch poster URL from TMDb
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=6d42be403f662f66d2a006836d536059&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

# Function to recommend movies and fetch posters
def recommend(movie):
    movie_index = list(movie_titles).index(movie)
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movie_ids[i[0]]
        recommended_movies.append(movie_titles[i[0]])
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# Streamlit app
st.title('Movie Recommender System')

selected_movie = st.selectbox(
    'Which movie would you like to select',
    movie_titles
)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie)
    cols = st.columns(5)  # Create 5 columns for displaying recommendations
    for i in range(len(recommendations)):
        with cols[i]:
            st.text(recommendations[i])
            st.image(posters[i])

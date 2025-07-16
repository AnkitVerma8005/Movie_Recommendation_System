import streamlit as st
import pickle
import requests

def get_movie_poster(movie_id):
    # Base URL for TMDb API
    base_url = "https://api.themoviedb.org/3/movie/"

    # Construct the full URL
    url = f"{base_url}{movie_id}?api_key=a0c167c8b2ce778b354eab85b4f956f4&language=en-US"

    # Make the request to the TMDb API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Get the poster path
        poster_path = data.get('poster_path')
        if poster_path:
            # Construct the full poster URL
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return poster_url
        else:
            return "Poster not found."
    else:
        return f"Error: {response.status_code}"


def recommend(movie):
    # Check if the movie exists in the dataset
    if movie not in movies:
        st.error(f"Movie '{movie}' not found in the dataset.")
        return []

    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].movie_id  # Assuming you have a movie_id column
        recommended_movies.append(movies_df.iloc[i[0]].title)
        poster_url = get_movie_poster(movie_id)  # Get the poster URL for the recommended movie
        recommended_movies_poster.append(poster_url)

    return recommended_movies, recommended_movies_poster


# Load the movies and similarity data
movies_df = pickle.load(open('movies.pkl', 'rb'))
movies = movies_df['title'].values.tolist()  # Convert to list

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Select movie',
    movies
)

if st.button('Recommend'):
    recommendation, posters = recommend(selected_movie_name)
    if recommendation:  # Only display if there are recommendations
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommendation[0])
            st.image(posters[0])
        with col2:
            st.text(recommendation[1])
            st.image(posters[1])
        with col3:
            st.text(recommendation[2])
            st.image(posters[2])
        with col4:
            st.text(recommendation[3])
            st.image(posters[3])
        with col5:
            st.text(recommendation[4])
            st.image(posters[4])
import pickle
import streamlit as st
import requests
import pandas as pd
import os
import datetime


# Cache the API call to keep images in memory
@st.cache_data
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=18352b2baa250cd6fe8b99a5c7a5c709&language=en-US".format(
        movie_id)
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        return "https://via.placeholder.com/500x750?text=No+Poster"
    except Exception:
        return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):
    # Load data only once per session
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    # Simple check for excluded movies
    excluded = []
    if os.path.exists('user_feedback.csv'):
        df = pd.read_csv('user_feedback.csv')
        excluded = df[df['feedback'] == 'Dislike']['movie_name'].unique()

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])

    recs = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        if title != movie and title not in excluded:
            recs.append({'title': title, 'poster': fetch_poster(movies.iloc[i[0]].movie_id)})
        if len(recs) == 5: break
    return recs


st.header('Movie Recommender System')

selected_movie = st.selectbox("Select a movie", pd.DataFrame(pickle.load(open('movie_dict.pkl', 'rb')))['title'].values)

if st.button('Show Recommendation'):
    st.session_state.recs = recommend(selected_movie)

if 'recs' in st.session_state:
    cols = st.columns(5)
    for i, movie in enumerate(st.session_state.recs):
        with cols[i]:
            st.text(movie['title'])
            # By using a static image link from cache, we reduce flickering
            st.image(movie['poster'], use_container_width=True)
            b1, b2 = st.columns(2)
            if b1.button("👍", key=f"l{i}"): pass  # Add feedback logic here
            if b2.button("👎", key=f"d{i}"): pass  # Add feedback logic here
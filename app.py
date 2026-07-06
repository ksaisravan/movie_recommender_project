import pickle
import streamlit as st
import requests
import pandas as pd
import os
import datetime

def save_feedback(movie_name, feedback):
    df = pd.DataFrame([[movie_name, feedback, datetime.datetime.now()]],
                      columns=['movie_name', 'feedback', 'timestamp'])
    if os.path.exists('user_feedback.csv'):
        existing = pd.read_csv('user_feedback.csv')
        df = pd.concat([existing, df], ignore_index=True)
    df.to_csv('user_feedback.csv', index=False)

def get_excluded_movies():
    if os.path.exists('user_feedback.csv'):
        df = pd.read_csv('user_feedback.csv')
        return df[df['feedback'] == 'Dislike']['movie_name'].unique()
    return []

@st.cache_data
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=18352b2baa250cd6fe8b99a5c7a5c709&language=en-US".format(movie_id)
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        return "https://via.placeholder.com/500x750?text=No+Poster"
    except Exception:
        return "https://via.placeholder.com/500x750?text=No+Poster"

def recommend(movie):
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    excluded = get_excluded_movies()
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    recs = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        if title != movie and title not in excluded:
            recs.append({'title': title, 'poster': fetch_poster(movies.iloc[i[0]].movie_id)})
        if len(recs) == 5:
            break
    return recs

st.header('Movie Recommender System')

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

if os.path.exists('user_feedback.csv'):
    feedback_df = pd.read_csv('user_feedback.csv')
    likes = len(feedback_df[feedback_df['feedback'] == 'Like'])
    dislikes = len(feedback_df[feedback_df['feedback'] == 'Dislike'])
    st.caption(f"Likes: {likes} | Dislikes: {dislikes}")

selected_movie = st.selectbox("Select a movie", movies['title'].values)

col1, col2 = st.columns([4, 1])
with col1:
    if st.button('Show Recommendation'):
        st.session_state.recs = recommend(selected_movie)
with col2:
    if st.button('Reset Feedback'):
        if os.path.exists('user_feedback.csv'):
            os.remove('user_feedback.csv')
            st.success("Feedback reset successfully!")
            st.rerun()

if 'recs' in st.session_state:
    cols = st.columns(5)
    for i, movie in enumerate(st.session_state.recs):
        with cols[i]:
            st.text(movie['title'])
            st.image(movie['poster'], use_container_width=True)
            b1, b2 = st.columns(2)
            if b1.button("👍", key=f"like_{i}"):
                save_feedback(movie['title'], 'Like')
                st.success(f"Liked: {movie['title']}")
                st.rerun()
            if b2.button("👎", key=f"dislike_{i}"):
                save_feedback(movie['title'], 'Dislike')
                st.success(f"Disliked: {movie['title']}")
                st.rerun()
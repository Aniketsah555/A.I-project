import streamlit as st

import pandas as pd

import pickle

import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=104cbb5dcb418935c15cae05f9c9a2b7&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(similarity[0])), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []

    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        # poster from API
        recommended_movies_posters.append(fetch_poster(i[0]))
    return recommended_movies,recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title(":Movie Recommendation System :blue[cool] :sunglasses:")

selected_movie_name= st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values,
    index=None,
    placeholder="Select contact method...",
)

st.write("You selected:", selected_movie_name)

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)

    '''for i in recommendations:
        st.write(i)'''



#
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

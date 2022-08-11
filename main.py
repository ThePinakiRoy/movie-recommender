import streamlit as st
import pandas as pd
import pickle
import requests

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox('How would you like to be contacted?', movies['title'].values)


def fetch_poster(movie_id):
    api = '8265bd1679663a7ea12ac168da84d2e8'
    res = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US&external_source=imdb_id'.format(api, movie_id))
    data = res.json()
    return 'http://image.tmdb.org/t/p/w500/' + data['poster_path']


def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    list_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = {}
    count = 0

    for i in list_movies:
        movie_id = movies.iloc[i[0]].movie_id
        image_url = fetch_poster(movie_id)
        recommended_movies[count] = {'name': movies.iloc[i[0]].title, 'movie_id': movie_id, 'image': image_url}
        count += 1

    return recommended_movies


if st.button('Recommend'):
    recommended = recommend(selected_movie_name)
    movie_list = st.columns(len(recommended))
    for i in recommended:
        with movie_list[i]:
            st.text(recommended[i]['name'])
            st.image(recommended[i]['image'])

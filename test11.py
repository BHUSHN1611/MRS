import streamlit as st
import pickle
import pandas as pd
# import cssloads
import requests

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))




def recommend_movies(movie):
    flag = False
    for i in movies['title']:
        if (movie == i):
            flag = True
            break
        else:
            flag = False

    if flag == True:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
        rec_movies = []
        movies_posterpath= []
        # rec_movies_rating = []

        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            rec_movies.append(movies.iloc[i[0]].title)
            movies_posterpath.append(getjson(movie_id))

        if (rec_movies):
            return movies_posterpath#,rec_movies,


    else:
        print("no movies found")


def getjson(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=621f11a3e889718c83d29d87d900be79&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

# movies_name = "Pirates of the Caribbean: At World's End"
#
# print(recommend_movies(movies_name))



movie_titles = [
    "Avatar",
    "Pirates of the Caribbean: At World's End",
    "Spectre",
    "The Dark Knight Rises",
    "John Carter",
    "Spider-Man 3",
    "Tangled",
    "Avengers: Age of Ultron",
    "Harry Potter and the Half-Blood Prince",
    "Batman v Superman: Dawn of Justice",
    "Superman Returns",
    "Quantum of Solace",
    "Pirates of the Caribbean: Dead Man's Chest",
    "The Lone Ranger",
    "Man of Steel",
    "The Chronicles of Narnia: Prince Caspian",
    "The Avengers",
    "Pirates of the Caribbean: On Stranger Tides",
    "Men in Black 3",
    "The Hobbit: The Battle of the Five Armies",
    "The Amazing Spider-Man"
]
# movies_poster_path = {}
for i in movie_titles:
    print(i,"=",recommend_movies(i))

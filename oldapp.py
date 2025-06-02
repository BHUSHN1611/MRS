import streamlit as st  # front-end framework
import pickle  # use for serialization - use to convert data structure into pkl form
import pandas as pd
import requests  # use for api request

st.set_page_config(layout="wide")
st.title(" ☄️ MARS")
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1.9rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=621f11a3e889718c83d29d87d900be79&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

# main function hu main
def recommend(movie):
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
        rec_movies_poster = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            rec_movies.append(movies.iloc[i[0]].title)
            # poster fetching
            rec_movies_poster.append(fetch_poster(movie_id))

        if (rec_movies):
            return rec_movies, rec_movies_poster # this returns two things

    else:
        st.write("Movie is not present in dataset or their is spelling mistake")


# gui continues

def set_page(page_name):
    st.session_state.page = page_name


# Create horizontal navbar with buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Movies", type="primary", use_container_width=True):
        set_page("Movies")

with col2:
    if st.button("Series", type="primary", use_container_width=True):
        set_page("Series")

with col3:
    if st.button("Ai recommendation", type="primary", use_container_width=True):
        set_page("Ai recommendation")
with col4:
    if st.button("About us", type="primary", use_container_width=True):
        set_page("About us")


#
# Get popular movies for initial display.
def display_popular_movies():
    popular_movies_response = requests.get(
        "https://api.themoviedb.org/3/trending/movie/day?api_key=621f11a3e889718c83d29d87d900be79&language=en-US")
    popular_movies_response_data = popular_movies_response.json()
    st.title("Popular Movies")
    for i in range(1, 20):
        st.text(popular_movies_response_data["results"][i]["title"])


if "page" not in st.session_state:
    st.session_state.page = display_popular_movies()

# Display content based on selected page


if st.session_state.page == "Movies":
    st.title(f"{st.session_state.page} Page")
    selected_movie = st.selectbox(
        'Select the movies',
        movies['title'].values,
        index=None,
        placeholder='Search movies '
    )
    if st.button('Show Recommendation'):
        if (selected_movie):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.image(recommended_movie_posters[0], width=300)
                st.text(recommended_movie_names[0])
            with col2:
                st.image(recommended_movie_posters[1], use_container_width=True)
                st.text(recommended_movie_names[1])
            with col3:
                st.image(recommended_movie_posters[2], use_container_width=True)
                st.text(recommended_movie_names[2])
            with col4:
                st.image(recommended_movie_posters[3], use_container_width=True)
                st.text(recommended_movie_names[3])
            with col5:
                st.image(recommended_movie_posters[4], use_container_width=True)
                st.text(recommended_movie_names[4])
        else:
            st.text('No movies selected ')

elif st.session_state.page == "Series":
    st.title(f"{st.session_state.page} Page")
    st.write("This is the about page.")

elif st.session_state.page == "Ai recommendation":
    st.title(f"{st.session_state.page} Page")
    st.write("This is the contact page.")

elif st.session_state.page == "About us":
    st.title(f"{st.session_state.page} Page")
    st.write("Akash sir ")






# things to fix if u r exsmart ,
# then u have noticed , their is something fishy in ratings.
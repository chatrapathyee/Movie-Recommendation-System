import pickle
import streamlit as st
import requests
from streamlit.components.v1 import html

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide", initial_sidebar_state="expanded")

with open('static/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("""<div class="header"><h1>🎬 Movie Recommender System</h1></div>""", unsafe_allow_html=True)

movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
st.markdown("<div class='movie-select-label'>Type or select a movie from the dropdown</div>", unsafe_allow_html=True)

selected_movie = st.selectbox("", movie_list, index=0,  label_visibility="collapsed")

button_html = """
<script>
function setLoading(button, isLoading) {
    if (isLoading) {
        button.classList.add('active');
    } else {
        button.classList.remove('active');
    }
}

const buttons = window.parent.document.querySelectorAll('.stButton > button');
buttons.forEach(button => {
    button.addEventListener('click', function() {
        setLoading(this, true);
        // Re-enable button after animation completes (5 seconds timeout as fallback)
        setTimeout(() => setLoading(this, false), 5000);
    });
});
</script>
"""
st.components.v1.html(button_html, height=0)

if st.button('Show Recommendation'):
    loading_container = st.empty()
    
    with loading_container.container():
        st.markdown('''
            <div class="loading">
                <span class="loading-text">Finding your perfect movie matches...</span>
            </div>
        ''', unsafe_allow_html=True)
    
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    loading_container.empty()
    
    cols = st.columns(5)      
    for i in range(len(recommended_movie_names)):
        with cols[i % 5]:
            st.markdown(
                f'''
                <div class="movie-container">
                    <div class="movie-title" title="{recommended_movie_names[i]}">
                        {recommended_movie_names[i][:30] + '...' if len(recommended_movie_names[i]) > 30 else recommended_movie_names[i]}
                    </div>
                    <img src="{recommended_movie_posters[i]}" class="movie-poster" 
                         alt="{recommended_movie_names[i]}" 
                         style="max-width: 100%; height: auto;">
                </div>
                ''',
                unsafe_allow_html=True
            )





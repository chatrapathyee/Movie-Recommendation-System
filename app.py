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
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


# Set page config for better layout
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for the entire app
st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e) !important;
        color: white !important;
    }
    
    /* Main Content Area */
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Text Color */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div > div,
    .css-1d391kg p,
    .stMarkdown p,
    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3,
    .stMarkdown h4,
    .stMarkdown h5,
    .stMarkdown h6 {
        color: white !important;
    }
    
    /* Button Styles */
    .stButton>button {
        background: linear-gradient(45deg, #2196F3, #00BCD4) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.6rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(33, 150, 243, 0.4) !important;
    }
    
    .stButton>button:active {
        transform: translateY(0) !important;
    }
    
    /* Modern Loading Animation */
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes fadeInOut {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
    
    .loading {
        position: relative;
        display: inline-flex;
        align-items: center;
        gap: 12px;
        font-size: 16px;
        font-weight: 500;
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .loading::before {
        content: '';
        display: inline-block;
        width: 24px;
        height: 24px;
        border: 3px solid rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        border-top-color: #2196F3;
        border-right-color: #00BCD4;
        border-bottom-color: #4CAF50;
        animation: rotate 1s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    }
    
    .loading-text {
        animation: fadeInOut 2s ease-in-out infinite;
    }
    
    .loading.active::after {
        opacity: 1;
    }
    
    .loading-text {
        opacity: 1;
        transition: all 0.3s ease;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        letter-spacing: 0.5px;
    }
    
    .loading.active .loading-text {
        opacity: 0.8;
    }
    
    /* Movie Title */
    .movie-title {
        font-weight: bold !important;
        font-size: 15px !important;
        text-align: center;
        margin: 8px 0 !important;
        min-height: 2.5em;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1.3;
        width: 100%;
        padding: 0 5px;
    }
    .movie-poster {
        transition: transform 0.3s ease-in-out;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        max-width: 100%;
        height: auto;
        display: block;
        margin: 0 auto;
    }
    .movie-poster:hover {
        transform: scale(1.05);
    }
    .movie-container {
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        padding: 10px;
        box-sizing: border-box;
    }
    @media (max-width: 768px) {
        .movie-container {
            margin-bottom: 30px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Header styling
st.markdown("""
    <style>
    .header {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px);
        color: white !important;
        padding: 1.5rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .header:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            to bottom right,
            rgba(255, 255, 255, 0.1) 0%,
            rgba(255, 255, 255, 0) 50%
        );
        transform: rotate(30deg);
        pointer-events: none;
    }
    
    .header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
        position: relative;
    }
    
    .header h1::after {
        content: '';
        display: none;
        width: 60px;
        height: 3px;
        background: white;
        margin: 0.5rem auto 0;
        border-radius: 3px;
    }
    
    @media (max-width: 768px) {
        .header h1 {
            font-size: 1.8rem;
        }
    }
    
    /* Styling for the select box */
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 1px solid #e0e0e0 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #2196F3 !important;
        box-shadow: 0 2px 12px rgba(33, 150, 243, 0.2) !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #2196F3 !important;
        box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2) !important;
    }
    
    .stSelectbox > label {
        font-weight: 600 !important;
        color: #333 !important;
        margin-bottom: 8px !important;
        font-size: 16px !important;
    }
    
    /* Select box input and selected item */
    .stSelectbox > div > div > div > div {
        padding: 12px 40px 12px 15px !important;
        font-size: 16px !important;
        color: #333 !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
    }
    
    /* Dropdown menu items */
    .stSelectbox [data-baseweb="menu"] {
        border-radius: 10px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15) !important;
        border: 1px solid #e0e0e0 !important;
        margin-top: 5px !important;
    }
    
    /* Dropdown item hover state */
    .stSelectbox [role="option"] {
        padding: 10px 15px !important;
        font-size: 15px !important;
        transition: all 0.2s ease !important;
    }
    
    .stSelectbox [role="option"]:hover {
        background-color: #f5f9ff !important;
        color: #1976D2 !important;
    }
    
    /* Selected item in dropdown */
    .stSelectbox [aria-selected="true"] {
        background-color: #e3f2fd !important;
        color: #1976D2 !important;
        font-weight: 500 !important;
    }
    
    .stSelectbox > div > div > div[data-baseweb="select"] > div:after {
        border-color: #2196F3 transparent transparent !important;
    }
    
    .stSelectbox > div > div > div[data-baseweb="select"]:hover > div:after {
        border-color: #1976D2 transparent transparent !important;
    }
    
    /* Custom label style */
    .movie-select-label {
        font-weight: 600 !important;
        color: #FFFFFF !important;
        margin-bottom: 8px !important;
        font-size: 16px !important;
        display: block;
        text-align: left;
        padding-left: 5px;
        letter-spacing: 0.3px;
        text-transform: none;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .movie-select-label::after {
        content: ' *';
        color: #ff4b4b;
    }
    </style>
    
    <div class="header">
        <h1>🎬 Movie Recommender System</h1>
    </div>
""", unsafe_allow_html=True)

# Load data
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
st.markdown("<div class='movie-select-label'>Type or select a movie from the dropdown</div>", unsafe_allow_html=True)

# Add custom CSS for the selectbox
st.markdown("""
<style>
    /* Base styles for the select box */
    .stSelectbox > div > div {
        background-color: white !important;
        border-radius: 8px !important;
        border: 1px solid #2196F3 !important;
        min-height: 40px !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Selected value text */
    .stSelectbox > div > div > div > div {
        color: #333333 !important;
        font-size: 16px !important;
        padding: 8px 15px 8px 12px !important;
        line-height: 1.5 !important;
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: unset !important;
        width: 100% !important;
        display: block !important;
    }
    
    /* Input field */
    .stSelectbox input {
        color: #333333 !important;
        background-color: white !important;
        padding: 10px 15px !important;
        font-size: 16px !important;
    }
    
    /* Placeholder text */
    .stSelectbox input::placeholder {
        color: #999999 !important;
        opacity: 1 !important;
    }
    
    /* Dropdown arrow */
    .stSelectbox > div > div > div[data-baseweb="select"] > div:after {
        border-color: #2196F3 transparent transparent !important;
    }
    
    /* Dropdown menu */
    [data-baseweb="popover"] {
        border-radius: 12px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        background: rgba(30, 30, 50, 0.95) !important;
        margin-top: 8px !important;
        backdrop-filter: blur(10px) !important;
        overflow: hidden !important;
    }
    
    /* Custom scrollbar for dropdown */
    [data-baseweb="popover"]::-webkit-scrollbar {
        width: 8px !important;
        background: #f5f5f5 !important;
        border-radius: 4px !important;
    }
    
    [data-baseweb="popover"]::-webkit-scrollbar-thumb {
        background: #2196F3 !important;
        border-radius: 4px !important;
    }
    
    [data-baseweb="popover"]::-webkit-scrollbar-track {
        background: #f5f5f5 !important;
        border-radius: 4px !important;
    }
    
    /* Dropdown items */
    [role="option"] {
        padding: 14px 24px !important;
        color: #ffffff !important;
        font-size: 15px !important;
        font-weight: 400 !important;
        transition: all 0.25s ease !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: transparent !important;
    }
    
    [role="option"]:hover {
        background: linear-gradient(90deg, rgba(33, 150, 243, 0.2), transparent) !important;
        color: #4fc3f7 !important;
        transform: translateX(4px);
        padding-left: 28px !important;
    }
    
    [aria-selected="true"] {
        background: linear-gradient(90deg, rgba(33, 150, 243, 0.3), transparent) !important;
        color: #4fc3f7 !important;
        font-weight: 500 !important;
        border-left: 3px solid #4fc3f7 !important;
    }
    
    /* Remove the last border */
    [role="option"]:last-child {
        border-bottom: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Create the selectbox
selected_movie = st.selectbox(
    "",  # Empty label since we're adding it separately
    movie_list,
    index=0,  # Set a default selected index
    label_visibility="collapsed"  # Hide the default label
)

# Add custom button with loading state
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
    # Create a container for the loading animation
    loading_container = st.empty()
    
    # Show loading animation
    with loading_container.container():
        st.markdown('''
            <div class="loading">
                <span class="loading-text">Finding your perfect movie matches...</span>
            </div>
            <style>
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .loading {
                    animation: fadeIn 0.5s ease-out forwards;
                    margin: 2rem 0;
                }
            </style>
        ''', unsafe_allow_html=True)
    
    # Get recommendations
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Clear the loading animation
    loading_container.empty()
    
    # Display recommendations
    cols = st.columns(5)  
    
    st.markdown("""
    <style>
        @media (max-width: 1200px) {
        .st-emotion-cache-ocqkz7 {
            display: flex !important;
            flex-wrap: wrap !important;
            justify-content: center !important;
            gap: 1.5rem !important;
        }
        [data-testid="column"] {
            min-width: 160px !important;
            max-width: 200px !important;
            flex: 1 1 auto !important;
        }
    }
    @media (max-width: 768px) {
        [data-testid="column"] {
            min-width: 140px !important;
            max-width: 160px !important;
        }
    }
    @media (max-width: 480px) {
        [data-testid="column"] {
            min-width: 120px !important;
            max-width: 160px !important;
        }    }
        }
    </style>
    """, unsafe_allow_html=True)
    
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





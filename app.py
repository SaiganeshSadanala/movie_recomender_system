import pickle
import streamlit as st
import requests
import pandas as pd

API_KEY = "YOUR API KEY"

st.set_page_config(
    page_title="Movie Recommender",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize session state variables if not already initialized
if 'recommend' not in st.session_state:
    st.session_state.recommend = ([], [], [], [])
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    try:
        data = requests.get(url).json()
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return None

def fetch_providers(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"
    try:
        data = requests.get(url).json()
        providers = data['results']
        max_providers = 0
        top_country = None
        top_country_providers = []
        for country, provider_info in providers.items():
            if 'flatrate' in provider_info:
                num_providers = len(provider_info['flatrate'])
                if num_providers > max_providers:
                    max_providers = num_providers
                    top_country = country
                    top_country_providers = provider_info['flatrate']
        return top_country, top_country_providers
    except Exception as e:
        st.error(f"Error fetching providers: {e}")
        return None, None

def recommend(selected_movie):
    if selected_movie in movies['title'].values:
        movie_index = movies[movies['title'] == selected_movie].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]
        recommended_movie_names = []
        recommended_movie_posters = []
        recommended_movie_details = []
        recommended_movie_cast = []
        for i in movie_list:
            recommended_movie_posters.append(fetch_poster(movies.iloc[i[0]].id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_details.append(movies.iloc[i[0]].overview)
            recommended_movie_cast.append(movies.iloc[i[0]].cast)
        return recommended_movie_names, recommended_movie_posters, recommended_movie_details, recommended_movie_cast
    else:
        return [], [], [], []

def fetch_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    trailers = [video for video in data['results'] if video['site'] == 'YouTube' and video['type'] == 'Trailer']
    if trailers:
        return f"https://www.youtube.com/watch?v={trailers[0]['key']}"
    else:
        return None

st.markdown("""
    <style>
    .poster-img {
        width: 100%;
        height: auto;
    }
    .selected-poster-img {
        width: 60%;
        height: auto;
    }
    .movie-details {
        font-size: 14px;
    }

    @media (max-width: 768px) {
        .selected-poster-img {
            width: 80%;
        }
    }
    @media (max-width: 480px) {
        .selected-poster-img {
            width: 100%;
        }
        .poster-img {
            width: 80%; /* Decrease the size of recommended movie posters */
        }
        .movie-details {
            font-size: 12px;
        }
    }

    /* Background video */
    .background-video {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: -1;
    }

    /* Container to hold content */
    .content {
        position: relative;
        z-index: 1;
    }

    /* Video container */
    .video-container {
        position: relative;
        padding-bottom: 56.25%; /* 16:9 aspect ratio */
        height: 0;
        overflow: hidden;
        max-width: 100%;
        background: #000;
    }
    .video-container iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Add a local video as background at the top of the web app
st.markdown("""
    <video autoplay muted loop class="background-video">
        <source src="background.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    <div class="content">
    """, unsafe_allow_html=True)

st.title("Welcome to the Movie Recommender System!")

movies_dic = pickle.load(open('movie_dic.pkl', 'rb'))
movies = pd.DataFrame(movies_dic)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Define a callback function for when a movie is selected
def movie_selected():
    st.session_state.selected_movie = st.session_state['selected_movie']
    if st.session_state.selected_movie:
        if 'recommendations' not in st.session_state or st.session_state.selected_movie != st.session_state.recommend[0]:
            st.session_state.recommend = recommend(st.session_state.selected_movie)
    else:
        st.session_state.recommend = ([], [], [], [])
    # Add JavaScript to blur the input field after a selection
    st.markdown("""
        <script>
        document.activeElement.blur();
        </script>
        """, unsafe_allow_html=True)

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    options=['Select any movie'] + list(movies['title'].values),
    key='selected_movie',
    on_change=movie_selected
)

def embed_youtube_video(video_id):
    return f'''
    <div class="video-container">
        <iframe src="https://www.youtube.com/embed/{video_id}" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
        </iframe>
    </div>
    '''

if st.session_state.selected_movie:
    st.markdown(f"<h2 class='fade-in'>Selected Movie: {st.session_state.selected_movie}</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])

    selected_movie_index = movies[movies['title'] == st.session_state.selected_movie].index[0]
    selected_movie_data = movies.iloc[selected_movie_index]
    selected_movie_poster = fetch_poster(selected_movie_data.id)

    # Embed image with custom class for selected movie poster
    col1.markdown(f"<img src='{selected_movie_poster}' class='selected-poster-img'>", unsafe_allow_html=True)

    middle_col = col2.empty()

    with middle_col:
        st.markdown(f"**Cast**: {selected_movie_data.cast}", unsafe_allow_html=True)
    with col3:
        trailer_link = fetch_trailer(selected_movie_data.id)
        if trailer_link:
            video_id = trailer_link.split('=')[-1]
            st.markdown(embed_youtube_video(video_id), unsafe_allow_html=True)

    with col2:
        movie_expander = st.expander(label=f"Details of {st.session_state.selected_movie}", expanded=True)
        with movie_expander:
            st.markdown(f"<div class='slide-down'>{selected_movie_data.overview}</div>", unsafe_allow_html=True)

    # Fetch and display providers with icons and links in a single row
    top_country, top_country_providers = fetch_providers(selected_movie_data.id)
    if top_country and top_country_providers:
        st.markdown(f"**Available in {top_country} on:**", unsafe_allow_html=True)
        provider_cols = st.columns(len(top_country_providers))
        for idx, provider in enumerate(top_country_providers):
            provider_name = provider['provider_name']
            provider_icon = f"https://image.tmdb.org/t/p/original{provider['logo_path']}"
            provider_url = provider.get('link', "#")
            with provider_cols[idx]:
                st.markdown(f"<a href='{provider_url}' target='_blank'><img src='{provider_icon}' alt='{provider_name}' title='{provider_name}' width='50'></a> {provider_name}", unsafe_allow_html=True)

    st.markdown(f"**Recommendations for movie:** {st.session_state.selected_movie}", unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    names, posters, info, cast = st.session_state.recommend

    for i in range(6):
        with col1 if i == 0 else col2 if i == 1 else col3 if i == 2 else col4 if i == 3 else col5 if i == 4 else col6:
            st.markdown(f"<b class='fade-in'>{names[i]}</b>", unsafe_allow_html=True)
            st.markdown(f"<img src='{posters[i]}' class='poster-img'>", unsafe_allow_html=True)
            movie_expander = st.expander(label=f"Details for {names[i]}", expanded=False)
            with movie_expander:
                st.markdown(f"<div class='slide-down'>{info[i]}</div>", unsafe_allow_html=True)

else:
    st.markdown("<h2>Select any movie</h2>", unsafe_allow_html=True)

# Close the content div
st.markdown("</div>", unsafe_allow_html=True)

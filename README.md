# 🍿 Movie Recommender System

Welcome to the Movie Recommender System! This project aims to provide personalized movie recommendations based on user input. By selecting a movie from the dropdown, users can receive a list of similar movies, complete with posters, details, and trailers.

## Features

- **Movie Selection**: Choose a movie from a dropdown menu to get recommendations.
- **Recommendations**: Get a list of six similar movies based on the selected movie.
- **Movie Posters**: View the poster of each recommended movie.
- **Movie Details**: Read an overview and cast information of the recommended movies.
- **Trailers**: Watch trailers of the recommended movies directly within the app.

## Demo

A live demo of the app can be accessed [here](#).

## Installation

To run the Movie Recommender System locally, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/movierecommender.git
    cd movierecommender
    ```

2. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Download the necessary data files**:
    - Ensure you have the `movie_list.pkl` and `similarity.pkl` files in the project directory.

4. **Run the application**:
    ```sh
    streamlit run app.py
    ```

## Usage

1. Open your web browser and go to `http://localhost:8501`.
2. Select a movie from the dropdown menu.
3. View the recommendations along with their posters, details, and trailers.

## Code Overview

### `app.py`

This file contains the main code for the Streamlit web application. Key functionalities include:

- **Fetching Movie Posters**: Using the TMDb API to get movie posters.
- **Generating Recommendations**: Calculating movie similarity and generating recommendations.
- **Fetching Trailers**: Using the TMDb API to get YouTube trailers for movies.
- **User Interface**: Displaying the selected movie, recommendations, and their details in a user-friendly format.

### `movie_recommendation_code.ipynb`

This Jupyter notebook contains the code used to preprocess data, compute movie similarities, and save the required `.pkl` files used by the Streamlit app.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License

## Acknowledgments

- Data provided by [The Movie Database (TMDb)](https://www.themoviedb.org/).
- [Streamlit](https://streamlit.io/) for the web application framework.

## Contact

For any questions or comments, please open an issue or contact [Gmail](mailto:sadanalasaiganesh54@gmail.com).

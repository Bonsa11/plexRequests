from imdb import Cinemagoer, IMDbDataAccessError
from PIL import Image
import requests
from io import BytesIO

def search_for_movies(search_term):
    access = Cinemagoer()
    search = access.search_movie(search_term)

    return search

def get_movie_data(search):

    all_data = []
    for film in search:
        try:
            access = Cinemagoer()
            movie = access.get_movie(film.movieID)

            if 'title' in movie:
                title = movie['title']
            else:
                title = 'None'

            if 'rating' in movie:
                rating = movie['rating']
            else:
                rating = 'None'

            if 'year' in movie:
                year = movie['year']
            else:
                year = 'None'

            if 'cover url' in movie:
                urlObj = requests.get(movie['cover url'])
                img = Image.open(BytesIO(urlObj.content))
            else:
                img = None

            movie_data = [img, [title, rating, year, film.movieID]]

            print(movie_data[1])
            all_data.append(movie_data)

        except IMDbDataAccessError:
            pass

    return all_data


def get_choices(search_term):
    search = search_for_movies(search_term)
    get_movie_data(search)

if __name__ == '__main__':
    get_choices('Dune')
from pyYify import yify
from variableConfigs import download_path
import os
from datetime import datetime


def get_torrents(searchTerm: str, imdbID: str):

    movie_list = yify.search_movies(searchTerm.lower())
    movie = [movie for movie in movie_list if movie.imdb_code == imdbID][0]

    if len(os.listdir(download_path)) > 10:
        raise MemoryError('too many torrents queed at this time, try again later')

    for file in os.listdir(download_path):
        if ''.join([searchTerm, datetime.now().strftime("%Y%m%d")]) in file:
            raise FileExistsError('Torrent exists in folder')
    if len(movie.torrents) == 0:
        raise FileNotFoundError('no torrents found')
    good_torrents = []
    for res in ['1080p', '2160p', '720p']:
        good_torrents += sorted([torrent for torrent in movie.torrents if torrent.quality == res], key=lambda x: x.seeds, reverse=True)

    for torrent in good_torrents:
        try:
            filename = ''.join([searchTerm, datetime.now().strftime("%Y%m%d-%H%M%S")])
            torrent.download_torrent_file(download_path, filename)
            print(f'successfully downloaded {movie.title} to {download_path}')
            break

        except Exception as e:
            print(e)
            print(f'failed to download {movie.title}, trying next torrent')

    if not os.path.exists(os.path.join(download_path, f'{filename}.torrent')):
        raise FileNotFoundError('Not able to downloads any of the Torrents')


if __name__ == '__main__':
    torrents = get_torrents('Dune', 'tt1160419')

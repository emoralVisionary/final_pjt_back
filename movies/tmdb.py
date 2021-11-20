# pip install requests
import requests
import json

API_KEY = '32a3b4bf2c76f30081e40ba9e1112640'
BASE_URL = 'https://api.themoviedb.org/3'

# movie_url = f'{BASE_URL}/movie/popular?api_key={API_KEY}&language=ko-KR&page='
# genre_url = f'{BASE_URL}/genre/movie/list?api_key={API_KEY}'


def create_genre_data():
  genre_url = f'{BASE_URL}/genre/movie/list?api_key={API_KEY}'

  data = requests.get(genre_url).json()
  genres = data.get('genres')

  genre_data = []

  for genre in genres:
    tmp = {
      'model': 'movies.genre',
      'pk': genre['id'],
      'fields': {
        'name': genre['name']
      }
    }
    genre_data.append(tmp)

  with open('fixtures/tmdb.json', 'w') as f:
    json.dump(genre_data, f, indent=4)

  

def create_movie_data():
  with open('fixtures/tmdb.json', 'r+') as f:
    movie_data = json.load(f)

  for page in range(1, 50):
    # print(str(page))
    movie_url = f'{BASE_URL}/movie/popular?api_key={API_KEY}&language=ko-KR&page={str(page)}'

    data = requests.get(movie_url).json()
    movies = data.get('results')

  for movie in movies:
    if movie.get('release_date') == "" or movie.get('poster_path') == "":
      continue

    movie.pop('backdrop_path')
    movie.pop('video')
    tmp = {
        'model': 'movies.movie',
        'pk': movie.pop('id'),
        'fields': movie,
    }
    movie_data.append(tmp)
    movie['like_users'] = []

  with open('fixtures/tmdb.json', 'w', encoding='utf-8') as f:
      json.dump(movie_data, f, ensure_ascii=False, indent=4)


create_genre_data()
create_movie_data()
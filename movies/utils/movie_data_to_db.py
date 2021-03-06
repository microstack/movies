import json
import datetime

from movies.models import db
from movies.models.actor import Actor
from movies.models.movie import Movie
from movies.models.genre import Genre

def read_movie_data_as_py_object(file_name):
    data = []
    with open(file_name, 'r') as f:
        data = json.loads(f.read())
    return data


def all_movie_data_to_db(data):
    for partial in data:
        one_movie_data_to_db(partial)


def one_movie_data_to_db(partial):
    def genres_to_db():
        for name in partial['genres']:
            query = Genre.query.filter_by(name=name).first()
            if query is not None:
                print('The genre already exists : %s' % name)
                continue
            elif query is '':
                print('blank query filtered')
                continue
 
            genre = Genre()
            genre.name = name
            db.session.add(genre)
            db.session.commit()
            print('db commit complete : %s' % genre)

       
    def actors_to_db():
        for name, link in partial['actors'].items():
            if Actor.query.filter_by(link=link).first() is not None:
                print('input actor link already exist : %s, %s' %
                    (name , link))
                continue
            actor = Actor()
            actor.name, actor.link = name, link
            db.session.add(actor)
            db.session.commit()
            print('db commit complete : %s' % actor)

    def movie_to_db():
        movie = Movie()

        movie.title = partial['title']
        movie.age = partial['age']
        movie.director = partial['director']

        try:
            movie.netizen_grade = float(partial['netizen_grade'])
        except ValueError:
            print("the string format cannot be converted as float : %s" %
                partial['netizen_grade'])

        date_list = partial['release_date'].split('.')
        if len(date_list) != 3:
            print("date format is incorrect, therefore ignored : %s" %
                date_list)
        else:
            year, month, day = partial['release_date'].split('.')
            year, month, day = int(year), int(month), int(day)
            if month == 0 or day == 0:
                month, day = 1, 1
            movie.release_date = datetime.date(year, month, day)

        running_time = partial['running_time']
        movie.running_time = ''.join(
            filter(lambda x: x.isdigit(), running_time))

        movie.story = partial['story']
        movie.thumbnail = partial['thumbnail']

        for name in partial['genres']:
            genre = Genre.query.filter_by(name=name).first()
            movie.genres.append(genre)

        for link in partial['actors'].values():
            actor = Actor.query.filter_by(link=link).first()
            movie.actors.append(actor)

        db.session.add(movie)
        db.session.commit()
        print('db commit complete : %s' % movie)

    genres_to_db()
    actors_to_db()
    movie_to_db()


import os
path = os.environ.get('MOVIES_UTIL_DATA_PATH')
movie_data_path = path + 'movie_data.json'


def all_in_one():
    db.drop_all()
    db.create_all()
    data = read_movie_data_as_py_object(movie_data_path)
    all_movie_data_to_db(data)

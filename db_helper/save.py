import logging
import traceback
import pymysql
from db_helper import passwd


def my_map(my_dict, my_key):
    if my_key in my_dict:
        return my_dict[my_key]
    else:
        return None


def my_map_double(my_dict, my_key):
    if my_key in my_dict:
        if my_dict[my_key]:
            return float(my_dict[my_key])
        else:
            return 0
    else:
        return 0


def my_map_int(my_dict, my_key):
    if my_key in my_dict:
        if my_dict[my_key]:
            return int(my_dict[my_key])
        else:
            return 0
    else:
        return 0


def list_to_string_split(my_list):
    res = ''
    if my_list:
        res = '/'.join(my_list)
    return res


def list_to_string(my_list):
    res = ''
    if my_list:
        res = ''.join(my_list)
    return res


def data_convert(film):
    film_data = (
        list_to_string_split(my_map(film, 'actors')), my_map(film, 'country'),
        list_to_string_split(my_map(film, 'directors')),
        my_map(film, 'filmType'), my_map(film, 'filmWatchURL'), my_map(film, 'imdb_filmID'), my_map(film, 'language'),
        my_map(film, 'name'),
        my_map(film, 'onTime'), my_map(film, 'posterURL'), my_map(film, 'ratingNum'), my_map_double(film, 'score'),
        my_map_double(film, 'douban_score'), list_to_string_split(my_map(film, 'scriptKeyWords')),
        my_map(film, 'summary'),
        my_map(film, 'tagLine'), list_to_string_split(my_map(film, 'tags')), my_map(film, 'cast'),
        my_map(film, 'storyline'),
        my_map(film, 'award'),
        my_map_double(film, 'runtime'), my_map(film, 'soundmix'), my_map_int(film, 'Oscar'),
        my_map_int(film, 'budget'),
        my_map_int(film, 'gross'), my_map_int(film, 'worldwideGross'),
        0, 0, 0, 0, 0, 0, 0, 0
    )

    return film_data


def save_producer(producer):
    producer_sql = '''INSERT ignore INTO filmdia.ProducerDB(films, image, imdb_producerID, name, producerType) 
                VALUES(%s,%s,%s,%s,%s)'''

    producer_data = (list_to_string_split(my_map(producer, 'films')), my_map(producer, 'image'),
                     my_map(producer, 'producer_id'), my_map(producer, 'name'), my_map(producer, 'type'))

    # print('producer', producer_data)
    try:
        cursor.execute(producer_sql, producer_data)
        db.commit()
    except Exception as e:
        db.rollback()
        print('insert producer wrong', e.args)
        logging.error(traceback.format_exc())


def save_film_update(film):
    # save to all FilmDB first
    save_film(film)

    update_film_sql = '''REPLACE INTO filmdia.UpdateFilm
    (actors, country, directors, filmType, filmWatchURL, imdb_filmID, 
    language, name, onTime, posterURL, ratingNum, score, douban_score, 
    scriptKeyWords, summary, tagLine, tags, cast, storyline, award, 
    runtime, soundmix, Oscar, budget, gross, worldwideGross, 
    linear_predict,linear_test,lasso_predict,lasso_test,knn_predict,knn_test,poly_predict,poly_test) 
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''

    film_data = data_convert(film)
    # print(film_data)
    try:
        cursor.execute(update_film_sql, film_data)
        db.commit()
    except Exception as e:
        db.rollback()
        print('update film wrong', e.args)
        logging.error(traceback.format_exc())
        print(film_data)


def save_film(film):
    film_sql = '''REPLACE INTO filmdia.FilmDB
        (actors, country, directors, filmType, filmWatchURL, imdb_filmID, 
        language, name, onTime, posterURL, ratingNum, score, douban_score, 
        scriptKeyWords, summary, tagLine, tags, cast, storyline, award, 
        runtime, soundmix, Oscar, budget, gross, worldwideGross) 
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''

    film_data = data_convert(film)

    try:
        cursor.execute(film_sql, film_data)
        db.commit()
        print('save film', film_data[7])
    except:
        db.rollback()


def save_review(review):
    review_sql = '''INSERT ignore INTO filmdia.Review(helpfulness, imdb_filmID, score, summary, text, time, userName, userCountry, userInfo_userID) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    review_data = (my_map(review, 'helpfulness'), my_map(review, 'imdb_filmID'), my_map_double(review, 'score'),
                   my_map(review, 'summary'), my_map(review, 'text'),
                   my_map(review, 'time'), my_map(review, 'userName'),
                   my_map(review, 'userCountry'), my_map(review, 'userInfo_userID')
                   )
    # print('review', review_data)
    try:
        cursor.execute(review_sql, review_data)
        db.commit()
    except Exception as e:
        db.rollback()
        print('insert review wrong', e.args)
        logging.error(traceback.format_exc())


db = pymysql.connect(passwd.domain, passwd.user, passwd.password, passwd.db, charset='utf8')
cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

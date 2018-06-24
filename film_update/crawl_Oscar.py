from crawler_util import page_read
from film_update import moviescrawler
from db_helper.save import cursor, db


def get_exist_list():
    exist_tup = cursor.fetchall()
    exists = list()
    for a_item in exist_tup:
        exists.append(a_item[0])
    return exists


cursor.execute('SELECT imdb_filmID FROM FilmDB')
exist_films = get_exist_list()
soup = page_read.page_read_nolog(
    'http://www.imdb.com/search/title?count=100&'
    'groups=oscar_best_picture_winners&title_type=feature&sort=release_date,desc')
imdb_href = 'http://www.imdb.com'
for item in soup.select('.lister-item-header'):
    # print  movieurl
    the_filmid = item.a.get('href').split('title/')[1].split('/')[0]
    if the_filmid in exist_films:
        cursor.execute(
            '''UPDATE FilmDB SET Oscar = 1 WHERE imdb_filmID=%s''',
            (the_filmid,))
        db.commit()
    else:
        print(the_filmid)
        moviescrawler.crawl_imdb(the_filmid, 'Oscar')
db.commit()

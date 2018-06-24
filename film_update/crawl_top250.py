from crawler_util import page_read
from film_update import moviescrawler
from db_helper.save import cursor, db


def get_exist_list():
    cursor.execute('SELECT imdb_filmID FROM FilmDB')
    exists = [x[0] for x in cursor]
    return exists


exist_films = get_exist_list()
soup = page_read.page_read_nolog('http://www.imdb.com/chart/top/?ref_=nv_mv_250_6')
for item in soup.select('.titleColumn'):
    ref = item.a.get('href').strip()
    film_id = ref.split('title/')[1].split('/')[0]

    if film_id in exist_films:
        cursor.execute(
            '''UPDATE FilmDB SET filmType = 'Top250' WHERE imdb_filmID=%s''',
            (film_id,))
        print(film_id)
        db.commit()
    else:
        moviescrawler.crawl_imdb(film_id, 'Top250')
db.commit()

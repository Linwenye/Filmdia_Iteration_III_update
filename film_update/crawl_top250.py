import MySQLdb
from crawler_util import page_read
from film_update import moviescrawler
from db_helper.save import cursor, db

i = 0
soup = page_read.page_read_nolog('http://www.imdb.com/chart/top/?ref_=nv_mv_250_6')
for item in soup.select('.titleColumn'):
    ref = item.a.get('href').strip()
    film_id = ref.split('title/')[1].split('/')[0]
    # if film_id:
    #     cursor.execute('''UPDATE FilmDB SET filmType =%s WHERE imdb_filmID=%s''',
    #                    ('Top250', film_id))
    # else:
    moviescrawler.crawl_imdb(film_id, 'Top250', 'False')
db.commit()

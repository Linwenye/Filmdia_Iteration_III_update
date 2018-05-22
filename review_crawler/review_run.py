import pymysql
import reviewscrawler
from db_helper import passwd

db_former = pymysql.connect('139.199.180.86', 'xzh', 'xzh123456', 'filmdia')
cursor_former = db_former.cursor()
cursor_former.execute('SELECT DISTINCT imdb_filmID FROM FilmDB')
filmids = cursor_former.fetchall()

db = pymysql.connect(passwd.domain, passwd.user, passwd.password, passwd.db,charset='utf8')
cursor = db.cursor()
db.set_character_set('utf8')
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

cursor.execute('SELECT DISTINCT imdb_filmID FROM filmdia.Review')
filmids_exist = cursor.fetchall()
for filmid in filmids:
    print(filmid[0])
    if filmid not in filmids_exist:
        reviewscrawler.reviewscrawler(filmid[0])

db.commit()
db.close()
db_former.close()

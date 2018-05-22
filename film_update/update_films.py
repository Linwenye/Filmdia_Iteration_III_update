# -*- coding: UTF-8 -*-
import pymysql
from crawler_util import page_read
from film_update import moviescrawler
from db_helper import passwd

db = pymysql.connect(passwd.domain, passwd.user, passwd.password, passwd.db,charset='utf8')
cursor = db.cursor()

create_film = '''CREATE TABLE IF NOT EXISTS UpdateFilm(
              filmID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
              actors VARCHAR(255),
              country VARCHAR(255),
              directors VARCHAR(255),
              filmType VARCHAR(255),
              filmWatchURL VARCHAR(255),
              imdb_filmID CHAR(9) NOT NULL,
              language VARCHAR(255),
              name VARCHAR(255),
              onTime DATE,
              posterURL VARCHAR(255),
              ratingNum INT,
              score DOUBLE,
              douban_score DOUBLE,
              scriptKeyWords VARCHAR(255),
              summary VARCHAR(1000),
              tagLine VARCHAR(255),
              tags VARCHAR(255),
              cast VARCHAR(1000),
              storyline VARCHAR(1500),
              award VARCHAR(255),
              runtime INT,
              soundmix VARCHAR(255),
              Oscar BOOL,
              budget INT,
              gross INT,
              worldwideGross INT,
              linear_predict INT,
              linear_test DOUBLE,
              lasso_predict INT,
              lasso_test DOUBLE,
              knn_predict INT,
              knn_test DOUBLE,
              poly_predict INT,
              poly_test DOUBLE,
              UNIQUE(imdb_filmID) 
              )DEFAULT CHARSET = utf8'''

cursor.execute(create_film)
cursor.execute('DELETE FROM UpdateFilm')
db.commit()
db.close()

imdb_href = 'http://www.imdb.com/'
soup = page_read.page_read_power(imdb_href)

film_type = ('ThisWeek', 'Latest', 'Coming')

for i in range(0, 3):
    for item in soup.select('.aux-content-widget-2')[i].select('.title'):
        film_id = item.a['href'].split('title/')[1].split('?')[0]

        moviescrawler.crawl_imdb(film_id, film_type[i], need_update=True)

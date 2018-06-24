# encoding = utf-8
from crawler_util import page_read
import urllib.parse
import re
from db_helper.save import cursor,db


def filter_click(s):
    if s:
        if s.find('ago') > 0:
            tt = s.split(' ago')
            tt[1] = get_num(tt[1])
            return tt


def get_num(s):
    if s.find('(') >= 0:
        s = s[:s.find('(')]
    res = ''
    pattern = '[0-9]+'
    numlist = re.findall(pattern, s)
    for letter in numlist:
        res += letter
    if res != '':
        return int(res)
    else:
        return 0


def get_click(name):
    name = name + ' official trailer'
    the_url = 'http://www.youtube.com/results?search_query=' + urllib.parse.quote(name)
    soup = page_read.page_read_nolog(the_url)
    if soup:
        print(soup)
        info_line = soup.find_all(id='metadata-line')
        print(info_line)
        if len(info_line) >= 2:
            print(info_line[0].span.get_string())
            # t1 = filter_click(soup.select('.yt-lockup-meta-info')[0].get_text())
            # t2 = filter_click(soup.select('.yt-lockup-meta-info')[1].get_text())
            # if t1 and t2:
            #     if t1[1] > t2[1]:
            #         return t1
            #     else:
            #         return t2
    else:
        print('fail to connect youtube')


if __name__ == '__main__':
    # # username password
    # db = MySQLdb.connect(passwd.domain, passwd.user, passwd.password, "filmdia")
    #
    # cursor = db.cursor()
    # db.set_character_set('utf8')
    # cursor.execute('SET NAMES utf8;')
    # cursor.execute('SET CHARACTER SET utf8;')
    # cursor.execute('SET character_set_connection=utf8;')
    #
    # cursor.execute('SELECT imdb_filmID,name FROM UpdateFilm')
    # # cursor.execute(
    # #     'SELECT imdb_filmID,name FROM FilmDB WHERE gross>1000000 AND gross>FilmDB.budget/2 AND onTime>\'2009-01-01\' AND (country=\'USA\' OR country = \'UK\')')
    # film_list = cursor.fetchall()
    #
    # print 'list:', len(film_list)
    # # cursor.execute('SELECT imdb_filmID FROM TrailerClick')
    # # film_exist_list = get_exist_list()
    #
    # db.close()
    #
    # for item in film_list:
    #     # if item[0] not in film_exist_list:
    #     t = get_click(item[1])
    #     if t:
    #         click = t[1]
    #         uploadtime = t[0]
    #         if click != 0:
    #             print item[0], item[1], uploadtime, click
    #             save.save_click(item[0], click, uploadtime)
    get_click('star wars')
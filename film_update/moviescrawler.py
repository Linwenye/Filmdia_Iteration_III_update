from crawler_util import page_read
from crawler_util import convert_time
from db_helper import save
import producerscrawler
from review_crawler import reviewscrawler
import douban_score
from crawler_util.util import get_num
import re


def crawl_imdb(film_id, film_type, need_update=False):
    movieurl = 'http://www.imdb.com/title/' + film_id + '/'
    soup = page_read.page_read_nolog(movieurl)
    if not soup:
        return
    film = dict()
    # write id and name
    film['imdb_filmID'] = film_id
    film_name = soup.find_all(attrs={'itemprop': 'name'})[0].get_text()
    film['name'] = film_name

    # write summary and directors,etc.
    summary_text = soup.select('.summary_text')[0]
    if summary_text:
        summary = summary_text.get_text().strip().split("See")[0].strip()
        film['summary'] = summary
    else:
        print 'no summary'
    directors = list()
    actors = list()
    for dire in soup.find_all(attrs={'itemprop': 'director'}):
        directors.append(dire.a['href'].split('name/')[1].split('/?')[0])
    for dire in soup.find_all(attrs={'itemprop': 'actors'}):
        actors.append(dire.a['href'].split('name/')[1].split('/?')[0])
    film['directors'] = directors
    film['actors'] = actors

    tags_list = soup.select('.see-more.inline.canwrap')
    pattern_plot = '\s[\s|]'

    # write plot key words
    if tags_list:
        plot_key = re.split(pattern_plot, tags_list[0].get_text().strip())
        writefile_plot(plot_key, film)
    else:
        print(movieurl + ": no plot key words\n")

    # write genres
    if len(tags_list) >= 2:
        genres = re.split(pattern_plot, tags_list[1].get_text().strip())
        writefile_plot(genres, film)
    else:
        print(movieurl + ": no genres\n")

    # write detail
    if soup.select('.txt-block'):
        writefile_detail(soup.select('.txt-block'), film)
    else:
        print(movieurl + ": no detail\n")

    if soup.select('.ratingValue'):
        film['score'] = float(soup.select('.ratingValue')[0].strong.get_text().strip())
        film['ratingNum'] = int(soup.find_all(attrs={'itemprop': 'ratingCount'})[0].get_text().replace(',', ''))

    # write poster and watchURL
    if soup.select('.poster'):
        film['posterURL'] = soup.select('.poster')[0].img.get('src')
    if soup.select('.slate'):
        film['filmWatchURL'] = 'http://www.imdb.com' + soup.select('.slate')[0].a['href']

    # write cast
    cast = ''
    if soup.select('.cast_list'):
        table = soup.select('.cast_list')[0]
        for item in table.find_all('tr'):
            if not item.has_attr('class'):
                continue
            cast += item.find_all(attrs={'itemprop': 'name'})[0].string + ':'
            i = 0
            for character in item.select('.character')[0].find_all('a'):
                if i == 0:
                    cast += character.string
                    i += 1
                else:
                    cast += ',' + character.string
            cast += '/'
        film['cast'] = cast

    # write storyline
    if soup.find_all(attrs={'itemprop': 'description'}):
        film['storyline'] = soup.find_all(attrs={'itemprop': 'description'})[0].get_text().strip()

    # write awards
    if soup.find_all(attrs={'itemprop': 'awards'}):
        tem_str = ''
        for a_str in soup.find_all(attrs={'itemprop': 'awards'})[0].get_text().strip().split('\n'):
            tem_str += a_str.strip() + ' '
        film['award'] = tem_str
    # write worldgross
    # film['worldwideGross'] = get_worldgross(movieurl)

    if film_type == 'Oscar':
        film['filmType'] = 'Normal'
        film['Oscar'] = 1
    else:
        film['filmType'] = film_type
    # write douban_score
    film['douban_score'] = douban_score.get_score(film_id)
    # save film
    if need_update:
        save.save_film_update(film)
    else:
        save.save_film(film)

    # scrape producer
    imdbref = 'http://www.imdb.com/'
    for director in soup.find_all(attrs={'itemprop': 'director'}):
        director_ref = imdbref + director.a.get('href')
        producerscrawler.producerscrawler(director_ref, 'Director')
    for actor in soup.find_all(attrs={'itemprop': 'actors'}):
        actor_ref = imdbref + actor.a.get('href')
        producerscrawler.producerscrawler(actor_ref, 'Actor')
    # scrape review
    reviewscrawler.reviewscrawler(film_id)


def writefile_plot(s, film):
    plotlist = list()
    is_script = False
    is_genre = False
    for item in s:
        if item:
            inpattern = '\w'
            if re.match(inpattern, item):
                if item.startswith('Plot Keyword'):
                    is_script = True
                if item.startswith('Genre'):
                    is_genre = True
                if not (item.startswith('Plot Keyword') or item.startswith('Genre')):
                    plotlist.append(item.replace('|', '').strip())
    if is_script:
        film['scriptKeyWords'] = plotlist
    if is_genre:
        film['tags'] = plotlist


def get_dollor(s):
    res = ''
    found_dollor = False
    for letter in s:
        if not found_dollor:
            if letter == '$':
                found_dollor = True
            else:
                continue
        else:
            if letter == ',':
                continue
            elif ord('0') <= ord(letter) <= ord('9'):
                res += letter
            else:
                break
    if res:
        return int(res)
    else:
        return 0


def writefile_detail(s, film):
    for item in s:
        if item.h4:
            if item.h4.string:
                striped_text = item.get_text().strip()
                if item.h4.string.startswith("Country:"):
                    if item.a:
                        film['country'] = item.a.string
                elif item.h4.string.startswith("Language"):
                    if item.a:
                        film['language'] = item.a.string
                elif item.h4.string.startswith("Release Date"):
                    # print item.get_text().strip().split('\n')[0].split('Release Date: ')[1].strip()
                    film['onTime'] = convert_time.local_date(
                        striped_text.split('\n')[0].split('Release Date: ')[1].strip())
                elif item.h4.string.startswith('Taglines'):
                    film['tagLine'] = striped_text.split('\n')[1]
                elif item.h4.string.startswith('Runtime'):
                    film['runtime'] = convert_time.filter_time(get_num(striped_text.split('Runtime:')[1]))
                elif item.h4.string.startswith('Sound Mix'):
                    film['soundmix'] = striped_text.split('Sound Mix:')[1].replace('\n', '')
                elif item.h4.string.startswith('Budget'):
                    film['budget'] = get_dollor(striped_text.split('Budget:')[1].replace('\n', ''))
                elif item.h4.string.startswith('Gross USA:'):
                    film['gross'] = get_dollor(striped_text.split('Gross USA:')[1].replace('\n', ''))
                elif item.h4.string.startswith('Cumulative Worldwide Gross:'):
                    # write worldgross
                    film['worldwideGross'] = get_dollor(
                        striped_text.split('Cumulative Worldwide Gross:')[1].replace('\n', ''))


# def get_worldgross(movieurl):
#     if movieurl.find('?') >= 0:
#         movieurl = movieurl.split('?')[0]
#     soup = page_read.page_read_nolog(movieurl + 'business?ref_=tt_dt_bus/')
#     film = dict()
#     # write detail
#     if soup:
#         if soup.select('#tn15content'):
#             my = soup.select('#tn15content')[0]
#             if len(my.get_text().split('Gross')) > 1:
#                 target = my.get_text().split('Gross')[1]
#                 for item in target.split(')'):
#                     if item.find('orldwide') >= 0:
#                         return get_num(item)
#     return None
if __name__ == '__main__':
    print(get_dollor(' $16,866,403, 16 November 2017'))

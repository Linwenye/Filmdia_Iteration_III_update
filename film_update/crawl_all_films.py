from film_update import moviescrawler
from crawler_util import page_read

the_url = 'http://www.imdb.com/search/title?count=100' \
          '&release_date=1915-01-01,2017-06-30&title_type=feature&page='
imdb_href = 'http://www.imdb.com'
for i in range(1, 100):
    target = the_url + str(i)
    soup = page_read.page_read_power(target)
    if soup:
        for item in soup.select('.lister-item-header'):
            movieurl = imdb_href + item.a.get('href')
            print(str(i) + ': ' + movieurl)
            the_filmid = item.a.get('href').split('title/')[1].split('/')[0]
            if the_filmid:
                moviescrawler.crawl_imdb(the_filmid, 'Normal', False)

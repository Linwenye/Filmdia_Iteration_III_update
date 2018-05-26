from db_helper import save
from crawler_util import convert_time
from crawler_util import page_read
from crawler_util.util import get_num


def review_page_crawler(film_id, myurl):
    soup = page_read.page_read_nolog(myurl)
    # soup = page_read.page_read(myurl, f_log)
    key = ''
    if soup:
        for item in soup.select('.lister-item-content'):
            review = dict()
            review['imdb_filmID'] = film_id

            if item.select_one('.ipl-ratings-bar'):
                review['score'] = float(item.select_one('.ipl-ratings-bar').get_text().strip().split('/')[0])
            else:
                review['score'] = 0
            helpfulness_str_split = item.select_one('.actions').get_text().strip().split(' ')
            review['helpfulness'] = helpfulness_str_split[0] + '/' + helpfulness_str_split[3]
            review['summary'] = item.select_one('.title').string
            review['userName'] = item.select_one('.display-name-date').select_one('.display-name-link').get_text()
            review['time'] = convert_time.local_date(
                item.select_one('.display-name-date').select_one('.review-date').get_text())

            review['userCountry'] = None

            review['text'] = item.select_one('.text').get_text().strip()
            # print(review)
            save.save_review(review)
        key = soup.select_one(".load-more-data")['data-key']
    return key


def reviewscrawler(filmid):
    # the_f_log = codecs.open('E:\GitHub\Filmdia\statistics\log/logReview.txt', 'a', 'utf-8')
    path_url = 'http://www.imdb.com/title/' + filmid + '/reviews'
    # print path_url
    # temsoup = page_read.page_read(path_url, the_f_log)
    temsoup = page_read.page_read_nolog(path_url)
    try:
        num_str = temsoup.select_one('.lister').select_one('.header').div.get_text().strip()
        reviews_num = get_num(num_str)

        # only crawl 500 reviews
        if reviews_num > 500:
            reviews_num = 500

        range_y = reviews_num // 25
        key = ''
        for i in range(range_y):
            theurl = 'http://www.imdb.com/title/' + filmid + '/reviews/_ajax?ref_=undefined&paginationKey=' + key
            key = review_page_crawler(filmid, theurl)
            # print(key)
        # review_page_crawler(filmid, theurl, the_f_log)
    except Exception as e:
        print(e.args)
        print("maybe no network")


if __name__ == '__main__':
    # reviewscrawler('tt0068646')
    reviewscrawler('tt0111161')
    # review_page_crawler('tt0111161', 'https://www.imdb.com/title/tt0111161/reviews?ref_=tt_urv')

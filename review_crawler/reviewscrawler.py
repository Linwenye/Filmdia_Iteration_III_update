from db_helper import save
from crawler_util import convert_time
from crawler_util import page_read
from crawler_util.util import get_num


def review_page_crawler(film_id, myurl):
    soup = page_read.page_read_nolog(myurl)
    # soup = page_read.page_read(myurl, f_log)
    if soup:
        contentls = soup.select('#tn15content')[0]

        for item in contentls.find_all('div'):
            review = dict()
            review['imdb_filmID'] = film_id
            if not item.attrs:

                if len(item.find_all('img')) > 1:
                    review['score'] = float(item.find_all('img')[1].get('alt').split('/')[0])

                count = None
                review_useful = False
                for temp in item.stripped_strings:
                    if temp.endswith('review useful:'):
                        review_useful = True
                        break
                if not review_useful:
                    count = 1
                for thestr in item.stripped_strings:
                    if thestr.endswith('review useful:'):
                        review['helpfulness'] = thestr.split(' ')[0] + '/' + thestr.split(' ')[3]
                        # print('Helpfulness: ' + thestr.split(' ')[0] + '/')
                        # print(thestr.split(' ')[3])
                        count = 1
                    elif thestr.startswith('***'):
                        continue
                    elif count == 1:
                        count += 1
                        review['summary'] = thestr
                        # print('Summary: ' + thestr)
                    elif count == 2:
                        count += 1
                        # # print(thestr + ' ')
                    elif count == 3:
                        review['userName'] = thestr
                        # print(thestr + ' ')
                        count += 1
                    elif count == 4:
                        # print(thestr)
                        if thestr.startswith('from'):
                            review['userCountry'] = thestr[5:]
                            count += 1
                        else:
                            review['time'] = convert_time.local_date(thestr)
                            count += 2
                    elif count == 5:
                        review['time'] = convert_time.local_date(thestr)

                pp = item.next_sibling.next_sibling
                text = ''
                for line in pp.get_text().strip().split('\n'):
                    text += line
                review['text'] = text
                save.save_review(review)
    return


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

        range_y = reviews_num / 10
        for i in range(0, range_y):
            theurl = 'http://www.imdb.com/title/' + filmid + '/reviews?start=' + str(i * 10)
            review_page_crawler(filmid, theurl)
            # review_page_crawler(filmid, theurl, the_f_log)
    except Exception as e:
        print(e.message)
        print "maybe no network"


if __name__ == '__main__':
    reviewscrawler('tt0111161')

from db_helper import save
from crawler_util import page_read


# some problem remained: the director may be an actor at the same time
# and the actor may rank behind in the movie that the actor's known for
def producerscrawler(producer_url, producer_type):
    producer = dict()
    producer['type'] = producer_type

    soup = page_read.page_read_nolog(producer_url)

    # get producer ID
    producer_id = producer_url.split('name/')[1].split('/')[0].split('?')[0]
    producer['producer_id'] = producer_id

    if soup:
        # get picture path
        if soup.select('.image'):
            if soup.select('.image')[0].img:
                picture_path = soup.select('.image')[0].img.get('src')
                producer['image'] = picture_path

        # get name
        name = soup.h1.get_text().strip()
        producer['name'] = name
        # write filmsid
        films_id = list()
        for filmiddiv in soup.select('.knownfor-title'):
            film_ref = 'http://www.imdb.com/' + filmiddiv.a.get('href')
            filmid = film_ref.split('title/')[1].split('/')[0]
            films_id.append(filmid)

        producer['films'] = films_id
        save.save_producer(producer)  # save to database


if __name__ == '__main__':
    producerscrawler('https://www.imdb.com/name/nm0001104/', 'Director')

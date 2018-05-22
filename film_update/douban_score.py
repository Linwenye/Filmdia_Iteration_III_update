import json
import logging
import socket
import traceback
import urllib2


def get_score(film_id):
    myurl = 'https://api.douban.com/v2/movie/imdb/' + film_id + '?apikey=02646d3fb69a52ff072d47bf23cef8fd'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    }

    socket.setdefaulttimeout(10)

    request = urllib2.Request(myurl, None, headers)
    html = None
    try:
        html = urllib2.urlopen(request, timeout=10)
    except Exception as e:
        logging.error(traceback.format_exc())
        print("can't open")
    try:
        html = html.read()
    except Exception as e:
        return 0

    try:
        js = json.loads(str(html))
    except:
        js = None
    try:
        return js['rating']['average']
    except:
        return 0


if __name__ == "__main__":
    print(float('123'))

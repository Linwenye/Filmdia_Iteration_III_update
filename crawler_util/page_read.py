import socket
import urllib2
import traceback
import logging
import time
from bs4 import BeautifulSoup


def inner_page_read(myurl, f_log):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    }
    socket.setdefaulttimeout(10)

    request = urllib2.Request(myurl, None, headers)
    html = None
    soup = None
    try:
        html = urllib2.urlopen(request, timeout=10)
    except Exception as e:
        logging.error(traceback.format_exc())
        print "can't open"
    try:
        html = html.read()
        soup = BeautifulSoup(html, "lxml")
    except Exception as e:
        logging.error(traceback.format_exc())
        f_log.write(myurl + ": can't open imdb\n")
        return
    return soup


def page_read(myurl, f_log):
    i = 0
    soup = inner_page_read(myurl, f_log)
    while not soup and i < 5:
        i += 1
        print myurl + 'try open again'
        soup = inner_page_read(myurl, f_log)
    return soup


def inner_page_read_nolog(myurl):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    }
    socket.setdefaulttimeout(10)

    request = urllib2.Request(myurl, None, headers)
    html = None
    soup = None
    try:
        html = urllib2.urlopen(request, timeout=10)
    except Exception as e:
        logging.error(traceback.format_exc())
        print "can't open"
    try:
        html = html.read()
        soup = BeautifulSoup(html, "lxml")
    except Exception as e:
        logging.error(traceback.format_exc())
        print (myurl + ": can't open imdb\n")
        return
    return soup


def page_read_nolog(myurl):
    i = 0
    soup = inner_page_read_nolog(myurl)
    while not soup and i < 5:
        i += 1
        print myurl + 'try open again'
        soup = inner_page_read_nolog(myurl)
    return soup


def page_read_power(myurl):
    soup = inner_page_read_nolog(myurl)
    while not soup:
        print myurl + 'try open again'
        soup = inner_page_read_nolog(myurl)
    return soup

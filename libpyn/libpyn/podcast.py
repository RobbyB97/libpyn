import logging
import requests
from bs4 import BeautifulSoup as bs

logging.basicConfig(filename='podcast.log',level=logging.DEBUG)

def get(link):

    # Get RSS feed
    try:
        if not '/rss' in link:
            link = link + '/rss'
        xml = requests.get(link).text
    except Exception:
        logging.exception('Link is not valid.')

    return xml

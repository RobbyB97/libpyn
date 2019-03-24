import os
import logging
import requests
from bs4 import BeautifulSoup as bs

logging.basicConfig(filename='podcast.log',level=logging.DEBUG)


class Podcast:


    def __init__(self, link, name='Unnamed podcast'):

        # Inner function to get data from each podcast on a channel
        def getItem(item):
            try:
                podcast = {}    # Dictionary for storing podcast info
                podcast['title'] = item.find('title').text
                podcast['date'] = item.find('pubdate').text
                podcast['mp3'] = item.find('enclosure')['url']
                podcast['image'] = item.find('itunes:image')['href']
            except Exception:
                log.exception('Could not parse item.')
            return podcast

        self.mp3list = []   # List of podcasts from channel
        self.name = name
        self.dir = os.path.dirname(os.path.realpath(__file__))

        # Get RSS feed
        try:
            if not '/rss' in link:
                link = link + '/rss'
            xml = requests.get(link).text
            xmlsoup = bs(xml, "lxml")
        except:
            logging.exception('Link is not valid.')

        # Loop through podcasts in feed and get data
        for item in xmlsoup.findAll('item'):
            self.mp3list.append(getItem(item))
        return


    def download(podcast, dir=None, foldername=None):
    # Download mp3 file(s)

        if dir:
            try:
                os.chdir(dir)
            except:
                logging.exception('Could not find directory at: %s ...' % dir)

        # Find Downloads folder, make one if it doesn't exist
        else:
            home = os.path.expanduser('~')
            try:
                os.chdir(home + '/Downloads')
            except:
                logging.warning('Could not find Downloads folder. Creating...')
                os.mkdir('%s/Downloads/' % home)
                os.chdir('%s/Downloads/' % home)

        # If folder previously created, clear its contents
        if foldername:
            try:
                os.chdir('./%s/' % foldername)
                for file in os.listdir():
                    os.remove(file)
            os.mkdir('./%s/' % foldername)
            os.chdir('./%s/' % foldername)

        return

import os
import logging
import requests
from time import sleep
from bs4 import BeautifulSoup as bs

logging.basicConfig(filename='podcast.log',level=logging.DEBUG)



class Podcast:


    def __init__(self, link):

        self.mp3list = []   # List of podcasts from channel
        self.dir = os.path.dirname(os.path.realpath(__file__))

        # Get Links
        if not '/rss' in link:
            self.rsslink = link + '/rss'
            self.htmllink = link
        if '/rss' in link:
            self.rsslink = link
            self.htmllink = link[:-4]

        # Parse links
        try:
            xml = requests.get(self.rsslink).text
            self.xmlsoup = bs(xml, "lxml")
            html = requests.get(self.htmllink).text
            self.htmlsoup = bs(html, "lxml")
        except:
            logging.exception('Link is not valid.')

        # Get RSS data
        self.name = self.xmlsoup.find('title')
        for item in self.xmlsoup.findAll('item'):
            self.mp3list.append(self.getRSSItem(item))
        return


    # Get data from each podcast on an RSS channel
    def getRSSItem(self, item):
        try:
            podcast = {}    # Dictionary for storing podcast info
            podcast['title'] = item.find('title').text
            podcast['date'] = item.find('pubdate').text
            podcast['mp3'] = item.find('enclosure')['url']
            podcast['image'] = item.find('itunes:image')['href']
        except Exception:
            log.exception('Could not parse item.')
        return podcast


    # Download mp3 file(s)
    def download(self, dir=None, foldername=None):

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

        # Set folder name to title of podcast if none was given
        if not foldername:
            foldername = self.name.replace(' ', '_')

        # Get into podcast directory, keep note of previously saved files
        try:
            os.chdir('./%s/' % foldername)
            filelist = []   # List of downloaded mp3 files
            for podcast in os.listdir():
                file = podcast.replace(' ', '_')[:-4]
                filelist.append(file)

        # Create foldername directory if it doesn't exist
        except:
            logging.warning('/%s/ doesn\'t exist. Creating...')
            os.mkdir('./%s/' % foldername)
            os.chdir('./%s/' % foldername)

        # Download files
        for podcast in self.mp3list:
            exists = False      # Flag for if file already exists

            # Ensure podcasts aren't redownloaded if directory not empty
            for file in filelist:
                if podcast['title'].replace(' ', '_') == file:
                    exists = True
                    logging.warning('%s already exists. Skipping...' % file)
                if exists == True:
                    break

            # Download file
            if exists  == False:
                sleep(1)    # Ensure no IP ban
                filename = podcast['title'].replace(' ', '_') + '.mp3'
                file = requests.get(podcast['mp3'])
                logging.debug('Downloading %s...' % podcast['title'])
                with open(filename, 'wb') as f:
                    f.write(file.content)
        return

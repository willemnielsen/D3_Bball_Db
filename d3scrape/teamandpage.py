from bs4 import BeautifulSoup as bs
import os
from d3scrape.scrapetools import ScrapeTools
from requests.exceptions import RequestException

class Team:
    def __init__(self, name, players=None, url=None, stats_page=None, ind_page=None):
        self.name = name
        self.players = players
        self.url = url
        if self.url:
            base_index = self.url.find('com')
            if base_index != -1:
                self.baseurl = url[:base_index + 3]
            else:
                base_index = self.url.find('edu')
                self.baseurl = url[:base_index + 3]
        self.stats_page = stats_page
        self.ind_page = ind_page

    def init_stats_page(self, stats_url):
        path = os.path.expanduser(f"~/stats_html/{self.name}")
        self.stats_page = Page(stats_url, path=path)
        self.stats_page.path = path

    def init_ind_page(self, ind_url):
        path = os.path.expanduser(f"~/ind_html/{self.name}")
        self.ind_page = Page(ind_url, path=path)
        self.stats_page.path = path


class Page:
    def __init__(self, url, team_name, path=None, site_type=None, has_doc=False, doc=None):
        self.url = url
        self.team_name = team_name
        self.has_doc = has_doc
        self.doc = doc

        if path:
            self.path = path
        else:
            if site_type:
                self.path = os.path.expanduser(f"~/{site_type}_html/") + url.replace('/', '-') + '.html'
            else:
                self.path = os.path.expanduser("~/off_site_html/") + url.replace('/', '-') + '.html'

    def download(self):
        response = ScrapeTools.get_response(self.url)
        with open(self.path, 'w+') as file:
            file.write(response.text)
        self.has_doc = True

    def set_doc(self):
        if self.has_doc:
            with open(self.path, 'r') as file:
                doc = file.read()
            return doc
        try:
            response = ScrapeTools.get_response(self.url)
        except (RequestException, ScrapeTools.Non200Status):
            return
        else:
            self.doc = response.text

    def get_soup(self):
        try:
            with open(self.path) as file:
                doc = file.read()
        except FileNotFoundError:
            return
        else:
            return bs(doc, 'html.parser')


class Player:
    def __init__(self, id, team, bio=None, stats=None, name=None):
        self.id, self.team = id, team
        self.stats = stats
        self.bio = bio
        self.name = name
        self.stats = stats













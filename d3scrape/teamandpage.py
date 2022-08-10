from bs4 import BeautifulSoup as bs
import os
from d3scrape.scrapetools import ScrapeTools


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

    def update_stats_page(self, stats_url):
        path = os.path.expanduser(f"~/stats_html/{self.name}")
        self.stats_page = Page(stats_url, path=path)
        self.stats_page.path = path

    def init_ind_page(self, ind_url):
        path = os.path.expanduser(f"~/ind_html/{self.name}")
        self.ind_page = Page(ind_url, path=path)
        self.stats_page.path = path


class Page:
    def __init__(self, url, path=None, site_type=None, has_doc=False):
        self.url = url
        self.has_doc = has_doc
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

    def get_soup(self):
        try:
            with open(self.path) as file:
                doc = file.read()
        except FileNotFoundError:
            return
        else:
            return bs(doc, 'html.parser')


class Player:
    def __init__(self, team, name, stats=None):
        self.team = team
        self.name = name
        self.stats = stats













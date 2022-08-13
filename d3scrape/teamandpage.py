from bs4 import BeautifulSoup as bs
import os
from d3scrape.scrapetools import ScrapeTools
from requests.exceptions import RequestException
from uuid import uuid4


class Team:
    def __init__(self, name, players=None, url=None, stats_page=None, ind_page=None):
        self.id = uuid4().time_low
        self.name = name
        self.players = players
        self._url = url
        if url:
            base_index = url.find('com')
            if base_index != -1:
                self._baseurl = url[:base_index + 3]
            else:
                base_index = url.find('edu')
                self._baseurl = url[:base_index + 3]
        self._stats_page = stats_page
        self._ind_page = ind_page

    def __setattr__(self, key, value):
        if key == 'stats_page':
            path = os.path.expanduser(f"~/stats_html/{self.name}")
            value = Page(value, self.name, path=path)
        if key == 'ind_page':
            path = os.path.expanduser(f"~/ind_html/{self.name}")
            value = Page(value, self.name, path=path)
        return super().__setattr__(key, value)

    @property
    def stats_page(self):
        return self._stats_page

    @property
    def ind_page(self):
        return self._ind_page

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url
        base_index = url.find('com')
        if base_index != -1:
            self.baseurl = url[:base_index + 3]
        else:
            base_index = url.find('edu')
            self.baseurl = url[:base_index + 3]


class Page:
    def __init__(self, url, team, path=None, site_type=None, has_doc=False, doc=None, tables=None, lineup=False):
        self._url = url
        self.team = team
        self.has_doc = has_doc
        self.doc = doc
        self.tables = [] if not tables else tables
        self._lineup = lineup
        if path:
            self.path = path
        else:
            if site_type:
                self.path = os.path.expanduser(f"~/{site_type}_html/") + url.replace('/', '-') + '.html'
            else:
                self.path = os.path.expanduser("~/off_site_html/") + url.replace('/', '-') + '.html'

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url
        self._lineup = True if 'lineup' in url else False

    def download(self):
        try:
            response = ScrapeTools.get_response(self.url)
        except (ScrapeTools.Non200Status, RequestException):
            return
        with open(self.path, 'w+') as file:
            file.write(response.text)
        self.has_doc = True

    def get_soup(self, from_where='sites_and_files'):
        if from_where == 'files' or from_where == 'sites_and_files':
            if self.team.stats_page.has_doc:
                return self.get_old_soup()
            if from_where == 'sites_and_files':
                return self.get_new_soup()
            return
        if from_where == 'sites':
            return self.get_new_soup()
        return

    def get_old_soup(self):
        try:
            with open(self.path) as file:
                doc = file.read()
        except FileNotFoundError:
            return
        else:
            return bs(doc, 'html.parser')

    def get_new_soup(self):
        return ScrapeTools.get_new_soup(self.url)


class Player:
    def __init__(self, team, bio=None, stats=None, name=None):
        self.id = uuid4().time_low
        self.team = team
        self.stats = stats
        self.bio = bio
        self.name = name













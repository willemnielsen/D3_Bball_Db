import collections
import csv
from bs4 import BeautifulSoup as bs
import pickle
import os
import pandas as pd


class DataBase:
    def __init__(self, teams):
        self.teams = teams

    def set_has_doc_home(self):
        for team in self.teams:
            if team.url:
                try:
                    f = open(team.home_page.path, 'r')
                except FileNotFoundError:
                    pass
                else:
                    team.home_page.has_doc = True



    def set_has_doc_ind(self):
        for team in self.teams:
            if team.url:
                if team.indiv_page:
                    try:
                        f = open(team.indiv_page.path, 'r')
                    except FileNotFoundError:
                        pass
                    else:
                        team.indiv_page.has_doc = True



    def save(self, path):
        with open(path, 'wb') as file:
            pickle.dump(self, file)

    def save_stats_urls(self):
        stats_urls = {}
        for team in self.teams:
            print('new team: ' + team.name)
            if team.has_statistics:
                with open(team.home_page.path, 'r') as file:
                    doc = file.read()
                soup = bs(doc, 'html.parser')
                a = soup.find('a', string='Statistics')
                rel_url = a.get('href')
                stats_url = team.baseurl + rel_url
                stats_urls[team.name] = stats_url
        with open('stats_urls.pkl') as file:
            pickle.dump(stats_urls, file)

    def set_stats_pages(self):
        stat_urls = collections.deque()
        with open('../misc_data/stats_urls.csv', 'r') as f:
            r = csv.reader(f)
            for row in r:
                for url in row:
                    stat_urls.append(url)
        for team in self.teams:
            if team.has_statistics:
                team.set_stats_page(stat_urls.popleft())

    def find_index_stats_url(self, stats_url):
        for idx, team in enumerate(self.teams):
            if team.stats_page:
                if team.stats_page.url == stats_url:
                    return idx

    def update_stats_pages(self, d3):
        for team in self.teams:
            if team.stats_page:
                team.stats_page.update(d3)

    def save_ind_urls(self):
        ind_urls = {}
        for team in self.teams:
            print('on to ' + team.name)
            if team.stats_page:
                if team.stats_page.has_doc:
                    with open(team.stats_page.path, 'r') as file:
                        doc = file.read()
                    soup = bs(doc, 'html.parser')
                    a = soup.find('a', string='Individual')
                    if a:
                        rel_url = a.get('href')
                        ind_url = team.stats_page.url + rel_url
                        ind_urls[team.name] = ind_url
                        team.has_individual = True
        with open('ind_urls.pkl') as file:
            pickle.dump(ind_urls, file)

    def set_ind_pages(self):
        ind_urls = collections.deque()
        with open('../misc_data/ind_urls.csv', 'r') as f:
            r = csv.reader(f)
            for row in r:
                for url in row:
                    ind_urls.append(url)
        for team in self.teams:
            if team.stats_page:
                if team.stats_page.has_doc:
                    if team.has_individual:
                        team.set_ind_page(ind_urls.popleft())

    def update_ind_pages(self, d3):
        for team in self.teams:
            if team.stats_page:
                if team.stats_page.has_doc:
                    if team.has_individual:
                        team.indiv_page.update(d3)

    def only_ind(self):
        only_ind = []
        for team in self.teams:
            if team.indiv_page:
                if team.indiv_page.has_doc:
                    only_ind.append(team)
        return only_ind



def update_teams():
    d3 = D3()
    d3.save_teams_local()
    db = DataBase(d3.get_teams())
    db.save()


def get_db(db=''):
    db_path = os.path.expanduser(f"~/databases/{db}")
    with open(db_path, 'rb') as my_file:
        db = pickle.load(my_file)
    return db



if __name__ == '__main__':
    db = get_db('db_ind')
    db.tables_to_pandas()
    with open('../mp/pandas_tables.pkl', 'rb') as file:
        tabs = pickle.load(file)
    pass

import csv
import requests
from bs4 import BeautifulSoup as bs
import pickle
import os
from d3scrape.teamandpage import Team, Page
from d3scrape.scrapetools import ScrapeTools


class D3Hoops(ScrapeTools):
    def scrape_names_and_sites(self):
        names_and_sites = {}
        region_urls = self.get_regions('https://d3hoops.com')
        for url in region_urls:
            links = self.get_links(url)
            for name, site in zip(links, self.get_off_sites(links)):
                names_and_sites[name] = site
        ScrapeTools.dump(names_and_sites, '../mp/names_and_sites.pkl')
        return names_and_sites

    @staticmethod
    def load_names_and_sites():
        names_and_sites = ScrapeTools.load('../mp/names_and_sites.pkl')
        return names_and_sites

    def get_regions(self, d3hoops_home_url):
        soup = self.get_new_soup(d3hoops_home_url)
        links = ['https://d3hoops.com' + soup.find('a', string=f"Region {i}").get('href') for i in range(1, 11)]
        return links

    def get_off_sites(self, links):
        d3hoops_sites = ['https://d3hoops.com' + link.get('href') for link in links]
        for i, url in enumerate(d3hoops_sites):
            d3hoops_sites[i] = url.replace('info/../', '')
        for url in d3hoops_sites:
            yield self.find_official_link(url)

    def get_links(self, region_url):
        soup = self.get_new_soup(region_url)
        table_data = [row.find('td') for row in soup.find_all('tr')]
        links = [data.a for data in table_data if data.a]
        return links

    def find_official_link(self, url):
        soup = self.get_new_soup(url)
        link = soup.find('a', string='Men')
        url = link.get('href')
        return url

    def save_to_dict(self):
        names = []
        off_sites = []
        di = {}
        with open('../misc_data/names.csv') as my_file:
            for row in csv.reader(my_file):
                for item in row:
                    names.append(item)
        with open('../misc_data/off_sites.csv') as my_file:
            for row in csv.reader(my_file):
                for item in row:
                    off_sites.append(item)
        for name, site in zip(names, off_sites):
            di[name] = site
        self.dump(di, '../mp/names_and_sites.pkl')




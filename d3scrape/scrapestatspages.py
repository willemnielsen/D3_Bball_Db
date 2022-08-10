import csv
from d3scrape.scrapetools import ScrapeTools as st, Non200Status
from requests import RequestException


class ScrapeStatsPages:
    def __init__(self, teams):
        self.teams = teams

    def update_stats_urls(self, path='mp/stats_link_dict_new.pkl'):
        stats_link_dict = {}
        non_stats_dict = {}
        invalid_dict = {}
        for team in self.teams:
            try:
                soup = st.get_new_soup(team.url)
            except (Non200Status, RequestException) as error:
                invalid_dict[team.name] = error
            else:
                stats_link = soup.find('a', string='Statistics')
                if stats_link:
                    rel_url = stats_link.get('href')
                    stats_url = team.baseurl + rel_url
                    stats_link_dict[team.name] = stats_url
                else:
                    non_stats_dict[team.name] = team.url
        st.dump(stats_link_dict, path)
        st.dump(non_stats_dict, '../mp/non_stats_dict.pkl')
        st.dump(invalid_dict, '../mp/invalid_dict.pkl')

    def update_stats_pages(self, dict_path='mp/stats_link_dict_new.pkl', new_urls=False, download=False):
        if new_urls:
            self.update_stats_urls(path=dict_path)
        sld = st.load(dict_path)
        for team in self.teams:
            for key, val in sld.items():
                if team.name == key:
                    team.update_stats_page(val)
                    if download:
                        team.stats_page.download()


import csv
from d3scrape.scrapetools import ScrapeTools as st
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
            except (st.Non200Status, RequestException) as error:
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

    @staticmethod
    def get_stat_url_from_extra_link():
        stats_link_dict = st.load('mp/stats_link_dict.pkl')
        no_ind_dict = st.load('mp/no_ind_dict.pkl')
        teams = st.load('mp/nts_up.pkl')
        for team in teams:
            if team.name in no_ind_dict:
                soup = team.stats_page.get_soup()
                if soup:
                    print('searching: ' + team.name)
                    buttons = soup.find_all('a')
                    for button in buttons:
                        name = button.get_text()
                        url = button.get('href')
                        if not name or not url:
                            continue
                        try:
                            if 'Statistics' in name and '2021-22' in url or '2021-22' in url and 'stats' in url:
                                print('found link for ' + team.name + ':' + team.baseurl + url)
                                stats_link_dict[team.name] = team.baseurl + url
                                team.init_stats_page(team.baseurl + url)
                        except AttributeError:
                            continue
        st.dump(teams, 'mp/teams_with_extra_stats_link')
        st.dump(stats_link_dict, 'mp/stats_link_dict.pkl')




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


from d3scrape.scrapetools import ScrapeTools as st
from d3scrape.scrapestatspages import ScrapeStatsPages
from d3scrape.scrapeindpages import ScrapeIndPages
from d3scrape.d3hoops import D3Hoops
from d3scrape.teamandpage import Team
from bs4 import BeautifulSoup as bs



class Scrape(st):
    @staticmethod
    def update_names_and_sites(path):
        dh = D3Hoops()
        names_and_sites = dh.scrape_names_and_sites()
        teams = []
        for key, val in names_and_sites.items():
            teams.append(Team(key, val))
        st.dump(teams, path)
        return teams

    @staticmethod
    def get_teams(teams_path, update_names_and_sites=False, new_teams=False, update_stats_pages=None, update_ind_pages=None):
        dh = D3Hoops()
        if update_names_and_sites:
            names_and_sites = dh.scrape_names_and_sites()
        else:
            names_and_sites = dh.load_names_and_sites()
        if new_teams:
            teams = []
            for key, val in names_and_sites.items():
                teams.append(Team(key, val))
            st.dump(teams, teams_path)
        teams = st.load(teams_path)
        if update_stats_pages:
            Scrape.update_stats_pages(teams_path, **update_stats_pages)
        if update_ind_pages:
            Scrape.update_ind_pages('mp/' **update_ind_pages)
        return teams

    @staticmethod
    def update_stats_pages(teams_path, new_urls=False, download=False):
        teams = st.load(teams_path)
        ssp = ScrapeStatsPages(teams)
        ssp.update_stats_pages(download=download, new_urls=new_urls)

    @staticmethod
    def update_ind_pages(teams_path, download=False, new_urls=False):
        teams = st.load(teams_path)
        sip = ScrapeIndPages(teams)
        sip.update_ind_pages(download=download, new_urls=new_urls)



    def tables_to_pandas(self):
        pandas_tables = {}
        with open('../mp/tables.pkl', 'rb') as file:
            tables = pickle.load(file)
        for key, value in tables.items():
            dfs = pd.read_html(value)
            pandas_tables[key] = dfs[0]
        with open('../mp/pandas_tables.pkl', 'wb') as file:
            pickle.dump(pandas_tables, file)

if __name__ == '__main__':
    my_teams = st.load('../mp/teams.pkl')
    my_ssp = ScrapeStatsPages(my_teams)
    my_ssp.convert_stats_csv_to_dict()














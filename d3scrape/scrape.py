from d3scrape.scrapetools import ScrapeTools as st
from d3scrape.scrapestatspages import ScrapeStatsPages
from d3scrape.scrapeindpages import ScrapeIndPages
from d3scrape.d3hoops import D3Hoops
from d3scrape.teamandpage import Team, Page, Player
from d3scrape.scrapeplayers import ScrapePlayers
from bs4 import BeautifulSoup as bs
import pickle
from uuid import uuid4

class Scrape(st):
    def __init__(self, teams):
        self.teams = teams

    base = '/Users/erichegonzales/PycharmProjects/playerscrape/mp/'
    @staticmethod
    def update_names_and_sites(path=None):
        dh = D3Hoops()
        names_and_sites = dh.scrape_names_and_sites()
        teams = []
        for key, val in names_and_sites.items():
            teams.append(Team(key, val))
        if path:
            st.dump(teams, path)
        return teams


    @staticmethod
    def get_new_teams():
        old_teams = st.load(Scrape.base + 'teams_with_players.pkl')
        new_teams = []
        for team in old_teams:
            try:
                new_teams.append(Team(team.name, players=team.players, url=team.url))
            except AttributeError:
                new_teams.append(Team(team.name, url=team.url))
        for nt, ot in zip(new_teams, old_teams):
            try:
                nt.stats_page = Page(ot.stats_page.url, nt.name, path=ot.stats_page.path, has_doc=ot.stats_page.has_doc)
            except AttributeError:
                continue
            try:
                nt.ind_page = Page(ot.indiv_page.url, nt.name, path=ot.indiv_page.path, has_doc=ot.indiv_page.has_doc)
                nt.ind_page.set_doc()
            except AttributeError:
                continue
        st.dump(new_teams, Scrape.base + 'teams_with_docstring.pkl')

    @staticmethod
    def clean_new_teams():
        teams = st.load(Scrape.base + 'teams_with_docstring.pkl')
        for team in teams:
            try:
                team.ind_page.doc = None
            except AttributeError:
                continue
        st.dump(teams, Scrape.base + 'updated_teams.pkl')

    @staticmethod
    def get_new_players():
        teams = st.load(Scrape.base + 'updated_teams.pkl')
        for team in teams:
            pls = team.players
            if pls:
                npls = []
                for p in pls:
                    npls.append(Player(uuid4().time_low, p.team, stats=p.stats, name=p.name))
                team.players = npls
        st.dump(teams, Scrape.base + 'updt_plys.pkl')

    @staticmethod
    def new_teams():
        teams = st.load(Scrape.base + 'updated_teams_with_players.pkl')
        nts = []
        for team in teams:
            nt = Team(team.name, players=team.players, url=team.url, stats_page=team.stats_page, ind_page=team.ind_page)
            nts.append(nt)
        st.dump(nts, Scrape.base + 'nts.pkl')







    @staticmethod
    def set_has_doc_ind():
        teams = st.load(Scrape.base + 'updated_teams.pkl')
        for team in teams:
            if team.url:
                if team.ind_page:
                    try:
                        f = open(team.ind_page.path, 'r')
                    except FileNotFoundError:
                        pass
                    else:
                        team.ind_page.has_doc = True
        st.dump(teams, Scrape.base + 'updated_teams.pkl')







    @staticmethod
    def get_teams(rescrape=False):
        ind_page_dict = {}
        Scrape.get_teams_special(Scrape.base + 'raw_teams')

    @staticmethod
    def get_teams_special(teams_path, update_names_and_sites=False, new_teams=False, update_stats_pages=None, update_ind_pages=None):
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

    def scrape_ind_pages(self, download=False, from_where='both'):
        return ScrapeIndPages.scrape(self.teams, download=download, from_where=from_where)

    def scrape_players(self):
        ScrapePlayers.scrape(self.teams)





    def tables_to_pandas(self):
        pandas_tables = {}
        with open('../mp/tables.pkl', 'rb') as file:
            tables = pickle.load(file)
        for key, value in tables.items():
            dfs = pd.read_html(value)
            pandas_tables[key] = dfs[0]
        with open('../mp/pandas_tables.pkl', 'wb') as file:
            pickle.dump(pandas_tables, file)

    @staticmethod
    def download_all(team_path):
        teams = st.load(team_path)
        ssp = ScrapeStatsPages(teams)
        ssp.download_all()





if __name__ == '__main__':
    new_teams = st.load('mp/teams_812.pkl')
    # old_teams = st.load('mp/nts_down.pkl')
    # ssp = ScrapeStatsPages(old_teams)
    # teams_with_has_doc = ssp.download_new(new_teams)
    # teams_with_has_doc = st.load('mp/extra_with_has_doc')
    # ScrapeIndPages.update_new_stats(old_teams, new_teams)
    # for team in new_teams:
    #     if team.ind_page:
    #         print(team.ind_page.path)
    sip = ScrapeIndPages(st.load('mp/teams_812.pkl'))
    sip.update_ind_urls(download=True)
    # sip.update_new(teams_with_has_doc, download=True)
    # ScrapeStatsPages.get_stat_url_from_extra_link()
    # no_ind = st.load('mp/new_no_ind_dict.pkl')

    # no_ind_teams = []
    # count = 0
    # for team in teams:
    #     if team.stats_page:
    #         if team.stats_page.has_doc:
    #             if team.ind_page:
    #                 if team.ind_page.has_doc:
    #                     count += 1
    # print(count)




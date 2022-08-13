from d3scrape.scrapetools import ScrapeTools as st
from bs4 import BeautifulSoup as bs
from d3scrape.teamandpage import Team, Page
from requests.exceptions import RequestException

base = '/Users/erichegonzales/PycharmProjects/playerscrape/mp/'

class ScrapeIndPages:
    def __init__(self, teams):
        self.teams = teams

    @staticmethod
    def scrape(teams, download=False, from_where='both'):
        failed = []
        for team in teams:
            if team.stats_page:
                ind_url = ScrapeIndPages.get_url(team, from_where)
                if ind_url:
                    team.set_ind_page(ind_url)
                    if download:
                        team.ind_page.download()
                else:
                    failed.append(team)
        return teams, failed

    def update_page(self, team, ind_path, download=False, new_urls=False):
        if new_urls:
            ScrapeIndPages.update_ind_url(team, ind_path, download=download)
        else:
            ind_urls = st.load(ind_path)
            url = ind_urls[team.name]
            team.update_stats_page(url)
            if download:
                team.stats_page.download()

    @staticmethod
    def update_ind_url(team, ind_path, download=False):
        ind_urls = st.load(ind_path)
        no_ind_teams = st.load('mp/no_ind_dict.pkl')
        no_doc_teams = st.load('mp/no_doc_teams.pkl')
        if team.stats_page:
            if team.stats_page.has_doc:
                soup = team.stats_page.get_soup()
                ind_button = soup.find('a', string='Individual')
                if ind_button:
                    rel_url = ind_button.get('href')
                    ind_url = team.stats_page.url + rel_url
                    ind_urls[team.name] = ind_url
                    team.update_stats_page(ind_url)
                    if download:
                        team.ind_page.download()
                else:
                    no_ind_teams[team.name] = team.stats_page.url
            else:
                no_doc_teams[team.name] = team.stats_page.url
        st.dump(ind_urls, ind_path)
        st.dump(no_ind_teams, 'mp/no_ind_dict.pkl')
        st.dump(no_doc_teams, 'mp/no_doc_teams.pkl')

    def update_ind_urls(self, download=False):
        ind_urls = {}
        no_ind_teams = {}
        for team in self.teams:
            if team.ind_page:
                ind_url = ScrapeIndPages.get_url(team)
                if ind_url:
                    ind_urls[team.name] = ind_url
                    team.set_ind_page(ind_url)
                    if download:
                        team.ind_page.download()
                else:
                    no_ind_teams[team.name] = team.stats_page.url
        st.dump(ind_urls, 'mp/new_ind_urls.pkl')
        st.dump(no_ind_teams, 'mp/new_no_ind_dict.pkl')
        st.dump(self.teams, 'mp/teams_812_f.pkl')


    @staticmethod
    def get_url(team, from_where='sites_and_files'):
        soup = team.stats_page.get_soup(team, from_where=from_where)
        if soup:
            return ScrapeIndPages.get_href(soup, team)



    @staticmethod
    def get_href(soup, team):
        button = soup.find('a', string='Individual')
        if button:
            return team.stats_page.url + button.get('href')
        button = soup.find('a', string='Lineup')
        if button:
            return team.baseurl + button.get('href')



    def update_new(self, teams, download=False):
        ind_urls = {}
        no_ind_teams = {}
        for old, new in zip(self.teams, teams):
            if old.stats_page and new.stats_page:
                if old.stats_page.url != new.stats_page.url:
                    ind_url = ScrapeIndPages.get_url(new)
                    if ind_url:
                        ind_urls[new.name] = ind_url
                        new.set_ind_page(ind_url)
                        if download:
                            new.ind_page.download()
                        else:
                            no_ind_teams[new.name] = new.stats_page.url
        st.dump(ind_urls, 'mp/new_ind_urls.pkl')
        st.dump(no_ind_teams, 'mp/new_no_ind_dict.pkl')
        st.dump(teams, 'mp/teams_812.pkl')

    @staticmethod
    def update_new_stats(old_teams, new_teams):
        for old, new in zip(old_teams, new_teams):
            if old.stats_page and new.stats_page:
                if old.stats_page.path != new.stats_page.path:
                    new.stats_page.path = old.stats_page.path
                    new.stats_page.download()
        st.dump(new_teams, 'mp/teams_812.pkl')

    def download_all(self):
        for team in self.teams:
            if team.ind_page:
                if not team.ind_page.has_doc:
                    try:
                        team.ind_page.download()
                    except (RequestException, st.Non200Status):
                        continue
        return self.teams

    def update_ind_pages(self, download=False, new_urls=False):
        url_path = 'ind_urls.pkl'
        team_path = 'nts_up.pkl'
        if new_urls:
            self.update_ind_urls(download=download)
        else:
            ind_urls = st.load(url_path)
            for team in self.teams:
                for key, val in ind_urls.items():
                    if team.name == key:
                        team.update_stats_page(val)
                        if download:
                            team.ind_page.download()
        st.dump(self.teams, team_path)

    @staticmethod
    def download_lineup_teams():
        lineup_urls = st.load(base + 'lineup_urls.pkl')
        teams = st.load(base + 'updated_teams.pkl')
        for team in teams:
            for key, val in lineup_urls.items():
                if team.name == key:
                    team.ind_page.download()





    @staticmethod
    def load_tables(teams):
        lineup_urls = st.load('../mp/lineup_urls.pkl')
        for team in teams:
            for key, val in lineup_urls.items():
                if team.name == key:
                    team.set_ind_page(val)
                    team.has_individual = True
        st.dump(teams, '../mp/teams.pkl')

    @staticmethod
    def teams_with_indpages():
        teams = st.load(base + 'updated_teams_with_players.pkl')
        for team in teams:
            if not team.stats_page:
                print(team.url)

    @staticmethod
    def no_ind_pages():
        teams = st.load(base + 'updated_teams_with_players.pkl')
        how_many = []
        for team in teams:
            if team.stats_page:
                if not team.ind_page:
                    how_many.append(team.name)
        print(f"{len(how_many)} don't have individual pages")
    @staticmethod
    def xml(teams):
        xml_dict = {}
        for team in teams:
            if team.stats_page:
                if team.stats_page.has_doc:
                    if team.has_individual:
                        with open(team.stats_page.path, 'r') as file:
                            doc = file.read()
                        soup = bs(doc, 'html.parser')
                        links = soup.find_all('a')
                        for link in links:
                            if 'XML' in link.get_text() and '22' in link.get('href'):
                                ind_url = team.baseurl + link.get('href')
                                print(team.name)
                                print(link.get('href'))
                                xml_dict[team.name] = ind_url
        st.dump(xml_dict, '../mp/xml_urls.pkl')

    def automate_button_search(self, path, has_individual=True, stir=None):
        d = {}
        teams = st.load('../mp/teams.pkl')
        for team in teams:
            if team.stats_page and team.stats_page.has_doc:
                if team.has_individual == has_individual:
                    with open(team.stats_page.path, 'r') as file:
                        doc = file.read()
                    soup = bs(doc, 'html.parser')
                    val = stir(soup)
                    d[team.name] = val
        st.dump(d, path)







    @staticmethod
    def quick_method(teams):
        xml = st.load('../mp/xml_urls.pkl')
        new_xml = {}
        for team in teams:
            for key, val in xml.items():
                if key == team.name:
                    if not key == 'Vassar':
                        new_xml[team.name] = val.replace(team.baseurl, '')
        new_xml['Vassar'] = xml['Vassar']
        st.dump(new_xml, '../mp/xml_urls.pkl')
    @staticmethod
    def add_xml(teams):
        xml_dict = st.load('../mp/xml_urls.pkl')
        for team in teams:
            for key, val in xml_dict.items():
                if key == team.name:
                    team.set_ind_page(xml_dict[team.name])
                    team.has_individual = True
                print(team.name)
        st.dump(teams, '../mp/teams.pkl')
        pass

    @staticmethod
    def stats_in_name(teams):
        sin = {}
        for team in teams:
            if team.stats_page:
                if team.stats_page.has_doc:
                    if not team.has_individual:
                        with open(team.stats_page.path, 'r') as file:
                            doc = file.read()
                        soup = bs(doc, 'html.parser')
                        links = soup.find_all('a')
                        for link in links:
                            if 'Statistics' in link.get_text() and '22' in link.get('href'):
                                print(team.name)
                                print(team.baseurl + link.get('href'))
                                sin[team.name] = link.get('href')
        st.dump(sin, '../mp/sin.pkl')


if __name__ == '__main__':
    ScrapeIndPages.teams_with_indpages()



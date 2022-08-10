from d3scrape.scrapetools import ScrapeTools as st
from bs4 import BeautifulSoup as bs
from d3scrape.teamandpage import Team, Page


class ScrapeIndPages:
    def __init__(self, teams):
        self.teams = teams

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
        no_ind_teams = st.load('mp/no_ind_teams.pkl')
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
        st.dump(no_ind_teams, 'mp/no_ind_teams.pkl')
        st.dump(no_doc_teams, 'mp/no_doc_teams.pkl')


    def update_ind_urls(self, path='mp/ind_urls', download=False):
        ind_urls = {}
        no_ind_teams = {}
        no_doc_teams = {}
        for team in self.teams:
            print('on to ' + team.name)
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
        st.dump(ind_urls, path)
        st.dump(no_ind_teams, 'mp/no_ind_teams.pkl')
        st.dump(no_doc_teams, 'mp/no_doc_teams.pkl')

    def update_ind_pages(self, dict_path, download=False, new_urls=False):
        if new_urls:
            self.update_ind_urls(path=dict_path, download=download)
        else:
            ind_urls = st.load(dict_path)
            for team in self.teams:
                for key, val in ind_urls.items():
                    if team.name == key:
                        team.update_stats_page(val)
                        if download:
                            team.stats_page.download()


    @staticmethod
    def load_tables(teams):
        lineup_urls = st.load('../mp/lineup_urls.pkl')
        for team in teams:
            for key, val in lineup_urls.items():
                if team.name == key:
                    team.init_ind_page(val)
                    team.has_individual = True
        st.dump(teams, '../mp/teams.pkl')

    @staticmethod
    def update_teams(teams):
        how_many = []
        for team in teams:
            if team.has_individual:
                how_many.append(team.name)
                if team.name == 'Vassar':
                    print('Vassar')
        print(f"{len(how_many)} teams have individual pages")

    @staticmethod
    def no_ind_pages(teams):
        for team in teams:
            if team.stats_page:
                if team.stats_page.has_doc:
                    if not team.has_individual:
                        print(team.name)
                        print(team.stats_page.url)

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
                    team.init_ind_page(xml_dict[team.name])
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





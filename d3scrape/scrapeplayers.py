from d3scrape.scrapeindpages import ScrapeIndPages
from d3scrape.scrapetools import ScrapeTools as st
from bs4 import BeautifulSoup as bs
from d3scrape.teamandpage import Player

base = '/Users/erichegonzales/PycharmProjects/playerscrape/mp/'
class ScrapePlayers:
    @staticmethod
    def get_tables(path):
        teams = st.load(path)
        all_tables = {}
        for team in teams:
            if team.ind_page.has_doc:
                soup = team.ind_page.get_soup()
                team_tables = soup.find_all('table')
                if team_tables and len(team_tables) >= 2:
                    team_table = team_tables[1]
                    if team_table:
                        all_tables[team.name] = str(team_table)
                else:
                    continue
        st.dump(all_tables, 'mp/tables.pkl')

    @staticmethod
    def get_players(teams):
        tables = st.load('../mp/tables.pkl')
        for team in teams:
            try:
                table = bs(tables[team.name], 'html.parser')
            except KeyError:
                continue
            else:
                table_body = table.tbody
                rows = table_body.find_all('tr')
                players = []
                for row in rows:
                    try:
                        name = row.th.a.get_text()
                    except AttributeError:
                        name = row.th.get_text()
                    stats = {}
                    for idx, stat in enumerate(row.find_all('td')):
                        if idx == 0:
                            col = 'Number'
                        else:
                            col = stat.get('data-label')
                        if idx == len(row.find_all('td')) - 1:
                            new_val = team.url + stat.find('a').get('href')
                        else:
                            new_val = stat.get_text()
                        stats[col] = new_val
                    players.append(Player(team.name, name, stats=stats))
                team.players = players
        st.dump(teams, '../mp/teams_with_players.pkl')

    @staticmethod
    def get_tables_from_lineup():
        teams = st.load(base + 'updated_teams.pkl')
        lineup_teams = st.load(base + 'lineup_urls.pkl')
        all_tables = {}
        for team in teams:
            if team.ind_page:
                if team.ind_page.has_doc:
                    if team.name in lineup_teams:
                        soup = team.ind_page.get_soup()
                        team_tables = soup.find_all('table')
                        if team_tables and len(team_tables) >= 4:
                            team_table = team_tables[3]
                            if team_table:
                                all_tables[team.name] = str(team_table)
                        else:
                            continue
        st.dump(all_tables, base + 'lineup_tables.pkl')


    @staticmethod
    def get_players_from_lineup():
        tables = st.load(base + 'lineup_tables.pkl')
        teams = st.load(base + 'updated_teams.pkl')
        for team in teams:
            try:
                table = bs(tables[team.name], 'html.parser')
            except KeyError:
                continue
            else:
                table_body = table.tbody
                rows = table_body.find_all('tr')
                players = []
                for row in rows:
                    stats = {}
                    for idx, stat in enumerate(row.find_all('td')):
                        if idx == 0:
                            col = 'Number'
                        elif idx == 1:
                            try:
                                name = stat.a.get_text().strip().replace(' ', '').replace('\n', ' ')
                                bio = team.baseurl + stat.a.get('href')
                                continue
                            except AttributeError:
                                continue
                        else:
                            col = stat.get_text()
                        new_val = stat.get_text()
                        stats[col] = new_val
                    players.append(Player(team.name, name, bio=bio, stats=stats))
                team.players = players
        st.dump(teams, base + 'updated_teams_with_players.pkl')













    # @staticmethod
    # def tables_to_pandas(self):
    #     pandas_tables = {}
    #     with open('../mp/tables.pkl', 'rb') as file:
    #         tables = pickle.load(file)
    #     for key, value in tables.items():
    #         dfs = pd.read_html(value)
    #         pandas_tables[key] = dfs[0]
    #     with open('../mp/pandas_tables.pkl', 'wb') as file:
    #         pickle.dump(pandas_tables, file)
if __name__ == '__main__':
    ScrapePlayers.get_players_from_lineup()

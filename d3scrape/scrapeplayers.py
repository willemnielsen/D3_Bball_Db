from d3scrape.scrapeindpages import ScrapeIndPages
from d3scrape.scrapetools import ScrapeTools as st
from bs4 import BeautifulSoup as bs
from d3scrape.teamandpage import Player
from uuid import uuid4

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
        teams = st.load(base + 'updt_plys.pkl')
        for team in teams:
            try:
                table = bs(tables[team.name], 'html.parser')
            except KeyError:
                continue
            else:
                if table.thead:
                    head_row = table.thead.find('tr')
                    body_rows = table.tbody.find_all('tr')
                else:
                    head_row = table.find('tr')
                    body_rows = table.find_all('tr')[1:]
                ths = head_row.find_all('th')
                headers = [th.get_text() for th in ths]
                players = []
                for row in body_rows:
                    stats = {}
                    for i, (stat, head) in enumerate(zip(row.find_all('td'), headers)):
                        if i == 1:
                            try:
                                new_val = stat.a.get_text().strip().replace(' ', '').replace('\n', ' ')
                                bio = team.baseurl + stat.a.get('href')
                            except AttributeError:
                                new_val = 'unknown'
                                bio = 'unknown'
                        else:
                            new_val = stat.get_text().strip().replace(' ', '').replace('\n', ' ')
                        stats[head] = new_val
                    players.append(Player(uuid4().time_low, team.name, bio=bio, stats=stats))
                team.players = players
        st.dump(teams, base + 'updated_teams_with_players.pkl')


    @staticmethod
    def teams_with_players():
        teams = st.load(base + 'updated_teams_with_players.pkl')
        count = 0
        for team in teams:
            if team.players:
                count += 1
        print(count)













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
    ScrapePlayers.teams_with_players()

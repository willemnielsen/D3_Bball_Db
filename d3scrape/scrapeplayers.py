from d3scrape.scrapeindpages import ScrapeIndPages
from d3scrape.scrapetools import ScrapeTools as st
from bs4 import BeautifulSoup as bs
from d3scrape.teamandpage import Player
from uuid import uuid4


class ScrapePlayers:
    @staticmethod
    def scrape(teams):
        tables = ScrapePlayers.get_tables(teams)
        ScrapePlayers.get_players(tables)

    @staticmethod
    def get_tables(teams, from_where='sites_and_files'):
        failed = []
        tables = {}
        for team in teams:
            if team.ind_page:
                table = ScrapePlayers.get_table(teams, from_where=from_where)
                if table:
                    tables[team.name] = str(table)
                else:
                    failed.append(team)
        return tables, failed

    @staticmethod
    def get_players(teams):
        tables = ScrapePlayers.get_tables(teams)
        for team in teams:
            if team.name in tables:
                table = bs(tables[team.name], 'html.parser')
                if team.ind_page.lineup:
                    players = ScrapePlayers.get_players_from_team_lineup(team, table)
                else:
                    players = ScrapePlayers.get_players_from_team_ind(team, table)
                team.players = players
        st.dump(teams, '../mp/teams_with_players.pkl')

    @staticmethod
    def get_players_from_team(team, table):
        if team.ind_page.lineup:
            return ScrapePlayers.get_players_from_team_lineup(team, table)
        else:
            return ScrapePlayers.get_players_from_team_ind(team, table)

    @staticmethod
    def get_players_from_team_lineup(team, table):
        headers, rows = ScrapePlayers.get_headers_and_rows(table)
        players = []
        for row in rows:
            players.append(ScrapePlayers.get_player_lineup(team, row, headers))
        return players

    @staticmethod
    def get_players_from_team_ind(team, table):
        players = []
        for row in table.tbody.find_all('tr'):
            ScrapePlayers.get_player_ind(team, row)
        return players

    @staticmethod
    def get_player_ind(team, row):
        name_obj = row.th.a if row.th.a else row.th
        name = name_obj.get_text()
        stats = ScrapePlayers.get_stats_ind(team, row)
        return Player(team, name=name, stats=stats)

    @staticmethod
    def get_stats_ind(team, row):
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
        return stats

    @staticmethod
    def get_headers_and_rows(table):
        if table.thead:
            head_row = table.thead.find('tr')
            body_rows = table.tbody.find_all('tr')
        else:
            head_row = table.find('tr')
            body_rows = table.find_all('tr')[1:]
        ths = head_row.find_all('th')
        headers = [th.get_text() for th in ths]
        return headers, body_rows


    @staticmethod
    def get_player_lineup(team, row, headers):
        stats, bio = ScrapePlayers.get_stats_lineup(team, row, headers)
        return Player(team, bio=bio, stats=stats)

    @staticmethod
    def get_stats_lineup(team, row, headers):
        stats = {}
        for i, (stat, head) in enumerate(zip(row.find_all('td'), headers)):
            if i == 1 and stat.a and stat.a.get('href'):
                new_val = stat.a.get_text().strip().replace(' ', '').replace('\n', ' ')
                bio = team.baseurl + stat.a.get('href')
            else:
                new_val = stat.get_text().strip().replace(' ', '').replace('\n', ' ')
            stats[head] = new_val
        return stats, bio




    @staticmethod
    def get_table(team, from_where):
        soup = team.ind_page.get_soup(from_where=from_where)
        if team.ind_page.lineup:
            try:
                team_table = soup.find_all('table')[3]
                return team_table
            except AttributeError:
                return
        else:
            try:
                team_table = soup.find_all('table')[1]
                return team_table
            except AttributeError:
                return



    @staticmethod
    def get_href(soup, team):
        button = soup.find('a', string='Individual')
        if button:
            return team.stats_page.url + button.get('href')
        button = soup.find('a', string='Lineup')
        if button:
            return team.baseurl + button.get('href')

    @staticmethod
    def get_soup(team, from_where):
        if from_where == 'old' or from_where == 'both':
            if team.stats_page.has_doc:
                return team.stats_page.get_soup()
            if from_where == 'both':
                return team.stats_page.get_new_soup()
            return
        if from_where == 'new':
            return team.stats_page.get_new_soup()
        return


    @staticmethod
    def save_tables(path):
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
        return all_tables


    @staticmethod
    def save_players(teams):
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
        teams = st.load('mp/updated_teams.pkl')
        lineup_teams = st.load('mp/lineup_urls.pkl')
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
        st.dump(all_tables,'mp/lineup_tables.pkl')





    @staticmethod
    def save_players_from_lineup():
        tables = st.load('mp/lineup_tables.pkl')
        teams = st.load('mp/updt_plys.pkl')
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
        st.dump(teams, 'mp/updated_teams_with_players.pkl')


    @staticmethod
    def teams_with_players():
        teams = st.load('mp/updated_teams_with_players.pkl')
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

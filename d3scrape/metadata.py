from teamandpage import Team, Page, Player
from scrapetools import ScrapeTools as st
import sys


path = sys.argv[0]
teams = st.load(path)


def num_teams():
    count = 0
    for i in range(len(teams)):
        count += 1
    print('Number of teams: ' + str(count))


def num_stats_pages():
    count = 0
    for team in teams:
        if team.stats_page:
            count += 1
    print('Number of stats pages: ' + str(count))


def num_stats_page_downloads():
    count = 0
    for team in teams:
        if team.stats_page:
            if team.stats_page.has_doc:
                count += 1
    print('Number of stats page downloads: ' + str(count))


def num_ind_pages():
    count = 0
    for team in teams:
        if team.ind_page:
            count += 1
    print('Number of indivdual pages: ' + str(count))


def num_ind_page_downloads():
    count = 0
    for team in teams:
        if team.ind_page:
            if team.ind_page.has_doc:
                count += 1
    print('Number of individual pages downloads' + str(count))


def num_teams_with_players():
    count = 0
    for team in teams:
        if team.players:
            count += 1
    print('Number of teams with players' + str(count))








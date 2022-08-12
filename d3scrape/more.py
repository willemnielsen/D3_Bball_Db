from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from scrapetools import ScrapeTools as st
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, NoSuchAttributeException,\
    WebDriverException, MoveTargetOutOfBoundsException
import time

base = '/Users/erichegonzales/PycharmProjects/playerscrape/mp/'
def more():
    no_more = []
    more_not_inter = []
    no_stats = []
    no_href = []
    teams = st.load(base + 'nts.pkl')
    for team in teams:
        # chrome_options = wd.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        count = 0
        if not team.stats_page:
            d = wd.Chrome()
            print('requesting: ' + team.name)
            try:
                d.get(team.url)
            except WebDriverException:
                d.close()
                continue
            try:
                more = d.find_element(By.XPATH, ("// a[contains(text(), 'More')]"))
            except NoSuchElementException:
                no_more.append(team.name)
                d.close()
                continue
            try:
                ActionChains(d).move_to_element(more).perform()
            except (ElementNotInteractableException, MoveTargetOutOfBoundsException):
                more_not_inter.append(team.name)
                d.close()
                continue
            time.sleep(1)
            try:
                stats = d.find_element(By.XPATH, "// a[contains(text(), 'Statistics')]")
            except NoSuchElementException:
                try:
                    stats = d.find_element(By.XPATH, "// a[contains(text(), 'Stats')]")
                except NoSuchElementException:
                    no_stats.append(team.name)
                    d.close()
                    continue
            try:
                url = stats.get_attribute('href')
            except NoSuchAttributeException:
                no_href.append(team.name)
                d.close()
                continue
            if url:
                print('found stats page for ' + team.name)
                count += 1
                team.init_stats_page(url)
            d.close()
    st.dump(no_more, base + 'no_more.pkl')
    st.dump(no_stats, base + 'no_stats.pkl')
    st.dump(more_not_inter, base + 'more_not_inter.pkl')
    st.dump(no_href, base + 'no_href.pkl')
    print(count)


def try_again():
    no_more = st.load(base + 'no_more.pkl')
    no_stats = st.load(base + 'no_stats.pkl')
    more_not_inter = st.load(base + 'more_not_inter.pkl')
    no_href = st.load(base + 'no_href.pkl')
    teams = st.load(base + 'nts.pkl')
    count = 0
    for team in teams:
        if not team.stats_page:
            if not team.name in no_more:
                if not team.name in no_stats:
                    if not team.name in more_not_inter:
                        if not team.name in no_href:
                            d = wd.Chrome()
                            print('requesting: ' + team.name)
                            try:
                                d.get(team.url)
                            except WebDriverException:
                                d.close()
                                continue
                            try:
                                more = d.find_element(By.XPATH, ("// a[contains(text(), 'More')]"))
                            except NoSuchElementException:
                                d.close()
                                continue
                            try:
                                ActionChains(d).move_to_element(more).perform()
                            except (ElementNotInteractableException, MoveTargetOutOfBoundsException):
                                d.close()
                                continue
                            time.sleep(1)
                            try:
                                stats = d.find_element(By.XPATH, "// a[contains(text(), 'Statistics')]")
                            except NoSuchElementException:
                                try:
                                    stats = d.find_element(By.XPATH, "// a[contains(text(), 'Stats')]")
                                except NoSuchElementException:
                                    d.close()
                                    continue
                            try:
                                url = stats.get_attribute('href')
                            except NoSuchAttributeException:
                                d.close()
                                continue
                            if url:
                                print('found stats page for ' + team.name)
                                count += 1
                                team.init_stats_page(url)
                            d.close()
    st.dump(teams, base + 'nts_sel.pkl')


def more_not_inter():
    more_not_inter = st.load(base + 'more_not_inter.pkl')
    teams = st.load(base + 'nts_sel.pkl')
    count = 0
    for team in teams:
        if team.name in more_not_inter:
            d = wd.Chrome()
            print('requesting: ' + team.name)
            try:
                d.get(team.url)
            except WebDriverException:
                d.close()
                continue
            try:
                more = d.find_element(By.XPATH, ("// a[contains(text(), 'More')]"))
            except NoSuchElementException:
                d.close()
                continue
            try:
                ActionChains(d).move_to_element(more).perform()
            except (ElementNotInteractableException, MoveTargetOutOfBoundsException):
                time.sleep(1)
                try:
                    stats = d.find_element(By.XPATH, "// a[contains(text(), 'Statistics')]")
                except NoSuchElementException:
                    try:
                        stats = d.find_element(By.XPATH, "// a[contains(text(), 'Stats')]")
                    except NoSuchElementException:
                        d.close()
                        continue
                try:
                    url = stats.get_attribute('href')
                except NoSuchAttributeException:
                    d.close()
                    continue
                if url:
                    print('found stats page for ' + team.name)
                    count += 1
                    team.init_stats_page(url)
                d.close()
    st.dump(teams, base + 'nts_sel.pkl')



if __name__ == '__main__':
    teams = st.load(base + 'nts_sel.pkl')
    count = 0
    for team in teams:
        if team.stats_page:
            count += 1
    print(count)

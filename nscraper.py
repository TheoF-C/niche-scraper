import time
import requests
from bs4 import BeautifulSoup
from page_paths import PATHS


class NScraper:

    def __init__(self, headers, page_lim=111, delay=7):
        self.HEADERS = headers
        self.PAGE_LIM = page_lim
        self.DELAY = delay
        self.data = {}

    def compile_colleges(self, pages=None, start=1):

        if pages is None:
            pages = self.PAGE_LIM

        url = "https://www.niche.com/colleges/search/best-colleges/"

        for i in range(start, pages + 1):
            response = requests.get(url, headers=self.HEADERS, params=(('page', str(i)),))
            soup = BeautifulSoup(response.content, 'html.parser')
            heated_soup = soup.find_all("li", {"class": "search-results__list__item"})
            self.add_colleges([college.find("section")["aria-label"] for college in heated_soup])
            time.sleep(self.DELAY)

    def scrape(self, actions, sync=False, thread=None):
        base_url = "https://www.niche.com/colleges/"

        for college, value in self.data.items():
            response = requests.get(base_url + college, headers=self.HEADERS)
            soup = BeautifulSoup(response.content, 'html.parser')
            start = time.perf_counter()

            for action in actions:
                value[action] = self.bucket_scrape(soup, PATHS[action][0], PATHS[action][1])

            if thread is not None:
                thread(value)

            if sync:
                time.sleep(self.DELAY - round(time.perf_counter() - start, 2))
            else:
                time.sleep(self.DELAY)

    def bucket_scrape(self, soup, eid, label):
        soup = soup.find(id=eid).find("div", {"class": "profile__buckets"}).find_all("span")
        heated_soup = None

        for span in soup:
            if span and span.text == label:
                heated_soup = span.parent.find_next_sibling()
                break

        if heated_soup is not None:
            return heated_soup.find("span").text

        return None

    def format_data(self, data):
        for key in data:
            value = data[key]
            if value:
                if key == "sat_range" or key == "act_range":
                    score_range = value.split("-")
                    data[key] = {"low": int(score_range[0]), "high": int(score_range[1])}
                elif value == 'No data available \xa0':
                    data[key] = None
                else:
                    try:
                        data[key] = int(value.translate({ord(c): None for c in "$%,"}))
                    except ValueError:
                        pass

    def format_all(self):
        for college in self.data:
            self.format_data(self.data[college])

    def process_name(self, name):
        return '-'.join(name.lower().split()).replace('&', '-and-').translate({ord(c): None for c in "()"})

    def get_colleges(self):
        return self.data.keys()

    def add_colleges(self, colleges):
        for college in colleges:
            self.data[self.process_name(college)] = {'name': college}

    def del_colleges(self, colleges):
        for college in colleges:
            del self.data[college]

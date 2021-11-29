from nscraper import NScraper
from page_paths import PATHS
from pymongo import MongoClient
import config

nScraper = NScraper(config.HEADERS)
nScraper.compile_colleges(pages=6)

client = MongoClient("")

my_database = client['niche_scraping']
my_collection = my_database['college_db_test']


def process(college):
    nScraper.format_data(college)
    my_collection.insert_one(college)


nScraper.scrape(actions=list(PATHS.keys()), sync=True, thread=process)
college_data = nScraper.data

for value in nScraper.data.values():
    print(value)

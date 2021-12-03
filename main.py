from nscraper import NScraper
from page_paths import PATHS
from pymongo import MongoClient
import config

nScraper = NScraper(config.HEADERS)
nScraper.add_colleges(['Massachusetts Institute of Technology', 'Harvard University', 'Stanford University'])
# nScraper.compile_colleges(pages=6)

client = MongoClient(config.CONNECT)
my_database = client['niche_scraping']
my_collection = my_database['college_db_test']

nScraper.scrape(actions=list(PATHS.keys()), sync=True, thread=my_collection.insert_one)
college_data = nScraper.data

for value in nScraper.data.values():
    print(value)

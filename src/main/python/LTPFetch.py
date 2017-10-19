from time import sleep

import requests
from bs4 import BeautifulSoup


class LTPFetch:
    # Url to fetch daily High Low LTP Open Close
    url = "http://www.bseindia.com/stock-share-price/SiteCache/EQHeaderData.aspx?text="

    def __init__(self, Code=''):
        # sleep(0.2)
        # print("Querying for Code = {}".format(Code))
        try:
            self.response = ''
            r = requests.get(self.url + Code)
            r.raise_for_status()
            # response
            soup = BeautifulSoup(r.text, 'html.parser')
            self.response = soup.text
            # print("response = {}".format(self.response))
        except requests.exceptions.HTTPError as e:
            print("Error occurred fetching data for Code = {}, error = {}".format(Code, e))

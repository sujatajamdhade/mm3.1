from time import sleep

import requests
from bs4 import BeautifulSoup


class HighLowQuery:
    url = "http://www.bseindia.com/stock-share-price/SiteCache/52WeekHigh.aspx?Type=EQ&text="

    def __init__(self, Code=''):
        sleep(1.0 / 4.0)
        # print("Querying for Code = {}".format(Code))
        try:
            self.response = ''
            r = requests.get(self.url + Code)
            r.raise_for_status()
            # response
            soup = BeautifulSoup(r.text, 'html.parser')
            self.response = soup.text
        except requests.exceptions.HTTPError as e:
            print("Error occurred fetching data for Code = {}, error = {}".format(Code, e))

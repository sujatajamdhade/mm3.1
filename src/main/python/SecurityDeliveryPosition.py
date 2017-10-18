import re
from time import sleep

import requests
from bs4 import BeautifulSoup


class SecurityDeliveryPosition:
    url = "http://www.bseindia.com/stock-share-price/SiteCache/SecurityPosition.aspx?Type=EQ&text="
    regex = "Securitywise Delivery PositionTrade Date\d\d [A-Za-z]{3} \d\d\d\dQuantity Traded([0-9.,]+)Deliverable Quantity\(Gross across client level\)([0-9.,]+)% of Deliverable Quantity to Traded Quantity([0-9.,]+)"

    def __init__(self, Code=''):
        sleep(2)
        # print("Querying for Code = {}".format(Code))
        try:
            self.PDQ2TQ = 0
            r = requests.get(self.url + Code)
            r.raise_for_status()
            # print("Status = " + str(r.status_code))
            # response
            soup = BeautifulSoup(r.text, 'html.parser')
            self.response = soup.text
            # print("response = " + self.response)
            pattern = re.compile(self.regex)
            result = pattern.match(self.response)
            if result:
                self.PDQ2TQ = float(result.group(3).replace(',', ''))
                # print("PDQ2TD = {}".format( self.PDQ2TQ ) )
            else:
                print("No match found. response = " + self.response)
        except requests.exceptions.HTTPError as e:
            print("Error occurred fetching data for Code = {}, error = {}".format(Code, e))
            # Save Code to retry at later time.



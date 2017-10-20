import datetime
from time import sleep

import requests
from bs4 import BeautifulSoup


class Holidays:
    url = "http://www.bseindia.com/markets/marketinfo/listholi.aspx"
    holidayDates = []

    def __init__(self):
        sleep(1.0/4.0)
        try:
            self.response = ''
            r = requests.get(self.url)
            r.raise_for_status()
            # response
            soup = BeautifulSoup(r.text, 'html.parser')
            self.response = soup.text
            tables = soup.find_all('table')
            # table index 3 is our table for 'Trading Holidays for 2017 - Equity Segment, Equity Derivative Segment and SLB Segment'
            equityHolidays = tables[3]
            for row in equityHolidays.find_all('tr'):
                cols = row.find_all('td')
                dt = ' '.join(cols[2].text.strip().split()) # e.g. January 26, 2017
                try:
                    obj = datetime.datetime.strptime(dt, "%B %d, %Y").date()
                    self.holidayDates.append(obj)
                except ValueError as v:
                    # print("Invalid Date = {}".format(dt))
                    None
            # print(len(self.holidayDates))
            # print(self.holidayDates)
        except requests.exceptions.HTTPError as e:
            print("Error occurred fetching holiday dates data, error = {}".format(e))

    def isTodayAHoliday(self):
        currentDate = datetime.datetime.today().date()
        # print(currentDate)
        for dt in self.holidayDates:
            if currentDate == dt:
                return True
        return False

# if __name__ == "__main__":
#     h = Holidays()
#     print(h.isTodayAHoliday())
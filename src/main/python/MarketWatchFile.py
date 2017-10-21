import csv
import re

import requests

from src.main.python.Security import Security

DATA_FOLDER = "/home/sachin/moneymachine/data"

RESOURCE_FOLDER = "/home/sachin/pycharm/moneymachine/src/main/resource"

EVENT_DATA_FILE = "{}/EVENT_DATA_MARKETWATCH_ALL.txt".format(RESOURCE_FOLDER)


class MarketWatchFile:
    CSV_URL = 'http://www.bseindia.com/markets/equity/EQReports/MarketWatch.aspx?expandable=2'
    D_SECURITIES = {}
    fname = ""
    decoded_content = None

    # req_data
    req_data = {}

    req_data['__EVENTTARGET'] = ''
    req_data['__EVENTARGUMENT'] = ''
    with open(EVENT_DATA_FILE) as fin:
        __VIEWSTATE = fin.readline()
        # print("VIEWSTATE = '{}'".format(__VIEWSTATE.strip()))
        req_data['__VIEWSTATE'] = __VIEWSTATE.strip()
        __EVENTVALIDATION = fin.readline()
        # print("VALIDATION = '{}'".format(__EVENTVALIDATION.strip()))
        req_data['__EVENTVALIDATION'] = __EVENTVALIDATION.strip()
    req_data['__VIEWSTATEGENERATOR'] = '31C5C149'
    req_data['myDestination'] = '#'
    req_data['WINDOW_NAMER'] = '1'
    # req_data['ctl00$ContentPlaceHolder1$hdfTy'] = 'AllMktAllMkt'
    req_data['ctl00$ContentPlaceHolder1$hdfTy'] = 'Group'
    # req_data['ctl00$ContentPlaceHolder1$hdfFL'] = 'All'
    req_data['ctl00$ContentPlaceHolder1$hdfFL'] = 'A'
    req_data['ctl00$ContentPlaceHolder1$hdfCOrder'] = 'TT'
    req_data['ctl00$ContentPlaceHolder1$DDate'] = ''
    req_data['ctl00$ContentPlaceHolder1$imgDownload.x'] = '8'
    req_data['ctl00$ContentPlaceHolder1$imgDownload.y'] = '10'
    # req_data['ctl00$ContentPlaceHolder1$ddlType'] = 'AllMkt'
    req_data['ctl00$ContentPlaceHolder1$ddlType'] = 'Group'
    req_data['ctl00$ContentPlaceHolder1$ddlGrp'] = 'A'
    req_data['ctl00$ContentPlaceHolder1$ddlIndx'] = '16'
    req_data['ctl00$ContentPlaceHolder1$ddlOrder'] = 'TT'

    def __init__(self):
        with requests.Session() as s:
            download = s.post(self.CSV_URL, self.req_data)

            # print(download.headers)
            d = download.headers['content-disposition']
            fnameList = re.findall("filename=(.+)", d)
            self.fname = fnameList[0].replace("/", "_")
            # print("fname = {}".format(fname))

            self.decoded_content = download.content.decode('utf-8')

            cr = csv.reader(self.decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            # ['Security Code', 'Security Name', 'Security Group', 'Open', 'High ', 'Low', 'LTP', 'No. of Shares Traded ',
            #  "Total Turnover  (<img src='../../../include/images/rs.gif' alt='my image' /> Lac)", 'No. of Trades']
            counter = 0
            for row in my_list:
                counter += 1
                if counter == 1:
                    continue
                # print(row)
                Code = row[0].strip()
                Name = row[1].strip()
                Group = row[2].strip()
                LTP = float(row[6].strip().replace(',', ''))
                VOLUME = float(row[7].strip().replace(',', ''))
                TURNOVER = float(row[8].strip().replace(',', ''))
                TRADES = float(row[9].strip().replace(',', ''))
                self.D_SECURITIES[Code] = Security(Code=Code, Name=Name, Group=Group, LTP=LTP, TURNOVER=TURNOVER,
                                                   VOLUME=VOLUME, TRADES=TRADES)
            print("Total securities loaded = {}".format(len(self.D_SECURITIES)))

    def get(self):
        return self.D_SECURITIES

    def download(self):
        thefile = open(DATA_FOLDER + "/" + self.fname, 'w')
        thefile.write("%s" % self.decoded_content)



if __name__ == "__main__":
    m = MarketWatchFile()
    m.download()

import csv

import requests

from src.main.python.Globals import RESOURCE_FOLDER
from src.main.python.Security import Security
from src.main.python.validateSecuritySells import getLastTradedPrice


class BSECorporateSecurities:


    def downloadAllEquitySecurities():
        LIST_URL = 'http://www.bseindia.com/corporates/List_Scrips.aspx'
        # req_data
        req_data = {}

        with open(EVENT_DATA_FILE) as fin:
            __VIEWSTATE = fin.readline()
            # print("VIEWSTATE = '{}'".format(__VIEWSTATE.strip()))
            req_data['__VIEWSTATE'] = __VIEWSTATE.strip()
            __EVENTVALIDATION = fin.readline()
            # print("VALIDATION = '{}'".format(__EVENTVALIDATION.strip()))
            req_data['__EVENTVALIDATION'] = __EVENTVALIDATION.strip()

        req_data['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$lnkDownload'
        req_data['__EVENTARGUMENT'] = ''
        req_data['__VIEWSTATEGENERATOR'] = 'CF507786'
        req_data['myDestination'] = '#'
        req_data['WINDOW_NAMER'] = '1'
        req_data['ctl00$ContentPlaceHolder1$hdnCode'] = ''
        req_data['ctl00$ContentPlaceHolder1$ddSegment'] = 'Equity'
        req_data['ctl00$ContentPlaceHolder1$ddlStatus'] = 'Active'
        req_data['ctl00$ContentPlaceHolder1$getTExtData'] = ''
        req_data['ctl00$ContentPlaceHolder1$ddlGroup'] = 'Select'
        req_data['ctl00$ContentPlaceHolder1$ddlIndustry'] = 'Select'

        with requests.Session() as s:
            download = s.post(LIST_URL, req_data)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            listOfSecurities = list(cr)
            print("Total Equity Securities = {}".format(len(listOfSecurities)))
            return listOfSecurities


    def filterSecurityByGroup(Securities, Group):
        L_SECURITIES = set()
        for row in Securities:
            currentGroup = str(row[4]).strip()
            currentCode = str(row[0]).strip()
            # print("Group = '{}', Current Group = '{}'".format(Group, currentGroup))
            if Group == currentGroup:
                ltp = getLastTradedPrice(currentCode).LTP
                L_SECURITIES.add(Security(Code=currentCode, Name=row[1], Group=row[4], LTP=ltp))
        print("Total Securities for Group {} = {}".format(Group, len(L_SECURITIES)))
        return L_SECURITIES


EVENT_DATA_FILE = "{}/EVENT_DATA_LIST_SECURITIES_ALL.txt".format(RESOURCE_FOLDER)
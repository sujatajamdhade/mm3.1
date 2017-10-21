#!/usr/bin/python3
# Version: 30092017.0.1
import base64
import csv
# Imports
from datetime import datetime

# Useful routines
import requests

from src.main.python.HighLowInfo import HighLowInfo
from src.main.python.HighLowQuery import HighLowQuery
from src.main.python.Holidays import Holidays
from src.main.python.MarketWatchFile import MarketWatchFile
from src.main.python.Security import Security
from src.main.python.SecurityDeliveryPosition import SecurityDeliveryPosition
from src.main.python.SendMail import SendMail
from src.main.python.validateSecuritySells import readHoldingsFile, HoldingsFile, getLastTradedPrice

SECURITY_FIELDS = "Code,Name,Group,10p,20p,30p,LTP,V52WH,V52WHDT,V52WL,V52WLDT,MH,ML,TURNOVER,VOLUME,TRADES,PDQ2TQ,PALOW"

# Empty List of Securities.
SECURITIES = set()

# Retry Set for Failed Codes
RETRY_CODES = set()

DATA_FOLDER = "/home/sachin/data"
# DATA_FOLDER = "/home/sachin/Downloads"
OUTPUT_FOLDER = "/home/sachin/data/out"

RESOURCE_FOLDER = "/home/sachin/moneymachine/src/main/resource"

EVENT_DATA_FILE = "{}/EVENT_DATA_LIST_SECURITIES_ALL.txt".format(RESOURCE_FOLDER)

# Get Current Date
dt = datetime.now()
DAY = dt.day
MONTH = dt.month
YEAR = dt.year

# File containing all Group A securities.
WatchFile = "{}/MarketWatch_{:02d}_00_{}.csv".format(DATA_FOLDER, DAY, YEAR)

# Output file.
MarketPositions = "{}/MarketPositions_{}_00_{}.csv".format(OUTPUT_FOLDER, DAY, YEAR)

# List of Securities currently holding position.
SECURITIES_IN_POS = {}

# Read all Group A securities.
# if not os.path.exists(WatchFile):
#     print(WatchFile + "does not exist.")
#     sys.exit(1)

# TODO: We need to replace this text in the watchfile something the BSE site adds.
TOTAL_TURNOVER = "Total Turnover  (<img src='../../../include/images/rs.gif' alt='my image' /> Lac)"


def readWatchFile():
    try:
        with open(WatchFile) as csvfile:
            # Read csv file.
            reader = csv.DictReader(csvfile)
            for row in reader:
                SEC = Security(Code=row['Security Code'], Name=row['Security Name'], Group=row['Security Group'],
                               LTP=float(row['LTP']), TURNOVER=float(row[TOTAL_TURNOVER]),
                               VOLUME=float(row['No. of Shares Traded ']), TRADES=float(row['No. of Trades']))
                SECURITIES.add(SEC)
                # print("Security Code = " + SEC.Code + ", Security Name = " + SEC.Name + ", Group = " + SEC.Group )
            print("Total Securities read = {}".format(len(SECURITIES)))
    except IOError:
        print(WatchFile + " File not found.")


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


def processCode(Code):
    q = HighLowQuery(Code)
    if not q.response:
        RETRY_CODES.add(Code)
        print("52 Week HighLow Fetch Error: Will retry Code = {} later.".format(Code))
        return None
    else:
        i = HighLowInfo(q.response)
        s = next((x for x in SECURITIES if x.Code == Code), None)
        s.update(i)
        d = SecurityDeliveryPosition(Code)
        if d.PDQ2TQ != 0:
            s.PDQ2TQ = d.PDQ2TQ
        else:
            RETRY_CODES.add(Code)
            print("Securitywise Deliverable Position Fetch Error: Will retry Code = {} later.".format(Code))
            return None
        return s

def sendReport():
    password = base64.b64decode("c2ExMjNBU0g=").decode('utf-8')
    m = SendMail(sender="sujata.c.jamdhade@gmail.com", password=password, recipients=['sachincjamdhade@gmail.com'],
                 subject="Market Positions", attachments=[MarketPositions], msg="Market Positions for {}".format(datetime.today().date()))
    m.send()

def main():
    h = Holidays()
    if (h.isTodayAHoliday() == True):
        print("Today is a holiday, YAYYYYY!!")
        return

    readHoldingsFile(HoldingsFile, SECURITIES_IN_POS)
    # print(SECURITIES_IN_POS)
    m = MarketWatchFile()
    # m_securities = m.get()
    m.download()
    readWatchFile()
    # listOfSecurities = downloadAllEquitySecurities()
    # SECURITIES = filterSecurityByGroup(listOfSecurities, "A")
    with open(MarketPositions, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        # Print in a vertical format so it is easy to import and analyze.
        print("No., " + SECURITY_FIELDS)
        csvwriter.writerow(SECURITY_FIELDS.split(','))
        counter = 0
        for SEC in SECURITIES:
            if any(x == SEC.Code for x in SECURITIES_IN_POS.keys()):
                print("Currently holding position for {} ... so skipping.".format(SEC.Code))
                continue
            s = processCode(SEC.Code)
            if s is not None:
                counter += 1
                print("{:3d}:{}".format(counter, s.print_r()))
                csvwriter.writerow(s.print_r().split(','))

        try:
            Code = RETRY_CODES.pop()
            while (Code):
                s = processCode(Code)
                if s is not None:
                    counter += 1
                    print("{:3d}:{}".format(counter, s.print_r()))
                    csvwriter.writerow(s.print_r().split(','))
                    print("Reprocessed Code = {}".format(Code))
                Code = RETRY_CODES.pop()
        except KeyError as e:
            print("All Codes processed.")

    sendReport()


if __name__ == "__main__":
    main()

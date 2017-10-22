#!/usr/bin/python3
import base64
import csv
from datetime import datetime

from src.main.python.Globals import OUTPUT_FOLDER, DAY, YEAR
from src.main.python.HighLowInfo import HighLowInfo
from src.main.python.HighLowQuery import HighLowQuery
from src.main.python.Holidays import Holidays
from src.main.python.MarketWatchFile import MarketWatchFile
from src.main.python.Security import SECURITY_FIELDS
from src.main.python.SecurityDeliveryPosition import SecurityDeliveryPosition
from src.main.python.SendMail import SendMail
from src.main.python.SecurityHoldings import readHoldingsFile, HoldingsFile

# Retry Set for Failed Codes
RETRY_CODES = set()

# Output file.
MarketPositions = "{}/MarketPositions_{}_00_{}.csv".format(OUTPUT_FOLDER, DAY, YEAR)


def processCode(Code, Securities):
    q = HighLowQuery(Code)
    if not q.response:
        RETRY_CODES.add(Code)
        print("52 Week HighLow Fetch Error: Will retry Code = {} later.".format(Code))
        return None
    else:
        i = HighLowInfo(q.response)
        s = next((x for x in Securities if x.Code == Code), None)
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
                 subject="Market Positions", attachments=[MarketPositions],
                 msg="Market Positions for {}".format(datetime.today().date()))
    m.send()


def main():
    h = Holidays()
    if (h.isTodayAHoliday() == True):
        print("Today is a holiday, YAYYYYY!!")
        return

    # List of Securities currently holding position.
    SECURITIES_IN_POS = {}

    readHoldingsFile(HoldingsFile, SECURITIES_IN_POS)
    # print(SECURITIES_IN_POS)
    m = MarketWatchFile()
    # m_securities = m.get()
    # m.download()
    SECURITIES = m.get()
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
            s = processCode(SEC.Code, SECURITIES)
            if s is not None:
                counter += 1
                print("{:3d}:{}".format(counter, s.print_r()))
                csvwriter.writerow(s.print_r().split(','))

        try:
            Code = RETRY_CODES.pop()
            while (Code):
                s = processCode(Code, None)
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

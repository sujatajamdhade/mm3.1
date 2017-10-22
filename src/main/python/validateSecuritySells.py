import csv

from src.main.python.Globals import OUTPUT_FOLDER, DAY, MONTH, YEAR
from src.main.python.Holidays import Holidays
from src.main.python.LTPFetch import LTPFetch
from src.main.python.LTPInfo import LTPInfo
# Get Current Date
from src.main.python.SecurityHoldings import SecurityHoldings
from src.main.python.SendMail import sendAlert
from src.main.python.Utilities import percentage

FIELDS = "Code,Name,Buy Price"

DAILY_FILE = "{}/DailyGain_{}_{}_{}.csv".format(OUTPUT_FOLDER, DAY, MONTH, YEAR)
DAILY_FIELDS = "Code, Name, BUY, LTP, 20p, Diff, Percentage"


def getLastTradedPrice(Code):
    ltp = LTPFetch(Code)
    return LTPInfo(ltp.response)


def main():
    h = Holidays()

    if (h.isTodayAHoliday() == True):
        print("Today is a holiday, YAYYYYY!!")
        return

    # Empty Dictionary of Securities.
    SECURITIES = {}
    h = SecurityHoldings()
    h.getSecurityHoldings(SECURITIES)

    with open(DAILY_FILE, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        print(DAILY_FIELDS)
        csvwriter.writerow(DAILY_FIELDS.split(','))
        for Code, Security in SECURITIES.items():
            LTPInfo = getLastTradedPrice(Code)
            # print("Code = {}, Name = {}, BUY = {:f}, LTP = {:f}, 20p = {:f}".format(Code, Security.Name, Security.BUY, LTPInfo.LTP,
            #                                                                               LTPInfo.LTP*1.2))
            buy20p = Security.BUY * 1.20
            diff = buy20p - LTPInfo.LTP
            f__Details = "{}, {}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}".format(Code, Security.Name, Security.BUY,
                                                                                 LTPInfo.LTP,
                                                                                 buy20p, diff, percentage(LTPInfo.LTP,
                                                                                                          Security.BUY) - 100.00)
            print(f__Details)
            csvwriter.writerow(f__Details.split(','))
            if diff <= 0:
                sendAlert(Security.Code, Security.Name, Security.BUY, LTPInfo.LTP)


if __name__ == "__main__":
    main()

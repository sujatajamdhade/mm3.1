import base64
import csv
import smtplib
from datetime import datetime

from src.main.python.Holidays import Holidays
from src.main.python.LTPInfo import LTPInfo
from src.main.python.LTPFetch import LTPFetch
from src.main.python.Security import Security

# Get Current Date
from src.main.python.Utilities import percentage

dt = datetime.now()
DAY = dt.day
MONTH = dt.month
YEAR = dt.year

HoldingsFile = "/home/sachin/moneymachine/holdings/holdings.csv"
FIELDS = "Code,Name,Buy Price"

OUTPUT_FOLDER = "/home/sachin/moneymachine/out"
DAILY_FILE = "{}/DailyGain_{}_{}_{}.csv".format(OUTPUT_FOLDER, DAY, MONTH, YEAR)
DAILY_FIELDS = "Code, Name, BUY, LTP, 20p, Diff, Percentage"

# Empty List of Securities.
SECURITIES = {}


def readHoldingsFile(file, securitiesHeld):
    try:
        with open(file) as csvfile:
            # Read csv file.
            reader = csv.DictReader(csvfile)
            for row in reader:
                SEC = Security(Code=row['Code'], Name=row['Name'], BUY=float(row['Buy Price']))
                securitiesHeld[SEC.Code] = SEC
                # print("Security Code = " + SEC.Code + ", Security Name = " + SEC.Name + ", Group = " + SEC.Group )
            print("Total Securities in holding = {}".format(len(securitiesHeld)))
    except IOError:
        print(file + " File not found.")


def getLastTradedPrice(Code):
    ltp = LTPFetch(Code)
    return LTPInfo(ltp.response)


def sendAlert(Code, Name, Buy, ltp):
    fromaddr = 'sujata.c.jamdhade@gmail.com'
    toaddrs = 'sachincjamdhade@gmail.com'
    msg = "\r\n".join([
        "Subject: Sell Alert for {}".format(Name),
        "",
        "Sell Security = {}, Buyed at = {:.2f}, Current Price ={:.2f} has crossed 20% gain.".format(Code, Buy, ltp)
    ])
    username = 'sujata.c.jamdhade@gmail.com'
    password = "c2ExMjNBU0g="
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, base64.b64decode(password).decode('utf-8'))
    server.sendmail(from_addr=fromaddr, to_addrs=toaddrs, msg=msg)
    server.quit()


def main():
    h = Holidays()

    if (h.isTodayAHoliday() == True):
        print("Today is a holiday, YAYYYYY!!")
        return

    readHoldingsFile(HoldingsFile, SECURITIES)

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

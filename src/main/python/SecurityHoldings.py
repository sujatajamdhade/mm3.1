import csv

from src.main.python.Globals import DATA_FOLDER
from src.main.python.Security import Security

HoldingsFile = "{}/holdings/holdings.csv".format(DATA_FOLDER)


class SecurityHoldings:


    def readHoldingsFile(self, inputFile='', securitiesHeld=None):
        try:
            with open(inputFile) as csvfile:
                # Read csv file.
                reader = csv.DictReader(csvfile)
                for row in reader:
                    SEC = Security(Code=row['Code'], Name=row['Name'], BUY=float(row['Buy Price']))
                    securitiesHeld[SEC.Code] = SEC
                    # print("Security Code = " + SEC.Code + ", Security Name = " + SEC.Name + ", Group = " + SEC.Group )
                print("Total Securities in holding = {}".format(len(securitiesHeld)))
        except IOError as e:
            print(e)

    def getSecurityHoldings(self, securitiesHeld):
        self.readHoldingsFile(HoldingsFile, securitiesHeld)

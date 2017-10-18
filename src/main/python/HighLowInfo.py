import re


class HighLowInfo:
    regex = "High Lows52 Week High \(adjusted\)([0-9.,]+)\((\d+/\d\d/\d\d\d\d)\)52 Week Low \(adjusted\)([0-9.,]+)\((\d+/\d\d/\d\d\d\d)\)52 Week High \(Unadjusted\)([0-9.,]+)\((\d+/\d\d/\d\d\d\d)\)52 Week Low \(Unadjusted\)([0-9.,]+)\((\d+/\d\d/\d\d\d\d)\)Month H/L([0-9.,]+)/([0-9.,]+)Week H/L([0-9.,]+)/([0-9.,]+)"

    def __init__(self, response=''):
        pattern = re.compile(self.regex)
        result = pattern.match(response)
        if result:
            self.V52WH = float(result.group(1).replace(',', ''))
            self.V52WHDT = result.group(2)
            self.V52WL = float(result.group(3).replace(',', ''))
            self.V52WLDT = result.group(4)
            result.group(5)
            result.group(6)
            result.group(7)
            result.group(8)
            self.MH = float(result.group(9).replace(',', ''))
            self.ML = float(result.group(10).replace(',', ''))
            result.group(11)
            result.group(12)
        else:
            print("No match found. response = " + response)



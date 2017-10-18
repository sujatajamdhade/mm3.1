import re


class LTPInfo:
    regex = "^BSE##B#As on \d\d .* \d\d \| \d\d:\d\d@C#\d+@P#@HL#([0-9.,]+),([0-9.,]+),([0-9.,]+),([0-9.,]+),([0-9.,]+)"

    def __init__(self, response=''):
        pattern = re.compile(self.regex)
        result = pattern.match(response)
        if result:
            # print("1 = {}, 2 = {}, 3 = {}, 4 = {}, 5 = {}".format(result.group(1), result.group(2), result.group(3), result.group(4), result.group(5)))
            self.PREVCLOSE = float(result.group(1).replace(',', ''))
            self.OPEN = float(result.group(2).replace(',',''))
            self.HIGH = float(result.group(3).replace(',', ''))
            self.LOW = float(result.group(4).replace(',', ''))
            self.LTP = float(result.group(5).replace(',', ''))
        else:
            print("No match found. response = " + response)
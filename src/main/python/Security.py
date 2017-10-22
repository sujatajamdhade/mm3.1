from src.main.python.Utilities import percentage

SECURITY_FIELDS = "Code,Name,Group,10p,20p,30p,LTP,V52WH,V52WHDT,V52WL,V52WLDT,MH,ML,TURNOVER,VOLUME,TRADES,PDQ2TQ,PALOW,BUY"

class Security:
    """A BSE Equity Security."""

    def __init__(self, Code="", Name="", Group="", V52WH=0, V52WL=0, LTP=0, MH=0, ML=0, V52WHDT="", V52WLDT="",
                 TURNOVER=0, VOLUME=0, TRADES=0, PDQ2TQ=0, BUY=0):
        self.Code = Code
        self.Name = Name
        self.Group = Group
        self.V52WH = V52WH
        self.V52WL = V52WL
        self.LTP = LTP
        self.MH = MH
        self.ML = ML
        self.V52WHDT = V52WHDT
        self.V52WLDT = V52WLDT
        self.TURNOVER = TURNOVER
        self.VOLUME = VOLUME
        self.TRADES = TRADES
        self.PDQ2TQ = PDQ2TQ
        self.PALOW = 0
        self.BUY = BUY
        # print( "Created Security = " + self.Name)

    def update(self, highLowInfo):
        self.V52WH = highLowInfo.V52WH
        self.V52WL = highLowInfo.V52WL
        self.V52WHDT = highLowInfo.V52WHDT
        self.V52WLDT = highLowInfo.V52WLDT
        self.MH = highLowInfo.MH
        self.ML = highLowInfo.ML
        self.PALOW = percentage(self.LTP - self.V52WL, self.V52WH - self.V52WL)

    def print_s(self):
        print(
            "Code = {}, "
            "Name = {}, "
            "Group = {}, "
            "10p = {:f}, "
            "20p = {:f}, "
            "30p = {:f}, "
            "LTP = {:f}, "
            "V52WH = {:f}, "
            "V52WHDT = {}, "
            "V52WL = {:f}, "
            "V52WLDT = {}, "
            "MH = {:f}, "
            "ML = {:f}, "
            "TURNOVER = {:f}, "
            "VOLUME = {:f}, "
            "TRADES = {:f}, "
            "PDQ2TQ = {:f},"
            "BUY = {:f}".format(
                self.Code,
                self.Name,
                self.Group,
                self.percentOfLow(10),
                self.percentOfLow(20),
                self.percentOfLow(30),
                self.LTP,
                self.V52WH,
                self.V52WHDT,
                self.V52WL,
                self.V52WLDT,
                self.MH,
                self.ML,
                self.TURNOVER,
                self.VOLUME,
                self.TRADES,
                self.PDQ2TQ,
                self.BUY));

    def print_v(self):
        # print( "Code,Name,Group,10p,20p,30p,LTP,V52WH,V52WHDT,V52WL,V52WLDT,MH,ML,TURNOVER,VOLUME,TRADES, BUY" );
        print(self.print_r());

    def print_r(self):
        return "{}, {}, {}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {}, {:.2f}, {}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}".format(
            self.Code, self.Name, self.Group, self.percentOfLow(10), self.percentOfLow(20), self.percentOfLow(30),
            self.LTP, self.V52WH, self.V52WHDT, self.V52WL, self.V52WLDT, self.MH, self.ML, self.TURNOVER, self.VOLUME,
            self.TRADES, self.PDQ2TQ, self.PALOW, self.BUY)

    def percentOfLow(self, percent):
        res = 0.0
        mul = (float(percent) / 100.0) + 1.0
        res = self.V52WL * mul
        return res



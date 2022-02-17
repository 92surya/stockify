class Stock:
    stock_name = ""
    previous_close = 0
    open_price = 0
    close_price = 0
    average_price = 0
    last_price = 0
    day_high = 0
    day_low = 0
    high_52 = 0
    low_52 = 0
    upper_band = 0
    lower_band = 0
    volume = 0

    def __init__(self, stock_dict):
        # print(stock_dict["symbol"])
        for key in stock_dict:
        	print(key,":",stock_dict[key])
        self.stock_name = stock_dict["symbol"]
        self.previous_close = stock_dict["previousClose"]
        self.open_price = stock_dict["open"]
        self.close_price = stock_dict["closePrice"]
        self.average_price = stock_dict["averagePrice"]
        self.last_price = stock_dict["lastPrice"]
        self.day_high = stock_dict["dayHigh"]
        self.day_low = stock_dict["dayLow"]
        self.high_52 = stock_dict["high52"]
        self.low_52 = stock_dict["low52"]
        self.upper_band = stock_dict["pricebandupper"]
        self.lower_band = stock_dict["pricebandlower"]
        self.volume = stock_dict["totalTradedVolume"]

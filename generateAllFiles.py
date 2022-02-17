import csv
import datetime
import os
import shutil
import subprocess
import time
from datetime import date
from jugaad_data.nse import bhavcopy_save, bhavcopy_fo_save
import sys
import getopt
import legacy_stocks as ls
import os.path

CWD = os.getcwd()#"/home/surya/git/stockify"


def setCWD():
    os.chdir(CWD)


def setIDXCWD():
    os.chdir("idxFiles/")


def setSBINCWD():
    os.chdir("sbinFiles/")


class StockData:
    trade_date = ""
    series = ""
    prev_close = 0
    open_price = 0
    high = 0
    low = 0
    ltp = 0
    close = 0
    vwap = 0
    w52_h = 0
    w52_l = 0
    volume = 0
    value = 0
    no_of_trades = 0
    symbol = ""

    def __init__(self, trade_date, series, open_price, high, low, prev_close, ltp, close, vwap, w52_h, w52_l, volume, value, no_of_trades, symbol):
        self.trade_date = trade_date
        self.series = series
        self.prev_close = prev_close
        self.open_price = open_price
        self.high = high
        self.low = low
        self.ltp = ltp
        self.close = close
        self.vwap = vwap
        self.w52_h = w52_h
        self.w52_l = w52_l
        self.volume = volume
        self.value = value
        self.no_of_trades = no_of_trades
        self.symbol = symbol


def main(argv):
    year = 2020
    month = 1
    day = 1
    start = 0
    end = 0
    name = 'SBIN'
    try:
        opts, args = getopt.getopt(argv, "hy:m:d:s:e:n:", [
                                   "year=", "month=", "day=", "start=", "end=", "name="])
    except getopt.GetoptError:
        print('generateAllFiles.py -y <year> -m <month> -d <day> -s <start> -e <end> -n <name>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                'generateAllFiles.py -y <year> -m <month> -d <day> -s <start> -e <end> -n <name>')
            sys.exit()
        elif opt in ("-y", "--year"):
            year = arg
        elif opt in ("-m", "--month"):
            month = arg
        elif opt in ("-d", "--day"):
            day = arg
        elif opt in ("-s", "--start"):
            start = arg
        elif opt in ("-e", "--end"):
            end = arg
        elif opt in ("-n", "--name"):
            name = arg
    print("Year is ", year)
    print("Month is ", month)
    print("Day is ", day)
    print("Start is ", start)
    print("End is ", end)
    print("Name is ", name)
    if year == 0 and start == 0:
        print('ERROR: enter valid date,month,year!')
        sys.exit()
    elif start != 0 and start > end:
        print('ERROR: enter valid start,end!')
        sys.exit()
    stock_data_list = []
    year = int(year)
    month = int(month)
    day = int(day)
    start = int(start)
    end = int(end)
    if name not in ls.legacy_stocks:
        name = 'SBIN'
    if start > 0:
        year = start
        while year <= end:
            month = 1
            while month <= 12:
                state = generateSBINFile(year, month, day, name)
                if state == -1:
                    return
                generateEQFile(year, month, day)
                generateFOFile(year, month, day)
                generateNIFTYFile(year, month, day)
                month = month + 1
            year = year + 1
    else:
        generateSBINFile(year, month, day)
        generateEQFile(year, month, day)
        generateFOFile(year, month, day)
        generateNIFTYFile(year, month, day)


def generateNIFTYFile(year, month, day):
    last_month_start_date = datetime.date(year, month, day)
    if month == 12:
        year = year + 1
        month = 0
    last_month_end_date = datetime.date(
        year, month + 1, day) - datetime.timedelta(days=1)
    if month == 0:
        year = year - 1
        month = 12
    if last_month_end_date > datetime.datetime.today().date():
        last_month_end_date = datetime.datetime.today().date()
    if last_month_start_date > datetime.datetime.today().date():
        print("data copy action completed till today!")
        return -1
    setCWD()
    # setIDXCWD()
    filename = "idx-" + str(year) + "-" + str(month) + ".csv"
    command = "jdata bhavcopy --idx -f " + \
        str(last_month_start_date) + " -t " + \
        str(last_month_end_date) + " -d idxFiles/"
    print("running command:", command)
    print("jdata run started!")
    process = subprocess.Popen(command,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    time.sleep(7)
    print("jdata run successful!")
    return 100


def generateSBINFile(year, month, day, stockname):
    last_month_start_date = datetime.date(year, month, day)
    if month == 12:
        year = year + 1
        month = 0
    last_month_end_date = datetime.date(
        year, month + 1, day) - datetime.timedelta(days=1)
    if month == 0:
        year = year - 1
        month = 12
    if last_month_end_date > datetime.datetime.today().date():
        last_month_end_date = datetime.datetime.today().date()
    if last_month_start_date > datetime.datetime.today().date():
        print("data copy action completed till today!")
        return -1
    setCWD()
    setSBINCWD()
    filename = "SBIN-" + str(year) + "-" + str(month) + ".csv"
    if os.path.exists(filename):
        os.remove(filename)
        print("File removed! :", filename)
    command = "jdata stock -s " + str(stockname) + " -f " + str(
        last_month_start_date) + " -t " + str(last_month_end_date) + " -o " + filename
    time.sleep(5)
    print("running command:", command)
    print("jdata run started!")
    process = subprocess.Popen(command,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    while not os.path.exists(filename):
        time.sleep(5)
        print("waiting for file processing to complete!")    
    time.sleep(5)
    print("jdata run successful!")
    return 100


def generateEQFile(year, month, day):
    stock_data_list = []
    last_month_start_date = datetime.date(year, month, day)
    if month == 12:
        year = year + 1
        month = 0
    last_month_end_date = datetime.date(
        year, month + 1, day) - datetime.timedelta(days=1)
    if month == 0:
        year = year - 1
        month = 12
    if last_month_end_date > datetime.datetime.today().date():
        last_month_end_date = datetime.datetime.today().date()
    if last_month_start_date > datetime.datetime.today().date():
        print("data copy action completed till today!")
        return -1
    setCWD()
    setSBINCWD()
    filename = "SBIN-" + str(year) + "-" + str(month) + ".csv"
    # command = "jdata stock -s SBIN -f " + str(last_month_start_date) + " -t " + str(last_month_end_date) + " -o " + filename
    # print("running command:", command)
    # print("jdata run started!")
    # process = subprocess.Popen(command,
    #                      shell=True,
    #                      stdout=subprocess.PIPE,
    #                      stderr=subprocess.PIPE)
    # time.sleep(7)
    # print("jdata run successful!")
    with open(filename, newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)  # Skip the header.
        # Unpack the row directly in the head of the for loop.
        for trade_date, series, open_price, high, low, prev_close, ltp, close, vwap, w52_h, w52_l, volume, value, no_of_trades, symbol in reader:
            # Convert the numbers to floats.
            prev_close = float(prev_close)
            open_price = float(open_price)
            high = float(high)
            low = float(low)
            ltp = float(ltp)
            close = float(close)
            vwap = float(vwap)
            value = float(value)
            # Now create the StockData instance and append it to the list.
            stock_data_list.append(StockData(trade_date, series, open_price, high, low,
                                             prev_close, ltp, close, vwap, w52_h, w52_l, volume, value, no_of_trades, symbol))
    # Then do something with the stock_data_list
    print("bhavcopy eq data copy started!")
    for stock_data_obj in stock_data_list:
        stock_date = stock_data_obj.trade_date
        print("copying eq data for date :", stock_date)
        datetimeobj = datetime.datetime.strptime(stock_date, "%Y-%m-%d")
        s_year = int(datetimeobj.year)
        s_month = int(datetimeobj.month)
        s_date = int(datetimeobj.day)
        # print(s_year)
        # print(s_month)
        # print(s_date)
        bhavcopy_save(date(int(s_year), int(s_month), int(s_date)),
                      CWD + '/eqFiles/')
        time.sleep(7)
    return 100


def generateFOFile(year, month, day):
    stock_data_list = []
    last_month_start_date = datetime.date(year, month, day)
    if month == 12:
        year = year + 1
        month = 0
    last_month_end_date = datetime.date(
        year, month + 1, day) - datetime.timedelta(days=1)
    if month == 0:
        year = year - 1
        month = 12
    if last_month_end_date > datetime.datetime.today().date():
        last_month_end_date = datetime.datetime.today().date()
    if last_month_start_date > datetime.datetime.today().date():
        print("data copy action completed till today!")
        return -1
    setCWD()
    setSBINCWD()
    filename = "SBIN-" + str(year) + "-" + str(month) + ".csv"
    # command = "jdata stock -s SBIN -f " + str(last_month_start_date) + " -t " + str(last_month_end_date) + " -o " + filename
    # print("running command:", command)
    # print("jdata run started!")
    # process = subprocess.Popen(command,
    #                      shell=True,
    #                      stdout=subprocess.PIPE,
    #                      stderr=subprocess.PIPE)
    # time.sleep(7)
    # print("jdata run successful!")
    with open(filename, newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)  # Skip the header.
        # Unpack the row directly in the head of the for loop.
        for trade_date, series, open_price, high, low, prev_close, ltp, close, vwap, w52_h, w52_l, volume, value, no_of_trades, symbol in reader:
            # Convert the numbers to floats.
            prev_close = float(prev_close)
            open_price = float(open_price)
            high = float(high)
            low = float(low)
            ltp = float(ltp)
            close = float(close)
            vwap = float(vwap)
            value = float(value)
            # Now create the StockData instance and append it to the list.
            stock_data_list.append(StockData(trade_date, series, open_price, high, low,
                                             prev_close, ltp, close, vwap, w52_h, w52_l, volume, value, no_of_trades, symbol))
    # Then do something with the stock_data_list
    print("bhavcopy fo data copy started!")
    for stock_data_obj in stock_data_list:
        stock_date = stock_data_obj.trade_date
        print("copying fo data for date :", stock_date)
        datetimeobj = datetime.datetime.strptime(stock_date, "%Y-%m-%d")
        s_year = int(datetimeobj.year)
        s_month = int(datetimeobj.month)
        s_date = int(datetimeobj.day)
        # print(s_year)
        # print(s_month)
        # print(s_date)
        # if s_date == 30:
        #     continue
        bhavcopy_fo_save(date(int(s_year), int(s_month), int(
            s_date)), CWD + '/foFiles/')
        time.sleep(7)
    return 100

if __name__ == "__main__":
    main(sys.argv[1:])

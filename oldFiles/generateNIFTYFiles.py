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

CWD = "/home/surya/git/customPrograms"

def setCWD():
    os.chdir(CWD)

def setIDXCWD():
    os.chdir("idxFiles/")

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
    year = 0
    month = 0
    day = 0
    start = 0
    end = 0
    try:
       opts, args = getopt.getopt(argv, "hy:m:d:s:e:", ["year=", "month=", "day=", "start=", "end="])
    except getopt.GetoptError:
       print('generateNIFTYFiles.py -y <year> -m <month> -d <day> -s <start> -e <end>')
       sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('generateNIFTYFiles.py -y <year> -m <month> -d <day> -s <start> -e <end>')
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
    print ("Year is ", year)
    print ("Month is ", month)
    print ("Day is ", day)
    print ("Start is ", start)
    print ("End is ", end)
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
    if start > 0:
        year = start
        while year <= end:
            month = 1
            while month <= 12:
                state = generateNIFTYFile(year, month, day)
                if state == -1:
                    return
                month = month + 1
            year = year + 1
    else:
        generateNIFTYFile(year, month, day)


def generateNIFTYFile(year, month, day):
    last_month_start_date = datetime.date(year, month, day)
    if month == 12:
        year = year + 1
        month = 0
    last_month_end_date = datetime.date(year, month+1, day) - datetime.timedelta(days=1)
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
    command = "jdata bhavcopy --idx -f " + str(last_month_start_date) + " -t " + str(last_month_end_date) + " -d idxFiles/"
    print("running command:", command)
    print("jdata run started!")
    process = subprocess.Popen(command,
                         shell=True,
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
    time.sleep(7)
    print("jdata run successful!")
    return 100

if __name__ == "__main__":
   main(sys.argv[1:])

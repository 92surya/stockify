import csv
import datetime
import os
import subprocess
import time
from datetime import date
from jugaad_data.nse import bhavcopy_save, bhavcopy_fo_save
import sys
import getopt

CWD = "/home/surya/git/customPrograms"

def setCWD():
    os.chdir(CWD)

def setSBINCWD():
    os.chdir("sbinFiles/")


def main(argv):
    year = 0
    month = 0
    day = 0
    start = 0
    end = 0
    try:
       opts, args = getopt.getopt(argv, "hy:m:d:s:e:", ["year=", "month=", "day=", "start=", "end="])
    except getopt.GetoptError:
       print('generateSBINFiles.py -y <year> -m <month> -d <day> -s <start> -e <end>')
       sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('generateSBINFiles.py -y <year> -m <month> -d <day> -s <start> -e <end>')
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
                state = generateSBINFile(year, month, day)
                if state == -1:
                    return
                month = month + 1
            year = year + 1
    else:
        generateSBINFile(year, month, day)

def generateSBINFile(year, month, day):
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
    setSBINCWD()
    filename = "SBIN-" + str(year) + "-" + str(month) + ".csv"
    if os.path.exists(filename):
        os.remove(filename)
        print("File removed! :",filename)
    command = "jdata stock -s SBIN -f " + str(last_month_start_date) + " -t " + str(last_month_end_date) + " -o " + filename
    time.sleep(3)
    print("running command:", command)
    print("jdata run started!")
    process = subprocess.Popen(command,
                         shell=True,
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
    time.sleep(7)
    print("jdata run successful!")

if __name__ == "__main__":
   main(sys.argv[1:])

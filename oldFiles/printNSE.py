from nsetools import Nse
from lots import lots
from stock_codes import all_stock_codes
from indexes import index_list
from Stock import Stock
from EnvProperties import EnvProperties
nse = Nse()

number_of_indexes = 0
# number_of_stocks = 0
# number_of_fno = 0

# stock_codes = []
# fno_stock_codes = []
# stock_objects = []

for i in index_list:
    number_of_indexes = number_of_indexes + 1
    

# for j in all_stock_codes:
#     number_of_stocks = number_of_stocks + 1
#     stock_codes.append(j)

# for k in lots:
#     number_of_fno = number_of_fno + 1
#     fno_stock_codes.append(k)

# for stock_code in fno_stock_codes:
#     if stock_code in stock_codes:
#         current_stock = nse.get_quote(stock_code)
#         stock_object = Stock(current_stock)
#         stock_objects.append(stock_object)

# for stock_obj in stock_objects:
#     print(stock_obj.stock_name," : ",stock_obj.current_price)

print("Number of Indexes:", number_of_indexes)
# print("Number of Stocks:", number_of_stocks)
# print("Number of F&O Stocks:", number_of_fno)
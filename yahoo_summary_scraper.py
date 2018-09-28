import requests
from bs4 import BeautifulSoup as bs
import lxml
import sys
import pprint

base_url = "https://in.finance.yahoo.com/quote/"
arguments = sys.argv[1:][0]
arguments = arguments.upper()
param = arguments+'?p='+arguments
print(base_url+param)

r = requests.get(base_url+param)
print(r.status_code)
soup = bs(r.text,'lxml')

data_points = []
for j in soup.find_all('td',class_="Ta(end) Fw(b) Lh(14px)"):
    data_points.append(j.text)

def replacer(list):
    for n, i in enumerate(list):
        if (i == "N/A" or i == "N/A (N/A)"):
            list[n] = "None"
    return list

data_points = replacer(data_points)
print(data_points)
print(len(data_points))

previous_close = data_points[0]
open = data_points[1]
bid = data_points[2]
ask = data_points[3]
days_range = data_points[4]
fiftytwo_week_range = data_points[5]
volume = data_points[6]
avg_volume = data_points[7]
market_cap = data_points[8]
beta = data_points[9]
pe_ratio = data_points[10]
eps = data_points[11]
earnings_date = data_points[12]
forward_div_yield = data_points[13]
ex_dividend_date = data_points[14]
y_target_est = data_points[15]

my_dict = {}
my_dict['previous_close'] = previous_close
my_dict['open'] =  open
my_dict['bid'] = bid
my_dict['ask'] = ask
my_dict['days_range'] = days_range
my_dict['fiftytwo_week_range'] = fiftytwo_week_range
my_dict['volume'] =volume
my_dict['avg_volume'] = avg_volume
my_dict['market_cap'] = market_cap
my_dict['beta'] = beta
my_dict['pe_ratio'] = pe_ratio
my_dict['eps'] = eps
my_dict['earnings_date'] = earnings_date
my_dict['forward_dividend_and_yield'] = forward_div_yield
my_dict['ex_dividend_date'] = ex_dividend_date
my_dict['1y_target_est'] = y_target_est

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(my_dict)

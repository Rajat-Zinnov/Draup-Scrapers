import requests
from bs4 import BeautifulSoup as bs
import lxml
import sys
import pprint

base_url = "https://in.finance.yahoo.com/quote/"
arguments = sys.argv[1:][0]
arguments = arguments.upper()
param = arguments+'/balance-sheet?p='+arguments
print(base_url+param)

r = requests.get(base_url+param)
print(r.status_code)
soup = bs(r.text,'lxml')

dates = []
for i in soup.find_all('td',class_="C($gray) Ta(end)"):
    dates.append(i.text)

balance_sheet = []
for i in soup.find_all('td',class_="Fz(s) Ta(end) Pstart(10px)"):
    balance_sheet.append(i.text)

balance_sheet_bold = []
for i in soup.find_all('td',class_="Fw(b) Fz(s) Ta(end) Pb(20px)"):
    balance_sheet_bold.append(i.text)

balance_sheet_remaining = []
for i in soup.find_all('td',class_="Fw(b) Fz(s) Ta(end)"):
    balance_sheet_remaining.append(i.text)

balance_sheet_remaining2 = []
for i in soup.find_all('td',class_="Fw(b) Fz(s) Ta(end) Py(8px)"):
    balance_sheet_remaining2.append(i.text)


# REPLACER
def replacer(list):
    for n, i in enumerate(list):
        if i == "-":
            list[n] = "None"
    return list

date = []
for i in dates:
    lis = i.split('/')
    date.append(lis[2]+'-'+lis[1]+'-'+lis[0])

#print(dates)
#print(balance_sheet)
#print(len(balance_sheet))
#print(balance_sheet_bold)
#print(len(balance_sheet_bold))
#print(balance_sheet_remaining)
#print(len(balance_sheet_remaining))
#print(balance_sheet_remaining2)
#print(len(balance_sheet_remaining2))

total_col = len(dates)
replacer(balance_sheet)
replacer(balance_sheet_bold)
replacer(balance_sheet_remaining)
replacer(balance_sheet_remaining2)

output = balance_sheet + balance_sheet_bold+balance_sheet_remaining+balance_sheet_remaining2
output = [ output[i:i+total_col] for i in range(0, len(output), total_col) ]

output.insert(5,output[32])
output.insert(13,output[30])
output.insert(17,output[35])
output.insert(23,output[33])
output.insert(33,output[35])
del output[-5:]

my_dict = {}
columns= len(output[0])
rows = len(output)

cash = []
short_term_investments = []
net_receivables = []
inventory = []
other_current_assests = []
total_current_assets = []
long_term_investments = []
property_plant = []
goodwill = []
intangible_assets = []
accumulated_amortisation = []
other_assets = []
deferred_long_term = []
total_assets = []

accounts_payable = []
short_long_term_debt = []
other_current_liabilities = []
total_current_liabilities = []
long_term_debt = []
other_liablities = []
deferred_long_term_liability = []
minority_interest = []
negative_goodwill = []
total_liabilities = []

misc_stock_options = []
redeemable_preferred_stock = []
preferred_stock = []
common_stock = []
retained_earnings = []
treasury_stock = []
capital_surplus = []
other_stockholder_equity = []
total_stockholder_equity = []
net_tangible_assets = []

for j in range(len(output)):
    for n,i in enumerate(output[j]):
        temp_dict = {}
        temp_dict['date'] = date[n]
        temp_dict['value'] = i
        if(j == 0):
            cash.append(temp_dict)
        elif(j==1):
            short_term_investments.append(temp_dict)
        elif (j == 2):
            net_receivables.append(temp_dict)
        elif (j == 3):
            inventory.append(temp_dict)
        elif (j == 4):
            other_current_assests.append(temp_dict)
        elif (j == 5):
            total_current_assets.append(temp_dict)
        elif (j == 6):
            long_term_investments.append(temp_dict)
        elif (j == 7):
            property_plant.append(temp_dict)
        elif (j == 8):
            goodwill.append(temp_dict)
        elif (j == 9):
            intangible_assets.append(temp_dict)
        elif (j == 10):
            accumulated_amortisation.append(temp_dict)
        elif (j == 11):
            other_assets.append(temp_dict)
        elif (j == 12):
            deferred_long_term.append(temp_dict)
        elif (j == 13):
            total_assets.append(temp_dict)
        elif (j == 14):
            accounts_payable.append(temp_dict)
        elif (j == 15):
            short_long_term_debt.append(temp_dict)
        elif (j == 16):
            other_current_liabilities.append(temp_dict)
        elif (j == 17):
            total_current_liabilities.append(temp_dict)
        elif (j == 18):
            long_term_debt.append(temp_dict)
        elif (j == 19):
            other_liablities.append(temp_dict)
        elif (j == 20):
            deferred_long_term_liability.append(temp_dict)
        elif (j == 21):
            minority_interest.append(temp_dict)
        elif (j == 22):
            negative_goodwill.append(temp_dict)
        elif (j == 23):
            total_liabilities.append(temp_dict)
        elif (j == 24):
            misc_stock_options.append(temp_dict)
        elif (j == 25):
            redeemable_preferred_stock.append(temp_dict)
        elif (j == 26):
            preferred_stock.append(temp_dict)
        elif (j == 27):
            common_stock.append(temp_dict)
        elif (j == 28):
            retained_earnings.append(temp_dict)
        elif (j == 29):
            treasury_stock.append(temp_dict)
        elif (j == 30):
            capital_surplus.append(temp_dict)
        elif (j == 31):
            other_stockholder_equity.append(temp_dict)
        elif (j == 32):
            total_stockholder_equity.append(temp_dict)
        elif (j == 33):
            net_tangible_assets.append(temp_dict)

current_assets = {}
current_assets['cash_and_cash_equivalents'] = cash
current_assets['short_term_investments'] = short_term_investments
current_assets['net_receivables'] = net_receivables
current_assets['inventory'] = inventory
current_assets['other_current_assets'] = other_current_assests
current_assets['total_current_assets'] = total_current_assets
current_assets['long_term_investments'] = long_term_investments
current_assets['property_plant_and_equipment '] = property_plant
current_assets['goodwill'] = goodwill
current_assets['intangible_assets'] = intangible_assets
current_assets['accumulated_amortisation'] = accumulated_amortisation
current_assets['other_assets'] = other_assets
current_assets['deferred_long_term_liability_charges'] = deferred_long_term
current_assets['total_assets'] = total_assets

current_liabilities  = {}
current_liabilities['accounts_payable'] = accounts_payable
current_liabilities['short_current_long_term_debt'] = short_long_term_debt
current_liabilities['other_current_liabilities'] = other_current_liabilities
current_liabilities['total_current_liabilities'] = total_current_liabilities
current_liabilities['long_term_debt'] = long_term_debt
current_liabilities['other_liabilities'] = other_liablities
current_liabilities['deferred_long_term_liability_charges'] = deferred_long_term_liability
current_liabilities['minority_interest'] = minority_interest
current_liabilities['negative_goodwill'] = negative_goodwill
current_liabilities['total_liabilities'] = total_liabilities

stockholders_equity = {}
stockholders_equity['misc_stock_options_warrants'] = misc_stock_options
stockholders_equity['redeemable_preferred_stock'] = redeemable_preferred_stock
stockholders_equity['preferred_stock'] = preferred_stock
stockholders_equity['common_stock'] = common_stock
stockholders_equity['retained_earnings'] = retained_earnings
stockholders_equity['treasury_stock'] = treasury_stock
stockholders_equity['capital_surplus'] = capital_surplus
stockholders_equity['other_stockholder_equity'] = other_stockholder_equity
stockholders_equity['total_stockholder_equity'] = total_stockholder_equity
stockholders_equity['net_tangible_assets'] = net_tangible_assets

balance_sheet_document = {}
balance_sheet_document['current_assets'] = current_assets
balance_sheet_document['current_liabilities'] = current_liabilities
balance_sheet_document['stockholders_equity'] = stockholders_equity

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(balance_sheet_document)

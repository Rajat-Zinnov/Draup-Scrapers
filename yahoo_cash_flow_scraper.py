import requests
from bs4 import BeautifulSoup as bs
import lxml
import sys
import pprint

base_url = "https://in.finance.yahoo.com/quote/"
arguments = sys.argv[1:][0]
arguments = arguments.upper()
param = arguments+'/cash-flow?p='+arguments
print(base_url+param)

r = requests.get(base_url+param)
print(r.status_code)
soup = bs(r.text,'lxml')

dates = []
for i in soup.find_all('td',class_="C($gray) Ta(end)"):
    dates.append(i.text)

date = []
for i in dates:
    lis = i.split('/')
    date.append(lis[2]+'-'+lis[1]+'-'+lis[0])

print(date)

cash_flow = []
for i in soup.find_all('td',class_="Fz(s) Ta(end) Pstart(10px)"):
    cash_flow.append(i.text)

cash_flow_bold = []
for i in soup.find_all('td',class_="Fw(b) Fz(s) Ta(end) Pb(20px)"):
    cash_flow_bold.append(i.text)

cash_flow_remaining = []
for i in soup.find_all('td',class_="Fz(s) Fw(b) Py(12px) Ta(end)"):
    cash_flow_remaining.append(i.text)

# REPLACER
def replacer(list):
    for n, i in enumerate(list):
        if i == "-":
            list[n] = "None"
    return list

replacer(cash_flow)
replacer(cash_flow_bold)
replacer(cash_flow_remaining)

del cash_flow_bold[:len(date)]

total_col = len(date)
#print(cash_flow)
#print(cash_flow_bold)
#print(cash_flow_remaining)
#print(len(cash_flow))
#print(len(cash_flow_bold))
#print(len(cash_flow_remaining))

output = cash_flow + cash_flow_bold+cash_flow_remaining
output = [ output[i:i+total_col] for i in range(0, len(output), total_col) ]

output.insert(6, output[14])
output.insert(10, output[16])
output.insert(15, output[18])
output.insert(17, output[20])

del output[-4:]

my_dict = {}
columns= len(output[0])
rows = len(output)


depreciation =  []
adjustments = []
changes_receivable = []
changes_liabilities = []
changes_inventory = []
changes_other = []
total_cash_flow_operating = []

capital_expenditure = []
investments = []
other_cash_flow_investment = []
total_cash_flow_investment = []

dividends_paid = []
sale_purchase = []
net_borrow = []
other_cash_flow_financial = []
total_cash_flow_financial = []
effect_exchange_rate = []
change_cash_equiv = []

for j in range(len(output)):
    for n,i in enumerate(output[j]):
        temp_dict = {}
        temp_dict['date'] = date[n]
        temp_dict['value'] = i
        if(j == 0):
            depreciation.append(temp_dict)
        elif(j==1):
            adjustments.append(temp_dict)
        elif (j == 2):
            changes_receivable.append(temp_dict)
        elif (j == 3):
            changes_liabilities.append(temp_dict)
        elif (j == 4):
            changes_inventory.append(temp_dict)
        elif (j == 5):
            changes_other.append(temp_dict)
        elif (j == 6):
            total_cash_flow_operating.append(temp_dict)
        elif (j == 7):
            capital_expenditure.append(temp_dict)
        elif (j == 8):
            investments.append(temp_dict)
        elif (j == 9):
            other_cash_flow_investment.append(temp_dict)
        elif (j == 10):
            total_cash_flow_investment.append(temp_dict)
        elif (j == 11):
            dividends_paid.append(temp_dict)
        elif (j == 12):
            sale_purchase.append(temp_dict)
        elif (j == 13):
            net_borrow.append(temp_dict)
        elif (j == 14):
            other_cash_flow_financial.append(temp_dict)
        elif (j == 15):
            total_cash_flow_financial.append(temp_dict)
        elif (j == 16):
            effect_exchange_rate.append(temp_dict)
        elif (j == 17):
            change_cash_equiv.append(temp_dict)

operating_activities = {}
operating_activities['depreciation'] = depreciation
operating_activities['adjustments_to_new_volume'] = adjustments
operating_activities['changes_in_acounts_receivable'] = changes_receivable
operating_activities['changes_in_liabilities'] = changes_liabilities
operating_activities['changes_in_inventory'] = changes_inventory
operating_activities['changes_in_others'] = changes_other
operating_activities['total_cash_flow'] = total_cash_flow_operating

investment_activities = {}
investment_activities['capital_expenditure'] = capital_expenditure
investment_activities['investments'] = investments
investment_activities['other_cash_flow'] = other_cash_flow_investment
investment_activities['total_cash_flow'] = total_cash_flow_investment

financimg_activities = {}
financimg_activities['dividends_paid'] = dividends_paid
financimg_activities['sale_purchase_of_stock'] = sale_purchase
financimg_activities['net_borrowings'] = net_borrow
financimg_activities['other_cash_flow'] = other_cash_flow_financial
financimg_activities['total_cash_flow'] = total_cash_flow_financial
financimg_activities['effect_of_exchange_rate_changes'] = effect_exchange_rate
financimg_activities['change_in_cash_and_cash_equivalents'] = change_cash_equiv

cash_flow_document = {}
cash_flow_document['operating_activities'] = operating_activities
cash_flow_document['investment_activities'] = investment_activities
cash_flow_document['financing_activities'] = financimg_activities

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(cash_flow_document)

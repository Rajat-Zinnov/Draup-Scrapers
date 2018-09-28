import requests
from bs4 import BeautifulSoup as bs
import lxml
import sys
import pprint

base_url = "https://in.finance.yahoo.com/quote/"
arguments = sys.argv[1:][0]
arguments = arguments.upper()
param = arguments+'/financials?p='+arguments
print(base_url+param)

r = requests.get(base_url+param)
print(r.status_code)
soup = bs(r.text,'lxml')

for i in soup.find_all(class_='Lh(1.7) W(100%) M(0)'):


dates = []
for i in soup.find_all('td',class_="C($gray) Ta(end)"):
    dates.append(i.text)

finance_data = []
for i in soup.find_all('td',class_="Fz(s) Ta(end) Pstart(10px)"):
    finance_data.append(i.text)

finance_data_bold = []
for i in soup.find_all('td',class_="Fw(b) Fz(s) Ta(end) Pb(20px)"):
    finance_data_bold.append(i.text)

finance_data_net_income = []
for i in soup.find_all('td',class_="Fw(b) Ta(end) Py(8px) Pt(36px)"):
    finance_data_net_income.append(i.text)

finance_data_net_income_common_shares = []
for i in soup.find_all('td',class_="Fw(b) Ta(end)"):
    finance_data_net_income_common_shares.append(i.text)

finance_data_net_income_prefer_stock = []
for i in soup.find_all('td',class_="Fz(s) Ta(end) Pstart(10px)"):
    if(i.get('data-reactid') == "212"):
        finance_data_net_income_prefer_stock.append(i.text)

date = []
for i in dates:
    lis = i.split('/')
    date.append(lis[2]+'-'+lis[1]+'-'+lis[0])

total_col = len(date)
print(date)

# REPLACER
def replacer(list):
    for n, i in enumerate(list):
        if i == "-":
            list[n] = "None"
    return list

replacer(finance_data)
replacer(finance_data_bold)
replacer(finance_data_net_income)
replacer(finance_data_net_income_common_shares)

#print(finance_data)
total_values = len(finance_data)
#print(total_values)
#print(len(finance_data_bold))
#print(len(finance_data_net_income))
#print(len(finance_data_net_income_common_shares))
#print(finance_data_bold)
#print(finance_data_net_income)

output = finance_data + finance_data_bold+finance_data_net_income+finance_data_net_income_common_shares
output = [ output[i:i+total_col] for i in range(0, len(output), total_col) ]

output.insert(2,output[17])
output.insert(8,output[19])
output.insert(15,output[21])
output.insert(20,output[23])
output.insert(21,output[25])
del output[-5:]

my_dict = {}
columns= len(output[0])
rows = len(output)

total_revenue = []
cost_revenue = []
gross_profit = []

research_dev = []
selling_gen_and_admin = []
non_recuring=[]
others = []
total_operating_expenses = []
operating_income = []

total_other_expenses = []
earnings_before_interest = []
interest_expense = []
income_before_tax = []
income_tax_expense = []
minority_interest = []
net_income_comtinuing_ops = []

discontinued_operations=[]
extraordinary_items = []
effect_changes = []
other_items = []

net_incomes = []
net_income_common_shares = []

for j in range(len(output)):
    for n,i in enumerate(output[j]):
        temp_dict = {}
        temp_dict['date'] = date[n]
        temp_dict['value'] = i
        if(j == 0):
            total_revenue.append(temp_dict)
        elif(j==1):
            cost_revenue.append(temp_dict)
        elif (j == 2):
            gross_profit.append(temp_dict)
        elif (j == 3):
            research_dev.append(temp_dict)
        elif (j == 4):
            selling_gen_and_admin.append(temp_dict)
        elif (j == 5):
            non_recuring.append(temp_dict)
        elif (j == 6):
            others.append(temp_dict)
        elif (j == 7):
            total_operating_expenses.append(temp_dict)
        elif (j == 8):
            operating_income.append(temp_dict)
        elif (j == 9):
            total_other_expenses.append(temp_dict)
        elif (j == 10):
            earnings_before_interest.append(temp_dict)
        elif (j == 11):
            interest_expense.append(temp_dict)
        elif (j == 12):
            income_before_tax.append(temp_dict)
        elif (j == 13):
            income_tax_expense.append(temp_dict)
        elif (j == 14):
            minority_interest.append(temp_dict)
        elif (j == 15):
            net_income_comtinuing_ops.append(temp_dict)
        elif (j == 16):
            discontinued_operations.append(temp_dict)
        elif (j == 17):
            extraordinary_items.append(temp_dict)
        elif (j == 18):
            effect_changes.append(temp_dict)
        elif (j == 19):
            other_items.append(temp_dict)
        elif (j == 20):
            net_incomes.append(temp_dict)
        elif (j == 21):
            net_income_common_shares.append(temp_dict)

pp = pprint.PrettyPrinter(indent=4)

#revenue = total_revenue+cost_revenue+gross_profit
#operating_expenses = research_dev+selling_gen_and_admin+non_recuring+others+total_operating_expenses+operating_income
#income_from_continuing_operations = total_other_expenses+earnings_before_interest+interest_expense+income_tax_expense+minority_interest+net_income_comtinuing_ops
#non_recuring_events = discontinued_operations+extraordinary_items+effect_changes+other_items
#net_income_head = net_income+net_income_common_shares
#pp.pprint(revenue)
#pp.pprint(operating_expenses)
#pp.pprint(income_from_continuing_operations)
#pp.pprint(non_recuring_events)
#pp.pprint(net_income_head)

revenue = {}
revenue['total_revenue'] =total_revenue
revenue['cost_of_revenue'] = cost_revenue
revenue['gross_profit'] = gross_profit

#pp.pprint(revenue)

operating_expenses = {}
operating_expenses['research_development'] = research_dev
operating_expenses['selling_general_and_administrative'] = selling_gen_and_admin
operating_expenses['non_recurring'] = non_recuring
operating_expenses['others'] = others
operating_expenses['total_operating_expenses'] = total_operating_expenses
operating_expenses['operating_income_or_loss'] = operating_income

#pp.pprint(operating_expenses)

income_from_continuing_ops = {}
income_from_continuing_ops['total_other_income'] = total_other_expenses
income_from_continuing_ops['earnings_before_interest_and_taxes'] = earnings_before_interest
income_from_continuing_ops['interest_expense'] = interest_expense
income_from_continuing_ops['income_before_tax'] = income_before_tax
income_from_continuing_ops['income_tax_expense'] = income_tax_expense
income_from_continuing_ops['minority_interest'] = minority_interest
income_from_continuing_ops['net_income_from_continuing_ops'] = net_income_comtinuing_ops

#pp.pprint(income_from_continuing_ops)

non_recuring_events = {}
non_recuring_events['discontinued_operations'] = discontinued_operations
non_recuring_events['extraordinary_items'] = extraordinary_items
non_recuring_events['effect_of_accounting_changes'] = effect_changes
non_recuring_events['other_items'] = other_items

#pp.pprint(non_recuring_events)

net_income = {}
net_income['net_income'] = net_incomes
net_income['net_income_applicable_to_common_shares'] = net_income_common_shares

#pp.pprint(net_income)

financial_document = {}
financial_document['revenue'] = revenue
financial_document['operating_expenses'] = operating_expenses
financial_document['income_from_continuing_ops'] = income_from_continuing_ops
financial_document['non_recurring_events'] = non_recuring_events
financial_document['net_income'] = net_income

pp.pprint(financial_document)
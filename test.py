import json
import pprint

output = [['1,16,92,713', '88,30,669', '67,79,511'], ['76,59,666', '60,29,901', '45,91,476'], ['40,33,047', '28,00,768', '21,88,035'], ['10,52,778', '8,52,098', '6,50,788'], ['21,41,590', '15,68,877', '12,31,421'], ['None', 'None', 'None'], ['None', 'None', 'None'], ['None', 'None', 'None'], ['8,38,679', '3,79,793', '3,05,826'], ['-1,15,154', '30,828', '-31,225'], ['7,23,525', '4,10,621', '2,74,601'], ['2,38,204', '1,50,114', '1,32,716'], ['4,85,321', '2,60,507', '1,41,885'], ['-73,608', '73,829', '19,244'], ['None', 'None', 'None'], ['5,58,929', '1,86,678', '1,22,641'], ['None', 'None', 'None'], ['None', 'None', 'None'], ['None', 'None', 'None'], ['None', 'None', 'None'], ['5,58,929', '1,86,678', '1,22,641'], ['5,58,929', '1,86,678', '1,22,641']]
date = ['31/12/2017','31/12/2016','31/12/2015']


dates = []
for i in date:
    lis = i.split('/')
    dates.append(lis[2]+'-'+lis[1]+'-'+lis[0])

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
        temp_dict['date'] = dates[n]
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
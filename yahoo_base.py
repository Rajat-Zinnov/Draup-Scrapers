import requests
from bs4 import BeautifulSoup as bs
import sys
import pprint
import re
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from datetime import datetime

base_url = "https://in.finance.yahoo.com/quote/"
arguments = sys.argv[1:][0]
arguments = arguments.upper()

income_param = arguments + '/financials?p=' + arguments
balance_param = arguments + '/balance-sheet?p=' + arguments
cash_param = arguments + '/cash-flow?p=' + arguments
ticker = arguments.upper()

print(base_url + income_param)

pp = pprint.PrettyPrinter(indent=4)
income_url = base_url + income_param
balance_url = base_url + balance_param
cash_url = base_url + cash_param

r1 = requests.get(income_url)
r2 = requests.get(balance_url)
r3 = requests.get(cash_url)

print(r1.status_code)
print(r2.status_code)
print(r3.status_code)

soup1 = bs(r1.text, 'lxml')
soup2 = bs(r2.text, 'lxml')
soup3 = bs(r3.text, 'lxml')
#
# income_rows = soup1.find_all('td')
# balance_rows = soup2.find_all('td')
# cash_rows = soup3.find_all('td')
#
# def replacer(list):
#     for n, i in enumerate(list):
#         if i == "-":
#             list[n] = "None"
#     return list
#
# company_name = soup1.find('h1').text
#
#
# #quote_market_notice = soup1.find('div',class_="C($c-fuji-grey-j) D(b) Fz(12px) Fw(n) Mstart(0)--mobpsm Mt(6px)--mobpsm").text
#
# # driver = webdriver.PhantomJS(executable_path="/home/admin/Downloads/phantomjs")
# # driver.get(income_url)
# # html = driver.execute_script("return document.documentElement.outerHTML")
# # soup = bs(html,'lxml')
# # price_details = soup.find('span', class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)").text
# # currency_details = soup.find('div',class_="C($c-fuji-grey-j) Fz(12px)").text
# # try:
# #     price_brackets = soup.find('span', class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($dataGreen)").text
# # except:
# #     price_brackets = soup.find('span',class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($dataRed)").text
# #
# # quote_market_notice = soup.find('div',id="quote-market-notice").text
# #
# # print(price_details+ ' '+price_brackets)
# # print(currency_details)
# # print(quote_market_notice)
#
# def scraper(rows):
#     dates = []
#     financial_data = []
#     for row in rows:
#         check = row.get('class')
#         try:
#             if ("C($gray)" in check and "Ta(end)" in check):
#                 dates.append(row.text)
#         except:
#             dates.append("None")
#         try:
#             if ("Ta(end)" in check):
#                 financial_data.append(row.text)
#                 financial_data = replacer(financial_data)
#         except:
#             financial_data.append("None")
#     return (dates, financial_data)
#
# (income_dates, income_data) = scraper(income_rows)
# (balance_dates, balance_data) = scraper(balance_rows)
# (cash_dates, cash_data) = scraper(cash_rows)
#
# income_total_col = len(income_dates)
# balance_total_col = len(balance_dates)
# cash_total_col = len(cash_dates)
#
# del income_data[:income_total_col]
# del balance_data[:balance_total_col]
# del cash_data[:cash_total_col]
#
# income_dates = [datetime.strptime(x, '%d/%m/%Y').strftime('%Y-%m-%d') for x in income_dates]
# balance_dates = [datetime.strptime(x, '%d/%m/%Y').strftime('%Y-%m-%d') for x in balance_dates]
# cash_dates = [datetime.strptime(x, '%d/%m/%Y').strftime('%Y-%m-%d') for x in cash_dates]
#
# income_data = [income_data[i:i + income_total_col] for i in range(0, len(income_data), income_total_col)]
# balance_data = [balance_data[i:i + balance_total_col] for i in range(0, len(balance_data), balance_total_col)]
# cash_data = [cash_data[i:i + cash_total_col] for i in range(0, len(cash_data), cash_total_col)]
#
# print(len(income_data))
# print(len(balance_data))
# print(len(cash_data))
#
# total_revenue, cost_revenue, gross_profit, research_dev, selling_gen_and_admin, non_recuring, others, total_operating_expenses, operating_income, total_other_expenses, earnings_before_interest, interest_expense, income_before_tax, income_tax_expense, minority_interest, net_income_comtinuing_ops, discontinued_operations, extraordinary_items, effect_changes, net_incomes, preferred_stock, net_income_common_shares = (
#     [] for i in range(22))
# cash, short_term_investments, net_receivables, inventory, other_current_assests, total_current_assets, long_term_investments, property_plant, goodwill, intangible_assets, accumulated_amortisation, other_assets, deferred_long_term, total_assets, accounts_payable, short_long_term_debt, other_current_liabilities, total_current_liabilities, long_term_debt, other_liablities, deferred_long_term_liability, minority_interests, negative_goodwill, total_liabilities, misc_stock_options, redeemable_preferred_stock, preferred_stocks, common_stock, retained_earnings, treasury_stock, capital_surplus, other_stockholder_equity, total_stockholder_equity, net_tangible_assets = (
#     [] for i in range(34))
# net_income_cash, depreciation, adjustments, changes_receivable, changes_liabilities, changes_inventory, changes_other, total_cash_flow_operating, capital_expenditure, investments, other_cash_flow_investment, total_cash_flow_investment, dividends_paid, sale_purchase, net_borrow, other_cash_flow_financial, total_cash_flow_financial, effect_exchange_rate, change_cash_equiv = (
#     [] for i in range(19))
#
# def dictMaker(data, dates, columns, flag):
#     for j, row in enumerate(data):
#         for col in range(columns):
#             temp_dict = {}
#             temp_dict['date'] = dates[col]
#             temp_dict['value'] = row[col]
#             if (j == 0 and flag == 0):
#                 total_revenue.append(temp_dict)
#             if (j == 0 and flag == 1):
#                 cash.append(temp_dict)
#             if (j == 0 and flag == 2):
#                 net_income_cash.append(temp_dict)
#             if (j == 1 and flag == 0):
#                 cost_revenue.append(temp_dict)
#             if (j == 1 and flag == 1):
#                 short_term_investments.append(temp_dict)
#             if (j == 1 and flag == 2):
#                 depreciation.append(temp_dict)
#             if (j == 2 and flag == 0):
#                 gross_profit.append(temp_dict)
#             if (j == 2 and flag == 1):
#                 net_receivables.append(temp_dict)
#             if (j == 2 and flag == 2):
#                 adjustments.append(temp_dict)
#             if (j == 3 and flag == 0):
#                 research_dev.append(temp_dict)
#             if (j == 3 and flag == 1):
#                 inventory.append(temp_dict)
#             if (j == 3 and flag == 2):
#                 changes_receivable.append(temp_dict)
#             if (j == 4 and flag == 0):
#                 selling_gen_and_admin.append(temp_dict)
#             if (j == 4 and flag == 1):
#                 other_current_assests.append(temp_dict)
#             if (j == 4 and flag == 2):
#                 changes_liabilities.append(temp_dict)
#             if (j == 5 and flag == 0):
#                 non_recuring.append(temp_dict)
#             if (j == 5 and flag == 1):
#                 total_current_assets.append(temp_dict)
#             if (j == 5 and flag == 2):
#                 changes_inventory.append(temp_dict)
#             if (j == 6 and flag == 0):
#                 others.append(temp_dict)
#             if (j == 6 and flag == 1):
#                 long_term_investments.append(temp_dict)
#             if (j == 6 and flag == 2):
#                 changes_other.append(temp_dict)
#             if (j == 7 and flag == 0):
#                 total_operating_expenses.append(temp_dict)
#             if (j == 7 and flag == 1):
#                 property_plant.append(temp_dict)
#             if (j == 7 and flag == 2):
#                 total_cash_flow_operating.append(temp_dict)
#             if (j == 8 and flag == 0):
#                 operating_income.append(temp_dict)
#             if (j == 8 and flag == 1):
#                 goodwill.append(temp_dict)
#             if (j == 8 and flag == 2):
#                 capital_expenditure.append(temp_dict)
#             if (j == 9 and flag == 0):
#                 total_other_expenses.append(temp_dict)
#             if (j == 9 and flag == 1):
#                 intangible_assets.append(temp_dict)
#             if (j == 9 and flag == 2):
#                 investments.append(temp_dict)
#             if (j == 10 and flag == 0):
#                 earnings_before_interest.append(temp_dict)
#             if (j == 10 and flag == 1):
#                 accumulated_amortisation.append(temp_dict)
#             if (j == 10 and flag == 2):
#                 other_cash_flow_investment.append(temp_dict)
#             if (j == 11 and flag == 0):
#                 interest_expense.append(temp_dict)
#             if (j == 11 and flag == 1):
#                 other_assets.append(temp_dict)
#             if (j == 11 and flag == 2):
#                 total_cash_flow_investment.append(temp_dict)
#             if (j == 12 and flag == 0):
#                 income_before_tax.append(temp_dict)
#             if (j == 12 and flag == 1):
#                 deferred_long_term.append(temp_dict)
#             if (j == 12 and flag == 2):
#                 dividends_paid.append(temp_dict)
#             if (j == 13 and flag == 0):
#                 income_tax_expense.append(temp_dict)
#             if (j == 13 and flag == 1):
#                 total_assets.append(temp_dict)
#             if (j == 13 and flag == 2):
#                 sale_purchase.append(temp_dict)
#             if (j == 14 and flag == 0):
#                 minority_interest.append(temp_dict)
#             if (j == 14 and flag == 1):
#                 accounts_payable.append(temp_dict)
#             if (j == 14 and flag == 2):
#                 net_borrow.append(temp_dict)
#             if (j == 15 and flag == 0):
#                 net_income_comtinuing_ops.append(temp_dict)
#             if (j == 15 and flag == 1):
#                 short_long_term_debt.append(temp_dict)
#             if (j == 15 and flag == 2):
#                 other_cash_flow_financial.append(temp_dict)
#             if (j == 16 and flag == 0):
#                 discontinued_operations.append(temp_dict)
#             if (j == 16 and flag == 1):
#                 other_current_liabilities.append(temp_dict)
#             if (j == 16 and flag == 2):
#                 total_cash_flow_financial.append(temp_dict)
#             if (j == 17 and flag == 0):
#                 extraordinary_items.append(temp_dict)
#             if (j == 17 and flag == 1):
#                 total_current_liabilities.append(temp_dict)
#             if (j == 17 and flag == 2):
#                 effect_exchange_rate.append(temp_dict)
#             if (j == 18 and flag == 0):
#                 effect_changes.append(temp_dict)
#             if (j == 18 and flag == 1):
#                 long_term_debt.append(temp_dict)
#             if (j == 18 and flag == 2):
#                 change_cash_equiv.append(temp_dict)
#             if (j == 19 and flag == 0):
#                 net_incomes.append(temp_dict)
#             if (j == 19 and flag == 1):
#                 other_liablities.append(temp_dict)
#             if (j == 20 and flag == 0):
#                 preferred_stock.append(temp_dict)
#             if (j == 20 and flag == 1):
#                 deferred_long_term_liability.append(temp_dict)
#             if (j == 21 and flag == 0):
#                 net_income_common_shares.append(temp_dict)
#             if (j == 21 and flag == 1):
#                 minority_interests.append(temp_dict)
#             if (j == 22 and flag == 1):
#                 negative_goodwill.append(temp_dict)
#             if (j == 23 and flag == 1):
#                 total_liabilities.append(temp_dict)
#             if (j == 24 and flag == 1):
#                 misc_stock_options.append(temp_dict)
#             if (j == 25 and flag == 1):
#                 redeemable_preferred_stock.append(temp_dict)
#             if (j == 26 and flag == 1):
#                 preferred_stocks.append(temp_dict)
#             if (j == 27 and flag == 1):
#                 common_stock.append(temp_dict)
#             if (j == 28 and flag == 1):
#                 retained_earnings.append(temp_dict)
#             if (j == 29 and flag == 1):
#                 treasury_stock.append(temp_dict)
#             if (j == 30 and flag == 1):
#                 capital_surplus.append(temp_dict)
#             if (j == 31 and flag == 1):
#                 other_stockholder_equity.append(temp_dict)
#             if (j == 32 and flag == 1):
#                 total_stockholder_equity.append(temp_dict)
#             if (j == 33 and flag == 1):
#                 net_tangible_assets.append(temp_dict)
#     revenue = {}
#     revenue['total_revenue'] = total_revenue
#     revenue['cost_of_revenue'] = cost_revenue
#     revenue['gross_profit'] = gross_profit
#
#     operating_expenses = {}
#     operating_expenses['research_development'] = research_dev
#     operating_expenses['selling_general_and_administrative'] = selling_gen_and_admin
#     operating_expenses['non_recurring'] = non_recuring
#     operating_expenses['others'] = others
#     operating_expenses['total_operating_expenses'] = total_operating_expenses
#     operating_expenses['operating_income_or_loss'] = operating_income
#
#     income_from_continuing_ops = {}
#     income_from_continuing_ops['total_other_income'] = total_other_expenses
#     income_from_continuing_ops['earnings_before_interest_and_taxes'] = earnings_before_interest
#     income_from_continuing_ops['interest_expense'] = interest_expense
#     income_from_continuing_ops['income_before_tax'] = income_before_tax
#     income_from_continuing_ops['income_tax_expense'] = income_tax_expense
#     income_from_continuing_ops['minority_interest'] = minority_interest
#     income_from_continuing_ops['net_income_from_continuing_ops'] = net_income_comtinuing_ops
#
#     non_recuring_events = {}
#     non_recuring_events['discontinued_operations'] = discontinued_operations
#     non_recuring_events['extraordinary_items'] = extraordinary_items
#     non_recuring_events['effect_of_accounting_changes'] = effect_changes
#
#     net_income = {}
#     net_income['net_income'] = net_incomes
#     net_income['preferred_stock_and_other_adjustments'] = preferred_stock
#     net_income['net_income_applicable_to_common_shares'] = net_income_common_shares
#
#     income_document = {}
#     income_document['revenue'] = revenue
#     income_document['operating_expenses'] = operating_expenses
#     income_document['income_from_continuing_ops'] = income_from_continuing_ops
#     income_document['non_recurring_events'] = non_recuring_events
#     income_document['net_income'] = net_income
#
#     current_assets = {}
#     current_assets['cash_and_cash_equivalents'] = cash
#     current_assets['short_term_investments'] = short_term_investments
#     current_assets['net_receivables'] = net_receivables
#     current_assets['inventory'] = inventory
#     current_assets['other_current_assets'] = other_current_assests
#     current_assets['total_current_assets'] = total_current_assets
#     current_assets['long_term_investments'] = long_term_investments
#     current_assets['property_plant_and_equipment '] = property_plant
#     current_assets['goodwill'] = goodwill
#     current_assets['intangible_assets'] = intangible_assets
#     current_assets['accumulated_amortisation'] = accumulated_amortisation
#     current_assets['other_assets'] = other_assets
#     current_assets['deferred_long_term_liability_charges'] = deferred_long_term
#     current_assets['total_assets'] = total_assets
#
#     current_liabilities = {}
#     current_liabilities['accounts_payable'] = accounts_payable
#     current_liabilities['short_current_long_term_debt'] = short_long_term_debt
#     current_liabilities['other_current_liabilities'] = other_current_liabilities
#     current_liabilities['total_current_liabilities'] = total_current_liabilities
#     current_liabilities['long_term_debt'] = long_term_debt
#     current_liabilities['other_liabilities'] = other_liablities
#     current_liabilities['deferred_long_term_liability_charges'] = deferred_long_term_liability
#     current_liabilities['minority_interest'] = minority_interests
#     current_liabilities['negative_goodwill'] = negative_goodwill
#     current_liabilities['total_liabilities'] = total_liabilities
#
#     stockholders_equity = {}
#     stockholders_equity['misc_stock_options_warrants'] = misc_stock_options
#     stockholders_equity['redeemable_preferred_stock'] = redeemable_preferred_stock
#     stockholders_equity['preferred_stock'] = preferred_stocks
#     stockholders_equity['common_stock'] = common_stock
#     stockholders_equity['retained_earnings'] = retained_earnings
#     stockholders_equity['treasury_stock'] = treasury_stock
#     stockholders_equity['capital_surplus'] = capital_surplus
#     stockholders_equity['other_stockholder_equity'] = other_stockholder_equity
#     stockholders_equity['total_stockholder_equity'] = total_stockholder_equity
#     stockholders_equity['net_tangible_assets'] = net_tangible_assets
#
#     balance_sheet_document = {}
#     balance_sheet_document['current_assets'] = current_assets
#     balance_sheet_document['current_liabilities'] = current_liabilities
#     balance_sheet_document['stockholders_equity'] = stockholders_equity
#
#     operating_activities = {}
#     operating_activities['depreciation'] = depreciation
#     operating_activities['adjustments_to_new_volume'] = adjustments
#     operating_activities['changes_in_acounts_receivable'] = changes_receivable
#     operating_activities['changes_in_liabilities'] = changes_liabilities
#     operating_activities['changes_in_inventory'] = changes_inventory
#     operating_activities['changes_in_others'] = changes_other
#     operating_activities['total_cash_flow'] = total_cash_flow_operating
#
#     investment_activities = {}
#     investment_activities['capital_expenditure'] = capital_expenditure
#     investment_activities['investments'] = investments
#     investment_activities['other_cash_flow'] = other_cash_flow_investment
#     investment_activities['total_cash_flow'] = total_cash_flow_investment
#
#     financimg_activities = {}
#     financimg_activities['dividends_paid'] = dividends_paid
#     financimg_activities['sale_purchase_of_stock'] = sale_purchase
#     financimg_activities['net_borrowings'] = net_borrow
#     financimg_activities['other_cash_flow'] = other_cash_flow_financial
#     financimg_activities['total_cash_flow'] = total_cash_flow_financial
#     financimg_activities['effect_of_exchange_rate_changes'] = effect_exchange_rate
#     financimg_activities['change_in_cash_and_cash_equivalents'] = change_cash_equiv
#
#     cash_flow_document = {}
#     cash_flow_document['operating_activities'] = operating_activities
#     cash_flow_document['investment_activities'] = investment_activities
#     cash_flow_document['financial_activities'] = financimg_activities
#
#     if (flag == 0):
#         return income_document
#     elif (flag == 1):
#         return balance_sheet_document
#     elif (flag == 2):
#         return cash_flow_document
#     else:
#         return None
# #
# # global currency_details
# # spans = soup1.find_all('div')
# # for i in spans:
# #     checks = i.get('class')
# #     if(checks is None):
# #         continue
# #     if("C($c-fuji-grey-j)" in checks and "Fz(12px)" in checks):
# #         currency_details = i.text

soup_script = soup1.find("script", text=re.compile("root.App.main")).text
json_script = json.loads(re.search("root.App.main\s+=\s+(\{.*\})", soup_script)[1])
fin_data = json_script['context']['dispatcher']['stores']['QuoteSummaryStore']
time = json_script['context']['dispatcher']['stores']['StreamDataStore']['quoteData'][ticker.upper()]['regularMarketTime']['fmt']
regular_val = fin_data['price']['regularMarketPrice']['fmt']
change = fin_data['price']['regularMarketChange']['fmt']
percent_change = fin_data['price']['regularMarketChangePercent']['fmt']
currency = fin_data['price']['currency']
exchange_name = fin_data['price']['exchangeName']
market_source = fin_data['price']['regularMarketSource']
details = json_script['context']['dispatcher']['stores']['LangStore']['baseLangs']['react-finance'][market_source]
#quote_source_name = json_script['context']['dispatcher']['stores']['StreamDataStore']['quoteData'][ticker.upper()]['quoteSourceName']
if(change[0] != '-'):
    change = '+{0}'.format(change)
price_details = '{0} {1} ({2})'.format(regular_val,change,percent_change)
quote_market_notice = 'At close: {0}'.format(time)
currency_details = '{0} - {1} {2}. Currency in {3}'.format(exchange_name,exchange_name,details,currency)

# currency_details= ''
# if('Delayed' in quote_source_name):
#     currency_details = '{0} - {1} Delayed Price. Currency in {2}'.format(exchange_name, exchange_name, currency)
# elif('Realtime' in quote_source_name):
#     currency_details = '{0} - {1} Real Time Price. Currency in {2}'.format(exchange_name, exchange_name, currency)
# elif('CryptoCompare' in quote_source_name):
#     currency_details = '{0} - CryptoCompare. Currency in {1}'.format(exchange_name, currency)
# print(currency_details)
print(price_details)
print(quote_market_notice)
print(currency_details)

def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def convertJSON(j):
    out = {}
    for k in j:
        newK = convert(k)
        if isinstance(j[k], dict):
            out[newK] = convertJSON(j[k])
        elif isinstance(j[k], list):
            out[newK] = convertArray(j[k])
        else:
            out[newK] = j[k]
    return out

def convertArray(a):
    newArr = []
    for i in a:
        if isinstance(i, list):
            newArr.append(convertArray(i))
        elif isinstance(i, dict):
            newArr.append(convertJSON(i))
        else:
            newArr.append(i)
    return newArr

income_qtrs = fin_data['incomeStatementHistoryQuarterly']['incomeStatementHistory']
cash_qtrs = fin_data['cashflowStatementHistoryQuarterly']['cashflowStatements']
balance_qtrs = fin_data['balanceSheetHistoryQuarterly']['balanceSheetStatements']

income_qtrs = convertArray(income_qtrs)
cash_qtrs = convertArray(cash_qtrs)
balance_qtrs = convertArray(balance_qtrs)

income_document = dictMaker(income_data, income_dates, income_total_col, 0)
balance_sheet_document = dictMaker(balance_data, balance_dates, balance_total_col, 1)
cash_flow_document = dictMaker(cash_data, cash_dates, cash_total_col, 2)

# pp.pprint(income_document)
# pp.pprint(balance_sheet_document)
# pp.pprint(cash_flow_document)

data = {}
data['income_statement'] = income_document
data['income_statement_quarterly'] = income_qtrs
data['balance_sheet'] = balance_sheet_document
data['balance_sheet_quarterly'] = balance_qtrs
data['cash_flow'] = cash_flow_document
data['cash_flow_quarterly'] = cash_qtrs

yahoo_financials = {}
yahoo_financials['ticker_symbol'] = ticker
yahoo_financials['company_name'] = company_name
yahoo_financials['yahoo_financial_link'] = income_url
yahoo_financials['data'] = data
yahoo_financials['created_at'] = datetime.now()



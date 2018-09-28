import requests
from bs4 import BeautifulSoup as bs
import pprint
from datetime import datetime

pp = pprint.PrettyPrinter()
url = 'http://www.4-traders.com/MICROSOFT-CORPORATION-4835/company'
htmlBody = requests.get(url)

soup = bs(htmlBody.content,'lxml')
summary = soup.find('div',class_='std_txt').text
all_tds = soup.find_all('td')

n_employees = ''
for i in all_tds:
    if i.get('class') is None:
        continue
    if('std_txt' in i.get('class') and 'th_inner' in i.get('class') and 'Number of employees' in i.text):
        q = i.text
        n_employees = q.split('Number of employees :')[1].strip()

tables = soup.find_all('table', class_='tabElemNoBor overfH fvtDiv')
spr,spb,man,eq,shares,hold = [],[],[],[],[],[]
spr_list = []
for t in tables:
    check = t.find_all('table')
    data_check = t.find_all('td')
    for i in data_check:
        if ('Sales per Businesses' in check[0].text):
            spr.append(i.text)
        elif ('Sales per Regions' in check[0].text):
            spb.append(i.text)
        elif ('Managers' in check[0].text):
            man.append(i.text)
        elif ('Equities' in check[0].text):
            eq.append(i.text)
        elif ('Shareholders' in check[0].text):
            shares.append(i.text)
        elif ('Holdings' in check[0].text):
            hold.append(i.text)

salesPerReg = []
del spr[0:4]
spr_iter =  [tuple(spr[7:][i:i+6]) for i in range(0, len(spr[7:]), 6)]
for n,dat in enumerate(spr_iter):
    main = {}
    temp1,temp2 = {},{}
    temp1['year'] = spr[0]
    temp1['currencySymbol'] = spr[3]
    temp1['currencyValue'] = dat[1]
    temp1['percentageSymbol'] = spr[4]
    temp1['percentageValue'] = dat[2]
    temp2['year'] = spr[1]
    temp2['currencySymbol'] = spr[3]
    temp2['currencyValue'] = dat[3]
    temp2['percentageSymbol'] = spr[4]
    temp2['percentageValue'] = dat[4]
    main['DomainName'] = dat[0]
    main['DeltaValue'] = dat[5]
    main['data'] = []
    main['data'].append(temp1)
    main['data'].append(temp2)
    salesPerReg.append(main)

salesPerBuz = []
del spb[0:4]
spb_iter =  [tuple(spb[7:][i:i+6]) for i in range(0, len(spb[7:]), 6)]
for n,dat in enumerate(spb_iter):
    main = {}
    temp1,temp2 = {},{}
    temp1['year'] = spb[0]
    temp1['currencySymbol'] = spb[3]
    temp1['currencyValue'] = dat[1]
    temp1['percentageSymbol'] = spb[4]
    temp1['percentageValue'] = dat[2]
    temp2['year'] = spb[1]
    temp2['currencySymbol'] = spb[3]
    temp2['currencyValue'] = dat[3]
    temp2['percentageSymbol'] = spb[4]
    temp2['percentageValue'] = dat[4]
    main['DomainName'] = dat[0]
    main['DeltaValue'] = dat[5]
    main['data'] = []
    main['data'].append(temp1)
    main['data'].append(temp2)
    salesPerBuz.append(main)

del man[0:3]
man_iter = [tuple(man[4:][i:i+4]) for i in range(0, len(man[4:]), 4)]

managers = []
for m in man_iter:
    temp= {}
    temp['name'] = m[0]
    temp['age'] = m[1]
    temp['since'] = m[2]
    temp['title'] = m[3]
    managers.append(temp)

del eq[:10]
eq_iter = [tuple(eq[i:i+8]) for i in range(0, len(eq), 8)]
equity = []
for e in eq_iter:
    temp = {}
    temp['share'] = e[0]
    temp['vote'] = e[1]
    temp['quantity'] = e[2]
    temp['floatValue'] = e[3]
    temp['floatPercent'] = e[4]
    temp['companyOwnedSharesValue'] = e[5]
    temp['companyOwnedSharesPercent'] = e[6]
    temp['totalFloat'] = e[7]
    equity.append(temp)

del shares[:4]
share_iter = [tuple(shares[3:][i:i+3]) for i in range(0, len(shares[3:]), 3)]
shareholders = []
for s in share_iter:
    temp = {}
    temp['name'] = s[0]
    temp['equities'] = s[1]
    temp['percent'] = s[2]
    shareholders.append(temp)

del hold[:7]
hold_iter = [tuple(hold[i:i+4]) for i in range(0, len(hold), 4)]
holdings = []
for h in hold_iter:
    temp = {}
    temp['name'] = h[0]
    temp['equities'] = h[1]
    temp['percent'] =  h[2]
    temp['valuation'] = h[3]
    holdings.append(temp)

sec = []
tab_sec = soup.find_all('table',class_='tabSector')
print(tab_sec)
for i in tab_sec:
    print(i.find_all('tr'))
    sec.append(i.find_all('tr'))
print(sec)
sectors = []
for i in sec[0]:
    sectors.append(i.text)

mark = soup.find_all('table',class_='std_txt')
market = mark[0].text.strip()
market = market[1:].replace('-',',')
stock = mark[1].text.strip()
# stock = stock[1:].replace('-',',')
contact = soup.find('div',class_='linkTabBl').text

company_name = soup.find('td',class_='fvTitle').text.strip()
pp.pprint(salesPerBuz)
company = {}
company['summary'] = summary
company['noOfEmployees'] = n_employees
company['name'] = company_name
company['salesPerBusinesses'] = salesPerBuz
company['salesPerRegions'] = salesPerReg
company['managers'] = managers
company['equities'] = equity
company['holdings'] = holdings
company['marketAndIndexes'] = market
company['stockExchangeCodes'] = stock
company['companyContactInformation'] = contact
company['sector'] = sectors
fourtraders_dict = {}
fourtraders_dict['company_name'] = company_name
fourtraders_dict['company'] = company
fourtraders_dict['created_at'] = datetime.now()
fourtraders_dict['updated_at'] = datetime.now()

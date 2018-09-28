import tldextract as tld
import requests
import json


ext = tld.extract('www.sgsits.ac.in')
owler_input = '{0}.{1}'.format(ext.domain,ext.suffix)
print(owler_input)
headers = {
    'user_key': 'c6d8482f8f2c7ecdf47371f65407ef3c',
}

params = (
    ('q', owler_input),
    ('fields', 'name,website,ticker'),
    ('limit', '10'),
    ('format', 'json'),
)

response = requests.get('https://api.owler.com/v1/company/basicsearch', headers=headers, params=params)

my_dict = response.json()

print(my_dict['company'][0]['company_id'])
print(my_dict['feeds']['pagination_id'])
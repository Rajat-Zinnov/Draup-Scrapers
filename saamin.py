from bs4 import BeautifulSoup as bs
import requests
from textblob import TextBlob
import re

headers = {
    'Origin': 'http://www.saramin.co.kr',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'text/html, */*; q=0.01',
    'Referer': 'http://www.saramin.co.kr/zf_user/jobs/relay/view?view_type=search&rec_idx=34133245&isMypage=no&gz=1&recommend_ids=eJxNkLsVAzEIBKtxDizf2IWo%2Fy585ycJwmFWgIBKMEyXVX7ii4FL%2FwVkwPP6xuufPA9%2FsD1nTL%2FxeinS4Q9uLyZJtMx5e31qva5CpK1wgLLD5iAfGKXWYRc3vkhiWTiIIgdGKxYab%2BHsEo3FZu9VbC%2FpWWNuohTji0Txnsh%2B0UlTgg%3D%3D&t_ref=search&t_ref_content=generic&searchword=data+scientist&paid_fl=n',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

data = [
  ('rec_idx', '34035073'),
  ('seq', '0'),
  ('isPopup', 'no'),
  ('view_type', 'search'),
  ('utm_source', ''),
  ('utm_medium', ''),
  ('utm_term', ''),
  ('t_ref', 'search'),
  ('t_ref_content', 'generic'),
  ('t_ref_scnid', ''),
  ('refer', ''),
  ('searchType', ''),
  ('searchword', 'java developer'),
  ('ref_dp', 'SRI_050_VIEW_MTRX_RCT_NOINFO'),
  ('dpId', ''),
]

response = requests.post('http://www.saramin.co.kr/zf_user/jobs/relay/view-ajax', headers=headers, data=data)
soup2 = bs(response.content,'lxml')
responsibility = ''
elig = ''
work_cond = ''
comp_info = ''
desc_cards = soup2.find('div',class_='view_summary').find_all('div',class_='summary')
for desc in desc_cards:
    checker = desc.find('strong',class_='tit_info').text
    # print(checker)
    if '담당업무' in checker:
        responsibility = desc.find('ul').text
    elif '지원자격' in checker:
        elig = desc.find('ul').text
    elif '근무조건' in checker:
        work_cond = desc.find('ul').text
    elif '기업정보' in checker:
        comp_info = desc.find('dl').text
    else:
        print('Not found')
summary = {}
summary['responsibilities'] = responsibility
summary['eligibility'] = elig
summary['working_conditions'] = work_cond
summary['company_info'] = comp_info
# print(len(desc_cards))
# print(desc_cards[0].text)
# print(desc_cards[1].text)
# print(desc_cards[2].text)
# print(desc_cards[3].text)

info_rec  = soup2.find('div',class_='info_recruit').text.split('|')
del info_rec[-1]

hits = ''
n_app = ''
views = ''
n_scraps = ''
is_form_down = ''
for info in info_rec:
    if '조회수' in info:
        hits = re.findall('\d+',info)[0]
    elif '스크랩수' in info:
        n_scraps = re.findall('\d+', info)[0]
    elif '지원자수' in info:
        n_app = re.findall('\d+', info)[0]
    elif '자사양식 다운수' in info:
        is_form_down = re.findall('\d+', info)[0]
    else:
        print('info not found')

info_recruits = {}
info_recruits['hits'] = hits
info_recruits['no_applicants'] = n_app
info_recruits['no_scraps'] = n_scraps
info_recruits['views'] = views
info_recruits['is_form_down'] = is_form_down
# print(soup2.find('table',class_='table_summary'))
# print(hits)
# print(n_app)
# print(n_scraps)
# print(is_form_down)
print(summary)
print(info_recruits)
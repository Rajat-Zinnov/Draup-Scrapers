import requests
from bs4 import BeautifulSoup as bs

cookies = {
    '_ga': 'GA1.3.356452706.1533039107',
    '_gid': 'GA1.3.96463390.1533039107',
    '__gads': 'ID=614a433b7c35887d:T=1533039107:S=ALNI_MaL-BUJCNI8T1EQD865VZLp_ZyWng',
    'PCID': '15330391081118526570651',
    'talent_search_mode': 'tab',
    'talent_search': '%7B%22talent_starter_layer%22%3A%7B%22value%22%3A%22invisible%22%2C%22expires%22%3A1533206485818%7D%7D',
    'talent_search_last_panel_id': 'job-category',
    'PHPSESSID': 'ebf2ov80jfv2j0hh16nap2aruh7pbu61',
    '_gat': '1',
    '_gat_saraminTracker': '1',
    '_gat_saraminTracker2': '1',
    'wcs_bt': 's_1d3a45fb0bfe:1533189693',
    'RSRVID': 'web30|W2KeQ|W2KeI',
}

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
  ('rec_idx', '34133245'),
  ('seq', '1'),
  ('isPopup', 'no'),
  ('view_type', 'search'),
  ('utm_source', ''),
  ('utm_medium', ''),
  ('utm_term', ''),
  ('t_ref', 'search'),
  ('t_ref_content', 'generic'),
  ('t_ref_scnid', '598'),
  ('refer', ''),
  ('searchType', ''),
  ('searchword', 'data scientist'),
  ('ref_dp', 'SRI_050_VIEW_MTRX_RCT_NOINFO'),
  ('dpId', ''),
]

response = requests.post('http://www.saramin.co.kr/zf_user/jobs/relay/view-ajax', headers=headers, cookies=cookies, data=data)

# print(response.content)

soup = bs(response.content,'lxml')
print(soup.find('div',class_='info_recruit').text)

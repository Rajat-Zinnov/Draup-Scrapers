import requests
from datetime import datetime
from urllib.request import Request, urlopen, HTTPError
import os
import json
import re
import json
import sys
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from flask import jsonify
import os
import sys
import linecache
import ssl
import requests
from bs4 import BeautifulSoup
import time
import random
import requests
from datetime import datetime
import random
import inspect
import logging
import re
#
# # # some common recipies
# # redis_url = os.getenv("REDISTOGO_URL", "redis://localhost:6379")
# # path_to_gecko = os.getenv("PATH_TO_GECKODRIVER", "/home/admin/Downloads/geckodriver")
# # CRUNCHBASE_KEY = "5ed0c56cf31fc9d4cb7460006208c18e"
# # CRUNCHBASE_ORG_RELATION = ["founders", "featured_team", "current_team", "past_team", "board_members_and_advisors", "investors", "sub_organizations", "products", "customers", "competitors", "funding_rounds", "investments", "acquisitions", "funds" ]
# # CRUNCHBASE_PEOPLE_RELATION = ["primary_affiliation", "jobs", "advisory_roles", "founded_companies", "investments"]
# # #https://api.crunchbase.com/v3.1/categories?user_key=5ed0c56cf31fc9d4cb7460006208c18e
# #
# # # mongodb://harvester:4UrBPaxz4Bidt9hm@cluster0-shard-00-00-i7t2t.mongodb.net:37017/admin?readPreference=primary&ssl=true
# # mongo_url = os.getenv("ATLAS_MONGO", "mongodb://localhost:27017/harvests")
# # mongo_p_url = os.getenv("MONGO_P", "mongodb://localhost:27017/harvests")
# # print("Mongo URL is {0}".format(mongo_url))
# # mongo_conn = MongoClient(mongo_url, connect=False, ssl_cert_reqs=ssl.CERT_NONE)
# # mongo_p_conn = MongoClient(mongo_p_url, connect=False)
# #
# # config_name = os.getenv("FLASK_CONFIGURATION", "default")
# # path_to_phantom = os.getenv("PATH_TO_PHANTOMJS", "/home/admin/Downloads/phantomjs")

desktop_agents = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
                 "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
                 "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
                 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
                 "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
                 "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"]

proxies = {
    "http": "http://35.173.16.12:8888/?noconnect",
    "https":"http://35.173.16.12:8888/?noconnect"
}

GOOGLE_COUNTRY_NAMES = [{"code":"AU","country":"Australia"},
{"code":"CA","country":"Canada"},
{"code":"CN","country":"China"},
{"code":"FI","country":"Finland"},
{"code":"FR","country":"France"},
{"code":"DE","country":"Germany"},
{"code":"HK","country":"Hong Kong"},
{"code":"IN","country":"India"},
{"code":"IL","country":"Israel"},
{"code":"JP","country":"Japan"},
{"code":"KR","country":"Korea"},
{"code":"RU","country":"Russia"},
{"code":"SG","country":"Singapore"},
{"code":"ZA","country":"South Africa"},
{"code":"UK","country":"United Kingdom"},
{"code":"US","country":"United States"}]

INDEED_COUNTRY_CODES = ["aq","ar","au","at","bh","be","br","ca","cl","cn","co","cr","cz","dk","ec","eg","fi","fr","de","gr","hk","hu","in","id","ie","il","it","jp","kw","lu","my","mx","ma","nl","nz","ng","no","om","pk","pa","pe","ph","pl","pt","qa","ro","ru","sa","sg","za","kr","es","se","ch","tw","th","tr","ua","ae","gb","us","uy","ve","vn"]

def fullname(o, args=[]):
    return o.__module__ + "." + o.__name__ + "(" + ",".join(args) + ")"

def proxied_request(url, extra_headers={}, params={}):
    headers = {
        "User-Agent":random.choice(desktop_agents),
        "Accept": ("text/html,application/xhtml+xml,application/xml;"
                   "q=0.9,*/*;q=0.8"),
        "Accept-Language": "en-US,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    headers.update(extra_headers)

    # if url.startswith("http://"):
    #     p = proxies("http")
    # else:
    #     p = proxies("https")

    resp = requests.get(url, headers=headers, proxies=proxies, params=params)
    return resp

#
# def check_queue(q,funct_to_queue, qname):
#     print("Function to be queued {0}, {1}".format(datetime.now(), funct_to_queue))
#     queued_job_ids = q.get_job_ids()
#     print("Queued JOB ids {0}".format(queued_job_ids))
#
#     registry = StartedJobRegistry(qname, connection=conn)
#     running_job_ids = registry.get_job_ids()
#     print("Running JOB ids {0}".format(running_job_ids))
#
#     already_queued = False
#
#     if funct_to_queue in queued_job_ids or funct_to_queue in running_job_ids:
#         already_queued = True
#         print("if check queue {0},{1},{2}, {3}".format(qname, funct_to_queue, running_job_ids, queued_job_ids))
#     else:
#         print("else check queue {0},{1},{2}, {3}".format(qname, funct_to_queue, running_job_ids, queued_job_ids))
#
#     return already_queued
#
# def whoami():
#     frame = inspect.currentframe()
#     return inspect.getframeinfo(frame).function
#
#
# def logme2db(fullname,type,message):
#     db = mongo_conn["harvests"]
#     log_dict = {}
#     log_dict["fullname"] = fullname
#     log_dict["type"] = type
#     log_dict["message"] = message
#     log_dict["created_at"] = datetime.now()
#
#     db["log_testing"].insert(log_dict)
#
# def logger_name(name):
#     logging.basicConfig(level=logging.INFO)
#     logger = logging.getLogger(name)
#     if("default" in config_name):
#         mon = MongoHandler(host="localhost", database_name="app_logs", collection="harvester_logs", capped=True)
#     else:
#         mon = MongoHandler(host="13.126.145.104", port=27017, username="superAdmin", password="QmMAhHLRQuaTeY9v", authentication_db="admin", database_name="app_logs", collection="harvester_logs", capped=True)
#     logger.addHandler(mon)
#
#     return logger
#
# def serial(dct):
#     for k in dct:
#         if isinstance(dct[k], ObjectId):
#             dct[k] = str(dct[k])
#     return dct
#
# def cursor_to_dict(q):
#     data = [serial(item) for item in q]
#
#     return data
#
# def phantomic_request(url):
#     driver = webdriver.PhantomJS(executable_path=path_to_phantom)
#     driver.get(url)
#     htmlBody = driver.execute_script("return document.documentElement.outerHTML")
#     soupy = BeautifulSoup(htmlBody,"lxml")
#     return soupy
#
# # def chromic_request(url):
# #     path = "/home/admin/Downloads/chromedriver" #PATH ON LOCAL
# #     os.environ["webdriver.chrome.driver"] = path
# #     display =Display(visible=0, size=(800,600))
# #     display.start()
# #     br = webdriver.Chrome(path)
# #     sauce = br.get(url)
# #
# #     return sauce
#
# # def firefoxic_virtualhead_request(url,class_name,tag_name=None,id_name=None,delay=5,flag=0):
# #     display = Display(visible=0, size=(800, 600))
# #     display.start()
# #     browser = webdriver.Firefox(executable_path=path_to_gecko)
# #     browser.get(url)
# #     try:
# #         wait = WebDriverWait(browser, delay)
# #         if(flag == 0):
# #             wait.until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
# #         elif(flag == 1):
# #             wait.until(EC.visibility_of_element_located((By.TAG_NAME, tag_name)))
# #         elif(flag == 2):
# #             wait.until(EC.visibility_of_element_located((By.ID, id_name)))
# #     except TimeoutException:
# #         print("page not loaded")
# #     finally:
# #         browser.quit()
# #         display.stop()
# #     htmlBody = browser.execute_script("return document.documentElement.outerHTML")
# #
# #     return htmlBody
#
# def Noner(list):
#     for n, i in enumerate(list):
#         if i == "-":
#             list[n] = "None"
#     return list
#
# def ExtraLoggers():
#     exc_type, exc_obj, tb = sys.exc_info()
#     f = tb.tb_frame
#     lineno = tb.tb_lineno
#     filename = f.f_code.co_filename
#     linecache.checkcache(filename)
#     line = linecache.getline(filename, lineno, f.f_globals)
#     return "EXCEPTION IN ({}, LINE {} {}): {}".format(filename, lineno, line.strip(), exc_obj)
#
# def fetch_results(search_term, number_results, language_code):
#     assert isinstance(search_term, str), "Search term must be a string"
#     assert isinstance(number_results, int), "Number of results must be an integer"
#     escaped_search_term = search_term.replace(" ", "+")
#
#     google_url = "https://www.google.com/search?q={}&num={}&hl={}".format(escaped_search_term, number_results, language_code)
#     response = proxied_request(google_url)
#     response.raise_for_status()
#
#     return search_term, response.text
#
#
# def parse_results(html, keyword):
#     soup = BeautifulSoup(html, "html.parser")
#     found_results = []
#     rank = 1
#     result_block = soup.find_all("div", attrs={"class": "g"})
#     for result in result_block:
#         link = result.find("a", href=True)
#         title = result.find("h3", attrs={"class": "r"})
#         description = result.find("span", attrs={"class": "st"})
#         if link and title:
#             link = link["href"]
#             title = title.get_text()
#             if description:
#                 description = description.get_text()
#             if link != "#":
#                 found_results.append({"keyword": keyword, "rank": rank, "title": title, "description": description, "link": link})
#                 rank += 1
#     return found_results
#
#
# def scrape_google(search_term, number_results, language_code):
#     try:
#         keyword, html = fetch_results(search_term, number_results, language_code)
#         results = parse_results(html, keyword)
#         return results
#     except AssertionError:
#         raise Exception("Incorrect arguments parsed to function")
#     except requests.HTTPError:
#         raise Exception("You appear to have been blocked by Google")
#     except requests.RequestException:
#         raise Exception("Appears to be an issue with your connection")
#
# def scrape_it(keyword):
#     data = []
#     try:
#         results = scrape_google(keyword, 10, "en")
#         for result in results:
#             data.append(result)
#     except Exception as e:
#         print(e)
#     return data
#
#
# # headers = {"content-type": "application/json"}
# # r = requests.get("https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite", headers=headers)
# # print(r.status_code)
# #
# # raw_page = r.text
# # try:
# #     page_dic = json.loads(raw_page)
# # except:
# #     print (sys.exc_info())
#
# # def extract_key(elem, key):
# #     if isinstance(elem, dict):
# #         if key in elem:
# #             return elem[key]
# #         for k in elem:
# #             item = extract_key(elem[k], key)
# #             if item is not None:
# #                 return item
# #     elif isinstance(elem, list):
# #         for k in elem:
# #             item = extract_key(k, key)
# #             if item is not None:
# #                 return item
# #     return None
# #
# def get_request_to_dic(link):
#     req = Request(link)
#     req.add_header("Accept", "application/json,application/xml")
#     try:
#         raw_page = urlopen(req).read().decode()
#         page_dic = json.loads(raw_page)
#     except HTTPError as err:
#         print("HTTPError", err.code)
#         page_dic = {}
#     return page_dic
# #
# # results = get_request_to_dic("https://oracle.taleo.net/careersection/2/jobsearch.ftl#")
# # print(results)
#
# # listitem_iterator = results["body"]["children"][0]["children"][0]["listItems"]
# # print(len(listitem_iterator))
# # # for n,card in enumerate(listitem_iterator):
# # #     title = listitem_iterator[n]["title"]["instances"][0]["text"]
# # #     location = listitem_iterator[n]["subtitles"][0]["instances"][0]["text"]
# # #     jr = listitem_iterator[n]["subtitles"][1]["instances"][0]["text"]
# # #     post = listitem_iterator[n]["subtitles"][2]["instances"][0]["text"]
# # #     title_url = listitem_iterator[n]["title"]["commandLink"]
# # #     rtps://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite".split(".com")[0] + ".com"
# # # pagination_key = "Pagination"
# # # for end_point in end_points:
# # #     if end_point["type"] == pagination_key:
# # #         pagination_end_point += end_point["uri"] + "/"
# # #         break
# # # job_postings = []
# # # while True:
# # #     postings_list = extract_key(results, "listItems")
# # #     if postings_list is None:
# # #         break
# # #     paginated_urls = [JobPosting(post, base_url) for post in postings_list]
# # #     job_postings += paginated_urls
# # #     postings_page_dic = get_request_to_dic(pagination_end_point + str(len(job_postings)))
# # #
# # # print(pagination_end_point)esults2 = get_request_to_dic("https://nvidia.wd5.myworkdayjobs.com{0}".format(title_url))
# # #     description = extract_key(results2, "description")
# # #     temp = {}
# # #     temp["title"] = title
# # #     temp["location"] = location
# # #     temp["jr"] = jr
# # #     temp["post"] = post
# # #     temp["title_url"] = title_url
# # #     temp["description"] = description
# # #     newArr.append(temp)
# #
# # pagination_end_point = "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite"
# # end_points = extract_key(results, "endPoints")
# # base_url = "ht
# #
# # res = get_request_to_dic("https://api.mktg.workday.com/v1/solr/uk1?requestType=search&api=customer&rows=96&start=1056")
# # print(res["docs"]["ungrouped"])
#
#
# # res = requests.post("https://oracle.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=101430233")
# #
# # print(res.content)
# #
# # res = requests.get("https://www.indiainfoline.com/article/news-top-story/inox-in-talks-to-acquire-satyam-cineplexes-114070100131_1.html")
# # soup = bs(res.content, "lxml")
# #
# # print(soup.find("p", class_="gray_txt").text)
# #
# # def phantomic_request(url):
# #     driver = webdriver.PhantomJS(executable_path="/home/admin/Downloads/phantomjs")
# #     driver.get(url)
# #     htmlBody = driver.execute_script("return document.documentElement.outerHTML")
# #     return htmlBody
# #
# # soup = phantomic_request(url="https://www.indiainfoline.com/article/news-top-story/inox-in-talks-to-acquire-satyam-cineplexes-114070100131_1.html")
# # sauce = bs(soup, "lxml")
# # print(sauce.find("span", class_=" fs14e current_publishDate").text)
#
#
# cookies = {
#     "locale": "en",
#     "JSESSIONID": "i1-ia-MlEKnicsVqKXk7IpBKWB4tO3IayDyddN7plfgEbzIZT9he!83557411",
#     "__atuvc": "7%7C28%2C3%7C29",
#     "__atuvs": "5b4c655c4956d596002",
# }
#
# headers = {
#     "Connection": "keep-alive",
#     "Pragma": "no-cache",
#     "Cache-Control": "no-cache",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
#     "Accept": "application/json, text/javascript, */*; q=0.01",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
#     "Referer": "https://oracle.taleo.net/careersection/2/jobsearch.ftl",
#     "authority": "s7.addthis.com",
#     "pragma": "no-cache",
#     "cache-control": "no-cache",
#     "upgrade-insecure-requests": "1",
#     "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "referer": "https://oracle.taleo.net/careersection/2/jobsearch.ftl",
#     "accept-encoding": "gzip, deflate, br",
#     "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
#     "cookie": "uid=5b1a1d06a1028ced; mus=0; na_id=2018060708102413668947223330; bku=jzA99snt1a+57fQ0; na_tc=T; loc=MDAwMDBBU0lOS0ExOTMxMjU3NjAwNDAwMDBDSA==; ouid=5b486fb2000135fc988738e73da952e15aec7bc28ebb361d3808; uvc=4%7C25%2C4%7C26%2C4%7C27%2C9%7C28%2C2%7C29",
#     "Origin": "https://oracle.taleo.net",
#     "X-Requested-With": "XMLHttpRequest",
#     "tz": "GMT+05:30",
#     "Content-Type": "application/json",
# }
#
# # data = """{"multilineEnabled":true,"sortingSelection":{"sortBySelectionParam":"3","ascendingSortingOrder":"false"},"fieldData":{"fields":{"KEYWORD":"","JOB_NUMBER":"","JOB_TITLE":""},"valid":true},"filterSelectionParam":{"searchFilterSelections":[{"id":"POSTING_DATE","selectedValues":[]},{"id":"LOCATION","selectedValues":[]},{"id":"JOB_FIELD","selectedValues":[]},{"id":"JOB_TYPE","selectedValues":[]},{"id":"JOB_SCHEDULE","selectedValues":[]},{"id":"JOB_SHIFT","selectedValues":[]}]},"advancedSearchFiltersSelectionParam":{"searchFilterSelections":[{"id":"ORGANIZATION","selectedValues":[]},{"id":"LOCATION","selectedValues":[]},{"id":"JOB_FIELD","selectedValues":[]},{"id":"URGENT_JOB","selectedValues":[]},{"id":"WILL_TRAVEL","selectedValues":[]},{"id":"JOB_SHIFT","selectedValues":[]}]},"pageNo":"6"}"""
# #
# # response = requests.post("https://nestle.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=2170452333", headers=headers, cookies=cookies, data=data)
# # #print(response.status_code)
# # resp = response.json()
# # #print(resp)
# # req = requests.get("https://nestle.taleo.net/careersection/3/jobsearch.ftl")
# # soup = bs(req.content, "lxml")
# # script = soup.find("script").text
# #
# # portal = re.findall("(portal\w+): "(.*?)"", script)[0][1]
# # lang = re.findall("(lan\w+): "(.*?)"",script)[0][1]
# #
# # title = resp["requisitionList"][5]["column"]
# # total_pages =resp["pagingData"]["totalCount"]
# # uri = soup.find_all("a")
# #
# # rq = requests.get("https://nestle.taleo.net/careersection/3/jobdetail.ftl?job=1800053V")
# # sauce = bs(rq.content, "lxml")
# # str = sauce.find_all("script")[-1].text
# # filler = re.findall("api.fillList.+\w",str)
# # filler = filler[0].replace("api.fillList("requisitionDescriptionInterface", "descRequisition", ","")
# # clean_txt = filler.replace("true"," ").replace("false"," ").replace("",""," ").replace("["," ").replace("]"," ").replace("%26nbsp;","").replace(""","").replace("Submission for the position:","")
# #
# # rrr = requests.get("https://appliedmat.taleo.net/careersection/10020/jobsearch.ftl")
# # so = bs(rrr.content,"lxml")
# # print(so.find("input",id="initialHistory").get("value"))
# # print(so.find("input",id="listRequisition.nbElements").get("value"))
# # script = so.find_all("script")[-1].text
# # fillis = re.findall("api.fillList.+",script)[0]
# # text = re.findall("\[.*?\]",fillis)[0]
# # text = text.replace("[","").replace("]","")
# # text = text.split(",")
# # items = [i for i in text if i not in (""true"",""false"","""")]
# # all = [ii for n,ii in enumerate(items) if ii not in items[:n]]
# # #print(all)
# #
# # def dou_jobs(company_name):
# #     company_name = company_name.replace(""","").replace(" ","-").lower()
# #     r = proxied_request("https://jobs.dou.ua/companies/{0}/vacancies/".format(company_name))
# #     soup = bs(r.content,"lxml")
# #     li_items = soup.find_all("li",class_="l-vacancy")
# #     site = soup.find("div",class_="site").text.strip()
# #     total_jobs = soup.find("div",class_="b-inner-page-header").find("h1").text
# #     total_jobs = re.findall("\d+",total_jobs)[0]
# #     additionals = []
# #     douDict = {}
# #     if int(total_jobs) > 20:
# #         while True:
# #             cookies = {
# #                 "csrftoken": "t6fjRW5QDzz0aZPDKc4iblWACdoXUdSESXxnYi6YpiBbm8QYo75Fpr5fV0OaRfoc",
# #                 "_ga": "GA1.2.927276990.1531737750",
# #                 "_gid": "GA1.2.964443387.1532436035",
# #                 "_gat": "1",
# #             }
# #             headers = {
# #                 "Origin": "https://jobs.dou.ua",
# #                 "Accept-Encoding": "gzip, deflate, br",
# #                 "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
# #                 "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
# #                 "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
# #                 "Accept": "application/json, text/javascript, */*; q=0.01",
# #                 "Referer": "https://jobs.dou.ua/companies/innovecs/vacancies/",
# #                 "X-Requested-With": "XMLHttpRequest",
# #                 "Connection": "keep-alive",
# #             }
# #             data = [
# #                 ("csrfmiddlewaretoken", "ou0zcK5L4kVqOJTHEg4OXV8LtwYRnacvNliDj66TQ3XB0SU2ib5bb1hqMjo4kcI3"),
# #                 ("count", "260"),
# #             ]
# #             response = requests.post("https://jobs.dou.ua/vacancies/ciklum/xhr-load/", headers=headers, cookies=cookies, data=data)
# #             html = response.json()["html"]
# #             checker = response.json()["last"]
# #             soupy = bs(html,"lxml")
# #             additionals += soupy.find_all("li",class_="l-vacancy")
# #             print(len(additionals))
# #             if checker is True:
# #                 break
# #
# #     added_li_items  = li_items + additionals
# #     dataArr = []
# #     for li in added_li_items:
# #         temp ={}
# #         title = li.find("div").find("div",class_="title").find("a").text.strip()
# #         try:
# #             cities = li.find("div").find("div", class_="title").find("span",class_="cities").text.strip()
# #         except:
# #             cities=None
# #         title_url = li.find("div").find("div",class_="title").find("a").get("href")
# #         try:
# #             salary = li.find("div").find("div", class_="title").find("span",class_="salary").text.strip()
# #         except:
# #             salary = None
# #         r2 = proxied_request(title_url)
# #         sauce = bs(r2.content,"lxml")
# #         try:
# #             desc = sauce.find("div",class_="l-vacancy").text.strip()
# #         except:
# #             desc =None
# #         try:
# #             snip =li.find("div").find("div",class_="sh-info").text.strip()
# #         except:
# #             snip = None
# #         temp["title"] = title
# #         temp["location"] = cities
# #         temp["salary"] = salary
# #         temp["title_url"] = title_url
# #         temp["snippet"] = snip
# #         temp["description"] = desc
# #         dataArr.append(temp)
# #     douDict["success"] = True
# #     douDict["total_jobs"] = total_jobs
# #     douDict["website"] = site
# #     douDict["company_name"] = company_name
# #     douDict["data"] = dataArr
# #     return douDict
# #
# # print(dou_jobs("innovecs"))
#
# def google_patents(company_name,page="0"):
#     patentDict = {}
#     patentDict["success"] =True
#     try:
#         response = proxied_request("https://patents.google.com/xhr/query?url=q%3D{0}%26oq%3D{1}%26page%3D{2}&exp=".format(company_name,company_name,page))
#     except Exception as e:
#         patentDict["success"] = False
#         patentDict["errorMessage"] = str(e)
#         return patentDict
#     response = response.json()
#     total_pages = response["results"]["total_num_pages"]
#     total_results = response["results"]["total_num_results"]
#     data_iterator = response["results"]["cluster"][0]["result"]
#     data = []
#     for d in data_iterator:
#         del d["rank"]
#         del d["is_similar_document"]
#         publication_no = d["patent"]["publication_number"]
#         try:
#             res = proxied_request("https://patents.google.com/patent/{0}/en?q={1}&oq={2}&page={3}".format(publication_no,company_name,company_name,page))
#         except Exception as e:
#             print(str(e))
#         soups = bs(res.content, "lxml")
#         try:
#             abstract = soups.find("abstract").text
#         except:
#             abstract = None
#         # try:
#         #     imp_people = soups.find("dl",class_="important-people style-scope patent-result")
#
#         data.append(d)
#     patentDict["total_pages"] = total_pages
#     patentDict["total_results"] = total_results
#     patentDict["data"] = data
#     return patentDict
# #
# # print(google_patents("amazon","13"))
#
# resp = proxied_request("https://patents.google.com/patent/US7379782B1/")
# soups = bs(resp.content, "lxml")
# # print(soups)
# # print(soups.find_all("section",class_="knowledge-card style-scope patent-result"))
# # print(soups.find("div", {"class":"abstract style-scope patent-text"}))
# # print(soups.find("span", {"itemprop" : "title"}).text)
# # print(soups.find("abstract").text)
#
# # print(soups.find("dl").find_all("dt"))
# # inventors = soups.find_all("dd",{"itemprop" : "inventor"})
# # current_assignees = soups.find_all("dd",{"itemprop" : "assigneeCurrent"})
# # orignal_assignee = soups.find("span",{"itemprop" : "assigneeOriginal"})
# # prior_date = soups.find("time", {"itemprop" : "priorityDate"})
# # app_no = soups.find("span", {"itemprop" : "applicationNumber"})
# # soups.find("span", {"itemprop" : "filingDate"})
# # print(soups.find("span", {"itemprop" : "ifiStatus"}))
# # title =soups.find("span", {"itemprop" : "title"})
# # li_items = soups.find_all("li", {"itemprop" : "cpcs"})
# #
# # classific = []
# # for l in li_items:
# #     if l.find("meta") is not None:
# #         classific.append(l.text)
# #
# # print(soups.find("meta",{"itemprop":"numberWithoutCodes"}).get("content"))
# # print(soups.find("meta",{"itemprop":"kindCode"}).get("content"))
# # print(soups.find("dd",{"itemprop":"countryCode"}).text)
# # print(soups.find("description-of-drawings").text)
# # print(len(soups.find_all("div", {"itemprop":"content"})))
# #
# # claim_no = soups.find("section",{"itemprop" : "claims"}).find("h2").text
# # num_claims = re.findall("\d+",claim_no)[0]
# # claim_text = soups.find("section",{"itemprop" : "claims"}).find("div").text
# #
# # print(num_claims)
# # print(claim_text)
# #
# # heads = soups.find_all("h2")
# # cited_by = ""
# # patent_citations = ""
# # non_patent_cit = ""
# # for head in heads:
# #     if "Cited By" in head.text:
# #         cited_by = head.text
# #     elif "Patent Citations" in head.text and "Non" not in head.text:
# #         patent_citations = head.text
# #     elif "Non-Patent" in head.text:
# #         non_patent_cit = head.text
# #     else:
# #         continue
# #
# # cited_by = re.findall("\d+",cited_by)[0]
# # patent_citations = re.findall("\d+",patent_citations)[0]
# # non_patent_cit = re.findall("\d+",non_patent_cit)[0]
# #
# # print(soups.find("section",{"itemprop" : "description"}).text.split("BRIEF DESCRIPTION OF DRAWINGS")[0])
# # print(orignal_assignee)
#
# #
# # uri = "http://www.patentsview.org/api/patent.html"
# # r = requests.get(uri)
# # soup = bs(r.content,"lxml")
# #
# # table = soup.find("table",class_="table table-striped documentation-fieldlist")
# # my_list = []
# # for row in table.find_all("tr")[1:]:
# #     col = row.find_all("td")
# #     my_list.append(col[0].text)
# #
# # print(my_list)
#
# # f_params = ["appcit_app_number", "appcit_category", "appcit_date", "appcit_kind", "appcit_sequence", "app_country", "app_date", "app_number", "app_type", "assignee_city", "assignee_country", "assignee_county", "assignee_county_fips", "assignee_first_name", "assignee_first_seen_date", "assignee_id", "assignee_last_name", "assignee_last_seen_date", "assignee_lastknown_city", "assignee_lastknown_country", "assignee_lastknown_latitude", "assignee_lastknown_location_id", "assignee_lastknown_longitude", "assignee_lastknown_state", "assignee_latitude", "assignee_location_id", "assignee_longitude", "assignee_organization", "assignee_sequence", "assignee_state", "assignee_state_fips", "assignee_total_num_inventors", "assignee_total_num_patents", "assignee_type", "cited_patent_category", "cited_patent_date", "cited_patent_kind", "cited_patent_number", "cited_patent_sequence", "cited_patent_title", "citedby_patent_category", "citedby_patent_date", "citedby_patent_kind", "citedby_patent_number", "citedby_patent_title", "cpc_category", "cpc_first_seen_date", "cpc_group_id", "cpc_group_title", "cpc_last_seen_date", "cpc_section_id", "cpc_sequence", "cpc_subgroup_id", "cpc_subgroup_title", "cpc_subsection_id", "cpc_subsection_title", "cpc_total_num_assignees", "cpc_total_num_inventors", "cpc_total_num_patents", "detail_desc_length", "examiner_first_name", "examiner_id", "examiner_last_name", "examiner_role", "examiner_group", "forprior_country", "forprior_date", "forprior_docnumber", "forprior_kind", "forprior_sequence", "govint_contract_award_number", "govint_org_id", "govint_org_level_one", "govint_org_level_two", "govint_org_level_three", "govint_org_name", "govint_raw_statement", "inventor_city", "inventor_country", "inventor_county", "inventor_county_fips", "inventor_first_name", "inventor_first_seen_date", "inventor_id", "inventor_last_name", "inventor_last_seen_date", "inventor_lastknown_city", "inventor_lastknown_country", "inventor_lastknown_latitude", "inventor_lastknown_location_id", "inventor_lastknown_longitude", "inventor_lastknown_state", "inventor_latitude", "inventor_location_id", "inventor_longitude", "inventor_sequence", "inventor_state", "inventor_state_fips", "inventor_total_num_patents", "ipc_action_date", "ipc_class", "ipc_classification_data_source", "ipc_classification_value", "ipc_first_seen_date", "ipc_last_seen_date", "ipc_main_group", "ipc_section", "ipc_sequence", "ipc_subclass", "ipc_subgroup", "ipc_symbol_position", "ipc_total_num_assignees", "ipc_total_num_inventors", "ipc_version_indicator", "lawyer_first_name", "lawyer_first_seen_date", "lawyer_id", "lawyer_last_name", "lawyer_last_seen_date", "lawyer_organization", "lawyer_sequence", "lawyer_total_num_assignees", "lawyer_total_num_inventors", "lawyer_total_num_patents", "nber_category_id", "nber_category_title", "nber_first_seen_date", "nber_last_seen_date", "nber_subcategory_id", "nber_subcategory_title", "nber_total_num_assignees", "nber_total_num_inventors", "nber_total_num_patents", "patent_abstract", "patent_average_processing_time", "patent_date", "patent_firstnamed_assignee_city", "patent_firstnamed_assignee_country", "patent_firstnamed_assignee_id", "patent_firstnamed_assignee_latitude", "patent_firstnamed_assignee_location_id", "patent_firstnamed_assignee_longitude", "patent_firstnamed_assignee_state", "patent_firstnamed_inventor_city", "patent_firstnamed_inventor_country", "patent_firstnamed_inventor_id", "patent_firstnamed_inventor_latitude", "patent_firstnamed_inventor_location_id", "patent_firstnamed_inventor_longitude", "patent_firstnamed_inventor_state", "patent_kind", "patent_num_cited_by_us_patents", "patent_num_claims", "patent_num_combined_citations", "patent_num_foreign_citations", "patent_num_us_application_citations", "patent_num_us_patent_citations", "patent_number", "patent_processing_time", "patent_title", "patent_type", "patent_year", "pct_102_date", "pct_371_date", "pct_date", "pct_docnumber", "pct_doctype", "pct_kind", "rawinventor_first_name", "rawinventor_last_name", "uspc_first_seen_date", "uspc_last_seen_date", "uspc_mainclass_id", "uspc_mainclass_title", "uspc_sequence", "uspc_subclass_id", "uspc_subclass_title", "uspc_total_num_assignees", "uspc_total_num_inventors", "uspc_total_num_patents", "wipo_field_id", "wipo_field_title", "wipo_sector_title", "wipo_sequence"]
#
# # year = '2001'
# # page = '2'
# # payload = "{"q":{"_gte\":{\"patent_date\":\"{0}-01-04\"}},\"f\":[\"patent_number\",\"patent_date\"]}".format(year)
# # res = requests.post('http://www.patentsview.org/api/patents/query',data=payload)
# # print(res.status_code)
# # print(res.json())
# # import requests
# #
# # title = "computer"
# # author = "Jobs"
# # start_date = "2007-01-01"
# # end_date = "2007-02-01"
# # url = "http://www.patentsview.org/api/patents/query"
# # data = {
# #     "q":{"_and":[{"_gte":{"patent_date":start_date}},{"_lte":{"patent_date":end_date }}]},
# #     "f":["patent_number","patent_date", "patent_title"],
# #     "o":{"page": 1, "per_page": 10000}
# # }
# # resp = requests.post(url, json=data)
# # print(resp.status_code)
# # if resp.status_code == 200:
# #     response = resp.json()
# #
# # data2 = {
# #     "q":{"patent_number" : "3930775"},
# #     "f": ["appcit_app_number", "appcit_category", "appcit_date", "appcit# }_kind", "appcit_sequence", "app_country", "app_date", "app_number", "app_type", "assignee_city", "assignee_country", "assignee_county", "assignee_county_fips", "assignee_first_name", "assignee_first_seen_date", "assignee_id", "assignee_last_name", "assignee_last_seen_date", "assignee_lastknown_city", "assignee_lastknown_country", "assignee_lastknown_latitude", "assignee_lastknown_location_id", "assignee_lastknown_longitude", "assignee_lastknown_state", "assignee_latitude", "assignee_location_id", "assignee_longitude", "assignee_organization", "assignee_sequence", "assignee_state", "assignee_state_fips", "assignee_total_num_inventors", "assignee_total_num_patents", "assignee_type", "cited_patent_category", "cited_patent_date", "cited_patent_kind", "cited_patent_number", "cited_patent_sequence", "cited_patent_title", "citedby_patent_category", "citedby_patent_date", "citedby_patent_kind", "citedby_patent_number", "citedby_patent_title", "cpc_category", "cpc_first_seen_date", "cpc_group_id", "cpc_group_title", "cpc_last_seen_date", "cpc_section_id", "cpc_sequence", "cpc_subgroup_id", "cpc_subgroup_title", "cpc_subsection_id", "cpc_subsection_title", "cpc_total_num_assignees", "cpc_total_num_inventors", "cpc_total_num_patents", "detail_desc_length", "examiner_first_name", "examiner_id", "examiner_last_name", "examiner_role", "examiner_group", "forprior_country", "forprior_date", "forprior_docnumber", "forprior_kind", "forprior_sequence", "govint_contract_award_number", "govint_org_id", "govint_org_level_one", "govint_org_level_two", "govint_org_level_three", "govint_org_name", "govint_raw_statement", "inventor_city", "inventor_country", "inventor_county", "inventor_county_fips", "inventor_first_name", "inventor_first_seen_date", "inventor_id", "inventor_last_name", "inventor_last_seen_date", "inventor_lastknown_city", "inventor_lastknown_country", "inventor_lastknown_latitude", "inventor_lastknown_location_id", "inventor_lastknown_longitude", "inventor_lastknown_state", "inventor_latitude", "inventor_location_id", "inventor_longitude", "inventor_sequence", "inventor_state", "inventor_state_fips", "inventor_total_num_patents", "ipc_action_date", "ipc_class", "ipc_classification_data_source", "ipc_classification_value", "ipc_first_seen_date", "ipc_last_seen_date", "ipc_main_group", "ipc_section", "ipc_sequence", "ipc_subclass", "ipc_subgroup", "ipc_symbol_position", "ipc_total_num_assignees", "ipc_total_num_inventors", "ipc_version_indicator", "lawyer_first_name", "lawyer_first_seen_date", "lawyer_id", "lawyer_last_name", "lawyer_last_seen_date", "lawyer_organization", "lawyer_sequence", "lawyer_total_num_assignees", "lawyer_total_num_inventors", "lawyer_total_num_patents", "nber_category_id", "nber_category_title", "nber_first_seen_date", "nber_last_seen_date", "nber_subcategory_id", "nber_subcategory_title", "nber_total_num_assignees", "nber_total_num_inventors", "nber_total_num_patents", "patent_abstract", "patent_average_processing_time", "patent_date", "patent_firstnamed_assignee_city", "patent_firstnamed_assignee_country", "patent_firstnamed_assignee_id", "patent_firstnamed_assignee_latitude", "patent_firstnamed_assignee_location_id", "patent_firstnamed_assignee_longitude", "patent_firstnamed_assignee_state", "patent_firstnamed_inventor_city", "patent_firstnamed_inventor_country", "patent_firstnamed_inventor_id", "patent_firstnamed_inventor_latitude", "patent_firstnamed_inventor_location_id", "patent_firstnamed_inventor_longitude", "patent_firstnamed_inventor_state", "patent_kind", "patent_num_cited_by_us_patents", "patent_num_claims", "patent_num_combined_citations", "patent_num_foreign_citations", "patent_num_us_application_citations", "patent_num_us_patent_citations", "patent_number", "patent_processing_time", "patent_title", "patent_type", "patent_year", "pct_102_date", "pct_371_date", "pct_date", "pct_docnumber", "pct_doctype", "pct_kind", "rawinventor_first_name", "rawinventor_last_name", "uspc_first_seen_date", "uspc_last_seen_date", "uspc_mainclass_id", "uspc_mainclass_title", "uspc_sequence", "uspc_subclass_id", "uspc_subclass_title", "uspc_total_num_assignees", "uspc_total_num_inventors", "uspc_total_num_patents", "wipo_field_id", "wipo_field_title", "wipo_sector_title", "wipo_sequence"]
# # }
# #
# # resp2 = requests.post(url, json=data2)
# # print(resp2.status_code)
# # print(resp2.json())
#
# search_word = 'java developer'
# samarin_url = 'http://www.saramin.co.kr/zf_user/search/recruit/page/1?searchword={0}'.format(search_word)
# req = requests.get(samarin_url)
# soup = bs(req.content,'lxml')
#
# # print(soup.find('h2',class_='tit').text)
# #
# # numcase = soup.find('span',class_='numcase').text
# # total_pages =re.findall('-\d+',numcase)[0].replace('-','')
# #
# listitem_iterator = soup.find('ul',class_='company_inbox').find_all('li')
# print(len(listitem_iterator))
# end_point = listitem_iterator[0].find('a',class_='').get('href')
# base_url = 'http://www.saramin.co.kr'
# desc_url = '{0}{1}'.format(base_url,end_point)
# rec_id = re.findall('rec.+=\d+',desc_url)[0].replace('rec_idx=','')
#
# params = (
#     ('view_type', 'search'),
#     ('rec_idx', rec_id),
#     ('isMypage', 'no'),
#     ('gz', '1'),
#     ('recommend_ids', 'eJxdj8sVwzAIB`KvJne8C5xSi/ruIXmyDno/DoNWipmEUtrzyE189cNk1SE/Cgrzx9hKsbnvAL+z3m3nyG9uHIg//4O2ZBRnLceWzAe6DgqrBXZ0djepKVgskly1J58fuJiSGQYc5TbIm0/mRmdYsh0rN8s4q0z6C2CWOKAaTNEpVxr/GD5iTUzQ='),
#     ('searchword', 'java developer'),
#     ('paid_fl', 'n'),
# )
#
# detail_url = 'http://www.saramin.co.kr/zf_user/jobs/relay/view-detail?rec_idx={0}'.format(rec_id)
# print(rec_id)
# req2 = requests.get(detail_url)
# soup2 = bs(req2.content,'lxml')
# recruitment_sector_elig = soup2.find('table',class_='table_summary').find('tbody').text
# # print(recruitment_sector_elig)
# # recruit_head = soup2.find('h1',class_='tit_recruit_header').text
# checker_main = soup2.find('h2',class_='tit_section')
#
# checker_work = checker_main.find_next('h2',class_='tit_section')
# checker_work_text = checker_work.text
# work_style = ''
# work_dep = ''
# work_day = ''
# work_area = ''
# salary = ''
# comp_addr = ''
# nearby_train = ''
# selec_proc = ''
# req_doc = ''
# rec_period = ''
# resume_form = ''
# how_register = ''
#
# work_dict = {}
# admission_dict = {}
# recep_dict = {}
# # print(checker_work)
# if '근무조건 및 환경' in checker_work:
#     work_trs = checker_work.find_all_next('tr')
#     # print(work_trs)
#     for tr in work_trs:
#         check1 = tr.th.text
#         if '근무형태' in check1:
#             try:
#                 work_style = tr.td.text
#             except:
#                 work_style = None
#         elif '근무부서' in check1:
#             try:
#                 work_dep = tr.td.text
#             except:
#                 work_dep = None
#         elif '근무요일/시간' in check1:
#             try:
#                 work_day = tr.td.text
#             except:
#                 work_day = None
#         elif '근무지역' in check1:
#             try:
#                 work_area = tr.td.text
#             except:
#                 work_area = None
#         elif '급여' in check1:
#             try:
#                 salary = tr.td.text
#             except:
#                 salary = None
#         elif '회사주소' in check1:
#             try:
#                 comp_addr = tr.td.text
#             except:
#                 comp_addr = None
#         elif '인근전철' in check1:
#             try:
#                 nearby_train = tr.td.text
#             except:
#                 nearby_train = None
#         elif '전형절차' in check1.strip():
#             try:
#                 selec_proc = tr.td.text
#             except:
#                 selec_proc = None
#         elif '제출서류' in check1:
#             try:
#                 req_doc = tr.td.text
#             except:
#                 req_doc = None
#         elif '접수기간' in check1:
#             try:
#                 rec_period = tr.td.text
#             except:
#                 rec_period = None
#         elif '이력서양식' in check1:
#             try:
#                 resume_form = tr.td.text
#             except:
#                 resume_form = None
#
#         elif '접수방법' in check1:
#             try:
#                 how_register = tr.td.text
#             except:
#                 how_register = None
#         else:
#             print('Not found')
#         work_dict['working_style'] = work_style
#         work_dict['working_area'] = work_area
#         work_dict['working_day'] = work_day
#         work_dict['working_department'] = work_dep
#         work_dict['company_address'] = comp_addr
#         work_dict['nearby_train'] = nearby_train
#         admission_dict['selection_procedure'] = selec_proc
#         admission_dict['requirement_doc'] = req_doc
#         recep_dict['reception_period'] = rec_period
#         recep_dict['resume_form'] = resume_form
#         recep_dict['how_to_register'] = how_register
# others = soup2.find('p',class_='txt_caution').text
# saraminDetails = {}
# saraminDetails['working_conditions'] = work_dict
# saraminDetails['addmission_procedure'] = admission_dict
# saraminDetails['reception_method'] = recep_dict
# saraminDetails['other_precautions'] = others
# #
# # print(saraminDetails)
# # checker_admin = checker_work.find_next('h2',class_='tit_section')
# # checker_admin_text = checker_admin.text
# # if '전형절차 및 제출서류' in checker_admin:
# #     admin_trs = checker_admin.find_all('tr')
# #
# # checker_recep = checker_admin.find_next('h2',class_='tit_section')
# # checker_recep_text = checker_recep.text
# # if '접수기간 및 방법' in checker_recep:
# #     recep_trs = checker_recep.find_all('tr')
#
#
# # print(soup2.find_all('div'))
# # responsibility = ''
# # elig = ''
# # work_cond = ''
# # comp_info = ''
# # print(soup2.find('div',class_='view_summary'))
# # desc_cards = soup2.find('div',class_='view_summary').find_all('div',class_='summary')
# # for desc in desc_cards:
# #     checker = desc.find('strong',class_='tit_info').text
# #     if checker is '담당업무':
# #         responsibility = desc.find('ul').text
# #     elif checker is '지원자격':
# #         elig = desc.find('ul').text
# #     elif checker is '근무조건':
# #         work_cond = desc.find('ul').text
# #     elif checker is '기업정보':
# #         comp_info = desc.find('ul').text
# # print(responsibility)
# # samarinDict = {}
# # data = []
# # for l in listitem_iterator:
# #     temp = {}
# #     try:
# #         title = l.find('h2',class_='tit').text.strip()
# #     except:
# #         title =None
# #     try:
# #         text = l.find('p',class_='txt').text.strip()
# #     except:
# #         text =None
# #     try:
# #         terms = l.find('p',class_='terms_li').text.strip()
# #     except:
# #         terms = None
# #     try:
# #         kw_line = l.find('p',class_='keywordline').text.strip()
# #     except:
# #         kw_line = None
# #     temp['title'] = title
# #     temp['text'] = text
# #     temp['terms'] = terms
# #     temp['kw_line'] = kw_line
# #     data.append(temp)
# #
# # samarinDict['data'] = data
# # samarinDict['total_pages'] = total_pages
# # print(samarinDict)
#
# import requests
#
#
# headers = {
#     'Origin': 'http://www.saramin.co.kr',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Accept': 'application/json, text/javascript, */*; q=0.01',
#     'Referer': 'http://www.saramin.co.kr/zf_user/talent/search',
#     'X-Requested-With': 'XMLHttpRequest',
#     'Connection': 'keep-alive',
# }
#
# data = [
#   ('componentData[KeywordSearchOption]', ''),
#   ('page', '1'),
#   ('pageCount', '10'),
#   ('List[page]', '1'),
#   ('List[pageCount]', '10'),
#   ('List[updateDate]', 'all'),
#   ('List[contact_open]', ''),
#   ('List[order]', 'last_dt'),
#   ('List[sort]', 'desc'),
#   ('viewTarget', ''),
# ]
#
# response = requests.post('http://www.saramin.co.kr/zf_user/talent/api/get-talent-list', headers=headers, data=data)
# talent_content = response.json()['content']
# print(response.json()['result_cnt'])
# # soups = bs(talent_content,'lxml')
#
# talent_cards = soups.find_all('tr',class_='resume_area')
# print(talent_cards[0])
#
# talent_data = []
# for talent in talent_cards:
#     temp = {}
#     try:
#         title = talent.find('p',   class_='point').text
#     except:
#         title = None
#     try:
#         profile_name = talent.find('span',class_='txt_name').text
#     except:
#         profile_name = None
#     try:
#         gender = talent.find('span',class_='gender').text
#     except:
#         gender = None
#     try:
#         profile_url = talent.find('div',class_='box_img').find('img').get('src')
#     except:
#         profile_url = None
#     try:
#         experience = talent.find('span',class_='badge_career experience').text
#     except:
#         experience = None
#     try:
#         career_info = talent.find('div',class_='btn_career_info').get('title')
#     except:
#         career_info = None
#     try:
#         details = talent.find('ul',class_='list').text
#     except:
#         details = None
#     try:
#         area = talent.find('p',class_='area').text
#     except:
#         area = None
#     try:
#         loc = talent.find('div',class_='unit').text
#     except:
#         loc = None
#     try:
#         headline = talent.find('a',class_='title').text
#     except:
#         headline = None
#     try:
#         kw_line = talent.find('p',class_='key_word').text
#     except:
#         kw_line = None
#     try:
#         details_url = talent.find('a',class_='title').get('href')
#     except:
#         details_url = None
#     try:
#         res_id = talent.find('a',class_='title').get('data-res_idx')
#     except:
#         res_id = None
#
#     import requests
#     headers = {
#         'Connection': 'keep-alive',
#         'Cache-Control': 'max-age=0',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#         'Referer': 'http://www.saramin.co.kr/zf_user/talent/search',
#         'Accept-Encoding': 'gzip, deflate',
#         'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     }
#
#     params = (
#         ('res_idx', res_id),
#         ('alertStyle', '2'),
#         ('open_type', 'default'),
#         ('route', 'talent_search'),
#         ('code', 'search'),
#         ('search', 'click'),
#     )
#     print(res_id)
#     response = requests.get('http://www.saramin.co.kr/zf_user/mandb/view', headers=headers, params=params)
#     soup2 = bs(response.content, 'lxml')
#     birthday_spans = []
#     dashboard = []
#     try:
#         resume_title = soup2.find('div',class_='section_profile').find('div',class_='area_title')
#     except:
#         resume_title = None
#     try:
#         birthday_spans = soup2.find('span',class_='birthday').find_all('span')
#         bday = birthday_spans[0].text
#     except:
#         bday = None
#     try:
#         gender = birthday_spans[1].text
#     except:
#         gender = None
#     try:
#         mail = soup2.find('li',class_='mail').text
#     except:
#         mail = None
#     try:
#         phone = soup2.find('li', class_='phone').text
#     except:
#         phone = None
#     try:
#         address = soup2.find('li', class_='address').text
#     except:
#         address = None
#     try:
#         tel = soup2.find('li', class_='tel').text
#     except:
#         tel =None
#     try:
#         dashboard = soup2.find('div',class_='dashboard').find_all('li')
#     except:
#         dash_board = None
#     dash_board = {}
#     # print(dashboard)
#     # print(len(dashboard))
#     # print(resume_title)
#     for dash in dashboard:
#         edu_hist,career,hope_salary,hope_workplace,portfolio = ['' for i in range(5)]
#         check = dash.strong.text
#         # print(check)
#         if '학력사항' in check:
#             print('edu')
#             edu_hist = dash.text
#             dash_board['education_history'] = edu_hist
#         elif '경력사항' in check:
#             print('career')
#             career = dash.text
#             dash_board['career'] = career
#         elif '희망연봉/근무형태' in check:
#             print('hope salry')
#             hope_salary = dash.text
#             dash_board['hope_salary'] = hope_salary
#         elif '희망근무지' in check:
#             print('hop workplace')
#             hope_workplace = dash.p.text
#             dash_board['hope_workplace'] = hope_workplace
#         elif '포트폴리오' in check:
#             print('portfolio')
#             portfolio = dash.text
#             dash_board['portfolio'] = portfolio
#         else:
#             print('not found')
#     # print(dash_board)
#     tables = soup2.find_all('div',class_='section_part')
#     educ = []
#     act = []
#     cert = []
#     tech = []
#     self_intro = ''
#     careers = {}
#     for table in tables:
#         check = table.h3.text
#         try:
#             detail = table.find('span',class_='indetail').text
#         except:
#             detail = None
#         if '학력' in check:
#             educ_detail = detail
#             tds = table.find_all('td')
#             period_study,div, school_name, majors,grades = ['' for i in range(5)]
#             tds_new = []
#             for t in tds:
#                 if t.get('colspan') is None:
#                     tds_new.append(t)
#                 else:
#                     continue
#             print(tds_new)
#             for n,td in enumerate(tds_new):
#                 temp_ed = {}
#                 if n % 5 == 0:
#                     period_study = td.text.strip()
#                 elif n % 5 == 1:
#                     div = td.text
#                 elif n % 5 == 2:
#                     school_name = td.text.strip()
#                 elif n % 5 == 3:
#                     majors = td.text.strip()
#                 elif n % 5 == 4:
#                     grades = td.text.strip()
#                 temp_ed['period_of_study'] = period_study
#                 temp_ed['division'] = div
#                 temp_ed['school_name'] = school_name
#                 temp_ed['major'] = majors
#                 temp_ed['grades'] = grades
#                 if n % 5 == 4:
#                     educ.append(temp_ed)
#         elif '학력' in check:
#             career_detail = detail
#             career_desc = table.find('div',class_='box_talented_nudge').text
#             careers['details'] = career_detail
#             careers['description'] = career_desc
#             print(careers)
#         elif '대외활동' in check:
#             term,div,agency,contents = ['' for i in range(4)]
#             tds = table.find_all('td')
#             for n,td in enumerate(tds):
#                 temp_act = {}
#                 if n % 4 == 0:
#                     term = td.text.strip()
#                 elif n % 4 == 1:
#                     div = td.text
#                 elif n % 4 == 2:
#                     agency = td.text.strip()
#                 elif n % 4 == 3:
#                     contents = td.text.strip()
#                 temp_act['term'] = term
#                 temp_act['division'] = div
#                 temp_act['agency'] = agency
#                 temp_act['contents'] = contents
#                 if n % 4 == 3:
#                     act.append(temp_act)
#         elif '자격증/어학/수상내역' in check:
#             acq_date,div,qual,publish,score  = ['' for i in range(5)]
#             tds = table.find_all('td')
#             for n,td in enumerate(tds):
#                 temp_cert = {}
#                 if n % 5 == 0:
#                     acq_date = td.text.strip()
#                 elif n % 5 == 1:
#                     div = td.text
#                 elif n % 5 == 2:
#                     qual = td.text.strip()
#                 elif n % 5 == 3:
#                     publish = td.text.strip()
#                 elif n % 5 == 4:
#                     score = td.text.strip()
#                 temp_cert['acquisition_date'] = acq_date
#                 temp_cert['division'] = div
#                 temp_cert['qualification'] = qual
#                 temp_cert['publisher'] = publish
#                 temp_cert['score'] = score
#                 if n % 5 == 4:
#                     cert.append(temp_cert)
#         elif '보유기술' in check:
#             abiity,detal,level  = ['' for i in range(3)]
#             tds = table.find_all('td')
#             for n,td in enumerate(tds):
#                 temp_tech = {}
#                 if n % 3 == 0:
#                     abiity = td.text.strip()
#                 elif n % 3 == 1:
#                     detal = td.text
#                 elif n % 3 == 2:
#                     level = td.text.strip()
#                 temp_tech['ability'] = abiity
#                 temp_tech['level'] = level
#                 temp_tech['detail'] = detal
#                 if n % 3 == 2:
#                     tech.append(temp_tech)
#         elif '자기소개서' in check:
#             try:
#                 self_intro = table.find('div',class_='box_talented_nudge').text
#             except:
#                 self_intro = None
#
#     temp['title'] = title
#     temp['headline'] = headline
#     temp['profile_name'] = profile_name
#     temp['profile_image_url'] = profile_url
#     temp['location'] = loc
#     temp['gender'] = gender
#     temp['kw_line'] = kw_line
#     temp['details'] = details
#     temp['experience'] = experience
#     temp['career_info'] = career_info
#     temp['university'] = area
#     talent_data.append(temp)
#
# # print(talent_data)

import requests
from bs4 import BeautifulSoup as bs
import re
import pprint
#
# req1 = requests.get('http://www.albamon.com/search?Keyword=Seoul&page=500')
# soup1 = bs(req1.content,'lxml')
#
# total_pages = soup1.find('span',class_='total').em.text
# base_url = 'http://www.albamon.com'
# listitem_iterator = soup1.find_all('dl',class_='list')
# print(len(listitem_iterator))
# albamonDict = {}
# albamonDict['success'] = True
# albamon_jobs = []
# for li in listitem_iterator:
#     temp ={}
#     temp['details'] = {}
#     try:
#         title = li.dt.text.strip()
#     except:
#         title = None
#     try:
#         detail_url = li.dt.find('a').get('href')
#     except:
#         detail_url =None
#     try:
#         location = li.find('dd',class_='local').text.strip()
#     except:
#         location = None
#     lis = li.find('dd',class_='etc').find_all('span')
#     try:
#         salary = li.find('dd',class_='etc').find_all('span')[0].text.strip()
#     except:
#         salary = None
#     try:
#         deadline = li.find('dd',class_='etc').find_all('span')[-1].text.strip().replace('마감일','').replace(':','')
#     except:
#         deadline = None
#     detail_url = '{0}{1}'.format(base_url,detail_url)
#     req2 = requests.get(detail_url)
#     soup2 = bs(req2.content,'lxml')
#     try:
#         company_name = soup2.find('span',class_='companyName')
#     except:
#         company_name = None
#     tables_recruit = soup2.find('div',class_='recruitCondition').find('div',class_='viewTable').find_all('tr')
#     rec_cond = {}
#     for table in tables_recruit:
#         check = table.th.text
#         if '마감일' in check:
#             rec_cond['deadline'] = table.td.text.strip()
#         elif '인원' in check:
#             rec_cond['personnel'] = table.td.text.strip()
#         elif '성별' in check:
#             rec_cond['gender'] = table.td.text.strip()
#         elif '연령' in check:
#             rec_cond['age'] = table.td.text.strip()
#         elif '학력' in check:
#             rec_cond['education'] = table.td.text.strip()
#         elif '우대' in check:
#             rec_cond['preference'] = table.td.text.strip()
#     try:
#         reg_date = soup2.find('div',class_='regDate').text.strip().replace('등록','').replace(':','')
#     except:
#         reg_date =None
#     working_cond = {}
#     tables_work = soup2.find('div',class_='workCondition').find('div',class_='viewTable').find_all('tr')
#     for table in tables_work:
#         check = table.th.text
#         if '급여' in check:
#             working_cond['salary'] = table.td.text.strip()
#         elif '근무기간' in check:
#             working_cond['employment_period'] = table.td.text.strip()
#         elif '근무요일' in check:
#             working_cond['working_day'] = table.td.text.strip()
#         elif '근무시간' in check:
#             working_cond['working_hours'] = table.td.text.strip()
#         elif '업직종' in check:
#             working_cond['occupation'] = table.td.text.strip()
#         elif '고용형태' in check:
#             working_cond['employment_type'] = table.td.text.strip()
#     try:
#         work_addr = soup2.find('div',class_='workAddr').text.strip()
#     except:
#         work_addr = None
#     map_summary = soup2.find('div',class_='mapSummary').find_all('li')
#     map_sum = {}
#     for map in map_summary:
#         check = map.find('span',class_='mapItemTitle').text
#         if '인근지하철' in check:
#             map_sum['nearby_subway'] = map.text.strip().replace('인근지하철','')
#         elif '인근대학' in check:
#             map_sum['nearby_university'] = map.text.strip().replace('인근대학','')
#     try:
#         detail_app = soup2.find('div',class_='GIContentDiv').text.strip()
#     except:
#         detail_app = None
#
#     career_info = {}
#     coorporate_name = soup2.find('div',class_='infoList').find('div',class_='title').text.strip()
#     career_info['company_corporate_name'] = coorporate_name
#     careers = soup2.find('div',class_='infoList').find_all('div',class_='listItem')
#     for career in careers:
#         check = career.find('span',class_='dataRow').text
#         if '대표자' in check:
#             career_info['representative'] = career.find('div',class_='data').text
#         elif '회사주소' in check:
#             career_info['company_address'] = career.find('div',class_='data').text
#         elif '사업내용' in check:
#             career_info['business_contents'] = career.find('div',class_='data').text
#         elif '홈페이지' in check:
#             career_info['homepage'] = career.find('div',class_='data').text
#
#
#     temp['details']['careers_corporate_info'] = career_info
#     temp['details']['detailed_application_guide'] = detail_app
#     temp['details']['map_summary'] = map_sum
#     temp['details']['work_address'] = work_addr
#     temp['details']['registration_date'] = reg_date
#     temp['details']['working_conditions'] = working_cond
#     temp['details']['recruitment_conditions'] = rec_cond
#     temp['title'] = title
#     temp['location'] = location
#     temp['deadline'] = deadline
#     temp['salary'] = salary
#     temp['detail_url'] = detail_url
#     albamon_jobs.append(temp)
#
pp = pprint.PrettyPrinter(indent=4)
#
# import requests
#
# page = '1'
# headers = {
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
#     'Accept': '*/*',
#     'Referer': 'http://www.albamon.com/ResumeSearch/?state=471653573',
#     'X-Requested-With': 'XMLHttpRequest',
#     'Connection': 'keep-alive',
# }
#
# params = (
#     ('IsMoveTop', 'true'),
#     ('MenuNumber', '1'),
#     ('Page', '{0}'.format(page)),
#     ('PageSize', '50'),
#     ('ListType', 'box'),
#     ('OrderType', '1'),
# )
#
# albamonDict = {}
# albamonDict['success'] = True
#
# response = requests.get('http://www.albamon.com/ResumeSearch/Get-Resume-List', headers=headers, params=params)
# soup = bs(response.content,'lxml')
#
# card_iterator = soup.find('ul',id='dev_listResult').find_all('li',recursive=False)
# print(len(card_iterator))
# total_count = soup.find('input',id='TotalCount').get('value')
# albamon_arr = []
# for card in card_iterator:
#     temp = {}
#     temp['details'] = {}
#     try:
#         name = card.find('p',class_='name').em.text.strip()
#     except:
#         name = None
#     try:
#         age = card.find('p',class_='name').text.strip().replace(name,'').split(',')[1].replace(')','').strip()
#     except:
#         age = None
#     try:
#         gender = card.find('p',class_='name').text.strip().replace(name,'').split(',')[0].replace('(','').strip()
#     except:
#         gender = None
#     try:
#         title = card.find('p',class_='title').text.strip()
#     except:
#         title = None
#     try:
#         career = card.find('p',class_='career').text.strip()
#     except:
#         career = None
#     try:
#         occup = card.find('div',class_='info2').p.text.strip()
#     except:
#         occup = None
#     try:
#         other_details = card.find('div',class_='info2').ul.text.strip()
#     except:
#         other_details = None
#     try:
#         demands = card.find('div',class_='info3').find('div',class_='txBx').text.strip()
#     except:
#         demands = None
#     try:
#         posted_at = card.find('div', class_='info3').find('p', class_='tx').text.strip()
#     except:
#         posted_at = None
#     try:
#         details_url = card.find('a', class_='').get('href')
#     except:
#         details_url = None
#     base_url = 'http://www.albamon.com'
#     details_url = '{0}{1}'.format(base_url,details_url)
#     req2 = requests.get(details_url)
#     soup2 = bs(req2.content,'lxml')
#     try:
#         rev_date = soup2.find('div',id='ggDate').text.strip()
#     except:
#         rev_date =None
#     try:
#         headline = soup2.find('p',class_='rsTit').text.strip()
#     except:
#         headline = None
#     personal_info = {}
#     try:
#         trows_all = soup2.find('table',class_='rsTbl').find_all('tr')
#     except:
#         trows_all = [[1,2,3],2,3]
#     for row in trows_all[0]:
#         try:
#             profile_name = row.find('span',class_='name').text.strip()
#         except:
#             profile_name = None
#         try:
#             sex = row.find('span',class_='sex').text.strip()
#         except:
#             sex = None
#         try:
#             avail_time = row.find('span',class_='time').text.strip()
#         except:
#             avail_time = None
#         personal_info['profile_name'] = profile_name
#         personal_info['sex']  = sex
#         personal_info['available_time'] = avail_time
#     for row in trows_all[1:]:
#         try:
#             check = row.th.text.strip()
#             if '휴대폰' in check:
#                 try:
#                     personal_info['telephone'] = row.td.text.strip()
#                 except:
#                     personal_info['telephone'] = None
#             elif '이메일' in check:
#                 try:
#                     personal_info['email'] = row.td.text.strip()
#                 except:
#                     personal_info['email'] = None
#             elif '주소' in check:
#                 try:
#                     personal_info['address'] = row.td.text.strip()
#                 except:
#                     personal_info['address'] = None
#             elif '홈페이지' in check:
#                 try:
#                     personal_info['homepage'] = row.td.text.strip()
#                 except:
#                     personal_info['homepage'] = None
#         except:
#             continue
#     work_info = {}
#     try:
#         work_place = soup2.find('div',class_='rsArea').text.strip()
#     except:
#         work_place = None
#     try:
#         work_days = soup2.find('div',class_='rsDate').text.strip()
#     except:
#         work_days = None
#     try:
#         work_style = soup2.find('div',class_='rsState').text.strip()
#     except:
#         work_style = None
#     try:
#         occ = soup2.find('div', class_='rsPart').text.strip()
#     except:
#         occ = None
#     try:
#         salary = soup2.find('div',class_='rsPay').text.strip()
#     except:
#         salary = None
#     try:
#         school = soup2.find('div',class_='rsSecSchool').find('div',class_='schoolWp').text.strip()
#     except:
#         school = None
#     work_info['work_place'] = work_place
#     work_info['work_style'] = work_style
#     work_info['work_days'] = work_days
#     work_info['salary'] = salary
#     work_info['occupation'] = occ
#     try:
#         hopes = soup2.find_all('div',class_='rsSec')
#     except:
#         hopes = []
#     wanted_things = {}
#     merits_strengths = []
#     hope_workplaces_list = []
#     try:
#         hope_workplaces = soup2.find('div',class_='rsSec rsSecArea').find_all('li')
#         for hope_workplace in hope_workplaces:
#             hope_workplaces_list.append(hope_workplace.text.strip())
#     except:
#         hope_workplaces_list = None
#     try:
#         hope_occ = soup2.find('div',class_='rsSec rsSecPart').text.strip().split('')
#     except:
#         hope_occ = None
#     try:
#         educ = soup2.find('div',class_='rsSec rsSecAchievement').text.strip()
#     except:
#         educ = None
#     try:
#         merits = soup2.find('div',class_='rsSec rsSecMerit').find_all('li')
#         for merit in merits:
#             merits_strengths.append(merit.text.strip())
#     except:
#         merits_strengths = None
#     wanted_things['hope_workplace'] = hope_workplaces_list
#     wanted_things['hope_occupation'] = hope_occ
#     wanted_things['education'] = educ
#     wanted_things['strengths'] = merits_strengths
#     careers_list = []
#     careers_dict = {}
#     try:
#         careers = soup2.find('div',class_='rsSec rsSecCareer').find_all('dl')
#         for c in careers:
#             careers_list.append(c)
#     except:
#         careers_list = None
#     try:
#         exp = soup2.find('div', class_='rsSec rsSecCareer').find('p',class_='career').text.strip()
#     except:
#         exp = None
#     try:
#         intro = soup2.find('div',class_='ggbCaution').text.strip()
#     except:
#         intro = None
#     careers_dict['careers'] = careers_list
#     careers_dict['experience'] = exp
#     work_preferece = {}
#     try:
#         works = soup2.find('div',class_='rsSec rsSecSensitive').find_all('div',class_='list')
#     except:
#         works = []
#
#     for w in works:
#         try:
#             check = w.find('h3',class_='tit').text
#             if '장애여부' in check:
#                 try:
#                     work_preferece['disablity'] = w.dd.text.strip()
#                 except:
#                     work_preferece['disablity'] = None
#             elif '병역사항' in check:
#                 try:
#                     work_preferece['military_service'] = w.dd.text.strip()
#                 except:
#                     work_preferece['military_service'] = None
#             elif '국가보훈' in check:
#                 try:
#                     work_preferece['national_vows'] = w.dd.text.strip()
#                 except:
#                     work_preferece['national_vows'] = None
#             elif '고용지원금' in check:
#                 try:
#                     work_preferece['employment_subsidy'] = w.dd.text.strip()
#                 except:
#                     work_preferece['employment_subsidy'] = None
#         except:
#             work_preferece = {}
#     temp['details']['work_info'] = work_info
#     temp['details']['work_preference'] = work_preferece
#     temp['details']['career_info'] = careers_dict
#     temp['details']['desired_things'] = wanted_things
#     temp['details']['headline'] = headline
#     temp['details']['revision_date'] = rev_date
#     temp['details']['personal_info'] = personal_info
#     temp['name'] = name
#     temp['age'] = age
#     temp['gender'] = gender
#     temp['career_info'] = career
#     temp['occupation'] = occup
#     temp['other_details'] = other_details
#     temp['posted_at'] = posted_at
#     temp['demands'] = demands
#     temp['details_url'] = details_url
#     albamon_arr.append(temp)
#
# albamonDict['data'] = albamon_arr
# pp.pprint(albamonDict)

page = '1'
count = '5'
keyword = 'google'

# headers = {
#     'Connection': 'keep-alive',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
#     'Accept': '*/*',
#     'Referer': 'http://www.alba.co.kr/search/Search.asp',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     'If-None-Match': '"5b6bf6d8:bb"',
#     'If-Modified-Since': 'Thu, 09 Aug 2018 08:10:00 GMT',
# }
#
# params = (
#     ('page', '{0}'.format(page)),
#     ('pagesize', '{0}'.format(count)),
#     ('Section', '0'),
#     ('WsSrchWord', '{0}'.format(keyword)),
# )
#
# albaDict = {}
# albaDict['success'] = True
# response = requests.get('http://www.alba.co.kr/search/Search.asp', headers=headers, params=params)
#
# soup = bs(response.content,'lxml')
#
# listitem_iterator = soup.find('ul',class_='jobNormal').find_all('li')
#
# total_count = soup.find('div',class_='searchJob').h2.em.text.strip()
# alba_data = []
#
# for item in listitem_iterator:
#     temp = {}
#     temp['details'] = {}
#     try:
#         title = item.find('p',class_='title').text.strip()
#     except:
#         title = None
#     try:
#         detail_url = item.find('p', class_='title').a.get('href')
#     except:
#         detail_url = None
#     try:
#         location = item.find('p',class_='info').find('span',class_='area').text.strip()
#     except:
#         location = None
#     try:
#         company = item.find('p', class_='info').find('span', class_='company').text.strip()
#     except:
#         company = None
#     try:
#         kw = item.find('p',class_='hotplace').find('span', class_='keyword').text.strip().split(',')
#     except:
#         kw = None
#     try:
#         reg_date = item.find('p', class_='etcInfo').find('span', class_='regDate').text.strip()
#     except:
#         reg_date = None
#     try:
#         deadline = item.find('p', class_='etcInfo').find('span', class_='deadline').text.strip()
#     except:
#         deadline = None
#     try:
#         payinfo = item.find('p',class_='payInfo').text.strip()
#     except:
#         payinfo = None
#
#     base_url = 'http://www.alba.co.kr'
#     detail_url = '{0}{1}'.format(base_url,detail_url)
#     req2 = requests.get(detail_url)
#     soup2 = bs(req2.content,'lxml')
#     try:
#         date_added = soup2.find('div',class_='update').find_all('em')[0].text.strip()
#     except:
#         date_added = None
#     try:
#         date_updated = soup2.find('div',class_='update').find_all('em')[1].text.strip()
#     except:
#         date_updated = None
#     try:
#         headline = soup2.find('p',class_='detailTitle').text.strip()
#     except:
#         headline = None
#     eligibity = {}
#     try:
#         eligibity_li = soup2.find('div',class_='infoQualify').ul.find_all('li')
#     except:
#         eligibity_li = []
#     for e in eligibity_li:
#         try:
#             check = e.span.text.strip()
#         except:
#             check = ''
#         if '경력' in check:
#             try:
#                 eligibity['career_experience'] = e.text.strip()
#             except:
#                 eligibity['career_experience'] = None
#         elif '성별' in check:
#             try:
#                 eligibity['sex'] = e.text.strip()
#             except:
#                 eligibity['sex'] = None
#         elif '연령무관' in check:
#             try:
#                 eligibity['age'] = e.text.strip()
#             except:
#                 eligibity['age'] = None
#         elif '학력' in check:
#             try:
#                 eligibity['education'] = e.text.strip()
#             except:
#                 eligibity['education'] = None
#     recruit = {}
#     try:
#         recruit_li = soup2.find('div', class_='infoContent divide').ul.find_all('li')
#     except:
#         recruit_li = []
#     for r in recruit_li:
#         try:
#             check = r.span.text.strip()
#         except:
#             check = ''
#         if '모집직종' in check:
#             try:
#                 recruit['occupation'] = r.text.strip()
#             except:
#                 recruit['occupation'] = None
#         elif '고용형태' in check:
#             try:
#                 recruit['employment_type'] = r.text.strip()
#             except:
#                 recruit['employment_type'] = None
#         elif '모집인원' in check:
#             try:
#                 recruit['no_applicants'] = r.text.strip()
#             except:
#                 recruit['no_applicants'] = None
#         elif '기타사항' in check:
#             try:
#                 recruit['other_items'] = r.text.strip()
#             except:
#                 recruit['other_items'] = None
#     work = {}
#     try:
#         work_li = soup2.find('div', class_='infoTerm').ul.find_all('li')
#     except:
#         work_li = []
#     for r in work_li:
#         try:
#             check = r.span.text.strip()
#         except:
#             check = ''
#         if '근무기간' in check:
#             try:
#                 work['working_period'] = r.text.strip()
#             except:
#                 work['working_period'] = None
#         elif '근무요일' in check:
#             try:
#                 work['working_day'] = r.text.strip()
#             except:
#                 work['working_day'] = None
#         elif '근무시간' in check:
#             try:
#                 work['working_hours'] = r.text.strip()
#             except:
#                 work['working_hours'] = None
#         elif '우대사항' in check:
#             try:
#                 work['preference'] = r.text.strip()
#             except:
#                 work['preference'] = None
#         elif '복리후생' in check:
#             try:
#                 work['welfare_benefits'] = r.text.strip()
#             except:
#                 work['welfare_benefits'] = None
#         elif '근무지주소' in check:
#             try:
#                 work['work_address'] = r.text.strip()
#             except:
#                 work['work_address'] = None
#         elif '인근지하철' in check:
#             try:
#                 work['nearby_subway'] = r.text.strip()
#             except:
#                 work['nearby_subway'] = None
#         elif '급여' in check:
#             try:
#                 work['salary'] = r.find('p',class_='pay').text.strip()
#             except:
#                 work['salary'] = None
#             try:
#                 work['pay_calculator'] = r.find('p',class_='calculator').text.strip()
#             except:
#                 work['pay_calculator'] = None
#         elif '핫플레이스' in check:
#             try:
#                 work['hotplace'] = r.text.strip()
#             except:
#                 work['hotplace'] = None
#     try:
#         detailed_content = soup2.find('div',id='DetailContent').text.strip()
#     except:
#         detailed_content = None
#     contact_info = {}
#     try:
#         contact_li = soup2.find('div',id='InfoApply').find('ul',class_='info').find_all('li')
#     except:
#         contact_li = []
#     for c in contact_li:
#         try:
#             check = c.span.text.strip()
#         except:
#             check = ''
#         if '모집마감일' in check:
#             try:
#                 contact_info['application_date'] = c.text.strip()
#             except:
#                 contact_info['application_date'] = None
#         elif '담당자명' in check:
#             try:
#                 contact_info['contact_person'] = c.text.strip()
#             except:
#                 contact_info['contact_person'] = None
#         elif '제출서류' in check:
#             try:
#                 contact_info['documents'] = c.text.strip()
#             except:
#                 contact_info['documents'] = None
#     try:
#         tel = soup2.find('dl',class_='modal-tel__tel').dd.text.strip()
#     except:
#         tel = None
#     contact_info['telephone'] = tel
#     workplace_info = {}
#     workplace = soup2.find('div',id='InfoWork').find('ul',class_='info').find_all('li')
#     for w in workplace:
#         try:
#             check = w.span.text.strip()
#         except:
#             check = ''
#         if '근무지명' in check:
#             try:
#                 workplace_info['workplace_name'] = w.text.strip()
#             except:
#                 workplace_info['workplace_name'] = None
#         elif '사업내용' in check:
#             try:
#                 workplace_info['business_contents'] = w.text.strip()
#             except:
#                 workplace_info['business_contents'] = None
#         elif '근무지주소' in check:
#             try:
#                 workplace_info['workplace_locations'] = w.text.strip()
#             except:
#                 workplace_info['workplace_locations'] = None
#         elif '직 원 수' in check:
#             try:
#                 workplace_info['no_employers'] = w.text.strip()
#             except:
#                 workplace_info['no_employers'] = None
#         elif '홈페이지' in check:
#             try:
#                 workplace_info['homepage'] = w.text.strip()
#             except:
#                 workplace_info['homepage'] = None
#     company_info = {}
#     company_li = soup2.find('div', id='InfoCompany').find('ul', class_='info').find_all('li')
#     for w in company_li:
#         try:
#             check = w.span.text.strip()
#         except:
#             check = ''
#         if '회 사 명' in check:
#             try:
#                 company_info['company_name'] = w.text.strip()
#             except:
#                 company_info['company_name'] = None
#         elif '사업내용' in check:
#             try:
#                 company_info['business_contents'] = w.text.strip()
#             except:
#                 company_info['business_contents'] = None
#         elif '회사주소' in check:
#             try:
#                 company_info['workplace_locations'] = w.text.strip()
#             except:
#                 company_info['workplace_locations'] = None
#         elif '직 원 수' in check:
#             try:
#                 company_info['total_employers'] = w.text.strip()
#             except:
#                 company_info['total_employers'] = None
#         elif '홈페이지' in check:
#             try:
#                 company_info['homepage'] = w.text.strip()
#             except:
#                 company_info['homepage'] = None
#         elif '대표자명' in check:
#             try:
#                 company_info['representative_name'] = w.text.strip()
#             except:
#                 company_info['representative_name'] = None
#         elif '대표자명' in check:
#             try:
#                 company_info['company_address'] = w.text.strip()
#             except:
#                 company_info['company_address'] = None
#
#     temp['details']['headline'] = headline
#     temp['details']['date_added'] = date_added
#     temp['details']['date_updated'] = date_updated
#     temp['details']['eligibility'] = eligibity
#     temp['details']['recruitment_details'] = recruit
#     temp['details']['working_condition'] = work
#     temp['details']['detailed_info'] = detailed_content
#     temp['details']['contact_info'] = contact_info
#     temp['details']['workplace_info'] = workplace_info
#     temp['details']['company_info'] = company_info
#     temp['title'] = title
#     temp['location'] = location
#     temp['company'] = company
#     temp['keywords'] = kw
#     temp['registration_date'] = reg_date
#     temp['deadline'] = deadline
#     temp['pay_info'] = payinfo
#     temp['detail_url'] = detail_url
#     alba_data.append(temp)
#
# albaDict['data'] = alba_data
# albaDict['total_count'] = total_count
# pp.pprint(albaDict)


import requests
#
# headers = {
#     'Connection': 'keep-alive',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Referer': 'http://www.alba.co.kr/resume/list/Main.asp',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
# }
#
# params = (
#     ('page', '1'),
#     ('pagesize', '50'),
# )
# albaDict  = {}
# albaDict['success'] = True
#
# response = requests.get('http://www.alba.co.kr/resume/list/Main.asp', headers=headers, params=dict(params))
#
# soup = bs(response.content,'lxml')
#
# regex = re.compile('clsList\d+')
# total_count = soup.find('p',class_='listCount').strong.text.strip()
# print(total_count)
# try:
#     card_iterator = soup.find('div',class_='listType').find_all('tr',{'class' : regex})
# except:
#     albaDict['data'] = []
#     card_iterator = []
#
# alba_data = []
# print(len(card_iterator))
# for card in card_iterator:
#     print('processing...')
#     temp = {}
#     temp['details'] = {}
#     try:
#         name = card.find('td',class_='name').text.strip().split('(')[0].strip()
#     except:
#         name = None
#     try:
#         gender = card.find('td',class_='name').find('span',class_='sexAge').text.strip().split('/')[0].replace('(','')
#     except:
#         gender = None
#     try:
#         age = card.find('td',class_='name').find('span',class_='sexAge').text.strip().split('/')[1].replace(')','')
#     except:
#         age = None
#     try:
#         title = card.find('td',class_='title').find('span',class_='title').text.strip()
#     except:
#         title = None
#     try:
#         detail_url = card.find('td',class_='title').find('a',class_='title').get('href')
#     except:
#         detail_url = None
#     try:
#         kind = card.find('td',class_='title').find('span',class_='kind').text.strip()
#     except:
#         kind = None
#     try:
#         exp = card.find('td',class_='license').find('span',class_='career').text.strip()
#     except:
#         exp = None
#     try:
#         cert = card.find('td',class_='license').find('span',class_='license').text.strip()
#     except:
#         cert = None
#     try:
#         loc = card.find('td',class_='local').text.strip()
#     except:
#         loc = None
#     try:
#         mod_date = card.find('td',class_='modDate').text.strip()
#     except:
#         mod_date = None
#     base_url = 'http://www.alba.co.kr'
#     detail_url = '{0}{1}'.format(base_url, detail_url)
#     req2 = requests.get(detail_url)
#     soup2 = bs(req2.content,'lxml')
#     try:
#         headline = soup2.find('div',class_='resumeWrap').h1.find('span',class_='title').text.strip()
#     except:
#         headline = None
#     try:
#         avail_time = soup2.find('span',class_='callstart').em.text.strip()
#     except:
#         avail_time = None
#     personal_info = {}
#     try:
#         personal = soup2.find('div',id='ResumeBaseInfo').find('ul',class_='infoList')
#     except:
#         personal  =[]
#     try:
#         personal_info['profile_name'] = personal.find('li',class_='name').text.strip()
#     except:
#         personal_info['profile_name'] = None
#     try:
#         personal_info['contact_no'] = personal.find('li',class_='contact').text.strip()
#     except:
#         personal_info['contact_no'] = None
#     try:
#         personal_info['address'] = personal.find('li',class_='address').text.strip()
#     except:
#         personal_info['address'] = None
#     try:
#         personal_info['mail'] = personal.find('li',class_='mail').text.strip()
#     except:
#         personal_info['mail'] = None
#     try:
#         personal_info['homepage'] = personal.find('li',class_='homepage').text.strip()
#     except:
#         personal_info['homepage'] = None
#
#     working_cond = {}
#     work = soup2.find('table',class_="resumeView-table").find_all('td')
#     for w in work:
#         check = w.find('dt',class_='title').text.strip()
#         if '근무기간' in check:
#             working_cond['employment_period'] = w.dd.text.strip()
#         elif '근무요일' in check:
#             working_cond['working_day'] = w.dd.text.strip()
#         elif '근무시간' in check:
#             working_cond['working_hours'] = w.dd.text.strip()
#         elif '근무형태' in check:
#             working_cond['working_style'] = w.dd.text.strip()
#         elif '희망급여' in check:
#             working_cond['hope_salary'] = w.dd.text.strip()
#     full_list = soup2.find('ul',class_='fullList').find_all('li')
#     for w in full_list:
#         check = w.find('span', class_='title').text.strip()
#         if '희망지역' in check:
#             working_cond['hope_locations'] = w.find('span',class_='result').text.strip().split(',')
#         elif '희망직종' in check:
#             working_cond['hope_occupation'] = w.find('span',class_='result').text.strip().split(',')
#     edu = {}
#     try:
#         final_edu = soup2.find('div',id='ResumeEducation').find('span',class_='desc').strong.text.strip()
#     except:
#         final_edu = None
#     edu['final_education'] = final_edu
#     try:
#         education = soup2.find('div',id='ResumeEducation').find_all('div',class_='infoArea')
#     except:
#         education = []
#     education_hist = []
#     for w in education:
#         temp_edu = {}
#         try:
#             year_range = w.find('div',class_='nameArea').text.strip()
#         except:
#             year_range = None
#         try:
#             edu_title = w.find('dl',class_='infoDetail').find('dt',class_='title').text.strip()
#         except:
#             edu_title = None
#         try:
#             types = w.find('dl', class_='infoDetail').find('dd', class_='type').text.strip()
#         except:
#             types = None
#         try:
#             status = w.find('dl', class_='infoDetail').find('dd', class_='date').text.strip()
#         except:
#             status = None
#         temp_edu['year_range'] = year_range
#         temp_edu['title'] = edu_title
#         temp_edu['status'] = status
#         temp_edu['type'] = types
#         education_hist.append(temp_edu)
#
#     edu['education_details'] = education_hist
#     career_info = {}
#     try:
#         careers = soup2.find('div',id='ResumeCareer').find('span',class_='desc').text.strip().replace('총경력','').strip()
#     except:
#         careers = None
#     career_info['experience'] = careers
#     try:
#         career_detail = soup2.find('div',id='ResumeCareer').find_all('div',class_='infoArea first')
#     except:
#         career_detail = []
#     # print(career_detail)
#     career_details = []
#     for c in career_detail:
#         temp_career = {}
#         try:
#             year_range_career = c.find('div', class_='nameArea').text.strip()
#         except:
#             year_range_career = None
#         try:
#             career_title = c.find('dl', class_='infoDetail').find('dt', class_='title').text.strip()
#         except:
#             career_title = None
#         try:
#             type = c.find('dl', class_='infoDetail').find('dd', class_='type').text.strip()
#         except:
#             type = None
#         try:
#             dur = c.find('dl', class_='infoDetail').find('dd', class_='date').text.strip()
#         except:
#             dur = None
#         try:
#             kind_title = c.find('dl', class_='infoDetail').find('dd', class_='kind').find('span',class_='title').text.strip()
#         except:
#             kind_title = None
#         try:
#             kind_career = c.find('dl', class_='infoDetail').find('dd', class_='kind').ul.text.strip()
#         except:
#             kind_career = None
#
#         temp_career['year_month_range'] = year_range_career
#         temp_career['duration'] = dur
#         temp_career['kind_title'] =kind_title
#         temp_career['kind'] = kind
#         temp_career['title'] = career_title
#         temp_career['type'] = type
#         career_details.append(temp_career)
#     career_info['career_details'] = career_details
#
#     temp['details']['headline'] = headline
#     temp['details']['available_time'] = avail_time
#     temp['details']['working_conditions'] = working_cond
#     temp['details']['personal_info'] = personal_info
#     temp['details']['education'] = edu
#     temp['details']['career'] = career_info
#     temp['name'] = name
#     temp['title'] = title
#     temp['age'] = age
#     temp['gender'] = gender
#     temp['kind'] = kind
#     temp['detail_url'] = detail_url
#     temp['career'] = exp
#     temp['desired_location'] = loc
#     temp['certificate'] = cert
#     temp['modified_date'] = mod_date
#     alba_data.append(temp)
#     print(alba_data)
#
# albaDict['data'] = alba_data
# albaDict['total_count'] = total_count
# # pp.pprint(albaDict)


from datetime import datetime
import requests

headers = {
    'Origin': 'https://ec.europa.eu',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'ajax-call': 'true',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://ec.europa.eu/eures/eures-searchengine/page/main?lang=en',
    'Connection': 'keep-alive',
}
params = (
    ('lang', 'en'),
    ('app', '2.0.1p2-build-0')
)

page = 1
count = 100

def eures_jobs(page=1,count=100):
    data = u'{"keywords":[],"positionScheduleCodes":[],"positionOfferingCodes":[],"educationLevelCodes":[],"euresFlagCodes":[],"nutsCodes":[],"notSpecifiedInNutsCodes":[],"requiredExperienceCodes":[],"solidarityContextCodes":[],"otherBenefitsCodes":[],"occupationUris":[],"includeJobsWithoutBenefits":false,"requiredLanguages":[],"includeJobsWithoutRequiredLanguages":false,"sortSearch":"MOST_RECENT","resultsPerPage":10,"page":1,"sessionId":"ayjgivltwyv8q7cwxl2s"}'
    data = json.loads(data)
    data['resultsPerPage'] = count
    data['page'] = page
    data = json.dumps(data)
    headers = {
        'Origin': 'https://ec.europa.eu',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'ajax-call': 'true',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://ec.europa.eu/eures/eures-searchengine/page/main?lang=en',
        'Connection': 'keep-alive',
    }
    params = (
        ('lang', 'en'),
        ('app', '2.0.1p2-build-0'),
    )
    response = requests.post('https://ec.europa.eu/eures/eures-searchengine/page/jv-search/search', headers=headers, params=params, data=data)

    eures_dict = {}
    try:
        total_results = response.json()['numberRecords']
    except:
        total_results = None
    try:
        page_results = len(response.json()['jvs'])
    except:
        page_results = None
    eures_dict['total_results'] = total_results
    eures_dict['count'] = page_results
    try:
        card_iterator = response.json()['jvs']
    except:
        card_iterator = []
    eures_data = []
    print(len(card_iterator))
    for card in card_iterator:
        temp = {}
        try:
            job_id = card['id']
        except:
            job_id = None
        try:
            creation_date = card['creationDate']
            creation_date = datetime.fromtimestamp(creation_date/1000)
        except:
            creation_date = None
        try:
            mod_date = card['lastModificationDate']
            mod_date = datetime.fromtimestamp(mod_date/1000)
        except:
            mod_date = None
        try:
            title = card['title']
        except:
            title = None
        try:
            desc = card['description']
        except:
            desc = None
        try:
            n_posts = card['numberOfPosts']
        except:
            n_posts = None
        try:
            loc = card['locationMap']
        except:
            loc = None
        try:
            job_categories = card['jobCategoriesCodes']
        except:
            job_categories = None
        try:
            emp_name = card['employer']['name']
        except:
            emp_name = None
        try:
            emp_website = card['employer']['website']
        except Exception as e:
            emp_website = None

        emp = {}
        emp['name'] = emp_name
        emp['website'] = emp_website
        temp['employer'] = emp
        temp['title'] = title
        temp['location'] = loc
        temp['job_id'] = job_id
        temp['creation_date'] = creation_date
        temp['modification_date'] = mod_date
        temp['description'] = desc
        temp['no_posts'] = n_posts
        temp['job_categories'] = job_categories

        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'ajax-call': 'true',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://ec.europa.eu/eures/eures-searchengine/page/main?lang=en',
            'Connection': 'keep-alive',
        }

        utc_now = int(time.time()*1000)
        params = (
            ('lang', 'en'),
            ('app', '2.0.1p2-build-0'),
            ('_', '{0}'.format(utc_now))
        )
        detail_url = 'https://ec.europa.eu/eures/eures-searchengine/page/jv/id/{0}'.format(job_id)
        response2 = requests.get(detail_url,headers=headers, params=params)
        response_json = response2.json()

        try:
            person_contacts = response_json['personContacts']
        except:
            person_contacts = None
        try:
            lang_code = response_json['requiredLanguages'][0]
        except:
            lang_code = None
        try:
            exp = response_json['requiredYearsOfExperience']
        except:
            exp = None
        try:
            salary = response_json['salary']
        except:
            salary = None
        try:
            start_date = response_json['startDate']
            start_date = datetime.fromtimestamp(start_date/1000)
        except Exception as e:
            print(e)
            start_date = None
        try:
            end_date = response_json['endDate']
            end_date = datetime.fromtimestamp(end_date/1000)
        except:
            end_date = None
        try:
            source = response_json['source']
        except:
            source = None
        try:
            edu_level_code = response_json['requiredEducationLevelCode']
        except:
            edu_level_code = None
        try:
            position_type_code = response_json['positionTypeCode']
        except:
            position_type_code = None
        try:
            contract_type_code = response_json['contractTypeCodes'][0]
        except:
            contract_type_code = None
        try:
            license = response_json['requiredDrivingLicenses']
        except:
            license = None
        try:
            country_code = list(loc.keys())[0].upper()
        except:
            country_code = None
        try:
            region_code = loc[country_code][0].upper()
        except:
            region_code = None
        try:
            sector_code = response_json['employer']['sectorCodes'][0].upper()
        except:
            sector_code = None
        try:
            app_details = response_json['applicationInstructions'][0]
        except:
            app_details = None

        headers = {
            'Origin': 'https://ec.europa.eu',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'ajax-call': 'true',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://ec.europa.eu/eures/eures-searchengine/page/main?lang=en',
            'Connection': 'keep-alive',
        }

        params = (
            ('app', '2.0.1p2-build-0'),
        )

        data = '["global.reg2018.position.type.{0}","global.reg2018.contract.type.{1}","global.country.{2}","global.nuts2013.{3}","global.nace.{4}","global.language.{5}"]'.format(position_type_code,contract_type_code,country_code,region_code,sector_code,lang_code)

        response3 = requests.post('https://ec.europa.eu/eures/eures-searchengine/page/i18n/messages/en', headers=headers,params=params, data=data)

        response3_json = response3.json()
        try:
            position_type = response3_json['global.reg2018.position.type.{0}'.format(position_type_code)]
        except:
            position_type = None
        try:
            contract_type = response3_json['global.reg2018.contract.type.{0}'.format(contract_type_code)]
        except:
            contract_type = None
        try:
            country = response3_json['global.country.{0}'.format(country_code)]
        except:
            country = None
        try:
            region = response3_json['global.nuts2013.{0}'.format(region_code)]
        except:
            region = None
        try:
            sector = response3_json['global.nace.{0}'.format(sector_code.upper())]
        except:
            sector = None
        try:
            lang = response_json['global.language.{0}'.format(lang_code)]
        except:
            lang = None
        try:
            job_vac_id = response_json['documentId']
        except:
            job_vac_id = None

        if exp is not None:
            exp = '{0} {1}'.format(str(exp),'years')

        if 'global' in region:
            region = None

        temp['required_language'] = lang
        temp['personal_contacts'] = person_contacts
        temp['source'] = source
        temp['sector'] = sector

        job_req = {}
        job_req['driving_license'] = license
        job_req['education_level'] = edu_level_code
        job_req['experience'] = exp
        job_info = {}
        job_info['contract_type'] = contract_type
        job_info['position_type'] = position_type
        job_info['salary'] = salary
        job_info['start_date'] = start_date
        job_info['end_date'] = end_date

        temp['job_requirements'] = job_req
        temp['job_info'] = job_info
        temp['application_details'] = app_details
        temp['job_vacancy_id'] = job_vac_id

        loc_map = {}
        loc_map['country'] = country
        loc_map['region'] = region
        temp['location'] = loc_map


        eures_data.append(temp)

    eures_dict['data'] = eures_data
    return eures_dict

   # job_categories_details = []
   #          for cat in job_categories:
   #              try:
   #                  response_ = proxied_request('http://ec.europa.eu/esco/portal/occupation?uri={0}&conceptLanguage=en&full=true'.format(cat))
   #                  logger.info('succesful request to job category for {0}'.format(cat))
   #              except Exception as e:
   #                  response_ =
   #                  logger.warning('request to job category details  {0} failed : {1}'.format(cat,str(e)))
   #
   #              soup = bs(response_.content, 'lxml')
   #              temp_={}
   #              try:
   #                  head = soup.find('div', class_='article-tools').h1.text.strip()
   #              except:
   #                  head = None
   #              try:
   #                  description = soup.find('div', class_='content-container').pre.text.strip()
   #              except:
   #                  description = None
   #              try:
   #                  isco_code = soup.find('div', class_='content-container').p.text.strip()
   #              except:
   #                  isco_code = None
   #              try:
   #                  hirarchy = soup.find('ul', id='hierarchy').text.strip()
   #              except:
   #                  hirarchy = None
   #              temp_['title'] = head
   #              temp_['description'] = description
   #              temp_['isco_code'] = isco_code
   #              temp_['hierarchy'] = hirarchy
   #              job_categories_details.append(temp_)
# i = 'http://data.europa.eu/esco/isco/C5223'
# j = 'https://ec.europa.eu/esco/portal/occupation?uri={0}&conceptLanguage=en&full=true'.format(i)
#
# response_ = requests.get(j)
# soup = bs(response_.content,'lxml')
#
# print(soup.find('div',class_='article-tools').h1.text.strip())
# print(soup.find('div',class_='content-container').pre.text.strip())
# print(soup.find('ul',id='hierarchy').text.strip())

datas = """
 <div class="content">
 <h2 class="pub-job_ad_content_description_section-title">Job summary</h2>
    <p>My international Private Equity Client is setting up an office in Frankfurt, Germany and they are looking for a bi-lingual English and German speaker to oversee the setting up of the office and to support the Executives from an EA standpoint.</p>
 <h2 class="pub-job_ad_content_description_section-title">Job description</h2>
    <p><p>It is a small satellite operation to begin with, but one where activity is expected to increase markedly given the company does a lot of business in Germany.</p>
<p><br />You need to be happy working as part of a small team to begin with and ideally have experience of setting up systems etc. You'll be liaising with the other international offices a lot and on the other side will be providing EA support, so need utmost confidence in managing calendars across different timezones and organising busy and ever-changing diaries.</p>
<p><br />This is a super business where you'll be well looked after, Great benefits too. Please send your CV if interested.</p>
<p>Sal: £40,000-£55,000 bonus and benefits</p></p>

                                                            <h2 class="pub-job_ad_content_description_section-title">Job qualifications</h2>
                                <p><p>Bi-lingual English and German.</p>
<p>Office Manager / Executive Assistant experience. </p></p>
                                                    
                                                    <div class="pub-job_ad_content_footer">
                                <a id="apply-button" href="#apply-form" class="pub-job_ad_apply_button btn btn-lg btn-primary">Apply</a>
                            </div>
                        </div>
"""

#
# soups = bs(datas,'lxml')
#
# hp = soups.find_all(['p','h2'])
# for h in hp:
#     try:
#         check = h.h2.text
#     except:
#         check = ''
#

def jobsInNetwork(page='1'):
    jobsDict = {}
    jobsDict['success'] = True
    job_url = 'https://www.jobsinnetwork.com/?page={0}'.format(page)
    response = requests.get(job_url)
    soup = bs(response.content,'lxml')

    total_count = soup.find('h1',class_='pub-search-results_title').text.strip()
    total_count = re.findall('\d+,\d+',total_count)[0].replace(',','')

    jobs_iterator = soup.find('div',class_='jobs').find_all('article')
    jobs_data = []
    for job in jobs_iterator:
        temp = {}
        temp['details'] = {}
        try:
            label = job.find('div',class_='job-label').text.strip()
        except:
            label = None
        try:
            title = job.find('h1',class_='job-title').text.strip()
        except:
            title = None
        try:
            comp = job.find('span',class_='job-details-company').text.strip()
        except:
            comp = None
        try:
            loc = job.find('span', class_='job-details-location').text.strip()
        except:
            loc = None
        try:
            desc = job.find('p', class_='description').text.strip()
        except:
            desc = None
        try:
            pub_date = job.find('span', class_='job-publication-date').text.strip()
        except:
            pub_date = None
        try:
            source = job.find('span', class_='job-source').text.strip()
        except:
            source = None
        try:
            detail_url = job.find('h1', class_='job-title').find('a').get('href')
        except:
            detail_url = None
        temp['title'] = title
        temp['source'] = source
        temp['label'] = label
        temp['company'] = comp
        temp['publication_time'] = pub_date
        temp['location'] = loc
        temp['description'] = desc
        temp['detail_url'] = detail_url
        jobs_data.append(temp)
        # try:
        #     response_ = requests.get(detail_url)
        # except Exception as e:
        #     print(e)
        #
        # soup_ = bs(response_.content,'lxml')
        # try:
        #     listitems = soup_.find('ul',class_='pub-job_ad_details_list').find_all('li')
        # except:
        #     listitems = []
        # job_info = {}
        # for li in listitems:
        #     check = li.find('span',class_='pub-job_ad_details_label').text.strip()
        #     if 'Company:' in check:
        #         try:
        #             job_info['company_name'] = li.text.replace('Company:','').strip()
        #         except:
        #             job_info['company_name'] = None
        #     elif 'Job Location:' in check:
        #         try:
        #             job_info['location'] = li.text.replace('Job Location:','').strip()
        #         except:
        #             job_info['location'] = None
        #     elif 'Date:' in check:
        #         try:
        #             job_info['date'] = li.text.replace('Date:','').strip()
        #         except:
        #             job_info['date'] = None
        #     elif 'Employment Type:' in check:
        #         try:
        #             job_info['employment_type'] = li.text.replace('Employment Type:','').strip()
        #         except:
        #             job_info['employment_type'] = None
        #     elif 'Experience:' in check:
        #         try:
        #             job_info['experience'] = li.text.replace('Experience:','').strip()
        #         except:
        #             job_info['experience'] = None
        #     elif 'Job Functions:' in check:
        #         try:
        #             job_info['function'] = li.text.replace('Job Functions:','').strip()
        #         except:
        #             job_info['function'] = None
        #     elif 'Internal reference:' in check:
        #         try:
        #             job_info['internal_reference'] = li.text.replace('Internal reference:','').strip()
        #         except:
        #             job_info['internal_reference'] = None

        # try:
        #     company_info = soup_.find('div',class_='pub-job_ad_content_company_info').text.strip()
        # except:
        #     company_info = None
        #
        # try:
        #     check_ = soup_.find('div',class_='content').find_all('h2',class_='pub-job_ad_content_description_section-title')
        # except:
        #     check_ = []



        jobsDict['data'] = jobs_data
        jobsDict['total_count'] = total_count
        return jobsDict
#
# # pp.pprint(jobsDict)

def indicatorComponent(topic,soup2):
    regex_ind = re.compile('economySubIndicator\w+_{0}'.format(topic))
    regex_comp = re.compile('economyTopicComponent\w+_{0}'.format(topic))
    try:
        indicator = json.loads(soup2.find('input', id=regex_ind).get('value'))
    except:
        indicator = None
    try:
        component = json.loads(soup2.find('input', id=regex_comp).get('value'))
    except:
        component = None

    return indicator,component

def procedures(topic,soup2):
    regex_procedures = re.compile('\b(?!economySub.+|!economyTopicComponent.+)\b\S+_{0}'.format(topic))
    try:
        procedures = soup2.find_all('input',id=regex_procedures)
    except:
        procedures = []
    proc = []
    for p in procedures:
        proc.append(json.loads(p))

    return proc

def topicConstructor(indicator,component,procedures):
    temp_={}
    temp_['indicator'] = indicator
    temp_['topic_component'] = component
    temp_['procedures'] = procedures

    return temp_

def doing_business():
    doingBuz = {}
    doingBuz['success'] = True

    response = requests.get('http://www.doingbusiness.org/rankings')
    soup = bs(response.content,'lxml')

    rank_data = soup.find('input',id='rankingDataSource').get('value')
    rank_json = json.loads(rank_data)
    rank_json_table = json.loads(rank_json['RankingDataTableJson'])

    doing_buz_data = []
    for economy in rank_json_table:
        temp = {}
        temp['data'] = economy
        temp['details'] = {}
        end_point = economy['EconomyURLName']
        economy_url = 'http://www.doingbusiness.org/data/exploreeconomies/{0}'.format(end_point)

        response2 = requests.get(economy_url)

        soup2 = bs(response2.content,'lxml')

        table_char = soup2.find('table',class_='table economy-characteristics-table').find_all('tr')

        economy_char = {}
        for t in table_char:
            try:
                check = t.th.text
            except:
                check = ''
            if 'Region' in check:
                try:
                    economy_char['region'] = t.td.text.strip()
                except:
                    economy_char['region'] = None
            elif 'Income Category' in check:
                try:
                    economy_char['income_category'] = t.td.text.strip()
                except:
                    economy_char['income_category'] = None
            elif 'Population' in check:
                try:
                    economy_char['population'] = t.td.text.strip()
                except:
                    economy_char['population'] = None
            elif 'GNI' in check:
                try:
                    economy_char['gni_per_capita_usd'] = t.td.text.strip()
                except:
                    economy_char['gni_per_capita_usd'] = None
            elif 'City' in check:
                try:
                    economy_char['city_covered'] = t.td.text.strip()
                except:
                    economy_char['city_covered'] = None

            temp['details']['economy_characteristics'] = economy_char

            dtf_data = soup2.find('input',id='economyOverallAggregatesJson').get('value')
            dtf_json = json.loads(dtf_data)

            temp['details']['distance_to_frontier'] = dtf_json

            eco_topic_breakdown = soup2.find('input',id='economyTopicBreakdownJson').get('value')
            eco_topic_breakdown_json = json.loads(eco_topic_breakdown)

            temp['details']['topic_breakdown'] = eco_topic_breakdown_json

            indicator_sb,component_sb = indicatorComponent('sb',soup2)
            indicator_dwcp, component_dwcp = indicatorComponent('dwcp', soup2)
            indicator_ge, component_ge = indicatorComponent('ge', soup2)
            indicator_rp, component_rp = indicatorComponent('rp', soup2)
            indicator_gc, component_gc = indicatorComponent('gc', soup2)
            indicator_pi, component_pi = indicatorComponent('pi', soup2)
            indicator_tax, component_tax = indicatorComponent('tax', soup2)
            indicator_tab, component_tab = indicatorComponent('tab', soup2)
            indicator_ec, component_ec = indicatorComponent('ec', soup2)
            indicator_ri, component_ri = indicatorComponent('ri', soup2)

            procedures_sb = procedures('sb',soup2)
            procedures_dwcp = procedures('dwcp', soup2)
            procedures_ge = procedures('ge', soup2)
            procedures_rp = procedures('rp', soup2)
            procedures_gc = procedures('gc', soup2)
            procedures_pi = procedures('pi', soup2)
            procedures_tax = procedures('tax', soup2)
            procedures_tab = procedures('tab', soup2)
            procedures_ec = procedures('ec', soup2)
            procedures_ri = procedures('ri', soup2)

            sb = topicConstructor(indicator_sb,component_sb,procedures_sb)
            dwcp = topicConstructor(indicator_dwcp, component_dwcp, procedures_dwcp)
            ge = topicConstructor(indicator_ge, component_ge, procedures_ge)
            rp = topicConstructor(indicator_rp, component_rp, procedures_rp)
            gc = topicConstructor(indicator_gc, component_gc, procedures_gc)
            pi = topicConstructor(indicator_pi, component_pi, procedures_pi)
            tax = topicConstructor(indicator_tax, component_tax, procedures_tax)
            tab = topicConstructor(indicator_tab, component_tab, procedures_tab)
            ec = topicConstructor(indicator_ec, component_ec, procedures_ec)
            ri = topicConstructor(indicator_ri, component_ri, procedures_ri)

            temp['details']['topics_explored_view'] = {}
            temp['details']['Starting_a_Business'] = sb
            temp['details']['Dealing_with_Construction_Permits'] = dwcp
            temp['details']['Getting_Electricity'] = ge
            temp['details']['Registering_Property'] = rp
            temp['details']['Getting_Credit'] = gc
            temp['details']['Protecting_Minority_Investors'] = pi
            temp['details']['Paying_Taxes'] = tax
            temp['details']['Trading_across_Borders'] = tab
            temp['details']['Enforcing_Contracts'] = ec
            temp['details']['Resolving_Insolvency'] = ri

            response3 = requests.get('http://www.doingbusiness.org/reforms/overview/economy/{0}'.format(end_point))
            soup3 = bs(response3.content,'lxml')

            reforms = json.loads(soup3.find('input',id='reformDetailsDataSource').get('value'))
            temp['details']['Reforms'] = reforms
            doing_buz_data.append(temp)

    doingBuz['data'] = doing_buz_data
    return doingBuz

# request = requests.get('http://www.doingbusiness.org/~/media/WBG/DoingBusiness/Documents/Profiles/Country/KOR.pdf')
#
# # print(request.content.encode('utf8'))
#
# request2 = proxied_request('https://www.countries-ofthe-world.com/world-time-zones.html')
# # print(request2.status_code)
#
# end_point = 'côte-divoire'
# res = requests.get('http://www.doingbusiness.org/data/exploreeconomies/{0}'.format(end_point))
# print(res.content)

def factGenerator(rows):
    factArr = []
    for r in rows:
        temp = {}
        try:
            temp['fact'] = r.find_all('td')[0].text.strip()
        except:
            temp['fact'] = None
        try:
            temp['value'] = r.find_all('td')[-1].text.strip()
        except:
            temp['value'] = None
        factArr.append(temp)

    return factArr

def census_data():
    try:
        censusData = {}
        censusData['success'] = True

        response = requests.get('https://www.census.gov/quickfacts/fact/table/floridacitycityflorida/PST045217')
        soup = bs(response.content,'lxml')

        try:
            rows_p = soup.find('tbody', { 'data-topic' : "Population" }).find_all('tr',class_='fact')
        except:
            rows_p = []
        try:
            rows_as = soup.find('tbody', { 'data-topic' : "Age and Sex" }).find_all('tr',class_='fact')
        except:
            rows_as = []
        try:
            rows_rho = soup.find('tbody', { 'data-topic' : "Race and Hispanic Origin" }).find_all('tr',class_='fact')
        except:
            rows_rho = []
        try:
            rows_pc = soup.find('tbody', { 'data-topic' : "Population Characteristics" }).find_all('tr',class_='fact')
        except:
            rows_pc = []
        try:
            rows_h = soup.find('tbody', { 'data-topic' : "Housing" }).find_all('tr',class_='fact')
        except:
            rows_h = []
        try:
            rows_fla = soup.find('tbody', { 'data-topic' : "Families & Living Arrangements" }).find_all('tr',class_='fact')
        except:
            rows_fla = []
        try:
            rows_e = soup.find('tbody', { 'data-topic' : "Education" }).find_all('tr',class_='fact')
        except:
            rows_e = []
        try:
            rows_hth = soup.find('tbody', { 'data-topic' : "Health" }).find_all('tr',class_='fact')
        except:
            rows_hth = []
        try:
            rows_eco = soup.find('tbody', { 'data-topic' : "Economy" }).find_all('tr',class_='fact')
        except:
            rows_eco = []
        try:
            rows_t = soup.find('tbody', { 'data-topic' : "Transportation" }).find_all('tr',class_='fact')
        except:
            rows_t = []
        try:
            rows_ip = soup.find('tbody', { 'data-topic' : "Income & Poverty" }).find_all('tr',class_='fact')
        except:
            rows_ip = []
        try:
            rows_bus = soup.find('tbody', { 'data-topic' : "Businesses" }).find_all('tr',class_='fact')
        except:
            rows_bus = []
        try:
            rows_geo = soup.find('tbody', { 'data-topic' : "Geography" }).find_all('tr',class_='fact')
        except:
            rows_geo = []

        data = {}
        ppl,buzs,geog = [{} for j in range(3)]

        facts_pop = factGenerator(rows_p)
        facts_eco = factGenerator(rows_eco)
        facts_hth = factGenerator(rows_hth)
        facts_h = factGenerator(rows_h)
        facts_as = factGenerator(rows_as)
        facts_rho = factGenerator(rows_rho)
        facts_trans = factGenerator(rows_t)
        facts_ip = factGenerator(rows_ip)
        facts_geo = factGenerator(rows_geo)
        facts_fla = factGenerator(rows_fla)
        facts_pc = factGenerator(rows_pc)
        facts_e = factGenerator(rows_e)
        facts_bus = factGenerator(rows_bus)

        print()
        ppl['population'] = facts_pop
        ppl['age_and_sex'] = facts_as
        ppl['race_and_hispanic_origin'] = facts_rho
        ppl['population_characteristics'] = facts_pc
        ppl['housing'] = facts_h
        ppl['families_and_living_arrangements'] = facts_fla
        ppl['education'] = facts_e
        ppl['health'] = facts_hth
        ppl['economy'] = facts_eco
        ppl['transportation'] = facts_trans
        ppl['income_and_poverty'] = facts_ip
        buzs['businesses'] = facts_bus
        geog['geography'] = facts_geo

        data['people'] = ppl
        data['businesses'] = buzs
        data['geography'] = geog
        censusData['data'] = data

        return censusData
    except Exception as e:
        print(str(e))
        return None

# pp.pprint(census_data())

# census_data()

def bls_category(t,year,month,index):
    temp = {}
    try:
        temp['year'] = year
    except:
        temp['year'] = None
    try:
        temp['month'] = month
    except:
        temp['month'] = None
    try:
        temp['value'] = t.find_all('td')[index].text.strip()
    except:
        temp['value'] = None
    return temp


def bls_explored(t,key):
    arr = []
    temp1 = bls_category(t, '2017', 'May', key)
    temp2 = bls_category(t, '2018', 'May', key+1)
    temp3 = bls_category(t, '2017', 'June', key+2)
    temp4 = bls_category(t, '2018', 'June', key+3)
    arr.append(temp1)
    arr.append(temp2)
    arr.append(temp3)
    arr.append(temp4)

    return arr

def bls_data():
    blsData = {}
    blsData['success'] = True

    resp = requests.get('https://www.bls.gov/news.release/metro.htm')
    soup = bs(resp.content,'lxml')
    table = soup.find('table',id='lau_metro_m1').tbody.find_all('tr')
    data = []
    print(len(table))
    for t in table:
        obj ={}
        try:
            obj['location'] = t.th.text.strip()
        except:
            obj['location'] = None
        try:
            obj['civilian_labour_force'] = bls_explored(t,0)
        except:
            obj['civilian_labour_force'] = None
        obj['unemployed'] = {}
        try:
            obj['unemployed']['number'] = bls_explored(t,4)
        except:
            obj['unemployed']['number'] = None
        try:
            obj['unemployed']['percent'] = bls_explored(t,8)
        except:
            obj['unemployed']['percent'] = None
        try:
            check = t.th.p.get('class')
        except:
            check = ''
        try:
            if 'sub0' in check:
                obj['type'] = 'state'
            elif 'sub1' in check:
                obj['type'] = 'city'
        except:
            obj['type'] = None
        data.append(obj)
    blsData['data'] = data
    return blsData

# pp.pprint(bls_data())

def surname_script():
    pages_indian = '0'
    pages_chinese = '0'
    surnameDict = {}
    surnameDict['success'] = True
    data_indian = []
    data_china = []
    while int(pages_indian) <= 5:
        url = 'https://www.familyeducation.com/baby-names/browse-origin/surname/indian?page={0}'.format(pages_indian)
        response = requests.get(url)
        soup = bs(response.content,'lxml')
        items = soup.find('section',class_='clearfix').find_all('li')
        for item in items:
            if 'page' in item.text.lower():
                continue
            data_indian.append(item.text.strip())
        pages_indian = str(int(pages_indian) + 1)
    while int(pages_chinese) <= 7:
        url_ = 'https://www.familyeducation.com/baby-names/browse-origin/surname/chinese?page={0}'.format(pages_chinese)
        response = requests.get(url_)
        soup = bs(response.content,'lxml')
        items = soup.find('section',class_='clearfix').find_all('li')
        for item in items:
            if 'page' in item.text.lower():
                continue
            data_china.append(item.text.strip())
        pages_chinese = str(int(pages_chinese) + 1)

    surnameDict['data_chinese'] = data_china
    surnameDict['data_indian'] = data_indian
    return surnameDict

# pp.pprint(surname_script())

def explore_economy(detail_url,flag):
    res = requests.get('https://www.theglobaleconomy.com{0}'.format(detail_url))
    soup = bs(res.content,'lxml')
    graph = soup.find_all('script')[7].text
    if flag == 0:
        graph_data = re.findall('graph_data = .+?(?=\;)',graph)[0].replace('graph_data = ','').strip()
    elif flag == 1:
        graph_data = re.findall('graphData = .+?(?=\;)', graph)[0].replace('graphData = ', '').strip()
    graph_data = json.loads(graph_data)
    return graph_data

def theglobaleconomy_index(category,keys = []):
    globalDict = {}
    globalDict['success'] = True
    url = 'https://www.theglobaleconomy.com/rankings/{0}/'.format(category)
    resp = requests.get(url)
    soup = bs(resp.content,'lxml')

    data_ = soup.find('input',id='export_data').get('value')
    data_ = re.findall('data=.+?(?=\&)',data_)[0]
    data_ = data_.replace('data=','').replace('&','').split(',')
    cards = soup.find('div',class_='outsideLinks').find_all('div')
    del cards[0]
    print(len(data_))
    print(len(cards))
    data = []
    for n,(card,value) in enumerate(zip(cards,data_)):
        temp = {}
        try:
            temp[keys[0]] = re.findall('\D+',card.text.strip())[0].replace('.','').strip()
        except:
            temp[keys[0]] = None
        try:
            temp[keys[1]] = value
        except:
            temp[keys[1]] = None
        try:
            temp[keys[2]] = card.find('a',class_='graph_outside_link').get('href')
        except:
            temp[keys[2]] = None
        try:
            temp[keys[3]] = str(n+1)
        except:
            temp[keys[3]] = None
        try:
            temp[keys[4]] = explore_economy(temp[keys[2]],flag=0)
        except:
            temp[keys[4]] = None
        data.append(temp)

    globalDict['data'] = data
    return globalDict

def theglobaleconomy_table(category,keys = []):
    globalDict = {}
    globalDict['success'] = True
    url = 'https://www.theglobaleconomy.com/rankings/{0}/'.format(category)
    resp = requests.get(url)
    soup = bs(resp.content,'lxml')

    cards = soup.find_all('div',class_='benchmarkTableRow')
    data = []
    for card in cards:
        temp = {}
        all_col = card.find_all('div')
        try:
            temp[keys[0]] = all_col[0].text.strip()
        except:
            temp[keys[0]] = None
        try:
            temp[keys[1]] = all_col[1].text.strip()
        except:
            temp[keys[1]] = None
        try:
            temp[keys[2]] = all_col[2].text.strip()
        except:
            temp[keys[2]] = None
        try:
            temp[keys[3]] = all_col[3].text.strip()
        except:
            temp[keys[3]] = None
        try:
            temp[keys[4]] = all_col[4].text.strip()
        except:
            temp[keys[4]] = None
        try:
            temp[keys[5]] = all_col[0].a.get('href')
        except:
            temp[keys[5]] = None
        try:
            temp[keys[6]] = explore_economy(temp[keys[5]],flag=1)
        except:
            temp[keys[6]] = None
        data.append(temp)
    globalDict['data'] = data
    return globalDict



# def nces_data(table_no,keys=[]):
#     url = 'https://nces.ed.gov/programs/digest/d17/tables/dt17_{0}.asp'.format(table_no)
#     resp = requests.get(url)
#     soup = bs(resp.content,'lxml')
#     iterator = soup.find('table',class_='tabletop tableMain tableWidth tableBracketRow').tbody.find_all('tr')
#     data = []
#     for iter in iterator:
#         temp = {}
#         cool = iter.find_all('td')
#         try:
#             th = iter.th
#             unwanted = th.sup
#             unwanted.extract()
#             temp[keys[0]] = th.text.strip()
#         except:
#             temp[keys[0]] = None
#         for i in range(1,len(keys)):
#             try:
#                 temp[keys[i]] = '{0} {1}'.format(cool[2*(i-1)].text.strip(),cool[2*(i-1)+1].text.strip())
#             except:
#                 temp[keys[i]] = None
#         data.append(temp)
#     return data


# pp.pprint(nces_data(table_no='302.20',keys=['year',
# 'total_percent_of_recent_high_school_completers_enrolled_in_college',
# 'white_percent_of_recent_high_school_completers_enrolled_in_college',
# 'black_percent_of_recent_high_school_completers_enrolled_in_college',
# 'hispanic_percent_of_recent_high_school_completers_enrolled_in_college',
# 'asian_percent_of_recent_high_school_completers_enrolled_in_college',
# 'total_percent_of_recent_high_school_completers_enrolled_in_college_3y_moving_avg',
# 'white_percent_of_recent_high_school_completers_enrolled_in_college_3y_moving_avg',
# 'black_percent_of_recent_high_school_completers_enrolled_in_college_3y_moving_avg',
# 'hispanic_percent_of_recent_high_school_completers_enrolled_in_college_3y_moving_avg',
# 'asian_percent_of_recent_high_school_completers_enrolled_in_college_3y_moving_avg',
# 'white_black_difference_bw_percent_enrolled',
# 'white_hispanic_difference_bw_percent_enrolled',
# 'white_asian_difference_bw_percent_enrolled']))
# #
# pp.pprint(nces_data(table_no='302.10',keys=['year',
# 'total_number_of_high_school_completers_enrolled_in_college',
# 'number_of_males_high_school_completers_enrolled_in_college',
# 'number_of_females_high_school_completers_enrolled_in_college',
# 'total_percent_of_high_school_completers_enrolled_in_college',
# 'total_percent_of_high_school_completers_enrolled_in_college_2y_college',
# 'total_percent_of_high_school_completers_enrolled_in_college_4y_college',
# 'total_percent_of_high_school_completers_enrolled_in_college_males',
# 'total_percent_of_high_school_completers_enrolled_in_college_males_2y_college',
# 'total_percent_of_high_school_completers_enrolled_in_college_males_4y_college',
# 'total_percent_of_high_school_completers_enrolled_in_college_females',
# 'total_percent_of_high_school_completers_enrolled_in_college_females_2y_college',
# 'total_percent_of_high_school_completers_enrolled_in_college_females_4y_college']))
#
# pp.pprint(nces_data(table_no='302.30',keys=['year',
# 'total_percent_of_high_school_completers_enrolled_in_college',
# 'percent_of_high_school_completers_enrolled_in_college_low_income',
# 'percent_of_high_school_completers_enrolled_in_college_middle_income',
# 'total_percent_of_high_school_completers_enrolled_in_college',
# 'total_percent_of_high_school_completers_enrolled_in_college_2y_college',
# 'total_percent_of_high_school_completers_enrolled_in_college_4y_college',
# 'total_percent_of_high_school_completers_enrolled_in_college_males',
# 'total_percent_of_high_school_completers_enrolled_in_college_males_2y_college',
# 'total_percent_of_high_school_completers_enrolled_in_college_males_4y_college',
# 'total_percent_of_high_school_completers_enrolled_in_college_females',
# 'total_percent_of_high_school_completers_enrolled_in_college_females_2y_college',
# 'total_percent_of_high_school_completers_enrolled_in_college_females_4y_college']))

def souper(url):
    resp = requests.get(url)
    soup = bs(resp.content,'lxml')
    return soup
pair_change = ['location', 'latest_data_from', 'latest_value', 'change_three_months', 'change_twelve_months','details_url', 'graph_data']
pair_value = ['location', 'latest_data_from', 'latest_value', 'value_three_months_ago', 'value_twelve_months_ago','details_url', 'graph_data']

def the_global_economy_pattern():
    base_url = 'https://www.theglobaleconomy.com'
    url = 'https://www.theglobaleconomy.com/indicators_list.php'
    resp = requests.get(url)
    soup = bs(resp.content,'lxml')
    cat_sub = [[sub.text.strip(), sub.parent.parent.find('div', class_='indicatorsCategoryTitle').text.strip(),sub.a.get('href')] for sub in soup.find_all('div',class_='indicatorsName')]
    pattern_dict = {}

    for cat in cat_sub:
        soup = souper('{0}{1}'.format(base_url,cat[2]))
        check = soup.find('div',class_='outsideLinks')
        try:
            check_ = soup.find('div',id='sort3months').text
        except:
            check_ =None
        if check:
            cat.append('index')
            cat.append([cat[2].split('/')[-2]])
        else:
            cat.append('table')
            if 'Value' in check_:
                cat.append(pair_value)
            elif 'Change' in check_:
                cat.append(pair_change)

    pattern_dict['sub_categories'] = cat_sub
    return pattern_dict
#
# print(the_global_economy_pattern())
#
# soup = souper('https://www.theglobaleconomy.com/rankings/GDP_per_capita_current_dollars/')

# print(soup.find('div',class_='outsideLinks'))

country_urls = ['study-in-usa','study-in-germany','study-in-canada','study-in-australia','study-in-singapore','study-in-australia','study-in-new-zealand','study-in-france','study-in-japan','study-in-united-kingdom','study-in-ireland','study-in-netherlands','study-in-sweden','study-in-switzerland']

def course_explore(course_name,course_url):
    base_url = 'https://yocket.in'
    resp = requests.get('{0}{1}'.format(base_url, course_url))
    soup = bs(resp.content, 'lxml')
    obj = {}
    obj['course_name'] = course_name
    try:
        obj['course_description'] = soup.find('div',class_='col-md-12 text-left').text.strip()
    except:
        obj['course_description'] = None
    try:
        obj['yocketers_applied'] = soup.find_all('div',class_='col-sm-4 col-xs-4')[0].span.text.strip()
    except:
        obj['yocketers_applied'] = None
    try:
        obj['yocketers_admitted'] = soup.find_all('div',class_='col-sm-4 col-xs-4')[1].span.text.strip()
    except:
        obj['yocketers_admitted'] = None
    try:
        obj['yocketers_interested'] = soup.find_all('div',class_='col-sm-4 col-xs-4')[2].span.text.strip()
    except:
        obj['yocketers_interested'] = None
    print(soup.find_all('div',class_='col-sm-6'))
    try:
        obj['tution_fee'] = soup.find_all('div',class_='col-sm-6')[-2].text.strip().replace('Tuition Fee','')
    except:
        obj['tution_fee'] = None
    try:
        obj['course_duration'] = soup.find_all('div',class_='col-sm-6')[-1].text.strip().replace('Course Duration','')
    except:
        obj['course_duration'] = None
    avg_profile = {}
    try:
        avg_profile['gre_score'] = [score.text.strip() for score in soup.find_all('div',class_='col-sm-3 col-xs-6 text-center') if 'GRE' in score.p.small.text.strip()][0].replace('GRE','').strip()
    except:
        avg_profile['gre_score'] = None
    try:
        avg_profile['toefl_score'] = [score.text.strip() for score in soup.find_all('div',class_='col-sm-3 col-xs-6 text-center') if 'TOEFL' in score.p.small.text.strip()][0].replace('TOEFL','').strip()
    except:
        avg_profile['toefl_score'] = None
    try:
        avg_profile['ug_score'] = [score.text.strip() for score in soup.find_all('div',class_='col-sm-3 col-xs-6 text-center') if 'UG' in score.p.small.text.strip()][0].replace('UG Score','').strip()
    except:
        avg_profile['ug_score'] = None
    try:
        avg_profile['work_exp'] = [score.text.strip() for score in soup.find_all('div',class_='col-sm-3 col-xs-6 text-center') if 'Work' in score.p.small.text.strip()][0].replace('Work Ex','').strip()
    except:
        avg_profile['work_exp'] = None
    obj['avg_profile'] = avg_profile
    try:
        obj['upcoming_deadline_date'] = soup.find_all('div', class_='col-sm-12')[3].text.strip().replace('Fall Deadline (Send docs)','').replace('Spring Deadline (Send docs)','')
    except:
        obj['upcoming_deadline_date'] = None
    try:
        obj['decision_date'] = soup.find_all('div', class_='col-sm-12')[4].text.strip()
    except:
        obj['decision_date'] = None

    return obj


def yocket_details(detail_url):
    base_url = 'https://yocket.in'
    resp = requests.get('{0}{1}'.format(base_url,detail_url))
    soup = bs(resp.content,'lxml')
    details = {}
    try:
        details['description'] = soup.find('div',class_='col-sm-9').p.text.strip()
    except:
        details['description'] = None
    try:
        details['logo_url'] = soup.find('div', class_='img-thumbnail').img.get('src')
    except:
        details['logo_url'] = None
    try:
        domains = [(domain.text.strip(),domain.a.get('href')) for domain in soup.find('div',class_='btn-group').find_all('li')]
    except:
        domains = []
    domain_data = []
    # print(domains)
    for n,dom in enumerate(domains):
        if n >= 1:
            resp = requests.get('{0}{1}'.format(base_url, dom[1]))
            soup = bs(resp.content, 'lxml')
        obj = {}
        obj['domain'] = dom[0]
        try:
            data_center = soup.find_all('div', class_='col-sm-3 col-xs-6')
        except:
            data_center = []
        try:
            obj['type'] = data_center[0].h3.text.strip()
        except:
            obj['type'] = None
        try:
            unwanted = data_center[1].small
            unwanted.extract()
            obj['acceptance_rate'] = data_center[1].h3.text.strip()
        except:
            obj['acceptance_rate'] = None
        try:
            unwanted = data_center[3].small
            unwanted.extract()
            obj['avg_tution_fee'] = data_center[2].h3.text.strip().replace('average tuition fee','')
        except:
            details['avg_tution_fee'] = None
        try:
            unwanted = data_center[4].small
            unwanted.extract()
            obj['avg_life_expense'] = data_center[3].h3.text.strip().replace('average living expense','')
        except:
            obj['avg_life_expense'] = None
        try:
            obj['yocketers_applied'] = data_center[4].p.text.strip()
        except:
            obj['yocketers_applied'] = None
        try:
            obj['yocketers_admitted'] = data_center[5].p.text.strip()
        except:
            obj['yocketers_admitted'] = None
        try:
            obj['yocketers_applied'] = data_center[6].p.text.strip()
        except:
            obj['yocketers_applied'] = None
        try:
            unwanted = data_center[1].small
            unwanted.extract()
            obj['avg_gre_quant_score'] = data_center[7].h3.text.strip()
        except:
            obj['avg_gre_quant_score'] = None
        try:
            unwanted = data_center[1].small
            unwanted.extract()
            obj['total_graduate_enrollment'] = data_center[8].h3.text.strip()
        except:
            obj['total_graduate_enrollment'] = None
        try:
            obj['course_list'] = [course.a.text.strip() for course in soup.find('ul',class_='university-course-list').find_all('li')]
        except:
            obj['course_list'] = None
        try:
            courses = [(course.a.text.strip(),course.a.get('href')) for course in soup.find('ul',class_='university-course-list').find_all('li')]
        except:
            courses = []
        course_data = []
        for m,cor in enumerate(courses):
            course_data.append(course_explore(cor[0],cor[1]))
        obj['courses'] = course_data
        domain_data.append(obj)
    details['domains'] = domain_data
    try:
        attrs = soup.find_all('div',class_='col-md-12')
    except:
        attrs = []
    try:
        details['location_details'] = [attr.p.text.strip() for attr in attrs if attr.h2 and 'Location' in attr.h2.text.strip()][0]
    except:
        details['location_details'] = None
    try:
        details['infrastructure_details'] = [attr.p.text.strip() for attr in attrs if attr.h2 and 'Infrastructure' in attr.h2.text.strip()][0]
    except:
        details['infrastructure_details'] = None
    try:
        details['residing_options'] = [attr.p.text.strip() for attr in attrs if attr.h2 and 'Residing' in attr.h2.text.strip()][0]
    except:
        details['residing_options'] = None
    try:
        details['weather'] = [attr.p.text.strip() for attr in attrs if attr.h2 and 'Weather' in attr.h2.text.strip()][0]
    except:
        details['weather'] = None
    try:
        details['faculty_and_pedagogy'] = [attr.p.text.strip() for attr in attrs if attr.h2 and 'Faculty' in attr.h2.text.strip()][0]
    except:
        details['faculty_and_pedagogy'] = None
    try:
        details['financial_aid'] = [attr.p.text.strip() for attr in attrs if attr.h2 and 'Financial' in attr.h2.text.strip()][0]
    except:
        details['financial_aid'] = None
    try:
        details['jobs_and_placements'] = [attr.p.text.strip() for attr in attrs if attr.h2 and 'Jobs' in attr.h2.text.strip()][0]
    except:
        details['jobs_and_placements'] = None
    try:
        details['campus_life'] = [attr.p.text.strip() for attr in attrs if attr.h2 and 'Crowd' in attr.h2.text.strip()][0]
    except:
        details['campus_life'] = None
    try:
        details['alumni'] = [attr.ul.text.strip() for attr in attrs if attr.h2 and 'Alumni' in attr.h2.text.strip()][0]
    except:
        details['alumni'] = None
    try:
        details['verdict'] = [attr.p.text.strip() for attr in attrs if attr.h2 and 'Verdict' in attr.h2.text.strip()][0]
    except:
        details['verdict'] = None
    return details


def yocket_univ(country,page=1):
    print(country)
    dict = {}
    dict['success'] = True
    url = 'https://yocket.in/universities/{0}/page={0}'.format(country,page)
    resp = requests.get(url)
    soup = bs(resp.content,'lxml')
    try:
        iterator = soup.find('div',id='university_list').find_all('div',class_='col-sm-9 col-xs-12')
    except:
        iterator = []
    data = []
    try:
        dict['total_pages'] = re.findall('\d+\)',soup.find('div',id='university_list').p.text.strip())[0].replace(')','')
        dict['total_universities'] = re.findall('\d+',soup.find('div',id='university_list').p.text.strip())[0]
    except:
        pass
    for iter in iterator:
        temp = {}
        try:
            temp['university_name'] = iter.find('span', class_='lead').text.strip()
        except:
            temp['university_name'] = None
        try:
            temp['detail_url'] = iter.find('span', class_='lead').a.get('href')
        except:
            temp['detail_url'] = None
        temp['details'] = yocket_details(temp['detail_url'])

        try:
            temp['location'] = iter.find_all('span')[1].text.strip()
        except:
            temp['location'] = None
        try:
            temp['label'] = iter.find('span',class_='label').text.strip()
        except:
            temp['label'] = None
        data.append(temp)
    dict['data'] = data

    return dict

def bls_base(n):
    try:
        bls_category_dict = {}
        url = 'http://www.bls.gov/oes/2016/may/oes151131.htm'
        try:
            req = requests.get(url)
        except Exception as e:
            bls_category_dict = None
            return bls_category_dict
        soup = BeautifulSoup(req.content, 'lxml')
        data = []
        if req.status_code == 200:
            keys_table = []
            values_tab = []
            try:
                card = soup.find('div', id='bodytext').find_all('table')[n]
            except:
                card = []
            try:
                trs = card.find_all('tr')
            except:
                trs = None
            for i,tr in enumerate(trs):
                regex_brackets =re.compile(r"\((\d+)\)")
                if i==0:
                    try:
                        key_th = tr.find_all('th')
                    except:
                        key_th = None
                    for j in key_th:
                        key_name = j.text.strip()
                        key_desc_check = bool(regex_brackets.search(key_name))
                        regex_word_check = re.compile(r"%\((\w+)\)")
                        word_check = bool(regex_word_check.search(key_name))
                        if word_check is True:
                            key_name = regex_word_check.sub('',key_name)
                            key_name = '{0}%'.format(key_name)
                        else:
                            if key_desc_check is True:
                                key_name = regex_brackets.sub('',key_name).strip()
                                key_name = key_name.replace(' ','_').lower()
                            else:
                                key_name = key_name.replace(' ','_').replace('(','_').replace(')','').lower()
                        keys_table.append(key_name)
                else:
                    try:
                        value_tr = tr.find_all('td')
                    except:
                        value_tr = None
                    range_keys = len(keys_table)
                    for k in range(range_keys):
                        try:
                            value = value_tr[k].text.strip()
                        except:
                            value = None
                        regex_row_check = re.compile(r"\w+\s\((\d+)\)")
                        row_check = bool(regex_row_check.findall(value))
                        if row_check is True:
                            value = regex_brackets.sub('',value).strip()
                        else:
                            value_check = bool(regex_brackets.search(value))
                            if value_check is True:
                                value = None
                            else:
                                value = value
                        values_tab.append(value)
            values_table = []
            for i in range(0,len(values_tab),len(keys_table)):
                values_table.append(values_tab[i:i+len(keys_table)])
            for val in values_table:
                obj = {}
                for index,ele in enumerate(val):
                    obj[keys_table[index]] = ele
                data.append(obj)
            bls_category_dict['data'] = data
            return bls_category_dict
    except Exception as e:
        print(str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return None


def bls_categories():
    try:
        blsDict = {}
        blsDict['success'] = True
        try:
            national_estimates_Dict = {}
            national_estimates_Dict['employment_mean_wage_estimates'] = bls_base(n=0)
            national_estimates_Dict['percentile_wage_estimates'] = bls_base(n=1)
            industry_profile_Dict = {}
            industry_profile_Dict['industry_high_levels_employments'] = bls_base(n=2)
            industry_profile_Dict['industry_high_concentration_employments'] = bls_base(n=3)
            industry_profile_Dict['industry_top_paying_industries'] = bls_base(n=4)
            geography_profile_Dict = {}
            geography_profile_Dict['highest_employment_level_state'] = bls_base(n=5)
            geography_profile_Dict['highest_conc_job_loc_quotient_state'] = bls_base(n=6)
            geography_profile_Dict['top_paying_states'] = bls_base(n=7)
            geography_profile_Dict['highest_employment_level_metropolitan_areas'] = bls_base(n=8)
            geography_profile_Dict['highest_conc_job_loc_quotient_metropolitan_areas'] = bls_base(n=9)
            geography_profile_Dict['top_paying_metropolitan_areas'] = bls_base(n=10)
            geography_profile_Dict['highest_employment_non_metropolitan_areas'] = bls_base(n=11)
            geography_profile_Dict['highest_conc_job_loc_quotient_non_metropolitan_areas'] = bls_base(n=12)
            geography_profile_Dict['top_paying_non_metropolitan_areas'] = bls_base(n=13)
            blsDict['national_estimates'] = national_estimates_Dict
            blsDict['industry_profile_Dict'] = industry_profile_Dict
            blsDict['geography_profile'] = geography_profile_Dict
            return blsDict
        except Exception as e:
            blsDict['success'] = False
            return blsDict
    except Exception as e:
        print(str(e))
        return None

#
# world_rank_url = 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/world_university_rankings_2018_limit0_369a9045a203e176392b9fb8f8c1cb2a.json'
# us_url = 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/united_states_rankings_2018_limit0_efdb24148bae97278bbfe6ecfd71cdd9.json'
# asia_url = 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/asia_university_rankings_2018_limit0_c36ae779f4180136af6e4bf9e6fc1081.json'
# euro_url = 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/european_teaching_rankings_2018_limit0_514072620922c26c28ccc550278168a7.json'
# japan_url = 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/japan_university_rankings_2018_limit0_e2da15cfd63ca207908b0c3fe5fe8a2d.json'
# latin_america_url = 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/latin_america_rankings_2018_limit0_3b4f7a3ed24dab53d4d94bbc240f0edb.json'
#
#
# def times_higher_edu(url):
#     the_dict = {}
#     the_dict['success'] = True
#     resp = requests.get(url)
#     ranks_json = resp.json()
#     ranks_data = ranks_json['data']
#     the_dict['data'] = ranks_data
#     return the_dict
#
# def times_higher_edu_details(nid,detail_url):
#     newDict = {}
#     newDict['success'] = True
#     resp_ = requests.get('https://www.timeshighereducation.com/sites/default/files/university/rankings/{0}.json'.format(str(nid)))
#     try:
#         newDict['details'] = resp_.json()['data']
#     except:
#         newDict['details'] = []
#     resp__ = requests.get('https://www.timeshighereducation.com/sites/default/files/institution_markers/gmap_{0}.json'.format(str(nid)))
#     try:
#         newDict['address'] = resp__.json()
#     except:
#         newDict['address'] = None
#     base_url = 'https://www.timeshighereducation.com'
#     req_ = requests.get('{0}{1}'.format(base_url,detail_url))
#     soup = bs(req_.content,'lxml')
#     try:
#         newDict['university_description'] = soup.find('div',class_='tabbed-content__panel tabbed-content__panel-0').text.strip()
#     except:
#         newDict['university_description'] = None
#
#     return newDict

def nces_data(table_no,keys=[]):
    url = 'https://nces.ed.gov/programs/digest/d17/tables/dt17_{0}.asp'.format(table_no)
    resp = requests.get(url)
    soup = bs(resp.content,'lxml')
    iterator = soup.find('table',class_='tabletop tableMain tableWidth tableBracketRow').tbody.find_all('tr')
    data = []
    for iter in iterator:
        temp = {}
        cool = iter.find_all('td')
        try:
            th = iter.th
            unwanted = th.sup
            unwanted.extract()
            temp[keys[0]] = th.text.strip()
        except:
            temp[keys[0]] = None
        for i in range(1,len(keys)):
            try:
                temp[keys[i]] = '{0} {1}'.format(cool[2*(i-1)].text.strip(),cool[2*(i-1)+1].text.strip())
            except:
                temp[keys[i]] = None
        data.append(temp)
    return data


def nces_univ_data(univ_name):
    ncesDict = {}
    ncesDict['success'] = True
    nces_url = 'https://nces.ed.gov/collegenavigator/?q={0}'.format(univ_name)
    resp = requests.get(nces_url)
    soup = bs(resp.content,'lxml')
    result_url = soup.find('tr',class_='resultsW').find_all('td')[-2].a.get('href')
    result_name = soup.find('tr', class_='resultsW').find('td',class_='pbe').h2.text.strip()
    nces_univ_url = 'https://nces.ed.gov/collegenavigator/{0}'.format(result_url)
    try:
        ncesDict['link'] = nces_univ_url
    except:
        ncesDict['link'] = None
    try:
        ncesDict['university_full_name'] = result_name
    except:
        ncesDict['university_full_name'] = None
    try:
        ncesDict['university_name'] = univ_name
    except:
        ncesDict['university_name'] = None
    resp_ = requests.get(nces_univ_url)
    soup_ = bs(resp_.content,'lxml')
    trs = soup_.find('table',class_='layouttab').find_all('tr')
    data = []
    nces_obj = {}
    try:
        nces_obj['general_info'] = [tr.find_all('td')[1].text.strip() for tr in trs if 'General' in tr.find_all('td')[0].text.strip()][0]
    except:
        nces_obj['general_info'] = None
    try:
        nces_obj['website'] = [tr.find_all('td')[1].text.strip() for tr in trs if 'Website' in tr.find_all('td')[0].text.strip()][0]
    except:
        nces_obj['website'] = None
    try:
        nces_obj['type'] = [tr.find_all('td')[1].text.strip() for tr in trs if 'Type' in tr.find_all('td')[0].text.strip()][0]
    except:
        nces_obj['type'] = None
    try:
        nces_obj['awards_offered'] = [tr.find_all('td')[1].text.strip() for tr in trs if 'Awards' in tr.find_all('td')[0].text.strip()][0]
    except:
        nces_obj['awards_offered'] = None
    try:
        nces_obj['campus_setting'] = [tr.find_all('td')[1].text.strip() for tr in trs if 'setting' in tr.find_all('td')[0].text.strip()][0]
    except:
        nces_obj['campus_setting'] = None
    try:
        nces_obj['campus_housing'] = [tr.find_all('td')[1].text.strip() for tr in trs if 'housing' in tr.find_all('td')[0].text.strip()][0]
    except:
        nces_obj['campus_housing'] = None
    try:
        nces_obj['student_population'] = [tr.find_all('td')[1].text.strip() for tr in trs if 'population' in tr.find_all('td')[0].text.strip()][0]
    except:
        nces_obj['student_population'] = None
    try:
        nces_obj['student_to_faculty_ratio'] = [tr.find_all('td')[1].text.strip() for tr in trs if 'Student-to-faculty' in tr.find_all('td')[0].text.strip()][0]
    except:
        nces_obj['student_to_faculty_ratio'] = None
    try:
        gen_data = [tab for tab in soup_.find_all('table',class_='tabular') if 'Faculty' in tab.thead.text.strip()][0].find_all('tr')
    except:
        gen_data = [2]
    gnrl_data = []
    for n,gen in enumerate(gen_data[1:]):
        temp = {}
        try:
            temp['category'] = gen.find_all('td')[0].text.strip()
        except:
            temp['category'] = None
        try:
            temp['full_time'] = gen.find_all('td')[1].text.strip()
        except:
            temp['full_time'] = None
        try:
            temp['part_time'] = gen.find_all('td')[2].text.strip()
        except:
            temp['part_time'] = None
        gnrl_data.append(temp)

    if len(gnrl_data) == 6:
        gnrl_data = [gnrl_data[x:x+3] for x in range(0,len(gnrl_data),3)]

    image_data = soup_.find('div',id='divctl00_cphCollegeNavBody_ucInstitutionMain_ctl03').find('table',class_='tabular').find_all('tr')
    img_data = []
    for n,img in enumerate(image_data):
        temp = {}
        if n == 0:
            try:
                temp['category'] = img.find_all('th')[0].text.strip()
            except:
                temp['category'] = None
            try:
                temp['value'] = img.find_all('th')[1].text.strip()
            except:
                temp['value'] = None
        else:
            try:
                temp['category'] = img.find_all('td')[0].text.strip()
            except:
                temp['category'] = None
            try:
                temp['value'] = img.find_all('td')[1].text.strip()
            except:
                temp['value'] = None
        img_data.append(temp)

    g_data = []
    image_data_ = soup_.find_all('table',class_='graphtabs')
    for i in image_data_:
        temp = {}
        graph_data = i.find_all('img')
        for graph in graph_data:
            try:
                temp['data'] = graph.get('alt')
            except:
                temp['data'] = None
            try:
                temp['category'] = graph.get('alt').split(':')[0]
            except:
                temp['category'] = None
            g_data.append(temp)
    g_datas = []
    for g in g_data:
        if g not in g_datas:
            g_datas.append(g)

    pms = soup_.find('table',class_='pmtabular').find_all('tr')
    pms_data = []
    temp_ = {}
    for n,pm in enumerate(pms):
        obj = {}

        if n == 0:
            temp_['keys'] = pm.find_all('th')
            continue
        if n > 1:
            obj['category'] = temp_['category']
        check = len(pm.find_all('td'))

        if check == 1:
            cat = pm.td.text.strip()
            temp_['category'] = cat
            continue
        for m, key in enumerate(temp_['keys']):
            try:
                obj['{0}'.format(key.text.replace(' ', '_').lower())] = pm.find_all('td')[m].text.replace('d','').strip()
            except:
                obj['{0}'.format(key.text.replace(' ', '_').lower())] = None
        pms_data.append(obj)

    nces_obj['programs_majors'] = pms_data
    nces_obj['images_graphs_data'] = g_datas
    nces_obj['enrollment'] = img_data
    nces_obj['general_information'] = gnrl_data
    data.append(nces_obj)
    ncesDict['data'] = data
    return ncesDict
#
# print(nces_univ_data('College of Lake County'))

def cjolDetail(detail_url):
    details = {}
    req = requests.get(detail_url)
    soup = bs(req.content,'lxml')
    details['job_details'] = {}
    try:
        details['job_details']['salary'] = soup.find('ul',class_='require-jobintro clearfix').find_all('li')[0].text.strip()
    except:
        details['job_details']['salary'] = None
    try:
        details['job_details']['requirement'] = soup.find('ul',class_='require-jobintro clearfix').find_all('li')[1].text.strip()
    except:
        details['job_details']['requirement'] = None
    try:
        details['job_details']['experience'] = soup.find('ul',class_='require-jobintro clearfix').find_all('li')[2].text.strip()
    except:
        details['job_details']['experience'] = None
    try:
        details['job_details']['vacancy'] = soup.find('ul',class_='require-jobintro clearfix').find_all('li')[3].text.strip()
    except:
        details['job_details']['vacancy'] = None
    try:
        details['job_details']['type'] = soup.find('ul',class_='require-jobintro clearfix').find_all('li')[4].text.strip()
    except:
        details['job_details']['type'] = None
    try:
        details['tagwords'] = [i.text.strip() for i in soup.find('ul',class_='taglist-jobintro clearfix').find_all('li')]
    except:
        details['tagwords'] = None
    try:
        details['location'] = soup.find('div',class_='btm-jobintro clearfix').find('div',class_='area-jobintro f_l').text.strip()
    except:
        details['location'] = None
    try:
        details['update_time'] = soup.find('div',class_='btm-jobintro clearfix').find('div',class_='pubtime-jobintro f_l').text.strip()
    except:
        details['update_time'] = None
    try:
        details['work_address'] = soup.find('div',class_='txtinfo-address').text.replace('查看地图','').strip()
    except:
        details['work_address'] = None
    try:
        details['job_description'] = soup.find('div',class_='coninfo-jobdesc').text.strip()
    except:
        details['job_description'] = None
    try:
        details['other_info'] = soup.find('div',class_='coninfo-otherinfo').text.strip()
    except:
        details['other_info'] = None
    try:
        comp_iterator = soup.find('ul',class_='ul-combscintro').find_all('li')
    except:
        comp_iterator = []
    details['company_details'] = []
    for c in comp_iterator:
        obj = {}
        try:
            obj['title'] = c.i.get('title')
        except:
            obj['title'] = None
        try:
            obj['description'] = c.text.strip()
        except:
            obj['description'] = None
        details['company_details'].append(obj)

    return details


def cjolBasic(page='1'):
    cjolDict = {}
    cjolDict['success'] = True

    params_ = (
        ('', ''),
        ('ListType', '2'),
        ('page', '{0}'.format(page)),
    )

    response = requests.post('http://s.cjol.com/service/joblistjson.aspx', params=params_)

    soup = bs(response.json()['JobListHtml'],'lxml')

    try:
        iterator = soup.find_all('ul',class_='results_list_box')
    except:
        iterator = []

    cjolDict['data'] = []
    for i in iterator:
        temp = {}
        try:
            temp['job_title'] = i.find('li',class_='list_type_first').text.strip()
        except:
            temp['job_title'] = None
        try:
            temp['detail_url'] = i.find('li',class_='list_type_first').a.get('href')
        except:
            temp['detail_url'] = None
        try:
            temp['company_name'] = i.find('li',class_='list_type_second').text.strip()
        except:
            temp['company_name'] = None
        try:
            temp['work_area'] = i.find('li',class_='list_type_third').text.strip()
        except:
            temp['work_area'] = None
        try:
            temp['education'] = i.find('li',class_='list_type_fifth').text.strip()
        except:
            temp['education'] = None
        try:
            temp['experience'] = i.find('li',class_='list_type_sixth').text.strip()
        except:
            temp['experience'] = None
        try:
            temp['monthly_salary'] = i.find('li',class_='list_type_seventh').text.strip()
        except:
            temp['monthly_salary'] = None
        try:
            temp['update_time'] = i.find('li',class_='list_type_eighth').text.strip()
        except:
            temp['update_time'] = None
        try:
            temp['details'] = cjolDetail(temp['detail_url'])
        except:
            temp['details'] = None

        cjolDict['data'].append(temp)

    return cjolDict

# pp.pprint(cjolBasic('1750'))

def newchinacarrer_details(detail_url):
    try:
        req = requests.get(detail_url)
        soup = bs(req.content,'lxml')
        details = {}
        try:
            details['job_description'] = soup.find('div',class_='jobsearch-JobComponent-description icl-u-xs-mt--md').text.strip()
        except:
            details['job_description'] = None
        try:
            details['keywords'] = soup.find('div',class_='jobsearch-JobMetadataHeader icl-u-xs-mb--md').text.strip()
        except:
            details['keywords'] = None
        try:
            details['job_title'] = soup.find('div',class_='jobsearch-DesktopStickyContainer').h3.text.strip()
        except:
            details['job_title'] = None
        try:
            details['company_name'] = soup.find('div',class_='jobsearch-InlineCompanyRating').div.text.strip()
        except:
            details['company_name'] = None
        try:
            details['location'] = soup.find('div',class_='jobsearch-InlineCompanyRating').find_all('div')[-1].text.strip()
        except:
            details['location'] = None
        return details
    except:
        return None

def newchinacareer(page='1'):
    chinaDict = {}
    chinaDict['success'] = True
    china_url = 'https://www.newchinacareer.com/jobs/*/{0}'.format(page)
    try:
        req = requests.get(china_url)
    except Exception as e:
        chinaDict['success'] =False
        chinaDict['errorMessage'] = str(e)
        return chinaDict

    chinaDict['data'] = []
    soup = bs(req.content,'lxml')
    try:
        iterator = soup.ol.find_all('li')
    except:
        return chinaDict
    try:
        chinaDict['total_pages'] = re.findall('of \d+,\d+',soup.find('p',class_='result-count').text.strip())[0].replace('of ','').replace(',','')
    except:
        chinaDict['total_pages'] = None
    print(len(iterator))
    for i in iterator:
        temp = {}
        try:
            temp['job_title'] = i.h2.text.strip()
        except:
            temp['job_title'] = None
        try:
            temp['job_summary'] = i.find('p',class_='company').find_all('span')[0].text.strip()
        except:
            temp['job_summary'] = None
        try:
            temp['snippet'] = i.find('p',class_='summary').text.strip()
        except:
            temp['snippet'] = None
        try:
            temp['location'] = i.find('p',class_='company').find('span',class_='location').text.strip()
        except:
            temp['location'] = None
        try:
            temp['source'] = i.find('p',class_='meta').find('span',class_='source').text.strip()
        except:
            temp['source'] = None
        try:
            temp['posted_time'] = i.find('p',class_='meta').find('span',class_='date').text.strip()
        except:
            temp['posted_time'] = None
        try:
            temp['detail_url'] = i.h2.a.get('href')
        except:
            temp['detail_url'] = None
        try:
            temp['details'] = newchinacarrer_details(temp['detail_url'])
        except:
            temp['details'] = None
        chinaDict['data'].append(temp)

    return chinaDict

# pp.pprint(newchinacareer('1'))


def liepin_detail(detail_url):
    try:
        req = requests.get(detail_url)
        soup = bs(req.content,'lxml')
        details = {}
        try:
            details['job_description'] = soup.find('div',class_='job-item main-message job-description').text.strip()
        except:
            details['job_description'] = None
        try:
            details['location'] = soup.find('p',class_='basic-infor').span.text.strip()
        except:
            details['location'] = None
        try:
            details['posted_time'] = soup.find('p',class_='basic-infor').time.text.strip()
        except:
            details['posted_time'] = None
        try:
            details['job_qualifications'] = soup.find('div',class_='job-qualifications').text.strip()
        except:
            details['job_qualifications'] = None
        try:
            details['tagwords'] = [j.text.strip() for j in soup.find('ul',class_='comp-tag-list clearfix').find_all('li')]
        except:
            details['tagwords'] = None
        return details
    except:
        return None


def liepin(page):
    lieDict = {}
    lieDict['success'] = True
    lieDict['data'] = []
    liepin_url = 'https://www.liepin.com/zhaopin/?pubTime=&ckid=03bce93783fc6b74&fromSearchBtn=2&compkind=&isAnalysis=&init=-1&searchType=1&dqs=&industryType=&jobKind=&sortFlag=15&degradeFlag=0&industries=&salary=&compscale=&key=&clean_condition=&headckid=03bce93783fc6b74&d_pageSize=40&siTag=1B2M2Y8AsgTpgAmY7PhCfg~fA9rXquZc5IkJpXC-Ycixw&d_headId=5fd98a99b0422e978206caefb41bc74a&d_ckId=5fd98a99b0422e978206caefb41bc74a&d_sfrom=search_prime&d_curPage=0&curPage={0}'.format(page)
    req = requests.get(liepin_url)
    soup = bs(req.content,'lxml')
    try:
        iterator = soup.find('ul',class_='sojob-list').find_all('li')
    except:
        iterator = []
    print(len(iterator))

    for i in iterator:
        temp = {}
        try:
            temp['job_title'] = i.find('div',class_='job-info').h3.text.strip()
        except:
            temp['job_title'] = None
        try:
            temp['detail_url'] = i.find('div', class_='job-info').h3.a.get('href')
        except:
            temp['detail_url'] = None
        try:
            temp['job_title'] = i.find('div',class_='job-info').h3.text.strip()
        except:
            temp['job_title'] = None
        try:
            temp['salary'] = i.find('p',class_='condition clearfix').find('span',class_='text-warning').text.strip()
        except:
            temp['salary'] = None
        try:
            temp['location'] = i.find('p',class_='condition clearfix').find('a',class_='area').text.strip()
        except:
            temp['location'] = None
        try:
            temp['education'] = i.find('p',class_='condition clearfix').find('span',class_='edu').text.strip()
        except:
            temp['education'] = None
        try:
            temp['experience'] = i.find('p',class_='condition clearfix').find_all('span')[-1].text.strip()
        except:
            temp['experience'] = None
        try:
            temp['posted_time'] = i.find('p',class_='time-info clearfix').time.text.strip()
        except:
            temp['posted_time'] = None
        try:
            temp['feedback'] = i.find('p',class_='time-info clearfix').span.text.strip()
        except:
            temp['feedback'] = None
        try:
            temp['company_name'] = i.find('div',class_='company-info nohover').find('p',class_='company-name').text.strip()
        except:
            temp['company_name'] = None
        try:
            temp['fields_financing'] = i.find('div',class_='company-info nohover').find('p',class_='field-financing').text.strip()
        except:
            temp['fields_financing'] = None
        try:
            temp['temptations'] = i.find('div',class_='company-info nohover').find('p',class_='temptation clearfix').split('\n')
        except:
            temp['temptations'] = None
        try:
            temp['details'] = liepin_detail(temp['detail_url'])
        except:
            temp['details'] = None

        lieDict['data'].append(temp)

    return lieDict

# pp.pprint(liepin('1'))



monster_us_states = [
  {
    "us_state": "Alabama",
    "link": "https://www.monster.com/jobs/browse/l-alabama.aspx"
  },
  {
    "us_state": "Alaska",
    "link": "https://www.monster.com/jobs/browse/l-alaska.aspx"
  },
  {
    "us_state": "Arizona",
    "link": "https://www.monster.com/jobs/browse/l-arizona.aspx"
  },
  {
    "us_state": "Arkansas",
    "link": "https://www.monster.com/jobs/browse/l-arkansas.aspx"
  },
  {
    "us_state": "California",
    "link": "https://www.monster.com/jobs/browse/l-california.aspx"
  },
  {
    "us_state": "Colorado",
    "link": "https://www.monster.com/jobs/browse/l-colorado.aspx"
  },
  {
    "us_state": "Connecticut",
    "link": "https://www.monster.com/jobs/browse/l-connecticut.aspx"
  },
  {
    "us_state": "Delaware",
    "link": "https://www.monster.com/jobs/browse/l-delaware.aspx"
  },
  {
    "us_state": "District of Columbia",
    "link": "https://www.monster.com/jobs/browse/l-district-of-columbia.aspx"
  },
  {
    "us_state": "Florida",
    "link": "https://www.monster.com/jobs/browse/l-florida.aspx"
  },
  {
    "us_state": "Georgia",
    "link": "https://www.monster.com/jobs/browse/l-georgia.aspx"
  },
  {
    "us_state": "Guam",
    "link": "https://www.monster.com/jobs/browse/l-guam.aspx"
  },
  {
    "us_state": "Hawaii",
    "link": "https://www.monster.com/jobs/browse/l-hawaii.aspx"
  },
  {
    "us_state": "Idaho",
    "link": "https://www.monster.com/jobs/browse/l-idaho.aspx"
  },
  {
    "us_state": "Illinois",
    "link": "https://www.monster.com/jobs/browse/l-illinois.aspx"
  },
  {
    "us_state": "Indiana",
    "link": "https://www.monster.com/jobs/browse/l-indiana.aspx"
  },
  {
    "us_state": "Iowa",
    "link": "https://www.monster.com/jobs/browse/l-iowa.aspx"
  },
  {
    "us_state": "Kansas",
    "link": "https://www.monster.com/jobs/browse/l-kansas.aspx"
  },
  {
    "us_state": "Kentucky",
    "link": "https://www.monster.com/jobs/browse/l-kentucky.aspx"
  },
  {
    "us_state": "Louisiana",
    "link": "https://www.monster.com/jobs/browse/l-louisiana.aspx"
  },
  {
    "us_state": "Maine",
    "link": "https://www.monster.com/jobs/browse/l-maine.aspx"
  },
  {
    "us_state": "Maryland",
    "link": "https://www.monster.com/jobs/browse/l-maryland.aspx"
  },
  {
    "us_state": "Massachusetts",
    "link": "https://www.monster.com/jobs/browse/l-massachusetts.aspx"
  },
  {
    "us_state": "Michigan",
    "link": "https://www.monster.com/jobs/browse/l-michigan.aspx"
  },
  {
    "us_state": "Minnesota",
    "link": "https://www.monster.com/jobs/browse/l-minnesota.aspx"
  },
  {
    "us_state": "Mississippi",
    "link": "https://www.monster.com/jobs/browse/l-mississippi.aspx"
  },
  {
    "us_state": "Missouri",
    "link": "https://www.monster.com/jobs/browse/l-missouri.aspx"
  },
  {
    "us_state": "Montana",
    "link": "https://www.monster.com/jobs/browse/l-montana.aspx"
  },
  {
    "us_state": "Nebraska",
    "link": "https://www.monster.com/jobs/browse/l-nebraska.aspx"
  },
  {
    "us_state": "Nevada",
    "link": "https://www.monster.com/jobs/browse/l-nevada.aspx"
  },
  {
    "us_state": "New Hampshire",
    "link": "https://www.monster.com/jobs/browse/l-new-hampshire.aspx"
  },
  {
    "us_state": "New Jersey",
    "link": "https://www.monster.com/jobs/browse/l-new-jersey.aspx"
  },
  {
    "us_state": "New Mexico",
    "link": "https://www.monster.com/jobs/browse/l-new-mexico.aspx"
  },
  {
    "us_state": "New York",
    "link": "https://www.monster.com/jobs/browse/l-new-york.aspx"
  },
  {
    "us_state": "North Carolina",
    "link": "https://www.monster.com/jobs/browse/l-north-carolina.aspx"
  },
  {
    "us_state": "North Dakota",
    "link": "https://www.monster.com/jobs/browse/l-north-dakota.aspx"
  },
  {
    "us_state": "Ohio",
    "link": "https://www.monster.com/jobs/browse/l-ohio.aspx"
  },
  {
    "us_state": "Oklahoma",
    "link": "https://www.monster.com/jobs/browse/l-oklahoma.aspx"
  },
  {
    "us_state": "Oregon",
    "link": "https://www.monster.com/jobs/browse/l-oregon.aspx"
  },
  {
    "us_state": "Pennsylvania",
    "link": "https://www.monster.com/jobs/browse/l-pennsylvania.aspx"
  },
  {
    "us_state": "Puerto Rico",
    "link": "https://www.monster.com/jobs/browse/l-puerto-rico.aspx"
  },
  {
    "us_state": "Rhode Island",
    "link": "https://www.monster.com/jobs/browse/l-rhode-island.aspx"
  },
  {
    "us_state": "South Carolina",
    "link": "https://www.monster.com/jobs/browse/l-south-carolina.aspx"
  },
  {
    "us_state": "South Dakota",
    "link": "https://www.monster.com/jobs/browse/l-south-dakota.aspx"
  },
  {
    "us_state": "Tennessee",
    "link": "https://www.monster.com/jobs/browse/l-tennessee.aspx"
  },
  {
    "us_state": "Texas",
    "link": "https://www.monster.com/jobs/browse/l-texas.aspx"
  },
  {
    "us_state": "Utah",
    "link": "https://www.monster.com/jobs/browse/l-utah.aspx"
  },
  {
    "us_state": "Vermont",
    "link": "https://www.monster.com/jobs/browse/l-vermont.aspx"
  },
  {
    "us_state": "Virgin Islands",
    "link": "https://www.monster.com/jobs/browse/l-virgin-islands.aspx"
  },
  {
    "us_state": "Virginia",
    "link": "https://www.monster.com/jobs/browse/l-virginia.aspx"
  },
  {
    "us_state": "Washington",
    "link": "https://www.monster.com/jobs/browse/l-washington.aspx"
  },
  {
    "us_state": "West Virginia",
    "link": "https://www.monster.com/jobs/browse/l-west-virginia.aspx"
  },
  {
    "us_state": "Wisconsin",
    "link": "https://www.monster.com/jobs/browse/l-wisconsin.aspx"
  },
  {
    "us_state": "Wyoming",
    "link": "https://www.monster.com/jobs/browse/l-wyoming.aspx"
  }
]


def monster_loc():
    url = 'https://www.monster.com/jobs/'
    soup = souper(url)
    iters = soup.find_all('div',class_='col-md-6')[2].find('ul').find_all('li')
    data = []
    for i in iters:
        temp = {}
        try:
            temp['us_state'] = i.text.strip().replace(' Jobs','')
        except:
            temp['us_state'] = None
        try:
            temp['link'] = i.a.get('href')
        except:
            temp['link'] = None
        data.append(temp)
    return data

# print(json.dumps(monster_loc()))

def monster_jds(location,company,page='1'):
    monsterDict = {}
    monsterDict['success'] = True
    api_url = 'https://www.monster.com/jobs/search/pagination/?where={0}&q={1}&isDynamicPage=true&isMKPagination=true&page={2}'.format(location,company,page)
    response = requests.get(api_url)
    data = response.json()

    for dat in data:
        if dat['Title'] is '':
            continue
        detail_url = dat['JobViewUrl']
        print(detail_url)
        req = requests.get(detail_url)
        soup = bs(req.content, 'lxml')
        try:
            dat['JobDescriptionText'] = soup.find('div',id='JobDescription').text.strip()
        except:
            dat['JobDescriptionText'] = None

    monsterDict['data'] = data
    return monsterDict


# pp.pprint(monster_jds('Alaska','Amazon'))


# def the_ladders_jobs(page='1'):
#     base_url = 'https://www.theladders.com'
#     req = requests.get(base_url)
#     soup = bs(req.content,'lxml')
#     locs = soup.find('div',class_='expando-items expando-items-company').find_all('a')
#     loc = [(l.text.strip(),'{0}{1}'.format(base_url,l.get('href'))) for l in locs]
#     return loc

# print(the_ladders_jobs())

def the_ladders_details(detail_url):
    details = {}
    req = requests.get(detail_url)
    soup = bs(req.content,'lxml')
    try:
        details['job_description'] = soup.find('div',id='description-new').text.strip()
    except:
        details['job_description'] = None
    try:
        details['other_locations'] = [l.text.strip() for l in soup.find('div',class_='job-page__other-locations-dropdown-content').find_all('a')]
    except AttributeError:
        details['other_locations'] = None
    return details


def the_ladder_jds(job_url,page='1'):
    theLadderDict = {}
    theLadderDict['success'] = True
    theLadderDict['data'] = []
    main_url = '{0}?sort=ByRelevance&page={1}'.format(job_url,page)
    req = requests.get(main_url)

    soup = bs(req.content,'lxml')
    try:
        x = soup.find('span',class_='large-header x-jobs-for-you__subheading-wrapper').text.strip()
        theLadderDict['total_jobs'] = int(re.findall('\d+,\d+',x)[0].replace(',',''))
    except AttributeError:
        theLadderDict['total_jobs'] = None
    try:
        if (int(theLadderDict['total_jobs']) % 25) == 0:
            theLadderDict['total_pages'] = int(theLadderDict['total_jobs']) // 25
        else:
            theLadderDict['total_pages'] = int(theLadderDict['total_jobs']) // 25 + 1
    except AttributeError:
        theLadderDict['total_pages'] = None

    try:
        cards = soup.find('ul',class_='search-results joblisting-wrapper').find_all('li')
    except AttributeError:
        return theLadderDict
    for card in cards:
        temp = {}
        try:
            temp['job_title'] = card.find('h2',class_='link large opportunity-item__title__search-ab-test').text.strip()
        except AttributeError:
            temp['job_title'] = None
        try:
            temp['detail_url'] = card.find('div',class_='opportunity-item__title-container__search-ab-test').a.get('href')
        except AttributeError:
            temp['detail_url'] = None
        try:
            temp['job_title'] = card.find('h2',class_='link large opportunity-item__title__search-ab-test').text.strip()
        except AttributeError:
            temp['job_title'] = None
        try:
            temp['company_name'] = card.find('div',class_='company-location-container').span.text.strip()
        except AttributeError:
            temp['company_name'] = None
        try:
            temp['location'] = card.find('a',class_='location-link').text.strip()
        except AttributeError:
            temp['location'] = None
        try:
            temp['job_snippet'] = card.find('div',class_='opportunity-description-short__search-ab-test').text.strip()
        except AttributeError:
            temp['job_snippet'] = None
        try:
            temp['experience'] = card.find('div',class_='years-industry-container').find('span',class_='search-results__job-item-details').text.strip()
        except AttributeError:
            temp['experience'] = None
        try:
            temp['industry'] = card.find('div',class_='years-industry-container').a.text.strip()
        except AttributeError:
            temp['industry'] = None
        try:
            temp['date_posted'] = card.find('div',class_='posted-by-container').time.get('datetime')
        except AttributeError:
            temp['date_posted'] = None
        try:
            temp['posted_by'] = card.find('div',class_='posted-by-container').a.text.strip()
        except AttributeError:
            temp['posted_by'] = None
        try:
            temp['details'] = the_ladders_details(temp['detail_url'])
        except AttributeError:
            temp['details'] = None
        theLadderDict['data'].append(temp)

    return theLadderDict

from datetime import timedelta

def reed_jds(job_url,page='1'):
    reedDict = {}
    reedDict['success'] = True
    reedDict['data'] = []
    reed_url = '{0}?pageno={1}'.format(job_url,page)
    req = requests.get(reed_url)
    soup = bs(req.content,'lxml')

    check_pagination = soup.find('div',class_='pages')
    if check_pagination:
        check_page = check_pagination.find('span',class_='dots')
        print(check_page)
        if check_page:
            reedDict['total_pages'] = 40
        else:
            reedDict['total_pages'] = int(check_pagination.find_all('a')[-2].text.strip())
    else:
        reedDict['total_pages'] = 1


    cards = soup.find_all('article',class_='job-result ')
    for card in cards:
        temp = {}
        try:
            temp['job_title'] = card.find('h3',class_='title').text.strip()
        except AttributeError:
            temp['job_title'] = None
        try:
            temp['detail_url'] = 'https://www.reed.co.uk{0}'.format(card.find('h3', class_='title').a.get('href'))
        except AttributeError:
            temp['detail_url'] = None
        try:
            temp['label'] = card.find('div',class_='badge-container ').label.text.strip()
        except AttributeError:
            temp['label'] = None
        try:
            temp['posted_by'] = card.find('div',class_='posted-by').a.text.strip()
        except AttributeError:
            temp['posted_by'] = None
        try:
            unwanted = card.find('div',class_='posted-by').span
            unwanted.extract()
            temp['posted_on'] = card.find('div',class_='posted-by').text.strip().replace('Posted','').replace(temp['posted_by'],'').replace('by','').strip()
        except AttributeError:
            temp['posted_on'] = None
        try:
            temp['salary'] = card.find('li',class_='salary').text.strip()
        except AttributeError:
            temp['salary'] = None
        try:
            temp['location'] = card.find('li',class_='location').text.strip().replace(' ','').replace('\n',', ')
        except AttributeError:
            temp['location'] = None
        try:
            temp['job_type'] = card.find('li',class_='time').text.strip()
        except AttributeError:
            temp['job_type'] = None
        try:
            temp['job_snippet'] = card.find('div',class_='description hidden-xs').text.strip()
        except AttributeError:
            temp['job_snippet'] = None


        if 'today' in temp['posted_on'].lower():
            temp['posted_on'] = datetime.now()
        elif 'yesterday' in temp['posted_on'].lower():
            temp['posted_on'] = datetime.now() - timedelta(days=1)
        elif 'days ago' in temp['posted_on'].lower():
            n = int(re.findall('\d+',temp['posted_on'])[0])
            temp['posted_on'] = datetime.now() - timedelta(days=n)

        # try:
        #     req_ = requests.get(temp['detail_url'])
        # except Exception as e:
        #     print(e)
        # soup_ = bs(req_.content,'lxml')
        # try:
        #     temp['job_description'] = soup_.find('div',class_='description').text.strip().replace('Apply now\n','')
        # except AttributeError:
        #     temp['job_description'] = None

        reedDict['data'].append(temp)

    return reedDict



# print(reed_jds('https://www.reed.co.uk/jobs/jobs-in-city-of-london'))

job_urls = ['https://www.reed.co.uk/location/south-east-england','https://www.reed.co.uk/location/south-west-england',
            'https://www.reed.co.uk/location/west-midlands-region','https://www.reed.co.uk/location/east-midlands',
            'https://www.reed.co.uk/location/east-anglia','https://www.reed.co.uk/location/north-west-england',
            'https://www.reed.co.uk/location/north-east-england','https://www.reed.co.uk/location/yorkshire-and-humberside',
            'https://www.reed.co.uk/location/scotland','https://www.reed.co.uk/location/northern-ireland',
            'https://www.reed.co.uk/location/wales']



def reed_loc(job_url):
    soup = souper(job_url)
    total_pages = soup.find('ul',class_='pages full').find_all('li')[-2].text.strip()
    page = 1
    data = []
    while page <= int(total_pages):
        city_list = soup.find('ul',class_='cities-list columns-list').find_all('li')
        county_list = soup.find('ul',class_='counties-list columns-list').find_all('li')
        main_list = city_list + county_list
        for city in main_list:
            temp = {}
            temp['city'] = city.a.text.strip().replace('Jobs in ','')
            temp['link'] = 'https://www.reed.co.uk{}'.format(city.a.get('href'))
            data.append(temp)
        page += 1
    return data

#
# data_= []
# for job_url in job_urls:
#     results = reed_loc(job_url)
#     for d in results:
#         temp_ = {}
#         temp_['link'] = d['link']
#         temp_['city'] = d['city']
#         data_.append(temp_)
#
# print(data_)

# print(reed_loc(job_urls[-2]))


def reed_company(job_url):
    soup = souper(job_url)
    total_pages = soup.find('ul', class_='pages full').find_all('li')[-2].text.strip()
    print(total_pages)
    page = 1
    data = []
    while page <= int(total_pages):
        comp_list = soup.find('div',class_='recruiter-dirtectory-main-content-logos row').find_all('div',class_='subtitle')
        for comp in comp_list:
            temp = {}
            temp['company'] = comp.a.text.strip().replace(' jobs','')
            temp['link'] = 'https://www.reed.co.uk{0}'.format(comp.a.get('href'))
            data.append(temp)
        page += 1
    return data

# data__ = reed_company('https://www.reed.co.uk/recruiterdirectory')
# print(data__)
# print(len(data__))

jobs_ch_urls = [{'region': 'German part of Switzerland', 'link': 'https://www.jobs.ch/en/vacancies/?region=2&term='}, {'region': 'Region of Zurich / Schaffhausen', 'link': 'https://www.jobs.ch/en/vacancies/?region=7&term='}, {'region': 'Eastern Switzerland / GR / FL', 'link': 'https://www.jobs.ch/en/vacancies/?region=11&term='}, {'region': 'Mittelland (AG / SO)', 'link': 'https://www.jobs.ch/en/vacancies/?region=12&term='}, {'region': 'Region of Bern', 'link': 'https://www.jobs.ch/en/vacancies/?region=13&term='}, {'region': 'Region of Basel', 'link': 'https://www.jobs.ch/en/vacancies/?region=14&term='}, {'region': 'Central Switzerland', 'link': 'https://www.jobs.ch/en/vacancies/?region=15&term='}, {'region': 'Region of Oberwallis', 'link': 'https://www.jobs.ch/en/vacancies/?region=16&term='}, {'region': 'Western Switzerland', 'link': 'https://www.jobs.ch/en/vacancies/?region=3&term='}, {'region': 'Region of Geneva', 'link': 'https://www.jobs.ch/en/vacancies/?region=6&term='}, {'region': 'Region of Neuchâtel / Jura', 'link': 'https://www.jobs.ch/en/vacancies/?region=8&term='}, {'region': 'Region of Fribourg', 'link': 'https://www.jobs.ch/en/vacancies/?region=9&term='}, {'region': 'Region of Vaud / Valais', 'link': 'https://www.jobs.ch/en/vacancies/?region=10&term='}, {'region': 'Ticino', 'link': 'https://www.jobs.ch/en/vacancies/?region=4&term='}, {'region': 'Abroad', 'link': 'https://www.jobs.ch/en/vacancies/?region=5&term='}]

def details_func(detail_url):
    try:
        details_data= []
        try:
            req = requests.get(detail_url)
        except Exception as e:
            details_data = None
            return details_data
        if req.status_code==200:
            soup = BeautifulSoup(req.content,'lxml')
            try:
                details_card = soup.find('div',class_='job_info').text.strip().replace('\xa0','').replace('\n','')
            except:
                details_card = None
            details_data.append(details_card)
            return details_data
    except Exception as e:
        print(str(e))
        return None


def jobstreet(detail_url):
    try:
        jobstreet_data =[]
        try:
            req = proxied_request(detail_url)
        except Exception as e:
            jobstreet_data=None
            return jobstreet_data
        if req.status_code==200:
            soup = BeautifulSoup(req.content,'lxml')
            details_obj = {}
            try:
                details_obj['job_desc'] = soup.find('div',id='job_description').text.strip().replace('\xa0',"").replace('\n','').replace('\r','')
            except:
                details_obj['job_desc'] = None
            try:
                loc = soup.find('div',class_='map-col-wraper').text.strip()
                pattern = re.compile(r"\s+")
                details_obj['details_location'] = pattern.sub(' ',loc).strip()
            except:
                details_obj['details_location'] = None
            try:
                firm_snapshot = soup.find_all('div',class_='col-lg-12 col-md-12 col-sm-12')[1].text.strip()
                details_obj['firm_snapshot'] = " ".join(firm_snapshot.split())
            except:
                details_obj['firm_snapshot'] = None
            try:
                details_obj['company_overview'] = soup.find('div',id='company_overview_all').text.strip().replace('\xa0',"").replace('\n','').replace('\r','').replace('\t','')
            except:
                details_obj['company_overview'] = None
            try:
                date_posted = soup.find(['p','span'],id='posting_date').text.strip().replace("Advertised: ",'')
                details_obj['posted_date'] = parse(date_posted)
            except:
                details_obj['posted_date'] = None
            jobstreet_data.append(details_obj)
        return jobstreet_data
    except Exception as e:
        print(str(e))
        return None

from dateparser import parse

def main_func(page_no):
    try:
        base_url = 'https://sg.jobsdb.com'
        source_url = 'https://sg.jobsdb.com/j?l=&p={0}&q=&surl=0&tk=YtRVt1yXuyxGftDXjFFo-hr3x3WphqlK3ctyCs45J'.format(page_no)
        jobsdb_dict = {}
        jobsdb_dict['success'] = True
        try:
            req = requests.get(source_url)
        except Exception as e:
            jobsdb_dict['success'] = False
            jobsdb_dict['errorMessage'] = str(e)
            return jobsdb_dict
        if req.status_code==200:
            data = []
            soup = BeautifulSoup(req.content, 'lxml')
            try:
                cards = soup.find(['div','ul'],class_='search-results-container').find_all('li',class_=['result sponsored trackable sponsored_top','result'])
            except:
                cards = []
            for item in cards:
                obj = {}
                try:
                    obj['title'] = item.div.div.h2.find('a').text.strip().replace('|','')
                except:
                    obj['title'] = None
                try:
                    details_url = item.div.div.a.get('href')
                    obj['details_url'] = '{0}{1}'.format(base_url, details_url)
                except:
                    obj['details_url'] = None
                try:
                    obj['company_name'] = item.div.div.find('span',class_='company').text.strip()
                except:
                    obj['company_name'] = None
                try:
                    obj['location'] = item.div.div.find('span',class_='location').text.strip()
                except:
                    obj['location'] = None
                try:
                    obj['summary'] = item.div.div.find('div',class_='summary').text.strip().replace('|','')
                except:
                    obj['summary'] = None
                try:
                    check_ad = item.div.div.div.find('span',class_='cite').text.strip()
                except:
                    check_ad = None
                try:
                    date = item.div.div.div.find('span',class_='date').text.strip()
                    date = date.replace('about', '').replace('ago','')
                    date = parse(date)
                except:
                    date = None
                if check_ad == 'AdJobstreet SG':
                    obj['details'] = jobstreet(detail_url=obj['details_url'])
                    obj['date'] = obj['details'][0]['posted_date']
                    del obj['details'][0]['posted_date']
                else:
                    obj['details'] = details_func(detail_url=obj['details_url'])
                    obj['date'] = date
                data.append(obj)
            jobsdb_dict['data'] = data
            jobsdb_dict['created_at'] = datetime.now()
            jobsdb_dict['updated_at'] = datetime.now()
            return jobsdb_dict
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return None


# pp.pprint(main_func('1'))


def jobs_ch_jds(job_url,page=1):
    jobDict = {}
    jobDict['success'] = True
    jobDict['data'] = []
    job_url = '{0}&page={1}='.format(job_url,str(page))
    req = requests.get(job_url)
    soup = bs(req.content,'lxml')
    cards = soup.find_all('div',class_='serp-item')
    for card in cards:
        temp = {}
        try:
            temp['job_title'] = card.find('h2',class_='e-heading serp-item-head-1').text.strip()
        except AttributeError:
            temp['job_title'] = None
        try:
            temp['detail_url'] = 'https://www.jobs.ch{0}'.format(card.find('h2',class_='e-heading serp-item-head-1').a.get('href'))
        except AttributeError:
            temp['detail_url'] = None
        try:
            temp['company_name'] = card.find('h3',class_='e-heading serp-item-head-2').a.get('title')
        except AttributeError:
            temp['company_name'] = None
        try:
            unwanted = card.find('a')
            unwanted.extract()
            temp['location'] = card.find('h3',class_='e-heading serp-item-head-2').text.strip().replace('—','').replace(temp['company_name'],'').strip()
        except AttributeError:
            temp['location'] = None
        try:
            temp['job_snippet'] = card.find('p', class_='hidden-xs serp-item-head-3').text.strip()
        except AttributeError:
            temp['job_snippet'] = None
        try:
            temp['date_posted'] = card.find('div', class_='badge-pool').find_all('span')[0].text.strip()
        except AttributeError:
            temp['date_posted'] = None
        try:
            temp['position'] = [c.text.strip() for c in card.find('div', class_='badge-pool').find_all('span') if 'position' in c.text.strip().lower()][0]
        except Exception as e:
            print(e)
            temp['position'] = None
        req_ = requests.get(temp['detail_url'])
        soup_ = bs(req_.content,'lxml')
        try:
            temp['job_description'] = soup_.find('div',class_='container vacancy-detail-content').text.strip()
        except AttributeError:
            temp['job_description'] = None
        jobDict['data'].append(temp)

    return jobDict

# print(jobs_ch_jds('https://www.jobs.ch/en/vacancies/?region=7&term='))

#
def keljobs(page=1):
    kelDict = {}
    kelDict['success'] = True
    kelDict['data'] = []
    job_url = 'https://www.keljob.com/recherche?page={0}'.format(str(page))
    req = requests.get(job_url)
    soup = bs(req.content,'lxml')
    try:
        kelDict['total_pages'] = int(soup.find('ul',class_='pagination').find_all('li')[-2].text.strip())
    except AttributeError:
        kelDict['total_pages'] = None

    cards = soup.find('section',class_='job-results').find_all('div',class_='search-offer clearfix')
    for card in cards:
        temp = {}
        try:
            temp['job_title'] = card.find('h2',class_='offre-title').text.strip()
        except AttributeError:
            temp['job_title'] = None
        try:
            temp['detail_url'] = 'https://www.keljob.com{0}'.format(card.find('h2',class_='offre-title').a.get('href'))
        except AttributeError:
            temp['detail_url'] = None
        try:
            temp['posted_on'] = card.find('li',class_='offre-date').text.strip()
        except AttributeError:
            temp['posted_on'] = None
        try:
            temp['contracts'] = card.find('li',class_='offre-contracts').text.strip()
        except AttributeError:
            temp['contracts'] = None
        try:
            temp['company_name'] = card.find('li',class_='offre-company').text.strip()
        except AttributeError:
            temp['company_name'] = None
        try:
            temp['location'] = card.find('li',class_='offre-location').text.strip()
        except AttributeError:
            temp['location'] = None
        try:
            temp['job_summary'] = card.find('p',class_='job-description').text.strip()
        except AttributeError:
            temp['job_summary'] = None

        if 'heure' in temp['posted_on']:
            n_h = re.findall('\d+',temp['posted_on'])[0]
            temp['posted_on'] = datetime.now() - timedelta(hours=int(n_h))
        elif 'jours' in temp['posted_on']:
            n_d = re.findall('\d+',temp['posted_on'])[0]
            temp['posted_on'] = datetime.now() - timedelta(days=int(n_d))

        req_ = requests.get(temp['detail_url'])
        soup_ = bs(req_.content, 'lxml')
        try:
            temp['job_description'] = soup_.find('div', class_='content').text.strip()
        except AttributeError:
            temp['job_description'] = None

        kelDict['data'].append(temp)

    return kelDict

# pp.pprint(keljobs(page=100))

def seek_jds(page=1):
    seekDict = {}
    seekDict['success'] =True
    seekDict['data'] = []
    job_url = 'https://www.seek.com.au/jobs?page={0}'.format(str(page))
    req = requests.get(job_url)
    soup = bs(req.content,'lxml')
    cards = soup.find('div',class_='_365Hwu1').find_all('article')
    print(len(cards))
    for card in cards:
        temp = {}
        try:
            temp['job_title'] = card.find('span',class_='_3FrNV7v _3Eb3poo HfVIlOd _2heRYaN E6m4BZb').h1.text.strip()
        except AttributeError:
            temp['job_title'] = None
        try:
            temp['detail_url'] = 'https://www.seek.com.au{0}'.format(card.find('span',class_='_3FrNV7v _3Eb3poo HfVIlOd _2heRYaN E6m4BZb').h1.a.get('href'))
        except AttributeError:
            temp['detail_url'] = None
        try:
            temp['company_name'] = card.find('span',class_='_3FrNV7v _3PZrylH E6m4BZb').a.text.strip()
        except AttributeError:
            temp['company_name'] = None

        temp['location'] = {}
        try:
            temp['location']['city'] = [c.text.strip() for c in card.find('div',class_='_1mzsMx5').find_all('span',class_='Eadjc1o') if 'location' in c.text.strip()][0].replace('location: ','')
        except AttributeError:
            temp['location']['city'] = None
        except IndexError:
            temp['location']['city'] = None
        try:
            temp['location']['area'] = [c.text.strip() for c in card.find('div',class_='_1mzsMx5').find_all('span',class_='Eadjc1o') if 'area' in c.text.strip()][0].replace('area: ','')
        except AttributeError:
            temp['location']['area'] = None
        except IndexError:
            temp['location']['area'] = None
        temp['classification'] = {}
        try:
            temp['classification']['class'] = [c.text.strip() for c in card.find('div',class_='_1mzsMx5').find_all('span',class_='Eadjc1o') if 'classification' in c.text.strip()][0].replace('classification: ','')
        except AttributeError:
            temp['classification']['class'] = None
        except IndexError:
            temp['classification']['class'] = None
        try:
            temp['classification']['subclass'] = [c.text.strip() for c in card.find('div',class_='_1mzsMx5').find_all('span',class_='Eadjc1o') if 'subClassification' in c.text.strip()][0].replace('subClassification: ','')
        except AttributeError:
            temp['classification']['subclass'] = None
        except IndexError:
            temp['classification']['subclass'] = None
        try:
            temp['salary'] = card.find('div',class_='_1mzsMx5').find('span',attrs={'data-automation' : 'jobSalary'}).find_next('span').text.strip()
        except AttributeError:
            temp['salary'] = None
        except IndexError:
            temp['salary'] = None
        try:
            temp['date_posted'] = parse(card.find('span',attrs={'data-automation' : 'jobListingDate'}).text.strip())
        except AttributeError:
            temp['date_posted'] = None
        try:
            temp['label'] = card.find('span',attrs={'data-automation' : 'jobPremium'}).text.strip()
            if 'Featured' in temp['label']:
                temp['date_posted'] = datetime.now()
        except AttributeError:
            temp['label'] = None
        try:
            temp['job_summary'] = card.find('span',attrs={'data-automation' : 'jobShortDescription'}).text.strip()
        except AttributeError:
            temp['job_summary'] = None
        try:
            temp['listings'] = [i.text.strip() for i in card.find('ul',class_='_1mzsMx5').find_all('li')][0]
        except AttributeError:
            temp['listings'] = None
        except IndexError:
            temp['listings'] = None

        req_ = requests.get(temp['detail_url'])
        soup_ = bs(req_.content, 'lxml')
        try:
            desc = soup_.find('div',attrs={'data-automation' : 'jobDescription'})
            if desc:
                desc = desc.text.split("-->").pop().strip()
            else:
                desc = soup_.find('div', class_='templatetext').text.split("-->").pop().strip()
        except AttributeError:
            desc = None
        temp['job_description'] = re.sub('\<[^)]*\>', '', desc)
        seekDict['data'].append(temp)
    return seekDict

print(seek_jds(1))
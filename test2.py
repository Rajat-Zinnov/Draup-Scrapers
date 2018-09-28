from selenium import webdriver
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup as bs
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

path_to_gecko = '/home/admin/Downloads/geckodriver'
display = Display(visible=0, size=(1920, 1080)).start()
browser = webdriver.Firefox(executable_path=path_to_gecko)
url = 'http://www.owler.com/iaApp/article/5b3353b046e0fb0056e80b8b.htm?utm_source=api&utm_medium=api&utm_campaign=api'
browser.get(url)
html = browser.execute_script('return document.documentElement.outerHTML')

soup = bs(html,'lxml')
delay = 50
try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'article-description'))
    WebDriverWait(browser, delay).until(element_present)
    print ("Page is ready!")
    print(element_present)
except TimeoutException:
    print ("Loading took too much time!")

# print(soup)
# print(soup.find('h2',class_='article-description').text)



#owler_url = 'http://www.owler.com/iaApp/article/5b3353b046e0fb0056e80b8b.htm?utm_source=api&utm_medium=api&utm_campaign=api'

# driver = webdriver.PhantomJS(executable_path="/home/admin/Downloads/phantomjs")
# driver.get(owler_url)
# html = driver.execute_script("return document.documentElement.outerHTML")
# soup = bs(html,'lxml')

#r = requests.get(owler_url)
#soup = bs(r.text,'lxml')
#snip = soup.find_all('script')

#print(snip)

# snip = soup.find('h2',class_='article-description').text
# print(snip)

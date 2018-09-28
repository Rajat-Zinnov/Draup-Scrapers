from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import os

url = 'http://www.owler.com/iaApp/article/5b3353b046e0fb0056e80b8b.htm?utm_source=api&utm_medium=api&utm_campaign=api'
path = '/home/admin/Downloads/chromedriver' #PATH ON LOCAL
os.environ['webdriver.chrome.driver'] = path
display =Display(visible=0, size=(800,600))
display.start()
driver = webdriver.Chrome(path)
driver.get(url)

q = driver.find_element_by_class_name('article-description')
q.send_keys('python')
q.send_keys(Keys.RETURN)
assert 'python' in driver.title
print(q)



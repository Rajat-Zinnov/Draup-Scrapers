from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
from sys import exit
from time import sleep

disneyland_url = "http://disneyland.disney.go.com/maps/service-details/18583410%3bentitytype%3dguest-service"
disneyworld_url = "http://disneyworld.disney.go.com/maps/service-details/18579731%3bentitytype%3dguest-service"

names_xpath = "//div[@class='textContainer']/div/text()"
coords_xpath = "//div[@class='textContainer']/parent::div/@data-id"

dlString = ""
dwString = ""

def scrape(url):
    global browser
    htmlString = ""
    display = Display(visible=0, size=(800, 600))
    display.start()
    print ("Displaying")
    for retry in range(3):
        try:
            browser = webdriver.Firefox()
            break
        except:
            sleep(3)
    try:
        browser.get("http://disneyland.disney.go.com/maps/service-details/18583410%3bentitytype%3dguest-service")
        print (browser.title)
        WebDriverWait(browser, 50).until(EC.presence_of_element_located((By.CLASS_NAME, "textContainer")))
        innerHTML = browser.execute_script("return document.body.innerHTML")
        htmlString = innerHTML
    except:
        print ("Website didn't load in time")
        browser.quit()
        display.stop()
        exit("Website Error")
    finally:
        browser.quit()
        display.stop()

    tree = html.fromstring(htmlString)
    print(htmlString)
    names = tree.xpath(names_xpath)
    print(names)

scrape('http://www.owler.com/iaApp/article/5b3353b046e0fb0056e80b8b.htm?utm_source=api&utm_medium=api&utm_campaign=api')

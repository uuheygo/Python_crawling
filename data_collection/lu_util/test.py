from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

browser = webdriver.Firefox()
url = "http://www.forbes.com/top-colleges/list/"
browser.get(url)
browser.implicitly_wait(10)
browser.get('http://www.forbes.com/colleges/united-states-military-academy/?list=top-colleges')
browser.implicitly_wait(10)
browser.back()
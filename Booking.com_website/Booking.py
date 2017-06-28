from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import time
import requests
from datetime import datetime
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1024, 768))
display.start()


month_map = {"January":'01' , "February": '02' , "March":'03',"April":'04',"May":'05',"June":'06',"July":'07',"August":'08',"September":'09',"October":'10',"November":11,
    "December":'12'}
def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 30)
    return driver

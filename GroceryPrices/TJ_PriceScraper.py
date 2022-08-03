# import dependencies
from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'https://www.traderjoes.com/home/products/category/food-8'
#url = 'http://olympus.realpython.org/profiles/dionysus'
#url = 'https://coinmarketcap.com/'

print(requests.get(url)) # returns status code; 200 is sucessful request

# enabling selenium's headless mode
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')

# making webdriver instance for Chrome browser
# driver = webdriver.Chrome(chrome_options=options)
driver = webdriver.Chrome()

# going to website
driver.get(url)
time.sleep(3)

page = driver.page_source # getting page html
driver.quit() # ends session

# instantiating BeatifulSoup; passing website's html and specifying parser
soup = BeautifulSoup(page, 'html.parser')

# finds all <li> tags with given class attribute 
html_product_name = soup.find_all('h2', class_='ProductCard_card__title__text__uiWLe')
html_price_quantity = soup.find_all('div', class_='ProductPrice_productPrice__1Rq1r ProductCard_card__productPrice__1W4Le')

print(html_product_name)

product_names = [i.get_text() for i in html_product_name]
price_quantity = [i.get_text() for i in html_price_quantity]
print(product_names)
print(price_quantity)

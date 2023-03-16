from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

# The Tony Fresh Market website requires the user to select a store location to view the price of any product.
# So without selecting a location, it is not possible to scrape the product data. 
# This script solves this issue

# cookies generated after I manually selected a store location on the website
# each dict is a cookie-value pair
cookies = [
	{"name":"_ga", "value": "GA1.1.907722779.1678302301"},
	{"name": "_ga_0MCW5VWV52", "value": "GS1.1.1678302311.1.0.1678302316.0.0.0"},
	{"name": "_ga_2CFGBMWTYQ", "value": "GS1.1.1678302301.1.1.1678302316.0.0.0"},
	{"name": "fp-history", "value": '{"0":{"name":"shop","stateParams":{"q":"jasmine rice"}},"1":{"name":"store-locator"}}'},
	{"name": "fp-pref",	"value": '{"store_id":"5809"}'},
	{"name": "fp-session", "value": '{"token":"d0912d11fd5e6959002e22b89d77b4ba"}'},
	{"name": "SGPBShowingLimitationDomain670", "value": '{"openingCount":1,"openingPage":""}'}
]

prod_card_selector = "li.fp-item.fp-item-fixed_price"
prod_data_selector = "div.fp-item-name.notranslate,span.fp-item-base-price,span.fp-item-size"

driver = webdriver.Chrome()

page_url = "https://www.tonysfreshmarket.com/shop?q=jasmine+rice"
error_url = "https://www.tonysfreshmarket.com/404"
driver.get(page_url)

# extra time is needed for all of the website's requests to finish
sleep(3)

# add all of the cookies to the selenium session
for cook in cookies:
	driver.add_cookie(cook)

# refresh to GET request with cookies in place
driver.refresh()

# arbiturary time used to see if website now shows a selected location
sleep(8)
html = driver.page_source
driver.quit()

soup = BeautifulSoup(html, 'html.parser')
product_cards = soup.select(prod_card_selector)[:]

prod_data = [
	
	",".join(

	[
	element.text 
	for element in product.select(prod_data_selector)
	]

	) for product in product_cards

	]

# for product in product_cards:
# 	temp_holder = [element.text for element in product.select(prod_data_selector)]
	# prod_data.append(",".join(temp_holder))

print(prod_data)
# print([datum.text for datum in data])
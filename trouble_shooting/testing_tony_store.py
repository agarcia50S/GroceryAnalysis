from selenium import webdriver
from time import sleep
# The Tony Fresh Market website requires the user to select a store location to view the price of any product.
# So without selecting a location, it is not possible to scrape the product data. 
# This script solves this issue

driver = webdriver.Chrome()

page_url = "https://www.tonysfreshmarket.com/shop?q=jasmine+rice"
error_url = "https://www.tonysfreshmarket.com/404"
driver.get(page_url)

# cookies generated after I manually selected a store location on the website
# each dict is a cookie-value pair
cookies = [
	{"name":"_ga", "value": "GA1.1.907722779.1678302301"},
	{"name": "_ga_0MCW5VWV52", "value": "GS1.1.1678302311.1.0.1678302316.0.0.0"},
	{"name": "_ga_2CFGBMWTYQ", "value": "GS1.1.1678302301.1.1.1678302316.0.0.0"},
	{"name": "fp-history", "value": '{"0":{"name":"shop","stateParams":{"q":"jasmine rice"}},"1":{"name":"store-locator"}}'},
	{"name": "fp-pref",	"value": '{"store_id":"5809"}'},
	{"name": "fp-session", "value": '{"token":"f44f6ef2fc1b992b282996fc3920e947"}'},
	{"name": "SGPBShowingLimitationDomain670", "value": '{"openingCount":1,"openingPage":""}'}
]
# extra time is needed for all of the website's requests to finish
sleep(3)

# add all of the cookies to the selenium session
for cook in cookies:
	driver.add_cookie(cook)

# refresh to GET request with cookies in place
driver.refresh()

# arbiturary time used to see if website now shows a selected location
sleep(15)
driver.quit()


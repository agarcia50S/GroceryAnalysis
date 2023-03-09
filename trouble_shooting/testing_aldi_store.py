from selenium import webdriver
from time import sleep

driver = webdriver.Chrome()
page_url = "https://new.aldi.us/results?query=jasmine+rice"
driver.get(page_url)
cookies = [
	{"name":"_gcl_au", "value": "1.1.583616297.1678311439"},
	{"name": "adobeujs-optin", "value": '{"aam":false,"adcloud":false,"aa":false,"campaign":false,"ecid":false,"livefyre":false,"target":false,"mediaaa":false}'},
	{"name": "at_check", "value": "True"},
	{"name": "mbox", "value": "session#a6409b1fdc04457fa1751c7028ad5fa0#1678313300"},
	{"name": "OptanonConsent",	"value": "isGpcEnabled=0&datestamp=Wed+Mar+08+2023+15:38:51+GMT-0600+(Central+Standard+Time)&version=202211.2.0&isIABGlobal=false&hosts=&consentId=32e73755-0fc8-4430-8d77-2b1e888fb9ea&interactionCount=1&landingPath=https://new.aldi.us/results?query=jasmine%20rice&groups=C1:1,C2:0,C4:0"},
]
sleep(3)
for cook in cookies:
    driver.add_cookie(cook)

driver.refresh()
sleep(15)
driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from time import sleep
from bs4 import BeautifulSoup


# grocery_list = ['meat', 'produce', 'dairy', 'frozen foods', 'bread AND bakery', 
#                 'beverages', 'baking goods', 'pantry food',  'seafood', 'snacks', 
#                 'pastry', 'deli', 'coffee']

grocery_list = ['meat', 'produce']

wd = webdriver.Chrome()

def get_page_count(driver, xpath):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except TimeoutException:
        print('Could not find element')

    else:
        page_num = int(element.text[-2:])
        return page_num


for i in grocery_list:
    page_indx = 0
    term = i
    url = f"https://www.target.com/s?searchTerm={term}&sortBy=relevance&category=5xt1a&Nao={page_indx}&moveTo=product-list-grid"
    wd.get(url) # navigates to url; returns none
    sleep(5)
    page_num_xpath = "//span[@class='Pagination__StyledSpan-sc-sq3l8r-5 gyBTAO']"
    num_max = get_page_count(wd, page_num_xpath)

    for _ in range(num_max - 1):
        url = f"https://www.target.com/s?searchTerm={term}&sortBy=relevance&category=5xt1a&Nao={page_indx}&moveTo=product-list-grid"
        wd.get(url) # navigates to url; returns none
        sleep(4.5)
        print(wd.page_source)
        page_indx += 24

wd.quit()

# soup = BeautifulSoup(response, 'html.parser')
# print(soup)
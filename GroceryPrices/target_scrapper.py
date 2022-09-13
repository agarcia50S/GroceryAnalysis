from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup


# grocery_list = ['meat', 'produce', 'dairy', 'frozen foods', 'bread AND bakery', 
#                 'beverages', 'baking goods', 'pantry food',  'seafood', 'snacks', 
#                 'pastry', 'deli', 'coffee']

grocery_list = ['meat', 'produce']

wd = webdriver.Chrome()

for i in grocery_list:
    page_indx = 0
    term = i
    url = f"https://www.target.com/s?searchTerm={term}&sortBy=relevance&category=5xt1a&Nao={page_indx}&moveTo=product-list-grid"
    wd.get(url) # navigates to url; returns none
    sleep(5)
    page_num_html = wd.find_element(By.XPATH, "//span[@class='Pagination__StyledSpan-sc-sq3l8r-5 gyBTAO']")
    num_max = int(page_num_html.text[-2:])

    for _ in range(num_max - 1):
        url = f"https://www.target.com/s?searchTerm={term}&sortBy=relevance&category=5xt1a&Nao={page_indx}&moveTo=product-list-grid"
        wd.get(url) # navigates to url; returns none
        sleep(4.5)
        print(wd.page_source)
        page_indx += 24

wd.quit()

# soup = BeautifulSoup(response, 'html.parser')
# print(soup)

print('hello'[-2:])
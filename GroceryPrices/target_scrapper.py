from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from time import sleep
from bs4 import BeautifulSoup

class TargetScrapper():
    def __init__(self, driver, url, last_pg_xpath, categories):
        self.driver = driver
        self.url = url
        self.last_pg_xpath = last_pg_xpath
        self.categories = categories

    def get_page_count(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.last_pg_xpath))
            )
        except TimeoutException:
            print('Could not find element')
        else:
            page_num = int(element.text[-2:])
            return page_num

    def find_products(self):
        for item in self.categories:
            url_parts = self.url.split('&')
            page_indx = 0

            # getting parts of url-- 'SearchTerm=' and 'nao=' 
            term_indx, num_indx = url_parts[0].find('='), url_parts[3].find('=') # assign indx of char '='
            url_part_0, url_part_3 = url_parts[0][:term_indx + 1], url_parts[3][:num_indx + 1] # assign url parts

            # constructing url for given item and page index
            url = f'{url_part_0}{item}&{url_parts[1]}&{url_parts[2]}&{url_part_3}{page_indx}&{url_parts[4]}'

            self.driver.get(url) # navigates to url; returns none
            last_pg_num = self.get_page_count() - 1 # remove current pg from total

            for _ in range(last_pg_num):
                url = f'{url_part_0}{item}&{url_parts[1]}&{url_parts[2]}&{url_part_3}{page_indx}&{url_parts[4]}'
                wd.get(url) # navigates to url; returns none
                sleep(4.5)
                print(wd.page_source)
                page_indx += 24

                # FOR TESTING
                if page_indx >= 96: 
                    break
        self.driver.quit()

    @staticmethod
    def make_xpath(tag, attr, val):
        '''
        Makes a relative xpath for an html element. xpath 
        form is //tagname[@attribute='value']
        '''
        return f"//{tag}[@{attr}='{val}']"

# soup = BeautifulSoup(response, 'html.parser')
# print(soup)

if __name__ == '__main__':
    
    # https://www.target.com/s?searchTerm=meat&sortBy=relevance&category=5xt1a&Nao=0&moveTo=product-list-grid

    # grocery_list = ['meat', 'produce', 'dairy', 'frozen foods', 'bread AND bakery', 
    #                 'beverages', 'baking goods', 'pantry food',  'seafood', 'snacks', 
    #                 'pastry', 'deli', 'coffee']

    grocery_list = ['meat', 'produce']

    wd = webdriver.Chrome()

    # pagination html info
    tag = 'span'
    attr = 'class'
    val = 'Pagination__StyledSpan-sc-sq3l8r-5 gyBTAO'

    pg_num_xpath = TargetScrapper.make_xpath(tag, attr, val)
    url = 'https://www.target.com/s?searchTerm=meat&sortBy=relevance&category=5xt1a&Nao=0&moveTo=product-list-grid'
    bot = TargetScrapper(wd, url, pg_num_xpath, grocery_list)
    bot.find_products()
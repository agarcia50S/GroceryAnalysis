from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from time import sleep
from bs4 import BeautifulSoup

import csv

class AldiScrapper:

    def __init__(self, categories, sub_category_attr, base_url, driver):
        self.categories = categories
        self.sub_category_attr = sub_category_attr
        self.base_url = base_url
        self.driver = driver

    # fnc that makes url
    def make_url(self, relative_url):
        return self.base_url + relative_url

    # make fnc collects all sub-category urls
    def collect_sub_category_urls(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        sub_category_elements = soup.find_all('a', attrs= self.sub_category_attr)

        # return list of urls as str types
        return [self.make_url(i['href']) for i in sub_category_elements]
        
    # make func that goes to a given page
    def get_page_source(self, url):
        self.driver.get(url)
        self.driver.refresh()
        sleep(3)
        return driver.page_source

    # store all urls
    def store_first_page_urls(self, csv_path=None):
        urls = []
        for category in self.categories:

            source = self.get_page_source(self.make_url(f'/shop/aisles/{category}.html'))
            urls += self.collect_sub_category_urls(source)

        # output: csv file with all urls
        if csv_path != None:
            with open(csv_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows([[url] for url in urls])

        else: return urls
    
    def extract_urls_from_csv(self, csv_path):
        with open(csv_path, mode='r') as in_file:
            return [row.rstrip() for row in in_file]

    # collect product info
    def collect_product_info(self, csv_path):
        product_data = []
        for url in self.extract_urls_from_csv(csv_path):
            temp_container = []
            soup = BeautifulSoup(self.get_page_source(url), 'html.parser')
            prod_count = int(soup.find('span', {'class':'category-count title-sm'}).text.strip()[1:-1]) # find total product count
            page_count = 1
            while len(temp_container) < prod_count:
                # combine lists with Tag objects into one big list
                temp_container += soup.find_all('div', {'class':'product-card-container product-card-container--with-out-ar'})
                page_count += 1
                driver.get(f'{url}?sort=&page={str(page_count)}')
                sleep(1)
            product_data += temp_container
            print(len(temp_container))
        return product_data                   

if __name__ == '__main__':
    from selenium import webdriver

    main_categories = ['beverages', 'bread-bakery', 'breakfast-cereal', 'canned-goods-soups', 
                       'condiments-spice-bake', 'cookies-snacks-candy', 'dairy-eggs-cheese',
                       'deli', 'forzen-foods', 'fruits-vegetables', 'grains-pasta-sides',
                       'meat-seafood', 'wine-beer-spirits']
    
    base_url = f'https://www.jewelosco.com'
    driver = webdriver.Chrome()
    t = AldiScrapper(main_categories, {'class':'sbc-link'}, base_url, driver)
    url_csv_path = '/Users/agarc/PersonalProjects/test_data/aldi_subcategory_urls.csv'
    t.store_first_page_urls(csv_path=url_csv_path)

    page_source_path = '/Users/agarc/PersonalProjects/test_data/aldi_subcategory_pg_source.html'
    # print(len(t.collect_product_info(url_csv_path)))
    driver.quit()

# https://www.jewelosco.com/shop/aisles/beverages/soft-drinks.3441.html?sort=&page=1
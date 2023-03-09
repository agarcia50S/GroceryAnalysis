from time import sleep
import urllib.parse
from bs4 import BeautifulSoup

# scrape the entire page source of a website
class GroceryScraper:
    def __init__(self, driver, all_websites=None):
        if all_websites is None: self.all_websites = []
        else: self.all_websites = all_websites

        self.driver = driver

    def _main(self):
        # Incomplete

        
        for website in self.all_websites:
            html = self._get_page_source(website)
        

    def _extract(self, html):
        '''
        Takes a single html element that contains the name, quantity, and price 
        of a given product
        '''
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.select()
        return [datum.text for datum in data]
    
    def format_as_table(self, html_elements):
        '''
        Takes list of html elements. Each element contains the name, price, and 
        quantity for a given grocery product. Returns a table in the following 
        format: [[name-quantity_1, price_1], ..., [name-quantity_n, price_n]]
        '''
        return [self.get_data_from_html(elmnt) for elmnt in html_elements]

    def _get_page_source(self, website):
        
        self.driver.get(website["url"])
        sleep(3)
        if len(website["cookies"]) > 0: self.share_cookies(website["cookies"])
        self.driver.refresh()
        return self.driver.page_source

    def _share_cookies(self, jar):
        '''
        Takes list of dict's, each containing two pairs: 
        {name: cookie's name, value: cookies value}. 
        Adds the cookies to selenium session
        RETURN None
        '''
        if len(jar) == 1: self.driver.add_cookie(jar[0])
        else:
            for cookie in jar:
                self.driver.add_cookie(cookie)
        
class ProductCardParser:
    def __init__(self, product_cards):
        self.product_card = product_cards





if __name__ == '__main__':
    from urllib.parse import urlparse
    urls =  [
        "https://www.jewelosco.com/shop/search-results.html?q=",
        "https://www.traderjoes.com/home/search?q=&section=products&global=no",
        "https://www.target.com/s?searchTerm=&sortBy=relevance&category=5xt1a",
        "https://www.tonysfreshmarket.com/shop#!/?q="
    ]

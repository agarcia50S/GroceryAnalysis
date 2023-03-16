from time import sleep
from urllib.parse import *
from bs4 import BeautifulSoup

# utility functions

def get_netloc_name(url):
    '''
    Takes urlparse obj and parses the netloc attr to get the netloc "name"
    '''
    if not isinstance(url, ParseResult):
        url = urlparse(url)
    
    parts = url.netloc.split('.')
    if len(parts) < 3: return parts[0]
    else: return parts[1]
    
def make_url_query(url, search_term):
    url.query = f"{url.query}{search_term}"
    return urlunparse(url)

# scrape the entire page source of a website
class GroceryScraper:
    def __init__(self, driver, grocery_list=None, all_websites=None):
        if all_websites is None: self.all_websites = []
        else: self.all_websites = self._parse_urls(all_websites) # make urlparse objs

        if grocery_list is None: self.grocery_list = grocery_list
        else: self.grocery_list = grocery_list
        self.driver = driver
        
        # container with product data from each website
        self.all_products = []

    def _main(self):
        # Incomplete

        for website in self.all_websites:
            # get company name
            store_name = get_netloc_name(website['url'])

            for item in self.grocery_list:
                # add item to website url's query string
                url = make_url_query(website['url'])

                html = self._get_page_source(website, url)

                # find all product cards on page
                soup = BeautifulSoup(html, 'html.parser')
                product_cards = soup.select(website['product_card_css'])

                # parse product name, quantity, and price
                product_data = self._extract(product_cards)

                # associate company name, item name, and product data
                item_info = (store_name, item, product_data)
            
                self.all_products.append(item_info)
                
        return self.all_products

    def _extract(self, bs4_tags, website):
        '''
        Takes list of bs4.element.Tag (i.e. html elements that comprise the websites
        product cards) and iterate over it. In each loop, it uses .select() on the Tag
        object to find html elements based on css selectors 
        (i.e. website["product_data_css"]), extracts the text, and adds them to a list.
        The list's items are joined into a list on ",".
        '''
        return [
	
        ",".join(

        [element.text for element in tag.select(website["product_data_css"])]

        ) for tag in bs4_tags

        ]

    def format_as_table(self, html_elements):
        '''
        Takes list of html elements. Each element contains the name, price, and 
        quantity for a given grocery product. Returns a table in the following 
        format: [[name-quantity_1, price_1], ..., [name-quantity_n, price_n]]
        '''
        return [self._extract(elmnt) for elmnt in html_elements]

    def _get_page_source(self, website, url):
        
        self.driver.get(url)
        sleep(3)
        if len(website["cookies"]) > 0: self._share_cookies(website["cookies"])
        self.driver.refresh()
        return self.driver.page_source

    def _parse_urls(self):
        '''
        Makes all of the urls into urlparse objects so that the grocery list
        items can be added to the query string
        '''
        for website in self.all_websites:
            website["url"] = urlparse(website["url"])

    def add_website_info(self, url, selector, cookie=None):
        '''
        Takes the url, css selectors (to find the product data), optionally, the
        cookies of a single website and them to a list with all of the websites
        info.

        url -- string
        selector -- string
        cookie -- list of dictionary's with each dict representing one 
                  cookie-value pair {'name':'cookie's name', 'value':'cookie's value'}
        '''
        self.all_websites.append(
            {
            "url": url,
            "selector": selector,
            "cookie": cookie
            }
        )

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

if __name__ == '__main__':
    from urllib.parse import urlparse
    urls =  [
        "https://www.jewelosco.com/shop/search-results.html?q=",
        "https://www.traderjoes.com/home/search?q=&section=products&global=no",
        "https://www.target.com/s?searchTerm=&sortBy=relevance&category=5xt1a",
        "https://www.tonysfreshmarket.com/shop#!/?q="
    ]

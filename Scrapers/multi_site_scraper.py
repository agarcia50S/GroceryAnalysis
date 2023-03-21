from time import sleep
from urllib.parse import *
from bs4 import BeautifulSoup

# utility functions

def format_cookie(cookie_seq):
    '''
    Takes sequence of cookies (e.g. name1=value1; name2=value2; ...; nameX=valueX)
    and formats them into a structure that works with selenium 
    (i.e. [{'name':name1, 'value':value1}, {'name':name2, 'value':value2}] )
    '''
    cookie_pairs = cookie_seq.split(';')

    # list of dicts where values are cookie name and cookie value, respectively
    formatted = [{'name': pair.strip().split('=')[0], 'value':pair.strip().split('=')[1]} for pair in cookie_pairs]
    return formatted
    
        

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
    # check if url even has query component
    if len(url.query) < 1:
        return url._replace(path=url.path + search_term).geturl()
    # find position to add search term in
    idx = 0
    char = url.query[idx]
    while char != "=":
        idx += 1
        char = url.query[idx]

    # add search term to the url's query string
    full_query = f"{url.query[:idx + 1]}{search_term}{url.query[idx + 1:]}"

    new_url = url._replace(query=full_query).geturl()
    return new_url

# scrape the entire page source of a website
class GroceryScraper:
    def __init__(self, driver, grocery_list=None, all_websites=None):
        if all_websites is None: 
            self.all_websites = []
        else: 
            self.all_websites = all_websites
            self._parse_urls() # make urlparse objs

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
                url = make_url_query(website['url'], item)

                html = self._get_page_source(website, url)

                # find all product cards on page
                soup = BeautifulSoup(html, 'html.parser')
                product_cards = soup.select(website['product_card_css'])

                # parse product name, quantity, and price
                product_data = self._extract(product_cards, website)

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
        sleep(8)
        return self.driver.page_source

    def _parse_urls(self):
        '''
        Makes all of the urls into urlparse objects so that the grocery list
        items can be added to the query string
        '''
        for website in self.all_websites:
            website["url"] = urlparse(website["url"])

    def add_website_info(self, url, product_card_css, product_data_css, cookie=None):
        '''
        Takes the url, css selectors (to find the product data), optionally, the
        cookies of a single website and them to a list with all of the websites
        info.

        url -- string
        cookie -- list of dictionary's with each dict representing one 
                  cookie-value pair {'name':'cookie's name', 'value':'cookie's value'}
        '''
        self.all_websites.append(
            {
            "url": url,
            "cookies": cookie,
            "product_card_css": product_card_css,
            "product_data_css": product_data_css
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
    from selenium import webdriver
    grocery_sites = [
            {
            "url": "https://www.jewelosco.com/shop/search-results.html?q=",
            "cookies": [],
            "product_card_css": "div.product-card-container.product-card-container--with-out-ar",
            "product_data_css": "a.product-title__name,span[data-qa=prd-itm-prc],div[data-qa=prd-itm-pprc-qty]"
            },
            
            {
            "url": "https://www.tonysfreshmarket.com/shop?q=",
            "cookies": [
        
                {"name":"_ga", "value": "GA1.1.907722779.1678302301"},
                {"name": "_ga_0MCW5VWV52", "value": "GS1.1.1678302311.1.0.1678302316.0.0.0"},
                {"name": "_ga_2CFGBMWTYQ", "value": "GS1.1.1678302301.1.1.1678302316.0.0.0"},
                {"name": "fp-history", "value": '{"0":{"name":"shop","stateParams":{"q":"jasmine rice"}},"1":{"name":"store-locator"}}'},
                {"name": "fp-pref",	"value": '{"store_id":"5809"}'},
                {"name": "fp-session", "value": '{"token":"f44f6ef2fc1b992b282996fc3920e947"}'},
                {"name": "SGPBShowingLimitationDomain670", "value": '{"openingCount":1,"openingPage":""}'}

                ],
            "product_card_css": "li.fp-item.fp-item-fixed_price",
            "product_data_css": "div.fp-item-name.notranslate,span.fp-item-base-price,span.fp-item-size"
            },

            {
            "url": "https://www.target.com/s?searchTerm=&sortBy=relevance&category=5xt1a",
            "cookies": [],
            "product_card_css": "div[data-test=product-details]",
            "product_data_css": "a[data-test=product-title],span[data-test=current-price]"
            },

            {
            "url": "https://www.traderjoes.com/home/search?q=&section=products&global=no",
            "cookies": [],
            "product_card_css": "article.SearchResultCard_searchResultCard__3V-_h",
            "product_data_css": "a.Link_link__1AZfr.SearchResultCard_searchResultCard__titleLink__2nz6x,span.ProductPrice_productPrice__price__3-50j,span.ProductPrice_productPrice__unit__2jvkA"
            },

            {
            "url": "https://new.aldi.us/results?query=",
            "cookies": [],
            "product_card_css": "div.product-teaser-item.product-grid__item",
            "product_data_css": "div.product-tile__name,span.base-price__regular"
            }        
    ]

    my_list = ['jasmine rice']

    wd = webdriver.Chrome()
    test_bot = GroceryScraper(driver=wd, 
                              grocery_list=my_list, 
                              all_websites=grocery_sites)
    
    data = test_bot._main()
    print(data)
    wd.quit()
    
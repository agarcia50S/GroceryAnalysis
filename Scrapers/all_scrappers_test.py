from time import sleep
import urllib.parse
from bs4 import BeautifulSoup
# create url
def format_url(base_url, params={}):
    return f"{base_url}{urllib.parse.urlencode(params)}"

# GET request url and retrieve page's html
def get_page_source(url, driver):
    driver.get(url)
    driver.refresh()
    sleep(5)
    html = driver.page_source
    return html

# find html with product name, quantity, and price
def find_product_html(pg_source, css_selector):
    soup = BeautifulSoup(pg_source, 'html.parser')
    return soup.select(css_selector)
   
def main(url, driver, css_sel):
    html = get_page_source(url, driver)
    return find_product_html(html, css_sel)

if __name__ == '__main__':
    # from selenium import webdriver
    
    # # urls with css selector to find product data
    # web_info ={
    #     "https://www.jewelosco.com/shop/search-results.html?q=jasmine+rice": "div.product-card-container.product-card-container--with-out-ar", 
    #     "https://www.traderjoes.com/home/search?q=jasmine+rice&section=products&global=no": "article.SearchResultCard_searchResultCard__3V-_h",
    #     "https://www.target.com/s?searchTerm=jasmine+rice&sortBy=relevance&category=5xt1a": "div.styles__StyledDetailsWrapper-sc-1iglypx-1.bgKEdY"
    #     }
    
    # jo_url, jo_css = list(web_info.keys())[0], list(web_info.values())[0]
    # trader_url, trader_css = list(web_info.keys())[1], list(web_info.values())[1]
    
    # wd = webdriver.Chrome()
    # pages = main("https://www.target.com/s?searchTerm=jasmine+rice&sortBy=relevance&category=5xt1a", wd, "div.styles__StyledDetailsWrapper-sc-1iglypx-1.bgKEdY")
    # print(pages)
    # wd.quit()

    # main_path = "C:/Users/agarc/PersonalProjects/" 
    # with open(f"{main_path}test_data/three_stores.txt", mode='w', encoding='utf-8') as file:
    #     for page in pages:
    #         file.write(f"{page}\n")



    with open("C:/Users/agarc/PersonalProjects/test_data/three_stores.txt", mode="r", encoding='utf-8') as file:
        products_html = [line for line in file]

    for product in products_html:
        soup = BeautifulSoup(product, 'html.parser')
        name_price = soup.select("a.styles__StyledLink-sc-vpsldm-0.styles__StyledTitleLink-sc-h3r0um-1.fajhWk.hWNNbR.h-display-block.h-text-bold.h-text-bs,span[data-test='current-price']")
        print(name_price[0].text, name_price[1].text)
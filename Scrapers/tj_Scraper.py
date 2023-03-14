# import dependencies
import requests
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
import page_nav_fncs as nav
import html_parsing_fncs as handle

def get_product_href(bs4_object, class_val, tag):
    html = bs4_object.find_all(tag, class_=class_val)
    return [i.get('href') for i in html]

url = 'https://www.traderjoes.com/home/products/category/food-8'

print(requests.get(url)) # returns status code; 200 is sucessful request

driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)

driver.refresh()
time.sleep(3)

# bypasses an "accept cookies" pop-up
driver.find_element(By.XPATH, "//button[@class='Button_button__3Me73 Button_button_variant_secondary__RwIii']").click()
time.sleep(3)

# links = [i.find('a').get('href') for i in html_product_name]

# xpath to button tag that makes the next-page button
next_button = "//button[@class='Pagination_pagination__arrow__3TJf0 Pagination_pagination__arrow_side_right__9YUGr']"

pages = nav.all_pages_html(driver, 3, next_button) # list of each page's html

# htmltag that has product name
product_tag = 'h2'
product_class = 'ProductCard_card__title__text__uiWLe'

# html tag that has product price per quauntity
price_quant_tag = 'div'
price_quant_class = 'ProductPrice_productPrice__1Rq1r ProductCard_card__productPrice__1W4Le'

# making list of tags that contain product name and product price per quantity
prod_html = handle.find_tag(pages, product_tag, product_class)
price_quant_html = handle.find_tag(pages, price_quant_tag, price_quant_class)

# getting text in html tags
prod_txt = handle.get_tag_text(prod_html)
price_quant_txt = handle.get_tag_text(price_quant_html)

# returns tuple of lists; first has price, second has quantity
price, quant = handle.split_in_two(price_quant_txt, on='/') 

container = handle.make_contaniner(Product=prod_txt, Price=price, Amount=quant) # makes dict
print(container)
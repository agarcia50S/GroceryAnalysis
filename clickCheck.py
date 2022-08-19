from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
import time

def next_page(driver, button_xpath):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath ))
            )
    except TimeoutException:
        print('Last Page Reached')
        return False
    finally:
        driver.find_element(By.XPATH, button_xpath).click()
        time.sleep(2)
        return True

def get_page_count(driver, count_xpath):
    '''
    driver --> chrome webdriver instance
    count_xpath --> xpath for html tag that has page count text
    '''
    element = driver.find_element(By.XPATH, count_xpath)
    total_pages = int(element.text[-3:][:3])
    return total_pages
    
url = 'https://www.traderjoes.com/home/products/category/food-8'

driver = webdriver.Chrome()

# going to website
driver.get(url)
time.sleep(3)
driver.find_element(By.XPATH, "//button[@class='Button_button__3Me73 Button_button_variant_secondary__RwIii']").click()
time.sleep(3)

def all_pages_html(wd, total_pages, next_button_xpath):
    html = []
    for _ in range(total_pages):
        html.append(wd.page_source)
        next_page(wd, next_button_xpath)
    driver.quit()
    return html

page_max = get_page_count(driver, "//ul[@class='Pagination_pagination__list__1JUIg']")
next_button = "//button[@class='Pagination_pagination__arrow__3TJf0 Pagination_pagination__arrow_side_right__9YUGr']"
pages_html = all_pages_html(driver, page_max, next_button)
print(pages_html)
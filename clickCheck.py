from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time

url = 'https://www.traderjoes.com/home/products/category/food-8'

driver = webdriver.Chrome()

# going to website
driver.get(url)
time.sleep(3)
driver.find_element(By.XPATH, "//button[@class='Button_button__3Me73 Button_button_variant_secondary__RwIii']").click()

try:
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Uncured Dry Rubbed Sliced Bacon"))
    )
except TimeoutException:
    print('Did not work')

finally:
    driver.find_element(By.LINK_TEXT, 'Uncured Dry Rubbed Sliced Bacon').click()
    time.sleep(3)
    driver.quit()

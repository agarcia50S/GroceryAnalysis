from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from time import sleep

class TargetScrapper:
    def __init__(self, driver, url, last_pg_xpath, categories):
        self.driver = driver
        self.url = url
        self.last_pg_xpath = last_pg_xpath
        self.categories = categories

    def make_url(self, item, page_indx=0):
        # split url str on '&'
        url_parts = self.url.split('&')

        # getting parts of url-- 'SearchTerm=' and 'nao=' 
        term_indx, num_indx = url_parts[0].find('='), url_parts[3].find('=') # assign indx of char '='
        url_part_0, url_part_3 = url_parts[0][:term_indx + 1], url_parts[3][:num_indx + 1] # assign url parts

        # reconstructing url with given item and page index
        return f'{url_part_0}{item}&{url_parts[1]}&{url_parts[2]}&{url_part_3}{page_indx}&{url_parts[4]}'

    def scroll_to_end(self, wait=2):
        screen_height = self.driver.execute_script("return window.screen.height;") # get page screen height
        scroll_height = self.driver.execute_script("return document.body.scrollHeight;") # get curr scroll height
        i = 1
        while screen_height * i < scroll_height:
            # scroll one screen height each time
            self.driver.execute_script(f"window.scrollTo(0, {screen_height}*{i});")  
            i += 1
            sleep(wait)
            # update scroll height, as the scroll height can change after we scrolled the page
            scroll_height = self.driver.execute_script("return document.body.scrollHeight;")  
                
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
    
    def load_page(self, item, wait=4.5, cur_page=0):
        '''
        Constructs page's url and then searches for url. Once on page
        we wait for x seconds and then scroll to bottom, 
        as page has scroll-dependent elements.
        '''
        url = self.make_url(item, cur_page) # build url with given item and default page num, 0
        self.driver.get(url) # navigates to url; returns none
        sleep(wait)
        self.scroll_to_end()

    def get_all_html(self):
        result = []
        for item in self.categories:
            self.load_page(item)
            result.append(self.driver.page_source)
            last_pg_num = self.get_page_count() - 1 # finds max val in pagination
            page_indx = 24
            end_pg = last_pg_num * page_indx

            while page_indx <= end_pg:
                self.load_page(item, cur_page=page_indx)
                result.append(self.driver.page_source)
                page_indx += 24

                # FOR TESTING
                # if page_indx > 24 * 2: 
                #     break

        self.driver.quit()
        return result

    @staticmethod
    def make_xpath(tag, attr, val):
        '''
        Makes a relative xpath for an html element. xpath 
        form is //tagname[@attribute='value']
        '''
        return f"//{tag}[@{attr}='{val}']"
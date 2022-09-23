from bs4 import BeautifulSoup
from target_scrapper import TargetScrapper
from selenium import webdriver
class Parser():
    def __init__(self, pages):
        self.pages = pages
        # self.tag = tag
        # self.tag_class = tag_class

    def find_all_elements(self, tag, tag_class):
        for page in self.pages:
            elements = []
            soup = BeautifulSoup(page, 'html.parser') 
            elements += soup.find_all(tag, class_=tag_class)
        return elements

    def extract_text(self, tag, tag_class):
        elements = self.find_all_elements(tag, tag_class)
        return [i.text for i in elements]
         
    @staticmethod
    def split_text(text, delim):
        split_loc = text.find(delim)
        return (text[:split_loc], text[split_loc:])

if __name__ == '__main__':
    grocery_list = ['meat', 'produce']

    wd = webdriver.Chrome()

    # pagination html info
    tag = 'span'
    attr = 'class'
    val = 'Pagination__StyledSpan-sc-sq3l8r-5 gyBTAO'

    pg_num_xpath = TargetScrapper.make_xpath(tag, attr, val)
    url = 'https://www.target.com/s?searchTerm=meat&sortBy=relevance&category=5xt1a&Nao=0&moveTo=product-list-grid'

    bot = TargetScrapper(wd, url, pg_num_xpath, grocery_list)
    pages = bot.find_products()

    
    p = Parser(pages)

    prod_class = 'Link__StyledLink-sc-frmop1-0 styles__StyledTitleLink-sc-h3r0um-1 iMNANe dcAXAu h-display-block h-text-bold h-text-bs'
    prod_tag = 'a'
    prod = p.extract_text(prod_tag, prod_class)

    print(prod[0])

    # template = {'Product':[], 
    #             'Price':[],
    #             'Quantity':[]
    # }
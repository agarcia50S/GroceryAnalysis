from bs4 import BeautifulSoup
from target_scrapper import TargetScrapper
from selenium import webdriver
class Parser():
    def __init__(self, 
                 pages, 
                 prod_qnt_tag='', 
                 prod_qnt_attr='',
                 prod_qnt_val='',
                 price_tag='', 
                 price_attr='',
                 price_val=''):

        self.pages = pages
        self.prod_qnt_tag = prod_qnt_tag
        self.prod_qnt_attr = prod_qnt_attr
        self.prod_qnt_val = prod_qnt_val
        self.price_tag = price_tag
        self.price_attr = price_attr
        self.price_val = price_val

    def find_all_elements(self, tag, attr, val):
        elements = []
        for page in self.pages:
            soup = BeautifulSoup(page, 'html.parser') 
            elements += soup.find_all(tag, attrs={attr:val})
        return elements

    def extract_text(self, tag, attr, val):
        elements = self.find_all_elements(tag, attr,  val)
        return [i.text for i in elements]

    # fnc that can get prod and quant info; return 2d array
    def find_prod_quant(self):

        # need to account for names like 
        # USDA Choice Angus Petite Sirloin Steak - 0.68-1.13 lbs - price per lb - Good & Gather™
        p = []
        q = []
        texts = self.extract_text(self.prod_qnt_tag, 
                                    self.prod_qnt_attr, 
                                    self.prod_qnt_val)
        if '$' in texts[0]:
            raise AttributeError('Incorrect Atttibute Assignment')
        else:
            for i in texts:
                split_name = i.split(' - ')
                if len(split_name) > 2:
                    if len(split_name[1]) <= 6: # ** make sure there is always a 3rd item **
                        split_name.pop(2)
                    else:
                        split_name.pop(1)
                p.append(split_name[0])
                q.append(split_name[1])
        return p, q
          
    # fnc that can get price info; return 1d array
    def find_prices(self):
        texts = self.extract_text(self.price_tag, 
                                       self.price_attr, 
                                       self.price_val)
        return [i.split('/')[0].strip('(') if '/' in i else i for i in texts]
        
    # fnc that can add return populated dict
    def make_dict(self):
        return {'Product':self.find_prod_quant()[0], 
                'Price':self.find_prod_quant()[1],
                'Quantity':self.find_prices()
        }
         
    @staticmethod
    def split_text(text, delim):
        split_loc = text.find(delim)
        return (text[:split_loc], text[split_loc:])
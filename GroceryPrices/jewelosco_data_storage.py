import csv
from bs4 import BeautifulSoup

class ExtractAndStore:
    def __init__(self, *css_selectors, path_to_html=None, all_html=None):
        self.all_html = all_html
        self.path_to_html = path_to_html
        self.css_selectors = css_selectors
    
    def file_to_arr(self):
        with open(self.path_to_html, mode='r') as in_file:
            contents = in_file.readlines()
        return contents

    def get_data_from_html(self, html):
        '''
        Takes html of a product card and returns an arr with the product's
        price, name-quantity, and price-per-quantity.
        '''
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.select(','.join(self.css_selectors))
        return [datum.text for datum in data]

    def format_as_csv(self, header, out_path):
        with open(out_path, mode='w', newline='', encoding='utf-8') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(self.format_as_table(header))

    def format_as_table(self, header):
        if self.all_html is not None: elements = self.all_html
        elif self.path_to_html is not None: elements = self.file_to_arr() 
        prod_category, container = '', [header] # ['price','name_qnt','price_per_qnt', 'category']
        for element in elements:
            # if category name place it in holder and don't make row. 
            if '<' not in element: prod_category = element.strip()
            # if not category name, make row and append held category name
            else:
                row = self.get_data_from_html(element)
                row.append(prod_category)
                container.append(row)
        return container

# check if string is measure
def is_measure(value):
    only_unit = ''.join([char.lower() for char in value if char.isalpha()])
    units = ['lb', 'oz', 'ml', 'g', 'ct', 'pk', 
             'qt', 'pt', 'count', 'fz', 'liter',
             'gallon', 'each', 'ea', 'floz']
    if only_unit in units: return only_unit in units
    for unit in units:
        if unit in only_unit and len(unit) == len(only_unit): return True
    return False

# seperate price-quantity string into price and quantity
def seperate_name_qnt(name_qnt):
    temp = name_qnt.split('-')
    if len(temp) == 2: return temp[0], temp[1]
    name, qnt = f'{temp[0]} ', ''
    for val in temp[1:]:
        cur = val.strip() # WRONG: should be for any non-alpha leading/trailing chars
        if is_measure(cur): qnt += cur
        elif cur.isnumeric(): qnt += f'{cur}-'
        else: name += cur
    if is_measure(qnt): return name, qnt
    else: return name, ''

# Price Selector: pg142200086price > span:nth-child(1)
# (Price class: product-price__saleprice product-price__discounted-price)
# Name-Quantity Selector: #pg960100621
# (Name-Quantity class: product-title__name)
# Price/Quant data-qa: prd-itm-pprc-qty

if __name__ == '__main__':
    in_path = 'C:/Users/agarc/PersonalProjects/extracted_data/JO_prod_card_html_data.txt'
    out_path = 'C:/Users/agarc/PersonalProjects/extracted_data/JO_raw_data.csv'
    price_sel = '.product-price__saleprice'
    name_qnt_sel = '.product-title__name'
    price_qnt_sel = 'div[data-qa="prd-itm-pprc-qty"]'

    jo_data = ExtractAndStore(price_sel, name_qnt_sel, price_qnt_sel, 
                              path_to_html=in_path)

    header = ['price','name_qnt','price_per_qnt', 'category']
    jo_data.format_as_csv(header, out_path=out_path)
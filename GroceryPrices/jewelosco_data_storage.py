import csv
from bs4 import BeautifulSoup

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
        cur = val.strip() # WRONG: needs to any non-alpha leading/trailing chars
        if is_measure(cur): qnt += cur
        elif cur.isnumeric(): qnt += f'{cur}-'
        else: name += cur
    return name, qnt
# extract product name and price-quantity data from html
# input html as string type
# output data structure with category, name, price-quantity, price/quantity
def get_data_from_html(html, price_slctr, name_qnt_slctr, price_qnt_slctr):
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.select(f'{price_slctr}, {name_qnt_slctr}, {price_qnt_slctr}')
    return [datum.text for datum in data]

# iterate over html-elements file and handle category assignment; return 2d array
def make_data_container(in_path, out_path, price_slctr, name_qnt_slctr, price_qnt_slctr):
    with open(in_path, mode='r') as in_file, open(out_path, mode='w', newline='', encoding='utf-8') as out_file:
        elements = in_file.readlines()
        writer = csv.writer(out_file)
        prod_category, container = '', [['price','name_qnt','price_per_qnt', 'category']]
        for element in elements:
            if '<' not in element: prod_category = element.strip()
            else:
                row = get_data_from_html(element, price_slctr, name_qnt_slctr, price_qnt_slctr)
                row.append(prod_category)
                container.append(row)
        writer.writerows(container)
# Price Selector: pg142200086price > span:nth-child(1)
# (Price class: product-price__saleprice product-price__discounted-price)
# Name-Quantity Selector: #pg960100621
# (Name-Quantity class: product-title__name)
# Price/Quant data-qa: prd-itm-pprc-qty

if __name__ == '__main__':
    in_path = 'C:/Users/agarc/PersonalProjects/extracted_data/JO_prod_card_html_data.txt'
    out_path = 'C:/Users/agarc/PersonalProjects/extracted_data/raw_product_data.csv'
    price_sel = '.product-price__saleprice'
    name_qnt_sel = '.product-title__name'
    price_qnt_sel = 'div[data-qa="prd-itm-pprc-qty"]'
    # make_data_container(in_path, out_path, price_sel, name_qnt_sel, price_qnt_sel)

    prod_name = 'StarKist Tuna Chunk Light in Water - 6.4 Oz'
    print(seperate_name_qnt(prod_name))
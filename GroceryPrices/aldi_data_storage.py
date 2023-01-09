import csv
from bs4 import BeautifulSoup

# check if string is measure
def is_measure(value):
    for unit in ['lb', 'oz', 'ml', 'g', 'ct', 'pk', 'qt', 'pt']:
        if unit in value.lower(): return True
        return False

# seperate price-quantity string into price and quantity
def seperate_name_qnt(name_qnt):
    temp = name_qnt.split('-')
    name, qnt = '', ''
    for val in temp:
        cur = val.strip()
        if is_measure(cur) == True or cur.isnumeric() == True: 
            qnt += cur
        else: name += cur

# extract product name and price-quantity data from html
# input html as string type
# output data structure with category, name, price-quantity, price/quantity
def get_data_from_html(html, price_slctr, name_qnt_slctr, price_qnt_slctr):
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.select(f'{price_slctr}, {name_qnt_slctr}, {price_qnt_slctr}')
    return [datum.text for datum in data]

# iterate over html-elements file and handle category assignment; return 2d array
def make_data_container(in_path, out_path, price_slctr, name_qnt_slctr, price_qnt_slctr):
    with open(in_path, mode='r') as in_file, open(out_path, mode='w', newline='') as out_file:
        elements = in_file.readlines()
        writer = csv.writer(out_file)
        cat, row = '', [['price','name_qnt','price_per_qnt', 'category']]
        for element in elements:
            if '<' not in element: cat = element.strip()
            else:
                data = get_data_from_html(element, price_slctr, name_qnt_slctr, price_qnt_slctr)
                data.append(cat)
                row.append(data)
        writer.writerows(row)

# Price Selector: pg142200086price > span:nth-child(1)
# (Price class: product-price__saleprice product-price__discounted-price)
# Name-Quantity Selector: #pg960100621
# (Name-Quantity class: product-title__name)
# Price/Quant data-qa: prd-itm-pprc-qty
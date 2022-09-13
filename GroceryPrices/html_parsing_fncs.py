from bs4 import BeautifulSoup

def find_tag(html_list, tag, tag_class):
    '''
    Iterates over list of page's html and finds 
    all the html tags with a given class 
    attribute, using .find_all(). The method
    returns a list of tags for each page; the
    lists are merged into list. 
    Returns the combined list.

    html_list --> list of html of individual 
                  pages
    tag --> html tag
    tag_class --> particular class attribute of 
                  tag

    '''
    values = []
    for page in html_list: 
        soup = BeautifulSoup(page, 'html.parser')
        values += soup.find_all(tag, class_=tag_class) # merging lists
    return values

def get_tag_text(tag_list):
    return [tag.text for tag in tag_list]

def make_contaniner(**group_name):
    return group_name
    
def split_in_two(str_list, on=' '):
    '''
    takes a list of strings and splits them
    into two parts, using .split() which
    returns a list per string containing 
    the two parts. Each list is split in 
    half, each half being merged into
    one list. 
    Returns both lists in a tuple.

    str_list --> list of strings
    on --> symbol to split str on; default is 
           a space
    '''
    one = []
    two = []
    for tag in str_list:
        one += tag.split(on)[:1] # first half of list
        two += tag.split(on)[1:] # second half of list
    return one, two

# quant = rate.text.split('/')[1]

if __name__ == '__main__':
    
# ----------------------- Testing Functions ----------------------
    product_tag = 'h2'
    product_class = 'ProductCard_card__title__text__uiWLe'
    price_quant_tag = 'div'
    price_quant_class = 'ProductPrice_productPrice__1Rq1r ProductCard_card__productPrice__1W4Le'

    f = open("GroceryPrices/html_for_testing.txt", "r")
    html = f.read()
    prod_html = find_tag([html], product_tag, product_class)
    
    price_quant_html = find_tag([html], price_quant_tag, price_quant_class)

    # getting text in html tags
    prod_txt = get_tag_text(prod_html)
    price_quant_txt = get_tag_text(price_quant_html)

    # returns tuple of lists; first has price, second has quantity
    price, quant = split_in_two(price_quant_txt, on='/') 
    
    container = make_contaniner(Product=prod_txt, Price=price, Amount=quant) # makes dict
    print(container)

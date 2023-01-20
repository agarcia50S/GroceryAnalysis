# %%
import pandas as pd
from jewelosco_data_storage import is_measure, seperate_name_qnt, ExtractAndStore

def seperation_test(arr):
    for name, qnt in arr:
        if len(name) < 1 or len(qnt) < 1: return 'TEST FAILED'
        
    return 'TEST PASSED'

def is_pair(pair):
    if len(pair[0]) > 0 and len(pair[1]) > 0: return True
    return False

# attempts to split prod name
def special_split(name_qnt, on='–'):
    if on in name_qnt: return name_qnt.split(on)
    for i in range(len(name_qnt)):
        if name_qnt[i].isnumeric() and is_measure(name_qnt[i:]):
            # return name, quantity 
            return name_qnt[:i], name_qnt[i:]
    return name_qnt

def split_price_per_qnt(price_qnt, on='/'):
    price, qnt = price_qnt.split(on)
    return price.strip('('), qnt.strip(')')

def clean_price(money, keep=[]):
    cleaned = ''
    if len(keep) < 1:
        for char in money:
            if char.isnumeric(): cleaned += char
        return cleaned

    for char in money:
        if char.isnumeric() or char in keep: cleaned += char
    return cleaned

#url_split = 'https://www.jewelosco.com/shop/aisles/beverages/soft-drinks.3441.html'.split()
#html = '<div class="product-card-container product-card-container--with-out-ar"><div class="product-item-142200086"><!----><div class="product-card-container__image-container mt-3"><a tabindex="-1" id="pg142200086Img" data-bpn="142200086" href="/shop/product-details.142200086.html"><picture class="product-image-opaque-full"><source media="(max-width: 575px)" data-srcset="//images.albertsons-media.com/is/image/ABS/142200086?$ecom-product-card-mobile-jpg$&amp;defaultImage=Not_Available" srcset="//images.albertsons-media.com/is/image/ABS/142200086?$ecom-product-card-mobile-jpg$&amp;defaultImage=Not_Available"><source media="(max-width: 768px)" data-srcset="//images.albertsons-media.com/is/image/ABS/142200086?$ecom-product-card-tablet-jpg$&amp;defaultImage=Not_Available" srcset="//images.albertsons-media.com/is/image/ABS/142200086?$ecom-product-card-tablet-jpg$&amp;defaultImage=Not_Available"><img class="ab-lazy product-card-container__product-image loaded" data-qa="prd-itm-img" data-src="//images.albertsons-media.com/is/image/ABS/142200086?$ecom-product-card-desktop-jpg$&amp;defaultImage=Not_Available" alt="Outshine Strawberry Frozen Fruit Bars - 6 Count" src="//images.albertsons-media.com/is/image/ABS/142200086?$ecom-product-card-desktop-jpg$&amp;defaultImage=Not_Available" data-was-processed="true"></picture></a><!----></div><!----><div class="product-card-container__approx"><!----></div><!----><!----><div class="product-card-container__details mt-3"><div class="product-price"><span class="product-price__saleprice product-price__discounted-price" data-qa="prd-itm-prc" id="pg142200086price"><span class="sr-only">Your Price</span> $4.49 <!----><!----><span class="sr-only" data-qa="each-or-lb">each</span></span><!----><del class="product-price__baseprice" data-qa="prd-itm-prc-del"><span class="sr-only">Original Price</span> $5.79 </del></div></div><div class="product-title"><div class="product-title__text"><a class="product-title__name" data-qa="prd-itm-pttl" id="pg142200086" data-bpn="142200086" href="/shop/product-details.142200086.html">Outshine Strawberry Frozen Fruit Bars - 6 Count</a><!----></div><!----><div class="product-title__details"><!----><div class="product-title__qty" data-qa="prd-itm-pprc-qty" id="pg142200086unitPer">($0.31 / Fl.oz)</div><!----></div><!----><!----><!----><!----><!----><!----><!----><product-coupon-v3><!----><!----></product-coupon-v3></div><!----><!----><!----><quantity-stepper-v3 id="pg142200086-qty"><!----><div class="quantity-stepper-v3"><div class="quantity-stepper-container"><div class="product-btn product-btn--without-ar full-loading"><!----><div class="btn product-btn__add product-btn--signin" data-qa="addbutton" role="button" tabindex="0" id="addButton_142200086" aria-describedby="pg142200086" data-qty-id="pc142200086Inpt" aria-label="Sign in to add 1 unit of Outshine Strawberry Frozen Fruit Bars - 6 Count"> Sign in to add </div><!----><!----></div></div></div><!----><!----></quantity-stepper-v3><!----><!----><!----><!----><!----><!----></div></div>'
path = 'C:/Users/agarc/PersonalProjects/extracted_data'
start = pd.read_csv('C:/Users/agarc/PersonalProjects/extracted_data/JO_raw_data.csv',  encoding="windows-1252")
starting_shape = start.shape
start.head()

#%%
# fix product names that contain partial name with '...'

# make df that only has corrected partial names

# run ExtractAndStore using css select for the div that has full name version of partial names
price_sel, price_per_qnt  = '.product-price__saleprice', 'div[data-qa="prd-itm-pprc-qty"]'
name_qnt = '.product-item-title-tooltip__inner'
builder = ExtractAndStore(price_sel, price_per_qnt, name_qnt, path_to_html=path + '/JO_prod_card_html_data.txt')

# table only contains complete rows for corrected partial names
corrected_names = builder.format_as_table(start.columns.tolist())

# make into df
corrected_names_df = pd.DataFrame(corrected_names[1:], columns=corrected_names[0])

# drop rows with nan as they are not corrected partial names
only_corrected_names_df = corrected_names_df.dropna()
only_corrected_names_df.head()
# %%
name_qnt = start['name_qnt'].apply(seperate_name_qnt)
start['name_qnt_pairs'] = name_qnt
start['is_pair'] = start['name_qnt_pairs'].apply(is_pair)

# %%
# df containing all name_qnt's that seperate_name_qnt
failed_seps = start[start['is_pair'] == False]
failed_seps['name_qnt_pairs'] = failed_seps['name_qnt'].apply(special_split)
# checks if val is str type as only failed-splits are str's
failed_seps['is_pair'] = failed_seps['name_qnt_pairs'].apply(lambda x: False if type(x) == str else True)
failed_seps.head()

#%%
fixed_seps_A = failed_seps[failed_seps['is_pair'] == True]
fixed_name_qnts = fixed_seps_A.loc[:, ['name_qnt_pairs']]
index_vals = list(fixed_name_qnts.index)
all_name_qnts = start.loc[:, ['name_qnt_pairs']]
temp_A = all_name_qnts.drop(index_vals)
all_name_qnts = pd.concat([temp_A, fixed_name_qnts]).sort_index()
start['name_qnt_pairs'] = all_name_qnts['name_qnt_pairs']
start['qnt'] = start['name_qnt_pairs'].apply(lambda x: x[1])
start.head()
#%%

#%%
# remaining split-fail name_qnt's
remaining_failed_seps = failed_seps[failed_seps['is_pair'] == False]
remaining_failed_seps['price'] = remaining_failed_seps['price_per_qnt'].apply(lambda x: split_price_per_qnt(x)[0])
# assign to price_qnt_pairs as same header names needed for later concat
remaining_failed_seps['qnt'] = remaining_failed_seps['price_per_qnt'].apply(lambda x: split_price_per_qnt(x)[1])
remaining_failed_seps.head()

#%%
remaining_idx_vals = list(remaining_failed_seps.index)
temp_B = start.drop(remaining_idx_vals)
start = pd.concat([remaining_failed_seps, temp_B]).sort_index()
start.shape

#%%
# clean up / wrangle dataframe
start['name'] = start['name_qnt_pairs'].apply(lambda x: x[0])
cleaned = start.drop(columns=['name_qnt_pairs', 'is_pair'])
cleaned['price'] = cleaned['price'].apply(lambda x: clean_price(x, ['.']))
cleaned.head()
# %%
start.to_csv(path + 'JO_cleaned_data.csv')

# vertically concat both dfs
        
# %%

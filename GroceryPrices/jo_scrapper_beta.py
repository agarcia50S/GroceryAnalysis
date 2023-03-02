import requests
import json
# make a url that can locate the results page of a given product
# full url = base url + search parameter (i.e. item from grocery list)

# https://www.jewelosco.com/abs/pub/xapi/pgmsearch/v1/search/products?request-id=3981677549256748407&url=https://www.jewelosco.com&pageurl=https://www.jewelosco.com&pagename=search&rows=30&start=0&search-type=keyword&storeid=3441&featured=true&search-uid=&q=riceselect rice&sort=&featuredsessionid=&screenwidth=1533&dvid=web-4.1search&channel=instore&banner=jewelosco
def make_request_url(search_word):
        prod_data_url = f"https://www.jewelosco.com/abs/pub/xapi/pgmsearch/v1/search/products?request-id=3981677549256748407&url=https://www.jewelosco.com&pageurl=https://www.jewelosco.com&pagename=search&rows=30&start=0&search-type=keyword&storeid=3441&featured=true&search-uid=&q={search_word}&sort=&featuredsessionid=&screenwidth=1533&dvid=web-4.1search&channel=instore&banner=jewelosco"
        return prod_data_url

def format_cookies(cookie_pairs):
     '''
     Takes a "list" of name-value pairs e.g. "cook1=value1; "cook2=val2"
     '''
     pairs = [pair.split('=') for pair in cookie_pairs.split('; ')]
     formatted_pairs = {cookie_val[0]:cookie_val[1] for cookie_val in pairs}
     return formatted_pairs

# query url and get json file with product data
def request_from_api(url, url_params, req_headers, req_cookies):
    response = requests.get(url, params=url_params, headers=req_headers, cookies=req_cookies)
    return response

if __name__ == '__main__':
    url = make_request_url('riceselect rice')
    header, value = "Ocp-Apim-Subscription-Key", "5e790236c84e46338f4290aa1050cdd4"
    print(request_from_api(url, header, value).json())
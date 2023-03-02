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
    # url that API is located at
    api_url = "https://www.jewelosco.com/abs/pub/xapi/pgmsearch/v1/search/products?"

    # url parameters
    url_params = {
            "request-id": "1771677643767994529",
            "url": "https://www.jewelosco.com",
            "pageurl": "https://www.jewelosco.com",
            "pagename": "search",
            "rows": "30",
            "start": "0",
            "search-type": "keyword",
            "storeid": "1118",
            "featured": "true",
            "search-uid": "",
            "q": "rice",
            "sort": "",
            "featuredsessionid": "",
            "screenwidth": "1533",
            "dvid": "web-4.1search",
            "channel": "instore",
            "banner": "jewelosco"
    }

    # API sub key
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "www.jewelosco.com",
        "Ocp-Apim-Subscription-Key": "5e790236c84e46338f4290aa1050cdd4",
        "Referer": "https://www.jewelosco.com/shop/search-results.html?q=rice",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"
    }

    combined_cookies = "visid_incap_1990338=s+w9h0GrTSqb/iWdgj5yGT7p/2MAAAAAQUIPAAAAAAD+pkwygiCfx/ikABjRUg/L; nlbi_1990338=mHC1ApVnlTLFJURPzoaznQAAAACG3swCSzQedoLPtuqqPhlT; incap_ses_8080_1990338=FeLoM/tDE2aUu2sos+0hcD7p/2MAAAAAyClJy0AvAh6rRWqmCVVCcw==; ECommBanner=jewelosco; abs_gsession=%7B%22info%22%3A%7B%22COMMON%22%3A%7B%22Selection%22%3A%22user%22%2C%22preference%22%3A%22J4U%22%2C%22userType%22%3A%22G%22%2C%22zipcode%22%3A%2252732%22%2C%22banner%22%3A%22jewelosco%22%7D%2C%22J4U%22%3A%7B%22zipcode%22%3A%2252732%22%2C%22storeId%22%3A%221118%22%7D%2C%22SHOP%22%3A%7B%22zipcode%22%3A%2252732%22%2C%22storeId%22%3A%221118%22%7D%7D%7D; SWY_SHARED_SESSION_INFO=%7B%22info%22%3A%7B%22COMMON%22%3A%7B%22userType%22%3A%22G%22%2C%22zipcode%22%3A%2252732%22%2C%22banner%22%3A%22jewelosco%22%2C%22preference%22%3A%22J4U%22%2C%22Selection%22%3A%22user%22%2C%22userData%22%3A%7B%7D%7D%2C%22J4U%22%3A%7B%22storeId%22%3A%221118%22%2C%22zipcode%22%3A%2252732%22%2C%22userData%22%3A%7B%7D%7D%2C%22SHOP%22%3A%7B%22storeId%22%3A%221118%22%2C%22zipcode%22%3A%2252732%22%2C%22userData%22%3A%7B%7D%7D%7D%7D; abs_previouslogin=%7B%22info%22%3A%7B%22COMMON%22%3A%7B%22Selection%22%3A%22user%22%2C%22preference%22%3A%22J4U%22%2C%22userType%22%3A%22G%22%2C%22zipcode%22%3A%2252732%22%2C%22banner%22%3A%22jewelosco%22%7D%2C%22J4U%22%3A%7B%22zipcode%22%3A%2252732%22%2C%22storeId%22%3A%221118%22%7D%2C%22SHOP%22%3A%7B%22zipcode%22%3A%2252732%22%2C%22storeId%22%3A%221118%22%7D%7D%7D; SWY_SYND_USER_INFO=%7B%22storeAddress%22%3A%22%22%2C%22storeZip%22%3A%2252732%22%2C%22storeId%22%3A%221118%22%2C%22preference%22%3A%22J4U%22%7D; ECommSignInCount=0; SAFEWAY_MODAL_LINK=; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Mar+01+2023+18%3A10%3A25+GMT-0600+(Central+Standard+Time)&version=202212.1.0&isIABGlobal=false&hosts=&consentId=2481ceef-8878-4f3b-924b-3b28079d9b13&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0004%3A0%2CC0003%3A1&AwaitingReconsent=false; nlbi_1990338_2147483392=jYckLK1heGBAHrRyzoaznQAAAACZvsW6rrz3C1oXWBs6UFc8; reese84=3:Gl8qjGMtFKfV15EgMleAnA==:OIn+iQ/52nnNf5lyREodaDDwUAjg8dDGS98wIlrt5otpbU+Cf8LVvyWEszAKcXR472IFIvx0GqApqQXL+AwRenGrptfNzKJtsu+zlyayIVp5q9BJEyz9T9tIFT2YmnQ+D1rZkBlw2lcnRZqxvVX5dSG6pFJH9nebThXLpHGzKF+j2O1jRKRTanLc72sHU5aqkDgp6aKgzvMI3IQTg9JPnSYW1I0779+gNrb/WfVOID4YT3FLG3OBiMxXsnGGrGQD+3QUsGWzJGXqKkLgErxusDcDI+J82YxLg8Lg7u+qbLFLdUPB4dUsPJJLlHJx8kMBuoRh/47QtMYdykoXYmcZ4PYYLnop7lpDFahVOwcqGmwGCCBjkAnxGuVejNESYc4Yiu5iHFluuEHSDyLxXUmlQWRfDl6axKS+0m6Zm7IqPmvetfC4BsZKbDRk5p/jbFDCIYD/iHbRi8OE/mkzTD03r+un1iC5GFK4BhIQrtBDybXmZYJU1VBwXl+raL8wR0Db3d3I/Mbh4/CK1uT/7CJDRIDznlCZC0/C3gFwXQpfLiA=:XtGGSfw6IB+W6dYIh0iO+xPVdddBfiRA1zwKMhu0OmE=; mbox=session#2686aefa9dea422db9f92c9b39a01830#1677717696; at_check=true; ADRUM_BT=R:57|i:5124367|g:a106a4d3-bbb8-4619-8262-9d3f98852991652436|e:104|n:safeway-loyalty_d99a98d0-07cc-4871-98b7-0beac77d0580"
    
    all_cookies = format_cookies(combined_cookies)

    # combine api_url and url_params and make GET request with headers
    product_data = request_from_api(api_url, url_params, headers, all_cookies).json()

    # pretty print json file
    print(json.dumps(product_data, indent=3))
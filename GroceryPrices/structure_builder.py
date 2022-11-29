from bs4 import BeautifulSoup
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
        elements = self.find_all_elements(tag, attr, val)
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
        self.products = texts
    
        for title in texts:
            split_txt = title.split(' - ')
            split_txt_length = len(split_txt)
            if split_txt_length > 2:
                p.append(split_txt.pop(0))
                for txt in split_txt:
                    strp_txt = txt.strip()
                    if (is_measure(strp_txt) == True) and '-' not in strp_txt and '&' not in strp_txt:
                        if 'price per' in strp_txt:
                            q.append(strp_txt)
                        elif strp_txt[0].isnumeric():
                            q.append(strp_txt)      
            elif split_txt_length == 2:
                p.append(split_txt[0])
                q.append(split_txt[1])
            else:
                print(split_txt)
                prod, quant = split_on_int(title)    
                p.append(prod)
                q.append(quant)
        return p, q
          
    # fnc that can get price info; return 1d array
    def find_prices(self):
        texts = self.extract_text(self.price_tag, 
                                       self.price_attr, 
                                       self.price_val)
        r = []
        
        # return [i.split('(')[1].split('/')[0] if '/' in i else i for i in texts]
        for i in texts:
            if '/' in i:
                if '(' in i:
                    try:
                        r.append(i.split('(')[1].split('/')[0])

                    except Exception as ex:
                        print(f"{ex}\nOccured with: {i}\nLOOP STOPPED ON: {texts}")
                        break
                else:
                    r.append(i.split('/')[0])
            else:
                r.append(i)
        return r
    # fnc that can add return populated dict
    def make_dict(self):
        return {'Product':self.find_prod_quant()[0], 
                'Quantity':self.find_prod_quant()[1],
                'Price':self.find_prices()
        }
         
    @staticmethod
    def split_text(text, delim):
        split_loc = text.find(delim)
        return (text[:split_loc], text[split_loc:])
    
    @staticmethod
    def split_on_int(title):
        '''
        Takes char, splits it on first numeric char
        returns list of the two parts
        '''
        for i, char in enumerate(title):
            if char.isnumeric():
                if is_measure(title[i:]):
                # return name and quantity 
                    return title[:i], title[i:]
        else: return title, None

    @staticmethod
    def is_measure(value):
        for unit in ['lb', 'oz', 'ml', 'g', 'ct']:
            if unit in value.lower(): return True
        return False

from bs4 import BeautifulSoup
class Storage():
    def __init__(self, template, pages):
        self.template = template
        self.pages = pages

    def extract_text(self, tag, tag_class):
        soup = BeautifulSoup(self.pages, 'html.parser') 
        html_elmnts = soup.find_all(tag, class_=tag_class)
        return [i.text for i in html_elmnts]
         
    @staticmethod
    def text_parser(text, delim):
        split_loc = text.find(delim)
        return text[:split_loc]

    






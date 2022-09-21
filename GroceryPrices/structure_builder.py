from bs4 import BeautifulSoup
class Storage():
    def __init__(self, template, pages):
        self.template = template
        self.pages = pages
    def extract_text(self, page_html, tag, tag_class):
        soup = BeautifulSoup(page_html, 'html.parser') 
        html_elmnts = soup.find_all(tag, class_=tag_class)
        return [i.text for i in html_elmnts]



#! /usr/bin/env python
#coding=utf-8
import urllib, json, logging
from HTMLParser import HTMLParser

#page num parser used for house-list and history-list page total num parser
class PageNumParser(HTMLParser):
    def __init__(self, url):
        HTMLParser.__init__(self)
        self.__pageTotal = None
        
        logging.debug("PageNumParser parse page "+url)
        
        try:
            page = urllib.urlopen(url)
            page_data = page.read()
            self.feed(page_data)  
        except:
            logging.error(url + "paraser error")
            
    def handle_starttag(self, tag, attrs):
        if tag == "div" and len(attrs) == 4 and attrs[0][1] == "page-box house-lst-page-box":
            page_dic = json.loads(str(attrs[3][1]))
            logging.debug("PageNumParser page_dic "+str(attrs[3][1]))
            self.__pageTotal = page_dic["totalPage"]
            #self.__pageCurrent = page_dic["curPage"]

    #detect the legality of page_num
    def pageNumCheck(self, page_num):
        if page_num == 0 or page_num > 99:
            return False
        else:
            return True
    
    def resPageNum(self):
        #None or page_num
        return self.__pageTotal

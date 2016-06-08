#! /usr/bin/env python
#coding=utf-8
import urllib, json, logging
from HTMLParser import HTMLParser
from page_num_parser import PageNumParser

#get house list
class HouseList(object):
    def __init__(self, comm_code):
        page_url = "http://bj.lianjia.com/ershoufang/pg1c" + str(comm_code)
        
        self.__comm_code = comm_code

        #there is already try-except structure in PageNumParser 
        tp_page = PageNumParser(page_url)
        tp_page.close()
        page_num = tp_page.resPageNum()

        
        if page_num==None or tp_page.pageNumCheck(page_num) == False:
            self.__page_list = ""
            logging.error("page_num invalid")  
        else:
            self.__page_list = []
            logging.debug("Parse list-page, get page_num : "+str(page_num))
  
            for i in range(1, int(page_num)+1):
                tp_list = HouseListParser(self.pageUrl(i))
                tp_list.close()
                self.__page_list += tp_list.resHouseList()

    #generate the list-page url
    #valid url:http://bj.lianjia.com/ershoufang/pgXc********    
    def pageUrl(self, page_num):
        url_base = "http://bj.lianjia.com/ershoufang/pg"
        url_end  = "c" + str(self.__comm_code)
        return url_base + str(page_num) + url_end

    def getHouseList(self):
        return self.__page_list


#get house list
class HouseListParser(HTMLParser):
    def __init__(self, url):
        HTMLParser.__init__(self)
        self.__houseList = []
        
        logging.debug("Parse list-page in " + url)

        try:
            page = urllib.urlopen(url)
            page_data = page.read()
            self.feed(page_data)
        except:
            self.__houseList = []
            logging.error("HouseListParser" + url + "parase error")
        
        logging.debug("Parse list-page end")    
    
    def handle_starttag(self, tag, attrs):
        if tag == "li" and len(attrs) == 2 and attrs[0][0]=="data-index":
            self.__houseList.append(attrs[1][1])

    def resHouseList(self):
        return self.__houseList

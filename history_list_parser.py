#! /usr/bin/env python
#coding=utf-8
import re, urllib, json, logging
from HTMLParser import HTMLParser
from page_num_parser import PageNumParser

#get house list
class HistoryList(object):
    def __init__(self, comm_code):
        page_url = "http://bj.lianjia.com/chengjiao/pg1c" + str(comm_code)
            
        self.__comm_code = comm_code

        #there is already try-except structure in PageNumParser
        tp_page = PageNumParser(page_url)
        tp_page.close()
        page_num = tp_page.resPageNum()
            
        if page_num==None or tp_page.pageNumCheck(page_num)==False:
            self.__history_list = ""
            logging.error("HistoryList page_num error")
        else:
            logging.debug("HistoryList page_num " + str(page_num))
            self.__history_list = []
            for i in range(1, int(page_num)+1):
                tp_list = HistoryListParser(self.pageUrl(i))
                tp_list.close()
                self.__history_list += tp_list.resHistoryList()
                #print len(self.__history_list)

    #generate the list-page url
    #valid url:http://bj.lianjia.com/ershoufang/pgXc********    
    def pageUrl(self, page_num):
        url_base = "http://bj.lianjia.com/chengjiao/pg"
        url_end  = "c" + str(self.__comm_code)
        return url_base + str(page_num) + url_end

    def getHistoryList(self):
        return self.__history_list
    

class HistoryListParser(HTMLParser):
    def __init__(self, url):
        HTMLParser.__init__(self)
        self.__historyList = []
        self.__in_div = False
        
        logging.debug("HistoryListParser parse "+url)
        
        try:
            page = urllib.urlopen(url)
            page_data = page.read()
            self.feed(page_data)  
        except:
            self.__historyList = []
            logging.error("HistoryListParser " + url + " parase error")
            
    
    def handle_starttag(self, tag, attrs):
        if tag == "h2":
            self.__in_div = True
            
        if self.__in_div == True:
            if tag == "a" and len(attrs)==2:
                tmp = re.findall("BJ\S\S\d+", attrs[0][1])
                self.__historyList.append(tmp[0])
            
    def handle_endtag(self, tag):
        if tag == "h2" and self.__in_div == True:
            self.__in_div = False

    def resHistoryList(self):
        return self.__historyList




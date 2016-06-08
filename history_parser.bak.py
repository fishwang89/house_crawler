#! /usr/bin/env python
#coding=utf-8
import re, urllib, logging
from HTMLParser import HTMLParser

#get history information, which include history_num and history_info, from lianjia web
class HistoryPageParser(HTMLParser):
    def __init__(self, url):
        HTMLParser.__init__(self)
        self.__historyInfoFlag = False
        self.__historyTitleFlag = False
        self.__historyInfoData  = ""
        
        logging.debug("HistoryPageParser parse page " + url)
        
        self.__url = url
        
        try:
            page = urllib.urlopen(url)
            page_data = page.read()
            self.feed(page_data)
        except:
            logging.error("page " + url + "parse error")
        
    def handle_starttag(self, tag, attrs):
        #get history info
        if tag=="div" and len(attrs)==True and attrs[0][1]=="title-box":
            self.__historyTitleFlag = True
            
        if tag=="div" and len(attrs)==True and attrs[0][1]=="info-txt":
            self.__historyInfoFlag = True
        
        if tag== "p" and len(attrs)==True and attrs[0][1]=="info-item02":
            self.__historyInfoFlag = False

    def handle_endtag(self, tag):
        if self.__historyTitleFlag == True:
            if tag == "div":
                self.__historyTitleFlag = False

    def handle_data(self, data):
        if self.__historyInfoFlag == True or self.__historyTitleFlag == True:
            tmp = data.strip()
            if len(tmp) != 0:
                self.__historyInfoData += tmp
                self.__historyInfoData += '\n'
        
    def resHistoryInfo(self):
        dp = DataProcess(self.__historyInfoData, self.__url)
        return dp.process()


#dispose web data
class DataProcess(object):

    def __init__(self, input, url):
        self.__mTotalPrice  = "\d+.*\n\xe4\xb8\x87\n"
        self.__mUnitPrice   = "\d+\xe5\x85\x83 / \xe5\xb9\xb3\xe7\xb1\xb3"
        self.__mAraeSize    = "\d+.*\xe5\xb9\xb3\xe7\xb1\xb3"
        self.__mStructure   = "\n\d\xe5\xae\xa4\d\xe5\x8e\x85\n"
        self.__mBuildingAge = "\d+\xe5\xb9\xb4"
        self.__mDirection   = "\xe5\xb9\xb4\n.*\n"
        self.__mStorey      = "\xe5\x8e\x85\n.*\n"
        self.__mSignTime    = "\xe5\xb9\xb3\xe7\xb1\xb3\n.*\n.*\n\d+\n"
        self.__mBroker      = "\xe5\xb9\xb3\xe7\xb1\xb3\n.*\n\xe5\xa5\xbd\xe8\xaf\x84\xe7\x8e\x87"
        
        self.__input = input
        self.__url = url
    
    def getTotalPrice(self):
        #print "1"
        temp_str = re.findall(self.__mTotalPrice, self.__input)     
        temp_list = temp_str[0].split("\n")
        return temp_list[0]
    
    def getUnitPrice(self):
        #print "2"
        temp_str = re.findall(self.__mUnitPrice, self.__input) 
        temp_list = temp_str[0].split("\xe5\x85\x83")
        return temp_list[0]
    
    def getAreaSize(self):
        #print "3"
        temp_str = re.findall(self.__mAraeSize, self.__input)
        temp_list = temp_str[2].split("\xe5\xb9\xb3\xe7\xb1\xb3")
        return temp_list[0]

    def getSturcture(self):
        #print "4"
        temp_str = re.findall(self.__mStructure, self.__input) 
        temp_list = temp_str[0].split("\n")
        return temp_list[1]
    
    def getBuildAge(self):
        #print "5"
        temp_str = re.findall(self.__mBuildingAge, self.__input) 
        temp_list = temp_str[0].split("\xe5\xb9\xb4")
        return temp_list[0]
        
    def getDirection(self):
        #print "6"
        temp_str = re.findall(self.__mDirection, self.__input)
        temp_list = temp_str[0].split("\n")
        return temp_list[1]
    
    def getStorey(self):
        #print "7"
        temp_str = re.findall(self.__mStorey, self.__input)  
        temp_list = temp_str[0].split("\n")
        return temp_list[1]
    
    def getSignTime(self):
        #print "8"
        temp_str = re.findall(self.__mSignTime, self.__input) 
        temp_list = temp_str[0].split("\n")
        return temp_list[1]+temp_list[2]
    
    def getBroker(self):
        #print "9"
        temp_str = re.findall(self.__mBroker, self.__input)
        temp_list = temp_str[0].split("\n")
        return temp_list[1]
    
    
    def process(self):
        #logging.debug("page text: \n" + self.__input + "\n")
        try:
            res_json = {"TotalPrice": self.getTotalPrice(),
                        "UnitPrice" : self.getUnitPrice(),
                        "AreaSize"  : self.getAreaSize(),
                        "Structure" : self.getSturcture(),
                        "BuildAge"  : self.getBuildAge(),
                        "Direction" : self.getDirection(),
                        "Storey"    : self.getStorey(),
                        "SignTime"  : self.getSignTime(),
                        "Broker"    : self.getBroker() }
            return res_json
        except:
            logging.error(self.__url + " : page text parser error")
            return {}

#! /usr/bin/env python
#coding=utf-8
import re, urllib, logging
from HTMLParser import HTMLParser

#get house information, which include house_num and house_info, from lianjia web
class HousePageParser(HTMLParser):
    def __init__(self, url):
        HTMLParser.__init__(self)
        self.__houseInfoFlag = False
        self.__houseNumFlag = False
        self.__houseNumDataFlag = False
        self.__houseInfoData  = ""
        self.__houseNumData = ""
        
        self.__viewFlag = False
        self.__viewText = ""
        
        logging.debug("HousePageParser parse page "+ url)
        
        try:
            page = urllib.urlopen(url)
            page_data = page.read()
            self.feed(page_data)
        except:
            logging.error("page " + url + " parse error")
    
        logging.debug("Parse page end")
    
    def handle_starttag(self, tag, attrs):
        #get house info
        if tag == "div" and len(attrs) == True:
            #print attrs
            if attrs[0][1] == "desc-text clear":
                self.__houseInfoFlag = True
                self.__houseInfoData = ""
                #print "get flag"

            #get house num
            if attrs[0][1] == "iinfo right":
                self.__houseNumFlag = True
            
            if attrs[0][1] == "house-uni":
                self.__viewFlag = True

        if self.__houseNumFlag == True:
            if tag == "p" and len(attrs) == True:
                self.__houseNumDataFlag = True
                #print attrs

    def handle_endtag(self, tag):
        if self.__houseInfoFlag == True:
            if tag == "div":
                self.__houseInfoFlag = False

        if self.__houseNumFlag == True:
            if self.__houseNumDataFlag == True:
                if tag == "p":
                    self.__houseNumFlag = False
                    self.__houseNumDataFlag = False
        
        if self.__viewFlag == True:
            if tag == "ul":
                self.__viewFlag = False
        
    def handle_data(self, data):
        if self.__houseInfoFlag == True:
            self.__houseInfoData += data
            self.__houseInfoData += '\n'
            #print self.text_data
        
        if self.__houseNumDataFlag == True:
            self.__houseNumData += data
            #print self.__houseNumData 
            
        if self.__viewFlag == True:
            self.__viewText += data
            self.__viewText += "\n" 
     
    def resViewTimes(self):
        tmp = re.findall("\d+", self.__viewText)
        #print self.__viewText
        return tmp 
               
    def resHouseInfo(self):
        #print self.__houseInfoData
        dp = DataProcess(self.__houseInfoData)
        res_tmp = dp.process()
        
        list_tmp = self.resViewTimes()
        if len(list_tmp) == 3:
            res_tmp["ViewTimes"] = list_tmp[2]
        else:
            res_tmp["ViewTimes"] = 999
            
        return res_tmp

    

    #currently not used
    #def resHouseNum(self):
        #res = re.findall(r"BJ\S*", self.__houseNumData)     
        #return res[0]


#dispose web data
class DataProcess(object):

    def __init__(self, input):
        self.__mTotalPrice  = "\xe5\x94\xae\xe4\xbb\xb7\xef\xbc\x9a\n\d+.*\n"
        self.__mUnitPrice   = "\d+ \xe5\x85\x83/\xe5\xb9\xb3\xe7\xb1\xb3"
        #self.__mAraeSize    = "\d+.\d+\xe3\x8e\xa1"
        self.__mAraeSize    = "\d+.*\xe3\x8e\xa1"
        self.__mStructure   = "\xe6\x88\xb7\xe5\x9e\x8b\xef\xbc\x9a\n\d+.*\d+.*"
        self.__mBuildingAge = "\d+\xe5\xb9\xb4"
        self.__mDirection   = "\xe6\x9c\x9d\xe5\x90\x91\xef\xbc\x9a\n.*\n"
        self.__mStorey      = "\xe6\xa5\xbc\xe5\xb1\x82\xef\xbc\x9a\n.*\n"
        self.__mAddress     = "\xe5\xb0\x8f\xe5\x8c\xba\xef\xbc\x9a\n.*\n.*\n.*\n.*\n.*\n\d+"
        
        self.__input = input
    
    def getTotalPrice(self):
        #print "1"
        temp_str = re.findall(self.__mTotalPrice, self.__input)     
        temp_list = temp_str[0].split("\n")
        return temp_list[1]
    
    def getUnitPrice(self):
        #print "2"
        temp_str = re.findall(self.__mUnitPrice, self.__input) 
        temp_list = temp_str[0].split(" ")
        return temp_list[0]
    
    def getAreaSize(self):
        #print "3"
        temp_str = re.findall(self.__mAraeSize, self.__input)
        temp_list = temp_str[0].split("\xe3\x8e\xa1")
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
    
    def getAddress(self):
        #print "8"
        temp_str = re.findall(self.__mAddress, self.__input)  
        temp_list = temp_str[0].split("\n")
        address = {'community':'', 'location':'', 'district':''}
        address['community'] = temp_list[1]
        address['location']  = temp_list[4]
        address['district']  = temp_list[3]
        return address
    
    def process(self):
        try:
            res_json = {"TotalPrice": self.getTotalPrice(),
                        "UnitPrice" : self.getUnitPrice(),
                        "AreaSize"  : self.getAreaSize(),
                        "Structure" : self.getSturcture(),
                        "BuildAge"  : self.getBuildAge(),
                        "Direction" : self.getDirection(),
                        "Storey"    : self.getStorey(),
                        "Address"   : self.getAddress() }
            return res_json
        except:            
            logging.error("page text parser error")
            return {}
        


#! /usr/bin/env python
#coding=utf-8
import urllib, sqlite3, logging, os
from house_parser   import HousePageParser
from history_parser import HistoryPageParser
from db_operate import DBOperator
from plotting import SelfPlot

if __name__=="__main__":
    print "test prog start"
    
    webpage_base   = "../webpage/"
    database_path  = "../crawler_res/"
    
    #db_file = database_path+u"菊园.db" 
    #db = DBOperator()  
    #data_tmp = db.getHistoryInfo(db_file, '''select UnitPrice,SignTime from HistoryInfo where \
    #                                    Structure="2室1厅" ''')

   #SelfPlot(data_tmp,"test")
    
    '''db_file = "main_test.db" 
    db = DBOperator()    
    db.create(db_file)
    
    url = webpage_base + "webpage-normal/new-1.html"
    #url = "http://bj.lianjia.com/ershoufang/BJHD91054944.html"
    #url = "test.html"
    tp = HousePageParser(url)
    tp.close()
    houseInfo = tp.resHouseInfo()
    
    db.writeHouseInfo(db_file, houseInfo, "123")'''
    
    
    #url = webpage_base + "webpage-history-unit/xnz-unit-1.html"
    url = "http://bj.lianjia.com/chengjiao/BJHD89714922.html"
    tp = HistoryPageParser(url)
    tp.close()
    print tp.resHistoryInfo()
    
    
    print "test prog end"
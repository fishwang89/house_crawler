#! /usr/bin/env python
#coding=utf-8
import urllib, sqlite3, logging, os
from house_parser        import HousePageParser
from house_list_parser   import HouseList
from history_parser      import HistoryPageParser
from history_list_parser import HistoryList
from db_operate import DBOperator


def house_parser(commu_name, commu_code, db_file):   
    logging.debug(commu_name + "house parse start!")
    
    db = DBOperator()
    
    #house page info get and store
    try:
        #house list test prog
        tp = HouseList(commu_code)
        houseNumList = tp.getHouseList()
        print "house list len: " + str(len(houseNumList))
        logging.debug("get HouseList, len=%s"% (str(len(houseNumList))))
    except Exception, e:
        logging.error("house list parse error " + str(e))
        
    if len(houseNumList) > 0:
        #check if *.db exists
        if os.path.exists(db_file) == False:
            db.create(db_file)
            logging.debug("create db file : "+db_file)
        
        #parse house page
        logging.debug("HousePage parse start")
        for houseNum in houseNumList:
            #generate url
            url_tmp = "http://bj.lianjia.com/ershoufang/" + str(houseNum) + ".html"
            
            try:
                #house page prase prog
                tp = HousePageParser(url_tmp)
                tp.close()
                houseInfo = tp.resHouseInfo()
                if len(houseInfo) != 0:
                    db.writeHouseInfo(db_file, houseInfo, houseNum)
            except Exception, e:
                logging.error(url_tmp+" HousePage Parse Error, " + str(e))
            
        logging.debug("HousePage parse end")
        
        
        #history list test prog
        #tp = HistoryPageParser(webpage_base + "webpage-history-unit/ly-unit-1.html")#("BJSJ90413143")
        #tp.close()
        #a = tp.resHistoryInfo()
        
    logging.debug(commu_name + "house parse end!")


def history_parser(commu_name, commu_code, db_file):
    logging.debug(commu_name + " history parse start!")
    
    db = DBOperator()
    
    #history page info get and store
    try:
        #history list test prog
        tp = HistoryList(commu_code)
        historyNumList = tp.getHistoryList()
        print "history list len: " + str(len(historyNumList))
        logging.debug("get HistoryList, len=%s"% (str(len(historyNumList))))
    except Exception, e:
        logging.error("history list parse error " + str(e))
    
           
    if len(historyNumList) > 0:
        #parse history page
        logging.debug("HistoryPage parse start")
        for historyNum in historyNumList:
            #generate url
            url_tmp = "http://bj.lianjia.com/chengjiao/" + str(historyNum) + ".html"
            #http://bj.lianjia.com/chengjiao/
            
            try:
                #house page prase prog
                tp = HistoryPageParser(url_tmp)
                tp.close()
                historyInfo = tp.resHistoryInfo()
                if len(historyInfo) != 0:
                    db.writeHistoryInfo(db_file, historyInfo, historyNum)
            except Exception, e:
                logging.error(url_tmp+" HistoryPage Parse Error, " + str(e))
            
        logging.debug("HistoryPage parse end")
                
    logging.debug(commu_name + "history parse end!")


def simulate_login(username, passwd):
    


if __name__=="__main__":
    
    #init parameters
    database_path  = "../crawler_res/"
    webpage_base   = "../webpage/"
    
    #set up logging parameters
    FORMAT = '%(asctime)s - %(levelname)s - %(filename)s-%(lineno)d : %(message)s'
    logging.basicConfig(filename="../crawler_res/log.txt",
                        level=logging.DEBUG, 
                        filemode='a', 
                        format=FORMAT)
    
    commnuity_name = ["菊园"]
    commnuity_code = ["1111027377498"]
    
    if len(commnuity_name) != len(commnuity_code):
        print "len error, prog exit!"
        os._exit() 
    
    print "program  start"

    for i in range(0, len(commnuity_name)):
        db_file = database_path + commnuity_name[i] + ".db" 
        
        house_parser(commnuity_name[i], commnuity_code[i], db_file)
        
        history_parser(commnuity_name[i], commnuity_code[i], db_file)
        
    print "program end"


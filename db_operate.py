#! /usr/bin/env python
#coding=utf-8
import sqlite3, os, logging

class DBOperator():
    def __init__(self):
        pass
    
    def create(self, database):
        conn = sqlite3.connect(database)
        cu   = conn.cursor()
        cu.execute('''create table if not exists BasicInfo
                   ('id' integer primary key, name varchar);''')
        
        #'TotalPrice' int, 'UnitPrice' int, 'ViewTimes' int, 
        cu.execute('''create table if not exists HouseInfo
                   ('HouseNum' varchar(32) primary key, 
                    'TotalPrice' varchar(10), 'UnitPrice' varchar(10), 'ViewTimes' varchar(10),
                    'AreaSize' varchar(10), 'BuildAge' varchar(10), 'Direction' varchar(48), 
                    'Structure' varchar(128), 'Storey' varchar(128));''')
        cu.execute('''create table if not exists HistoryInfo
                   ('HouseNum' varchar(32) primary key, 
                    'TotalPrice' varchar(10), 'UnitPrice' varchar(10), 
                    'AreaSize' varchar(10), 'Direction' varchar(48), 
                    'Structure' varchar(128), 'Storey' varchar(128),
                    'SignTime' varchar(128), 'Broker' varchar(64));''')
                    
        conn.commit()
        conn.close()
            
     
    def writeBasicInfo(self, database, json, house_num):
        if os.path.exists(database) == False:
            self.create(database)
        
        conn = sqlite3.connect(database)
        cu   = conn.cursor()
        #cu.execute("insert into Basic "+data)
        conn.commit()
        conn.close()
        
    def writeHouseInfo(self, database, json, house_num):
        if os.path.exists(database) == False:
            self.create(database)
        
        conn = sqlite3.connect(database)
        cu   = conn.cursor()
        cu.execute("insert into \
        HouseInfo(HouseNum, TotalPrice, UnitPrice, ViewTimes, AreaSize, BuildAge, Direction, \
        Structure, Storey) values('%s', %s, %s, %s, %s, %s, '%s', '%s','%s')" \
        %(house_num, json["TotalPrice"], json["UnitPrice"], json["ViewTimes"], \
        json["AreaSize"], json["BuildAge"], json["Direction"], \
        json["Structure"], json["Storey"])) 
        conn.commit()
        conn.close()
        
    def writeHistoryInfo(self, database, json, house_num):
        if os.path.exists(database) == False:
            self.create(database)
            
        conn = sqlite3.connect(database)
        cu   = conn.cursor()
        cu.execute("insert into \
        HistoryInfo(HouseNum, TotalPrice, UnitPrice, AreaSize, Direction, \
        Structure, Storey, SignTime, Broker) \
        values('%s', %s, %s, %s, '%s', '%s', '%s', '%s', '%s')" \
        %(house_num, json["TotalPrice"], json["UnitPrice"], json["AreaSize"],\
          json["Direction"], json["Structure"], json["Storey"],\
          json["SignTime"], json["Broker"]))
        conn.commit()
        conn.close()
    
    def getHistoryInfo(self, database, sql_cmd):
        if os.path.exists(database) == False:
            logging.error("database "+database+" not exist")
            return ""
        
        conn = sqlite3.connect(database)
        cu   = conn.cursor()
        try:
            cu.execute(sql_cmd)
            res = cu.fetchall()
        except:
            logging.error(str(database)+" search, sql cmd "+str(sql_cmd)+" error")
            res = ""
            
        conn.close()        
        return res
     
    '''def writeHistoryInfo(self, database, json, house_num):
        if os.path.exists(database) == False:
            self.create(database)
            
        conn = sqlite3.connect(database)
        cu   = conn.cursor()
        cu.execute("insert into \
        HistoryInfo(HouseNum, TotalPrice, UnitPrice, AreaSize, Direction, \
        Structure, Storey, SignTime, Broker) \
        values('%s', %d, %d, %d, '%s', '%s', '%s', '%s', '%s')" \
        %(house_num, int(json["TotalPrice"]), int(json["UnitPrice"]), int(json["AreaSize"]),\
          json["Direction"], json["Structure"], json["Storey"],\
          json["SignTime"], json["Broker"]))
        conn.commit()
        conn.close()
    '''    
    
    '''def writeHouseInfo(self, database, json, house_num):
        if os.path.exists(database) == False:
            self.create(database)
        
        conn = sqlite3.connect(database)
        cu   = conn.cursor()
        cu.execute("insert into \
        HouseInfo(HouseNum, TotalPrice, UnitPrice, ViewTimes, AreaSize, BuildAge, Direction, \
        Structure, Storey) values('%s', %d, %d, %d, %d, %d, '%s', '%s','%s')" \
        %(house_num, int(json["TotalPrice"]), int(json["UnitPrice"]), int(json["ViewTimes"]), \
        int(json["AreaSize"]), int(json["BuildAge"]), json["Direction"], \
        json["Structure"], json["Storey"])) 
        conn.commit()
        conn.close()
    '''    
            
    '''def insert(self, database, json, house_num):
        conn = sqlite3.connect(database)
        cu   = conn.cursor()
        
        tmp = { "tables" : "HouseInfo",
                "HouseNum": house_num,
                "AreaSize": int(json["AreaSize"]),
                "BuildAge": int(json["BuildAge"]),
                "TotalPrice":int(json["TotalPrice"])
              }
        
        template = "INSERT INTO %(tables)s VALUES('%(HouseNum)s' '%(AreaSize)d' '%(BuildAge)d' '%(TotalPrice)d')"
        cu.execute(template % tmp)
        conn.commit()
        conn.close()'''
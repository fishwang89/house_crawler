#! /usr/bin/env python
#coding=utf-8
import re
import matplotlib.pyplot as plt

def SelfPlot(data_array, community):
    time_list = []
    price_list = []
    i = 0
    x = []
    
    for cell in data_array:
        price_list.append(cell[0])
        time_list.append(re.findall("\d{4}.\d{2}", cell[1]))
        i+=1
        x.append(i)
        
    print price_list
    print "-----------------------------------------------"
    print time_list
        
    plt.title(str(community)+ " Average UnitPrice Trend")
    plt.xlabel("Time")
    plt.ylabel("UnitPrice")
    #plt.xlim()
    #plt.ylim()
    plt.plot(x, price_list, 'go--')
    plt.show()
    
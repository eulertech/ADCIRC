# -*- coding: utf-8 -*-
"""
Created on Wed May 18 13:25:40 2016
get_WL(stationID, startDate, endDate,productName="waterlevelverifiedsixmin",Datum= "MSL")
    stationID = 8454000
    beginDate = 20160201
    endDate = 20160301
    Datum = "MSL"
    productName ="waterlevelverifiedsixmin"
@author: liang.kuang
"""
import wget, os,sys
import datetime
from matplotlib.dates import datestr2num
import csv, requests
import numpy as np
import pandas as pd

def get_WL(stationID, beginDate, endDate,productName="waterlevelverifiedsixmin",Datum= "MSL"):

#wl_ts:http://opendap.co-ops.nos.noaa.gov/axis/webservices/waterlevelverifiedsixmin/response.jsp?stationId=8454000&beginDate=20160301&endDate=20160301&datum=MLLW&unit=0&timeZone=0&format=text&Submit=Submit
#prediction:http://opendap.co-ops.nos.noaa.gov/axis/webservices/predictions/response.jsp?stationId=8454000&beginDate=20160601&endDate=20160601&datum=MLLW&unit=0&timeZone=0&dataInterval=6&format=text&Submit=Submit

    print("Retrieving Station %d %s at %s from CO-OPS through OPENDAP" %(stationID,productName, Datum))
    if(productName == "waterlevelverifiedsixmin"):
        url = ("http://opendap.co-ops.nos.noaa.gov/axis/webservices/" + productName +
        "/response.jsp?stationId=" + str(stationID) + 
        "&beginDate=" +str(beginDate) + "&endDate=" + str(endDate) + "&datum=" + 
            Datum + "&unit=0&timeZone=0&format=text&Submit=Submit")
    elif (productName == "predictions"):
        url = ("http://opendap.co-ops.nos.noaa.gov/axis/webservices/" + productName +
                "/response.jsp?stationId=" + str(stationID) + 
        "&beginDate=" +str(beginDate) + "&endDate=" + str(endDate) + "&datum=" + 
            Datum + "&unit=0&timeZone=0&dataInterval=6&format=text&Submit=Submit")
        
    print(url)
    file2save = 'wl' + str(stationID) + '.dat'
    filename = wget.download(url)    
    try:
        os.replace(filename,file2save)
    except:
        pass
    lines = open(file2save).readlines()
       
    if (len(lines)) <40:  # no data skip
        print(lines)
        sys.exit()
    else:
        preLoc = [line.find('pre>') for line in lines]
        loc = []
        for n in np.arange(len(preLoc)):
            if(preLoc[n]!=-1):
                print(lines[n])
                loc.append(n)
        content = lines[loc[1]+1:loc[2]] 
    data = []        
    for n in np.arange(len(content)):
        data.append(content[n].split())
    if(productName == "waterlevelverifiedsixmin"):    
        df=pd.DataFrame(data,dtype=(float),columns=['StationID','Date','Time','WL','Sigma','I','F','R','T'])    
    elif(productName == "predictions"):
        df=pd.DataFrame(data,dtype=(float),columns=['StationID','Date','Time','WL'])    
    date = df['Date']
    time = df['Time']
    dt = ','.join('%s %s' %t for t in zip(date,time))
    dt = dt.split(sep=',')
    if(productName == "waterlevelverifiedsixmin"):        
        dd=[datetime.datetime.strptime(d,'%Y-%m-%d %H:%M') for d in dt] 
    elif(productName == "predictions"):
        dd=[datetime.datetime.strptime(d,'%m/%d/%Y %H:%M') for d in dt]                 
    elv = [float(eta) for eta in df['WL']  ]
    df['DateTime']=pd.Series(data=dd)
    df['Elevation'] =pd.Series(data = elv)
    df['Elevation'].astype(float)
    cols = [col for col in df.columns if col in ['DateTime','Elevation']]
    df = df[cols]
    df.dtypes
    print("Successfully downloaded waterlevel data from opendap.co-ops.noaa.gov \n")
#    import matplotlib.pyplot as plt
#    fig1 = plt.figure(1,figsize=(6,4),dpi=200)
#    fig1.clf()
#    ax1 = fig1.add_axes([0.1 ,0.1 ,0.8,0.8])
#    df.plot(ax=ax1,x='DateTime',y='Elevation',grid='on',fontsize=5,legend=False)
    return df    
    
    
    

    
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 13:19:25 2016
download harmonic constant at GMT with unit of meter
get_ha(stationID): stationID is integer
may need to de first element in the dictionary as it is empty. post processing (del ha[0])
@author: liang.kuang
"""
#import wget,json
import csv,datetime
import urllib3
from bs4 import BeautifulSoup
#ha: http://opendap.co-ops.nos.noaa.gov/axis/webservices/harmonicconstituents/response.jsp?stationId=8454000&unit=0&timeZone=0&format=text&Submit=Submit
def get_ha(stationID,saveData=False):
#    url = 'http://opendap.co-ops.nos.noaa.gov/axis/webservices/harmonicconstituents/response.jsp?stationId=8454000&unit=0&timeZone=0&format=text&Submit=Submit'
#    url_html = 'http://opendap.co-ops.nos.noaa.gov/axis/webservices/harmonicconstituents/response.jsp?stationId=8454000&unit=0&timeZone=0&format=html&Submit=Submit'
#    stationID = 1630000
    startTime = datetime.datetime.now() 
    url = 'https://tidesandcurrents.noaa.gov/harcon.html?unit=0&timezone=0&id='+str(stationID)
    http = urllib3.PoolManager(retries = 3)
#    filename = wget.download(url_html)
    r = http.request('GET',url)
    soup = BeautifulSoup(r.data,"lxml")
    table=soup.find("table", attrs = {"class":"table table-striped"})
    
    headings = [th.get_text() for th in table.find("tr").find_all("th")]
    datasets = []
    for row in table.find_all("tr"):
        dataset = dict(zip(headings, (td.get_text() for td in row.find_all("td"))))
    #    dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
        datasets.append(dataset)
        
#print(datasets[1]['Amplititude'])
    if(saveData):
        file2save="HarmonicConstant_"+str(stationID)+".csv"   
        fn = csv.writer(open(file2save,"w",newline = ''))
        i = 0
        while i < len(datasets):
            ampphase = datasets[i]
            for key,val in ampphase.items():
                #print(key,val)
                fn.writerow([key,val])
            i = i + 1
    print("Harmonic Constant for Station %d is finished" %(stationID))
    print("Elapsed Time is %s\n" %(datetime.datetime.now() - startTime))
    return datasets
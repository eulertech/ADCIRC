# -*- coding: utf-8 -*-
"""
Created on Fri May 13 10:36:24 2016
Updated on Thu Sep 08 15:31:00 2016

@author: liang.kuang
"""

import numpy as np
import datetime
import csv
from ADCIRC.Grid.Plot_Grid import plot_grid

startTime = datetime.datetime.now()
class myGrid(object):
    gridType = "ADCIRC Triangular Grid"
    def __init__(self,NP,NE,coordinates,triangles,obc_locations,lnd_locations,
                 NOPE, NETA, NVDLL,NBDV, NBOU, NVEL,NVELL,IBTYPE,NBVV,IBCONN,
                 BARINHT,BARINCFSB,BARINCFSP,BARLANHT,BARLANCFSP,
                 PIPEHT,PIPECOEF,PIPEDIAM,missingData):
        self.np = NP
        self.ne = NE
        self.coordinates= coordinates
        self.triangles = triangles
        self.obc_locations = obc_locations
        self.lnd_locations = lnd_locations
        self.NOPE = NOPE
        self.NETA = NETA
        self.NVDLL = NVDLL
        self.NBDV = NBDV
        self.NBOU = NBOU
        self.NVEL = NVEL
        self.NVELL = NVELL
        self.IBTYPE = IBTYPE
        self.NBVV = NBVV
        self.IBCONN = IBCONN
        self.BARINHT = BARINHT
        self.BARINCFSB = BARINCFSB
        self.BARINCFSP = BARINCFSP
        self.BARLANHT = BARLANHT
        self.BARLANCFSP= BARLANCFSP
        self.PIPEHT = PIPEHT
        self.PIPECOEF = PIPECOEF
        self.PIPEDIAM = PIPEDIAM
        self.missingData = missingData

    def description(self):
        print ("ADCIRC grid created with:")
        print ("Total number of nodes is %d and total elements is %d" % (self.np,self.ne))


def read_grid(filename,missingData = -999999.):
    print('Starting to read ADCIRC grid with name: %s\n' %(filename))
    f = open(filename)
    f.readline()
    line2 = f.readline()
    [NE,NP]=line2.split()
    NE = int(NE)
    NP= int(NP)
    coordinates = np.zeros([NP,3],dtype=float)
    triangles = np.zeros([NE,3],dtype = int)
# read nodes nodeID, x,y,z
    cnt = 0
    while cnt<NP:
        line = f.readline()
        coordinates[cnt,0] = float(line.split()[1]) #x
        coordinates[cnt,1] = float(line.split()[2]) #y
        coordinates[cnt,2] = float(line.split()[3]) #z-depth
        cnt = cnt + 1
    print("nodes coordinates reading done!")
# read triangles elementID, np1,np2,np3
    cnt = 0
    while cnt<NE:
        line = f.readline()
       # print(line)
        triangles[cnt,0] = int(line.split()[2])
        triangles[cnt,1] = int(line.split()[3])
        triangles[cnt,2] = int(line.split()[4])
        cnt = cnt + 1
    print("Elements/Triangle information reading done!")
    line = f.readline()
    NOPE = int(line.split()[0])
    line = f.readline()
    NETA = int(line.split()[0])
    obc_locations = np.nan * np.ones([NETA+NOPE-1,2])

    NVDLL = np.zeros([NOPE,1],dtype=int)
    NBDV = np.zeros([NOPE,NETA],dtype=int)  #many empty cells
    cnt=0
    for k in np.arange(0,NOPE,dtype = int):
        line = f.readline()
        NVDLL[k] = int(line.split()[0])
        if(k>0):
            cnt = cnt + 1  # pad
            obc_locations[cnt,0] = missingData
            obc_locations[cnt,1] = missingData

        for j in np.arange(0,NVDLL[k]):
            line = f.readline()
            NBDV[k,j] = int(line.split()[0]) #node ID of OBC of group k (NOPE)
            obc_locations[cnt,0] = coordinates[int(NBDV[k,j])-1,0]
            obc_locations[cnt,1] = coordinates[int(NBDV[k,j])-1,1]
            cnt = cnt + 1
    print("Open boundary information done!")
    #NBDV[NBDV==0] = np.nan  # remove empty cells

    line = f.readline()
    NBOU = int(line.split()[0]) # number of land boundaries
    line = f.readline()
    NVEL = int(line.split()[0])  # total number of land boundary nodes
    lnd_locations = np.nan * np.ones([NVEL+NBOU-1,2])



    NVELL = np.zeros([NBOU,1],dtype = int)
    NBVV = np.zeros([NBOU,NVEL],dtype = int)  #many empty cells
    BARLANHT = np.zeros([NBOU,NVEL])  #[3,13,23 BTYPE]
    BARLANCFSP = np.zeros([NBOU,NVEL]) #[3,13,23 BTYPE]
    IBCONN = np.zeros([NBOU,NVEL],dtype = int)  #[4,24 BTYPE]
    BARINHT = np.zeros([NBOU,NVEL])
    BARINCFSB = np.zeros([NBOU,NVEL])
    BARINCFSP = np.zeros([NBOU,NVEL])
    PIPEHT = np.zeros([NBOU,NVEL]) #[5,25 BTYPE]
    PIPECOEF = np.zeros([NBOU,NVEL])
    PIPEDIAM = np.zeros([NBOU,NVEL])

    cnt =0
    IBTYPE = np.zeros([NBOU,1],dtype = int)
    for k in np.arange(0,NBOU,dtype = int):
        line = f.readline()
        NVELL[k] = int(line.split()[0])
        IBTYPE[k] = int(line.split()[1])
        if (k>0):
            cnt = cnt + 1
            lnd_locations[cnt,0] = missingData
            lnd_locations[cnt,1] = missingData
            #print("pad nan between land boundaries %f" %(lnd_locations[cnt,0]))
        # here only deal with IBTYPE is 0,1,2,10 etc...
            #print('Land Boundary Type readed is %d\n' %IBTYPE[k])
        if (np.in1d(IBTYPE[k],np.asarray([0, 1, 2, 10, 11, 12, 20, 21, 22, 30],dtype = int))):
            #print("read land boundary locations!")
            for j in np.arange(0,NVELL[k],dtype = int):
                line = f.readline()
                NBVV[k,j] = int(line.split()[0])
                lnd_locations[cnt,0] = coordinates[int(NBVV[k,j])-1,0]
                lnd_locations[cnt,1] = coordinates[int(NBVV[k,j])-1,1]
                cnt = cnt + 1
        elif(np.in1d(IBTYPE[k],np.asarray([3,13,23],dtype = int))):  #
            for j in np.arange(0,NVELL[k],dtype = int):
                line = f.readline()
                NBVV[k,j] = int(line.split()[0])
                BARLANHT[k,j] = float(line.split()[1])
                BARLANCFSP[k,j] = float(line.split()[2])
                lnd_locations[cnt,0] = coordinates[int(NBVV[k,j])-1,0]
                lnd_locations[cnt,1] = coordinates[int(NBVV[k,j])-1,1]
                cnt = cnt + 1
        elif (np.in1d(IBTYPE[k],np.asarray([4,24],dtype = int))):  #weir
            for j in np.arange(0,NVELL[k],dtype = int):
                line = f.readline()
                NBVV[k,j] = int(line.split()[0])
                IBCONN[k,j] = int(line.split()[1])
                BARINHT[k,j] = float(line.split()[2])
                BARINCFSB[k,j] = float(line.split()[3])
                BARINCFSP[k,j] = float(line.split()[4])
                lnd_locations[cnt,0] = coordinates[int(NBVV[k,j])-1,0]
                lnd_locations[cnt,1] = coordinates[int(NBVV[k,j])-1,1]
                cnt = cnt + 1
        elif(np.in1d(IBTYPE[k],np.asarray([5,25],dtype = int))):
            for j in np.arange(0,NVELL[k],dtype = int):
                line = f.readline()
                NBVV[k,j] = int(line.split()[0])
                IBCONN[k,j] = int(line.split()[1])
                BARINHT[k,j] = float(line.split()[2])
                BARINCFSB[k,j] = float(line.split()[3])
                BARINCFSP[k,j] = float(line.split()[4])
                PIPEHT[k,j] = float(line.split()[5])
                PIPECOEF[k,j] = float(line.split()[6])
                PIPEDIAM[k,j] = float(line.split()[7])
                lnd_locations[cnt,0] = coordinates[int(NBVV[k,j])-1,0]
                lnd_locations[cnt,1] = coordinates[int(NBVV[k,j])-1,1]
                cnt = cnt + 1

    print("Land boundary information done!")
    #NVELL[NVELL==0] = np.nan  # remove empty cells

    with open('ADCIRC_OBC.csv','w', newline = '') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(obc_locations)

# save the grid
    ADCIRC_Grid = myGrid(NP,NE,coordinates,triangles,obc_locations,lnd_locations,
                         NOPE, NETA, NVDLL,NBDV, NBOU, NVEL,NVELL,IBTYPE,NBVV,IBCONN,
                         BARINHT,BARINCFSB,BARINCFSP,BARLANHT,BARLANCFSP,
                         PIPEHT,PIPECOEF,PIPEDIAM,missingData);
    elapsedTime = datetime.datetime.now() - startTime
    print("Total elapsed time is %s minutes!" %elapsedTime)
    print(ADCIRC_Grid)
    f.close()
    return ADCIRC_Grid


#plot the grid to check

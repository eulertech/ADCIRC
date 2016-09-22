# -*- coding: utf-8 -*-
"""
Created on Fri May 13 14:43:16 2016
Updated on Thu Sep 08 15:31:00 2016

@author: liang.kuang
"""
import numpy as np
import datetime
startTime = datetime.datetime.now()

header = 'ADCIRC Grid written by Python'
numEdge = 3
def write_grid(myGrid,fileOut):
    print('Start to write ADCIRC grid! ')
    f = open(fileOut,'w')
    f.write('%s\n' %(header) )
    f.write('%d  %d\n' % (myGrid.ne,myGrid.np))

    for i in np.arange(0,myGrid.np,dtype = int):
        f.write('%10d %15.10f %15.10f %16.9f\n' %(i+1,myGrid.coordinates[i,0],myGrid.coordinates[i,1],myGrid.coordinates[i,2]))
    print('Nodes written!')
    for i in np.arange(0,myGrid.ne,dtype = int):
        f.write('%4d %4d %5d %5d %5d\n' %(i+1,numEdge,myGrid.triangles[i,0],myGrid.triangles[i,1],myGrid.triangles[i,2]))
    print('Elements written!')
# write number of OPE
    f.write('%d     %s\n' %(myGrid.NOPE,'! Number of Open Boundary'))
    f.write('%d     %s\n' %(myGrid.NETA,'!Total Number of nodes for all open Boundary'))

    for k in np.arange(0,myGrid.NOPE,dtype = int):
        f.write('%d     %s %d\n' %(myGrid.NVDLL[k],'!Open Boundary Number #',k+1))
        for j in np.arange(0,myGrid.NVDLL[k],dtype = int):
            f.write('%d\n' %(myGrid.NBDV[k,j]))
    print('Open Boundary Written!')
## write land boundary
    f.write('%d     %s\n' %(myGrid.NBOU,'!Number of Land Boundary '))
    f.write('%d     %s\n' %(myGrid.NVEL,'!Total number of nodes for land Boundary'))
#
    for k in np.arange(0,myGrid.NBOU,dtype = int):
        f.write('%d %d  %s %d\n' %(myGrid.NVELL[k], myGrid.IBTYPE[k],' = Number of node for land boundary ',k+1 ))  #
        if(np.in1d(myGrid.IBTYPE[k],np.asarray([0, 1, 2, 10, 11, 12, 20, 21, 22, 30]))):
            #print("Writing mainland[0,20],island[1] boundaries,river or ocean inflow[2].")
            for j in np.arange(0,myGrid.NVELL[k],dtype = int):
                f.write('%d\n' %(myGrid.NBVV[k,j]) )
        elif(np.in1d(myGrid.IBTYPE[k],np.asarray([3,13,23]))):
            #print("Writing flow over a weir out of the domain Boundary Type[3,13,33].")
            for j in np.arange(0,myGrid.NVELL[k],dtype = int):
                f.write('%d\n' %(myGrid.NBVV[k,j]),myGrid.BARLANHT[k,j],myGrid.BARLANCFSP[k,j] )
        elif(np.in1d(myGrid.IBTYPE[k],np.asarray([4,24]))):
            #print('Writing interior levees information for IBTYPE[4,24].')
            for j in np.arange(0,myGrid.NVELL[k],dtype = int):
                f.write('%d %d %d %d %d\n' %(myGrid.NBVV[k,j],myGrid.IBCONN[k,j],
                        myGrid.BARINHT[k,j],myGrid.BARINCFSB[k,j],myGrid.BARINCFSP[k,j]))
        elif(np.in1d(myGrid.IBTYPE[k],np.asarray([5,25]))):
            #print("Writing interior levees with cross-barrier pipes[5,25].")
            for j in np.arange(0,myGrid.NVELL[k],dtype = int):
                f.write('%d %d %d %d %d\n' %(myGrid.NBVV[k,j],myGrid.IBCONN[k,j],
                        myGrid.BARINHT[k,j],myGrid.BARINCFSB[k,j],myGrid.BARINCFSP[k,j],
                        myGrid.PIPEHT[k,j],myGrid.PIPECOEF[k,j],myGrid.PIPEDIAM[k,j]))
    print('Land Boundaries Written!')
    f.close()
    print("Grid successfully written to:" + fileOut)
    elapsedTime = datetime.datetime.now() - startTime
    print("Total elapsed time for writing this grid is %s minutes!" %elapsedTime)

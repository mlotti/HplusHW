#! /usr/bin/env python

import os
import collections
import sys
import copy


def getShortName(name):
    n = name.replace("_QCDinv_DataDriven","")
    n = n.replace("NoCuts","N")
    n = n.replace("LoosePlus","L")
    n = n.replace("MediumPlus","M")
    n = n.replace("TightPlus","T")
    n = n.replace("_nodphi","")
    n = n.replace("nominal","met60")
    n = n.replace("_x","_")
    mySplit = n.split("_")
    s = ""
    for i in range(0,len(mySplit)):
        if mySplit[i].startswith("OptQCDTailKiller"):
            if not "met" in mySplit[i+1]:
                s = "met60"
            else:
                if "tau" in mySplit[i+1]:
                   s = mySplit[i+1].replace("tau",", tau")
                else:
                   s = mySplit[i+1]
            if not "tau" in mySplit[i+1]:
                s += ", tau41"
            else:
                if not "met" in mySplit[i+1]:
                    s += ", "+mySplit[i+1]
            s += ", "+mySplit[i].replace("OptQCDTailKiller","")
            return s

def printTable(table, n, m):
    s = ""
    for l in table:
       s += " & ".join(map(str, l[n:m]))
       s += "\\\\ \n"
    print "\n",s,"\n"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("provide input file!")
    print "analyzing",sys.argv[1]

    if not os.path.exists(sys.argv[1]):
        raise Exception("Cannot find file '%s'!"%sys.argv[1])

    f = open(sys.argv[1])
    lines = f.readlines()
    f.close()

    # Read
    myDictionaryList = []
    myDict = None
    myMasses = []
    for l in lines:
        # fill previous
        if "datacard" in l:
            if myDict != None and len(myDict.keys()) > 1:
                myDictionaryList.append(copy.deepcopy(myDict))
            myDict = {}
            myDict["name"] = l.replace("\n","")
        mySplit = l.split()
        if len(mySplit) > 1:
            if mySplit[0][len(mySplit[0])-1] == '0' or mySplit[0][len(mySplit[0])-1] == '5':
                myDict[(mySplit[0])] = float(mySplit[1])
                if not float(mySplit[0]) in myMasses:
                    myMasses.append(float(mySplit[0]))
    # Save last one
    if len(myDict.keys()) > 1:
        myDictionaryList.append(copy.deepcopy(myDict))

    # Find key list:
    myMasses.sort()

    table = []
    for i in myDictionaryList:
        table.append([])
    table.append([])

    # Print sorted list
    for m in myMasses:
       mm = "%d"%m
       table[0].append("\\Hpm = %d \\GeVcc"%m)
       myList = []
       for i in myDictionaryList:
           if not mm in i.keys():
               i[mm] = 999
           myList.append(i)
           
       l = sorted(myList, key=lambda x: x[mm])
       print "\n Optimum for m =",mm
       n = 1
       for item in l:
           if abs(item[mm] - 999) > 0.0001 and item[mm] < 1.2:
               s = "%.4f (%s)"%(item[mm],getShortName(item["name"]))
           else:
               s = "n.a. (%s)"%(getShortName(item["name"]))
           table[n].append(s)
           print s
           n += 1

    # print table
    n = 0
    step = 3
    while n < len(myMasses):
        printTable(table, n, n+step)
        n += step

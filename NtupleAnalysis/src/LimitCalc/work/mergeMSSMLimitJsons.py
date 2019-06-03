#!/usr/bin/env python

import sys
import re
import array
import os
import json

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.LimitCalc.limit as limit
import HiggsAnalysis.LimitCalc.BRXSDatabaseInterface as BRXSDB

tanbMax = 65

ROOT.gROOT.LoadMacro("LHCHiggsUtils.C")

db = None

def usage():
    print
    print "### Usage:  ",sys.argv[0],"<light H+ MSSM limit json > <heavy H+ MSSM limit json>"
    print
    sys.exit()

def xminmax(points,label="x"):
    xmin = 999
    xmax = -999

    for p in points:
        x = float(p[label])
        if x < xmin:
            xmin = x
        if x > xmax:
            xmax = x
            
    return xmin,xmax


def findHighEndPosition(limit):

    xmin,xmax = xminmax(limit)
    print "check xmin,xmax",xmin,xmax
    ymin,ymax = xminmax(limit,"y")
    print "check ymin,ymax",ymin,ymax
    highestXY = -1
    for i,p in enumerate(limit):
        if p["x"] == xmax and p["y"] == ymax:
            return i
    return None

def append(index,json1,json2):
    #append json2 into json1 starting from position index
    merged = []
    if index == 0:
        for p in reversed(json2):
            print "Json2       ",p["x"],p["y"]
            merged.append(p)
        for i,p in enumerate(json1):
            print "Json1, first part",p["x"],p["y"]
            merged.append(p)
    else:
        for i,p in enumerate(json1):
            if i <= index:
                print "Json1, first part",p["x"],p["y"]
                merged.append(p)
        if json2[0]["y"] > json2[len(json2)-1]["y"]:
            for p in json2:
                print "Json2       ",p["x"],p["y"]
                merged.append(p)
        else:
            for p in reversed(json2):
                print "Json2       ",p["x"],p["y"]
                merged.append(p)
        for i,p in enumerate(json1):
            if i > index:
                print "Json1, second part",p["x"],p["y"]
                merged.append(p)
    return merged                  
        
def mergeJson(json1,json2):
    returnJson = json1
    for k in json1.keys():
        if k in ["exp2","exp1","obs","exp","Allowed"]:
            if k == "Allowed":
                if len(json2[k]) > len(json1[k]):
                    returnJson[k] = json2[k]
            else:
                print k
                i = findHighEndPosition(json1[k])
                returnJson[k] = append(i,json1[k],json2[k])

    return returnJson
    
def mergeJsons(jsonfiles):
    merged = {}
    for jsonfile in jsonfiles:
        f = open(jsonfile, "r")
        limits = json.load(f)
        f.close()
        if len(merged.keys()) == 0:
            merged = limits
        else:
            mergeJson(merged,limits)

    merged["regime"] = "combined"
    merged["name"] = merged["name"].replace("light","combined",1) 
    return merged
            
def main():
    if len(sys.argv) == 1:
        usage()

    jsonfiles = []
    for argv in sys.argv:
        if os.path.isfile(argv) and "json" in argv:
            jsonfiles.append(argv)

    jsonfile = mergeJsons(jsonfiles)

    with open(jsonfile["name"]+'.json', 'w') as fOUT:
#        json.dump(jsonfile, fOUT, sort_keys=True, indent=2 )
        json.dump(jsonfile, fOUT, indent=2 )
        print "created",jsonfile["name"]+'.json'

if __name__ == "__main__":
    main()

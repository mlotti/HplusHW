#!/usr/bin/env python

import sys
import os
import ROOT

class JsonWriter:

    def __init__(self):
        self.graphs = {}
        self.parameters = {}
        
    def addParameter(self,name,value):
        self.parameters[name] = value
        
    def addGraph(self,name,graph):
        self.graphs[name] = graph

    def timeStamp(self):
        import datetime
        time = datetime.datetime.now().ctime()
        return time
    
    def write(self,fOUTname):
        fOUT = open(fOUTname,"w")
        fOUT.write("{\n")
        time = self.timeStamp()
        fOUT.write("  \"_timestamp\":   \"Generated on "+time+" by HiggsAnalysis/NtupleAnalysis/src/LimitCalc/work/JsonWriter.py\",\n")
        for key in self.parameters.keys():
            fOUT.write("  \""+key+"\": \"%s\",\n"%self.parameters[key])

        nkeys = 0
        for key in self.graphs.keys():
            fOUT.write("  \""+key+"\": [\n")
            for i in range(self.graphs[key].GetN()):
                x = self.graphs[key].GetX()
                y = self.graphs[key].GetY()
                comma = ","
                if i == self.graphs[key].GetN() - 1:
                    comma = ""
                fOUT.write("      { \"x\": %s, \"y\": %s }%s\n"%(x[i],y[i],comma))
            nkeys+=1
            if nkeys < len(self.graphs.keys()):
                fOUT.write("  ],\n")
            else:
                fOUT.write("  ]\n")

        fOUT.write("}\n")
                
        fOUT.close()
        print "Created",fOUTname

        sys.exit()
        """
        runrange_re = re.compile("(?P<firstRun>(\d+))-(?P<lastRun>(\d+))")
        comma = ","
        subranges = []
        subranges = self.ranges
        for i,r in enumerate(subranges):
            if i == len(subranges)-1:
                comma = ""
                #            if r.name == name:
                match = runrange_re.search(r.runrange)
                if not match:
                    print "Run range not valid",r.runrange
                    sys.exit()
                    
                    fOUT.write("      \"runs_"+match.group("firstRun")+"_"+match.group("lastRun")+"\": {\n")
                    fOUT.write("          \"era\": \""+r.label+"\",\n")
                    fOUT.write("          \"firstRun\"  :"+match.group("firstRun")+",\n")
                    fOUT.write("          \"lastRun\"   :"+match.group("lastRun")+",\n")
                    fOUT.write("          \"luminosity\": %s,\n"%r.lumi)
                    self.writeJSONBins(fOUT,r.label,r.eff)
                    fOUT.write("      }"+comma+"\n")
                    fOUT.write("  },\n")
                    
                    fOUT.write("  \"mcParameters\": {\n")
                    comma = ","
                    subranges = []
                    #        for mc in self.mcs:
                    #            if mc.name == name:
                    #                subranges.append(mc)
                    subranges = self.mcs
                    for i,mc in enumerate(subranges):
                        if i == len(subranges)-1:
                                                                                                                                                     """
        

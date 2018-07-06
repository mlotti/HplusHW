#!/usr/bin/env python

import os
import re
import sys
from math import sqrt

import ROOT

class PythonWriter:
    class Parameters:
        def __init__(self,name,label,runrange,lumi,eff):
            self.name     = name
            self.label    = label
            self.runrange = runrange
            self.lumi     = lumi
            self.eff      = eff
        def Print(self):
            print "Parameters",self.name,self.label,self.runrange,self.lumi
            #for i in range(0,self.eff.GetN()):
            #    print "    ",i,self.eff.GetX()[i],self.eff.GetY()[i]

    def __init__(self):#,title):
#        self.title  = title
        self.ranges = []
        self.mcs    = []
        self.namedSelection = []
        self.bins   = []
        self.plotDir = "./"

        self.rootVersion = ROOT.gROOT.GetVersion()

    def setInput(self,inString):
        self.inString = os.path.basename(inString)

    def setPlotDir(self,dirname):
        self.plotDir = dirname

    def setStatOption(self,statOption):
        self.statOption = statOption

    def addParameters(self,path,label,runrange,lumi,eff):
        name = "dummy"
        #print "check addParameters",name,path,label,runrange,lumi 
        labelFound = False
#        for r in self.ranges:
#            if r.name == name and r.label == label and r.runrange == runrange:
#                labelFound = True
#        if not labelFound and not label == "Unweighted":
#            self.ranges.append(self.Parameters(name,label,runrange,lumi,eff))
#            self.dumpParameters(path,label,runrange,lumi,eff)
        self.ranges.append(self.Parameters(name,label,runrange,lumi,eff))
        #print "check self.ranges size",len(self.ranges)
        for r in self.ranges:
            r.Print()

    def addMCParameters(self,label,eff):
        name = "dummy"
        #print "check addMCParameters",name,label
        labelFound = False
        for mc in self.mcs:
            if mc.label == label and mc.name == name:
                labelFound = True
        if not labelFound:
            self.mcs.append(self.Parameters(name,label,"","",eff))
        for mc in self.mcs:
            mc.Print()

    def SaveOfflineSelection(self,selection):
        found = False
        for n in self.namedSelection:
            if n == selection:
                found = True
        if not found:
            self.namedSelection.append(selection)

    def dumpParameters(self,path,label,runrange,lumi,eff):

        fName = os.path.join(path,"dataParameters.py")
        fOUT = open(fName,"w")

        self.writeParameters(fOUT,label,runrange,lumi,eff)

    def write(self,fileName):
        fName = os.path.join(self.plotDir,fileName)
        fOUT = open(fName,"w")
        time = self.timeStamp()
        fOUT.write("# Generated on "+time+"\n")
        fOUT.write("# by HiggsAnalysis/TriggerEfficiency/test/PythonWriter.py\n\n")

        for r in self.ranges:
            self.findBins(r.eff)

        fOUT.write("import FWCore.ParameterSet.Config as cms\n\n")

        fOUT.write("def triggerBin(pt, efficiency, uncertainty):\n")
        fOUT.write("    return cms.PSet(\n")
        fOUT.write("        pt = cms.double(pt),\n")
        fOUT.write("        efficiency = cms.double(efficiency),\n")
        fOUT.write("        uncertaintyPlus = cms.double(uncertaintyPlus),\n")
        fOUT.write("        uncertaintyMinus = cms.double(uncertaintyMinus)\n")
        fOUT.write("    )\n\n")

        #print "check self.namedSelection",self.namedSelection

        for ns in self.namedSelection:
            name      = ns[0]
            selection = ns[1]

            #fOUT.write("\ntauLegEfficiency_"+name+" = cms.untracked.PSet(\n")
            fOUT.write("\n"+self.title+"_"+name+" = cms.untracked.PSet(\n")

            fOUT.write("    # The selected triggers for the efficiency. If one trigger is\n")
            fOUT.write("    # given, the parametrization of it is used as it is (i.e.\n")
            fOUT.write("    # luminosity below is ignored). If multiple triggers are given,\n")
            fOUT.write("    # their parametrizations are used weighted by the luminosities\n")
            fOUT.write("    # given below.\n")
            fOUT.write("    # selectTriggers = cms.VPSet(\n")
            fOUT.write("    #     cms.PSet(\n")
            fOUT.write("    #         trigger = cms.string(\"HLT_IsoPFTau35_Trk20_EPS\"),\n")
            fOUT.write("    #         luminosity = cms.double(0)\n")
            fOUT.write("    #     ),\n")
            fOUT.write("    # ),\n")
            fOUT.write("    # The parameters of the trigger efficiency parametrizations,\n")
            fOUT.write("    # looked dynamically from TriggerEfficiency_cff.py\n\n")

            fOUT.write("    # Offline selection: "+selection+"\n\n")

            fOUT.write("    # Used input: "+self.inString+"\n\n")

            fOUT.write("    dataParameters = cms.PSet(\n")
            for r in self.ranges:
                if r.name == name:
                    self.writeParameters(fOUT,r.label,r.runrange,r.lumi,r.eff)
            fOUT.write("    ),\n")

            fOUT.write("    mcParameters = cms.PSet(\n")
            for mc in self.mcs:
                #print "check write mc",mc.name,name
                if mc.name == name:
                    self.writeMCParameters(fOUT,mc.label,mc.eff)
            fOUT.write("    ),\n")

            fOUT.write("    dataSelect = cms.vstring(),\n")
            fOUT.write("    mcSelect = cms.string(\""+self.mcs[0].label+"\"),\n")
            fOUT.write("    mode = cms.untracked.string(\"disabled\") # dataEfficiency, scaleFactor, disabled\n")
            fOUT.write(")\n")

            self.writeJSON(ns)

    def writeParameters(self,fOUT,label,runrange,lumi,eff):
        runrange_re = re.compile("(?P<firstRun>(\d+))-(?P<lastRun>(\d+))")
        match = runrange_re.search(runrange)
        if not match:
            print "Run range not valid",runrange
            sys.exit()

        fOUT.write("        # "+label+"\n")
        fOUT.write("        runs_"+match.group("firstRun")+"_"+match.group("lastRun")+" = cms.PSet(\n")
        fOUT.write("            firstRun = cms.uint32("+match.group("firstRun")+"),\n")
        fOUT.write("            lastRun = cms.uint32("+match.group("lastRun")+"),\n")
        fOUT.write("            luminosity = cms.double(%s), # 1/pb\n"%lumi)
        self.writeBins(fOUT,label,eff)
        fOUT.write("        ),\n")

    def writeMCParameters(self,fOUT,label,eff):
        fOUT.write("        "+label+" = cms.PSet(\n")
        self.writeBins(fOUT,label,eff,ihisto=1)
        fOUT.write("        ),\n")

    def writeBins(self,fOUT,label,eff,ihisto=0):
        fOUT.write("            bins = cms.VPSet(\n")
        nbins = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetN()
        for i in range(1,nbins):
            binLowEdge = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetX()[i]
            binLowEdge-= eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorX(i)
            efficiency = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetY()[i]
#            error      = max(eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorYhigh(i),eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorYlow(i))
            errorPlus = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorYhigh(i)
            errorMinus = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorYlow(i)
#            efficiency = eff.ratios[0].getRootGraph().GetY()[i]
#            error = max(eff.ratios[0].getRootGraph().GetErrorYhigh(i),eff.ratios[0].getRootGraph().GetErrorYlow(i))
            fOUT.write("                triggerBin("+str(binLowEdge)+", "+str(efficiency)+", "+str(errorPlus)+", "+str(errorMinus)+"),\n")
        #print "check writeBins",nbins,len(self.bins)
        if nbins < len(self.bins):
            for i in range(nbins,len(self.bins)):
                #print self.bins[i],efficiency,error
                fOUT.write("                triggerBin("+str(self.bins[i])+", "+str(efficiency)+", "+str(errorPlus)+", "+str(errorMinus)+"), # duplicated bin\n")
        fOUT.write("            ),\n")

    def findBins(self,eff):
        nbins = eff.histoMgr.getHistos()[0].getRootHisto().GetN()
        for i in range(nbins):
            binLowEdge = eff.histoMgr.getHistos()[0].getRootHisto().GetX()[i]
            binLowEdge-= eff.histoMgr.getHistos()[0].getRootHisto().GetErrorX(i)
            if binLowEdge not in self.bins:
                self.bins.append(binLowEdge)

    def timeStamp(self):
        import datetime
        time = datetime.datetime.now().ctime()
        return time

    def sysError(self):
        ihisto = 0
        ranges = self.removeDuplicateRunRanges(self.ranges)
        lumiSum = 0
        effSum = []
        for i in range(ranges[0].eff.histoMgr.getHistos()[ihisto].getRootHisto().GetN()):
            effSum.append(0)

        for r in ranges:
            lumiSum += r.lumi
            print "RunRange",r.runrange
            print "    Lumi",r.lumi
            eff = r.eff
            for i in range(eff.histoMgr.getHistos()[ihisto].getRootHisto().GetN()):
                binLowEdge = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetX()[i]
                binLowEdge-= eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorX(i)
                efficiency = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetY()[i]
                error      = max(eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorYhigh(i),eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorYlow(i))
                effSum[i]+= r.lumi*r.lumi*error*error
                print "    ",binLowEdge,efficiency,error

        print
        print "Summed lumi",lumiSum
        print "Summed uncertainty"
        for i in range(len(effSum)):
            binLowEdge = ranges[0].eff.histoMgr.getHistos()[ihisto].getRootHisto().GetX()[i]
            binLowEdge-= ranges[0].eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorX(i)
            print "    ",binLowEdge,sqrt(effSum[i])/lumiSum

    def removeDuplicateRunRanges(self,ranges):
        returnRanges = []
        runMin = 999999999
        runMax = 0
        runrange_re = re.compile("(?P<firstRun>(\d+))-(?P<lastRun>(\d+))")
        for r in ranges:
            match = runrange_re.search(r.runrange)
            if match:
                firstRun = match.group("firstRun")
                lastRun = match.group("lastRun")
                if not(firstRun < runMax and firstRun > runMin) and not(lastRun > runMin and lastRun < runMax):
                    if firstRun < runMin:
                        runMin = firstRun
                    if lastRun > runMax:
                        runMax = lastRun
                    returnRanges.append(r)
        return returnRanges

    def writeJSON(self,fName): #Soti

#        name      = namedSelection[0]
#        selection = namedSelection[1]
#        selection = selection.replace("&&","\n                   &&")

#        fName = os.path.join(fileName)
        fOUT = open(fName,"w")
        fOUT.write("{\n")
        time = self.timeStamp()
        fOUT.write("  \"_timestamp\":   \"Generated on "+time+" by HiggsAnalysis/NtupleAnalysis/src/SystTopBDT/work/PythonWriter.py\",\n")
        fOUT.write("  \"_rootVersion\": \"%s\",\n"%self.rootVersion)
#        fOUT.write("  \"_statOption\" : %s,\n"%self.statOption)
#        fOUT.write("  \"_selection\"  : \""+selection+"\",\n")
#        fOUT.write("  \"_input\"      : \""+self.inString+"\",\n")

        fOUT.write("  \"dataParameters\": {\n")
        runrange_re = re.compile("(?P<firstRun>(\d+))-(?P<lastRun>(\d+))")
        comma = ","
        subranges = []
#        for r in self.ranges:
#            if r.name == name:
#                subranges.append(r)
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
                comma = ""
#            if mc.name == name:
            fOUT.write("      \""+mc.label+"\": {\n")
            self.writeJSONBins(fOUT,mc.label,mc.eff)
            fOUT.write("      }"+comma+"\n")
        fOUT.write("  }\n")

        fOUT.write("}\n")
        fOUT.close()

    def writeParametersJSON(self,fOUT,label,runrange,lumi,eff):
        runrange_re = re.compile("(?P<firstRun>(\d+))-(?P<lastRun>(\d+))")
        match = runrange_re.search(runrange)
        if not match:
            print "Run range not valid",runrange
            sys.exit()

        fOUT.write("      \"era\":"+label+",\n")
        fOUT.write("      \"runs_"+match.group("firstRun")+"_"+match.group("lastRun")+"\": {\n")
        fOUT.write("          \"firstRun\"  :"+match.group("firstRun")+",\n")
        fOUT.write("          \"lastRun\"   :"+match.group("lastRun")+",\n")
        fOUT.write("          \"luminosity\": %s,\n"%lumi)
        self.writeBinsJSON(fOUT,label,eff)
        fOUT.write("      }\n")

    def writeJSONBins(self,fOUT,label,eff):
        fOUT.write("          \"bins\" : [\n")
        nbins = eff.GetN()
#        nbins = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetN()
        comma = ","
        for i in range(0,nbins):
            if i == nbins-1:
                comma = ""
            binLowEdge = eff.GetX()[i]
            binLowEdge-= eff.GetErrorXlow(i)
            efficiency = eff.GetY()[i]
            errorPlus  = eff.GetErrorYhigh(i)
            errorMinus = eff.GetErrorYlow(i)
#            binLowEdge = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetX()[i]
#            binLowEdge-= eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorX(i)
#            efficiency = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetY()[i]
#            errorPlus = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorYhigh(i)
#            errorMinus = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorYlow(i)

            fOUT.write("             {\n")
            fOUT.write("               \"pt\"              :"+str(binLowEdge)+",\n")
            fOUT.write("               \"efficiency\"      :"+str(efficiency)+",\n")
            fOUT.write("               \"uncertaintyPlus\" :"+str(errorPlus)+",\n")
            fOUT.write("               \"uncertaintyMinus\":"+str(errorMinus)+"\n")
            fOUT.write("             }%s\n"%comma)

        if nbins < len(self.bins):
            comma = ","
            for i in range(nbins,len(self.bins)):
                #print self.bins[i],efficiency,error                                                       
                if i == len(self.bins)-1:
                    comma = ""
                fOUT.write("             {\n")
                fOUT.write("               \"pt\"              :"+str(self.bins[i])+",\n")
                fOUT.write("               \"efficiency\"      :"+str(efficiency)+",\n")
                fOUT.write("               \"uncertaintyPlus\" :"+str(errorPlus)+",\n")
                fOUT.write("               \"uncertaintyMinus\":"+str(errorMinus)+"\n")
                fOUT.write("             }\n")

        fOUT.write("          ]\n")

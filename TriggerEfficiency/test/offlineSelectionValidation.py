#!/usr/bin/env python

import sys
import ROOT
from array import array

varexp = "PFTauPt>>hnumpt"
verbose = False
#verbose = True

varname = ""
#varname = "MuonTauInvMass"

class Data:
    def __init__(self,name,selection,data,var):
        self.name      = name
	self.selection = selection
	self.data      = data
	self.var       = var

class Counters:
#    def __init__(self,names,values);
    def __init__(self,histo):
        self.names  = []
        self.values = []

        for i in range(1,histo.GetNbinsX()+1):
            self.append(histo.GetXaxis().GetBinLabel(i),histo.GetBinContent(i))

    def append(self,name,value):
        self.names.append(name)
        self.values.append(value)


def usage():
    print
    print "### Usage:   ",sys.argv[0],"<root file1> <root file2>"
    print "### Example: ",sys.argv[0],"tteffAnalysis-hltpftau-hpspftau-highpurity_noTauID.root tteffAnalysis-hltpftau-hpspftau-highpurity_vloose.root"
    print
    sys.exit()

def main():

    if len(sys.argv) < 3:
	usage() 

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    name1,name2 = difference(file1,file2)

    data1,counter1 = analyse(file1)
    data2,counter2 = analyse(file2)

    printComparison(data1,counter1,name1,data2,counter2,name2)

def analyse(fname):

    noSelection = ""

    MuIsolation = "(MuonPFIsoChargedPt + MuonPFIsoNeutralEt + MuonPFIsoGammaEt)/MuonPt < 0.1"
    MuFilter = "Sum$(%s) == 1"%MuIsolation
    VetoMuonsHighPurity = "MuonPt > 15"
    VetoMuonsHighPurity+= "&& abs(MuonEta) < 2.4"
    VetoMuonsHighPurity+= "&& MuonIsGlobalMuon"
    VetoMuonsHighPurity+= "&& (MuonPFIsoChargedPt + MuonPFIsoNeutralEt + MuonPFIsoGammaEt)/MuonPt < 0.15"
    VetoMuFilter = "Sum$(%s) <= 1"%VetoMuonsHighPurity
    TauSelection = "PFTauLeadChargedHadrCandPt > 20"
    TauSelection+= "&& PFTau_decayModeFinding > 0.5"
    TauSelection+= "&& PFTauProng == 1"
    TauSelection+= "&& PFTau_againstMuonTight > 0.5"
    TauSelection+= "&& PFTau_againstElectronTightMVA3 > 0.5"
    TauSelection+= "&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5"
    TauFilter = "Sum$(%s) == 1"%TauSelection
    HighPurityMuTauFilter = MuFilter+"&&"+VetoMuFilter+"&&"+TauFilter

    offlineSelectionHPlusBase = "PFTauPt > 20 && abs(PFTauEta) < 2.1"
    offlineSelectionHPlusBase += "&& PFTauLeadChargedHadrCandPt > 20"
    offlineSelectionHPlusBase += "&& PFTauProng == 1"
    offlineSelectionHPlusBase += "&& PFTau_againstMuonTight > 0.5" # selection before V53_2 pattuples                           
##    offlineSelectionHPlusBase += "&& PFTau_againstMuonTight2 > 0.5" # selection after V53_2 pattuples                          
#    offlineSelectionHPlusBase += "&& MuonTauInvMass < 80"

    offlineSelectionMediumMVA3 = offlineSelectionHPlusBase
    offlineSelectionMediumMVA3+= "&& PFTau_againstElectronTightMVA3 > 0.5"
#    offlineSelectionMediumMVA3+= "&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5"

    offlineSelectionMediumMVA3b = offlineSelectionMediumMVA3
    offlineSelectionMediumMVA3b += "&& MuonTauInvMass < 80"
    ##############

    offlineSelections = []
    offlineSelections.append(namedselection("No selection",noSelection))
    offlineSelections.append(namedselection("High purity muTau selection",HighPurityMuTauFilter))
#    offlineSelections.append(namedselection("MediumMVA3",offlineSelectionMediumMVA3))
#    offlineSelections.append(namedselection("MediumMVA3b",offlineSelectionMediumMVA3b))


    data = []

    fIN = ROOT.TFile.Open(fname,"R")
    tree = fIN.Get("TTEffTree")
    counters = Counters(fIN.Get("Counters"))
    counters.append("TTEffTree",tree.GetEntries())

    if tree.GetEntries() == 0:
	print "TTree in",fname,"has 0 entries!"
	sys.exit()

    for offlineSelection in offlineSelections:
	#print "check",offlineSelection[0],offlineSelection[1]

        tree.Draw(">>list",offlineSelection[1],"entrylist")
        entrylist = ROOT.gDirectory.Get("list")

#	tmpTree = tree.CopyTree(offlineSelection[1])
#	Npassed = tmpTree.GetEntries()
        Npassed = entrylist.GetN()

        eventList = [] #event:run:lumi
	varlist   = [] 
        event = array('i',[0])
        run   = array('i',[0])
        lumi  = array('i',[0])
	var   = array('f',[0])
    
        tree.SetBranchAddress("event",event)
        tree.SetBranchAddress("run",run)
        tree.SetBranchAddress("lumi",lumi)

	if len(varname) > 0:
	    tree.SetBranchAddress(varname,var)

        for i in range(0,Npassed):
            j = entrylist.GetEntry(i)
            tree.GetEntry(j)
#        for i in range(0,Npassed):
#	    tmpTree.GetEntry(i)
	    eventList.append("%s:%s:%s"%(run[0],lumi[0],event[0]))
	    if len(varname) > 0:
		#print "check",var[0]
                varlist.append(varname+"=%d"%var[0])

	data.append(Data(fname.replace(".root",""),offlineSelection[0],eventList,varlist))

    fIN.Close()

    return data,counters

def printComparison(data1,counter1,name1,data2,counter2,name2):

    if not len(data1) == len(data2):
	print "Warning, data1 size different from data2 size"
	sys.exit()
####    if not len(counter1.names) == len(counter2.names):
####        print "Warning, counter1 size different from counter2 size"
####        sys.exit()

    pos1 = max(35,len("    Events found in "+name1)+1,len("    Events found in "+name2)+1)
    pos2 = max(10,len(name1)+1)
    counterNames = "Counters                           "
    while len(counterNames) < pos1:
        counterNames+=" "
    counterNames+=name1
    while len(counterNames) < pos1+pos2:
        counterNames+=" "
    counterNames+=name2
    print
    print counterNames
    print
    for i in range(max(len(counter1.names),len(counter2.names))):
	if len(counter1.names) > len(counter2.names):
	    counterName = counter1.names[i]
	    counter1Value = str(counter1.values[i])
	    counter2Value = "-"
	    for j in range(len(counter2.names)):
		if counter2.names[j] == counterName:
		    counter2Value = str(counter2.values[j])
		    break
	else:
	    counterName = counter2.names[i]
            counter2Value = str(counter2.values[i])
	    counter1Value = "-"
            for j in range(len(counter1.names)):
                if counter1.names[j] == counterName:
                    counter1Value = str(counter1.values[j])
                    break

        binLabel = "    "+counterName
        while len(binLabel) < pos1:
            binLabel += " "
        sys.stdout.write(binLabel)
        counter1Content = counter1Value
        while len(counter1Content) < pos2:
            counter1Content += " "
        sys.stdout.write(counter1Content)
        sys.stdout.write(counter2Value)
        sys.stdout.write("\n")

    for i in range(0,len(data1)):
	print
	print data1[i].selection

        data1sub = subsection(data1[i].data,data2[i].data)
        data2sub = subsection(data2[i].data,data1[i].data)

        nevLine = "    Number of events   "
        while len(nevLine) < pos1:
            nevLine += " "
        nevLine += str(len(data1[i].data))
        while len(nevLine) < pos1+pos2:
            nevLine += " "
        nevLine += str(len(data2[i].data))
        print nevLine




        line3 = "    but not in "+name2
        while len(line3) < pos1:
            line3 += " "
        print
        print "    Events found in",name1
        print line3+str(len(data1sub))
        if verbose:
            if len(data1sub) > 0:
                print "        run:lumi:event"
                for j,data in enumerate(data1[i].data):
                    sys.stdout.write("        "+data)
                    if len(varname) > 0:
                        sys.stdout.write(" %s"%data1[i].var[j])
                        if data in data1sub:
                            sys.stdout.write("  Not found")
                    sys.stdout.write("\n")
                print
                print "       List of events not found: ("+str(len(data1sub))+")"
                for data in data1sub:
                    sys.stdout.write(data+",")
                sys.stdout.write("\n")
            else:
        	print "        None"
        line4 = "    but not in "+name1
        while len(line4) < pos1+pos2:
            line4 += " "
        print
        print "    Events found in",name2
        print line4+str(len(data2sub))
        if verbose:
            if len(data2sub) > 0:
                print "        run:lumi:event"                                       
                for j,data in enumerate(data2[i].data):                              
                    sys.stdout.write("        "+data)                                
                    if len(varname) > 0:                                             
                        sys.stdout.write(" %s"%data2[i].var[j])                      
                    if data in data2sub:                                             
                        sys.stdout.write("  Not found")                              
                    sys.stdout.write("\n")                                           
                print                                                                
                print "        List of events not found: ("+str(len(data2sub))+")"
                sys.stdout.write("        ")                                         
                for i,data in enumerate(data2sub):                                   
                    sys.stdout.write(data)                                           
                    if i < len(data2sub)-1:                                          
                        sys.stdout.write(",")                                        
                    if i%8 == 7:                                                     
                        sys.stdout.write("\n        ")                               
                sys.stdout.write("\n")
            else:
                print "        None"

def subsection(data1,data2):
    notFound = []
    for data in data1:
	if not data in data2:
	    notFound.append(data)
    return notFound

def namedselection(name,selection):
    namedSelection = []
    namedSelection.append(name)
    namedSelection.append(selection)
    return namedSelection

def difference(name1,name2):
    s1list = name1.split('/')
    s2list = name2.split('/')
    newS1list = []
    newS2list = []
    for i in range(len(s1list)):
        if not s1list[i] == s2list[i]:
            newS1list.append(s1list[i])
            newS2list.append(s2list[i])

    newS1list = newS1list[0].split('_')
    newS2list = newS2list[0].split('_')
    for i in range(len(newS1list)):
        if not newS1list[i] == newS2list[i]:
            newname1 = newS1list[i]
            newname2 = newS2list[i]

    return newname1,newname2

if __name__ == "__main__":
    main()

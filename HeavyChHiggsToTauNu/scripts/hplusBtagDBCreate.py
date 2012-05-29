#!/usr/bin/env python

import os,sys,re

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

analysis = "signalAnalysis"
counters = analysis+"Counters/weighted"

treeDraw = dataset.TreeDraw(analysis+"/tree", weight="weightPileup")

class BTagDBCreator :
    def __init__(self,algo):
	self.setAlgorithm(algo)

    def setMultiCrabDir(self, name):

        dirs = []
        dirs.append(name)
                
        datasets = dataset.getDatasetsFromMulticrabDirs(dirs,counters=counters)
	datasets.loadLuminosities()

	plots.mergeRenameReorderForDataMC(datasets)

	self.ds = datasets.getDataset(self.datasetName)

    def setMC(self,name):
	self.datasetName = name

    def setAlgorithm(self,name):
	self.algo = name
	self.algoAcronym = "BTAG"
	if name == "TrackCountingHigheffLoose":
	    self.algoAcronym += "TCHEL"

    def setEtaBinning(self,N,min,max):
	self.EtaBinN   = N
	self.EtaBinMin = min
	self.EtaBinMax = max

    def setPtBinning(self,binlist):
	self.PtBins = binlist

    def setDiscriminatorCut(self,value):
	self.discriminatorCut = value

    def getEfficiency(self,etamin,etamax,ptmin,ptmax):

	den_selection = "jets_p4.Pt()>"+str(ptmin)
	den_selection+= "&&jets_p4.Pt()<="+str(ptmax)
	den_selection+= "&&fabs(jets_p4.Eta())>"+str(etamin)
	den_selection+= "&&fabs(jets_p4.Eta())<="+str(etamax)

	num_selection = den_selection + "&&jets_btag>" + str(self.discriminatorCut)

	bin = "(1,"+str(ptmin)+","+str(ptmax)+")"
	den = self.ds.getDatasetRootHisto(treeDraw.clone(varexp="jets_p4.Pt()>>dist1"+bin, selection=den_selection)).getHistogram()
	num = self.ds.getDatasetRootHisto(treeDraw.clone(varexp="jets_p4.Pt()>>dist2"+bin, selection=num_selection)).getHistogram()

#	print "check",den.GetBinContent(1),num.GetBinContent(1)
    	eff = num.Clone()
    	eff.Divide(den)

#	print "eff=",eff.GetBinContent(1),eff.GetBinError(1)
	return eff.GetBinContent(1),eff.GetBinError(1)

    def createTextDB(self):
	self.fOUTName = self.algoAcronym + "_hplusBtagDB_" + self.datasetName + ".txt"

	fOUT = open(self.fOUTName,"w")
        fOUT.write(self.algo+"\n")
	fOUT.write(str(self.discriminatorCut)+"\n")
	fOUT.write("PerformancePayloadFromTable\n")
	fOUT.write("2\n")
	fOUT.write("2\n")
	fOUT.write("1001 1002\n");
#        fOUT.write("1 2\n");
	fOUT.write("5 2\n");

	deta = (self.EtaBinMax - self.EtaBinMin)/self.EtaBinN
        etamin = self.EtaBinMin
	for i in range(self.EtaBinN):
	    etamax = etamin + deta

	    for j in range(len(self.PtBins)-1):
		ptmin = self.PtBins[j]
		ptmax = self.PtBins[j+1]

		eff,err = self.getEfficiency(etamin,etamax,ptmin,ptmax)
		line = self.format(etamin)
		line+= self.format(etamax)
		line+= self.format(ptmin)
		line+= self.format(ptmax)
		line+= self.format(eff,True)
		line+= self.format(err,True)
		line+= "\n"

		fOUT.write(line)

		ptmin = ptmax

	    etamin = etamax
		
	fOUT.close()
	os.system("cat "+self.fOUTName)

    def format(self,value,dec=False):
	if dec:
	    str_value = "%.2f"%value
	else:
	    str_value = str(value)
	while len(str_value) < 9:
	    str_value+=" "
	return str_value


    def Print(self):
	print 
	print "Btagging DB creation described in"
	print "https://twiki.cern.ch/twiki/bin/view/CMS/BtagPerformanceDBV2\n"
	print "    Table",self.fOUTName,"created"
	print "    DB",self.fOUTName.replace(".txt",".db"),"created \n"
	print " cp DBs/* HiggsAnalysis/HeavyChHiggsToTauNu/data/*"
	print " cp Btag_*.py Pool_*.py HiggsAnalysis/HeavyChHiggsToTauNu/python"
	print 

    def createDB(self):
	self.createCmsRunCfg("createDB.csh")
	self.runCfg()

    def createCmsRunCfg(self,name):

	self.csh_script = name

    	path_re = re.compile("(?P<path>(^\S+?)):")
	rm_re = re.compile("rm -f (?P<file>(\S+$))")
	online_re = re.compile("Online")

	searchPath = os.environ['SRT_CMSSW_SEARCH_PATH_SCRAMRTDEL']
	match = path_re.search(searchPath)
	if match :
	    path = os.path.join(match.group("path"),"RecoBTag/PerformanceDB/test/process")

            fIN = open(os.path.join(path,"makeSingle.csh"))
            fOUT = open(name,"w")

            mkdirNotDone = True

            for line in fIN:

                if len(line) < 5 and mkdirNotDone:
                    fOUT.write("\n"+"if ( ! -d DBs ) mkdir DBs\n")
                    mkdirNotDone = False

                line = line.replace("test/","")
#               line = line.replace("DBs/","")

                line = line.replace("templates/",os.path.join(path,"templates/"))
  
                rm_match = rm_re.search(line)
                if rm_match:
                    line = line.replace("rm -f","if ( -f "+rm_match.group("file")+" ) rm -f")

#                online_match = online_re.search(line)
#                if online_match:
#                    line = "#"+line

                fOUT.write(line)

            fOUT.close()
            fIN.close()

    def runCfg(self):
	command = "csh "
	command+= self.csh_script
	command+= " " + self.fOUTName
	command+= " " + self.fOUTName.replace(".txt","")
	print command
	os.system(command)

def main():

    if len(sys.argv) < 2:
        usage()

    newDB = BTagDBCreator("TrackCountingHigheffLoose")
    newDB.setMC("TTJets")
    newDB.setMultiCrabDir(sys.argv[1])
    newDB.setEtaBinning(10,0,2.5)
    newDB.setPtBinning([30,40,50,60,70,80,90,100,120,140,230])
    newDB.setDiscriminatorCut(1.7)
    newDB.createTextDB()
    newDB.createDB()
    newDB.Print()

def usage():
    print "\n"
    print "### Usage:   hplusBtagDBCreate.py <multicrab dir>\n"
    print "\n"
    sys.exit()


if __name__ == "__main__":
    main()

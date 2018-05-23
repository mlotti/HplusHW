#!/usr/bin/env python
'''
INSTRUCTIONS:
The required minimum input is a multiCRAB directory with at least one dataset. If successfull
a pseudo multiCRAB with name "analysis_YYMMDD_HHMMSS/" will be created, inside which each
dataset has its own directory with the results (ROOT files with histograms). These can be later
used as input to plotting scripts to get the desired results.


PROOF:
Enable only if your analysis is CPU-limited (e.g. limit calculation) With one analyzer at
a time most probably you are I/O -limited. The limit is how much memory one process is using.


USAGE:
./run.py -m <multicrab_directory> -j <numOfCores> -i <DatasetName>
or
./run.py -m <multicrab_directory> -n 10 -e "Keyword1|Keyword2|Keyword3"

Example:
./run.py -m /multicrab_CMSSW752_Default_07Jan2016/
./run.py -m multicrab_CMSSW752_Default_07Jan2016/ -j 16
./run.py -m multicrab_Hplus2tbAnalysis_v8014_20160818T1956 -n 1000 -e QCD
./run.py -m <multicrab-directory> -e TT_extOB
./run.py -m <multicrab_directory> -n 10 -e "QCD_bEnriched_HT300|2016|ST_"

ROOT:
The available ROOT options for the Error-Ignore-Level are (const Int_t):
        kUnset    =  -1
        kPrint    =   0
        kInfo     =   1000
        kWarning  =   2000
        kError    =   3000
        kBreak    =   4000

HistoLevel:
For the histogramAmbientLevel each DEEPER level is a SUBSET of the rest. 
For example "kDebug" will include all kDebug histos but also kInformative, kVital, kSystematics, and kNever.  
Setting histogramAmbientLevel=kSystematics will include kSystematics AND kNever.
    1. kNever = 0,
    2. kSystematics,
    3. kVital,
    4. kInformative,
    5. kDebug,
    6. kNumberOfLevels
'''

#================================================================================================
# Imports
#================================================================================================
import sys
from optparse import OptionParser
import time

from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer
from HiggsAnalysis.NtupleAnalysis.AnalysisBuilder import AnalysisBuilder


import ROOT
    
#================================================================================================
# Options
#================================================================================================
prefix      = "SystTopBDT"
postfix     = ""
dataEras    = ["2016"]
searchModes = ["80to1000"]

ROOT.gErrorIgnoreLevel = 0 


#================================================================================================
# Function Definition
#================================================================================================
def Verbose(msg, printHeader=False):
    if not opts.verbose:
        return

    if printHeader:
        print "=== run.py:"

    if msg !="":
        print "\t", msg
    return


def Print(msg, printHeader=True):
    if printHeader:
        print "=== run.py:"

    if msg !="":
        print "\t", msg
    return


#================================================================================================
# Setup the main function
#================================================================================================
def main():

    # Save start time (epoch seconds)
    tStart = time.time()
    Verbose("Started @ " + str(tStart), True)

    # Require at least two arguments (script-name, path to multicrab)      
    if len(sys.argv) < 2:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        print __doc__
        sys.exit(0)
    else:
        pass
        

    # ================================================================================================
    # Setup the process
    # ================================================================================================
    completeList = GetDatasetCompleteList()
    whiteList    = GetDatasetWhitelist(opts)
    blackList    = GetDatasetBlackList(completeList, whiteList)
    maxEvents = {}
    for d in whiteList:
        #maxEvents[d] = 100
        maxEvents[d] = -1
    process = Process(prefix, postfix, maxEvents)
                
    # ================================================================================================
    # Add the datasets (according to user options)
    # ================================================================================================
    if (opts.includeOnlyTasks):
        Print("Adding only dataset %s from multiCRAB directory %s" % (opts.includeOnlyTasks, opts.mcrab))
        process.addDatasetsFromMulticrab(opts.mcrab, includeOnlyTasks=opts.includeOnlyTasks)
    elif (opts.excludeTasks):
        Print("Adding all datasets except %s from multiCRAB directory %s" % (opts.excludeTasks, opts.mcrab))
        Print("If collision data are present, then vertex reweighting is done according to the chosen data era (era=2015C, 2015D, 2015) etc...")
        process.addDatasetsFromMulticrab(opts.mcrab, excludeTasks=opts.excludeTasks)
    else:
        myBlackList = []
        myBlackList.extend(blackList)
        Verbose("Adding all datasets from multiCRAB directory %s" % (opts.mcrab))
        Verbose("If collision data are present, then vertex reweighting is done according to the chosen data era (era=2015C, 2015D, 2015) etc...")
        regex =  "|".join(myBlackList)
        if len(whiteList)>0:
            process.addDatasetsFromMulticrab(opts.mcrab, includeOnlyTasks="|".join(whiteList))
        elif len(myBlackList)>0:
            process.addDatasetsFromMulticrab(opts.mcrab, excludeTasks=regex)
        else:
            process.addDatasetsFromMulticrab(opts.mcrab)



    # ================================================================================================
    # Overwrite Default Settings  
    # ================================================================================================
    from HiggsAnalysis.NtupleAnalysis.parameters.jetTriggers import allSelections
    allSelections.verbose = opts.verbose
    allSelections.histogramAmbientLevel = opts.histoLevel
    import HiggsAnalysis.NtupleAnalysis.parameters.scaleFactors as scaleFactors
    #==========================
    #  Systematics selections
    #==========================


    # BDT MisID SF
    MisIDSF = PSet(
        MisIDSFJsonName = "Efficiency_SystBDT_CR2.json", # For Fake TT:  Efficiency_SystBDT_CR1.json",   # For QCD, EWK & SingleTop:  Efficiency_SystBDT_CR2.json
        ApplyMisIDSF    = False,
        )
    scaleFactors.assignMisIDSF(MisIDSF, "nominal", MisIDSF.MisIDSFJsonName)
    allSelections.MisIDSF = MisIDSF

    allSelections.SystTopBDTSelection.MiniIsoCutValue    = 0.1
    allSelections.SystTopBDTSelection.MiniIsoInvCutValue = 0.1
    allSelections.SystTopBDTSelection.METCutValue        = 50.0
    allSelections.SystTopBDTSelection.METInvCutValue     = 20.0

    # Muon
    allSelections.MuonSelection.muonPtCut = 30

    # Jets
    allSelections.JetSelection.numberOfJetsCutValue = 4
    allSelections.JetSelection.jetPtCuts = [40.0, 40.0, 40.0, 30.0]

    # Trigger
    allSelections.Trigger.triggerOR = ["HLT_Mu50"]

    # Bjets
    allSelections.BJetSelection.jetPtCuts = [40.0, 30.0]
    allSelections.BJetSelection.numberOfBJetsCutValue = 2

    #Top
    #allSelections.TopSelectionBDT.WeightFile             = "BDTG_DeltaR0p3.weights.xml"
    
    # allSelections.BjetSelection.triggerMatchingApply = True
    # allSelections.TopSelection.ChiSqrCutValue = 100.0
    # allSelections.BJetSelection.numberOfBJetsCutValue = 0
    # allSelections.BJetSelection.numberOfBJetsCutDirection = "=="

    
    # ================================================================================================
    # Add Analysis Variations
    # ================================================================================================
    # selections = allSelections.clone()
    # process.addAnalyzer(prefix, Analyzer(prefix, config=selections, silent=False) ) #trigger passed from selections


    # ================================================================================================
    # Command Line Options
    # ================================================================================================ 
    # from HiggsAnalysis.NtupleAnalysis.parameters.signalAnalysisParameters import applyAnalysisCommandLineOptions
    # applyAnalysisCommandLineOptions(sys.argv, allSelections)

    
    #================================================================================================
    # Build analysis modules
    #================================================================================================
    PrintOptions(opts)
    builder = AnalysisBuilder(prefix,
                              dataEras,
                              searchModes,
                              usePUreweighting       = opts.usePUreweighting,
                              useTopPtReweighting    = opts.useTopPtReweighting,
                              doSystematicVariations = opts.doSystematics,
                              analysisType="HToTB")

    # Add variations (e.g. for optimisation)
    # builder.addVariation("METSelection.METCutValue", [100,120,140])
    # builder.addVariation("AngularCutsBackToBack.workingPoint", ["Loose","Medium","Tight"])
    # builder.addVariation("BJetSelection.triggerMatchingApply", [False])
    # builder.addVariation("TopSelection.ChiSqrCutValue", [5, 10, 15, 20])

    # Build the builder
    builder.build(process, allSelections)

    # ================================================================================================
    # Example of adding an analyzer whose configuration depends on dataVersion
    # ================================================================================================
    #def createAnalyzer(dataVersion):
    #a = Analyzer("ExampleAnalysis")
    #if dataVersion.isMC():
    #a.tauPtCut = 10
    #else:
    #a.tauPtCut = 20
    #return a
    #process.addAnalyzer("test2", createAnalyzer)

    
    # ================================================================================================
    # Pick events
    # ================================================================================================
    #process.addOptions(EventSaver = PSet(enabled = True,pickEvents = True))
    # ================================================================================================
    # Run the analysis
    # ================================================================================================
    # Run the analysis with PROOF? You can give proofWorkers=<N> as a parameter
    if opts.jCores:
        Print("Running process with PROOF (proofWorkes=%s)" % ( str(opts.jCores) ) )
        process.run(proof=True, proofWorkers=opts.jCores)
    else:
        Print("Running process")
        process.run()

    # Print total time elapsed
    tFinish = time.time()
    dt      = int(tFinish) - int(tStart)
    days    = divmod(dt,86400)      # days
    hours   = divmod(days[1],3600)  # hours
    mins    = divmod(hours[1],60)   # minutes
    secs    = mins[1]               # seconds
    Print("Total elapsed time is %s days, %s hours, %s mins, %s secs" % (days[0], hours[0], mins[0], secs), True)
    return

#================================================================================================
def GetDatasetBlackList(completeList, whiteList):
    myBlacklist = []
    for d in completeList:
        if d in whiteList:
            continue
        myBlacklist.append(d)
    return myBlacklist
            
def GetDatasetCompleteList():
    myCompleteList = []
    myCompleteList.append("SingleMuon_Run2016B_03Feb2017_ver2_v2_273150_275376")
    myCompleteList.append("SingleMuon_Run2016C_03Feb2017_v1_275656_276283")
    myCompleteList.append("SingleMuon_Run2016D_03Feb2017_v1_276315_276811")
    myCompleteList.append("SingleMuon_Run2016E_03Feb2017_v1_276831_277420")
    #
    myCompleteList.append("SingleMuon_Run2016F_03Feb2017_v1_277932_278800")
    myCompleteList.append("SingleMuon_Run2016F_03Feb2017_v1_278801_278808")
    myCompleteList.append("SingleMuon_Run2016G_03Feb2017_v1_278820_280385")
    myCompleteList.append("SingleMuon_Run2016H_03Feb2017_ver2_v1_281613_284035")
    myCompleteList.append("SingleMuon_Run2016H_03Feb2017_ver3_v1_284036_284044")

    myCompleteList.append("TT")
    #
    myCompleteList.append("TT_GluonMoveCRTune")
    #
    myCompleteList.append("TT_QCDbasedCRTune_erdON")
    myCompleteList.append("TT_QCDbasedCRTune_erdON_ext1")
    #
    myCompleteList.append("TT_TuneCUETP8M2T4down")
    myCompleteList.append("TT_TuneCUETP8M2T4down_ext1")
    myCompleteList.append("TT_TuneCUETP8M2T4up")
    myCompleteList.append("TT_TuneCUETP8M2T4up_ext1")
    myCompleteList.append("TT_TuneEE5C")
    myCompleteList.append("TT_TuneEE5C_ext2")
    myCompleteList.append("TT_TuneEE5C_ext3")
    #
    myCompleteList.append("TT_erdON")
    myCompleteList.append("TT_erdON_ext1")
    myCompleteList.append("TT_evtgen")
    #
    myCompleteList.append("TT_fsrdown")
    myCompleteList.append("TT_fsrdown_ext1")
    myCompleteList.append("TT_fsrdown_ext2")
    myCompleteList.append("TT_fsrup")
    myCompleteList.append("TT_fsrup_ext1")
    myCompleteList.append("TT_fsrup_ext2")
    #
    myCompleteList.append("TT_hdampDOWN")
    myCompleteList.append("TT_hdampDOWN_ext1")
    myCompleteList.append("TT_hdampUP")
    myCompleteList.append("TT_hdampUP_ext1")
    #
    myCompleteList.append("TT_isrdown")
    myCompleteList.append("TT_isrdown_ext1")
    myCompleteList.append("TT_isrdown_ext2")
    myCompleteList.append("TT_isrup_ext1")
    myCompleteList.append("TT_isrup_ext2")
    #
    myCompleteList.append("TT_mtop1665")
    myCompleteList.append("TT_mtop1695_ext1")
    myCompleteList.append("TT_mtop1695_ext2")
    myCompleteList.append("TT_mtop1715")
    myCompleteList.append("TT_mtop1735")
    myCompleteList.append("TT_mtop1755")
    myCompleteList.append("TT_mtop1755_ext1")
    myCompleteList.append("TT_mtop1755_ext2")
    myCompleteList.append("TT_mtop1785")
    #
    myCompleteList.append("TT_widthx0p2")
    myCompleteList.append("TT_widthx0p5")
    myCompleteList.append("TT_widthx0p8")
    myCompleteList.append("TT_widthx2")
    myCompleteList.append("TT_widthx4")
    myCompleteList.append("TT_widthx8")

    myCompleteList.append("TTZToQQ")

    myCompleteList.append("TTWJetsToQQ")
    myCompleteList.append("TTWJetsToLNu_ext2")
    myCompleteList.append("TTWJetsToLNu_ext1")

    myCompleteList.append("TTToSemiLep_hdampUP")
    myCompleteList.append("TTToSemiLep_hdampDOWN")
    myCompleteList.append("TTToSemiLep_TuneCUETP8M2T4up")
    myCompleteList.append("TTToSemiLep_TuneCUETP8M2T4down")

    myCompleteList.append("TTGJets_ext1")
    myCompleteList.append("TTGJets")

    myCompleteList.append("ZZ_ext1")
    myCompleteList.append("ZZ")

    myCompleteList.append("WWToLNuQQ")

    myCompleteList.append("WZ_ext1")
    myCompleteList.append("WZ")

    myCompleteList.append("WJetsToLNu_HT_2500ToInf_ext1")
    myCompleteList.append("WJetsToLNu_HT_2500ToInf")
    myCompleteList.append("WJetsToLNu_HT_1200To2500_ext1")
    myCompleteList.append("WJetsToLNu_HT_1200To2500")
    myCompleteList.append("WJetsToLNu_HT_800To1200_ext1")
    myCompleteList.append("WJetsToLNu_HT_800To1200")
    myCompleteList.append("WJetsToLNu_HT_600To800_ext1")
    myCompleteList.append("WJetsToLNu_HT_600To800")
    myCompleteList.append("WJetsToLNu_HT_400To600_ext1")
    myCompleteList.append("WJetsToLNu_HT_400To600")
    myCompleteList.append("WJetsToLNu_HT_200To400_ext2")
    myCompleteList.append("WJetsToLNu_HT_200To400_ext1")
    myCompleteList.append("WJetsToLNu_HT_200To400")
    myCompleteList.append("WJetsToLNu_HT_100To200_ext2")
    myCompleteList.append("WJetsToLNu_HT_100To200_ext1")
    myCompleteList.append("WJetsToLNu_HT_100To200")
    myCompleteList.append("WJetsToLNu_HT_70To100")

    myCompleteList.append("DYJetsToLL_M_50_ext1")

    myCompleteList.append("TTJets_SingleLeptFromT_amcatnlo")
    myCompleteList.append("TTJets_SingleLeptFromT_genMET_150_madgraph")
    myCompleteList.append("TTJets_SingleLeptFromT_madgraph")
    myCompleteList.append("TTJets_SingleLeptFromT_madgraph_ext1")
    myCompleteList.append("TTJets_SingleLeptFromTbar_amcatnlo")
    myCompleteList.append("TTJets_SingleLeptFromTbar_genMET_150_madgraph")
    myCompleteList.append("TTJets_SingleLeptFromTbar_madgraph")
    myCompleteList.append("TTJets_SingleLeptFromTbar_madgraph_ext1")

    myCompleteList.append("QCD_Pt_120to170_MuEnrichedPt5")
    myCompleteList.append("QCD_Pt_15to20_MuEnrichedPt5")
    myCompleteList.append("QCD_Pt_170to300_MuEnrichedPt5")
    myCompleteList.append("QCD_Pt_170to300_MuEnrichedPt5_ext1")
    myCompleteList.append("QCD_Pt_20to30_MuEnrichedPt5")
    myCompleteList.append("QCD_Pt_300to470_MuEnrichedPt5")
    myCompleteList.append("QCD_Pt_300to470_MuEnrichedPt5_ext1")
    myCompleteList.append("QCD_Pt_300to470_MuEnrichedPt5_ext2")
    myCompleteList.append("QCD_Pt_30to50_MuEnrichedPt5")
    myCompleteList.append("QCD_Pt_470to600_MuEnrichedPt5")
    myCompleteList.append("QCD_Pt_470to600_MuEnrichedPt5_ext1")
    myCompleteList.append("QCD_Pt_470to600_MuEnrichedPt5_ext2")
    myCompleteList.append("QCD_Pt_50to80_MuEnrichedPt5")
    myCompleteList.append("QCD_Pt_600to800_MuEnrichedPt5")
    myCompleteList.append("QCD_Pt_600to800_MuEnrichedPt5_ext1")
    myCompleteList.append("QCD_Pt_800to1000_MuEnrichedPt5")
    myCompleteList.append("QCD_Pt_800to1000_MuEnrichedPt5_ext1")
    myCompleteList.append("QCD_Pt_800to1000_MuEnrichedPt5_ext2")
    myCompleteList.append("QCD_Pt_80to120_MuEnrichedPt5")
    myCompleteList.append("QCD_Pt_80to120_MuEnrichedPt5_ext1")
    myCompleteList.append("QCD_Pt_1000toInf_MuEnrichedPt5")
    return myCompleteList

def GetDatasetWhitelist(opts):
    myWhitelist = []

    if opts.group == "A":
        myWhitelist.append("SingleMuon_Run2016B_03Feb2017_ver2_v2_273150_275376")
        myWhitelist.append("SingleMuon_Run2016C_03Feb2017_v1_275656_276283")
        myWhitelist.append("SingleMuon_Run2016D_03Feb2017_v1_276315_276811")
        myWhitelist.append("SingleMuon_Run2016E_03Feb2017_v1_276831_277420")    
    elif opts.group == "B":
        myWhitelist.append("SingleMuon_Run2016F_03Feb2017_v1_277932_278800")
        myWhitelist.append("SingleMuon_Run2016F_03Feb2017_v1_278801_278808")
        myWhitelist.append("SingleMuon_Run2016G_03Feb2017_v1_278820_280385")
        myWhitelist.append("SingleMuon_Run2016H_03Feb2017_ver2_v1_281613_284035")
        myWhitelist.append("SingleMuon_Run2016H_03Feb2017_ver3_v1_284036_284044")
    elif opts.group == "C":
        myWhitelist.append("TT")
        #
        myWhitelist.append("TT_GluonMoveCRTune")
        #
        myWhitelist.append("TT_QCDbasedCRTune_erdON")
        myWhitelist.append("TT_QCDbasedCRTune_erdON_ext1")
        #
        myWhitelist.append("TT_TuneCUETP8M2T4down")
        myWhitelist.append("TT_TuneCUETP8M2T4down_ext1")
        myWhitelist.append("TT_TuneCUETP8M2T4up")
        myWhitelist.append("TT_TuneCUETP8M2T4up_ext1")
        myWhitelist.append("TT_TuneEE5C")
        myWhitelist.append("TT_TuneEE5C_ext2")
        myWhitelist.append("TT_TuneEE5C_ext3")
        #
        myWhitelist.append("TT_erdON")
        myWhitelist.append("TT_erdON_ext1")
        myWhitelist.append("TT_evtgen")
        #
        myWhitelist.append("TT_fsrdown")
        myWhitelist.append("TT_fsrdown_ext1")
        myWhitelist.append("TT_fsrdown_ext2")
        myWhitelist.append("TT_fsrup")
        myWhitelist.append("TT_fsrup_ext1")
        myWhitelist.append("TT_fsrup_ext2")
        #
        myWhitelist.append("TT_hdampDOWN")
        myWhitelist.append("TT_hdampDOWN_ext1")
        myWhitelist.append("TT_hdampUP")
        myWhitelist.append("TT_hdampUP_ext1")
        #
        myWhitelist.append("TT_isrdown")
        myWhitelist.append("TT_isrdown_ext1")
        myWhitelist.append("TT_isrdown_ext2")
        myWhitelist.append("TT_isrup_ext1")
        myWhitelist.append("TT_isrup_ext2")
        #
        myWhitelist.append("TT_mtop1665")
        myWhitelist.append("TT_mtop1695_ext1")
        myWhitelist.append("TT_mtop1695_ext2")
        myWhitelist.append("TT_mtop1715")
        myWhitelist.append("TT_mtop1735")
        myWhitelist.append("TT_mtop1755")
        myWhitelist.append("TT_mtop1755_ext1")
        myWhitelist.append("TT_mtop1755_ext2")
        myWhitelist.append("TT_mtop1785")
        #
        myWhitelist.append("TT_widthx0p2")
        myWhitelist.append("TT_widthx0p5")
        myWhitelist.append("TT_widthx0p8")
        myWhitelist.append("TT_widthx2")
        myWhitelist.append("TT_widthx4")
        myWhitelist.append("TT_widthx8")
    elif opts.group == "D":
        myWhitelist.append("WJetsToLNu_HT_2500ToInf_ext1")
        myWhitelist.append("WJetsToLNu_HT_2500ToInf")
        myWhitelist.append("WJetsToLNu_HT_1200To2500_ext1")
        myWhitelist.append("WJetsToLNu_HT_1200To2500")
        myWhitelist.append("WJetsToLNu_HT_800To1200_ext1")
        myWhitelist.append("WJetsToLNu_HT_800To1200")
        myWhitelist.append("WJetsToLNu_HT_600To800_ext1")
        myWhitelist.append("WJetsToLNu_HT_600To800")
        myWhitelist.append("WJetsToLNu_HT_400To600_ext1")
        myWhitelist.append("WJetsToLNu_HT_400To600")
        myWhitelist.append("WJetsToLNu_HT_200To400_ext2")
        myWhitelist.append("WJetsToLNu_HT_200To400_ext1")
        myWhitelist.append("WJetsToLNu_HT_200To400")
        myWhitelist.append("WJetsToLNu_HT_100To200_ext2")
        myWhitelist.append("WJetsToLNu_HT_100To200_ext1")
        myWhitelist.append("WJetsToLNu_HT_100To200")
        myWhitelist.append("WJetsToLNu_HT_70To100")    
    elif opts.group == "E":
        myWhitelist.append("QCD_Pt_120to170_MuEnrichedPt5")
        myWhitelist.append("QCD_Pt_15to20_MuEnrichedPt5")
        myWhitelist.append("QCD_Pt_170to300_MuEnrichedPt5")
        myWhitelist.append("QCD_Pt_170to300_MuEnrichedPt5_ext1")
        myWhitelist.append("QCD_Pt_20to30_MuEnrichedPt5")
        myWhitelist.append("QCD_Pt_300to470_MuEnrichedPt5")
        myWhitelist.append("QCD_Pt_300to470_MuEnrichedPt5_ext1")
        myWhitelist.append("QCD_Pt_300to470_MuEnrichedPt5_ext2")
        myWhitelist.append("QCD_Pt_30to50_MuEnrichedPt5")
        myWhitelist.append("QCD_Pt_470to600_MuEnrichedPt5")
        myWhitelist.append("QCD_Pt_470to600_MuEnrichedPt5_ext1")
        myWhitelist.append("QCD_Pt_470to600_MuEnrichedPt5_ext2")
        myWhitelist.append("QCD_Pt_50to80_MuEnrichedPt5")
        myWhitelist.append("QCD_Pt_600to800_MuEnrichedPt5")
        myWhitelist.append("QCD_Pt_600to800_MuEnrichedPt5_ext1")
        myWhitelist.append("QCD_Pt_800to1000_MuEnrichedPt5")
        myWhitelist.append("QCD_Pt_800to1000_MuEnrichedPt5_ext1")
        myWhitelist.append("QCD_Pt_800to1000_MuEnrichedPt5_ext2")
        myWhitelist.append("QCD_Pt_80to120_MuEnrichedPt5")
        myWhitelist.append("QCD_Pt_80to120_MuEnrichedPt5_ext1")
        myWhitelist.append("QCD_Pt_1000toInf_MuEnrichedPt5")    
    elif opts.group == "F":
        myWhitelist.append("TTJets_SingleLeptFromT_amcatnlo")
        myWhitelist.append("TTJets_SingleLeptFromT_genMET_150_madgraph")
        myWhitelist.append("TTJets_SingleLeptFromT_madgraph")
        myWhitelist.append("TTJets_SingleLeptFromT_madgraph_ext1")
        myWhitelist.append("TTJets_SingleLeptFromTbar_amcatnlo")
        myWhitelist.append("TTJets_SingleLeptFromTbar_genMET_150_madgraph")
        myWhitelist.append("TTJets_SingleLeptFromTbar_madgraph")
        myWhitelist.append("TTJets_SingleLeptFromTbar_madgraph_ext1")
    elif opts.group == "G":
        myWhitelist.append("TTZToQQ")
        myWhitelist.append("TTWJetsToQQ")
        myWhitelist.append("TTWJetsToLNu_ext2")
        myWhitelist.append("TTWJetsToLNu_ext1")    
    elif opts.group == "H":
        myWhitelist.append("TTToSemiLep_hdampUP")
        myWhitelist.append("TTToSemiLep_hdampDOWN")
        myWhitelist.append("TTToSemiLep_TuneCUETP8M2T4up")
        myWhitelist.append("TTToSemiLep_TuneCUETP8M2T4down")
    elif opts.group == "I":    
        myWhitelist.append("TTGJets_ext1")
        myWhitelist.append("TTGJets")               
    elif opts.group == "J":
        myWhitelist.append("ZZ_ext1")
        myWhitelist.append("ZZ")        
    elif opts.group == "K":
        myWhitelist.append("WWToLNuQQ")        
        myWhitelist.append("WW")
        myWhitelist.append("WW_ext1")
    elif opts.group == "L":
        myWhitelist.append("WZ_ext1")
        myWhitelist.append("WZ")
    elif opts.group == "M":
        myWhitelist.append("DYJetsToLL_M_50_ext1")    
    else:
        msg = "Unknown systematics submission dataset group \"%s\"%" % (opts.group)
        raise Exception(msg)
    return myWhitelist

def PrintOptions(opts):
    '''
    '''
    table    = []
    msgAlign = "{:<20} {:<10} {:<10}"
    title    =  msgAlign.format("Option", "Value", "Default")
    hLine    = "="*len(title)
    table.append(hLine)
    table.append(title)
    table.append(hLine)
    #table.append( msgAlign.format("mcrab" , opts.mcrab , "") )
    table.append( msgAlign.format("jCores", opts.jCores, "") )
    table.append( msgAlign.format("includeOnlyTasks", opts.includeOnlyTasks, "") )
    table.append( msgAlign.format("excludeTasks", opts.excludeTasks, "") )
    table.append( msgAlign.format("nEvts", opts.nEvts, NEVTS) )
    table.append( msgAlign.format("verbose", opts.verbose, VERBOSE) )
    table.append( msgAlign.format("histoLevel", opts.histoLevel, HISTOLEVEL) )
    table.append( msgAlign.format("usePUreweighting", opts.usePUreweighting, PUREWEIGHT) )
    table.append( msgAlign.format("useTopPtReweighting", opts.useTopPtReweighting, TOPPTREWEIGHT) )
    table.append( msgAlign.format("doSystematics", opts.doSystematics, DOSYSTEMATICS) ) 
    table.append( hLine )

    # Print("Will run on multicrab directory %s" % (opts.mcrab), True)     
    for i, line in enumerate(table):
        Print(line, i==0)

    return


#================================================================================================      
if __name__ == "__main__":
    '''
    https://docs.python.org/3/library/argparse.html

    name or flags...: Either a name or a list of option strings, e.g. foo or -f, --foo.
    action..........: The basic type of action to be taken when this argument is encountered at the command line.
    nargs...........: The number of command-line arguments that should be consumed.
    const...........: A constant value required by some action and nargs selections.
    default.........: The value produced if the argument is absent from the command line.
    type............: The type to which the command-line argument should be converted.
    choices.........: A container of the allowable values for the argument.
    required........: Whether or not the command-line option may be omitted (optionals only).
    help............: A brief description of what the argument does.
    metavar.........: A name for the argument in usage messages.
    dest............: The name of the attribute to be added to the object returned by parse_args().
    '''

    # Default Values
    VERBOSE       = False
    NEVTS         = -1
    HISTOLEVEL    = "Debug" #"Informative" #"Debug"
    PUREWEIGHT    = True
    TOPPTREWEIGHT = True
    DOSYSTEMATICS = False
    GROUP         = "A"

    parser = OptionParser(usage="Usage: %prog [options]" , add_help_option=False,conflict_handler="resolve")
    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("-j", "--jCores", dest="jCores", action="store", type=int, 
                      help="Number of CPU cores (PROOF workes) to use. (default: all available)")

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    parser.add_option("-n", "--nEvts", dest="nEvts", action="store", type=int, default = NEVTS,
                      help="Number of events to run on (default: %s" % (NEVTS) )

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default = VERBOSE, 
                      help="Enable verbosity (for debugging) (default: %s)" % (VERBOSE))

    parser.add_option("-h", "--histoLevel", dest="histoLevel", action="store", default = HISTOLEVEL,
                      help="Histogram ambient level (default: %s)" % (HISTOLEVEL))

    parser.add_option("--noPU", dest="usePUreweighting", action="store_false", default = PUREWEIGHT, 
                      help="Do NOT apply Pileup re-weighting (default: %s)" % (PUREWEIGHT) )

    parser.add_option("--noTopPt", dest="useTopPtReweighting", action="store_false", default = TOPPTREWEIGHT, 
                      help="Do NOT apply top-pt re-weighting (default: %s)" % (TOPPTREWEIGHT) )

    parser.add_option("--doSystematics", dest="doSystematics", action="store_true", default = DOSYSTEMATICS, 
                      help="Do systematics variations  (default: %s)" % (DOSYSTEMATICS) )

    parser.add_option("--group", dest="group", default = GROUP, 
                      help="The group of datasets to run on. Capital letter from \"A\" to \"I\"  (default: %s)" % (GROUP) )

    (opts, args) = parser.parse_args()

    if opts.mcrab == None:
        raise Exception("Please provide input multicrab directory with -m")

    allowedLevels = ['Never', 'Systematics', 'Vital', 'Informative', 'Debug']
    if opts.histoLevel not in allowedLevels:
        raise Exception("Invalid ambient histogram level \"%s\"! Valid options are: %s" % (opts.histoLevel, ", ".join(allowedLevels)))

    main()

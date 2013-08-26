#!/usr/bin/env python

######################################################################
# All imported modules
######################################################################
### System modules
import sys
import array
import math
import ROOT
from ROOT import gStyle
### HPlus modules
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
### Script-specific modules
from TreeHelper import *
from TreeCutHelper import * 
from TreeVarHelper import * 

######################################################################
### Define options and declarations
######################################################################
### Create boolean dictionary
boolDict = {
"bBatchMode"        : True,
"bRatio"            : False,
"bPrintPSet"        : False,
"bLogY"             : True,
"bNormalizeToOne"   : True,
"bAddMCUncertainty" : True,   #Requires: bStackHistos == True
"bAddLumiText"      : True,
# 
"bStackHistos"      : False, 
"bMergeEwk"         : False,
#
"bRemoveData"       : False,
"bRemoveSignal"     : True,  #Requires : RemoveData==True
"bRemoveEwk"        : False,
"bRemoveQcd"        : True,
"bRemoveWJetsExcl"  : False, #NEVER change this!
"bRemoveWJetsIncl"  : False, #NEVER change this!
}
    
### Other Global Definitions
getBool = lambda Key: boolDict[Key]
BR_tH          = 0.01
BR_Htaunu      = 1.0
signalMass     = "160"
yMin           = 0.0
yMax           = 200.0
yMinLog        = 1E-01
yMaxLog        = 1E+03
yMinRatio      = 0.0
yMaxRatio      = 2.0
yMaxFactor     = 2
yMaxFactorTH2  = yMaxFactor*0.7
yMinLog        = 1E-03
yMaxFactorLog  = 10
xLegMin        = 0.65
xLegMax        = 0.93
yLegMin        = 0.65
yLegMax        = 0.93
MyLumi         = 2.3*1000 #(pb)
pSetToPrint    = "TTToHplusBHminusB_M120_Fall11"
myDataEra      = "Run2011AB" #"Run2011A" "Run2011B" "Run2011AB"
#multicrabPath  = "/Users/attikis/my_work/cms/lxplus/TreeAnalysis_JetThrustAndNonIsoLeptons_v44_5_130312_171728/"
multicrabPath  = "/Users/attikis/my_work/cms/lxplus/FullHplusMass_130328_170951/" #Wjets weight needed or "weightAtFill"
myAnalysis     = "signalAnalysisLight"
ROOT.gROOT.SetBatch( getBool("bBatchMode") )

######################################################################
### Function declarations
######################################################################
def main():
    '''
    def main():
    The main function where auxuliary methods are called. Specifically,
    The datasets are retrieved for a specified data Era. These are then 
    passed to relevant module where all manipulations are performed.
    '''

    ### Get the desired datasets 
    datasets = getDatasets(multicrabPath, myDataEra)

    ### Plot all histograms defined in the HistoList found in the file HistoHelper.py
    #doTreeScan(datasets, HistoList, "", SaveExtension="")

    ### Define the TCuts to be used in a list
    MyCuts = []
    MyCuts.append(JetSelectionSanityCuts)
    MyCuts.append(And(JetSelectionSanityCuts, Met + ">= 60"))
    MyCuts.append(And(JetSelectionSanityCuts, Met + ">= 60", BtagCut))
    MyCuts.append(And(JetSelectionSanityCuts, Met + ">= 60", BtagCut, DeltaPhiLooseCuts))
    MyCuts.append(And(JetSelectionSanityCuts, Met + ">= 60", BtagCut, DeltaPhiMediumCuts))
    MyCuts.append(And(JetSelectionSanityCuts, Met + ">= 60", BtagCut, DeltaPhiMediumPlusCuts))
    MyCuts.append(And(JetSelectionSanityCuts, Met + ">= 60", BtagCut, DeltaPhiTightCuts))
    MyCuts.append(And(JetSelectionSanityCuts, Met + ">= 60", BtagCut, DeltaPhiTightPlusCuts))

    ### Define the TCut corresponding names to be used in the tables
    MyCutsNames = []
    MyCutsNames.append("Njets cut")
    MyCutsNames.append("MET > 60 GeV")
    MyCutsNames.append("B tagging")
    MyCutsNames.append("TailKiller, Loose")
    MyCutsNames.append("TailKiller, Medium")
    MyCutsNames.append("TailKiller, Medium+")
    MyCutsNames.append("TailKiller, Tight")
    MyCutsNames.append("TailKiller, Tight+")

    ### Create the counters and print the results using the selected TCuts
    doCounters(datasets, MyCuts, MyCutsNames)
     
    return

######################################################################
def getDatasets(multicrabPath, myDataEra):
    '''
    def getDatasets(multicrabPath, myDataEra):
    This module used the user-defined path to a multicrab directory to 
    get the available datasets for a given Data-Era. 
    According to the boolean dictionary in the beginning of this file
    the datasets are merged and reordered. Optionally the PSet parameters
    are also printed for a specified dataset, also selected at the beginning 
    of this file with the "pSetToPrint" string.
    '''

    ### Get the ROOT files for all datasets, merge datasets and reorder them
    print "*** Obtaining datasets from: %s" % (multicrabPath)
    datasets = dataset.getDatasetsFromMulticrabCfg(directory=multicrabPath, dataEra=myDataEra)
    #print "*** Available datasets: %s" % (datasets.getAllDatasetNames())

    ### Print PSets used in ROOT-file generation
    if getBool("bPrintPSet"):
        print datasets.getDataset(pSetToPrint).getParameterSet()
        
    ### Take care of PU weighting, luminosity, signal merging etc... of the datatasets
    manageDatasets(datasets)

    ### Print the dataset information for sanity checks
    datasets.printInfo()

    return datasets

######################################################################
def manageDatasets(datasets):
    '''
    def manageDatasets(datasets):
    Handles the PU weighting, luminosity loading and signal merging of the datatasets.
    '''
    
    ### Since (by default) we use weighted counters, and the analysis job inputs are 
    ### normally skims (as are "v44_4" and "v53_1"), need to update events to PU weighted
    print "\n*** Updating events to PU weighted:"
    datasets.updateNAllEventsToPUWeighted()

    if getBool("bRemoveData"):
        datasets.remove(datasets.getDataDatasetNames())
        histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    else:
        datasets.loadLuminosities()

    ### Now optionally remove datasets
    if getBool("bRemoveWJetsExcl"):
        print "*** Removing WJets Exclusinve samples"
        datasets.remove(filter(lambda name:"W1Jets_TuneZ2_Fall11" in name, datasets.getAllDatasetNames())) 
        datasets.remove(filter(lambda name:"W2Jets_TuneZ2_Fall11" in name, datasets.getAllDatasetNames())) 
        datasets.remove(filter(lambda name:"W3Jets_TuneZ2_v2_Fall11" in name, datasets.getAllDatasetNames())) 
        datasets.remove(filter(lambda name:"W4Jets_TuneZ2_Fall11" in name, datasets.getAllDatasetNames())) 
        print "*** Available datasets: %s" % (datasets.getAllDatasetNames())

    if getBool("bRemoveWJetsIncl"):
        print "*** Removing WJets Inclusive samples"
        datasets.remove(filter(lambda name: "WJets_TuneZ2_Fall11" in name, datasets.getAllDatasetNames())) 
        print "*** Available datasets: %s" % (datasets.getAllDatasetNames())
        
    print "\n*** Default merging of dataset components:"
    plots.mergeRenameReorderForDataMC(datasets)
                
    if getBool("bRemoveSignal"): 
        print "\n*** Removing all signal samples"
        datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))
        datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    else:
        print "\n*** Removing all signal samples, except m=%s GeV/cc" % (signalMass)
        datasets.remove(filter(lambda name: "TTToHplus" in name and not "M"+signalMass in name, datasets.getAllDatasetNames()))
        datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
        plots._legendLabels["TTToHplus_M"+signalMass] = "m_{H^{#pm}} = " + signalMass + " GeV/c^{2}"

    ### Setup style
    styleGenerator = styles.generator(fill=False)
    style = tdrstyle.TDRStyle()

    print "*** Setting signal cross sections, using BR(t->bH+)=%s and BR(H+ -> tau+ nu)=%s" % (BR_tH, BR_Htaunu)
    xsect.setHplusCrossSectionsToBR(datasets, BR_tH, BR_Htaunu)
    print "*** Merging WH and HH signals"
    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section
    
    if getBool("bRemoveEwk"):
        mergeEwkMc(datasets)
        datasets.remove(filter(lambda name: "EWK MC" in name, datasets.getAllDatasetNames()))
    else:
        if getBool("bMergeEwk"):
            mergeEwkMc(datasets)
    if getBool("bRemoveQcd"):
        datasets.remove(filter(lambda name: "QCD" in name, datasets.getAllDatasetNames()))
        
        print "*** Datasets that will be used: %s" % (datasets.getAllDatasetNames())

    return datasets

######################################################################
def mergeEwkMc(datasets):
    '''
    def mergeEwkMc(datasets):
    Merges the EWK MC samples into a single dataset. The style adopted is that of ttbar (default).
    The merging is controlled by the use of the "bMergeEwk" boolean.
    '''
    
    print "*** Merging EWK MC"
    datasets.merge("EWK MC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=False)
    plots._plotStyles["EWK MC"] = styles.ttStyle

    return #datasets

######################################################################
def doTreeScan(datasets, HistoList, MyCuts, SaveExtension):
    
    print "*** Warning! This TreeScan module is in testing phase."

    ### Define the event "weight" to be used
    EvtWeight = GetEventWeight(MyCuts)

    treePath = myAnalysis+"/tree"
    treeDraw = dataset.TreeDraw(treePath, weight=EvtWeight)

    f = open("treeEvents.txt", "w")
    def printTreeEvent(tree):
        expr = tree.event
        print "*** ", expr
        f.write("%d\n" % (expr) )

    ts1 = dataset.TreeScan(treeDraw.tree, function=printTreeEvent, selection=And(BtagCut))
    ts2 = dataset.TreeScan(treeDraw.tree, function=printTreeEvent, selection=And(BtagCut, Met + ">=60"))
    ts3 = dataset.TreeScan(treeDraw.tree, function=printTreeEvent, selection=And(BtagCut, Met + ">=60", DeltaPhiLooseCuts))
    datasets.getDataset("Data").getDatasetRootHisto(ts1)
    f.close()

    return

######################################################################
def doCounters(datasets, MyCuts, MyCutsName):
    
    ### Define the counters to be used
    #eventCounter = counter.EventCounter(datasets, counters=myAnalysis + myDataEra + "/counters")
    eventCounter = counter.EventCounter(datasets)

    ### Normalise the MC sample to a luminosity before creating a table
    eventCounter.normalizeMCToLuminosity(GetLumi(datasets))
    

    myRowNames = []
    for iCut, iCutName in zip(MyCuts, MyCutsName):
        #print "*** Cut: %s\n*** CutName: %s" % (iCut, iCutName)
        print "*** Processing TCut with:\n    Name = \"%s\" \n    Expr = \"%s\"" % (iCutName, iCut)

        ### Define the event "weight" to be used
        EvtWeight = GetEventWeight(iCut)
    
        ### Define the TTree to be used
        treePath = "tree" # treePath = myAnalysis+"/tree"
        treeDraw = dataset.TreeDraw(treePath, weight=EvtWeight, selection=iCut)

        ### Append custom rows to the event counter. An asterisk denotes that the counter row was added. Informative and makes things easier
        myRowName = iCutName #"*" + iCutName
        myRowNames.append(myRowName)
        eventCounter.getMainCounter().appendRow(myRowName, treeDraw)

    ### Get table with all default rows removed and manage the table format
    myTable = GetCustomTable(eventCounter, myRowNames)

    if getBool("bMergeEwk"):    
        DataMinusEwkMc = counter.subtractColumn("DataMinusEwkMc", myTable.getColumn(name="Data"), myTable.getColumn(name="EWK MC"))
        QcdPurity      = counter.divideColumn("QCD Purity", DataMinusEwkMc, myTable.getColumn(name="Data"))
        myTable.appendColumn(QcdPurity)

    ### See http://docs.python.org/2/library/string.html for string format
    cellTextFormat  = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.2E', valueOnly=True)) #%.2e
    cellLaTeXFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat='%.2E', valueOnly=True)) #%.2e
    purityFormat    = counter.CellFormatTeX(valueFormat='%.2f', valueOnly=True)

    ### Customise the "QCD Purity" column
    cellTextFormat.setColumnFormat(purityFormat, name="QCD Purity") #does nothing
    cellLaTeXFormat.setColumnFormat(purityFormat, name="QCD Purity") #does nothing

    # between construction of table format and table format

    ### Print the final table with the desired format
    print "============================================================"
    print "Data-Era: %s (%s pb-1)" % (myDataEra, GetLumi(datasets))
    print "============================================================"
    print myTable.format(cellTextFormat)

    print "============================================================"
    print "Data-Era: %s (%s pb-1)" % (myDataEra, GetLumi(datasets))
    print "============================================================"
    print myTable.format(cellLaTeXFormat)

    return

######################################################################
def GetLumi(datasets):
    if getBool("bRemoveData"):
        trueLumi = MyLumi
    else:
        trueLumi = datasets.getDataset("Data").getLuminosity()
    return trueLumi

######################################################################
def GetEventWeight(MyCuts):
    EvtWeight = "weightAtFill"    
    ### Obsolete code
    #if "passedBTagging" in MyCuts:
    #    EvtWeight = "(weightPileup*weightTauTrigger*weightPrescale*weightBTagging)"
    #else:
    #    EvtWeight = "weightPileup*weightTauTrigger*weightPrescale"
    return EvtWeight

######################################################################
def GetCustomTable(eventCounter, myRowNames):

    table     = eventCounter.getMainCounterTable()
    tableCopy = table.clone()
    #print table.getRowNames()
    
    ### Define the table rows that are NOT to be deleted from the counter
    #DefaultRowNames = ['Trigger and HLT_MET cut', 'primary vertex', 'taus > 0', 'taus == 1', 'tau trigger scale factor', 'tau veto', 'electron veto', 'muon veto']
    DefaultRowNames = ['Trigger and HLT_MET cut', 'taus > 0', 'electron veto', 'muon veto']
    RowsNotToRemove = myRowNames + DefaultRowNames

    ### Remove unwanted rows from the counter
    nRows = table.getNrows()
    for iRow in range(0, nRows-1):
        rowName = table.getRowNames()[iRow]

        if rowName not in RowsNotToRemove:
            #print "*** Removing row with name %s (#%s of %s)" % (rowName, iRow, nRows)
            tableCopy.removeRow(name=rowName)
            
    ### Copy back the new table version
    table = tableCopy.clone()
    return table

######################################################################
if __name__ == "__main__":

    ### Call the main function
    main()

    ### Keep session alive (otherwise canvases close automatically)
    if not getBool("bBatchMode"):
        raw_input("*** DONE! Press \"ENTER\" key exit session: ")

#!/usr/bin/env python
'''

Usage:
Launch default script
./plotTemplate.py -m <pseudo_mcrab_directory>

Launch but exclude the M_180 sample
./plotTest.py -m Kinematics_161025_020335 -e M_180

Launch but exclude the multiple signal samples
./plotTest.py -m Kinematics_161025_020335 -e "M_180|M_200|M_220|M_250|M_300|M_350|M_400"

Launch but only include the QCD_Pt samples
./plotTest.py -m Kinematics_161025_020335 -i QCD_Pt

Launch but exclude various samples
./plotTest.py -m Kinematics_161025_020335 -e "M_200|M_220|M_250|M_300|M_350|M_400|QCD_Pt|JetHT"
or 
./plotTest.py -m Hplus2tbAnalysis_161026_135227 -e "M_180|M_200|M_220|M_250|M_300|M_350|M_400|M_500|ZZTo4Q"


Last Used:
./plotTest.py -m Hplus2tbAnalysis_161108_064941 -e "QCD_Pt_15to30|TTJets" && rsync --partial --progress *.png attikis@lxplus.cern.ch:~/public/html/.

./plotTest.py -m Hplus2tbAnalysis_161109_20161104T0853/ -e "ChargedHiggs|QCD_b|QCD_Pt_15to30|TTJets|ST_t|WW|WZ|ZZ|TTTT|TTZToQQ|ttbb|TTWJetsToQQ|WJetsToQQ"

./plotTest.py -m Hplus2tbAnalysis_161109_20161104T0853/ -e "ChargedHiggs|QCD_b|QCD_Pt_15to30|TTJets|ST_t|WW|WZ|ZZ|TTTT|TTZToQQ|ttbb|TTWJetsToQQ|WJetsToQQ|2016F_PromptReco_v1_278801_278808|2016G"

./plotTest.py -m Hplus2tbAnalysis_161109_20161104T0853/ -e "ChargedHiggs|QCD_b|QCD_Pt_15to30|TTJets|ST_t|WW|WZ|ZZ|TTTT|TTZToQQ|ttbb|TTWJetsToQQ|WJetsToQQ|2016B|2016C|2016D|2016E|2016F_PromptReco_v1_277816_278800"

'''

#================================================================================================
# Imports
#================================================================================================
import os
import sys
from optparse import OptionParser
import getpass
import socket

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

import ROOT

#================================================================================================
# Variable Definition
#================================================================================================
kwargs = {
    "verbose"          : False,
    "dataEra"          : "Run2016",
    "searchMode"       : "80to1000",
    "analysis"         : "Hplus2tbAnalysis",
    "optMode"          : "",
    "savePath"         : os.getcwd() + "/Plots/", #"/Users/attikis/latex/talks/post_doc.git/HPlus/HIG-XY-XYZ/2016/Kinematics_06September2016/figures/all/",
    "saveFormats"      : [".png", ".pdf"],
    "xlabel"           : "", #b-tag SF
    "ylabel"           : "Events / %.0f",
    "rebinX"           : 4,
    "rebinY"           : 1,
    "xlabelsize"       : None, #10
    "ratio"            : True,
    "ratioYlabel"      : None,
    "ratioInvert"      : False,
    "stackMCHistograms": True,
    "addMCUncertainty" : True,
    "addLuminosityText": True,
    "addCmsText"       : True,
    "errorBarsX"       : True,
    "logX"             : False,
    "logY"             : True,
    "gridX"            : True,
    "gridY"            : True,
    "cmsExtraText"     : "Preliminary", #"Preliminary" "Simulation"
    "removeLegend"     : False,
    #"moveLegend"       : {"dx": -0.05, "dy": +0.0, "dh": -0.1},
    "moveLegend"       : {"dx": -0.45, "dy": -0.4, "dh": +0.1},
    "cutValue"         : 1.2,
    "cutLine"          : False,
    "cutBox"           : False,
    "cutLessthan"      : False,
    "cutFillColour"    : ROOT.kAzure-4,
}


hNames = [#"counters/weighted/counter",
          "btagSF",
          #"counters/weighted/counter",
          #"counters/weighted/METFilter selection",
          #"counters/weighted/e selection (Veto)",
          #"counters/weighted/mu selection (Veto)",
          #"counters/weighted/jet selection",
          #"counters/weighted/bjet selection",
          ]


#================================================================================================
# Main
#================================================================================================
def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return


def Verbose(msg, printHeader=True, verbose=False):
    if not verbose:
        return
    Print(msg, printHeader)
    return


def SaveAs(p, savePath, saveName, saveFormats, verbose):

    # For-loop: All formats to save file
    for i, ext in enumerate(saveFormats):
        sName = saveName + ext
        if "html" in sName:
            user    = getpass.getuser()
            initial = getpass.getuser()[0]
            sName   = sName.replace("/afs/cern.ch/user/%s/" % (initial), "http://cmsdoc.cern.ch/~")
            sName   = sName.replace("%s/public/html/" % (user), "%s/" % (user))

        if not os.path.exists(savePath):
            os.mkdir(savePath)

        fullPath = os.path.join(savePath, saveName + ext)
        Print("%s" % fullPath, i==0)

    p.saveAs(os.path.join(savePath, saveName), saveFormats)
    return


def HasKeys(keyList, **kwargs):
    for key in keyList:
        if key not in kwargs:
            raise Exception("Could not find the keyword \"%s\" in kwargs" % (key) )
    return


def GetDatasetsFromDir(mcrab, opts, **kwargs):

    dataEra    = kwargs.get("dataEra")
    searchMode = kwargs.get("searchMode")
    analysis   = kwargs.get("analysis")
    optMode    = kwargs.get("optMode")

    if opts.includeTasks != "":
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], dataEra=dataEra, searchMode=searchMode, analysisName=analysis, includeOnlyTasks=opts.includeTasks, optimizationMode=optMode)
    elif opts.excludeTasks != "":
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], dataEra=dataEra, searchMode=searchMode, analysisName=analysis, excludeTasks=opts.excludeTasks, optimizationMode=optMode)
        # excludeTasks="M_180|M_220|M_250"
    else:
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], dataEra=dataEra, searchMode=searchMode, analysisName=analysis, optimizationMode=optMode)
    return datasets


def main(opts):

    # Setup the style
    style = tdrstyle.TDRStyle()
    
    # Set ROOT batch mode boolean
    ROOT.gROOT.SetBatch(opts.batchMode)

    # Setup & configure the dataset manager
    datasetsMgr = GetDatasetsFromDir(opts.mcrab, opts, **kwargs)
    datasetsMgr.updateNAllEventsToPUWeighted()
    datasetsMgr.PrintCrossSections()
    datasetsMgr.PrintLuminosities()

    # Set/Overwrite cross-sections
    for d in datasetsMgr.getAllDatasets():
        if "ChargedHiggs" in d.getName():
            datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)
    
    # Merge datasets: All JetHT to "Data", QCD_Pt to "QCD", QCD_bEnriched to "QCD_b",  single-top to "SingleTop", WW, WZ, ZZ to "Diboson"           
    plots.mergeRenameReorderForDataMC(datasetsMgr)

    # Remove datasets
    # datasetsMgr.remove("QCD-b") 
    # datasetsMgr.remove("QCD")
    
    # Print dataset information
    datasetsMgr.PrintInfo()

    # Create data-MC comparison plot, with the default 
    p = plots.DataMCPlot(datasetsMgr, hNames[0])
    
    # Create a comparison plot
    ratioOpts = {"ymin": 0.0, "ymax": 2.0}
    if kwargs.get("logY")==True:
        canvOpts = {"xmin": 0.0, "ymin": 1e-1, "ymaxfactor": 10}
    else:
        canvOpts = {"ymin": 0.0, "ymaxfactor": 1.2}

    # Draw a customised plot & Save it
    plots.drawPlot(p, 
                   hNames[0].replace("/", "_").replace(" ", "_").replace("(", "_").replace(")", ""),
                   xlabel=kwargs.get("xlabel"), 
                   ylabel=kwargs.get("ylabel"),
                   rebinX=kwargs.get("rebinX"), 
                   rebinY=kwargs.get("rebinY"),
                   xlabelsize=kwargs.get("xlabelsize"),
                   ratio=kwargs.get("ratio"), 
                   stackMCHistograms=kwargs.get("stackMCHistograms"), 
                   ratioYlabel=kwargs.get("ratioYlabel"),
                   ratioInvert=kwargs.get("ratioInvert"),
                   addMCUncertainty=kwargs.get("addMCUncertainty"), 
                   addLuminosityText=kwargs.get("addLuminosityText"),
                   addCmsText=kwargs.get("addCmsText"),
                   opts=canvOpts, opts2=ratioOpts, 
                   log=kwargs.get("logY"), 
                   errorBarsX=kwargs.get("errorBarsX"),
                   cmsExtraText=kwargs.get("cmsExtraText"),
                   moveLegend=kwargs.get("moveLegend"),
                   #cutLine=kwargs.get("cutValue"),
                   cutBox={"cutValue": kwargs.get("cutValue"), "fillColor": kwargs.get("cutFillColour"), "box": kwargs.get("cutBox"), "line": kwargs.get("cutLine"), "lessThan": kwargs.get("cutLessthan")},
                   )
    
    # Remove legend?
    if kwargs.get("removeLegend"):
        p.removeLegend()

    # Additional text
    # histograms.addText(0.4, 0.9, "Alexandros Attikis", 17)
    # histograms.addText(0.4, 0.11, "Runs " + datasetsMgr.loadRunRange(), 17)
    
    # Save the canvas to a file
    # SaveAs(p, kwargs.get("savePath"), hNames[0].replace("/","_"), kwargs.get("saveFormats"), True)

    
    if not opts.batchMode:
        raw_input("=== plotTest.py:\n\tPress any key to quit ROOT ...")

    return


#================================================================================================
# Main
#================================================================================================
if __name__ == "__main__":

    parser = OptionParser(usage="Usage: %prog [options]" , add_help_option=False,conflict_handler="resolve")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=True, 
                      help="Enables batch mode (canvas creation  NOT generates a window)")

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, 
                      help="Enables verbose mode (for debugging purposes)")

    parser.add_option("-i", "--includeTasks", dest="includeTasks" , default="", type="string",
                      help="Only perform action for this dataset(s) [default: '']")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks" , default="", type="string",
                      help="Exclude this dataset(s) from action [default: '']")

    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if opts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        print __doc__
        sys.exit(0)
    else:
        pass

    # Program execution
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotTemplate.py: Press any key to quit ROOT ...")

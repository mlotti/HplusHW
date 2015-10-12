#######################################################################################################
# All imported modules
#######################################################################################################
# System modules
import os
# ROOT modules
import ROOT
# HPlus modules
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms

class HistoTemplate:
    '''
    class HistoTemplate():
    Define all attribues of the histogram, including names, x- and y-Labels, x- and y- axis min and max etc..
    '''

    def __init__(self, name, xLabel, xMin, xMax, bLogX, yLabel, yMin, yMax, bLogY, legendLabel, legendHeader=None):
        # name           : Define histogram name
        # xLabel, yLabel : Define the x-axis label. Use "None" for default
        # xMin, xMax     : Overwrite the default x-axis range
        # yMin, yMax     : Overwrite the default y-axis range
        # bLogX, bLogY   : Set whether you want the histogram's axes in log-scale
        # legendLabel    : Set the legend label for the histogram

        self.name    = name
        #
        self.xLabel  = xLabel
        self.xMin    = xMin
        self.xMax    = xMax
        self.bLogX   = bLogX
        #
        self.yLabel  = yLabel
        self.yMin    = yMin
        self.yMax    = yMax
        self.bLogY   = bLogY
        #
        self.legendLabel = legendLabel
        self.legendHeader = legendHeader

#######################################################################################################
def GetPurityHistoNames(sMyLeg):
    '''
    def GetPurityHistoNames(sMyLeg):
    Return a list of histogram templates for all purity-related histograms.
    '''
    
    # Create empty list for paths to histograms within ROOT file 
    hNameList = []
    # Create empty list for 
    hTemplateList = []

    # Fill the histogram path list 
    hNameList.append("Purity_*ErrorType*_QCDfactorised_TradPlusCollinearTailKiller_NevtAfter" + sMyLeg)

    # Fill the histogram template list 
    for h in hNameList:
        #hTemplateList.append(HistoTemplate(h, "p_{T, #tau_{h}} (GeV/c)", None, None, False, "Purity / 20-200 GeV/c", 0.0, 1.02, False, None))
        hTemplateList.append(HistoTemplate(h, "p_{T, #tau_{h}} (GeV/c)", None, None, False,  "Purity / 20-200 GeV/c", 0.0, 1.02, False, None))

    return hTemplateList

#######################################################################################################
def GetEfficiencyHistoNames(sMyLeg):
    '''
    def GetEfficiencyHistoNames(sMyLeg):
    Return a list of histogram templates for all efficiency-related histograms.
    '''

    # Create empty list for paths to histograms within ROOT file 
    hNameList = []
    # Create empty list for 
    hTemplateList = []

    # Fill the histogram path list 
    hNameList.append("Efficiency_"+sMyLeg+"_*ErrorType*_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterStandardSelections")

    # Fill the histogram template list 
    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "p_{T, #tau_{h}} (GeV/c)", None, None, False, "Efficiency / 20-200 GeV/c", 0.5E-03, 1E+00, True, None))

    return hTemplateList

#######################################################################################################
def GetNEventsHistoNames(sMyLeg):
    '''
    def GetNEventsHistoNames(sMyLeg):
    Return a list of histogram templates for all Event counting-related histograms.
    '''

    # Create empty list for paths to histograms within ROOT file 
    hNameList = []
    # Create empty list for 
    hTemplateList = []

    # Fill the histogram path list 
    hNameList.append("Nevents_*ErrorType*_QCDfactorised_TradPlusCollinearTailKiller_NevtAfter" + sMyLeg)


    # Fill the histogram template list 
    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "p_{T, #tau_{h}} (GeV/c)", None, None, False, "Events / 20-200 GeV/c" , None, None, True, None))

    return hTemplateList

#######################################################################################################
def GetMtShapeHistoNames(sMyLeg):
    '''
    def GetMtShapeHistoNames(sMyLeg):
    Return a list of histogram templates for all mT-shape related histograms.
    '''

    # Create empty list for paths to histograms within ROOT file 
    hNameList = []
    # Create empty list for 
    hTemplateList = []

    # Fill the histogram path list 
    folder = "Closure_Shape_QCDfactorised_TradPlusCollinearTailKiller_MtAfter" + sMyLeg
    hNameList.append( folder + "/" + folder + "_*ErrorType*")
    legendLabel = sMyLeg.replace("Leg1", "E_{T}^{miss}").replace("Leg2", "#tau_{h}").replace("leg1", "E_{T}^{miss}").replace("leg2", "#tau_{h}").replace("StandardSelections", "Std.")
    
    # Fill the histogram template list 
    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "m_{T}(#tau_{h}, E_{T}^{miss}) (GeV/c^{2})", None, None, False, "Events / 20-200 GeV/c^{2}", None, None, False, legendLabel))
        
    return hTemplateList

#######################################################################################################
def GetMtBinShapeHistoNames(lBinList, sMyLeg):
    '''
    def GetMtBinShapeHistoNames(sMyLeg):
    Return a list of histogram templates for all mT bin shape related histograms.
    '''

    # Create empty list for paths to histograms within ROOT file 
    hNameList = []
    # Create empty list for 
    hTemplateList = []

    # Fill the histogram-path and histogram-template lists for the list of bins defined by the user
    folder = "Closure_Shape_QCDfactorised_TradPlusCollinearTailKiller_MtAfter" + sMyLeg
    legendLabel = sMyLeg.replace("Leg1", "E_{T}^{miss}").replace("Leg2", "#tau_{h}").replace("leg1", "E_{T}^{miss}").replace("leg2", "#tau_{h}").replace("StandardSelections", "Std.")

    tauBinNames = getTauPtBinsDict()
    for index, myBin in enumerate(lBinList):

        tauBinNames  = getTauPtBinsDict()        
        legendLabel  = legendLabel
        legendHeader = tauBinNames[myBin]
        hPath = folder + "/" + folder + "_binInfo%s_*ErrorType*" % (str(myBin)) 
        hTemplateList.append(HistoTemplate(hPath, "m_{T}(#tau_{h}, E_{T}^{miss}) (GeV/c^{2})", None, None, False, "Events / 20-200 GeV/c^{2}", None, None, False, legendLabel, tauBinNames[myBin]))

    return hTemplateList


#######################################################################################################
def GetMetShapeHistoNames(sMyLeg):
    '''
    def GetMetShapeHistoNames(sMyLeg):
    Return a list of histogram templates for all mT-shape related histograms.
    '''

    # Create empty list for paths to histograms within ROOT file 
    hNameList = []
    # Create empty list for 
    hTemplateList = []

    # Fill the histogram path list 
    folder = "Closure_Shape_QCDfactorised_TradPlusCollinearTailKiller_CtrlMET" + sMyLeg
    hNameList.append( folder + "/" + folder + "_*ErrorType*")

    if sMyLeg == "":
        legendLabel = "Std."
    else:
        legendLabel = sMyLeg.replace("Leg1", "E_{T}^{miss}").replace("Leg2", "#tau_{h}").replace("leg1", "E_{T}^{miss}").replace("leg2", "#tau_{h}").replace("StandardSelections", "Std.").replace("After", "")

    # Fill the histogram template list 
    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "E_{T}^{miss} (GeV)", None, None, False, "Events / %0.f-%0.f GeV", None, None, False, legendLabel))
        
    return hTemplateList

#######################################################################################################
def GetMetBinShapeHistoNames(lBinList, sMyLeg):
    '''
    def GetMetBinShapeHistoNames(sMyLeg):
    Return a list of histogram templates for all mT bin shape related histograms.
    '''

    # Create empty list for paths to histograms within ROOT file 
    hNameList = []
    # Create empty list for 
    hTemplateList = []

    # Fill the histogram-path and histogram-template lists for the list of bins defined by the user
    folder = "Closure_Shape_QCDfactorised_TradPlusCollinearTailKiller_CtrlMET" + sMyLeg

    if sMyLeg == "":
        legendLabel = "Std."
    else:
        legendLabel = sMyLeg.replace("Leg1", "E_{T}^{miss}").replace("Leg2", "#tau_{h}").replace("leg1", "E_{T}^{miss}").replace("leg2", "#tau_{h}").replace("StandardSelections", "Std.").replace("After", "")

        
    tauBinNames = getTauPtBinsDict()        
    for index, myBin in enumerate(lBinList):

        legendLabel  = legendLabel
        legendHeader = tauBinNames[myBin]
        hPath = folder + "/" + folder + "_binInfo%s_*ErrorType*" % (str(myBin)) 
        hTemplateList.append(HistoTemplate(hPath, "E_{T}^{miss} (GeV)", None, None, False, "Events / %0.f-%0.f GeV", None, None, True, legendLabel, legendHeader))

    return hTemplateList

#######################################################################################################
def GetMassShapeHistoNames(sMyLeg):
    '''
    def GetMassShapeHistoNames(sMyLeg):
    Return a list of histogram templates for all full mass shape related histograms.
    '''

    # Create empty list for paths to histograms within ROOT file 
    hNameList = []
    # Create empty list for 
    hTemplateList = []

    # Fill the histogram path list 
    folder = "Ctrl_Shape_QCDfactorised_TradPlusCollinearTailKiller_MassAfter" + sMyLeg
    hNameList.append( folder + "/" + folder + "_*ErrorType*")

    # Fill the histogram template list 
    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "m (#tau_{h}, E_{T}^{miss}) (GeV/c^{2})", None, None, False, "Events / %0.f GeV/c^{2}", None, None, False, None))
    
    return hTemplateList

#######################################################################################################
def GetCtrlNjetsHistoNames():
    '''
    def GetCtrlNjetsHistoNames():
    Return a list of histogram templates for all Njets control histograms.
    '''

    # Create empty list for paths to histograms within ROOT file 
    hNameList = []
    # Create empty list for 
    hTemplateList = []

    # Fill the histogram path list 
    folder = "Ctrl_Shape_QCDfactorised_TradPlusCollinearTailKiller_CtrlNjets"
    hNameList.append( folder + "/" + folder + "_*ErrorType*")

    # Fill the histogram template list 
    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "N^{sel}_{jets}", None, None, False, "Events / %0.f", None, None, True, None))
    
    return hTemplateList

#######################################################################################################
def GetCtrlNbjetsHistoNames():
    '''
    def GetCtrlNbjetsHistoNames():
    Return a list of histogram templates for all Nbjets control histograms.
    '''

    # Create empty list for paths to histograms within ROOT file 
    hNameList = []
    # Create empty list for 
    hTemplateList = []

    # Fill the histogram path list 
    folder = "Ctrl_Shape_QCDfactorised_TradPlusCollinearTailKiller_CtrlNbjets"
    hNameList.append( folder + "/" + folder + "_*ErrorType*")

    # Fill the histogram template list 
    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "N^{sel}_{b-jets}", None, None, False, "Events / %0.f", None, None, True, None))
    
    return hTemplateList

#######################################################################################################
def GetNQcdHistoNames():
    '''
    def GetCtrlNbjetsHistoNames():
    Return a list of histogram templates for all N_{QCD} histograms.
    '''

    # Create empty list for paths to histograms within ROOT file 
    hNameList = []
    # Create empty list for 
    hTemplateList = []

    # Fill the histogram path list 
    hNameList.append("NQCD_*ErrorType*")

    # Fill the histogram template list 
    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "p_{T, #tau_{h}} (GeV/c)", None, None, False, "dN_{QCD} / dp_{T, #tau_{h}}", 1E-04, 1E+02, True, None))

    return hTemplateList

#######################################################################################################
def getTauPtBinsDict():
        
    tauBinDict = {}
    tau   = "  p_{T, #tau_{h}}"
    units = "" #"GeV/c"
    
    tauBinDict[0]  = tau + "< 41 " + units
    tauBinDict[1]  = "41 #leq" + tau  + "< 50 "+ units
    tauBinDict[2]  = "50 #leq" + tau  + "< 60 "+ units
    tauBinDict[3]  = "60 #leq" + tau  + "< 70 "+ units
    tauBinDict[4]  = "70 #leq" + tau  + "< 80 "+ units
    tauBinDict[5]  = "80 #leq" + tau  + "< 100 "+ units
    tauBinDict[6]  = "100 #leq" + tau  + "< 120 "+ units
    tauBinDict[7]  = "120 #leq" + tau  + "< 150 "+ units
    tauBinDict[8]  = "150 #leq" + tau  + "< 200 "+ units
    tauBinDict[9]  = "200 #leq" + tau  + "< 300 "+ units
    tauBinDict[10] = tau + "> 300 " + units
    
    return tauBinDict

######################################################################
def getDataEra(myValidDataEras):

    cwd = os.getcwd()
    myDataEra = None
    
    # Check all valid data-eras
    for era in myValidDataEras:
        if "_" + era + "_" in cwd:
            myDataEra = era
        else:
            continue

    if myDataEra == None:
        print "*** ERROR: Invalid data-era selected. Please select one of the following:\n    %s" %(myValidDataEras)
        sys.exit()
    else:
        return myDataEra

######################################################################
def getLumi(myDataEra):

    # Check if user-defined data-era is allowed
    if myDataEra == "Run2011A":
        myLumi            = 2311.191 #(pb)
    elif myDataEra == "Run2011B":
        myLumi            = 2739 #(pb)
    elif myDataEra == "Run2011AB":
        myLumi            = 5050.191 #(pb)
    else:
        print "*** ERROR: Invalid data-era selected. Please select one of the following:\n    %s" %(myValidDataEras)
        sys.exit()

    return myLumi

######################################################################
def checkUserOptions(QCDscheme, ErrorType):

    myQCDschemes = ["TauPt", "TauEta", "Nvtx", "Full"]    
    myErrorTypes = ["StatAndSyst", "StatOnly"]

    if QCDscheme not in myQCDschemes:
        print "*** ERROR: Invalid QCD factorisation scheme selected. Please select one of the following:\n    %s" %(myQCDschemes)
        sys.exit()
        
    if ErrorType not in myErrorTypes:
        print "*** ERROR: Invalid Error-Type selected. Please select one of the following:\n    %s" %(myFactorisationSchemes)
        sys.exit()
    
    return

######################################################################
def getRootFile(myPath):

    if os.path.exists(myPath):
        print "*** Opening ROOT file \"%s\"" % (myPath)
        f = ROOT.TFile.Open(myPath)
        return f
    else:
        print "*** ERROR: The path \"%s\" defined for the ROOT file is invalid. Please check the path name." % (myPath)
        sys.exit()

######################################################################
def getHisto(rootFile, pathName):
    
    histo = rootFile.Get(pathName)
    if not isinstance(histo, ROOT.TH1):
        print "*** ERROR: Histogram \"%s\" is not a ROOT.TH1 instance. Check that its path is correct." %(pathName)
        sys.exit()
    else:
        return histo

######################################################################
######################################################################
def setLabelOption(p):
   
    
    # See: http://root.cern.ch/root/htmldoc/TAxis.html#TAxis:LabelsOption
    if p.getFrame().GetXaxis().GetLabels() == None:
        return
    else:
        p.getFrame().GetXaxis().LabelsOption("u") #"h", "v" "d" "u"
        p.getFrame().GetXaxis().SetLabelSize(14.5) #"h", "v" "d" "u"
        
    return

######################################################################    
def setHistoStyle(histo, counter):
    
    # Since the list of supported styles/colours contains 12 entries, if counter goes out of scope it
    if counter > 11:
        counter = 0
        
    myColours = [ROOT.kRed+1, ROOT.kAzure+1, ROOT.kOrange+1, ROOT.kViolet+1, ROOT.kMagenta+1, ROOT.kGreen+3, 
                 ROOT.kRed-7, ROOT.kOrange-7, ROOT.kGreen-5, ROOT.kAzure-7,  ROOT.kViolet-7, ROOT.kMagenta-7]

    myMarkerStyles = [ROOT.kFullCircle, ROOT.kFullSquare, ROOT.kFullTriangleUp, ROOT.kFullTriangleDown, ROOT.kStar, ROOT.kPlus, ROOT.kCircle, 
                      ROOT.kOpenCircle, ROOT.kOpenSquare, ROOT.kOpenTriangleUp, ROOT.kOpenCross, ROOT.kDot]

    myLineStyles = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] #[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2]

    histo.SetMarkerColor(myColours[counter])
    histo.SetMarkerColor(myColours[counter])
    histo.SetMarkerStyle(myMarkerStyles[counter])
    histo.SetMarkerSize(1.2)

    histo.SetLineColor(myColours[counter])
    histo.SetLineStyle(myLineStyles[counter]);
    histo.SetLineWidth(2);

    histo.SetFillStyle(3001)
    histo.SetFillColor(myColours[counter])
    
    return histo

######################################################################
def createPlot(histo, myLumi, legendLabel, sLegStyle, sDrawStyle, **kwargs):
    
    style      = tdrstyle.TDRStyle()

    if isinstance(histo, ROOT.TH1):
        args = {"legendStyle": sLegStyle, "drawStyle": sDrawStyle}
        args.update(kwargs)
        histo.GetZaxis().SetTitle("")
        #p = plots.PlotBase([histograms.Histo(histo, legendLabel, **args)])
        p = plots.ComparisonManyPlot(histograms.Histo(histo, legendLabel, **args), [])
        p.setLuminosity(myLumi)
        return p
    else:
        print "*** ERROR: Histogram \"%s\" is not a valid instance of a ROOT.TH1" % (histo)
        sys.exit()

######################################################################
def customizePlot(logY, addLuminosityText, ratio, ratioInvert, ratioYlabel, yMin, yMax, yMaxFactor, yMinRatio, yMaxRatio, yMinLog, yMaxFactorLog):

    # Customise the plot. Use custom y-axis range only if defined in the HistoTemplate creation
    if yMin == None or yMax == None:
        drawPlot = plots.PlotDrawer(log=logY, addLuminosityText=True, opts={"ymaxfactor": yMaxFactor}, opts2={"ymin": yMinRatio, "ymax": yMaxRatio}, optsLog={"ymin": yMinLog, "ymaxfactor": yMaxFactorLog})
    else:
        drawPlot = plots.PlotDrawer(log=logY, addLuminosityText=True, opts={"ymin": yMin, "ymax": yMax}, opts2={"ymin": yMinRatio, "ymax": yMaxRatio}, optsLog={"ymin": yMin, "ymax": yMax})

    return drawPlot

######################################################################
def getTailKillerFromDir(myTailKillers):

    scenario = None
    for tailKiller in myTailKillers:
        if tailKiller in os.getcwd():
            scenario = tailKiller
        else:
            continue

    if scenario == None:
        print "*** ERROR: Could not determine a Tail-Killer from the current working directory"
        sys.exit()
    else:
        return scenario

######################################################################
def getTailKillerDir(myTailKillers, myDataEra):
    
    myDirsDict = {}
    for tailKiller in myTailKillers:
        for dirName in os.walk('.').next()[1]: 
            if ("_" + myDataEra  + "_") not in dirName:
                continue
            else:
                if tailKiller in dirName:
                    myDirsDict[tailKiller] = dirName
                    #print "*** tailKiller = %s , dirName = %s" % (tailKiller, dirName)
                else:
                    continue

    if len(myDirsDict) < 1:
        print "*** ERROR: No valid Tail-Killer directory was found in the current working directory. Check that the Tail-Killer scenarios are valid. %s" % (myTailKillers)
        sys.exit()
    else:
        return myDirsDict

######################################################################
def getFullSaveName(myDataEra, myTailKiller, bNormalizeToOne, mySaveName):
    
    if mySaveName == None:
        saveName = myDataEra + "_" + histoName
        saveName = saveName.replace("/", "__")
    else:
        saveName = myDataEra + "_" + mySaveName
    
    saveName = saveName.replace("Leg1", "MetLeg").replace("Leg2", "TauLeg").replace("leg1", "MetLeg").replace("leg2", "TauLeg")
    
    if myTailKiller is not None:
        saveName = saveName + "_" + myTailKiller

    if bNormalizeToOne == True:
        saveName = saveName + "_normalizedToOne"

    return saveName

######################################################################
def getHistoNameAndPath(QCDscheme, ErrorType, h):
    
    # First take care of the histogram name
    histoName = h.name.replace("*QcdScheme*", QCDscheme).replace("*ErrorType*", ErrorType)
    # Temporary quick-fix to naming difference
    if "Shape_" in histoName:
        histoName = histoName.replace("StatAndSyst", "fullUncert").replace("StatOnly", "statUncert") 

    # Then create the histogram path 
    folderName = "Contraction_" + QCDscheme
    pathName   = folderName + "/" + histoName

    return pathName, histoName

######################################################################

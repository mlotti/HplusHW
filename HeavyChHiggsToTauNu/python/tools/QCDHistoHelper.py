#######################################################################################################
# HistoHelper module: 
# To be used in parallel with a plotting script, such as "plotHisto_DataMinusEwk_Template.py".
#
# The primary goal of this module is to have a clean way of plotting several histograms, 
# each with customised setting on x-label, y-label, and binWidthX. Future additionals would 
# be staight-forwards with the appropriate expansion of the __init__ module. Each histogram requires
# name, a histogram path (in ROOT file), an x-label, a y-label and a binWidthX which defines the 
# desirable bin width in the x-axis. Therefore, to add a new histogram in 
# the plotting loop one needs create a new HistoTemplate class instance with all aforementioned qualities
# and add it (i.e. append it) to the HistoTemplateList to be plotted automatically.
# In order to remove/exclude a histogram from the plotting loop just do not append it in this list.

# NOTE: Please do not change this file. Copy it and re-name it.
#       Remember to include this file in your plotting script, such as "plotHisto_DataMinusEwk_Template.py".
#       Suggestions are more than welcome.
#######################################################################################################
class HistoTemplate:
    '''
    class HistoTemplate():
    Define the histogram names, their path in ROOT files, xLabels, yLabels and binWidthX. 
    '''

    def __init__(self, name, xLabel, xMin, xMax, bLogX, yLabel, yMin, yMax, bLogY, legendLabel):
        # name: Define histogram name
        # path: Define histogram path in ROOT file
        # xMin, xMax: Overwrite the default x-axis range
        # yMin, yMax: Overwrite the default y-axis range
        
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

#######################################################################################################
def GetPurityHistoNames():
    hTemplateList = []
    hNameList = []

    # *QcdScheme* = ["TauPt", "TauEta", "Nvtx", "Full"]
    # *Error*     = ["StatAndSyst", "StatOnly"]

    hNameList.append("Purity_*QcdScheme*_*ErrorType*_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterStandardSelections")
    hNameList.append("Purity_*QcdScheme*_*ErrorType*_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterLeg1")
    hNameList.append("Purity_*QcdScheme*_*ErrorType*_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterLeg2")

    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "p_{T, #tau_{h}} (GeV/c)", -1, -1, False, "Purity", 0.0, 1.0, False, None))

    return hTemplateList

#######################################################################################################
def GetEfficiencyHistoNames():
    hTemplateList = []
    hNameList = []

    hNameList.append("Efficiency_leg1_*QcdScheme*_*ErrorType*_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterStandardSelections")
    hNameList.append("Efficiency_leg2_*QcdScheme*_*ErrorType*_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterStandardSelections")

    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "p_{T, #tau_{h}} (GeV/c)", -1, -1, False, "Efficiency", 1E-03, 1E-01, True, None))

    return hTemplateList

#######################################################################################################
def GetNEventsHistoNames():
    hTemplateList = []
    hNameList = []



    hNameList.append("Nevents_*QcdScheme*_*ErrorType*_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterStandardSelections")
    hNameList.append("Nevents_*QcdScheme*_*ErrorType*_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterLeg1")
    hNameList.append("Nevents_*QcdScheme*_*ErrorType*_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterLeg2")

    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "p_{T, #tau_{h}} (GeV/c)", -1, -1, False, "dN_{QCD} / dp_{T, #tau_{h}}", 0.0, 10.0, False, None))

    return hTemplateList

#######################################################################################################
def GetMtShapeHistoNames():
    hTemplateList = []
    hNameList = []

    folder = "Shape_*QcdScheme*_QCDfactorised_TradPlusCollinearTailKiller_MtAfterLeg1"
    hNameList.append( folder + "/" + folder + "_*ErrorType*")

    for h in hNameList:
        #hTemplateList.append(HistoTemplate(h, "m_{T}(#tau_{h}, E_{T}^{miss}) (GeV/c^{2})", -1, -1, False, "Events / %0.f GeV/c^{2}", 0.0, 10.0, False, None))
        hTemplateList.append(HistoTemplate(h, "m_{T}(#tau_{h}, E_{T}^{miss}) (GeV/c^{2})", -1, -1, False, "Events / 20-200 GeV/c^{2}", 0.0, 10.0, False, None))
    
    return hTemplateList

#######################################################################################################
def GetMtShapeBinHistoNames():
    hTemplateList = []
    hNameList = []

    folder = "Shape_*QcdScheme*_QCDfactorised_TradPlusCollinearTailKiller_MtAfterLeg1"
    hNameList.append( folder + "/" + folder + "_binInfo0_*ErrorType*")
    hNameList.append( folder + "/" + folder + "_binInfo1_*ErrorType*")
    hNameList.append( folder + "/" + folder + "_binInfo2_*ErrorType*")
    hNameList.append( folder + "/" + folder + "_binInfo3_*ErrorType*")
    hNameList.append( folder + "/" + folder + "_binInfo4_*ErrorType*")
    hNameList.append( folder + "/" + folder + "_binInfo5_*ErrorType*")
    hNameList.append( folder + "/" + folder + "_binInfo6_*ErrorType*")
    hNameList.append( folder + "/" + folder + "_binInfo7_*ErrorType*")
    hNameList.append( folder + "/" + folder + "_binInfo8_*ErrorType*")
    hNameList.append( folder + "/" + folder + "_binInfo9_*ErrorType*")
    hNameList.append( folder + "/" + folder + "_binInfo10_*ErrorType*")
    
    counter = 0
    for h in hNameList:
        #hTemplateList.append(HistoTemplate(h, "m_{T}(#tau_{h}, E_{T}^{miss}) (GeV/c^{2})", -1, -1, False, "Events / %0.f GeV/c^{2}", 0.0, 10.0, False, "bin " + str(counter)))
        hTemplateList.append(HistoTemplate(h, "m_{T}(#tau_{h}, E_{T}^{miss}) (GeV/c^{2})", -1, -1, False, "Events / 20-200 GeV/c^{2}", 0.0, 10.0, False, "bin " + str(counter)))
        counter = counter +1 

    return hTemplateList

#######################################################################################################
def GetMassShapeHistoNames():
    hTemplateList = []
    hNameList = []

    folder = "Shape_*QcdScheme*_QCDfactorised_TradPlusCollinearTailKiller_MassAfterLeg1"
    hNameList.append( folder + "/" + folder + "_*ErrorType*")

    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "m (#tau_{h}, E_{T}^{miss}) (GeV/c^{2})", -1, -1, False, "Events / %0.f GeV/c^{2}", 0.0, 10.0, False, None))
    
    return hTemplateList

#######################################################################################################
def GetCtrlNjetsHistoNames():
    hTemplateList = []
    hNameList = []

    folder = "Shape_*QcdScheme*_QCDfactorised_TradPlusCollinearTailKiller_CtrlNjets"
    hNameList.append( folder + "/" + folder + "_*ErrorType*")

    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "N^{sel}_{jets}", -1, -1, False, "Events / %0.f", 0.0, 5E+03, False, None))
    
    return hTemplateList

#######################################################################################################
def GetCtrlNbjetsHistoNames():
    hTemplateList = []
    hNameList = []

    folder = "Shape_*QcdScheme*_QCDfactorised_TradPlusCollinearTailKiller_CtrlNbjets"
    hNameList.append( folder + "/" + folder + "_*ErrorType*")

    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "N^{sel}_{b-jets}", -1, -1, False, "Events / %0.f", 0.0, 5E+03, False, None))
    
    return hTemplateList


#######################################################################################################
def GetNQcdHistoNames():
    hTemplateList = []
    hNameList = []

    hNameList.append("NQCD_*QcdScheme*_*ErrorType*")

    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "p_{T, #tau_{h}} (GeV/c)", -1, -1, False, "dN_{QCD} / dp_{T, #tau_{h}}", 1E-03, 1E+02, True, None))

    return hTemplateList

#######################################################################################################
def GetEntireHistoList():
    
    # Create lists of histograms to be created
    EfficiencyList  = GetEfficiencyHistoNames()
    PurityList      = GetPurityHistoNames()
    NQcdHistoList   = GetNQcdHistoNames()
    NEvtsList       = GetNEventsHistoNames()
    MtShapeList     = GetMtShapeHistoNames() + GetMtShapeBinHistoNames()
    MassShapeList   = GetMassShapeHistoNames()
    CtrlNjetsList   = GetCtrlNjetsHistoNames()
    CtrlNbjetsList  = GetCtrlNbjetsHistoNames()

    # Define & Get the list of histograms to be plotted
    hTemplateList = []
    hTemplateList = NQcdHistoList + PurityList + EfficiencyList + NEvtsList + MtShapeList + MassShapeList + CtrlNjetsList + CtrlNbjetsList
    
    return hTemplateList
#######################################################################################################

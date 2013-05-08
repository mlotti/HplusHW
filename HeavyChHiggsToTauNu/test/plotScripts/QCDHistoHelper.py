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

    hNameList.append("Purity_StatOnly_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterStandardSelections")
    hNameList.append("Purity_StatAndSyst_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterStandardSelections")
    hNameList.append("Purity_StatOnly_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterLeg1")
    hNameList.append("Purity_StatAndSyst_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterLeg1")
    hNameList.append("Purity_StatOnly_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterLeg2")
    hNameList.append("Purity_StatAndSyst_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterLeg2")

    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "p_{T}^{#tau-jet} (GeV/c)", -1, -1, False, "Purity", 0.0, 1.0, False, None))

    return hTemplateList

#######################################################################################################
def GetEfficiencyHistoNames():
    hTemplateList = []
    hNameList = []

    hNameList.append("Efficiency_leg1_StatOnly_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterStandardSelections")
    hNameList.append("Efficiency_leg1_StatAndSyst_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterStandardSelections")
    hNameList.append("Efficiency_leg2_StatOnly_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterStandardSelections")
    hNameList.append("Efficiency_leg2_StatAndSyst_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterStandardSelections")

    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "p_{T}^{#tau-jet} (GeV/c)", -1, -1, False, "Efficiency", 1E-03, 1E-01, True, None))

    return hTemplateList

#######################################################################################################
def GetNEventsHistoNames():
    hTemplateList = []
    hNameList = []

    hNameList.append("Nevents_StatOnly_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterStandardSelections")
    hNameList.append("Nevents_StatAndSyst_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterStandardSelections")
    hNameList.append("Nevents_StatOnly_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterLeg1")
    hNameList.append("Nevents_StatAndSyst_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterLeg1")
    hNameList.append("Nevents_StatOnly_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterLeg2")
    hNameList.append("Nevents_StatAndSyst_QCDfactorised_TradPlusCollinearTailKiller_NevtAfterLeg2")

    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "p_{T}^{#tau-jet} (GeV/c)", -1, -1, False, "dN_{QCD} / dp_{T}^{#tau-jet}", 0.0, 10.0, False, None))

    return hTemplateList

#######################################################################################################
def GetShapeHistoNames():
    hTemplateList = []
    hNameList = []

    #hNameList.append("Shape_QCDfactorised_TradPlusCollinearTailKiller_MtAfterLeg1/Shape_QCDfactorised_TradPlusCollinearTailKiller_MtAfterLeg1_statUncert")
    #hNameList.append("Shape_QCDfactorised_TradPlusCollinearTailKiller_MtAfterLeg1/Shape_QCDfactorised_TradPlusCollinearTailKiller_MtAfterLeg1_fullUncert")
    hNameList.append("Shape_QCDfactorised_TradPlusCollinearTailKiller_CtrlNJets/Shape_QCDfactorised_TradPlusCollinearTailKiller_CtrlNJets_statUncert")
    hNameList.append("Shape_QCDfactorised_TradPlusCollinearTailKiller_CtrlNJets/Shape_QCDfactorised_TradPlusCollinearTailKiller_CtrlNJets_fullUncert")

    for h in hNameList:
        hTemplateList.append(HistoTemplate(h, "m_{T} (GeV/c^{2})", -1, -1, False, "Events / bin", 0.0, 100.0, False, None))
    
    return hTemplateList

#######################################################################################################
def GetNQcdHistoNames():
    hTemplateList = []
    hNameList = []

    hNameList.append("NQCD_StatOnly")
    hNameList.append("NQCD_StatAndSyst")

    for h in hNameList:
        #hTemplateList.append(HistoTemplate(h, "p_{T}^{#tau-jet} (GeV/c)", -1, -1, False, "dN_{QCD} / dp_{T}^{#tau-jet}", 0.0, 10.0, False, None))
        hTemplateList.append(HistoTemplate(h, "p_{T}^{#tau-jet} (GeV/c)", -1, -1, False, "dN_{QCD} / dp_{T}^{#tau-jet}", 1E-03, 10.0, True, None))

    return hTemplateList

#######################################################################################################
def GetHistoList():
    
    hTemplateList = []
    NQcdHistoList = GetNQcdHistoNames()
    PurityList = GetPurityHistoNames()
    EfficiencyList = GetEfficiencyHistoNames()
    NEvtsList = GetNEventsHistoNames() #not yet fully functional
    ShapeList  = GetShapeHistoNames() #not yet functional

    hTemplateList = NQcdHistoList + PurityList + EfficiencyList
    #hTemplateList = NQcdHistoList + PurityList + EfficiencyList + NEvtsList + ShapeList
    
    return hTemplateList
#######################################################################################################

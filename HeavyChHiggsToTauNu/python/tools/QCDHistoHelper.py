#######################################################################################################
# QCDHistoHelper module
#######################################################################################################
class HistoTemplate:
    '''
    class HistoTemplate():
    Define all attribues of the histogram, including names, x- and y-Labels, x- and y- axis min and max etc..
    '''

    def __init__(self, name, xLabel, xMin, xMax, bLogX, yLabel, yMin, yMax, bLogY, legendLabel):
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

    for index, myBin in enumerate(lBinList):
        legendLabel = legendLabel + " (bin " + str(myBin) + ")"
        hPath = folder + "/" + folder + "_binInfo%s_*ErrorType*" % (str(myBin)) 
        hTemplateList.append(HistoTemplate(hPath, "m_{T}(#tau_{h}, E_{T}^{miss}) (GeV/c^{2})", None, None, False, "Events / 20-200 GeV/c^{2}", None, None, False, legendLabel))

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

        
    for index, myBin in enumerate(lBinList):
        legendLabel = legendLabel + " (bin " + str(myBin) + ")"
        hPath = folder + "/" + folder + "_binInfo%s_*ErrorType*" % (str(myBin)) 
        hTemplateList.append(HistoTemplate(hPath, "E_{T}^{miss} (GeV)", None, None, False, "Events / %0.f-%0.f GeV", None, None, True, legendLabel))

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

#######################################################################################################
# HistoHelper module: 
# To be used in parallel with a plotting script, such as "plotHisto_DataMinusEwk_Template.py".
#
# The primary goal of this module is to have a clean way of plotting several histograms, 
# each with customised setting on x-label, y-label, and binWidthX. Future additionals would 
# be staight-forwards with the declaration of an appropriate dictionary. Each histogram is 
# uniquely defined with a dictionary key. This key maps all options like histogram path (in ROOT file), 
# x-label, y-label and binWidthX to a single histogram. Therefore, to add a new histogram in 
# the plotting loop one needs to add a new entry to all dictionaries with the same key in the 
# form Dict = {key: value}. All the histograms defined in histoDict are plotted automatically.
# In order to remove a histogram from the plotting loop a simple commenting of the relevant 
# line in histoDict is enough.

# NOTE: Please do not change this file. Copy it and re-name it. 
#       Remember to include this it in your plotting instead of "HistoHelper.py"
#       Suggestions are more than welcome.
#######################################################################################################
def GetDictionaries():
    '''
    def GetDictionaries():
    Define the histogram names, their path in ROOT files, xLabels, yLabels and binWidths. 
    These are all mapped to a unique histogram name key.
    '''

    ### Define histogram name and path in ROOT file. All entries in this dictionaries will be plotted! 
    ### histoDict = {"Histo_Key": "path_In_ROOT_File"}
    histoDict = {
        "HiggsMass": "FullHiggsMass/HiggsMass",
        #"HiggsMass_GEN": "FullHiggsMass/HiggsMass_GEN",
        #"HiggsMass_GEN_NeutrinosReplacedWithMET": "FullHiggsMass/HiggsMass_GEN_NeutrinosReplacedWithMET",
        #"Discriminant": "FullHiggsMass/Discriminant",
        #"Discriminant_GEN": "FullHiggsMass/Discriminant_GEN",
        #"Discriminant_GEN_NeutrinosReplacedWithMET": "FullHiggsMass/Discriminant_GEN_NeutrinosReplacedWithMET",
        #"TransMass_Vs_InvMass": "FullHiggsMass/TransMassVsInvMass",
        "HiggsMass_greater": "FullHiggsMass/HiggsMass_greater",
        "HiggsMass_smaller": "FullHiggsMass/HiggsMass_smaller",
        "HiggsMass_tauNuAngleMax": "FullHiggsMass/HiggsMass_tauNuAngleMax",
        "HiggsMass_tauNuAngleMin": "FullHiggsMass/HiggsMass_tauNuAngleMin",
        "HiggsMass_tauNuDeltaEtaMax": "FullHiggsMass/HiggsMass_tauNuDeltaEtaMax",
        "HiggsMass_tauNuDeltaEtaMin": "FullHiggsMass/HiggsMass_tauNuDeltaEtaMin",
        #"HiggsMass_GEN_greater": "FullHiggsMass/HiggsMass_GEN_greater",
        #"HiggsMass_GEN_smaller": "FullHiggsMass/HiggsMass_GEN_smaller",
        #"HiggsMass_GEN_tauNuAngleMax": "FullHiggsMass/HiggsMass_GEN_tauNuAngleMax",
        #"HiggsMass_GEN_tauNuAngleMin": "FullHiggsMass/HiggsMass_GEN_tauNuAngleMin",
        #"HiggsMass_GEN_tauNuDeltaEtaMax": "FullHiggsMass/HiggsMass_GEN_tauNuDeltaEtaMax",
        #"HiggsMass_GEN_tauNuDeltaEtaMin": "FullHiggsMass/HiggsMass_GEN_tauNuDeltaEtaMin",
        #"HiggsMass_GEN_NuToMET_greater": "FullHiggsMass/HiggsMass_GEN_NuToMET_greater",
        #"HiggsMass_GEN_NuToMET_smaller": "FullHiggsMass/HiggsMass_GEN_NuToMET_smaller",
        #"HiggsMass_GEN_NuToMET_tauNuAngleMax": "FullHiggsMass/HiggsMass_GEN_NuToMET_tauNuAngleMax",
        #"HiggsMass_GEN_NuToMET_tauNuAngleMin": "FullHiggsMass/HiggsMass_GEN_NuToMET_tauNuAngleMin",
        #"HiggsMass_GEN_NuToMET_tauNuDeltaEtaMax": "FullHiggsMass/HiggsMass_GEN_NuToMET_tauNuDeltaEtaMax",
        #"HiggsMass_GEN_NuToMET_tauNuDeltaEtaMin": "FullHiggsMass/HiggsMass_GEN_NuToMET_tauNuDeltaEtaMin",
        #"TopMassSolution": "FullHiggsMass/TopMassSolution",
        #"SelectedNeutrinoPzSolution": "FullHiggsMass/SelectedNeutrinoPzSolution",
        #"HiggsMassPure": "FullHiggsMass/HiggsMassPure",
        #"HiggsMassImpure": "FullHiggsMass/HiggsMassImpure",
        #"HiggsMassBadTau": "FullHiggsMass/HiggsMassBadTau",
        #"HiggsMassBadMET": "FullHiggsMass/HiggsMassBadMET",
        #"HiggsMassBadTauAndMET": "FullHiggsMass/HiggsMassBadTauAndMET",
        #"HiggsMassBadBjet": "FullHiggsMass/HiggsMassBadBjet",
        #"HiggsMassBadBjetAndTau": "FullHiggsMass/HiggsMassBadBjetAndTau",
        #"HiggsMassBadBjetAndMET": "FullHiggsMass/HiggsMassBadBjetAndMET",
        #"HiggsMassBadBjetAndMETAndTau": "FullHiggsMass/HiggsMassBadBjetAndMETAndTau",
        #"DiscriminantPure": "FullHiggsMass/DiscriminantPure",
        #"DiscriminantImpure": "FullHiggsMass/DiscriminantImpure",
        #"NeutrinosTauAngle1": "FullHiggsMass/NeutrinosTauAngle1",
        #"NeutrinosTauAngle2": "FullHiggsMass/NeutrinosTauAngle2",
        }
    
    ### Define histogram name, expression, and binning here: "hName": "xLabel"
    ### xLabelDict = {"Histo_Key": "X_Axis_Label"}
    xLabelDict = {
        "HiggsMass": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_GEN": "m_{H^{#pm}} (#tau^{GEN}, #nu_{#tau}^{GEN}) (GeV/c^2)",
        "HiggsMass_GEN_NeutrinosReplacedWithMET": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "Discriminant": "D",
        "Discriminant_GEN": "D^{GEN}",
        "Discriminant_GEN_NeutrinosReplacedWithMET": "D^{GEN}_{#nu #rightarrow E_{T}^{miss}}",
        "TransMass_Vs_InvMass": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_greater": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_smaller": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_tauNuAngleMax": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_tauNuAngleMin": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_tauNuDeltaEtaMax": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_tauNuDeltaEtaMin": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_GEN_greater": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_GEN_smaller": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_GEN_tauNuAngleMax": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_GEN_tauNuAngleMin": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_GEN_tauNuDeltaEtaMax": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_GEN_tauNuDeltaEtaMin": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_GEN_NuToMET_greater": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_GEN_NuToMET_smaller": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_GEN_NuToMET_tauNuAngleMax": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_GEN_NuToMET_tauNuAngleMin": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_GEN_NuToMET_tauNuDeltaEtaMax": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMass_GEN_NuToMET_tauNuDeltaEtaMin": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "TopMassSolution": "TopMassSolution",
        "SelectedNeutrinoPzSolution": "#nu p_{z} solution",
        "HiggsMassPure": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMassImpure": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMassBadTau": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMassBadMET": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMassBadTauAndMET": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMassBadBjet": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMassBadBjetAndTau": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMassBadBjetAndMET": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "HiggsMassBadBjetAndMETAndTau": "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)",
        "DiscriminantPure": "D_{pure}",
        "DiscriminantImpure": "D_{impure}",
        "NeutrinosTauAngle1": "Angle(#nu, #tau)_{1}",
        "NeutrinosTauAngle2": "Angle(#nu, #tau)_{2}",
        }
    
    ### Define histogram name, expression, and binning here: "hName": "yLabel"
    ### xLabelDict = {"Histo_Key": "Y_Axis_Label"}
    yLabelDict = {
        "HiggsMass": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_GEN": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_GEN_NeutrinosReplacedWithMET": "Events / %0.0f GeV/c^{2}",
        "Discriminant": "Events / %0.0f",
        "Discriminant_GEN": "Events / %0.0f",
        "Discriminant_GEN_NeutrinosReplacedWithMET": "Events / %0.1f",
        "TransMass_Vs_InvMass": "m_{T} (#tau-jet, E_{T}^{miss} GeV/c^2)",
        "HiggsMass_greater": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_smaller": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_tauNuAngleMax": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_tauNuAngleMin": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_tauNuDeltaEtaMax": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_tauNuDeltaEtaMin": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_GEN_greater": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_GEN_smaller": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_GEN_tauNuAngleMax": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_GEN_tauNuAngleMin": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_GEN_tauNuDeltaEtaMax": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_GEN_tauNuDeltaEtaMin": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_GEN_NuToMET_greater": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_GEN_NuToMET_smaller": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_GEN_NuToMET_tauNuAngleMax": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_GEN_NuToMET_tauNuAngleMin": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_GEN_NuToMET_tauNuDeltaEtaMax": "Events / %0.0f GeV/c^{2}",
        "HiggsMass_GEN_NuToMET_tauNuDeltaEtaMin": "Events / %0.0f GeV/c^{2}",
        "TopMassSolution": "Events / %0.0f GeV/c^{2}",
        "SelectedNeutrinoPzSolution": "Events / %0.0f GeV/c^{2}",
        "HiggsMassPure": "Events / %0.0f GeV/c^{2}",
        "HiggsMassImpure": "Events / %0.0f GeV/c^{2}",
        "HiggsMassBadTau": "Events / %0.0f GeV/c^{2}",
        "HiggsMassBadMET": "Events / %0.0f GeV/c^{2}",
        "HiggsMassBadTauAndMET": "Events / %0.0f GeV/c^{2}",
        "HiggsMassBadBjet": "Events / %0.0f GeV/c^{2}",
        "HiggsMassBadBjetAndTau": "Events / %0.0f GeV/c^{2}",
        "HiggsMassBadBjetAndMET": "Events / %0.0f GeV/c^{2}",
        "HiggsMassBadBjetAndMETAndTau": "Events / %0.0f GeV/c^{2}",
        "DiscriminantPure": "Events / %0.0f",
        "DiscriminantImpure": "Events / %0.0f",
        "NeutrinosTauAngle1": "Events / %0.1f",
        "NeutrinosTauAngle2": "Events / %0.1f",
        }
            
    ### Define histogram name, expression, and binning here: "hName": "xLabel"
    ### xLabelDict = {"Histo_Key": "X_Axis_Bin_Width"}
    binWidthXDict = {
        "HiggsMass": 20,
        "HiggsMass_GEN": 20,
        "HiggsMass_GEN_NeutrinosReplacedWithMET": 20,
        "Discriminant": -1,
        "Discriminant_GEN": -1,
        "Discriminant_GEN_NeutrinosReplacedWithMET": -1,
        "TransMass_Vs_InvMass": -1,
        "HiggsMass_greater": 20,
        "HiggsMass_smaller": 20,
        "HiggsMass_tauNuAngleMax": 20,
        "HiggsMass_tauNuAngleMin": 20,
        "HiggsMass_tauNuDeltaEtaMax": 20,
        "HiggsMass_tauNuDeltaEtaMin": 20,
        "HiggsMass_GEN_greater": -1,
        "HiggsMass_GEN_smaller": -1,
        "HiggsMass_GEN_tauNuAngleMax": -1,
        "HiggsMass_GEN_tauNuAngleMin": -1,
        "HiggsMass_GEN_tauNuDeltaEtaMax": -1,
        "HiggsMass_GEN_tauNuDeltaEtaMin": -1,
        "HiggsMass_GEN_NuToMET_greater": -1,
        "HiggsMass_GEN_NuToMET_smaller": -1,
        "HiggsMass_GEN_NuToMET_tauNuAngleMax": -1,
        "HiggsMass_GEN_NuToMET_tauNuAngleMin": -1,
        "HiggsMass_GEN_NuToMET_tauNuDeltaEtaMax": -1,
        "HiggsMass_GEN_NuToMET_tauNuDeltaEtaMin": -1,
        "TopMassSolution": -1,
        "SelectedNeutrinoPzSolution": -1,
        "HiggsMassPure": 20,
        "HiggsMassImpure": 20,
        "HiggsMassBadTau": 20,
        "HiggsMassBadMET": 20,
        "HiggsMassBadTauAndMET": 20,
        "HiggsMassBadBjet": 20,
        "HiggsMassBadBjetAndTau": 20,
        "HiggsMassBadBjetAndMET": 20,
        "HiggsMassBadBjetAndMETAndTau": 20,
        "DiscriminantPure": -1,
        "DiscriminantImpure": -1,
        "NeutrinosTauAngle1": -1,
        "NeutrinosTauAngle2": -1,
        }

    return histoDict, xLabelDict, yLabelDict, binWidthXDict

#######################################################################################################
def StartProgressBar(maxValue):
    ''' 
    def StartProgressBar(maxValue):
    Simple module to create and initialise a progress bar. The argument "maxvalue" refers to the 
    total number of tasks to be completed. This must be defined at the start of the progress bar.
    '''
    import progressbar

    widgets = [progressbar.FormatLabel(''), ' ', progressbar.Percentage(), ' ', progressbar.Bar('+'), ' ', progressbar.RotatingMarker()]
    pBar = progressbar.ProgressBar(widgets=widgets, maxval=maxValue)

    if pBar.start_time is None:
        pBar.start()

    return pBar

#######################################################################################################
def printPSet(bPrintPset, folderName):
    '''
    def printPSet():
    Simple module that prints the parameters set in running the analysis
    '''
    if bPrintPset:
        from ROOT import gROOT
        gDirectory = gROOT.GetGlobal("gDirectory")
        named = gDirectory.Get("%s/parameterSet" % (folderName))
        raw_input("*** Press \"ENTER\" key to continue: ")
        print named.GetTitle()
        raw_input("*** Press \"ENTER\" key to continue: ")
    else:
        return

#######################################################################################################

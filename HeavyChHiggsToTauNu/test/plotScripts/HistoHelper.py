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
class HistoTemplate:
    '''
    class HistoTemplate():
    Define the histogram names, their path in ROOT files, xLabels, yLabels and binWidthX. 
    '''

    def __init__(self, name, path, xlabel, ylabel, binWidthX):
        # name: Define histogram name
        # path: Define histogram path in ROOT file
        # xlabel: the xlabel for histogram. Set to None if you want the original label to be used)
        # binWidthX: the bin-width of x-axis for histogram. Set to None if you want the original width to be used)
        
        self.name      = name
        self.path      = path
        self.xlabel    = xlabel
        self.ylabel    = ylabel
        self.binWidthX = binWidthX

#######################################################################################################
HistoTemplateList = []

### Define Histograms and their attributes here
HiggsMass         = HistoTemplate("HiggsMass", "FullHiggsMass/HiggsMass", "m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)", "Events / %0.0f GeV/c^{2}", 20)
HiggsMass_greater = HistoTemplate("HiggsMass_greater", "FullHiggsMass/HiggsMass_greater","m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)", "Events / %0.0f GeV/c^{2}", 20)
HiggsMass_smaller = HistoTemplate("HiggsMass_smaller", "FullHiggsMass/HiggsMass_smaller","m_{H^{#pm}} (#tau-jet, #nu_{#tau}) (GeV/c^2)", "Events / %0.0f GeV/c^{2}", 20)

### Add/Remove Histograms to be plotted/considered here
HistoTemplateList.append(HiggsMass)
HistoTemplateList.append(HiggsMass_greater)
HistoTemplateList.append(HiggsMass_smaller)
#######################################################################################################

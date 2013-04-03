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

    def __init__(self, name, path, xlabel, ylabel, binWidthX):
        # name: Define histogram name
        # path: Define histogram path in ROOT file
        # xlabel: the xlabel for histogram. Set it to "None" if you want the original label to be used.
        # binWidthX: the bin-width of x-axis for histogram. Set it to "None" if you want the original width to be used.
        
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

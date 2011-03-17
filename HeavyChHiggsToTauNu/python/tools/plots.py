## \package tools.plots
# Plot utilities and classes
#
# The package is intended to gather the following commonalities in the
# plots of H+ analysis (signal analysis, QCD and EWK background
# analyses)
# - Dataset merging (see plots._datasetMerge)
# - Dataset order (see plots._datasetOrder)
# - Dataset legend labels (see plots._legendLabels)
# - Dataset plot styles (see plots._plotStyles)
# - Various datasets.DatasetManager operations (see plots.mergeRenameReorderForDataMC())
# - Various histograms.HistoManager operations (see plots.PlotBase and the derived classes)
#
# The intended usage is to first construct datasets.DatasetManager as
# usual, then call plots.mergeRenameReorderForDataMC() and then
# construct an object of the appropriate plots.PlotBase derived class.
# Further customisations and operations should be done via the
# interface of the plots.PlotBase derived class, or directly with the
# histograms.HistoManager object contained by the plot object (via
# histoMgr member).

import ROOT
import array

import dataset
import histograms
import styles

## Map the physical dataset names to logical names
#
# Map the physical dataset names (in multicrab.cfg) to logical names
# used in plots._legendLabels and plots._plotStyles. The mapping is
# used in the mergeRenameReorderForDataMC() function.
_physicalToLogical = {
    "TTToHplusBWB_M90_Winter10":  "TTToHplusBWB_M90", 
    "TTToHplusBWB_M100_Winter10": "TTToHplusBWB_M100",
    "TTToHplusBWB_M120_Winter10": "TTToHplusBWB_M120",
    "TTToHplusBWB_M140_Winter10": "TTToHplusBWB_M140",
    "TTToHplusBWB_M160_Winter10": "TTToHplusBWB_M160",

    "TTJets_TuneD6T_Winter10": "TTJets",
    "TTJets_TuneZ2_Winter10": "TTJets",

    "WJets_TuneD6T_Winter10": "WJets",
    "WJets_TuneZ2_Winter10": "WJets",
    "WJets_TuneZ2_Winter10_noPU": "WJets",

    "DYJetsToLL_TuneZ2_Winter10":          "DYJetsToLL_M50",
    "DYJetsToLL_M50_TuneZ2_Winter10":          "DYJetsToLL_M50",
    "DYJetsToLL_M10to50_TuneD6T_Winter10":          "DYJetsToLL_M10to50",
    "DYJetsToLL_M50_TuneD6T_Winter10":          "DYJetsToLL_M50",

    "TToBLNu_s-channel_TuneZ2_Winter10": "TToBLNu_s-channel",
    "TToBLNu_t-channel_TuneZ2_Winter10": "TToBLNu_t-channel",
    "TToBLNu_tW-channel_TuneZ2_Winter10": "TToBLNu_tW-channel",

    "QCD_Pt30to50_TuneZ2_Winter10":   "QCD_Pt30to50",
    "QCD_Pt50to80_TuneZ2_Winter10":   "QCD_Pt50to80",
    "QCD_Pt80to120_TuneZ2_Winter10":  "QCD_Pt80to120",
    "QCD_Pt120to170_TuneZ2_Winter10": "QCD_Pt120to170",
    "QCD_Pt170to300_TuneZ2_Winter10": "QCD_Pt170to300",
    "QCD_Pt300to470_TuneZ2_Winter10": "QCD_Pt300to470",

    "QCD_Pt20_MuEnriched_TuneZ2_Winter10": "QCD_Pt20_MuEnriched",

    "WW_TuneZ2_Winter10": "WW",
    "WZ_TuneZ2_Winter10": "WZ",
    "ZZ_TuneZ2_Winter10": "ZZ",
}

## Map the datasets to be merged to the name of the merged dataset.
_datasetMerge = {
    "QCD_Pt30to50":   "QCD",
    "QCD_Pt50to80":   "QCD",
    "QCD_Pt80to120":  "QCD",
    "QCD_Pt120to170": "QCD",
    "QCD_Pt170to300": "QCD",
    "QCD_Pt300to470": "QCD",

    "TToBLNu_s-channel": "SingleTop",
    "TToBLNu_t-channel": "SingleTop",
    "TToBLNu_tW-channel": "SingleTop",

    "DYJetsToLL_M10to50": "DYJetsToLL",
    "DYJetsToLL_M50": "DYJetsToLL",

    "WW": "Diboson",
    "WZ": "Diboson",
    "ZZ": "Diboson",
}

## Default ordering of datasets
_datasetOrder = [
    "Data",
    "TTToHplusBWB_M90", 
    "TTToHplusBWB_M100",
    "TTToHplusBWB_M120",
    "TTToHplusBWB_M140",
    "TTToHplusBWB_M160",
    "QCD",
    "QCD_Pt20_MuEnriched",
    "DYJetsToLL",
    "WJets",
    "SingleTop",
    "TTJets",
    "Diboson",
]

## Map the logical dataset names to legend labels
_legendLabels = {
    "Data":                  "Data",

    "TTToHplusBWB_M90":  "H^{#pm} m=90", 
    "TTToHplusBWB_M100": "H^{#pm} m=100",
    "TTToHplusBWB_M120": "H^{#pm} m=120",
    "TTToHplusBWB_M140": "H^{#pm} m=140",
    "TTToHplusBWB_M160": "H^{#pm} m=160",

    "TTJets":                "t#bar{t}+jets",
    "WJets":                 "W+jets",

    "QCD_Pt30to50":          "QCD, 30 < #hat{p}_{T} < 50",
    "QCD_Pt50to80":          "QCD, 50 < #hat{p}_{T} < 80",
    "QCD_Pt80to120":         "QCD, 80 < #hat{p}_{T} < 120",
    "QCD_Pt120to170":        "QCD, 120 < #hat{p}_{T} < 170",
    "QCD_Pt170to300":        "QCD, 170 < #hat{p}_{T} < 300",
    "QCD_Pt300to470":        "QCD, 300 < #hat{p}_{T} < 470",

    "DYJetsToLL":            "DY+jets",
    "QCD_Pt20_MuEnriched":   "QCD (#mu enr.), #hat{p}_{T} > 20",
    "SingleTop":             "Single t",
}

## Map the logical dataset names to plot styles
_plotStyles = {
    "Data":                  styles.dataStyle,

    "TTToHplusBWB_M90":           styles.signal90Style,
    "TTToHplusBWB_M100":          styles.signal100Style,
    "TTToHplusBWB_M120":          styles.signal120Style,
    "TTToHplusBWB_M140":          styles.signal140Style,
    "TTToHplusBWB_M150":          styles.signal160Style,

    "TTJets":                styles.ttStyle,
    "WJets":                 styles.wStyle,

    "QCD":                   styles.qcdStyle,

    "DYJetsToLL":            styles.dyStyle,
    "QCD_Pt20_MuEnriched":   styles.qcdStyle,
    "SingleTop":             styles.stStyle,
    "Diboson":               styles.dibStyle,
}

## Helper class for setting properties
#
# Helper class for setting properties of histograms.Histo objects (legend label, plot style)
class SetProperty:
    ## Constructor
    #
    # \param properties  Dictionary of properties (from name of
    #                    histograms.Histo to the property understood
    #                    by the setter)
    # \param setter      Function for setting the property. It should take
    #                    two parameters, first one is the
    #                    histograms.Histo object, second one is the
    #                    property to be set
    def __init__(self, properties, setter):
        self.properties = properties
        self.setter = setter

    ## Set the property of a given object
    #
    # \param histoData   histograms.Histo object for which to set the property
    #
    # If there is no property to be set for a given histo, nothing is done to it
    def __call__(self, histoData):
        prop = self._getProperty(histoData.getName())
        if prop != None:
            self.setter(histoData, prop)

    ##
    # \todo Replace this with self.properties.get(name, None)...
    def _getProperty(self, name):
        if name in self.properties:
            return self.properties[name]
        else:
            return None

## Construct a "function" to set legend labels
#
# \param labels   Dictionary of labels (from the histo name to the legend label)
#
# \return   Object with implemented function call operator " to be used
#           with histograms.HistoManagerImpl.forEachHisto().
def SetLegendLabel(labels):
    return SetProperty(labels, lambda hd, label: hd.setLegendLabel(label))

## Construct a "function" to set plot styles
#
# \param styleMap   Dictionary of styles (from the histo name to the style)
#
# \return   Object with implemented function call operator " to be used
#           with histograms.HistoManagerImpl.forEachHisto().
def SetPlotStyle(styleMap):
    return SetProperty(styleMap, lambda hd, style: hd.call(style))

## Construct a "function" to update some styles to filled
#
# \param styleMap       Dictionary of styles (from the histo name to the style)
# \param namesToFilled  List of histogram names for which to apply the filled style
#
# \return   Object with implemented function call operator " to be used
#           with histograms.HistoManagerImpl.forEachHisto().
#
# The filled style is implemented via style.StyleFill
def UpdatePlotStyleFill(styleMap, namesToFilled):
    def update(hd, style):
        if hd.getName() in namesToFilled:
            hd.call(styles.StyleFill(style))

    return SetProperty(styleMap, update)

## Default dataset merging, naming and reordering for data/MC comparison
#
# \param datasetMgr  dataset.DatasetManager object
#
# Merges data datasets and the MC datasets as specified in
# plots._datasetMerge. The intention is that the datasets to be merged
# as one are kind of binned ones, and the final merged dataset forms a
# logical entity. For example, data in multiple run periods, QCD in
# pthat bins, single top in the separate channels, WW, WZ and ZZ for
# diboson.
#
# Renames the datasets as specified in plots._physicalToLogical. The
# intention is that the physical dataset names (i.e. the crab task
# names in multicrab.cfg) can contain some rather specific information
# (e.g. the pythia tune, MC production era) which is not that relevant
# in actual plotting (i.e. TTJets in TuneZ2 and TuneD6T, and from
# Fall10 and Winter10, all are logically TTJets sample). This choice
# makes e.g. the plots._datasetMerge, plots._datasetOrder,
# plots._legendLabels and plots._plotStyles shorter and more generic.
#
# Finally orders the datasets as specified in plots._datasetOrder. The
# datasets not in the plots._datasetOrder list are left at the end in
# the same order they were originally.
def mergeRenameReorderForDataMC(datasetMgr):
    datasetMgr.mergeData()
    datasetMgr.renameMany(_physicalToLogical, silent=True)

    datasetMgr.mergeMany(_datasetMerge)

    mcNames = datasetMgr.getAllDatasetNames()
    newOrder = []
    for name in _datasetOrder:
        try:
            i = mcNames.index(name)
            newOrder.append(name)
            del mcNames[i]
        except ValueError:
            pass
    newOrder.extend(mcNames)
    datasetMgr.selectAndReorder(newOrder)

def _createRatio(rootHisto1, rootHisto2, ytitle):
    ratio = rootHisto1.Clone()
    ratio.Divide(rootHisto2)
    styles.getDataStyle().apply(ratio)
    ratio.GetYaxis().SetTitle(ytitle)
    return ratio

def _createRatioLine(xmin, xmax):
    line = ROOT.TGraph(2, array.array("d", [xmin, xmax]), array.array("d", [1.0, 1.0]))
    line.SetLineColor(ROOT.kBlack)
    line.SetLineWidth(2)
    line.SetLineStyle(3)
    return line

def _createCoverPad(xmin=0.065, ymin=0.285, xmax=0.165, ymax=0.33):
    coverPad = ROOT.TPad("coverpad", "coverpad", xmin, ymin, xmax, ymax)
    coverPad.SetBorderMode(0)
    return coverPad
 

## Base class for plots
class PlotBase:
    ## Construct plot from DatasetManager and histogram name
    #
    # \param datasetRootHistos  dataset.DatasetRootHistoBase objects to plot
    # \param saveFormats        List of suffixes for formats for which to save the plot
    def __init__(self, datasetRootHistos, saveFormats=[".png", ".eps", ".C"]):
        # Create the histogram manager
        self.histoMgr = histograms.HistoManager(datasetRootHistos = datasetRootHistos)

        # Save the format
        self.saveFormats = saveFormats

    def _setLegendStyles(self):
        self.histoMgr.setHistoLegendStyleAll("F")
        if self.histoMgr.hasHisto("Data"):
            self.histoMgr.setHistoLegendStyle("Data", "p")

    def _setLegendLabels(self):
        self.histoMgr.forEachHisto(SetLegendLabel(_legendLabels))

    def _setPlotStyles(self):
        self.histoMgr.forEachHisto(SetPlotStyle(_plotStyles))
        if self.histoMgr.hasHisto("Data"):
            self.histoMgr.setHistoDrawStyle("Data", "EP")

    def binWidth(self):
        return self.histoMgr.getHistos()[0].getBinWidth(1)

    ## Add a format for which to save the plot
    #
    # \param format  Suffix recognised by ROOT
    def appendSaveFormat(self, format):
        self.saveFormats.append(format)

    ## Set the legend object
    # 
    # \param legend   TLegend object
    #
    # All histograms in the plot are added to the legend object
    def setLegend(self, legend):
        self.legend = legend
        self.histoMgr.addToLegend(legend)

    ## Remove the legend object
    def removeLegend(self):
        delattr(self, "legend")

    ## Add MC uncertainty histogram
    def addMCUncertainty(self):
        self.histoMgr.addMCUncertainty(styles.getErrorStyle())

    ## Stack all MC histograms 
    #
    # Internally, THStack is used
    ## Create TCanvas and frames for the histogram and a data/MC ratio
    #
    # \param filename   Name for TCanvas (becomes the file name)
    # \param kwargs     Keyword arguments, forwarded to histograms.CanvasFrame.__init__()
    def createFrame(self, filename, **kwargs):
        self.cf = histograms.CanvasFrame(self.histoMgr, filename, **kwargs)
        self.frame = self.cf.frame

    def getFrame(self):
        return frame
    def getPad(self):
        return self.cf.pad

    ## Draw the plot
    #
    # Draw also the legend if one has been associated
    def draw(self):
        self.histoMgr.draw()
        if hasattr(self, "legend"):
            self.legend.Draw()

    ## Add text for integrated luminosity
    #
    # \param x   X coordinate (in NDC, None for the default value)
    # \param y   Y coordinate (in NDC, None for the default value)
    def addLuminosityText(self, x=None, y=None):
        self.histoMgr.addLuminosityText(x, y)

    ## Save the plot to file(s)
    #
    # \param formats   Save to these formats (if not given, the values
    #                  given in the constructor and in
    #                  appendSaveFormat() are used
    def save(self, formats=None):
        if formats == None:
            formats = self.saveFormats

        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kWarning

        for f in formats:
            self.cf.canvas.SaveAs(f)

        ROOT.gErrorIgnoreLevel = backup

    ## \var histoMgr
    # histograms.HistoManager object for histogram management
    ## \var datasetMgr
    # datasets.DatasetManager object to have the datasets at hand
    ## \var saveFormats
    # List of formats to which to save the plot
    ## \var legend
    # TLegend object if legend has been added to the plot
    ## \var cf
    # histograms.CanvasFrame object to hold the TCanvas and TH1 for frame
    ## \var frame
    # TH1 object for the frame (from the cf object)


class PlotSameBase(PlotBase):
    """Base class for plots with same histogram from many datasets."""

    def __init__(self, datasetMgr, name, **kwargs):
        """Constructor.
        Arguments:
        datasetMgr   DatasetManager for datasets
        name         Name of the histogram in the ROOT files

        Keyword arguments:
        see PlotBase.__init__()
        """
        PlotBase.__init__(self, datasetMgr.getDatasetRootHistos(name), **kwargs)
        self.datasetMgr = datasetMgr
        self.rootHistoPath = name

    def getRootHistoPath(self):
        return self.rootHistoPath

    def stackMCHistograms(self):
        mcNames = self.datasetMgr.getMCDatasetNames()
        self.histoMgr.forEachHisto(UpdatePlotStyleFill(_plotStyles, mcNames))
        self.histoMgr.stackHistograms("StackedMC", mcNames)

## Class for data-MC comparison plot.
# 
class DataMCPlot(PlotSameBase):
    ## Construct from DatasetManager and a histogram path
    #
    # \param datasetMgr  DatasetManager for datasets
    # \param name        Path of the histogram in the ROOT files
    # \param kwargs      Keyword arguments, forwarded to PlotSameBase.__init__()
    def __init__(self, datasetMgr, name, normalizeToOne=False, **kwargs):
        PlotSameBase.__init__(self, datasetMgr, name, **kwargs)
        
        # Normalize the MC histograms to the data luminosity
        self.histoMgr.normalizeMCByLuminosity()
        self.normalizeToOne = normalizeToOne

        self._setLegendStyles()
        self._setLegendLabels()
        self._setPlotStyles()

    def _normalizeToOne(self):
        if not self.normalizeToOne:
            return

        if not self.histoMgr.hasHisto("StackedMC"):
            self.histoMgr.forEachHisto(lambda h: dataset._normalizeToOne(h.getRootHisto()))
            return

        # Normalize the stacked histograms
        handled = []
        h = self.histoMgr.getHisto("StackedMC")
        sumInt = h.getSumRootHisto().Integral()
        for th1 in h.getAllRootHistos():
            dataset._normalizeToFactor(th1, 1.0/sumInt)
        handled.append("StackedMC")

        # Normalize the the uncertainty histogram if it exists
        if self.histoMgr.hasHisto("MCuncertainty"):
            dataset._normalizeToFactor(self.histoMgr.getHisto("MCuncertainty").getRootHisto(), 1.0/sumInt)
            handled.append("MCuncertainty")
        
        # Normalize the rest
        for h in self.histoMgr.getHistos():
            if not h.getName() in handled:
                dataset._normalizeToOne(h.getRootHisto())

    ## Stack MC histograms
    #
    # \param stackSignal  Should the signal histograms be stacked too?
    #
    # Signal histograms are identified by checking if the name contains "TTToHplus"
    def stackMCHistograms(self, stackSignal=False):
        def isNotSignal(name):
            return not "TTToHplus" in name

        mcNames = self.datasetMgr.getMCDatasetNames()
        mcNamesNoSignal = filter(isNotSignal, mcNames)
        if not stackSignal:
            mcNames = mcNamesNoSignal

        # Leave the signal datasets unfilled
        self.histoMgr.forEachHisto(UpdatePlotStyleFill( _plotStyles, mcNamesNoSignal))
        self.histoMgr.stackHistograms("StackedMC", mcNames)

    def addMCUncertainty(self):
        if not self.histoMgr.hasHisto("StackedMC"):
            raise Exception("Must call stackMCHistograms() before addMCUncertainty()")
        self.histoMgr.addMCUncertainty(styles.getErrorStyle(), nameList=["StackedMC"])

    def createFrame(self, filename, **kwargs):
        self._normalizeToOne()
        PlotSameBase.createFrame(self, filename, **kwargs)

    ## Create TCanvas and frames for the histogram and a data/MC ratio
    #
    # \param filename   Name for TCanvas (becomes the file name)
    # \param kwargs     Keyword arguments, forwarded to histograms.CanvasFrameTwo.__init__()
    def createFrameFraction(self, filename, **kwargs):
        if not self.histoMgr.hasHisto("StackedMC"):
            raise Exception("Must call stackMCHistograms() before createFrameFraction()")

        self._normalizeToOne()

        self.ratio = _createRatio(self.histoMgr.getHisto("Data").getRootHisto(),
                                  self.histoMgr.getHisto("StackedMC").getSumRootHisto(),
                                  "Data/MC")

        self.cf = histograms.CanvasFrameTwo(self.histoMgr, [self.ratio], filename, **kwargs)
        self.frame = self.cf.frame
        self.cf.frame2.GetYaxis().SetNdivisions(505)

    def getFrame1(self):
        return self.cf.frame1
    def getFrame2(self):
        return self.cf.frame2
    def getPad1(self):
        return self.cf.pad1
    def getPad2(self):
        return self.cf.pad2

    def draw(self):
        PlotSameBase.draw(self)
        if hasattr(self, "ratio"):
            self.cf.canvas.cd(2)

            self.line = _createRatioLine(self.cf.frame.getXmin(), self.cf.frame.getXmax())
            self.line.Draw("L")

            self.ratio.Draw("EP same")
            self.cf.canvas.cd()

            # Create an empty, white-colored pad to hide the topmost
            # label of the y-axis of the lower pad. Then move the
            # upper pad on top, so that the lowest label of the y-axis
            # of it is shown
            self.coverPad = _createCoverPad()
            self.coverPad.Draw()

            self.cf.canvas.cd(1)
            self.cf.pad1.Pop() # Move the first pad on top

class ComparisonPlot(PlotBase):
    """Class to create comparison plots of two quantities."""

    def __init__(self, datasetRootHisto1, datasetRootHisto2):
        """Constructor.

        Arguments:
        datasetRootHisto1
        datasetRootHisto2

        ratio is datasetRootHisto1/datasetRootHisto2
        """
        PlotBase.__init__(self,[datasetRootHisto1, datasetRootHisto2])

    def createFrame(self, filename, doRatio=True, **kwargs):
        if not doRatio:
            PlotBase.createFrame(self, filename, **kwargs)
        else:
            histos = self.histoMgr.getHistos()
            self.ratio = _createRatio(histos[0].getRootHisto(), histos[1].getRootHisto(),
                                      "%s/%s" % (histos[0].getName(), histos[1].getName()))

            self.cf = histograms.CanvasFrameTwo(self.histoMgr, [self.ratio], filename, **kwargs)
            self.frame = self.cf.frame
            self.cf.frame2.GetYaxis().SetNdivisions(505)

    def getFrame1(self):
        return self.cf.frame1
    def getFrame2(self):
        return self.cf.frame2
    def getPad1(self):
        return self.cf.pad1
    def getPad2(self):
        return self.cf.pad2

    def draw(self):
        PlotBase.draw(self)
        if hasattr(self, "ratio"):
            self.cf.canvas.cd(2)

            self.line = _createRatioLine(self.cf.frame.getXmin(), self.cf.frame.getXmax())
            self.line.Draw("L")

            self.ratio.Draw("EP same")
            self.cf.canvas.cd()

            # Create an empty, white-colored pad to hide the topmost
            # label of the y-axis of the lower pad. Then move the
            # upper pad on top, so that the lowest label of the y-axis
            # of it is shown
            self.coverPad = _createCoverPad()
            self.coverPad.Draw()

            self.cf.canvas.cd(1)
            self.cf.pad1.Pop() # Move the first pad on top


        

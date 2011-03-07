import ROOT
import array

import histograms
import styles

# Map the physical dataset names (in multicrab.cfg) to logical names
# used in _legendLabels and _plotStyles
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

# Map the logical dataset names to legend labels
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

# Map the logical dataset names to plot styles
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


class SetProperty:
    def __init__(self, properties, setter):
        self.properties = properties
        self.setter = setter

    def __call__(self, histoData):
        prop = self._getProperty(histoData.getName())
        if prop != None:
            self.setter(histoData, prop)

    def _getProperty(self, name):
        if name in self.properties:
            return self.properties[name]
        else:
            return None

def SetLegendLabel(labels):
    return SetProperty(labels, lambda hd, label: hd.setLegendLabel(label))

def SetPlotStyle(styleList):
    return SetProperty(styleList, lambda hd, style: hd.call(style))

def UpdatePlotStyleFill(styleList, namesToFilled):
    def update(hd, style):
        if hd.getName() in namesToFilled:
            hd.call(styles.StyleFill(style))

    return SetProperty(styleList, update)

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
 

class PlotBase:
    """Base class for plots."""

    def __init__(self, datasetRootHistos, saveFormats=[".png", ".eps", ".C"]):
        """Constructor.

        Arguments:
        datasetRootHistos  List of DatasetRootHisto objects to plot
        saveFormats        List of the default formats to save (default: ['.png', '.eps', '.C'])
        """
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

    def appendSaveFormat(self, format):
        self.saveFormats.append(format)

    def setLegend(self, legend):
        self.legend = legend
        self.histoMgr.addToLegend(legend)

    def removeLegend(self):
        delattr(self, "legend")

    def addMCUncertainty(self):
        self.histoMgr.addMCUncertainty(styles.getErrorStyle())

    def createFrame(self, filename, **kwargs):
        self.cf = histograms.CanvasFrame(self.histoMgr, filename, **kwargs)
        self.frame = self.cf.frame

    def getFrame(self):
        return frame
    def getPad(self):
        return self.cf.pad

    def draw(self):
        self.histoMgr.draw()
        if hasattr(self, "legend"):
            self.legend.Draw()

    def addLuminosityText(self, x=None, y=None):
        self.histoMgr.addLuminosityText(x, y)

    def save(self, formats=None):
        if formats == None:
            formats = self.saveFormats

        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kWarning

        for f in formats:
            self.cf.canvas.SaveAs(f)

        ROOT.gErrorIgnoreLevel = backup

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

    def stackMCHistograms(self):
        mcNames = self.datasetMgr.getMCDatasetNames()
        self.histoMgr.forEachHisto(UpdatePlotStyleFill(_plotStyles, mcNames))
        self.histoMgr.stackHistograms("StackedMC", mcNames)

class DataMCPlot(PlotSameBase):
    """Class to create data-MC comparison plot."""

    def __init__(self, datasetMgr, name, **kwargs):
        """Constructor.

        Arguments:
        datasetMgr   DatasetManager for datasets
        name         Name of the histogram in the ROOT files

        Keyword arguments:
        see PlotSameBase.__init__()
        """
        PlotSameBase.__init__(self, datasetMgr, name, **kwargs)
        
        # Normalize the MC histograms to the data luminosity
        self.histoMgr.normalizeMCByLuminosity()

        self._setLegendStyles()
        self._setLegendLabels()
        self._setPlotStyles()

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

    def createFrameFraction(self, filename, **kwargs):
        if not self.histoMgr.hasHisto("StackedMC"):
            raise Exception("Must call stackMCHostograms() before createFrameFraction()")

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


        

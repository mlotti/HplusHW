## \package tauEmbedding
# Tau embedding (EWK+ttbar tau background measurement) related plotting utilities

import os
import re
import math
import array

import ROOT
ROOT.gROOT.SetBatch(True)

import dataset
import histograms
import plots
import counter
import styles
import cutstring
import aux
import systematics

## Apply embedding normalization (muon efficiency, W->tau->mu factor
normalize = True
## Data era
era = "Run2011AB"

## When doing the averaging, take the stat uncertainty as the average of the stat uncertanties of the trials
uncertaintyByAverage = False

## Signal analysis multicrab directories for embedding trials
dirEmbs_120911 = [
    "multicrab_signalAnalysis_systematics_v44_3_seed0_Run2011AB_120911_144711",
#    "multicrab_signalAnalysis_systematics_v44_3_seed1_Run2011AB_120911_152858",
#    "multicrab_signalAnalysis_systematics_v44_3_seed2_Run2011AB_120911_162417"
]
## Signal analysis multicrab directories for embedding trials
#
# This variable is used to select from possibly multiple sets of embedding directories
dirEmbs = dirEmbs_120911
## Signal analysis multicrab directory for normal MC
dirSig = "multicrab_signalAnalysisGenTau_systematics_120912_084953" # for 120911


## Tau analysis multicrab directories for embedding trials
tauDirEmbs = [ # TTJets only
#    "multicrab_analysis_v44_4_2_seed0_Muon40_121016_092812"
    "multicrab_analysis_v44_4_2_seed0_Muon40_121023_104038"
#    "multicrab_analysis_v44_4_2_seed0_allGenuineTaus_121114_152418"

#    "multicrab_analysis_v44_4_2_seed0_Run2011AB_121011_085855",
]
## Tau analysis multicrab directories for embedding trials
#
# This variable is used to select from possibly multiple sets of embedding directories
#tauDirEmbs = tauDirEmbs_121011
## Tau analysis multicrab directory for normal MC
#tauDirSig = "multicrab_analysisTau_121009_112529" # 121011 # this is the one with "MostLikelySelected"
tauDirSig = "multicrab_analysisTau_firstGenTau_121011_112052"
#tauDirSig = "multicrab_analysisTau_firstGenTau40_121016_133933"
#tauDirSig = "multicrab_analysisTau_121009_112529"


class MuonAnalysisSelectorArgs(dataset.SelectorArgs):
    def __init__(self, **kwargs):
        dataset.SelectorArgs.__init__(self,
                                      [("era", ""),
                                       ("puVariation", ""),
                                       ("isolationMode", "standard"),
                                       ("bquarkMode", "disabled"),
                                       ("topPtReweighting", True),
                                       ("topPtReweightingScheme", ""),
                                       ],
                                      **kwargs)

class TauAnalysisSelectorArgs(dataset.SelectorArgs):
    def __init__(self, **kwargs):
        dataset.SelectorArgs.__init__(self,
                                      [("puWeight", ""),
                                       ("isEmbedded", False),
                                       ("embeddingWTauMuFile", ""),
                                       ("embeddingWTauMuPath", ""),
                                       ("mcTauMultiplicity", ""),
                                       ("mcTauMode", ""),
                                       ("embeddingNormalizationMode", ""),
                                       ("embeddingMuonWeights", None),
                                       ],
                                      **kwargs)

class Selections:
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

## Selections for tau ntuple
tauNtuple = Selections(decayModeExpression = "(taus_decayMode<=2)*taus_decayMode + (taus_decayMode==10)*3 +(taus_decayMode > 2 && taus_decayMode != 10)*4>>tmp(5,0,5)",
                       rtauExpression = "(taus_leadPFChargedHadrCand_p4.P() / taus_p4.P() -1e-10)",
                       deltaPhiExpression = "acos( (taus_p4.Px()*pfMet_p4.Px()+taus_p4.Py()*pfMet_p4.Py())/(taus_p4.Pt()*pfMet_p4.Et()) )*57.3")

# tau candidate selection
#tauNtuple.decayModeFinding = "taus_decayMode >= 0" # replace with discriminator after re-running ntuples
tauNtuple.decayModeFinding = "taus_f_decayModeFinding > 0.5" # replace with discriminator after re-running ntuples
tauNtuple.tauPtPreCut = "taus_p4.Pt() > 15"
tauNtuple.tauPtCut = "taus_p4.Pt() > 40"
tauNtuple.tauEtaCut = "abs(taus_p4.Eta()) < 2.1"
tauNtuple.tauLeadPt = "taus_leadPFChargedHadrCand_p4.Pt() > 20"
tauNtuple.ecalFiducial = "!( abs(taus_p4.Eta()) < 0.018 || (0.423 < abs(taus_p4.Eta()) && abs(taus_p4.Eta()) < 0.461)"
tauNtuple.ecalFiducial += " || (0.770 < abs(taus_p4.Eta()) && abs(taus_p4.Eta()) < 0.806)"
tauNtuple.ecalFiducial += " || (1.127 < abs(taus_p4.Eta()) && abs(taus_p4.Eta()) < 1.163)"
tauNtuple.ecalFiducial += " || (1.460 < abs(taus_p4.Eta()) && abs(taus_p4.Eta()) < 1.558)" # gap
tauNtuple.ecalFiducial += ")"
#tauNtuple.electronRejection = "taus_f_againstElectronMedium > 0.5"
tauNtuple.electronRejection = "taus_f_againstElectronMVA > 0.5"
tauNtuple.muonRejection = "taus_f_againstMuonTight > 0.5"

# tau ID
#tauNtuple.tightIsolation = "taus_f_byTightIsolation > 0.5"
tauNtuple.tightIsolation = "taus_f_byMediumCombinedIsolationDeltaBetaCorr > 0.5"
tauNtuple.oneProng = "taus_signalPFChargedHadrCands_n == 1"
tauNtuple.rtau = "%s > 0.7" % tauNtuple.rtauExpression

# Short-hand notations for tau candidate selection and tau id (and yes, the isolation is intentionally part of tau candidate selection here)
tauNtuple.tauCandidateSelection = cutstring.And(*[getattr(tauNtuple, name) for name in ["decayModeFinding", "tightIsolation", "tauPtCut", "tauEtaCut", "tauLeadPt", "ecalFiducial", "electronRejection", "muonRejection"]])
tauNtuple.tauID = cutstring.And(*[getattr(tauNtuple, name) for name in ["tightIsolation", "oneProng", "rtau"]])

# Rest of the event selection
tauNtuple.pvSelection = "selectedPrimaryVertices_n >= 1"
tauNtuple.metSelection = "pfMet_p4.Pt() > 50"
tauNtuple.jetSelection = "jets_looseId && jets_p4.Pt() > 30 && abs(jets_p4.Eta()) < 2.4 && sqrt((jets_p4.Eta()-taus_p4[0].Eta())^2+(jets_p4.Phi()-taus_p4[0].Phi())^2) > 0.5"
tauNtuple.jetEventSelection = "Sum$(%s) >= 3" % tauNtuple.jetSelection
#tauNtuple.btagSelection = "jets_f_tche > 1.7"
tauNtuple.btagSelection = "jets_f_csv > 0.898" # CSVL = 0.244, CSVM = 0.679, CSVT = 0.898
tauNtuple.btagEventSelection = "Sum$(%s && %s) >= 1" % (tauNtuple.jetSelection, tauNtuple.btagSelection)
tauNtuple.deltaPhi160Selection = "%s <= 160)" % tauNtuple.deltaPhiExpression

tauNtuple.caloMetNoHF = "tecalometNoHF_p4.Pt() > 60"
tauNtuple.caloMet = "tecalomet_p4.Pt() > 60"
tauNtuple.weight = {
#    "EPS": "weightPileup_Run2011A",
#    "Run2011A-EPS": "pileupWeight_Run2011AnoEPS",
    "": "",
    "Run2011A": "weightPileup_Run2011A",
    "Run2011B": "weightPileup_Run2011B",
    "Run2011AB": "weightPileup_Run2011AB",
    }

## Customization function for decay mode plot (all decay modes)
#
# \param h   plots.PlotBase object
def decayModeCheckCustomize(h):
    n = 16
    if hasattr(h, "getFrame1"):
        h.getFrame1().GetXaxis().SetNdivisions(n)
        h.getFrame2().GetXaxis().SetNdivisions(n)
    else:
        h.getFrame().GetXaxis().SetNdivisions(n)

    xaxis = h.getFrame().GetXaxis()
    xaxis.SetBinLabel(1, "#pi^{#pm}")
    xaxis.SetBinLabel(2, "#pi^{#pm}#pi^{0}")
    xaxis.SetBinLabel(3, "#pi^{#pm}#pi^{0}#pi^{0}")
    xaxis.SetBinLabel(4, "#pi^{#pm}#pi^{0}#pi^{0}#pi^{0}")
    xaxis.SetBinLabel(5, "#pi^{#pm} N#pi^{0}")
    xaxis.SetBinLabel(6, "#pi^{+}#pi^{-}")
    xaxis.SetBinLabel(7, "#pi^{+}#pi^{-}#pi^{0}")
    xaxis.SetBinLabel(8, "#pi^{+}#pi^{-}#pi^{0}#pi^{0}")
    xaxis.SetBinLabel(9, "#pi^{+}#pi^{-}#pi^{0}#pi^{0}#pi^{0}")
    xaxis.SetBinLabel(10, "#pi^{+}#pi^{-} N#pi^{0}")
    xaxis.SetBinLabel(11, "#pi^{+}#pi^{-}#pi^{#pm}")
    xaxis.SetBinLabel(12, "#pi^{+}#pi^{-}#pi^{#pm}#pi^{0}")
    xaxis.SetBinLabel(13, "#pi^{+}#pi^{-}#pi^{#pm}#pi^{0}#pi^{0}")
    xaxis.SetBinLabel(14, "#pi^{+}#pi^{-}#pi^{#pm}#pi^{0}#pi^{0}#pi^{0}")
    xaxis.SetBinLabel(15, "#pi^{+}#pi^{-}#pi^{#pm} N#pi^{0}")
    xaxis.SetBinLabel(16, "Other")


## Customization function for decay mode plot (relevant decay modes)
#
# \param h   plots.PlotBase object
def decayModeCustomize(h):
    n = 5
    if hasattr(h, "getFrame1"):
        h.getFrame1().GetXaxis().SetNdivisions(n)
        xaxis = h.getFrame2().GetXaxis()
    else:
        xaxis = h.getFrame().GetXaxis()

    xaxis.SetNdivisions(n)
    xaxis.SetBinLabel(1, "#pi^{#pm}")
    xaxis.SetBinLabel(2, "#pi^{#pm}#pi^{0}")
    xaxis.SetBinLabel(3, "#pi^{#pm}#pi^{0}#pi^{0}")
    xaxis.SetBinLabel(4, "#pi^{+}#pi^{-}#pi^{#pm}")
    xaxis.SetBinLabel(5, "Other")

def decayModeLabels(h, ndiv):
    if hasattr(h, "hasFrame2") and h.hasFrame2():
        h.getFrame1().GetXaxis().SetNdivisions(ndiv)
        xaxis = h.getFrame2().GetXaxis()
    else:
        xaxis = h.getFrame().GetXaxis()
    xaxis.SetNdivisions(ndiv)

    labels = ["#pi^{#pm}",
              "#pi^{#pm}#pi^{0}",
              "#pi^{#pm}#pi^{0}#pi^{0}",
              "#pi^{#pm}#pi^{0}#pi^{0}#pi^{0}",
              "#pi^{#pm} N#pi^{0}",
              "#pi^{+}#pi^{-}",
              "#pi^{+}#pi^{-}#pi^{0}",
              "#pi^{+}#pi^{-}#pi^{0}#pi^{0}",
              "#pi^{+}#pi^{-}#pi^{0}#pi^{0}#pi^{0}",
              "#pi^{+}#pi^{-} N#pi^{0}",
              "#pi^{+}#pi^{-}#pi^{#pm}",
              "#pi^{+}#pi^{-}#pi^{#pm}#pi^{0}",
              "#pi^{+}#pi^{-}#pi^{#pm}#pi^{0}#pi^{0}",
              "#pi^{+}#pi^{-}#pi^{#pm}#pi^{0}#pi^{0}#pi^{0}",
              "#pi^{+}#pi^{-}#pi^{#pm} N#pi^{0}",
              ]
    for i in xrange(0, min(ndiv, len(labels))):
        xaxis.SetBinLabel(i+1, labels[i])


## Selections for signal analysis tree
signalNtuple = Selections(
    deltaPhiExpression="acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3",
    mtExpression = "sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi())))",
    )
signalNtuple.metCut = "met_p4.Et() > 50"
signalNtuple.bTaggingCut = "passedBTagging"
signalNtuple.deltaPhi160Cut = "%s <= 160" % signalNtuple.deltaPhiExpression
signalNtuple.deltaPhi130Cut = "%s <= 130" % signalNtuple.deltaPhiExpression
signalNtuple.weight = "weightPileup*weightTrigger"
signalNtuple.weightBTagging = signalNtuple.weight+"*weightBTagging"


# http://pdg.lbl.gov/2013/reviews/rpp2012-rev-tau-branching-fractions.pdf
#                 e        mu
BR_tau_hadr = 1 - 0.1783 - 0.1741
def scaleTauBRNormalization(h):
    # All other normalization is within the job
    h.Scale(BR_tau_hadr)


## Apply embedding normalization
#
# \param obj  plots.PlotBase, histograms.Histo, or counter.EventCounter object
#
# The normalization includes the muon trigger and ID efficiency, and W->tau->mu fraction
def scaleNormalization(obj):
    if not normalize:
        return

    #scaleMCfromWmunu(obj) # data/MC trigger correction
#    scaleMuTriggerIdEff(obj)
#    scaleWmuFraction(obj)

## Apply muon trigger and ID efficiency normalization
#
# \param obj  plots.PlotBase, histograms.Histo, or counter.EventCounter object
def scaleMuTriggerIdEff(obj):
    # From 2011A only
    #data = 0.508487
    #mc = 0.541083
    # May10 in 41X
    #data = 0.891379
    #mc = 0.931707
    # 1fb in 42X
    # data = None
    # if era == "EPS":
    #     data = 0.884462
    # elif era == "Run2011A-EPS":
    #     data = 0.879
    # elif era == "Run2011A":
    #     data = 0.881705 
    # elif era == "Run2011AB":
    #     print "WARNING: using Run2011A mu trigger+ID efficiency. This should be updated!"
    #     data = 0.881705
    # else:
    #     raise Exception("No mu trigger+ID efficiency available for era %s" % era)
    # mc = 0.919829

    # From Sami for 44X, muon pT > 41
    # 20120902-160154
    scaleMap41 = {
        # HLT_Mu20
        "160431-163261": 0.882968,
        # HLT_Mu24
        "163270-163869": 0.891375,
        # HLT_Mu30
        "165088-166150": 0.904915,
        # HLT_Mu40
        "166161-166164": 0.877395,
        "166346-166346": 0.877395,
        "166374-167043": 0.877395,
        "167078-167913": 0.877395,
        "170722-172619": 0.877395,
        "172620-173198": 0.877395,
        # HLT_Mu40_eta2p1 A
        "173236-173692": 0.867646,
        "173693-177452": 0.867646,
        # HLT_Mu40_eta2p1 B
        "177453-178380": 0.957712,
        "178411-179889": 0.957712,
        "179942-180371": 0.957712,
        # MC
        "MC": 0.888241,
        }
    scaleMap40 = {"MC": 0.878604}
    scaleMapOld = {"MC": 0.919829}

    scaleMap = scaleMap41
#    scaleMap = scaleMap40
#    scaleMap = scaleMapOld

    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonReferenceEffs
    # This is only ID efficiency
    scaleMap = {"MC": (0.955+0.9519)/2}

    # Transform to inverse
    for key in scaleMap.keys():
        scaleMap[key] = 1/scaleMap[key]

    scaleHistosCounters(obj, scaleDataHisto, "scaleData", scaleMap)
    scaleHistosCounters(obj, scaleMCHisto, "scaleMC", scaleMap)

## Apply W->tau->mu normalization
#
# \param obj  plots.PlotBase, histograms.Histo, or counter.EventCounter object
def scaleWmuFraction(obj):
    Wtaumu = 0.038479

    scaleHistosCounters(obj, scaleHisto, "scale", 1-Wtaumu)

## Helper function to scale histos or counters
#
# \param obj          plots.PlotBase, histograms.Histo, or counter.EventCounter object
# \param plotFunc     Function to apply for plots.PlotBase and histograms.Histo objects
# \param counterFunc  Name of counter.EventCounter function to apply
# \param scale        Multiplication factor
def scaleHistosCounters(obj, plotFunc, counterFunc, scale):
    if isinstance(obj, plots.PlotBase):
        scalePlot(obj, plotFunc, scale)
    elif isinstance(obj, counter.EventCounter):
        scaleCounters(obj, counterFunc, scale)
    elif isinstance(obj, dataset.DatasetRootHistoBase):
        scaleDatasetRootHisto(obj, plotFunc, scale)
    else:
        plotFunc(obj, scale)

## Helper function to scale plots.PlotBase objects
#
# \param plot       plots.PlotBase object
# \param function   Function to apply
# \param scale      Multiplication factor
def scalePlot(plot, function, scale):
    plot.histoMgr.forEachHisto(lambda histo: function(histo, scale))

## Helper function to scale counter.EventCounter
#
# \param eventCounter  counter.EventCounter object
# \param methodName    Name of the counter.EventCounter method to apply
# \param scale         Multiplication factor
def scaleCounters(eventCounter, methodName, scale):
    s = scale
    if isinstance(scale, dict):
        s = scale["MC"]
    getattr(eventCounter, methodName)(s)

## Helper function to scale dataset.DatasetRootHisto
#
# \param drh       dataset.DatasetRootHisto object
# \param function  Function to apply
# \param scaleMap     ??? FIXME
def scaleDatasetRootHisto(drh, function, scaleMap):
    if not isinstance(scaleMap, dict):
        drh.modifyRootHisto(lambda histo: function(histo, scaleMap))
        return

    if drh.isMC():
        drh.modifyRootHisto(lambda histo: function(histo, scaleMap["MC"]))
    else:
        runrange_re = re.compile("_(?P<range>(\d+)-(\d+))_")
        m = runrange_re.search(drh.getDataset().getName())
        if not m:
            raise Exception("Data dataset %s does not have run range in its name?" % drh.getDataset().getName())
        drh.modifyRootHisto(lambda histo: function(histo, scaleMap[m.group("range")]))


## Helper function to scale only MC histograms.Histo objects
#
# \param histo   histograms.Histo object
# \param scale   Multiplication factor
def scaleMCHisto(histo, scale):
    if histo.isMC():
        scaleHisto(histo, scale)

## Helper function to scale only data histograms.Histo objects
#
# \param histo   histograms.Histo object
# \param scale   Multiplication factor
def scaleDataHisto(histo, scale):
    if histo.isData():
        scaleHisto(histo, scale)

## Helper function to scale histograms.Histo objects
#
# \param histo   histograms.Histo object
# \param scale   Multiplication factor
def scaleHisto(histo, scale):
    if isinstance(histo, histograms.Histo):
        th1 = histo.getRootHisto()
    else:
        th1 = histo
    th1.Scale(scale)
    return th1


## Calculate square sum of TH1 bins
def squareSum(th1):
    s = 0
    for bin in xrange(0, th1.GetNbinsX()+2):
        #print "Bin %d, low edge %.1f, value %f" % (bin, th1.GetBinLowEdge(bin), th1.GetBinContent(bin))
        value = th1.GetBinContent(bin)
        s += value*value
    return s


## Class for doing the averaging over many dataset.DatasetManager objects
class DatasetsMany:
    ## Constructor
    #
    # \param dirs                      List of paths multicrab directories, either absolute or relative to working directory
    # \param normalizeMCByCrossSection Normalize MC to cross section
    # \param normalizeMCByLuminosity   Normalize MC to data luminosity?
    # \param kwargs                    Keyword arguments, forwarded to dataset.getDatasetsFromMulticrabCfg()
    #
    # Construct a dataset.DatasetManager object from each multicrab directory
    def __init__(self, dirs, normalizeMCByCrossSection=False, normalizeMCByLuminosity=False, **kwargs):
        self.datasetManagers = []
        for d in dirs:
            datasets = dataset.getDatasetsFromMulticrabCfg(directory=d, **kwargs)
            datasets.updateNAllEventsToPUWeighted()
#            datasets.loadLuminosities()
            self.datasetManagers.append(datasets)

        self.normalizeMCByCrossSection = normalizeMCByCrossSection
        self.normalizeMCByLuminosity = normalizeMCByLuminosity

    ## Apply a function for each dataset.DatasetManager object
    def forEach(self, function):
        for dm in self.datasetManagers:
            function(dm)

    ## Get dataset.DatasetManager object from the first multicrab directory
    def getFirstDatasetManager(self):
        return self.datasetManagers[0]

    ## Remove dataset.Dataset objects (compatibility with dataset.DatasetManager)
    #
    # \param args    Positional arguments (forwarded to dataset.Dataset.remove())
    # \param kwargs  Keyword arguments (forwarded to dataset.Dataset.remove())
    def remove(self, *args, **kwargs):
        self.forEach(lambda d: d.remove(*args, **kwargs))

    ## Get a list of names of all dataset.Dataset objects (compatibility with dataset.DatasetManager)
    def getAllDatasetNames(self):
        return self.datasetManagers[0].getAllDatasetNames()

    ## Close all TFiles of the contained dataset.Dataset objects (compatibility with dataset.DatasetManager)
    #
    # \see dataset.DatasetManager.close()
    def close(self):
        self.forEach(lambda d: d.close())

    
    ## Get dataset.Dataset object from the first dataset.DatasetManager
    #
    # \param name   Name of the dataset
    def getDatasetFromFirst(self, name):
        return self.getFirstDatasetManager().getDataset(name)

    ## Set the integrated luminosity from data dataset
    def setLumiFromData(self):
        self.lumi = self.getDatasetFromFirst("Data").getLuminosity()
        for dm in self.datasetManagers:
            mlumi = dm.getDataset("Data").getLuminosity()
            if abs(mlumi-self.lumi)/self.lumi > 1e-3: # allow 1 per mille variations
                raise Exception("Luminosity in some multicrab directory is %.5f, while it is %.5f in other(s)" % (mlumi, lumi))

    ## Get the integrated luminosity
    def getLuminosity(self):
        return self.lumi

    ## Get a ROOT histogram for a given dataset, averaged over the multiple dataset.DatasetManager objects
    #
    # \param datasetName   Name of the dataset
    # \param name          Name of the histogram (or dataset.TreeDraw object)
    # \param rebin         Rebin
    #
    # \return tuple of (histogram, min_max_graph)
    #
    # The min/max graph has the average as the value, and for each bin
    # the minimum and maximum in the asymmetric errors.
    def getHistogram(self, datasetName, name, rebin=1):
        histos = self.getHistograms(datasetName, name)

        # Averaging is done here
        histo = histos[0]
        histo_low = histo.Clone(histo.GetName()+"_low")
        histo_high = histo.Clone(histo.GetName()+"_high")
        for h in histos[1:]:
            for bin in xrange(0, histo.GetNbinsX()+2):
                histo.SetBinContent(bin, histo.GetBinContent(bin)+h.GetBinContent(bin))
                if uncertaintyByAverage:
                    histo.SetBinError(bin, histo.GetBinError(bin)+h.GetBinError(bin))
                else:
                    histo.SetBinError(bin, math.sqrt(histo.GetBinError(bin)**2+h.GetBinError(bin)**2))

                histo_low.SetBinContent(bin, min(histo_low.GetBinContent(bin), h.GetBinContent(bin)))
                histo_high.SetBinContent(bin, max(histo_high.GetBinContent(bin), h.GetBinContent(bin)))

        for bin in xrange(0, histo.GetNbinsX()+2):
            histo.SetBinContent(bin, histo.GetBinContent(bin)/len(histos))
            if uncertaintyByAverage:
                histo.SetBinError(bin, histo.GetBinError(bin)/len(histos))
            else:
                histo.SetBinError(bin, histo.GetBinError(bin)/len(histos))

        if rebin > 1:
            histo.Rebin(rebin)
            histo_low.Rebin(rebin)
            histo_high.Rebin(rebin)

        binCenters = []
        values = []
        errLow = []
        errHigh = []
        for bin in xrange(1, histo.GetNbinsX()+1):
            binCenters.append(histo.GetXaxis().GetBinCenter(bin))
            values.append(histo.GetBinContent(bin))
            errLow.append(histo.GetBinContent(bin) - histo_low.GetBinContent(bin))
            errHigh.append(histo_high.GetBinContent(bin) - histo.GetBinContent(bin))

        gr = ROOT.TGraphAsymmErrors(len(binCenters),
                                    array.array("d", binCenters), array.array("d", values),
                                    array.array("d", [0]*len(binCenters)), array.array("d", [0]*len(binCenters)),
                                    array.array("d", errLow), array.array("d", errHigh))

        histo.SetName("Average")

        return (histo, gr) # Average histogram, min/max graph

    ## Create TEfficiency for a given dataset, merged over the multiple dataset.DatasetManager objects
    #
    # \param datasetName   Name of the dataset
    # \param numerator     Name of the numerator histogram
    # \param denominator   Name of the denominator histogram
    #
    # \return TEfficiency object 
    def getEfficiency(self, datasetName, numerator, denominator):
        effs = []
        for dm in self.datasetManagers:
            if not dm.hasDataset(datasetName):
                print "WARNING: no dataset %s in one of the managers, skipping the manager" % datasetName
                continue

            ds = dm.getDataset(datasetName)
            num = ds.getDatasetRootHisto(numerator).getHistogram()
            den = ds.getDatasetRootHisto(denominator).getHistogram()

            eff = ROOT.TEfficiency(num, den)
            effs.append(eff)

        # Here we use merging, as the trials are just about extending statistics
        result = effs[0]
        for e in effs[1:]:
            result.Add(e)
        return result

    ## Check if a histogram exists for all dataset.DatasetManager objects
    #
    # \param datasetName   Name of the dataset
    # \param name          Name of the histogram to check
    def hasHistogram(self, datasetName, name):
        has = True
        for dm in self.datasetManagers:
            if not dm.hasDataset(datasetName):
                continue

            has = has and dm.getDataset(datasetName).hasRootHisto(name)
        return has

    ## Get the ROOT histograms of a given name from all dataset.DatasetManager objects
    #
    # \param datasetName   Name of the dataset
    # \param name          Name of the ROOT histogram
    #
    # \return list of ROOT histograms
    def getHistograms(self, datasetName, name):
        histos = []
        for i, dm in enumerate(self.datasetManagers):
            if not dm.hasDataset(datasetName):
                print "WARNING: no dataset %s in one of the managers, skipping the manager" % datasetName
                continue

            ds = dm.getDataset(datasetName)
            h = ds.getDatasetRootHisto(name)
            if h.isMC():
                if self.normalizeMCByCrossSection:
                    h.normalizeByCrossSection()
                if self.normalizeMCByLuminosity:
                    h.normalizeToLuminosity(self.lumi)
            scaleNormalization(h)
            h = h.getHistogram()
            h.SetName("Trial %d"%(i+1))
            histos.append(h)

        return histos # list of individual histograms

    ## Get a counter.HistoCounter for a given dataset and counter
    #
    # \param datasetName   Name of the dataset
    # \param name          Name of the counter ROOT histogram
    #
    # \return counter.HistoCounter object
    def getCounter(self, datasetName, name):
        (embDataHisto, tmp) = self.getHistogram(datasetName, name)
        return counter.HistoCounter(datasetName, embDataHisto)

## Class for obtaining the residual MC results
class DatasetsResidual:
    ## Constructor
    #
    # \param datasetsEmb    tauEmbedding.DatasetsMany object for embedding datasets
    # \param datasetsSig    dataset.DatasetManager obejct for normal MC
    # \param analysisEmb    Analysis directory for embeddded datasets (directory containing the ROOT histograms in the TFile)
    # \param analysisSig    Analysis directory for normal MC datasets (directory containing the ROOT histograms in the TFile)
    # \param residualNames  List of names of the datasets for which to derive the residuals (e.g. DYJetsToLL and WW)
    # \param totalNames     List of names of "total" datasets, for which to add the residual MC on top of the original contribution (e.g. emb.data+res.MC and emb.MC+res.MC)
    def __init__(self, datasetsEmb, datasetsSig, analysisEmb, analysisSig, residualNames, totalNames=[]):
        self.datasetsEmb = datasetsEmb
        self.datasetsSig = datasetsSig

        # For an ugly hack
        self.analysisEmb = analysisEmb
        self.analysisSig = analysisSig

        self.residualNames = residualNames
        self.totalNames = totalNames
        for name in totalNames:
            if name in residualNames:
                raise Exception("residualNames and totalNames must be disjoint (dataset '%s' was given in both)")

    ## Replace embedding analysis directory name with a normal MC analysis directory
    #
    # \param name  Histogram name, or dataset.TreeDraw object
    def _replaceSigName(self, name):
        if isinstance(name, basestring):
            return name.replace(self.analysisEmb, self.analysisSig)
        else:
            return name.clone(tree=lambda name: name.replace(self.analysisEmb, self.analysisSig))

    ## Apply a function for each dataset.DatasetManager object
    def forEach(self, function):
        self.datasetsEmb.forEach(function)
        function(self.datasetsSig)

    ## Remove dataset.Dataset objects (compatibility with dataset.DatasetManager)
    #
    # \param args    Positional arguments (forwarded to dataset.Dataset.remove())
    # \param kwargs  Keyword arguments (forwarded to dataset.Dataset.remove())
    def remove(self, *args, **kwargs):
        self.forEach(lambda d: d.remove(*args, **kwargs))

    ## Get a list of names of all dataset.Dataset objects (compatibility with dataset.DatasetManager)
    def getAllDatasetNames(self):
        return self.datasetsEmb.getAllDatasetNames()

    ## Close all TFiles of the contained dataset.Dataset objects (compatibility with dataset.DatasetManager)
    #
    # \see dataset.DatasetManager.close()
    def close(self):
        self.forEach(self, lambda d: d.close())


    ## Ask if the residual MC is added to a given dataset
    #
    # \param datasetName   Dataset name
    #
    # \return  True, if residual MC has been added for this dataset
    def isResidualAdded(self, datasetName):
        return datasetName in self.totalNames or datasetName in self.residualNames

    ## Get the integrated luminosity
    def getLuminosity(self):
        return self.datasetsEmb.getLuminosity()

    ## Check if a histogram exists for all dataset.DatasetManager objects
    #
    # \param datasetName   Name of the dataset
    # \param name          Name of the histogram to check
    def hasHistogram(self, datasetName, name):
        return self.datasetsEmb.hasHistogram(datasetName, name) and self.datasetsSig.getDataset(datasetName).hasHistogram(name)

    ## Get a ROOT histogram for a given dataset
    #
    # \param datasetName   Name of the dataset
    # \param name          Name of the histogram (or dataset.TreeDraw object)
    # \param rebin         Rebin
    #
    # If dataset is not in \a totalNames nor \a residual names, return
    # the embedded result (averaged over multiple dataset.DatasetManager object).
    #
    # If dataset is in \a residualNames, calculate the residual result
    # as normal-embedded.
    #
    # If dataset is in \a totalNames, calculate sum of total_emb + sum(res_mc)
    def getHistogram(self, datasetName, name, rebin=1):
        if datasetName in self.totalNames:
            #print "Creating sum for "+datasetName
            (histo, tmp) = self.datasetsEmb.getHistogram(datasetName, name, rebin)
            for res in self.residualNames:
                #print "From residual of "+res
                (h, tmp) = self.getHistogram(res, name, rebin)
                histo.Add(h)
            return (histo, None)
        elif not datasetName in self.residualNames:
            return self.datasetsEmb.getHistogram(datasetName, name)

        #print "Calculating residual of "+datasetName

        # Ugly hack
        sigName = self._replaceSigName(name)

        # Get properly normalized embedded data, embedded DY and normal DY histograms
        (embHisto, tmp) = self.datasetsEmb.getHistogram(datasetName, name)
        sigHisto = self.datasetsSig.getDataset(datasetName).getDatasetRootHisto(sigName) # DatasetRootHisto
        sigHisto.normalizeToLuminosity(self.datasetsEmb.getLuminosity())
        sigHisto = sigHisto.getHistogram() # ROOT.TH1

        # residual = normal-embedded
        sigHisto.Add(embHisto, -1)

        sigHisto.SetName(embHisto.GetName()+"Residual")
        if rebin > 1:
            sigHisto.Rebin(rebin)

        return (sigHisto, None)

    ## Get a counter.HistoCounter for a given dataset and counter
    #
    # \param datasetName   Name of the dataset
    # \param name          Name of the counter ROOT histogram
    #
    # \return counter.HistoCounter object
    #
    # For datasets not in \a residualNames, return the embedded result
    #
    # For datasets in \a residualNames, calculate the result as normal-embedded
    def getCounter(self, datasetName, name):
        if not datasetName in self.residualNames:
            return self.datasetsEmb.getCounter(datasetName, name)

        # Ugly hack
        sigName = name
        if isinstance(sigName, basestring):
            sigName = sigName.replace(self.analysisEmb, self.analysisSig)
        else:
            sigName = sigName.clone(tree=sigName.tree.replace(self.analysisEmb, self.analysisSig))

        # Get properly normalized embedded data, embedded DY and normal DY histograms
        (embHisto, tmp) = self.datasetsEmb.getHistogram(datasetName, name)
        sigHisto = self.datasetsSig.getDataset(datasetName).getDatasetRootHisto(sigName) # DatasetRootHisto
        sigHisto.normalizeToLuminosity(self.datasetsEmb.getLuminosity())
        sigHisto = sigHisto.getHistogram() # ROOT.TH1

        table = counter.CounterTable()
        table.appendColumn(counter.HistoCounter("Embedded", embHisto))
        table.appendColumn(counter.HistoCounter("Normal", sigHisto))
        table.removeNonFullRows()

        embColumn = table.getColumn(name="Embedded")
        sigColumn = table.getColumn(name="Normal")
        residual = counter.subtractColumn(datasetName+" residual", sigColumn, embColumn)
        return residual

## Event counter for doing the averaging over many datasets.DatasetManager objects
class EventCounterMany:
    ## Constructor
    #
    # \param datasetsMany   tauEmbedding.DatasetsMany object
    # \param normalize      Apply embedding normalization?
    # \param args           Positional arguments (forwarded to counter.EventCounter.__init__())
    # \param kwargs         Keyword arguments (forwarded to counter.EventCounter.__init__())
    def __init__(self, datasetsMany, normalize=True, *args, **kwargs):
        self.eventCounters = []
        for dsMgr in datasetsMany.datasetManagers:
            ec = counter.EventCounter(dsMgr, *args, **kwargs)
            ec.normalizeMCToLuminosity(datasetsMany.getLuminosity())
            if normalize:
                scaleNormalization(ec)
            self.eventCounters.append(ec)

    ## Remove columns
    #
    # \param datasetNames   List of dataset names to remove
    def removeColumns(self, datasetNames):
        for ec in self.eventCounters:
            ec.removeColumns(datasetNames)

    ## Append row from TTree to main counter
    #
    # \param args   Positional arguments (forwarded to counter.Counter.appendRow())
    # \param kwargs Keyword arguments (forwarded to counter.Counter.appendRow())
    def mainCounterAppendRow(self, *args, **kwargs):
        for ec in self.eventCounters:
            ec.getMainCounter().appendRow(*args, **kwargs)

    def mainCounterAppendRows(self, *args, **kwargs):
        for ec in self.eventCounters:
            ec.getMainCounter().appendRows(*args, **kwargs)

    ## Append row from TTree to a sub counter
    #
    # \param name   Name of the subcounter
    # \param args   Positional arguments (forwarded to counter.Counter.appendRow())
    # \param kwargs Keyword arguments (forwarded to counter.Counter.appendRow())
    def subCounterAppendRow(self, name, *args, **kwargs):
        for ec in self.eventCounters:
            ec.getSubCounter(name).appendRow(*args, **kwargs)

    ## Get main counter table
    #
    # \return counter.CounterTable object
    #
    # Calculated as the mean of the counter.CounterTable objects from
    # the individual trials
    def getMainCounterTable(self):
        return counter.meanTable([ec.getMainCounterTable() for ec in self.eventCounters], uncertaintyByAverage)

    def getMainCounterTableColumn(self, colname):
        tables = []
        for ec in self.eventCounters:
            if colname in ec.getMainCounter().getColumnNames():
                t = ec.getMainCounterTable()
                col = t.getColumn(name=colname)
                tmp = counter.CounterTable()
                tmp.appendColumn(col)
                tables.append(tmp)

        return counter.meanTable(tables, uncertaintyByAverage)

    ## Get subcounter table
    #
    # \param name  Name of the subcounter
    #
    # \return counter.CounterTable object
    #
    # Calculated as the mean of the counter.CounterTable objects from
    # the individual trials
    def getSubCounterTable(self, name):
        return counter.meanTable([ec.getSubCounterTable(name) for ec in self.eventCounters], uncertaintyByAverage)

    ## Get main counter table from fit
    #
    # \return counter.CounterTable object
    #
    # Calculated with a least-square fit of a zero-order polynomial to
    # counter.CounterTable objects from the individual trials
    def getMainCounterTableFit(self):
        return counter.meanTableFit([ec.getMainCounterTable() for ec in self.eventCounters])

    ## Get subcounter table from fit
    #
    # \param name  Name of the subcounter
    #
    # \return counter.CounterTable object
    #
    # Calculated with a least-square fit of a zero-order polynomial to
    # counter.CounterTable objects from the individual trials
    def getSubCounterTableFit(self, name):
        return counter.meanTableFit([ec.getSubCounterTable(name) for ec in self.eventCounters])

    def constructMainTableTEfficiencies(self, function):
        effs = self.eventCounters[0].getMainCounter().constructTEfficiencies(function)
        for ec in self.eventCounters[1:]:
            tmp = ec.getMainCounter().constructTEfficiencies(function)
            for i, eff in enumerate(effs):
                eff.Add(tmp[i])
        return effs

    ## Get current normalization scheme string
    def getNormalizationString(self):
        return self.eventCounters[0].getNormalizationString()

## Event counter for adding the residual MC
class EventCounterResidual:
    ## Constructor
    #
    # \param datasetsResidual  tauEmbedding.DatasetsResidual object
    # \param counters          Name of the counter histogram in the embedded analysis
    # \param kwargs            Keyword arguments (forwarded to counter.EventCounter.__init__())
    def __init__(self, datasetsResidual, counters=None, **kwargs):
        self.datasetsResidual = datasetsResidual
        self.residualNames = datasetsResidual.residualNames

        countersSig = counters
        if countersSig != None:
            countersSig = datasetsResidual._replaceSigName(countersSig)

        self.eventCounterEmb = EventCounterMany(datasetsResidual.datasetsEmb, counters=counters, **kwargs)
        self.eventCounterSig = counter.EventCounter(datasetsResidual.datasetsSig, counters=countersSig, **kwargs)
        self.eventCounterSig.normalizeMCToLuminosity(datasetsResidual.datasetsEmb.getLuminosity())

    ## Append row from TTree to main counter
    #
    # \param rowName   Name of the row
    # \param treeDraw  dataset.TreeDraw object
    #
    # The TTree name should be the one in embedded analysis
    def mainCounterAppendRow(self, rowName, treeDraw):
        treeDrawSig = self.datasetsResidual._replaceSigName(treeDraw)
        self.eventCounterEmb.mainCounterAppendRow(rowName, treeDraw)
        self.eventCounterSig.getMainCounter().appendRow(rowName, treeDrawSig)

    ## Append row from TTree to subcounter
    #
    # \param name      Name of the subcounter
    # \param rowName   Name of the row
    # \param treeDraw  dataset.TreeDraw object
    #
    # The TTree name should be the one in embedded analysis
    def subCounterAppendRow(self, name, rowName, treeDraw):
        treeDrawSig = self.datasetsResidual._replaceSigName(treeDraw)
        self.eventCounterEmb.subCounterAppendRow(name, rowName, treeDraw)
        self.eventCounterSig.getSubCounter(name).appendRow(rowName, treeDrawSig)

    ## Helper function for adding columns for residual datasets
    #
    # \param table     counter.CounterTable for embedding
    # \param sigTable  counter.CounterTable for normal MC
    #
    # \return counter.CounterTable with residual columns added (same object as \a table argument)
    def _calculateResidual(self, table, sigTable):
        columnNames = table.getColumnNames()
        for name in columnNames:
            if name in self.residualNames:
                i = columnNames.index(name)
                col = table.getColumn(index=i)
                table.removeColumn(i)
                col = counter.subtractColumn(name+" residual", sigTable.getColumn(name=name), col)
                table.insertColumn(i, col)
        return table

    ## Get main counter table with residual columns
    #
    # \return counter.CounterTable object
    def getMainCounterTable(self):
        table = self.eventCounterEmb.getMainCounterTable()
        sigTable = self.eventCounterSig.getMainCounterTable()
        
        table = self._calculateResidual(table, sigTable)
        return table

    ## Get subcounter table with residual columns
    #
    # \param name  Name of the subcounter
    #
    # \return counter.CounterTable object
    def getSubCounterTable(self, name):
        table = self.eventCounterEmb.getSubCounterTable(name)
        sigTable = self.eventCounterSig.getSubCounterTable(name)
        
        table = self._calculateResidual(table, sigTable)
        return table


## Plot drawer for embedding plots
#
# Adds the normalization step to the workflow if plots.PlotDrawer
class PlotDrawerTauEmbedding(plots.PlotDrawer):
    ## Constructor
    #
    # \param normalize   Apply embedding normalization
    # \param kwargs      Keyword arguments (forwarded to plots.PlotDrawer.__init__())
    def __init__(self, normalize=True, **kwargs):
        plots.PlotDrawer.__init__(self, **kwargs)
        self.normalizeDefault = normalize

    ## Apply the tau embedding normalization
    #
    # \param p       plots.PlotBase (or deriving) object
    # \param kwargs  Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a normalize   Should embedding normalization be applied? (default given in __init__()/setDefaults())
    def tauEmbeddingNormalization(self, p, **kwargs):
        if kwargs.get("normalize", self.normalizeDefault):
            scaleNormalization(p)

    def __call__(self, p, name, **kwargs):
        self.rebin(p, name, **kwargs)

        self.tauEmbeddingNormalization(p, **kwargs)

        self.stackMCHistograms(p, **kwargs)
        self.createFrame(p, name, **kwargs)
        self.setLegend(p, **kwargs)
        self.addCutLineBox(p, **kwargs)
        self.customise(p, **kwargs)
        self.finish(p, **kwargs)

## Default plot drawer object for tau embedding (embedded data vs. embedded MC) plots
drawPlot = PlotDrawerTauEmbedding(ylabel="Events / %.0f GeV/c", log=True, stackMCHistograms=True, addMCUncertainty=True)


## Plot drawer for embedding vs. normal MC plots
#
# More customization is needed for the uncertainties
class PlotDrawerTauEmbeddingEmbeddedNormal(PlotDrawerTauEmbedding):
    ## Constructor
    #
    # \param kwargs      Keyword arguments (forwarded to tauEmbedding.PlotDrawerTauEmbedding.__init__())
    def __init__(self, **kwargs):
        PlotDrawerTauEmbedding.__init__(self, normalize=False, **kwargs)

    def __call__(self, p, name, **kwargs):
        self.rebin(p, name, **kwargs)

        self.tauEmbeddingNormalization(p, **kwargs)

        sigErr = p.histoMgr.getHisto("Normal").getRootHisto().Clone("Normal_err")
        sigErr.SetFillColor(ROOT.kRed-7)
        sigErr.SetMarkerSize(0)
#        sigErr.SetFillStyle(3005)
        sigErr.SetFillStyle(3545)
        p.prependPlotObject(sigErr, "E2")
        if p.histoMgr.hasHisto("Embedded"):
            embErr = p.histoMgr.getHisto("Embedded").getRootHisto().Clone("Embedded_err")
            embErr.SetFillColor(ROOT.kBlue-7)
#            embErr.SetFillStyle(3004)
            embErr.SetFillStyle(3554)
            embErr.SetMarkerSize(0)
            p.prependPlotObject(embErr, "E2")

        if hasattr(p, "embeddingVariation"):
            p.prependPlotObject(h.embeddingVariation, "[]")
        if hasattr(p, "embeddingDataVariation"):
            p.prependPlotObject(p.embeddingDataVariation, "[]")

        if kwargs.get("log", self.logDefault):
            name = name+"_log"

        self.createFrame(p, name, **kwargs)
        if kwargs.get("ratio", self.ratioDefault):
            p.getFrame2().GetYaxis().SetTitle("Ratio")
            # Very, very ugly hack

            for r in p.ratioHistoMgr.getHistos():
                r.getRootHisto().SetLineStyle(1)

            if p.histoMgr.hasHisto("EmbeddedData"):
                if p.ratios[1].getName() != "Embedded":
                    raise Exception("Assumption that [1] is from embedded MC failed")
                p.ratios[1].setDrawStyle("PE2")
                rh = p.ratios[1].getRootHisto()
                rh.SetFillColor(ROOT.kBlue-7)
#                rh.SetFillStyle(3004)
                rh.SetFillStyle(3554)

        self.setLegend(p, **kwargs)
        # Add the legend box for stat uncertainty band
        tmp = sigErr.Clone("tmp")
        tmp.SetFillColor(ROOT.kBlack)
#        tmp.SetFillStyle(3013)
        tmp.SetFillStyle(3444)
        tmp.SetLineColor(ROOT.kWhite)
        if not p.histoMgr.hasHisto("Embedded"):
            tmp.SetFillStyle(sigErr.GetFillStyle())
            tmp.SetFillColor(sigErr.GetFillColor())
        p.legend.AddEntry(tmp, "Stat. unc.", "F")

        # Add "legend" entries manually for brackets in embedded variations
        x = p.legend.GetX1()
        y = p.legend.GetY1()
        x += 0.05; y -= 0.03
        if hasattr(p, "embeddingDataVariation"):
            p.appendPlotObject(histograms.PlotText(x, y, "[  ]", size=17, color=p.embeddingDataVariation.GetMarkerColor())); x += 0.05
            p.appendPlotObject(histograms.PlotText(x, y, "Embedded data min/max", size=17)); y-= 0.03
        if hasattr(p, "embeddingVariation"):
            p.appendPlotObject(histograms.PlotText(x, y, "[  ]", size=17, color=p.embeddingVariation.GetMarkerColor())); x += 0.05
            p.appendPlotObject(histograms.PlotText(x, y, "Embedded sim. min/max", size=17)); y-= 0.03

        self.addCutLineBox(p, **kwargs)
        self.customise(p, **kwargs)
        self.finish(p, **kwargs)

## Plot creator for embedded vs. normal plots
class PlotCreatorMany:
    ## Constructor
    #
    # \param analysisEmb    Name of the embedding analysis TDirectory
    # \param analysisSig    Name of the normal MC analysis TDirectory
    # \param datasetsEmb    tauEmbedding.DatasetsMany object for embedded datasets
    # \param datasetsSig    dataset.DatasetManager object for normal MC datasets
    # \param datasetName    Name of the dataset
    # \param styles         List of plot styles
    # \param addData        Add embedded data?
    # \param addVariation   Add min/max values from embedding trials?
    def __init__(self, analysisEmb, analysisSig, datasetsEmb, datasetsSig, datasetName, styles, addData=False, addVariation=False, ntupleCacheEmb=None, ntupleCacheSig=None):
        self.analysisEmb = analysisEmb
        self.analysisSig = analysisSig
        self.datasetsEmb = datasetsEmb # DatasetsMany
        self.datasetsSig = datasetsSig # DatasetManager
        self.datasetName = datasetName
        self.styles = styles # list of styles
        self.addData = addData
        self.addVariation = addVariation
        try:
            self.isResidual = self.datasetsEmb.isResidualAdded(datasetName)
        except:
            self.isResidual = False

        self.ntupleCacheEmb = ntupleCacheEmb
        self.ntupleCacheSig = ntupleCacheSig

    ## Function call syntax for creating the plot
    #
    # \param name   Name of the histogram (with embedding analysis path)
    # \param rebin  Rebin
    #
    # \return plots.PlotBase derived object
    def __call__(self, name, rebin=1):
        lumi = self.datasetsEmb.getLuminosity()

        name2Emb = name
        name2Sig = name
        if isinstance(name, basestring):
            name2Emb = self.analysisEmb+"/"+name
            name2Sig = self.analysisSig+"/"+name
        elif isinstance(name, dataset.NtupleCacheDrawer):
            name2Emb = self.ntupleCacheEmb.histogram(name.histoName)
            name2Sig = self.ntupleCacheSig.histogram(name.histoName)
        else: # assume TreeDraw
            name2Emb = name.clone(tree=self.analysisEmb+"/tree")
            name2Sig = name.clone(tree=self.analysisSig+"/tree")
        
        (emb, embVar) = self.datasetsEmb.getHistogram(self.datasetName, name2Emb, rebin)
        sig = self.datasetsSig.getDataset(self.datasetName).getDatasetRootHisto(name2Sig)
        sig.normalizeToLuminosity(lumi)
        sig = sig.getHistogram()
        if rebin > 1:
            sig.Rebin(rebin)

        emb.SetName("Embedded")
        sig.SetName("Normal")
        p = None
        sty = self.styles[:]
        if self.addData:
            (embData, embDataVar) = self.datasetsEmb.getHistogram("Data", name2Emb, rebin=rebin)
            embData.SetName("EmbeddedData")
            p = plots.ComparisonManyPlot(sig, [embData, emb])
            p.histoMgr.reorderDraw(["EmbeddedData", "Embedded", "Normal"])
            p.histoMgr.reorderLegend(["EmbeddedData", "Embedded", "Normal"])
            p.histoMgr.setHistoDrawStyle("EmbeddedData", "EP")
            p.histoMgr.setHistoLegendStyle("EmbeddedData", "P")
            p.histoMgr.setHistoLegendStyle("Embedded", "PL")
            p.setLuminosity(lumi)
            sty = [styles.dataStyle]+sty
        else:
            p = plots.ComparisonPlot(emb, sig)

        embedded = "Embedded "
        legLabel = plots._legendLabels.get(self.datasetName, self.datasetName)
        legLabelEmb = legLabel
        if legLabel != "Data":
            legLabel += " sim."
        residual = ""
        if self.isResidual:
            embedded = "Emb. "
            residual = " + res. sim."
        legLabelEmb += " sim."

        p.setLuminosity(lumi)
        p.histoMgr.setHistoLegendLabelMany({
                "Embedded":     embedded + legLabelEmb + residual,
                "Normal":       "Normal " + legLabel,
                "EmbeddedData": embedded+"data"+residual,
                })
        p.histoMgr.forEachHisto(styles.Generator(sty))
        if self.addVariation:
            if self.addData:
                if embDataVar != None:
                    aux.copyStyle(p.histoMgr.getHisto("EmbeddedData").getRootHisto(), embDataVar)
                    embDataVar.SetMarkerStyle(2)
                    p.embeddingDataVariation = embDataVar
            if embVar != None:
                aux.copyStyle(p.histoMgr.getHisto("Embedded").getRootHisto(), embVar)
                embVar.SetMarkerStyle(2)
                p.embeddingVariation = embVar
    
        return p


def strIntegral(th1):
    return "%.1f" % aux.th1Integral(th1)

def writeToFile(optMode, fname, content):
    d = optMode
    if d is None:
        d = "."
    if not os.path.exists(d):
        os.makedirs(d)

    f = open(os.path.join(d, fname), "w")
    f.write(content)
    f.write("\n")
    f.close()

class CommonPlotter:
    def __init__(self, optimizationMode, midfix, plotDrawer):
        self._ind = 0
        self._optMode = optimizationMode
        self._midfix = midfix
        self._plotDrawer = plotDrawer

        if self._optMode is not None and not os.path.exists(self._optMode):
            os.mkdir(self._optMode)

    def getOutputDirectory(self):
        if self._optMode is None:
            return "."
        return self._optMode

    def _createPlot(self, name):
        p = self._plotCreator(name)
        return p

    def _drawPlotCommon(self, plot, name, *args, **kwargs):
        kargs = {}
        kargs.update(kwargs)
        if name in self._plotOptions:
            kargs.update(self._plotOptions[name])
        if not "rebin" in kwargs and not "rebinToWidthX" in kwargs:
            name2 = name
            if name2[-4:] == "_log":
                name2 = name[:-4]
            kargs["rebin"] = systematics.getBinningForPlot(name2)
        if not "cmsTextPosition" in kargs:
            kargs["cmsTextPosition"] = "outframe"

        self._plotDrawer(plot, *args, **kargs)

    def _drawPlot(self, plot, name, *args, **kwargs):
        if plot is None:
            return
        self._ind += 1
        if self._datasetName is None:
            path = "%03d_%s_%s" % (self._ind, self._midfix, name)
        else:
            path = "%03d_%s_%s_%s" % (self._ind, self._midfix, self._datasetName, name)
        if self._optMode is not None:
            path = "%s/%s" % (self._optMode, path)
        self._drawPlotCommon(plot, name, path, *args, **kwargs)

    def plot(self, datasetName, plotCreator, plotOptions={}):
        self._datasetName = datasetName
        self._plotCreator = plotCreator
        self._plotOptions = plotOptions

#        opts2def = {"ymin": 0.8, "ymax": 1.2}
#        opts2def = {"ymin": 0.5, "ymax": 1.5}
        opts2def = {"ymin": 0, "ymax": 2}

        def drawControlPlot(path, *args, **kwargs):
            self._drawPlot(self._createPlot("ForDataDrivenCtrlPlots/"+path), path, *args, **kwargs)

        def update(d1, d2):
            tmp = {}
            tmp.update(d1)
            tmp.update(d2)
            return tmp

        # Control plots
        optsdef = {}
        opts = optsdef

        # After Njets
        tauPtBins = [0]+range(40, 160, 10)+[160, 200, 300, 400, 500]
        tauEtaBins = [-2.1, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.1]
        drawControlPlot("SelectedTau_pT_AfterStandardSelections", xlabel="Selected #tau p_{T} (GeV/c)",
                        #ylabel="Events / #Delta p_{T} / %.0f-%.0f GeV/c",
                        ylabel="< Events / GeV/c >",
                        divideByBinWidth=True, opts={"ymin": 1e-3})
        drawControlPlot("SelectedTau_eta_AfterStandardSelections", opts={"xmin": -2.1, "xmax": 2.1}, moveLegend={"dy": -0.4})
        drawControlPlot("SelectedTau_phi_AfterStandardSelections", moveLegend={"dy": -0.4})
        drawControlPlot("SelectedTau_Rtau_AfterStandardSelections", opts={"xmin": 0.7, "xmax":1 }, moveLegend={"dy": -0.4, "dx": -0.3}, ylabel="Events / %.2f")
        drawControlPlot("Njets_AfterStandardSelections", ylabel="Events", opts={"xmin": 3, "xmax": 10, "ymin": 1})
        drawControlPlot("JetPt_AfterStandardSelections", divideByBinWidth=True)
        drawControlPlot("JetEta_AfterStandardSelections", moveLegend={"dy": -0.4})

#        drawControlPlot("NjetsAfterJetSelectionAndMETSF", opts={"xmin": 0, "xmax": 16}, ylabel="Events", cutLine=3)
#        drawControlPlot("ImprovedDeltaPhiCutsJet1Collinear", rebinToWidthX=10)
#        drawControlPlot("ImprovedDeltaPhiCutsJet2Collinear", rebinToWidthX=10, moveLegend={"dy": -0.4, "dx": -0.2})<
#        drawControlPlot("ImprovedDeltaPhiCutsJet3Collinear", rebinToWidthX=10, moveLegend={"dy": -0.4, "dx": -0.2})
        drawControlPlot("ImprovedDeltaPhiCutsCollinearMinimum", rebinToWidthX=10)

        moveLegend = {"DYJetsToLL": {"dx": -0.02}}.get(datasetName, {})
        drawControlPlot("MET",
                        #"Uncorrected PF E_{T}^{miss} (GeV)",
                        "Type I PF E_{T}^{miss} (GeV)",
                        #ylabel="Events / #Delta E_{T}^{miss} / %.0f-%.0f GeV",
                        ylabel="< Events / GeV >",
                        divideByBinWidth=True,
                        opts=update(opts, {"xmax": 500, "ymin": 1e-3}),
                        #cutLine=50,
                        moveLegend=moveLegend)

        drawControlPlot("METPhi", rebin=2, moveLegend={"dy": -0.4})


        # after MET
        moveLegend = {"dx": -0.5, "dy": -0.45}
        moveLegend = {
            "WJets": {},
            "DYJetsToLL": {"dx": -0.02},
            "SingleTop": {},
            "Diboson": {}
            }.get(datasetName, moveLegend)
        drawControlPlot("NBjets", "Number of selected b jets", opts=update(opts, {"xmax": 6, "ymin": 1e-1}), ylabel="Events", moveLegend=moveLegend,
                        #cutLine=1
        )

        drawControlPlot("BtagDiscriminator", opts={"xmin": -1, "xmax": 1.5}, ylabel="Events / %.1f")
        bjetPtBins = [0]+range(30, 100, 10)+range(100, 200, 20)+[200, 250, 300, 400, 500]
        drawControlPlot("BJetPt", rebin=bjetPtBins, divideByBinWidth=True)
        drawControlPlot("BJetEta", rebin=2, opts={"xmin": -2.4, "xmax": 2.4}, moveLegend={"dy": -0.4})

        # DeltapPhi
        opts = {
#            "WJets": {"ymax": 35},
#            "DYJetsToLL": {"ymax": 12},
#            "Diboson": {"ymax": 1},
            }.get(datasetName, {"ymaxfactor": 1.2})
        opts2=opts2def
        moveLegend = {
            "DYJetsToLL": {"dx": -0.24},
            }.get(datasetName, {"dx":-0.22})
#        drawControlPlot("ImprovedDeltaPhiCutsJet1BackToBack", rebinToWidthX=10, moveLegend={"dy": -0.4})
#        drawControlPlot("ImprovedDeltaPhiCutsJet2BackToBack", rebinToWidthX=10, moveLegend={"dy": -0.4})
#        drawControlPlot("ImprovedDeltaPhiCutsJet3BackToBack", rebinToWidthX=10, moveLegend={"dy": -0.4})
        drawControlPlot("ImprovedDeltaPhiCutsBackToBackMinimum", "R^{min}_{bb}, {}^{o}", ylabel="Events / %.0f^{o}", rebinToWidthX=20, moveLegend={"dx": -0.4, "dy": -0.45})

        # Remaining control plots
        #drawControlPlot("TopMass")
        #drawControlPlot("TopPt")
        #drawControlPlot("WMass")
        #drawControlPlot("WPt")

        # Transverse mass
        drawControlPlot("SelectedTau_pT_AfterMtSelections", xlabel="Selected #tau p_{T} (GeV/c)",
                        #ylabel="Events / #Delta p_{T} / %.0f-%.0f GeV/c",
                        ylabel="< Events / GeV/c >",
                        divideByBinWidth=True, opts={"ymin": 1e-3})
        drawControlPlot("SelectedTau_eta_AfterMtSelections", xlabel="Selected #tau #eta", 
                        #ylabel="Events / %.1f-%.1f",
                        ylabel="Events",
                        opts={"xmin": -2.5, "xmax": 2.5}, moveLegend={"dx": -0.3, "dy": -0.4})
        drawControlPlot("SelectedTau_phi_AfterMtSelections", xlabel="Selected #tau #phi",
                        #ylabel="Events / %.2f-%.2f",
                        ylabel="Events",
                        moveLegend={"dy": -0.4})
        drawControlPlot("SelectedTau_LeadingTrackPt_AfterMtSelections", rebin=range(0, 100, 10)+[150,200,300,400,500], divideByBinWidth=True, opts={"ymin": 1e-3})

        maxModes = 5
        drawControlPlot("SelectedTau_DecayMode_AfterMtSelections", xlabel="Selected #tau decay mode", ylabel="Events", opts={"xmax": maxModes, "nbinsx": maxModes, "ymin": 1}, customizeBeforeDraw=lambda p: decayModeLabels(p, maxModes))
        drawControlPlot("SelectedTau_Rtau_AfterMtSelections", xlabel="Selected #tau R_{#tau}", ylabel="Events / %.2f", opts={"xmin": 0.7, "xmax":1 }, moveLegend={"dy": -0.4, "dx": -0.3})
        drawControlPlot("Njets_AfterMtSelections", ylabel="Events")
        drawControlPlot("JetPt_AfterMtSelections",
                        #ylabel="Events / #Delta p_{T} / %.0f-%.0f GeV/c",
                        ylabel="< Events / GeV/c >",
                        divideByBinWidth=True)
        drawControlPlot("JetEta_AfterMtSelections", ylabel="Events / %.1f", opts={"ymin": 1e-1}, moveLegend={"dy": -0.4})
        drawControlPlot("METAfterMtSelections", "Type I PF E_{T}^{miss} (GeV)",
                        #ylabel="Events / #Delta E_{T}^{miss} / %.0f-%.0f GeV",
                        ylabel="< Events / GeV >",
                        divideByBinWidth=True, opts={"ymin": 1e-3}, moveLegend={"dx": -0.05, "dy":-0.2})
        drawControlPlot("METPhiAfterMtSelections", "E_{T}^{miss} #phi",
                        #ylabel="Events / %.2f-%.2f",
                        ylabel="Events",
                        moveLegend={"dy": -0.4}, opts={"ymaxfactor": 10})
        drawControlPlot("NBjetsAfterMtSelections", ylabel="Events", opts={"ymin": 1e-1})
        drawControlPlot("BJetPtAfterMtSelections",
                        #ylabel="Events / #Delta p_{T} / %.0f-%.0f GeV/c",
                        ylabel="< Events / GeV/c >",
                        divideByBinWidth=True)
        drawControlPlot("BJetEtaAfterMtSelections", ylabel="Events / %.1f", opts={"xmin": -2.5, "xmax": 2.5}, moveLegend={"dy": -0.4})
        drawControlPlot("BtagDiscriminatorAfterMtSelections", opts={"xmin": -1, "xmax": 1, "ymin": 1},
                        ylabel="Events",
                        #ylabel="Events / %.2f-%.2f",
                        moveLegend={"dy": -0.4})
        drawControlPlot("ImprovedDeltaPhiCutsCollinearMinimumAfterMtSelections", "R_{coll}^{min} (^{o})", ylabel="Events / %.0f^{o}", opts={"ymin": 1e-1}, moveLegend={"dy": -0.43, "dx": -0.3})
        drawControlPlot("ImprovedDeltaPhiCutsBackToBackMinimumAfterMtSelections", "R_{bb}^{min} (^{o})", ylabel="Events / %.0f^{o}", opts={"ymin": 1e-1}, moveLegend={"dy": -0.43, "dx": -0.2})

        opts = {
#            "TTJets": {"ymax": 28},
#            "SingleTop": {"ymax": 4.5},
#            "DYJetsToLL": {"ymax": 18},
#            "Diboson": {"ymax": 1.2},
#            "WJets": {"ymax": 50},
            }.get(datasetName, {})
        #opts["xmax"] = 400
        #opts2 = {"ymin": 0, "ymax": 2}
        moveLegend = {"DYJetsToLL": {"dx": -0.02}}.get(datasetName, {})
        p = self._createPlot("shapeTransverseMass")
        #p.appendPlotObject(histograms.PlotText(0.6, 0.7, "#Delta#phi(#tau jet, E_{T}^{miss}) < 160^{o}", size=20))
        self._drawPlot(p, "shapeTransverseMass", "m_{T} (GeV)", # (^{}#tau_{h}, ^{}E_{T}^{miss}) (GeV)",
                       #ylabel="Events / #Delta m_{T} %.0f-%.0f GeV",
                       ylabel="< Events / GeV >",
                       log=False, moveLegend=moveLegend,
                       opts=opts,
                       #opts2=opts2,
                       divideByBinWidth=True,
                       cmsTextPosition="right"
                 )
        p = self._createPlot("shapeTransverseMass")
        self._drawPlot(p, "shapeTransverseMass_log", "m_{T} (GeV)", #"m_{T}(^{}#tau_{h}, ^{}E_{T}^{miss}) (GeV)",
                       #ylabel="Events / #Delta m_{T} %.0f-%.0f GeV",
                       ylabel="< Events / GeV >",
                       log=True, moveLegend=moveLegend,
                       opts={"ymin": 1e-3},
                       #opts2=opts2,
                       divideByBinWidth=True,
                       cmsTextPosition="right"
                 )

        self._drawPlot(self._createPlot("shapeInvariantMass"), "shapeInvariantMass", 
                       xlabel="m_{H^{+}} (GeV/c^{2})",
                       ylabel="< Events / GeV/c^{2} >",
                       log=False, divideByBinWidth=True)


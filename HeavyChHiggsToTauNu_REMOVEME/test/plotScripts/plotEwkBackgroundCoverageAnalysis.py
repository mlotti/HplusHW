#!/usr/bin/env python

######################################################################
#
# This plot script is for studying the coverage of the EWK background
# measurement. The corresponding python job configuration is
# ewkBackgroundCoverageAnalysis_cfg.py
#
# Authors: Matti Kortelainen
#
######################################################################

import math
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import *

#analysis = "ewkBackgroundCoverageAnalysis"
dataEra = "Run2011AB"

# Enumerations
class Enum:
    (tauNone, tauTau1, tauTau1OtherCorrect, tauTau1OtherWrong, tauObj2, tauObj2Other, tauOther, tauSize) = range(0, 8)
    (leptonNone, leptonTau1, leptonObj2, leptonOther, leptonSize) = range(0, 5)
    (obj2None, obj2Electron, obj2Muon, obj2MuonEmb, obj2Quark, obj2TauNotInAcceptance, obj2Tauh, obj2Taue, obj2Taumu, obj2TaumuEmb, obj2Size) = range(0, 11)

# Bin labels
def tauIDLabels(obj2):
    return ["None", "#tau_{1}", "#tau_{1}+other (corr. sel.)", "#tau_{1}+other (wrong sel.)", obj2, obj2+"+other", "Other"]
def leptonVetoLabels(obj2):
    return ["None", "#tau_{1}", obj2, "Other"]
    


def main(opts):
    datasets = dataset.getDatasetsFromMulticrabCfg(directory=opts.mdir, dataEra=dataEra, weightedCounters=False)
#    datasets = dataset.getDatasetsFromRootFiles([("TTJets_TuneZ2_Summer11", "histograms.root")], counters=counters, dataEra=dataEra, analysisBaseName=analysis, weightedCounters=False)

    plots.mergeRenameReorderForDataMC(datasets)

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    process(datasets, "TTJets", "Before", ">= 1 genuine tau in acceptance")
#    process(datasets, "TTJets", "AfterJetSelection", "njets")
#    process(datasets, "TTJets", "AfterMET", "MET")
#    process(datasets, "TTJets", "AfterBTag", "btagging")
#    process(datasets, "TTJets", "AfterAllSelections", "DeltaPhi(Tau MET) upper limit")

class Counts:
    def __init__(self):
        self._fields = ["all", "rejected", "embedding", "faketau", # properly included ones
                        "case1",
                        "case2",
                        "case3",
                        "case4"]
        for f in self._fields:
            setattr(self, f, 0)

    def __iadd__(self, counts):
        if not isinstance(counts, Counts):
            raise Exception("counts is not Counts")

        for f in self._fields:
            setattr(self, f, getattr(self, f) + getattr(counts, f))

        return self

    def crossCheck(self):
        s = sum([getattr(self, f) for f in self._fields[1:]])
        if int(s) != int(self.all):
            raise Exception("Cross check failed, self.all = %d, s = %d" % (int(self.all), int(s)))

    def printResults(self):
        print "All events:           %d" % int(self.all)
        print "Correctly rejected:   %d" % int(self.rejected)
        print "Embedding (included): %d" % int(self.embedding)
        print "Fake tau (included):  %d" % int(self.faketau)
        print "Case 1:               %d" % int(self.case1)
        print "Case 2:               %d" % int(self.case2)
        print "Case 3:               %d" % int(self.case3)
        print "Case 4:               %d" % int(self.case4)

    def printLegend(self):
        print "Case 1 (event incorrectly included): tau_1 identified in lepton veto and in tau ID"
        print "Case 2 (event incorrectly rejected): tau_1 not identified as tau_h, but decay of tau_2 would be"
        print "Case 3 (event correctly included): wrong object selected as tau_h"
        print "Case 4 (event incorrectly rejected): mu_2 accepted for embedding, but not identified in lepton veto"



def process(datasets, datasetName, postfix, countName):
    # Handle counter
    eventCounter = counter.EventCounter(datasets)
    mainTable = eventCounter.getMainCounterTable()

    neventsCount = mainTable.getCount(rowName=countName, colName=datasetName)
    nevents = neventsCount.value()
#    column = eventCounter.getSubCounterTable("Classification"+postfix).getColumn(name=datasetName)
#
#    columnFraction = column.clone()
#    columnFraction.setName("Fraction (%)")
#
#    # Consistency check, and do the division
#    tmp = 0
#    for irow in xrange(column.getNrows()):
#        tmp += column.getCount(irow).value()
#
#        frac = dataset.divideBinomial(columnFraction.getCount(irow), neventsCount)
#        frac.multiply(dataset.Count(100))
#        columnFraction.setCount(irow, frac)
#
#    if int(nevents) != int(tmp):
#        raise Exception("Consistency check failed: nevents = %d, tmp = %d" % (int(nevents), int(tmp)))
#
    table = counter.CounterTable()
#    table.appendColumn(column)
#    table.appendColumn(columnFraction)
#
    cellFormat = counter.CellFormatText(valueFormat='%.4f', withPrecision=2)
    tableFormat = counter.TableFormatText(cellFormat)

    print
    print "Dataset %s, step %s, nevents %d" % (datasetName, postfix, int(nevents))
    print table.format(tableFormat)

    # Make plots
    dset = datasets.getDataset(datasetName)
    tmp = Counts()
    oldCanvasDefW = ROOT.gStyle.GetCanvasDefW()
    ROOT.gStyle.SetCanvasDefW(int(oldCanvasDefW*1.5))

    # (tauID, leptonVeto)
    def usualRejected(obj2):
        _tauIDLabels = tauIDLabels(obj2)
        ret = [("None", "None"), ("None", "#tau_{1}")]
        ret.extend([(x, "#tau_{1}") for x in _tauIDLabels[4:]])
        ret.extend([(x, obj2) for x in _tauIDLabels])
        ret.extend([(x, "Other") for x in _tauIDLabels])
        return ret
    usualEmbedding = [("#tau_{1}", "None"), ("#tau_{1}+other (corr. sel.)", "None")]
    def usualFakeTau(obj2):
        return [(x, "None") for x in tauIDLabels(obj2)[4:]]
    doubleFakeTau = [("Other", "None")]
    usualCase1 = [(x, "#tau_{1}") for x in tauIDLabels("")[1:4]]
    usualCase3 = [("#tau_{1}+other (wrong sel.)", "None")]
    embCase4 = [(x, "None") for x in tauIDLabels("")[1:4]]
    def doubleCase2(obj2):
        return [(obj2, "None"), (obj2+"+other", "None")]

    selectionStep = {"Before": "",
                     "AfterJetSelection": "passJetSelection",
                     "AfterMET": "passMET",
                     "AfterBTag": "passBTag",
                     "AfterAllSelections": "passDeltaPhi"}[postfix]

    treeDraw = dataset.TreeDraw("tree", varexp="LeptonVetoStatus:TauIDStatus >>htemp(%d,0,%d, %d,0,%d" % (Enum.tauSize, Enum.tauSize, Enum.leptonSize, Enum.leptonSize))

    for name, obj2, obj2Type in [
        ("tau1_electron2", "e_{2}", Enum.obj2Electron),
        ("tau1_quark2", "q_{2}", Enum.obj2Quark),
        ("tau1_muon2_nonEmb", "#mu_{2}", Enum.obj2Muon),
        ]:
        tmp += calculatePlot(dset, neventsCount, name, postfix,
                             treeDraw=treeDraw.clone(selection=And("Obj2Type==%d"%obj2Type, selectionStep), binLabelsX=tauIDLabels(obj2), binLabelsY=leptonVetoLabels(obj2)),
                             rejected=usualRejected(obj2), embedding=usualEmbedding, faketau=usualFakeTau(obj2),
                             case1=usualCase1, case3=usualCase3)

    tmp += calculatePlot(dset, neventsCount, "tau1_muon2_Emb", postfix,
                         treeDraw=treeDraw.clone(selection=And("Obj2Type==%d"%Enum.obj2MuonEmb, selectionStep), binLabelsX=tauIDLabels("#mu_{2}"), binLabelsY=leptonVetoLabels("#mu_{2}")),
                         rejected=usualRejected("#mu_{2}")+usualCase1,
                         faketau=usualFakeTau("#mu_{2}"),
                         case4=embCase4)
#    createMuon2Plot(dset, "tau1_muon2_Emb", postfix)

    for name, obj2, obj2Type in [
        ("tau1_tau2_notInAcceptance", "#tau_{2}", Enum.obj2TauNotInAcceptance),
        ("tau1_tauh2", "#tau_{h,2}", Enum.obj2Tauh),
        ("tau1_taue2", "#tau_{e,2}", Enum.obj2Taue),
        ("tau1_taumu2_nonEmb", "#tau_{#mu,2}", Enum.obj2Taumu),
        ]:
        tmp += calculatePlot(dset, neventsCount, name, postfix,
                             treeDraw=treeDraw.clone(selection=And("Obj2Type==%d"%obj2Type, selectionStep), binLabelsX=tauIDLabels(obj2), binLabelsY=leptonVetoLabels(obj2)),
                             rejected=usualRejected(obj2), embedding=usualEmbedding, faketau=doubleFakeTau,
                             case1=usualCase1, case3=usualCase3,
                             case2=doubleCase2(obj2))

    tmp += calculatePlot(dset, neventsCount, "tau1_taumu2_Emb", postfix,
                         treeDraw=treeDraw.clone(selection=And("Obj2Type==%d"%Enum.obj2TaumuEmb, selectionStep), binLabelsX=tauIDLabels("#tau_{#mu,2}"), binLabelsY=leptonVetoLabels("#tau_{#mu,2}")),
                         rejected=usualRejected("#tau_{#mu,2}")+usualCase1,
                         faketau=doubleFakeTau,
                         case4=embCase4)

    ROOT.gStyle.SetCanvasDefW(oldCanvasDefW)


    ## Ntuple stuff

    embeddingSelection = Or(*[And("Obj2Type == %d"%obj2, "LeptonVetoStatus == %d"%Enum.leptonNone, Or(*["TauIDStatus == %d" % x for x in [Enum.tauTau1, Enum.tauTau1OtherCorrect]]))
                              for obj2 in [Enum.obj2Electron, Enum.obj2Quark, Enum.obj2Muon, Enum.obj2TauNotInAcceptance, Enum.obj2Tauh, Enum.obj2Taue, Enum.obj2Taumu]])
    case1Selection = Or(*[And("Obj2Type == %d"%obj2, "LeptonVetoStatus == %d"%Enum.leptonTau1, Or(*["TauIDStatus == %d" % x for x in [Enum.tauTau1, Enum.tauTau1OtherCorrect, Enum.tauTau1OtherWrong]]))
                              for obj2 in [Enum.obj2Electron, Enum.obj2Quark, Enum.obj2Muon, Enum.obj2TauNotInAcceptance, Enum.obj2Tauh, Enum.obj2Taue, Enum.obj2Taumu]])
    case2Selection = Or(*[And("Obj2Type == %d"%obj2, "LeptonVetoStatus == %d"%Enum.leptonNone, Or(*["TauIDStatus == %d" % x for x in [Enum.tauObj2, Enum.tauObj2Other]]))
                              for obj2 in [Enum.obj2TauNotInAcceptance, Enum.obj2Tauh, Enum.obj2Taue, Enum.obj2Taumu]])

    embeddingSelection = And(selectionStep, embeddingSelection)
    case1Selection = And(selectionStep, case1Selection)
    case2Selection = And(selectionStep, case2Selection)
    
    createTransverseMassPlot(dset, "case1", postfix, nominalSelection=embeddingSelection, compareSelection=case1Selection,
                             nominalLegend="Embedding (correct)", compareLegend="Case 1")
    createTransverseMassPlot(dset, "case2", postfix, nominalSelection=embeddingSelection, compareSelection=case2Selection,
                             nominalLegend="Embedding (correct)", compareLegend="Case 2")

    # plotNames = [
    #             "tau1_electron2",
    #             "tau1_quark2",
    #             "tau1_muon2_nonEmb",     
    #             "tau1_muon2_Emb",
    #             "tau1_tau2_notInAcceptance",
    #             "tau1_tauh2", 
    #             "tau1_taue2",
    #             "tau1_taumu2_nonEmb",
    #             "tau1_taumu2_Emb"
    #             ]
    # for name in plotNames:
    #     tmp += calculatePlot(dset, neventsCount, name, postfix)

    if int(nevents) != int(tmp.all):
        raise Exception("Consistency check failed: nevents = %d, tmp = %d" % (int(nevents), int(tmp.all)))

    tmp.printResults()
    print
    tmp.printLegend()
    tmp.crossCheck()

    allEmbeddingIncluded = int(tmp.embedding) + int(tmp.case1) + int(tmp.case3)

    print
    print "So, the number of events included by embedding is %d" % allEmbeddingIncluded
    print "Of these,"
 
    frac = dataset.divideBinomial(dataset.Count(int(tmp.embedding)), dataset.Count(allEmbeddingIncluded))
    frac.multiply(dataset.Count(100))
    print "  * %d (%s %%) are included correctly" % (int(tmp.embedding), cellFormat.format(frac))

    frac = dataset.divideBinomial(dataset.Count(int(tmp.case3)), dataset.Count(allEmbeddingIncluded))
    frac.multiply(dataset.Count(100))
    print "  * %d (%s %%) are included correctly, but wrong object is chosen as tau_h" % (int(tmp.case3), cellFormat.format(frac))

    frac = dataset.divideBinomial(dataset.Count(int(tmp.case1)), dataset.Count(allEmbeddingIncluded))
    frac.multiply(dataset.Count(100))
    print "  * %d (%s %%) are included incorrectly (tau_1 identified in lepton veto)" % (int(tmp.case1), cellFormat.format(frac))

    print "In addition, the following events are incorrectly rejected"
    # Note that these ratios are NOT binomial!
    # Although apparently, in practice, the result is the same
    
    #frac = dataset.divideBinomial(dataset.Count(int(tmp.case2)), dataset.Count(allEmbeddingIncluded))
    frac = dataset.Count(tmp.case2, math.sqrt(tmp.case2))
    frac.divide(dataset.Count(allEmbeddingIncluded, math.sqrt(allEmbeddingIncluded)))
    frac.multiply(dataset.Count(100))
    print "  * %d (%s %%): tau_1 not identified as tau_h, but decay of tau_2 would be" % (int(tmp.case2), cellFormat.format(frac))

    #frac = dataset.divideBinomial(dataset.Count(int(tmp.case4)), dataset.Count(allEmbeddingIncluded))
    frac = dataset.Count(tmp.case4, math.sqrt(tmp.case4))
    frac.divide(dataset.Count(allEmbeddingIncluded, math.sqrt(allEmbeddingIncluded)))
    frac.multiply(dataset.Count(100))
    print "  * %d (%s %%): mu_2 would be accepted for embedding, and is not identified in lepton veto" % (int(tmp.case4), cellFormat.format(frac))
    


def calculatePlot(dset, neventsCount, name, postfix, treeDraw=None, rejected=None, embedding=None, faketau=None, case1=None, case2=None, case3=None, case4=None):
    datasetName = dset.getName()
    if treeDraw is None:
        h = dset.getDatasetRootHisto(name+"_"+postfix).getHistogram()
    else:
        h = dset.getDatasetRootHisto(treeDraw).getHistogram()
    ROOT.gStyle.SetPaintTextFormat(".0f")
    createDrawPlot("count_"+datasetName+"_"+name+"_"+postfix, h)

    hFrac = h.Clone("hfrac")
    hFracErr = h.Clone("hfracErr")
    counts = Counts()
    for xbin in xrange(1, h.GetNbinsX()+1):
        for ybin in xrange(1, h.GetNbinsY()+1):
            value = h.GetBinContent(xbin, ybin)
            counts.all += value

            this = (h.GetXaxis().GetBinLabel(xbin), h.GetYaxis().GetBinLabel(ybin))
            if rejected is not None and this in rejected:
                counts.rejected += value
            elif embedding is not None and this in embedding:
                counts.embedding += value
            elif faketau is not None and this in faketau:
                counts.faketau += value
            elif case1 is not None and this in case1:
                counts.case1 += value
            elif case2 is not None and this in case2:
                counts.case2 += value
            elif case3 is not None and this in case3:
                counts.case3 += value
            elif case4 is not None and this in case4:
                counts.case4 += value

            frac = dataset.divideBinomial(dataset.Count(value, 0), neventsCount)
            frac.multiply(dataset.Count(100))
            hFrac.SetBinContent(xbin, ybin, frac.value())
            hFracErr.SetBinContent(xbin, ybin, frac.uncertainty())

#    print name
#    counts.printResults()
#    print
    try:
        counts.crossCheck()
    except Exception as e:
        raise Exception(str(e)+"\nBin sources:\nrejected: %s\nembedding: %s\nfaketau: %s\ncase1: %s\ncase2: %s\ncase3: %s\ncase4: %s" % (rejected, embedding, faketau, case1, case2, case3, case4))


    ROOT.gStyle.SetPaintTextFormat(".4f")
    createDrawPlot("frac_"+datasetName+"_"+name+"_"+postfix, hFrac)
#    createDrawPlot("frac_"+datasetName+"_"+name+"_"+postfix+"_Uncertainty", hFracErr)

    return counts

def createMuon2Plot(dset, name, postfix):
    datasetName = dset.getName()
    treeDraw = dataset.TreeDraw("tree", selection="Obj2Type == 3 && LeptonVetoStatus == 0 && (TauIDStatus == 1 || TauIDStatus == 2 || TauIDStatus == 3)") # nothing passes lepton veto

    tdFullIsolation = treeDraw.clone(varexp="(muon2_f_chargedHadronIso + max(muon2_f_photonIso+muon2_f_neutralHadronIso-0.5*muon2_f_puChargedHadronIso, 0))/muon2_p4.Pt() >>tmp(50, 0, 0.5)")
    tdChargedIsolation = treeDraw.clone(varexp="(muon2_f_chargedHadronIso)/muon2_p4.Pt() >>tmp(50, 0, 0.5)")
    tdNeutralIsolation = treeDraw.clone(varexp="(max(muon2_f_photonIso+muon2_f_neutralHadronIso-0.5*muon2_f_puChargedHadronIso, 0))/muon2_p4.Pt() >>tmp(50, 0, 0.5)")

    h = dset.getDatasetRootHisto(tdFullIsolation).getHistogram()
    p = plots.PlotBase([histograms.Histo(h, "histo")])
    p.createFrame("muon2fullIsolation_"+datasetName+"_"+name+"_"+postfix)
    p.draw()
    p.save()

    h = dset.getDatasetRootHisto(tdChargedIsolation).getHistogram()
    integralAll = h.Integral(0, h.GetNbinsX()+1)
    integral = h.Integral(0, h.FindBin(0.1)+1)
    p = plots.PlotBase([histograms.Histo(h, "histo")])
    p.appendPlotObject(histograms.PlotText(0.5, 0.55, "%d events in total" % int(integralAll)))
    p.appendPlotObject(histograms.PlotText(0.5, 0.5, "%d events in <= 0.1" % int(integral)))
    p.createFrame("muon2chargedIsolation_"+datasetName+"_"+name+"_"+postfix)
    p.draw()
    p.save()

    h = dset.getDatasetRootHisto(tdNeutralIsolation).getHistogram()
    p = plots.PlotBase([histograms.Histo(h, "histo")])
    p.createFrame("muon2neutralIsolation_"+datasetName+"_"+name+"_"+postfix)
    p.draw()
    p.save()

def createTransverseMassPlot(*args, **kwargs):
    createTransverseMassPlotInternal(*args, normalizeToOne=False, **kwargs)
    createTransverseMassPlotInternal(*args, normalizeToOne=True, **kwargs)
    
def createTransverseMassPlotInternal(dset, name, postfix, normalizeToOne, nominalSelection, compareSelection, nominalLegend="Nominal", compareLegend="Compare", moveLegend={}):
    datasetName = dset.getName()
    treeDraw = dataset.TreeDraw("tree", varexp="TauMETTransverseMass >>tmp(10,0,200)")

    tdNominal = treeDraw.clone(selection=nominalSelection)#selection="Obj2Type == 3 && LeptonVetoStatus == 0 && (TauIDStatus == 1 || TauIDStatus == 2 || TauIDStatus == 3)") # FIXME
    tdCompare = treeDraw.clone(selection=compareSelection)

    drhNominal = dset.getDatasetRootHisto(tdNominal)
    drhCompare = dset.getDatasetRootHisto(tdCompare)

    integrate = lambda h: h.Integral(0, h.GetNbinsX()+1)
    nNominal = integrate(drhNominal.getHistogram())
    nCompare = integrate(drhCompare.getHistogram())

    if normalizeToOne:
        drhNominal.normalizeToOne()
        drhCompare.normalizeToOne()

    drhNominal.setName("Nominal")
    drhCompare.setName("Compare")

    p = plots.ComparisonPlot(drhNominal, drhCompare)

    p.histoMgr.forEachHisto(styles.generator())
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineWidth(3))
    p.histoMgr.setHistoLegendLabelMany({
            "Nominal": nominalLegend+ " (%d)" % int(nNominal),
            "Compare": compareLegend+ " (%d)" % int(nCompare)
            })

    pfix = postfix
    if normalizeToOne:
        pfix += "_unit"
    p.createFrame("mt_"+datasetName+"_"+name+"_"+pfix, createRatio=normalizeToOne, invertRatio=True, opts2={"ymin": 0, "ymax": 2})
    p.frame.GetXaxis().SetTitle("Transverse mass (GeV/c^{2})")
    if normalizeToOne:
        p.frame.GetYaxis().SetTitle("Arbitrary units")
    else:
        p.frame.GetYaxis().SetTitle("MC events")
    p.setLegend(histograms.moveLegend(histograms.createLegend(y1=0.93, y2=0.80, x1=0.45, x2=0.85), **moveLegend))

    nomErr = p.histoMgr.getHisto("Nominal").getRootHisto().Clone("Nominal_err")
    nomErr.SetFillColor(ROOT.kBlue-7)
    nomErr.SetFillStyle(3004)
    nomErr.SetMarkerSize(0)
    p.prependPlotObject(nomErr, "E2")

    comErr = p.histoMgr.getHisto("Compare").getRootHisto().Clone("Compare_err")
    comErr.SetFillColor(ROOT.kRed-7)
    comErr.SetFillStyle(3013)
    comErr.SetMarkerSize(0)
    p.prependPlotObject(comErr, "E2")

    if normalizeToOne:
        p.appendPlotObject(histograms.PlotText(0.6, 0.75, "Normalized to unit area", size=17))

    p.draw()
    p.save()

def createDrawPlot(name, h):
    h.SetMarkerSize(800)
    p = plots.PlotBase([histograms.Histo(h, "histo", drawStyle="TEXT")])
    p.createFrame(name, opts={"ymaxfactor": 1,
                              "nbinsx": h.GetNbinsX(),
                              "nbinsy": h.GetNbinsY(),
                              })
    for bin in xrange(1, h.GetNbinsX()+1):
        p.frame.GetXaxis().SetBinLabel(bin, h.GetXaxis().GetBinLabel(bin))
    for bin in xrange(1, h.GetNbinsY()+1):
        p.frame.GetYaxis().SetBinLabel(bin, h.GetYaxis().GetBinLabel(bin))
            
    p.draw()
    p.save()

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")
    parser.add_option("--mdir", dest="mdir", default=".",
                      help="Multicrab directory (default '.')")
    (opts, args) = parser.parse_args()

    main(opts)

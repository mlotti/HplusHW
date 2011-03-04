#!/usr/bin/env python

import os
from array import array

import ROOT
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

ROOT.gROOT.SetBatch(True)

style = tdrstyle.TDRStyle()
style.setPalettePretty()

histograms.textDefaults.setEnergyDefaults(x=0.17)
histograms.textDefaults.setCmsPreliminaryDefaults(x=0.6)

createLegend = histograms.createLegend
createLegend2 = createLegend.copy()
createLegend2.setDefaults(x1=0.6, y1=0.8, y2=0.94)

def getHisto(datasets, path, name, func=None):
    h = histograms.HistoManager(datasets, path)
    h = h.getHistos()[0]
    h.setName(name)
    h.setLegendLabel(name)
    if func != None:
        func(h)
    return h

class PlotBase(plots.PlotSameBase):
    def __init__(self):
        self.histoMgr = histograms.HistoManagerImpl([])
        self.saveFormats = [".png",
#                            ".eps", ".C"
                            ]

    def binWidth(self):
        return self.histoMgr.getHistos()[0].getBinWidth(1)

class Plot(PlotBase):
    def __init__(self, datasets, directory, names):
        PlotBase.__init__(self)

        self.prefix = directory.replace("/", "_")+"_"

        for name in names:
            self.histoMgr.append(getHisto(datasets, directory+"/"+name, name))

        self.histoMgr.forEachHisto(styles.generator())

    def createFrame(self, plotname, **kwargs):
        plots.PlotSameBase.createFrame(self, self.prefix+plotname, **kwargs)

class Plot2(PlotBase):
    def __init__(self, datasets, datasetsTau, directories, name):
        PlotBase.__init__(self)

        self.histoMgr.append(getHisto(datasets, directories[0]+"/"+name, name+"Embedded"))
        self.histoMgr.append(getHisto(datasetsTau, directories[1]+"/"+name, name+"Tau"))

        self.histoMgr.forEachHisto(styles.generator())

        self.histoMgr.setHistoLegendLabelMany({name+"Embedded": "Embedded #tau",
                                               name+"Tau": "Real #tau"})

class PlotMuonTau:
    def __init__(self, rebin={}):
        self.rebin = {"Pt": 2,
                      "Eta": 10,
                      "Phi": 10
                      }
        self.rebin.update(rebin)

    def plot(self, datasets, an, q):
        rebin = self.rebin[q]
        xlabel = {"Pt": "p_{T} (GeV/c)",
                  "Eta": "#eta",
                  "Phi": "#phi (rad)"}[q]
    
        name = "Muon_Tau_"+q
        h = Plot(datasets, an, ["Tau_"+q, "GenTauVis_"+q, "Muon_"+q])
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

        ylabel = "Number of MC events / %.1f" % h.binWidth() 
        if q == "Pt":
            ylabel += " GeV/c"
        elif q == "Phi":
            ylabel += " rad"

        h.histoMgr.setHistoLegendLabelMany({"Muon_"+q: "Original muon",
                                            "Tau_"+q: "Embedded tau",
                                            "GenTauVis_"+q: "Embedded visible tau",
                                            })
        h.createFrame(name, yfactor=1.2)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(createLegend2())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.save()
    
        if q == "Pt":
            h.createFrame(name+"_log", ymin=0.1, yfactor=2)
            h.frame.GetXaxis().SetTitle(xlabel)
            h.frame.GetYaxis().SetTitle(ylabel)
            h.setLegend(createLegend2())
            ROOT.gPad.SetLogy(True)
            h.draw()
            histograms.addCmsPreliminaryText()
            histograms.addEnergyText()
            h.save()
    
        xmin, ymin = 0, 0
        xmax, ymax = 200, 200
        label = "p_{T}^{%s} (GeV/c)"
        if q == "Eta":
            xmin, ymin = -2.5, -2.5
            xmax, ymax = 2.5, 2.5
            label = "#eta_{%s}"
        elif q == "Phi":
            xmin, ymin = -3.5, -3.5
            xmax, ymax = 3.5, 3.5
            label = "#phi_{%s}"
    
        style.setWide(True)
        h = Plot(datasets, an, ["Muon_Tau_"+q])
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin2D(rebin, rebin))
        h.createFrame(name+"_2D", xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
        h.frame.GetXaxis().SetTitle(label%"#mu")
        h.frame.GetYaxis().SetTitle(label%"#tau")
        h.histoMgr.setHistoDrawStyleAll("COLZ")
        h.draw()
        histograms.updatePaletteStyle(h.histoMgr.getHistos()[0].getRootHisto())
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.save()
        style.setWide(False)

class PlotGenTauNu:
    def __init__(self, rebin={}):
        self.rebin = {"Pt": 2,
                      "Eta": 10,
                      "Phi": 10,
                      "DR": 10
                      }
        self.rebin.update(rebin)

    def plot(self, datasets, an, q):
        rebin = self.rebin[q]
        xlabel = "p_{T} (GeV/c)"
        xlabelDiff = "p_{T}^{#tau} - p_{T}^{#nu} (GeV/c)"
    
        if q == "Eta":
            xlabel = "#eta"
            xlabelDiff = "#eta^{#tau} - #eta^{#nu} (GeV/c)"
        elif q == "Phi":
            xlabel = "#phi"
            xlabelDiff = "#phi^{#tau} - #phi^{#nu} (GeV/c)"
    
        h = Plot(datasets, an, ["GenTau_"+q, "GenTauNu_"+q])
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

        ylabel = "Number of MC events / %.2f" % h.binWidth()
        if q == "Pt":
            ylabel += " GeV/c"
        elif q == "Phi":
            ylabel += " rad"

        h.histoMgr.setHistoLegendLabelMany({"GenTau_"+q: "Gen #tau", "GenTauNu_"+q: "Gen #nu_{#tau}"})
        h.createFrame("GenTau_GenTauNu_"+q, yfactor=1.2)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(createLegend2())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.save()

        name = "GenTau,GenTauNu_D"+q
        h = Plot(datasets, an, [name])
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
        h.createFrame(name)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.save()
    
        xmin, ymin = 0, 0
        xmax, ymax = 200, 200
        label = "p_{T}^{%s} (GeV/c)"
        if q == "Eta":
            xmin, ymin = -2.5, -2.5
            xmax, ymax = 2.5, 2.5
            label = "#eta_{%s}"
        elif q == "Phi":
            xmin, ymin = -3.5, -3.5
            xmax, ymax = 3.5, 3.5
            label = "#phi_{%s}"
    
        style.setWide(True)
        h = Plot(datasets, an, ["GenTau_GenTauNu_"+q])
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin2D(rebin, rebin))
        h.createFrame("GenTau_GenTauNu_"+q+"2D", xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
        h.frame.GetXaxis().SetTitle(label%"#tau")
        h.frame.GetYaxis().SetTitle(label%"#nu")
        h.histoMgr.setHistoDrawStyleAll("COLZ")
        h.draw()
        histograms.updatePaletteStyle(h.histoMgr.getHistos()[0].getRootHisto())
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.save()
        style.setWide(False)

    def plotDR(self, datasets, an):
        rebin = self.rebin["DR"]
        ylabel = self.ylabels["DR"](rebin)
        xlabel = "#DeltaR(#tau, #nu)"

        name = "GenTau,GenTauNu_DR"
        h = Histo(datasets, an, [name])
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
        h.createFrame(name)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.draw()
        addCmsPreliminaryText()
        addEnergyText()
        h.save()
        

def tauGenMass(datasets, an):
    h = Plot(datasets, an, ["GenTau_Mass", "GenTauDecay_Mass"])
    h.histoMgr.setHistoLegendLabelMany({"GenTau_Mass": "#tau",
                                   "GenTauDecay_Mass": "#tau decays"})
    h.createFrame("GenTau_Mass")
    h.frame.GetXaxis().SetTitle("M (GeV/c^{2})")
    h.frame.GetYaxis().SetTitle("Number of MC events / 0.02")
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.save()

def muonTauIso(datasets, an):
    style.setWide(True)
    name = "Muon_IsoTrk_Tau_IsoChargedHadrPtSum"
    h = Plot(datasets, an, [name])
    h.createFrame(name, xmax=25, ymax=80)
    h.frame.GetXaxis().SetTitle("#mu tracker isolation #Sigma p_{T} (GeV/c)")
    h.frame.GetYaxis().SetTitle("#tau isolation charged cand #Sigma p_{T} (GeV/c)")
    h.histoMgr.setHistoDrawStyleAll("COLZ")
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.save()
    style.setWide(False)

    #style.setWide(True)
    #h = Plot(datasets, an, ["muonIsoTrkTauPtSumRel"])
    #h.createFrame(an_name+"_muonIsoTrkTauPtSumRel")
    #h.frame.GetXaxis().SetTitle("#mu trk isol. #Sigma p_{T}/p^{#mu}_{T}")
    #h.frame.GetYaxis().SetTitle("#tau isol. chrg cand #Sigma p_{T}/p^{#tau}_{T}")
    #h.histoMgr.setHistoDrawStyleAll("COLZ")
    #h.draw()
    #h.save()
    #style.setWide(False)

    style.setWide(True)
    name = "Muon_IsoTotal_Tau_IsoChargedHadrPtSumRel"
    h = Plot(datasets, an, [name])
    h.createFrame(name, xmax=0.5, ymax=10)
    h.frame.GetXaxis().SetTitle("#mu rel. iso")
    h.frame.GetYaxis().SetTitle("#tau isol. chrg cand #Sigma p_{T}/p^{#tau}_{T}")
    h.histoMgr.setHistoDrawStyleAll("COLZ")
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.save()
    style.setWide(False)


def muonTauDR(datasets, an):
    rebin = 1

    name = "Muon,Tau_DR"
    h = Plot(datasets, an, [name])
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

    ylabel = "Number of MC events / %.2f" % h.binWidth()

    h.createFrame(name, ymin=0.1, yfactor=2, xmax=1)
    h.frame.GetXaxis().SetTitle("#DeltaR(#mu, #tau)")
    h.frame.GetYaxis().SetTitle(ylabel)
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.save()

    name = "Muon,TauLdg_DR"
    h = Plot(datasets, an, [name])
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    h.createFrame(name, ymin=0.1, yfactor=2, xmax=1)
    h.frame.GetXaxis().SetTitle("#DeltaR(#mu, #tau ldg cand)")
    h.frame.GetYaxis().SetTitle(ylabel)
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.save()

class PlotMet:
    def __init__(self, rebin={}):
        self.rebin = {"Et": 2,
                      "X": 2,
                      "Y": 2,
                      "Phi": 2
                      }
        self.rebin.update(rebin)
        self.ylabel = "Number of MC events / %.1f"
        self.xlabels = {
            "Et": "MET (GeV)",
            "X": "MET_{x} (GeV)",
            "Y": "MET_{y} (GeV)",
            "Phi": "#phi_{MET} (rad)"
            }

    def plot(self, datasets, an, t="Met", q="Et"):
        rebin = self.rebin[q]
        xlabel = self.xlabels[q]
    
        h = Plot(datasets, an, [t+"_"+q, t+"Original_"+q])
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

        ylabel = self.ylabel % h.binWidth()
        if q != "Phi":
            ylabel += "GeV"

        h.histoMgr.setHistoLegendLabelMany({t+"_"+q: "Embedded", t+"Original_"+q: "Original"})
        h.createFrame(t+"_"+q)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(createLegend2())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.save()
    
        if t == "Met" and q == "Et":
            name = t+"Original_"+q+"_AfterCut"
            h = Plot(datasets, an, [name])
            h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
            h.createFrame(name)
            h.frame.GetXaxis().SetTitle("Original "+xlabel)
            h.frame.GetYaxis().SetTitle(ylabel)
            h.draw()
            histograms.addCmsPreliminaryText()
            histograms.addEnergyText()
            h.save()
        
        xmin, ymin = [0]*2
        xmax, ymax = [200]*2
        #ymin = 60
    
        if q in ["X", "Y"]:
            ymin = -ymax/2
            ymax = ymax/2
            xmin = -xmax/2
            xmax = xmax/2
        elif q == "Phi":
            xmin, ymin = [-3.5]*2
            xmax, ymax = [3.5]*2
    
        low = max(xmin, ymin)
        high = min(xmax, ymax)
        line = ROOT.TGraph(2, array("d", [low, high]), array("d", [low, high]))
        line.SetLineStyle(2)
        line.SetLineWidth(2)
    
        if q == "Phi":
            rebin = rebin*5

        style.setWide(True)
        name = t+"Original_"+t+"_"+q
        h = Plot(datasets, an, [name])
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin2D(rebin, rebin))
        #h.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetAxisRange(ymin, ymax, "Y"))
        h.createFrame(name, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
        h.frame.GetXaxis().SetTitle("Original "+xlabel)
        h.frame.GetYaxis().SetTitle("Embedded "+xlabel)
        h.histoMgr.setHistoDrawStyleAll("COLZ")
        h.draw()
        line.Draw("L")
        histograms.updatePaletteStyle(h.histoMgr.getHistos()[0].getRootHisto())
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.save()

        h.createFrame(name+"_log", xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
        h.frame.GetXaxis().SetTitle("Original "+xlabel)
        h.frame.GetYaxis().SetTitle("Embedded "+xlabel)
        h.histoMgr.setHistoDrawStyleAll("COLZ")
        ROOT.gPad.SetLogz(True)
        h.draw()
        line.Draw("L")
        histograms.updatePaletteStyle(h.histoMgr.getHistos()[0].getRootHisto())
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.save()

        style.setWide(False)

    def plotOne(self, datasets, an, t="Met", q="Et"):
        rebin = self.rebin[q]
        xlabel = self.xlabels[q]
        ylabel = self.ylabels[q](rebin)

        name = t+"_"+q
        h = Histo(datasets, an, [name])
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
        h.createFrame(name)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.draw()
        addCmsPreliminaryText()
        addEnergyText()
        h.save()


class PlotMuonTauMetDeltaPhi:
    def __init__(self, rebin=10, rebinMet=5):
        self.rebin = rebin
        self.rebinMet = rebinMet

        self.ylabel = "Number of MC events / %.2f"
        self.ylabelMet = "Number of MC events / %.1f GeV"

    def plot(self, datasets, an, t="Met"):
        h = Plot(datasets, an, [
                #"Muon,"+t+"_DPhi",
                "Tau,"+t+"_DPhi",
                "Muon,"+t+"Original_DPhi",
                #"Tau,"+t+"Original_DPhi"
                ])

        ylabel = self.ylabel % h.binWidth()

        h.histoMgr.setHistoLegendLabelMany({
                #"Muon,"+t+"_DPhi": "#Delta#phi(#mu, MET_{#tau})",
                "Muon,"+t+"Original_DPhi": "#Delta#phi(#mu, MET_{#mu})",
                "Tau,"+t+"_DPhi": "#Delta#phi(#tau, MET_{#tau})",
                #"Tau,"+t+"Original_DPhi": "#Delta#phi(#tau, MET_{#mu})"
                })
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(self.rebin))
        h.createFrame("MuonTau,"+t+"_DPhi")
        h.frame.GetXaxis().SetTitle("#Delta#phi")
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(createLegend2(y1=0.75))
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.save()
    
        style.setWide(True)
        h = Plot(datasets, an, ["Muon,"+t+"Original_Tau,"+t+"_DPhi"])
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin2D(self.rebin, self.rebin))
        h.createFrame("MuonTau,"+t+"DPhi2D", xmin=-3.5, ymin=-3.5, xmax=3.5, ymax=3.5)
        h.frame.GetXaxis().SetTitle("#Delta#phi(#mu, MET_{#mu})")
        h.frame.GetYaxis().SetTitle("#Delta#phi(#tau, MET_{#tau})")
        h.histoMgr.setHistoDrawStyleAll("COLZ")
        h.draw()
        histograms.updatePaletteStyle(h.histoMgr.getHistos()[0].getRootHisto())
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.save()
        style.setWide(False)

        name = t+","+t+"Original_DPhi"
        h = Plot(datasets, an, [name])
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(self.rebin))
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetStats(True))
        h.createFrame(name)
        h.frame.GetXaxis().SetTitle("#Delta#phi(MET_{#tau},MET_{#mu}) (rad)")
        h.frame.GetYaxis().SetTitle(self.ylabel)
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.save()
    
        #style.setOptStat(1)
        name = t+","+t+"Original_DEt"
        h = Plot(datasets, an, [name])
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(self.rebinMet))
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetStats(True))
        h.createFrame(name, xmin=-100, xmax=200)
        h.frame.GetXaxis().SetTitle("MET_{#tau}-MET_{#mu} (GeV)")
        h.frame.GetYaxis().SetTitle(self.ylabelMet)
        h.draw()
        #ROOT.gPad.Update()
        #box = h.histoMgr.getHistos()[0].FindObject("stats")
        #box.SetOptStat("em")
        #box.SetX1NDC(0.8)
        #box.SetX2NDC(0.92)
        #box.SetY1NDC(0.8)
        #box.SetY2NDC(0.92)
        #box.Draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.save()
        #style.setOptStat(0)
   
        style.setWide(True)
        name = "Muon,"+t+"Original_DPhi_"+name
        h = Plot(datasets, an, [name])
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin2D(self.rebin, self.rebinMet))
        h.createFrame(name, xmin=-3.5, ymin=-100, xmax=3.5, ymax=200)
        h.frame.GetXaxis().SetTitle("#Delta#phi(#mu, MET_{#mu})")
        h.frame.GetYaxis().SetTitle("MET_{#tau}-MET_{#mu}")
        h.histoMgr.setHistoDrawStyleAll("COLZ")
        h.draw()
        histograms.updatePaletteStyle(h.histoMgr.getHistos()[0].getRootHisto())
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.save()
        style.setWide(False)
    
        numEventsAll = h.histoMgr.getHistos()[0].getRootHisto().GetEntries()
    
        h = Plot(datasets, an, [
                "GenWTauNu,"+t+"_DPhi",
                "GenWNu,"+t+"Original_DPhi",
                ])
        h.histoMgr.setHistoLegendLabelMany({
                "GenWTauNu,"+t+"_DPhi": "#Delta#phi(#nu_{#mu}+#nu_{#tau}, MET_{#tau})",
                "GenWNu,"+t+"Original_DPhi": "#Delta#phi(#nu_{#mu}, MET_{#nu})"
                })
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(self.rebin))
        h.createFrame("GenWNu_GenWTauNu_"+t+"_DPhi")
        h.frame.GetXaxis().SetTitle("#Delta#phi")
        h.frame.GetYaxis().SetTitle(self.ylabel)
        h.setLegend(createLegend2())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.save()
    
        numEventsGenMu = h.histoMgr.getHistos()[0].getRootHisto().GetEntries()
        print "%s: N(W->munu) / N(all) = %d/%d = %.1f %%" % (an, numEventsGenMu, numEventsAll, numEventsGenMu/numEventsAll*100)
        
        style.setWide(True)
        h = Plot(datasets, an, ["GenWNu,"+t+"Original_GenWTauNu,"+t+"_DPhi"])
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin2D(self.rebin, self.rebin))
        h.createFrame("GenWNu_GenWTauNu_"+t+"_DPhi2D", xmin=-3.5, ymin=-3.5, xmax=3.5, ymax=3.5)
        h.frame.GetXaxis().SetTitle("#Delta#phi(#nu_{#mu}, MET_{#mu})")
        h.frame.GetYaxis().SetTitle("#Delta#phi(#nu_{#mu}+#nu_{#tau}, MET_{#tau})")
        h.histoMgr.setHistoDrawStyleAll("COLZ")
        h.draw()
        histograms.updatePaletteStyle(h.histoMgr.getHistos()[0].getRootHisto())
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.save()
        style.setWide(False)
    

def embeddingPlots():
    datasets = None
    if os.path.exists("histograms.root"):
        datasets = dataset.getDatasetsFromRootFiles([("Test", "histograms.root")], counters=None)
    else:
        datasets = dataset.getDatasetsFromMulticrabCfg(counters="countAnalyzer")

    muonTau = PlotMuonTau()
    genTauNu = PlotGenTauNu()
    met = PlotMet()
    muonTauMetDeltaPhi = PlotMuonTauMetDeltaPhi()

    for analysis in [
        "EmbeddingAnalyzer",
    #    "tauIdEmbeddingAnalyzer",
    #    "tauPtIdEmbeddingAnalyzer"
    #    "EmbeddingAnalyzer/matched",
    #    "tauIdEmbeddingAnalyzer/matched",
    #    "tauPtIdEmbeddingAnalyzer/matched"
        ]:
        for q in ["Pt", "Eta", "Phi"]:
            muonTau.plot(datasets, analysis, q)
#            genTauNu.plot(datasets, analysis, q)
#        muonTauDR(datasets, analysis)
#        muonTauIso(datasets, analysis)
#        tauGenMass(datasets, analysis)
    
#        muonTauMetDeltaPhi.plot(datasets, analysis, "Met")
        for t in [
            "Met",
    #        "MetNoMuon",
    #        "GenMetTrue",
    #        "GenMetCalo",
    #        "GenMetCaloAndNonPrompt",
    #        "GenMetNuSum",
    #        "GenMetNu"
            ]:
            muonTauMetDeltaPhi.plot(datasets, analysis, t)
            for q in [
                "Et",
                "X",
                "Y",
                "Phi"
                ]:
                met.plot(datasets, analysis, t=t, q=q)

def tauPlots():
    datasets = None
    if os.path.exists("histograms.root"):
        datasets = getDatasetsFromRootFiles([("Test", "histograms.root")], counters=None)
    else:
        datasets = getDatasetsFromMulticrabCfg(counters="countAnalyzer")
    
    genTauNu = PlotGenTauNu()
    tauMetDeltaPhi = PlotMuonTauMetDeltaPhi()
    met = PlotMet()

    for analysis in [
        "TauAnalyzer",
        "GenPt40TauAnalyzer",
        "GenPt40Eta21TauAnalyzer"
        ]:
        for q in ["Pt", "Eta", "Phi"]:
            genTauNu.plot(datasets, analysis, q)
        genTauNu.plotDR(datasets, analysis)
        tauMetDeltaPhi.plot(datasets, analysis, "GenMetNu")

        met.plot(datasets, analysis, "GenMetNu", "Et")
        met.plot(datasets, analysis, "GenMetNu", "Phi")

        for t in [
            "Met",
            "GenMetNuSum",
            "GenMetNu"
            ]:
            for q in [
                "Et",
#                "X",
#                "Y",
                "Phi"
                ]:
                met.plotOne(datasets, analysis, t=t, q=q)


def embeddingVsTauPlots():
    datasetsTau = getDatasetsFromCrabDirs(["WJets"], counters=None)
    datasetsTau = getDatasetsFromRootFiles[("WJets", "histograms.root")], counters=None


embeddingPlots()
#tauPlots()
#embeddingVsTauPlots()

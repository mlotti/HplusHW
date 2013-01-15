#!/usr/bin/env python

import sys
import os
import ROOT

from datetime import date, time, datetime

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter

analysis = "signalAnalysis"
era = "Run2011A"
#counters = analysis+"Counters"

debugstatus = False


def getDatasetNames(multiCrabDir,counters,era,legacy=False):
    datasets = None
    if not legacy:
        datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=multiCrabDir+"/multicrab.cfg",dataEra=era,counters=counters)
        datasets.updateNAllEventsToPUWeighted()
    else:
        datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=multiCrabDir+"/multicrab.cfg",counters=counters)
        #datasets.updateNAllEventsToPUWeighted()
    #datasets.loadLuminosities(fname="dummy")
    #datasets.printInfo()
    return datasets.getAllDatasetNames()

def validateDatasetExistence(dataset1names,dataset2names):
    print
    print "Validating dataset names.."
    return validateNames(dataset1names,dataset2names)

def validateNames(names1,names2):
    names = []
    for name1 in names1:
        match = False
        for name2 in names2:
            if name2 == name1:
                match = True
        if match:
            names.append(name1)
        else:
            print "    ",name1,"found in the reference datasets, but not in the validated datasets"
    print
    for name2 in names2:
        match = False
        for name1 in names1:
            if name2 == name1:
                match = True
        if not match:
            print "    ",name2,"found in the validated datasets, but not in the reference datasets"
    print

    return names

def findValue(row,counter):
    if counter == None:
        return -1
    for i in xrange(counter.getNrows()):
        if row == counter.rowNames[i]:
            return int(counter.getCount(i,0).value())
    #print "Counter value not found"
    return -1

def format(row,value1,value2):
    fString = "    "
    fString += row
    while len(fString) < 40:
        fString += " "
    fString += str(value1)
    while len(fString) < 50:
        fString += " "
    fString += str(value2)
    while len(fString) < 60:
        fString += " "
    return fString

def getagreementwithcolor(ratio):
    myoutput = ""
    if abs(ratio-1) < 0.0001:
        myoutput += "<td></td>"
    elif abs(ratio-1) < 0.01:
        myoutput += "<td align=center>%1.5f</td>" % ratio
    elif abs(ratio-1) < 0.03:
        myoutput += "<td align=center bgcolor=#d0d000>%1.5f</td>" % ratio
    else:
        myoutput += "<td align=center bgcolor=#d00000>%1.5f</td>" % ratio
    return myoutput

def report(oldrow,row,counter1,counter2):
    # obtain event counts
    value1 = findValue(row,counter1)
    value2 = findValue(row,counter2)
    myoutput = "<tr>\n"
    myoutput += "<td><b>"+row+"</b></td>"
    if value2 >= 0:
        myoutput += "<td align=center>"+str(value2)+"</td>"
    else:
        myoutput += "<td align=center>-</td>"
    if value1 >= 0:
        myoutput += "<td align=center>"+str(value1)+"</td>"
    else:
        myoutput += "<td align=center>-</td>"
    if value1 == value2 and value1 > 0:
        myoutput += "<td></td>"
        print format(row,value2,value1)
    else:
        myratio = -1;
        if value1 > 0:
            myratio = float(value2) / float(value1)
        myoutput += getagreementwithcolor(myratio)
        print format(row,value2,value1),"ratio=",myratio
    # obtain efficiencies
    oldvalue1 = 0
    oldvalue2 = 0
    eff1 = 0
    eff2 = 0
    if not oldrow == "":
        oldvalue1 = findValue(oldrow,counter1)
        oldvalue2 = findValue(oldrow,counter2)
    if oldvalue1 > 0:
        eff1 = float(value1) / float(oldvalue1)
    if oldvalue2 > 0:
        eff2 = float(value2) / float(oldvalue2)
    myratio = 1.0;
    if eff1 > 0:
         myratio = eff2 / eff1
    myoutput += "<td align=center>%1.5f</td>" % eff2
    myoutput += "<td align=center>%1.5f</td>" % eff1
    myoutput += getagreementwithcolor(myratio)

    myoutput += "</tr>\n"
    return myoutput

def validateCounterValues(counter1,counter2):
    # Make table in output
    myoutput = "<table>\n"
    myoutput += "<tr><td><b>Counter</b></td>"
    myoutput += "<td><b>New counts</b></td><td><b>Ref. counts</b></td><td><b>New/Ref.</b></td>"
    myoutput += "<td><b>New eff.</b></td><td><b>Ref. eff.</b></td><td><b>New/Ref.</b></td>"
    myoutput += "</tr>\n"
    oldrow = ""
    if counter1 == None:
        rownames = counter2.getRowNames()
    else:
        rownames = counter1.getRowNames()
    for row in rownames:
        myoutput += report(oldrow, row,counter1,counter2)
        oldrow = row
    myoutput += "</table>\n"
    return myoutput

def validateCounters(dataset1,dataset2):
    print "Reporting main counters:"
    eventCounter1 = counter.EventCounter(dataset1)
    counter1 = eventCounter1.getMainCounter().getTable()
    #rownames1 = counter1.getRowNames()

    eventCounter2 = counter.EventCounter(dataset2)
    counter2 = eventCounter2.getMainCounter().getTable()
    #rownames2 = counter2.getRowNames()
    # table of main counters
    #rownames = validateNames(rownames1,rownames2)
    myoutput = validateCounterValues(counter1,counter2)
    # table of subcounters
    subcounternames1 = eventCounter1.getSubCounterNames()
    subcounternames2 = eventCounter2.getSubCounterNames()
    for item in subcounternames1:
        print "Reporting subcounter:",item
        myoutput += "<br>\n<b>Subcounter: "+item+"</b><br>\n<br>\n"
        counter1 = eventCounter1.getSubCounterTable(item)
        if item in subcounternames2:
            counter2 = eventCounter2.getSubCounterTable(item)
            myoutput += validateCounterValues(counter1,counter2)
        else:
            myoutput += validateCounterValues(counter1,None)
    for item in subcounternames2:
        print "Reporting subcounter:",item
        if not item in subcounternames1:
            myoutput += "Subcounter: "+item+"<br>\n"
            counter2 = eventCounter2.getSubCounterTable(item)
            myoutput += validateCounterValues(None,counter2)
    return myoutput

def getHistogram(dataset, histoname, name, isRef):
    roothisto = dataset.getDatasetRootHisto(name)
    #roothisto.normalizeToOne()
    hnew = roothisto.getHistogram()
    # Rebin
    binwidth = hnew.GetXaxis().GetBinWidth(1)
    if histoname[1] > binwidth:
        hnew.Rebin(int(histoname[1] / binwidth))
    myName = "New"
    if isRef:
        myName = "Reference"
    binwidth = hnew.GetXaxis().GetBinWidth(1)
    h = ROOT.TH1F("h_"+myName,"h_"+myName, hnew.GetNbinsX()+2, hnew.GetXaxis().GetXmin() - binwidth, hnew.GetXaxis().GetXmax() + binwidth)
    # Copy bin contents
    for i in range (1, hnew.GetNbinsX()+1):
        h.SetBinContent(i+1, hnew.GetBinContent(i))
        h.SetBinError(i+1, hnew.GetBinError(i))
        if hnew.GetXaxis().GetBinLabel(i) <> "":
            h.GetXaxis().SetBinLabel(i+1, hnew.GetXaxis().GetBinLabel(i))
    # Set under/overflow bins
    h.SetBinContent(1, hnew.GetBinContent(0))
    h.SetBinError(1, hnew.GetBinError(0))
    h.SetBinContent(h.GetNbinsX(), hnew.GetBinContent(hnew.GetNbinsX()+1))
    h.SetBinError(h.GetNbinsX(), hnew.GetBinError(hnew.GetNbinsX()+1))
    # Set attributes
    h.SetEntries(hnew.GetEntries())
    h.SetTitle(hnew.GetTitle())
    h.SetXTitle(hnew.GetXaxis().GetTitle())
    h.SetYTitle(hnew.GetYaxis().GetTitle())
    h.SetStats(1)
    h.SetName(myName)
    if isRef:
        h.SetFillStyle(1001)
        h.SetFillColor(ROOT.kBlue-6)
        h.SetLineColor(ROOT.kBlue-6)
        #statbox.SetTextColor(ROOT.kBlue-6)
    else:
        h.SetMarkerColor(ROOT.kBlack)
        h.SetLineColor(ROOT.kBlack)
        h.SetMarkerStyle(20)
        h.SetMarkerSize(1.0)
        #statbox.SetTextColor(ROOT.kBlack)
    return h

def setframeextrema(myframe, h1, h2, logstatus):
    # obtain and set x range
    xmin = h1.GetXaxis().GetXmin()
    if h2.GetXaxis().GetXmin() > h1.GetXaxis().GetXmin():
        xmin = h2.GetXaxis().GetXmin()
    xmax = h1.GetXaxis().GetXmax()
    if h2.GetXaxis().GetXmax() > h1.GetXaxis().GetXmax():
        xmax = h2.GetXaxis().GetXmax()
    myframe.GetXaxis().Set(1, xmin, xmax)
    # obtain and set minimum y value
    ymin = 0.0
    if logstatus == "log":
        ymin = 1.5
        for i in range(1, h1.GetNbinsX()):
            if h1.GetBinContent(i) > 0 and h1.GetBinContent(i) < ymin:
                ymin = h1.GetBinContent(i)
        for i in range(1, h2.GetNbinsX()):
            if h2.GetBinContent(i) > 0 and h2.GetBinContent(i) < ymin:
                ymin = h2.GetBinContent(i)
        if ymin > 1:
            ymin = 1.5
    myscalefactor = 1.1
    if logstatus == "log":
        myscalefactor = 1.5
        myframe.SetMinimum(ymin / myscalefactor)
    else:
        myframe.SetMinimum(ymin)
    # obtain and set maximum y value
    ymax = h1.GetMaximum()
    if h2.GetMaximum() > h1.GetMaximum():
        ymax = h2.GetMaximum()
    myframe.SetMaximum(ymax*myscalefactor)

def analysehistodiff(canvas,h1,h2):
    canvas.GetPad(1).SetFrameFillColor(4000)
    canvas.GetPad(2).SetFrameFillColor(4000)
    diff = 0.0
    if not h1.GetNbinsX() == h2.GetNbinsX():
        canvas.GetPad(1).SetFillColor(ROOT.kOrange)
        canvas.GetPad(2).SetFillColor(ROOT.kOrange)
    else:
        # same number of bins in histograms
        zerocount = 0
        for i in range(1, h1.GetNbinsX()):
            if h1.GetBinContent(i) > 0:
                diff += abs(h2.GetBinContent(i) / h1.GetBinContent(i) - 1.0)
            elif h2.GetBinContent(i) > 0:
                zerocount = zerocount + 1
        if (diff > 0.03 or zerocount > 3):
            canvas.GetPad(1).SetFillColor(ROOT.kRed+1)
            canvas.GetPad(2).SetFillColor(ROOT.kRed+1)
        elif (diff > 0.01 or zerocount > 1):
            canvas.GetPad(1).SetFillColor(ROOT.kOrange)
            canvas.GetPad(2).SetFillColor(ROOT.kOrange)
    return diff

def setCanvasDefinitions(canvas):
    canvas.Range(0,0,1,1)
    canvas.SetFrameFillColor(ROOT.TColor.GetColor("#fdffff"))
    canvas.SetFrameFillStyle(1001)
    canvas.Divide(2,1)
    canvas.GetPad(1).SetPad(0,0.3,1.,1.)
    canvas.GetPad(2).SetPad(0,0.0,1.,0.3)
    # agreement pad
    pad = canvas.GetPad(2)
    #pad.SetFillStyle(4000);
    pad.SetBorderMode(0);
    pad.SetBorderSize(2);
    pad.SetTickx(1);
    pad.SetTicky(1);
    pad.SetLeftMargin(0.10);
    pad.SetRightMargin(0.05);
    pad.SetTopMargin(0);
    pad.SetBottomMargin(0.34);
    # plot pad
    myplotpad = canvas.GetPad(1)
    myplotpad = canvas.GetPad(1)
    myplotpad.SetTickx(1)
    myplotpad.SetTicky(1)
    myplotpad.SetLeftMargin(0.10)
    myplotpad.SetRightMargin(0.05)
    myplotpad.SetTopMargin(0.065)
    myplotpad.SetBottomMargin(0.0)

def validateHistograms(mydir,histoDir,dataset1,dataset2):
    mysubdir = mydir+"/"+dataset1.getName()
    if not os.path.exists(mysubdir):
        os.mkdir(mysubdir)
    mydir = dataset1.getName()

    myoutput = "<br><a href=#maintop>Back to datasets</a>\n"
    myoutput += "<h3><a name=histotop_"+dataset1.getName()+">Histograms for validation:</a></h3><br>\n"
    myoutput += "Note: the underflow (overflow) bin is shown as the first (last) bin in the histogram<br>\n"
    myoutput += "Color legend: blue histogram = reference, red points = dataset to be validated<br>\n"
    myoutput += "Difference is defined as sum_i (abs(new_i / ref_i - 1.0)), where sum goes over the histogram bins<br><br>\n"
    print "Generating validation histograms"
    # entry syntax: histogram_name_with_path, bin_width, linear/log
    histolist = [
        ["Primary vertices", [
            [histoDir+"/Vertices/verticesBeforeWeight", 1, "log"],
            [histoDir+"/Vertices/verticesAfterWeight", 1, "log"],
            [histoDir+"/Vertices/verticesTriggeredBeforeWeight", 1, "log"],
            [histoDir+"/Vertices/verticesTriggeredAfterWeight", 1, "log"],
        ]],
        ["Trigger matched tau collection", [
            [["signalAnalysis/tauID/N_TriggerMatchedTaus","signalAnalysis/TauSelection/N_TriggerMatchedTaus"], 1, "log"],
            [["signalAnalysis/tauID/N_TriggerMatchedSeparateTaus","signalAnalysis/TauSelection/N_TriggerMatchedSeparateTaus"], 1, "log"],
            [["signalAnalysis/tauID/HPSDecayMode","signalAnalysis/TauSelection/HPSDecayMode"], 1, "log"],
            [["signalAnalysis/tauID/TauSelection_all_tau_candidates_N","signalAnalysis/TauSelection/TauSelection_all_tau_candidates_N"], 1, "log"],
            [["signalAnalysis/tauID/TauSelection_all_tau_candidates_pt","signalAnalysis/TauSelection/TauSelection_all_tau_candidates_pt"], 5, "log"],
            [["signalAnalysis/tauID/TauSelection_all_tau_candidates_eta","signalAnalysis/TauSelection/TauSelection_all_tau_candidates_eta"], 0.1, "log"],
            [["signalAnalysis/tauID/TauSelection_all_tau_candidates_phi","signalAnalysis/TauSelection/TauSelection_all_tau_candidates_phi"], 3.14159265 / 36, "log"],
            [["signalAnalysis/tauID/TauSelection_all_tau_candidates_MC_purity","signalAnalysis/TauSelection/TauSelection_all_tau_candidates_MC_purity"], 1, "log"]
        ]],
        ["Tau candidate selection", [
            [["signalAnalysis/tauID/TauCand_JetPt","signalAnalysis/TauSelection/TauCand_JetPt"], 5, "log"],
            [["signalAnalysis/tauID/TauCand_JetEta","signalAnalysis/TauSelection/TauCand_JetEta"], 0.1, "log"],
            [["signalAnalysis/tauID/TauCand_LdgTrackPtCut","signalAnalysis/TauSelection/TauCand_LdgTrackPtCut"], 5, "log"],
            [["signalAnalysis/tauID/TauCand_EMFractionCut","signalAnalysis/TauSelection/TauCand_EMFractionCut"], 0.05, "log"],
            [["signalAnalysis/tauID/TauSelection_cleaned_tau_candidates_N","signalAnalysis/TauSelection/TauSelection_cleaned_tau_candidates_N"], 1, "log"],
            [["signalAnalysis/tauID/TauSelection_cleaned_tau_candidates_pt","signalAnalysis/TauSelection/TauSelection_cleaned_tau_candidates_pt"], 5, "log"],
            [["signalAnalysis/tauID/TauSelection_cleaned_tau_candidates_eta","signalAnalysis/TauSelection/TauSelection_cleaned_tau_candidates_eta"], 0.1, "log"],
            [["signalAnalysis/tauID/TauSelection_cleaned_tau_candidates_phi","signalAnalysis/TauSelection/TauSelection_cleaned_tau_candidates_phi"], 3.14159265 / 36, "log"],
            [["signalAnalysis/tauID/TauSelection_cleaned_tau_candidates_MC_purity","signalAnalysis/TauSelection/TauSelection_cleaned_tau_candidates_MC_purity"], 1, "log"]
        ]],
        ["Tau ID", [
            [["signalAnalysis/tauID/IsolationPFChargedHadrCandsPtSum","signalAnalysis/TauSelection/IsolationPFChargedHadrCandsPtSum"], 1, "log"],
            [["signalAnalysis/tauID/IsolationPFGammaCandEtSum","signalAnalysis/TauSelection/IsolationPFGammaCandEtSum"], 1, "log"],
            [["signalAnalysis/tauID/TauID_OneProngNumberCut","signalAnalysis/TauSelection/TauID_OneProngNumberCut"], 1, "log"],
            [["signalAnalysis/tauID/TauID_ChargeCut","signalAnalysis/TauSelection/TauID_ChargeCut"], 1, "log"],
            [["signalAnalysis/tauID/TauID_RtauCut","signalAnalysis/TauSelection/TauID_RtauCut"], 0.05, "log"],
            [["signalAnalysis/tauID/TauSelection_selected_taus_N","signalAnalysis/TauSelection/TauSelection_selected_taus_N"], 1, "log"],
            [["signalAnalysis/tauID/TauSelection_selected_taus_pt","signalAnalysis/TauSelection/TauSelection_selected_taus_pt"], 5, "log"],
            [["signalAnalysis/tauID/TauSelection_selected_taus_eta","signalAnalysis/TauSelection/TauSelection_selected_taus_eta"], 0.1, "log"],
            [["signalAnalysis/tauID/TauSelection_selected_taus_phi","signalAnalysis/TauSelection/TauSelection_selected_taus_phi"], 3.14159265 / 36, "log"],
            [["signalAnalysis/tauID/TauSelection_selected_taus_MC_purity","signalAnalysis/TauSelection/TauSelection_selected_taus_MC_purity"], 1, "log"],
            [["signalAnalysis/FakeTauIdentifier/TauMatchType","signalAnalysis/FakeTauIdentifier_TauID/TauMatchType"], 1, "log"],
            [["signalAnalysis/FakeTauIdentifier/TauOrigin","signalAnalysis/FakeTauIdentifier_TauID/TauOrigin"], 1, "log"],
            [["signalAnalysis/FakeTauIdentifier/MuOrigin","signalAnalysis/FakeTauIdentifier_TauID/MuOrigin"], 1, "log"],
            [["signalAnalysis/FakeTauIdentifier/ElectronOrigin","signalAnalysis/FakeTauIdentifier_TauID/ElectronOrigin"], 1, "log"],
        ]],
        ["Tau after tau ID", [
            [histoDir+"/SelectedTau/SelectedTau_pT_AfterTauID", 5, "log"],
            [histoDir+"/SelectedTau/SelectedTau_eta_AfterTauID", 0.1, "log"],
            [histoDir+"/SelectedTau/SelectedTau_phi_AfterTauID", 3.14159265 / 36, "log"],
            [histoDir+"/SelectedTau/SelectedTau_Rtau_AfterTauID", 0.05, "log"],
        ]],
        ["Tau after all cuts", [
            ["signalAnalysis/SelectedTau/SelectedTau_pT_AfterCuts", 10, "log"],
            ["signalAnalysis/SelectedTau/SelectedTau_eta_AfterCuts", 0.2, "log"],
            ["signalAnalysis/SelectedTau/SelectedTau_Rtau_AfterCuts", 0.05, "log"],
            [["signalAnalysis/SelectedTau/NonQCDTypeII_SelectedTau_pT_AfterCuts","signalAnalysis/SelectedTau/NonQCDTypeII_SelectedTau_pT_AfterCuts"], 10, "log"],
            [["signalAnalysis/SelectedTau/NonQCDTypeII_SelectedTau_eta_AfterCuts","signalAnalysis/SelectedTau/NonQCDTypeII_SelectedTau_eta_AfterCuts"], 0.2, "log"],
        ]],
        ["Electrons", [
            [histoDir+"/GlobalElectronVeto/GlobalElectronPt", 5, "log"],
            [histoDir+"/GlobalElectronVeto/GlobalElectronEta", 0.1, "log"]
        ]],
        ["Muons", [
            [histoDir+"/GlobalMuonVeto/GlobalMuonPt", 5, "log"],
            [histoDir+"/GlobalMuonVeto/GlobalMuonEta", 0.1, "log"]
        ]],
        ["All jets", [
            [histoDir+"/JetSelection/jet_pt", 10, "log"],
            [histoDir+"/JetSelection/jet_pt_central", 5, "log"],
            [histoDir+"/JetSelection/jet_eta", 0.2, "log"],
            [histoDir+"/JetSelection/jet_phi", 3.14159265 / 36, "log"],
            [histoDir+"/JetSelection/jetEMFraction", 0.05, "log"],
            [histoDir+"/JetSelection/firstJet_pt", 10, "log"],
            [histoDir+"/JetSelection/firstJet_eta", 0.2, "log"],
            [histoDir+"/JetSelection/firstJet_phi", 3.14159265 / 36, "log"],
            [histoDir+"/JetSelection/secondJet_pt", 10, "log"],
            [histoDir+"/JetSelection/secondJet_eta", 0.2, "log"],
            [histoDir+"/JetSelection/secondJet_phi", 3.14159265 / 36, "log"],
            [histoDir+"/JetSelection/thirdJet_pt", 10, "log"],
            [histoDir+"/JetSelection/thirdJet_eta", 0.2, "log"],
            [histoDir+"/JetSelection/thirdJet_phi", 3.14159265 / 36, "log"],
        ]],
        ["Selected jets", [
            [histoDir+"/JetSelection/NumberOfSelectedJets", 10, "log"],
            [histoDir+"/JetSelection/SelectedJets/jet_pt", 5, "log"],
            [histoDir+"/JetSelection/SelectedJets/jet_eta", 0.2, "log"],
            [histoDir+"/JetSelection/SelectedJets/jet_phi", 3.14159265 / 36, "log"],
            [histoDir+"/JetSelection/SelectedJets/jet_NeutralEmEnergyFraction", 0.05, "log"],
            [histoDir+"/JetSelection/SelectedJets/jet_NeutralHadronFraction", 0.05, "log"],
            [histoDir+"/JetSelection/SelectedJets/jet_NeutralHadronMultiplicity", 1, "log"],
            [histoDir+"/JetSelection/SelectedJets/jet_PhotonEnergyFraction", 0.05, "log"],
            [histoDir+"/JetSelection/SelectedJets/jet_PhotonMultiplicity", 1, "log"],
            [histoDir+"/JetSelection/SelectedJets/jet_ChargedHadronEnergyFraction", 0.05, "log"],
            [histoDir+"/JetSelection/SelectedJets/jet_ChargedMultiplicity", 1, "log"],
            [histoDir+"/JetSelection/SelectedJets/jet_PartonFlavour", 1, "log"],
        ]],
        ["Excluded jets, i.e. jets with DeltaR(jet, tau) < 0.5", [
            [histoDir+"/JetSelection/ExcludedJets/jet_pt", 10, "log"],
            [histoDir+"/JetSelection/ExcludedJets/jet_eta", 0.2, "log"],
            [histoDir+"/JetSelection/ExcludedJets/jet_phi", 3.14159265 / 36, "log"],
            [histoDir+"/JetSelection/ExcludedJets/jet_NeutralEmEnergyFraction", 0.05, "log"],
            [histoDir+"/JetSelection/ExcludedJets/jet_NeutralHadronFraction", 0.05, "log"],
            [histoDir+"/JetSelection/ExcludedJets/jet_NeutralHadronMultiplicity", 1, "log"],
            [histoDir+"/JetSelection/ExcludedJets/jet_PhotonEnergyFraction", 0.05, "log"],
            [histoDir+"/JetSelection/ExcludedJets/jet_PhotonMultiplicity", 1, "log"],
            [histoDir+"/JetSelection/ExcludedJets/jet_ChargedHadronEnergyFraction", 0.05, "log"],
            [histoDir+"/JetSelection/ExcludedJets/jet_ChargedMultiplicity", 1, "log"],
            [histoDir+"/JetSelection/ExcludedJets/jet_PartonFlavour", 1, "log"],
        ]],
        ["MET", [
            [histoDir+"/MET/met", 20, "log"],
            [histoDir+"/MET/metSignif", 5, "log"],
            [histoDir+"/MET/metSumEt", 20, "log"],
        ]],
        ["b-jet tagging", [
            [histoDir+"/Btagging/NumberOfBtaggedJets", 1, "log"],
            [histoDir+"/Btagging/jet_bdiscriminator", 0.1, "log"],
            [histoDir+"/Btagging/bjet_pt", 10, "log"],
            [histoDir+"/Btagging/bjet_eta", 0.2, "log"],
            [histoDir+"/Btagging/bjet1_pt", 20, "log"],
            [histoDir+"/Btagging/bjet1_eta", 0.2, "log"],
            [histoDir+"/Btagging/bjet2_pt", 20, "log"],
            [histoDir+"/Btagging/bjet2_eta", 0.2, "log"],
            [histoDir+"/Btagging/MCMatchForPassedJets", 1, "log"],
        ]],
        ["Transverse mass", [
            ["signalAnalysis/deltaPhi", 10, "linear"],
            [["signalAnalysis/transverseMass","signalAnalysis/transverseMassAfterDeltaPhi160"], 20, "linear"],
            [["signalAnalysis/NonQCDTypeIITransverseMassAfterDeltaPhi160","signalAnalysis/EWKFakeTausTransverseMass"], 20, "linear"],
        ]]
    ]
    if debugstatus:
        histolist = [["Primary vertices", [[histoDir+"/Vertices/verticesBeforeWeight", 1, "log"],[histoDir+"/TauSelection/N_TriggerMatchedTaus", 1, "log"]]]]

    mycolumns = 2
    myscale = 200.0 / float(mycolumns)
    myindexcount = 0
    # table of contents
    myoutput += "List of histogram groups:</a><br>\n"
    for group in histolist:
        myoutput += "<a href=#idx"+str(myindexcount)+"_"+dataset1.getName()+">"+group[0]+"</a><br>\n"
        myindexcount += 1
    myoutput += "<br>\n"

    # histograms
    myindexcount = 0
    mydifference = 0
    for group in histolist:
        myoutput += "<hr><h3><a name=idx"+str(myindexcount)+"_"+dataset1.getName()+">"+group[0]+"</a></h3><br>\n"
        myindexcount += 1
        myoutput += "<table>\n"
        mycount = 0
        for histoname in group[1]:
            print "Getting histogram",histoname[0]
            if mycount == 0:
                myoutput += "<tr>\n"
            mycount = mycount + 1
            myoutput += "<td>"
            # Failsafe for legacy histogram names
            hname1 = None
            hname2 = None
            if isinstance(histoname[0],list):
                for aname in histoname[0]:
                    if dataset1.hasRootHisto(aname):
                        hname1 = aname
                    if dataset2.hasRootHisto(aname):
                        hname2 = aname
            else:
                if dataset1.hasRootHisto(histoname[0]):
                    hname1 = histoname[0]
                if dataset2.hasRootHisto(histoname[0]):
                    hname2 = histoname[0]
            # Check that histograms are found and make comparison plot
            if hname1 != None and hname2 != None:
                # construct output name
                myname = hname1.replace("/", "_")
                # Obtain histograms and make canvas
                h1 = getHistogram(dataset1, histoname, hname1, True)
                #expandOverflowBins(h1)
                h2 = getHistogram(dataset2, histoname, hname2, False)
                #expandOverflowBins(h2)
                # Make sure that binning is compatible
                #print "binning:",h1.GetNbinsX(),h1.GetXaxis().GetXmin(),h1.GetXaxis().GetXmax()," / ",h2.GetNbinsX(),h2.GetXaxis().GetXmin(),h2.GetXaxis().GetXmax()
                #if h1.GetXaxis().GetXmax() > h2.GetXaxis().GetXmax():
                    #nbins = (h1.GetXaxis().GetXmax()-h1.GetXaxis().GetXmin()) / h2.GetXaxis().GetBinWidth(1)
                    #h2.GetXaxis().Set(int(nbins),h1.GetXaxis().GetXmin(),h1.GetXaxis().GetXmax())
                    #print "- range changed:",h1.GetNbinsX(),h1.GetXaxis().GetXmin(),h1.GetXaxis().GetXmax()," / ",h2.GetNbinsX(),h2.GetXaxis().GetXmin(),h2.GetXaxis().GetXmax()
                #if h1.GetNbinsX() != h2.GetNbinsX():
                    #if h1.GetNbinsX() > h2.GetNbinsX():
                        #mystatus = False
                        #i = 1
                        #while not mystatus and i < 10:
                            #if h1.GetNbinsX() * i % h2.GetNbinsX() == 0:
                                #h1.Rebin(floor(float(h1.GetNbinsX()) / float(h2.GetNbinsX())))
                                #h2.Rebin(i)
                                #print "rebin:",h1.GetNbinsX(),h1.GetXaxis().GetXmin(),h1.GetXaxis().GetXmax()," / ",h2.GetNbinsX(),h2.GetXaxis().GetXmin(),h2.GetXaxis().GetXmax()
                                #mystatus = True
                            #i += 1
                    #else:
                        #if h2.GetNbinsX() % h1.GetNbinsX() == 0:
                            #h2.Rebin(h2.GetNbinsX() / h1.GetNbinsX())

                # Create canvas
                canvas = ROOT.TCanvas(hname1,hname1,600,500)
                canvas.cd()
                setCanvasDefinitions(canvas)
                # Make frame and set its extrema
                myframe = h1.Clone("hclone")
                myframe.SetBinContent(1,0)
                myframe.SetStats(0)
                myframe.SetXTitle("")
                myframe.GetXaxis().SetLabelSize(0)
                myframe.SetTitleSize(0.06, "Y")
                myframe.SetLabelSize(0.05, "Y")
                myframe.GetYaxis().SetTitleOffset(0.75)
                setframeextrema(myframe,h1,h2,histoname[2])
                # Make agreement histograms
                hdiff = h2.Clone("hdiffclone")
                hdiff.SetStats(0)
                hdiff.Divide(h1)
                hdiffWarn = hdiff.Clone("hdiffwarn")
                hdiffWarn.SetLineColor(ROOT.kOrange)
                hdiffWarn.SetFillColor(ROOT.kOrange)
                hdiffWarn.SetMarkerColor(ROOT.kOrange)
                hdiffError = hdiff.Clone("hdifferror")
                hdiffError.SetLineColor(ROOT.kRed+1)
                hdiffError.SetFillColor(ROOT.kRed+1)
                hdiffError.SetMarkerColor(ROOT.kRed+1)
                for i in range(1, hdiff.GetNbinsX()+1):
                    if hdiff.GetBinContent(i) > 0 and abs(hdiff.GetBinContent(i) - 1) > 0.03:
                        hdiffError.SetBinContent(i, hdiff.GetBinContent(i))
                        hdiffError.SetBinError(i, hdiff.GetBinError(i))
                        hdiff.SetBinContent(i, -100)
                        hdiffWarn.SetBinContent(i, -100)
                    elif hdiff.GetBinContent(i) > 0 and abs(hdiff.GetBinContent(i) - 1) > 0.01:
                        hdiffWarn.SetBinContent(i, hdiff.GetBinContent(i))
                        hdiffWarn.SetBinError(i, hdiff.GetBinError(i))
                        hdiff.SetBinContent(i, -100)
                # Line at zero
                hdiffLine = h1.Clone("hdifflineclone")
                hdiffLine.SetLineColor(ROOT.kGray)
                for i in range(1, hdiff.GetNbinsX()+1):
                    hdiffLine.SetBinContent(i,1)
                    hdiffLine.SetBinError(i,0)
                hdiffLine.SetLineWidth(1)
                hdiffLine.SetFillStyle(0)
                hdiffLine.SetMaximum(2)
                hdiffLine.SetMinimum(0)
                hdiffLine.SetTitle("")
                hdiffLine.SetStats(0)
                hdiffLine.SetTitleSize(0.05 / 0.3 * 0.7, "XYZ")
                hdiffLine.SetLabelSize(0.05 / 0.3 * 0.7, "XYZ")
                hdiffLine.SetNdivisions(505, "Y")
                hdiffLine.GetXaxis().SetTitleOffset(1.1)
                hdiffLine.GetYaxis().SetTitleOffset(0.4)
                hdiffLine.SetXTitle(h1.GetXaxis().GetTitle())
                hdiffLine.SetYTitle("New/Ref.")
                # Analyse agreement
                mydifference = analysehistodiff(canvas,h1,h2)
                # Plot pad
                canvas.cd(1)
                if histoname[2] == "log":
                    canvas.GetPad(1).SetLogy()
                myframe.Draw()
                h1.Draw("histo sames")
                h2.Draw("e1 sames")
                canvas.GetPad(1).RedrawAxis()
                # Modify stat boxes
                canvas.GetPad(1).Update()
                h1.FindObject("stats").SetLineColor(ROOT.kBlue-6)
                h1.FindObject("stats").SetTextColor(ROOT.kBlue-6)
                h1.FindObject("stats").Draw()
                h2.FindObject("stats").SetY1NDC(0.615)
                h2.FindObject("stats").SetY2NDC(0.775)
                h2.FindObject("stats").Draw()
                canvas.GetPad(1).Modified()
                #canvas.GetPad(1).Update()
                # Difference pad
                canvas.cd(2)
                hdiffLine.Draw()
                hdiffError.Draw("e same")
                hdiffWarn.Draw("e same")
                hdiff.Draw("e same")
                canvas.GetPad(2).RedrawAxis()
                canvas.GetPad(2).Modified()
                # Save plot
                canvas.Modified()
                canvas.Print(mysubdir+"/"+myname+".png")
                canvas.Close()
                myoutput += "<br><img"
                #myoutput += " width=%f%%" % myscale
                #myoutput += " height=%f%%" % myscale
                myoutput += " src="+mydir+"/"+myname+".png alt="+hname1+"><br>"
            else:
                # cannot create figure because one or both histograms are not available
                if hname1 == None:
                    print "  Warning: Did not find histogram",histoname[0],"in",dataset1.getName()
                    myoutput += "<text color=e00000>Not found for reference!</text><br>"
                if hname2 == None:
                    print "  Warning: Did not find histogram",histoname[0],"in",dataset2.getName()
                    myoutput += "<text color=e00000>Not found for new dataset!</text><br>"
            hnamestr = None
            if isinstance(histoname[0],list):
                hnamestr = "["
                for aname in histoname[0]:
                    hnamestr += aname+" "
                hnamestr += "]"
            else:
                hnamestr = histoname[0]
            myoutput += "\n<br>src = "+hnamestr
            myoutput += "<br>bin width = "+str(histoname[1])
            myoutput += "<br>Difference = %1.3f\n" % mydifference
            # close cell (and if necessary also row) in table
            myoutput += "</td>\n"
            if mycount == mycolumns:
                myoutput += "</tr>\n"
                mycount = 0
        # close if necessary row in table
        if mycount > 0:
            myoutput += "</tr>\n"
        myoutput += "</table>\n"
        myoutput += "<a href=#histotop_"+dataset1.getName()+">Back to histogram list</a><br>\n"
    print "\nHistograms done for dataset",dataset1.getName()
    print "Legend: blue histogram = reference, red points = dataset to be validated\n"
    return myoutput

def makehtml(mydir, myoutput):
    myhtmlheader = "<html>\n<head>\n<title>ValidationResults</title>\n</head>\n<body>\n"
    myhtmlfooter = "</body>\n</html>\n"
    myfile = open(mydir+"/index.html","w")
    #myfile = open("index.html","w")
    myfile.write(myhtmlheader)
    myfile.write("<h1>Validation results for: "+mydir+"</h1><br>\n<hr><br>\n")
    myfile.write(myoutput)
    myfile.write(myhtmlfooter)
    myfile.close()

def main(argv):
    if not len(sys.argv) == 4:
        print "\n"
        print "### Usage:   EventCounterValidation.py <ref multi-crab path> <new multi-crab path> era\n"
        print "\n"
        sys.exit()

    referenceData = sys.argv[1]
    validateData  = sys.argv[2]
    era           = sys.argv[3]

    oldCounters = "signalAnalysisCounters"
    newCounters = "signalAnalysis/counters"
    era = "Run2011A"
    #newCounters = "signalAnalysisData2011A/counters"

    oldCounters = "signalAnalysisCounters"
    newCounters = "signalAnalysis/counters"
    era = "Run2011A"
    #newCounters = "signalAnalysisData2011A/counters"

    oldCounters = "signalAnalysisCounters"
    newCounters = "signalAnalysis/counters"
    era = "Run2011A"
    #newCounters = "signalAnalysisData2011A/counters"

    mytimestamp = datetime.now().strftime("%d%m%y_%H%M%S")
    if debugstatus:
        mytimestamp = "debug"
    mydir = "validation_"+mytimestamp
    if not os.path.exists(mydir):
        os.mkdir(mydir)

    myoutput = ""

    histoDir = "signalAnalysis"+era
    counterDir = histoDir+"/counters"

    print "Running script EventCounterValidation.py on"
    print
    print "          reference datasets = ",referenceData
    print "          validated datasets = ",validateData
    print
    print "          era = ",era
    print "          counter dir = ",counterDir
    print



    ROOT.gROOT.SetBatch() # no flashing canvases

    myoutput += "<b>Shell command that was run:</b>"
    for arg in argv:
         myoutput += " "+arg
    myoutput += "<br><br>\n"
    myoutput += "<b>Reference multicrab directory:</b> "+referenceData+"<br>\n"
    myoutput += "<b>New multicrab directory to be validated:</b> "+validateData+"<br><br>\n"
    myoutput += "<b>Era: "+era+"</b><br>\n<hr><br>\n"

    refDatasetNames = getDatasetNames(referenceData,counters=oldCounters,era=era,legacy=True)
    valDatasetNames = getDatasetNames(validateData,counters=newCounters,era=era)

    datasetNames = validateDatasetExistence(refDatasetNames,valDatasetNames)
    myoutput += "<h3><a name=maintop>List of datasets analysed:</a></h3><br>\n"
    for datasetname in datasetNames:
        myoutput += "<a href=#dataset_"+datasetname+">"+datasetname+"</a><br>\n"
    myoutput += "<hr><br>\n"
    for datasetname in datasetNames:
        print "\n\n"
        print datasetname
        myoutput += "<h2><a name=dataset_"+datasetname+">Dataset: "+datasetname+"</a></h2><br>\n"
        refDatasets = dataset.getDatasetsFromCrabDirs([referenceData+"/"+datasetname],counters=oldCounters)
        valDatasets = dataset.getDatasetsFromCrabDirs([validateData+"/"+datasetname],counters=newCounters,dataEra=era)

        myoutput += validateCounters(refDatasets,valDatasets)
        myoutput += validateHistograms(mydir,histoDir,refDatasets.getDataset(datasetname),valDatasets.getDataset(datasetname))
        myoutput += "<hr><br>\n"

    print "\nResults saved into directory:",mydir
    print "To view html version, use link "+mydir+"/index.html"
    makehtml(mydir,myoutput)

main(sys.argv[1:])



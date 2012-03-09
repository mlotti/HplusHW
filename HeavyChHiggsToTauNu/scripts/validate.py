#!/usr/bin/env python

import sys
import os
import ROOT

from datetime import date, time, datetime

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter

analysis = "signalAnalysis"
counters = analysis+"Counters"

debugstatus = True


def getDatasetNames(multiCrabDir):
    datasets = dataset.getDatasetsFromMulticrabDirs([multiCrabDir],counters=counters)
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
    for i in xrange(counter.getNrows()):
        if row == counter.rowNames[i]:
            return int(counter.getCount(i,0).value())
    print "Counter value not found, exiting.."
    sys.exit()

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
    myoutput += "<td align=center>"+str(value2)+"</td>"
    myoutput += "<td align=center>"+str(value1)+"</td>"
    if value1 == value2:
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

def validateCounterValues(rownames,counter1,counter2):
    # Make table in output
    myoutput = "<table>\n"
    myoutput += "<tr><td><b>Counter</b></td>"
    myoutput += "<td><b>New counts</b></td><td><b>Ref. counts</b></td><td><b>New/Ref.</b></td>"
    myoutput += "<td><b>New eff.</b></td><td><b>Ref. eff.</b></td><td><b>New/Ref.</b></td>"
    myoutput += "</tr>\n"
    oldrow = ""
    for row in rownames:
        myoutput += report(oldrow, row,counter1,counter2)
        oldrow = row
    myoutput += "</table>\n"
    return myoutput

def validateCounters(dataset1,dataset2):
    eventCounter1 = counter.EventCounter(dataset1)
    counter1 = eventCounter1.getMainCounter().getTable()
    rownames1 = counter1.getRowNames()

    eventCounter2 = counter.EventCounter(dataset2)
    counter2 = eventCounter2.getMainCounter().getTable()
    rownames2 = counter2.getRowNames()

    rownames = validateNames(rownames1,rownames2)

    myoutput = validateCounterValues(rownames,counter1,counter2)
    return myoutput

def getHistogram(dataset, histoname, isRef):
    roothisto = dataset.getDatasetRootHisto(histoname[0])
    roothisto.normalizeToOne()
    h = roothisto.getHistogram()
    # Rebin
    a = (h.GetXaxis().GetXmax() - h.GetXaxis().GetXmin()) / h.GetNbinsX()
    if histoname[1] > a:
        h.Rebin(int(histoname[1] / a))
    # Set attributes
    h.SetStats(1)
    if isRef:
        h.SetName("Reference")
        h.SetFillStyle(1001)
        h.SetFillColor(ROOT.kBlue-6)
        h.SetLineColor(ROOT.kBlue-6)
        #statbox.SetTextColor(ROOT.kBlue-6)
    else:
        h.SetName("New")
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
    canvas.GetPad(1).SetFrameFillColor(ROOT.TColor.GetColor("#fdffff"))
    canvas.GetPad(2).SetFrameFillColor(ROOT.TColor.GetColor("#fdffff"))
    if not h1.GetNbinsX() == h2.GetNbinsX():
        canvas.GetPad(1).SetFillColor(ROOT.kOrange)
        canvas.GetPad(2).SetFillColor(ROOT.kOrange)
    else:
        # same number of bins in histograms
        diff = 0.0
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

def validateHistograms(mydir,dataset1,dataset2):
    mysubdir = mydir+"/"+dataset1.getName()
    if not os.path.exists(mysubdir):
        os.mkdir(mysubdir)
    mydir = dataset1.getName()

    myoutput = "<br><h3><a name=histotop>Histograms for validation:</a></h3><br>\n"
    myoutput += "Color legend: blue histogram = reference, red points = dataset to be validated<br>\n"
    myoutput += "Difference is defined as sum_i (abs(new_i / ref_i - 1.0)), where sum goes over the histogram bins<br><br>\n"
    print "Generating validation histograms"
    # entry syntax: histogram_name_with_path, bin_width, linear/log
    histolist = [
        ["Primary vertices", [
            ["signalAnalysis/Vertices/verticesBeforeWeight", 1, "log"],
            ["signalAnalysis/Vertices/verticesAfterWeight", 1, "log"],
            ["signalAnalysis/Vertices/verticesTriggeredBeforeWeight", 1, "log"],
            ["signalAnalysis/Vertices/verticesTriggeredAfterWeight", 1, "log"],
        ]],
        ["Trigger matched tau collection", [
            ["signalAnalysis/tauID/N_TriggerMatchedTaus", 1, "log"],
            ["signalAnalysis/tauID/N_TriggerMatchedSeparateTaus", 1, "log"],
            ["signalAnalysis/tauID/HPSDecayMode", 1, "log"],
            ["signalAnalysis/tauID/TauSelection_all_tau_candidates_N", 1, "log"],
            ["signalAnalysis/tauID/TauSelection_all_tau_candidates_pt", 5, "log"],
            ["signalAnalysis/tauID/TauSelection_all_tau_candidates_eta", 0.1, "log"],
            ["signalAnalysis/tauID/TauSelection_all_tau_candidates_phi", 3.14159265 / 36, "log"],
            ["signalAnalysis/tauID/TauSelection_all_tau_candidates_MC_purity", 1, "log"]
        ]],
        ["Tau candidate selection", [
            ["signalAnalysis/tauID/TauCand_JetPt", 5, "log"],
            ["signalAnalysis/tauID/TauCand_JetEta", 0.1, "log"],
            ["signalAnalysis/tauID/TauCand_LdgTrackPtCut", 5, "log"],
            ["signalAnalysis/tauID/TauCand_EMFractionCut", 0.05, "log"],
            ["signalAnalysis/tauID/TauSelection_cleaned_tau_candidates_N", 1, "log"],
            ["signalAnalysis/tauID/TauSelection_cleaned_tau_candidates_pt", 5, "log"],
            ["signalAnalysis/tauID/TauSelection_cleaned_tau_candidates_eta", 0.1, "log"],
            ["signalAnalysis/tauID/TauSelection_cleaned_tau_candidates_phi", 3.14159265 / 36, "log"],
            ["signalAnalysis/tauID/TauSelection_cleaned_tau_candidates_MC_purity", 1, "log"]
        ]],
        ["Tau ID", [
            ["signalAnalysis/tauID/IsolationPFChargedHadrCandsPtSum", 1, "log"],
            ["signalAnalysis/tauID/IsolationPFGammaCandEtSum", 1, "log"],
            ["signalAnalysis/tauID/TauID_OneProngNumberCut", 1, "log"],
            ["signalAnalysis/tauID/TauID_ChargeCut", 1, "log"],
            ["signalAnalysis/tauID/TauID_RtauCut", 0.05, "log"],
            ["signalAnalysis/tauID/TauSelection_selected_taus_N", 1, "log"],
            ["signalAnalysis/tauID/TauSelection_selected_taus_pt", 5, "log"],
            ["signalAnalysis/tauID/TauSelection_selected_taus_eta", 0.1, "log"],
            ["signalAnalysis/tauID/TauSelection_selected_taus_phi", 3.14159265 / 36, "log"],
            ["signalAnalysis/tauID/TauSelection_selected_taus_MC_purity", 1, "log"],
            ["signalAnalysis/FakeTauIdentifier/TauMatchType", 1, "log"],
            ["signalAnalysis/FakeTauIdentifier/TauOrigin", 1, "log"],
            ["signalAnalysis/FakeTauIdentifier/MuOrigin", 1, "log"],
            ["signalAnalysis/FakeTauIdentifier/ElectronOrigin", 1, "log"],
        ]],
        ["Tau after tau ID", [
            ["signalAnalysis/SelectedTau/SelectedTau_pT_AfterTauID", 5, "log"],
            ["signalAnalysis/SelectedTau/SelectedTau_eta_AfterTauID", 0.1, "log"],
            ["signalAnalysis/SelectedTau/SelectedTau_phi_AfterTauID", 3.14159265 / 36, "log"],
            ["signalAnalysis/SelectedTau/SelectedTau_Rtau_AfterTauID", 0.05, "log"],
        ]],
        ["Tau after all cuts", [
            ["signalAnalysis/SelectedTau/SelectedTau_pT_AfterCuts", 10, "log"],
            ["signalAnalysis/SelectedTau/SelectedTau_eta_AfterCuts", 0.2, "log"],
            ["signalAnalysis/SelectedTau/SelectedTau_Rtau_AfterCuts", 0.05, "log"],
            ["signalAnalysis/SelectedTau/NonQCDTypeII_SelectedTau_pT_AfterCuts", 10, "log"],
            ["signalAnalysis/SelectedTau/NonQCDTypeII_SelectedTau_eta_AfterCuts", 0.2, "log"],
        ]],
        ["Electrons", [
            ["signalAnalysis/GlobalElectronVeto/GlobalElectronPt", 5, "log"],
            ["signalAnalysis/GlobalElectronVeto/GlobalElectronEta", 0.1, "log"]
        ]],
        ["Muons", [
            ["signalAnalysis/GlobalMuonVeto/GlobalMuonPt", 5, "log"],
            ["signalAnalysis/GlobalMuonVeto/GlobalMuonEta", 0.1, "log"]
        ]],
        ["All jets", [
            ["signalAnalysis/JetSelection/jet_pt", 5, "log"],
            ["signalAnalysis/JetSelection/jet_pt_central", 5, "log"],
            ["signalAnalysis/JetSelection/jet_eta", 0.1, "log"],
            ["signalAnalysis/JetSelection/jet_phi", 3.14159265 / 36, "log"],
            ["signalAnalysis/JetSelection/jetEMFraction", 0.05, "log"],
            ["signalAnalysis/JetSelection/firstJet_pt", 5, "log"],
            ["signalAnalysis/JetSelection/firstJet_eta", 0.1, "log"],
            ["signalAnalysis/JetSelection/firstJet_phi", 3.14159265 / 36, "log"],
            ["signalAnalysis/JetSelection/secondJet_pt", 5, "log"],
            ["signalAnalysis/JetSelection/secondJet_eta", 0.1, "log"],
            ["signalAnalysis/JetSelection/secondJet_phi", 3.14159265 / 36, "log"],
            ["signalAnalysis/JetSelection/thirdJet_pt", 5, "log"],
            ["signalAnalysis/JetSelection/thirdJet_eta", 0.1, "log"],
            ["signalAnalysis/JetSelection/thirdJet_phi", 3.14159265 / 36, "log"],
        ]],
        ["Selected jets", [
            ["signalAnalysis/JetSelection/NumberOfSelectedJets", 1, "log"],
            ["signalAnalysis/JetSelection/SelectedJets/jet_pt", 5, "log"],
            ["signalAnalysis/JetSelection/SelectedJets/jet_eta", 0.1, "log"],
            ["signalAnalysis/JetSelection/SelectedJets/jet_phi", 3.14159265 / 36, "log"],
            ["signalAnalysis/JetSelection/SelectedJets/jet_NeutralEmEnergyFraction", 0.05, "log"],
            ["signalAnalysis/JetSelection/SelectedJets/jet_NeutralHadronFraction", 0.05, "log"],
            ["signalAnalysis/JetSelection/SelectedJets/jet_NeutralHadronMultiplicity", 1, "log"],
            ["signalAnalysis/JetSelection/SelectedJets/jet_PhotonEnergyFraction", 0.05, "log"],
            ["signalAnalysis/JetSelection/SelectedJets/jet_PhotonMultiplicity", 1, "log"],
            ["signalAnalysis/JetSelection/SelectedJets/jet_ChargedHadronEnergyFraction", 0.05, "log"],
            ["signalAnalysis/JetSelection/SelectedJets/jet_ChargedMultiplicity", 1, "log"],
            ["signalAnalysis/JetSelection/SelectedJets/jet_PartonFlavour", 1, "log"],
        ]],
        ["Excluded jets, i.e. jets with DeltaR(jet, tau) < 0.5", [
            ["signalAnalysis/JetSelection/ExcludedJets/jet_pt", 5, "log"],
            ["signalAnalysis/JetSelection/ExcludedJets/jet_eta", 0.1, "log"],
            ["signalAnalysis/JetSelection/ExcludedJets/jet_phi", 3.14159265 / 36, "log"],
            ["signalAnalysis/JetSelection/ExcludedJets/jet_NeutralEmEnergyFraction", 0.05, "log"],
            ["signalAnalysis/JetSelection/ExcludedJets/jet_NeutralHadronFraction", 0.05, "log"],
            ["signalAnalysis/JetSelection/ExcludedJets/jet_NeutralHadronMultiplicity", 1, "log"],
            ["signalAnalysis/JetSelection/ExcludedJets/jet_PhotonEnergyFraction", 0.05, "log"],
            ["signalAnalysis/JetSelection/ExcludedJets/jet_PhotonMultiplicity", 1, "log"],
            ["signalAnalysis/JetSelection/ExcludedJets/jet_ChargedHadronEnergyFraction", 0.05, "log"],
            ["signalAnalysis/JetSelection/ExcludedJets/jet_ChargedMultiplicity", 1, "log"],
            ["signalAnalysis/JetSelection/ExcludedJets/jet_PartonFlavour", 1, "log"],
        ]],
        ["MET", [
            ["signalAnalysis/MET/met", 5, "log"],
            ["signalAnalysis/MET/metSignif", 5, "log"],
            ["signalAnalysis/MET/metSumEt", 10, "log"],
        ]],
        ["b-jet tagging", [
            ["signalAnalysis/Btagging/NumberOfBtaggedJets", 1, "log"],
            ["signalAnalysis/Btagging/jet_bdiscriminator", 5, "log"],
            ["signalAnalysis/Btagging/bjet_pt", 5, "log"],
            ["signalAnalysis/Btagging/bjet_eta", 0.1, "log"],
            ["signalAnalysis/Btagging/bjet1_pt", 5, "log"],
            ["signalAnalysis/Btagging/bjet1_eta", 0.1, "log"],
            ["signalAnalysis/Btagging/bjet2_pt", 5, "log"],
            ["signalAnalysis/Btagging/bjet2_eta", 0.1, "log"],
            ["signalAnalysis/Btagging/MCMatchForPassedJets", 1, "log"],
        ]],
        ["Transverse mass", [
            ["signalAnalysis/deltaPhi", 10, "linear"],
            ["signalAnalysis/transverseMass", 20, "linear"],
            ["signalAnalysis/transverseMassAfterDeltaPhi160", 20, "linear"],
            ["signalAnalysis/transverseMassAfterDeltaPhi130", 20, "linear"],
        ]]
    ]

    #histolist = [["Primary vertices", [["signalAnalysis/Vertices/verticesBeforeWeight", 1, "log"],["signalAnalysis/tauID/N_TriggerMatchedTaus", 1, "log"]]]]

    mycolumns = 2
    myscale = 200.0 / float(mycolumns)
    myindexcount = 0
    # table of contents
    myoutput += "List of histogram groups:</a><br>\n"
    for group in histolist:
        myoutput += "<a href=#idx"+str(myindexcount)+">"+group[0]+"</a><br>\n"
        myindexcount += 1
    myoutput += "<br>\n"

    # histograms
    myindexcount = 0
    mydifference = 0
    for group in histolist:
        myoutput += "<hr><h3><a name=idx"+str(myindexcount)+">"+group[0]+"</a></h3><br>\n"
        myoutput += "<table>\n"
        mycount = 0
        for histoname in group[1]:
            if mycount == 0:
                myoutput += "<tr>\n"
            mycount = mycount + 1
            myoutput += "<td>"
            if dataset1.hasRootHisto(histoname[0]) and dataset2.hasRootHisto(histoname[0]):
                # construct output name
                myname = histoname[0].replace("/", "_")
                # Obtain histograms and make canvas
                h1 = getHistogram(dataset1, histoname, True)
                h2 = getHistogram(dataset2, histoname, False)
                canvas = ROOT.TCanvas(histoname[0],histoname[0],600,500)
                canvas.cd()
                setCanvasDefinitions(canvas)
                # Make frame and set its extrema
                myframe = h1.Clone("hclone")
                myframe.SetBinContent(1,0)
                myframe.SetStats(0)
                myframe.SetXTitle("")
                myframe.SetYTitle("A.u. (normalised to 1)")
                myframe.GetXaxis().SetLabelSize(0)
                setframeextrema(myframe,h1,h2,histoname[2])
                # Make agreement histograms
                hdiff = h2.Clone("hdiffclone")
                hdiff.SetStats(0)
                hdiff.Divide(h1)
                hdiffWarn = hdiff.Clone("hdiffwarn")
                hdiffWarn.SetLineColor(ROOT.kOrange)
                hdiffWarn.SetMarkerColor(ROOT.kOrange)
                hdiffError = hdiff.Clone("hdifferror")
                hdiffError.SetLineColor(ROOT.kRed+1)
                hdiffError.SetMarkerColor(ROOT.kRed+1)
                for i in range(1, hdiff.GetNbinsX()):
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
                hdiffLine = ROOT.TH1F("line","line",1,h2.GetXaxis().GetXmin(),h2.GetXaxis().GetXmax())
                hdiffLine.SetLineColor(ROOT.kGray)
                hdiffLine.SetBinContent(1,1)
                hdiffLine.SetLineWidth(1)
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
                #canvas.GetPad(1).Update()
                # Difference pad
                canvas.cd(2)
                hdiffLine.Draw()
                hdiffError.Draw("e same")
                hdiffWarn.Draw("e same")
                hdiff.Draw("e same")
                canvas.GetPad(2).RedrawAxis()
                canvas.GetPad(2).Update()
                # Save plot
                #canvas.Modified()
                canvas.Print(mysubdir+"/"+myname+".png")
                canvas.Close()
                myoutput += "<br><img"
                #myoutput += " width=%f%%" % myscale
                #myoutput += " height=%f%%" % myscale
                myoutput += " src="+mydir+"/"+myname+".png alt="+histoname[0]+"><br>"
            else:
                # cannot create figure because one or both histograms are not available
                if not dataset1.hasRootHisto(histoname[0]):
                    print "  Warning: Did not find histogram",histoname[0],"in",dataset1.getName()
                    myoutput += "<text color=e00000>Not found for reference!</text><br>"
                if not dataset2.hasRootHisto(histoname[0]):
                    print "  Warning: Did not find histogram",histoname[0],"in",dataset2.getName()
                    myoutput += "<text color=e00000>Not found for new dataset!</text><br>"
            myoutput += "\n<br>src = "+histoname[0]
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
        myoutput += "<a href=#histotop>Back to histogram list</a><br>\n"
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
    if not len(sys.argv) == 3:
        print "\n"
        print "### Usage:   EventCounterValidation.py <ref multi-crab path> <new multi-crab path>\n"
        print "\n"
        sys.exit()

    referenceData = sys.argv[1]
    validateData  = sys.argv[2]

    mytimestamp = datetime.now().strftime("%d%m%y_%H%M%S")
    if debugstatus:
        mytimestamp = "debug"
    mydir = "validation_"+mytimestamp
    if not os.path.exists(mydir):
        os.mkdir(mydir)

    myoutput = ""

    print "Running script EventCounterValidation.py on"
    print
    print "          reference datasets = ",referenceData
    print "          validated datasets = ",validateData
    print

    myoutput += "<b>Shell command that was run:</b>"
    for arg in argv:
         myoutput += " "+arg
    myoutput += "<br><br>\n"
    myoutput += "<b>Reference datasets:</b> "+referenceData+"<br>\n"
    myoutput += "<b>New datasets to be validated:</b> "+validateData+"<br>\n<hr><br>\n"

    refDatasetNames = getDatasetNames(referenceData)
    valDatasetNames = getDatasetNames(validateData)

    datasetNames = validateDatasetExistence(refDatasetNames,valDatasetNames)

    for datasetname in datasetNames:
        print "\n\n"
        print datasetname
        myoutput += "<h2>Dataset: "+datasetname+"</h2><br>\n"
        refDatasets = dataset.getDatasetsFromCrabDirs([referenceData+"/"+datasetname],counters=counters)
        valDatasets = dataset.getDatasetsFromCrabDirs([validateData+"/"+datasetname],counters=counters)

        myoutput += validateCounters(refDatasets,valDatasets)
        myoutput += validateHistograms(mydir,refDatasets.getDataset(datasetname),valDatasets.getDataset(datasetname))
        myoutput += "<hr><br>\n"

    print "\nResults saved into directory:",mydir
    makehtml(mydir,myoutput)

main(sys.argv[1:])



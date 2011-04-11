import ROOT
from ROOT import gROOT, TFile, TCanvas, TH1F

baseDir = "DQMData/Run 1/Validation/Run summary/TriggerEfficiency"

#fIN = TFile("DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root")
fIN = TFile("TTJets_TuneZ2_7TeV-madgraph-tauola_Spring11_20110324.root")
fIN.cd(baseDir);
fIN.ls()

num = gROOT.FindObject('Eta tau hltFilterL3TrackIsolationSingleIsoTau20Trk15MET25 matched')
den = gROOT.FindObject('Eta tau')

num.Divide(den)

canvas = TCanvas("canvas","",500,500)
canvas.cd()
num.Draw()
canvas.Print("triggerEff_eta.png")

num = gROOT.FindObject('Eta smallZ hltFilterL3TrackIsolationSingleIsoTau20Trk15MET25 matched')
den = gROOT.FindObject('Eta smallZ')

num.Divide(den)

canvas = TCanvas("canvas","",500,500)
canvas.cd()
num.Draw()
canvas.Print("triggerEff_eta_smallZ.png")

num = gROOT.FindObject('Eta largeZ hltFilterL3TrackIsolationSingleIsoTau20Trk15MET25 matched')
den = gROOT.FindObject('Eta largeZ')

num.Divide(den)

canvas = TCanvas("canvas","",500,500)
canvas.cd()
num.Draw()
canvas.Print("triggerEff_eta_largeZ.png")

num = gROOT.FindObject('Phi tau hltFilterL3TrackIsolationSingleIsoTau20Trk15MET25 matched')
den = gROOT.FindObject('Phi tau')

num.Divide(den)

canvas = TCanvas("canvas","",500,500)
canvas.cd()
num.Draw()
canvas.Print("triggerEff_phi.png")


num = gROOT.FindObject('Eta Z hltFilterL3TrackIsolationSingleIsoTau20Trk15MET25 matched')
den = gROOT.FindObject('Eta Z')

num.Divide(den)

canvas = TCanvas("canvas","",500,500)
canvas.cd()
num.Draw("CONT4COL ")
canvas.Print("triggerEff_etaZ.png")
canvas.Print("triggerEff_etaZ.C")


canvas = TCanvas("canvas","",500,500)
canvas.cd()
#zslice = num.ProjectionX(" ",14,16)
#zslice = num.ProjectionX(" ",24,26)
zslice = num.ProjectionX(" ",34,36)
zslice.SetStats(0)
zslice.Draw()
#zslice2 = num.ProjectionX(" ",14,16)
#zslice2.Draw('same')
canvas.Print("triggerEff_etaZprofile.png")


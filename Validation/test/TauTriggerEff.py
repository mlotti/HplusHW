import ROOT
from ROOT import gROOT, TFile, TCanvas, TH1F

baseDir = "DQMData/Run 1/Validation/Run summary/TriggerEfficiency"

fIN = TFile("DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root")
fIN.cd(baseDir);
fIN.ls()

num = gROOT.FindObject('Eta tau hltFilterL3TrackIsolationSingleIsoTau20Trk15MET25 matched')
den = gROOT.FindObject('Eta tau')

num.Divide(den)

canvas = TCanvas("canvas","",500,500)
canvas.cd()
num.Draw()
canvas.Print("triggerEff_eta.png")

import ROOT
import array
import sys

f = ROOT.TFile.Open(sys.argv[1]+"/ChargedHiggs_HplusTB_HplusToTauNu_M_350/res/histograms-ChargedHiggs_HplusTB_HplusToTauNu_M_350.root", 'read')

f2 = ROOT.TFile.Open(sys.argv[1]+"/TT/res/histograms-TT.root", 'read')

hist_signal = f.Get('Hplus2hwAnalysis_background_350to3000_Run2016/TransverseMass')

hist_TT = f2.Get('Hplus2hwAnalysis_background_350to3000_Run2016/TransverseMass')

##############################################
##############################################

ls = 35916.636

print ls

#signal normalised to 10 fb
xs_signal = 0.01
xs_TT = 831.76

#normalisation factors
norm_signal = ls*xs_signal/26584

norm_TT = ls*xs_TT/76664700


#scale histos
hist_signal.Scale(norm_signal)

hist_TT.Scale(norm_TT)

##############################################
##############################################

#bins = [20,25,30,35,40,50,60,120]
#bins = [20,40,60,120]

#n = hist_dummy_num_1pr.Rebin(len(bins)-1,"data_nnew",array.array("d",bins))
#d = hist_dummy_den_1pr.Rebin(len(bins)-1,"data_dnew",array.array("d",bins))

#bins = [20,25,30,35,40,50,60,120]
#bins = [20,40,60,120]

#n = hist_num_DY.Rebin(len(bins)-1,"DY_nnew",array.array("d",bins))
#d = hist_den_DY.Rebin(len(bins)-1,"DY_dnew",array.array("d",bins))

canvas = ROOT.TCanvas('canvas', '', 500,500)

hist_TT.Draw()
hist_TT.SetMarkerStyle(20)
hist_TT.GetXaxis().SetRangeUser(0,1000)
#hist_TT.GetYaxis().SetRangeUser(0,0.5)

hist_signal.Draw("SAME")
#hist_signal.GetXaxis().SetRangeUser(20,120)
hist_signal.SetMarkerStyle(1)

canvas.Print('signalInAntiIsoArea.png')


f.Close()
f2.Close()

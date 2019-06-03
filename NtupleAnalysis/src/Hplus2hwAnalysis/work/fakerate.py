import ROOT
import array
import sys

f = ROOT.TFile.Open(sys.argv[1], 'read')

f2 = ROOT.TFile.Open(sys.argv[2], 'read')

f3 = ROOT.TFile.Open(sys.argv[3], 'read')

f4 = ROOT.TFile.Open(sys.argv[4], 'read')

#f5 = ROOT.TFile.Open(sys.argv[11], 'read')
f5 = ROOT.TFile.Open(sys.argv[5], 'read')

f6 = ROOT.TFile.Open(sys.argv[6], 'read')

for x in sys.argv:
  print x


pr = "3pr"

hist_num_g_WZ = f.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_num_g_'+pr)
hist_den_g_WZ = f.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_den_g_'+pr)

hist_num_g_ZZ = f2.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_num_g_'+pr)
hist_den_g_ZZ = f2.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_den_g_'+pr)

hist_num_WZ = f.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_num_'+pr)
hist_den_WZ = f.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_den_'+pr)

hist_num_ZZ = f2.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_num_'+pr)
hist_den_ZZ = f2.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_den_'+pr)

hist_num_DY = f3.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_num_'+pr)
hist_den_DY = f3.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_den_'+pr)

hist_mu_DY = f3.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/muPt')
hist_mu_WZ = f.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/muPt')
hist_mu_ZZ = f2.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/muPt')
hist_mu_TT = f4.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/muPt')

hist_jet_DY = f3.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/nJet')
hist_jet_WZ = f.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/nJet')
hist_jet_ZZ = f2.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/nJet')
hist_jet_TT = f4.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/nJet')

hist_num_g_DY = f3.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_num_g_'+pr)
hist_den_g_DY = f3.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_den_g_'+pr)

hist_num_g_TT = f4.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_num_g_'+pr)
hist_den_g_TT = f4.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_den_g_'+pr)

hist_num_TT = f4.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_num_'+pr)
hist_den_TT = f4.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_den_'+pr)

hist_dummy_num_1pr = f6.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_num_'+pr)
hist_dummy_den_1pr = f6.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_den_'+pr)

hist_dummy_mu = f6.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/muPt')

hist_dummy_jet = f6.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/nJet')

hist_num_g_WW = f5.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_num_g_'+pr)
hist_den_g_WW = f5.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_den_g_'+pr)

hist_num_WW = f5.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_num_'+pr)
hist_den_WW = f5.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_den_'+pr)

##############################################
##############################################


ls = 35916.636
#ls = 5746.01+2572.903+4242.292+4024.47+2697.733+406.776
#ls = 7575.824+8434.663+215.965

print ls 

xs_WZ = 47.13
xs_ZZ = 16.523
xs_DY = 1921.8*3.0
xs_TT = 831.76
xs_WW_2l = 12.178

#normalisation factors
norm_WZ = ls*xs_WZ/3000000 #3000000 #1000000

norm_ZZ = ls*xs_ZZ/1000000 #1000000 #990064

norm_DY = ls*xs_DY/49144300

norm_TT = ls*xs_TT/76664700

norm_WW = ls*xs_WW_2l/2000000

#scale histos
hist_num_g_WZ.Scale(norm_WZ)

hist_den_g_WZ.Scale(norm_WZ)

hist_num_g_ZZ.Scale(norm_ZZ)

hist_den_g_ZZ.Scale(norm_ZZ)

hist_num_g_TT.Scale(norm_TT)

hist_den_g_TT.Scale(norm_TT)

hist_num_WZ.Scale(norm_WZ)

hist_den_WZ.Scale(norm_WZ)

hist_num_ZZ.Scale(norm_ZZ)

hist_den_ZZ.Scale(norm_ZZ)

hist_num_WW.Scale(norm_WW)

hist_den_WW.Scale(norm_WW)


#hist_num_DY.Sumw2()

#hist_den_DY.Sumw2()

hist_num_DY.Scale(norm_DY)

hist_den_DY.Scale(norm_DY)

hist_mu_DY.Scale(norm_DY)

hist_mu_WZ.Scale(norm_DY)

hist_mu_ZZ.Scale(norm_DY)

hist_mu_TT.Scale(norm_DY)

hist_jet_DY.Scale(norm_DY)

hist_jet_WZ.Scale(norm_DY)

hist_jet_ZZ.Scale(norm_DY)

hist_jet_TT.Scale(norm_DY)


# add data together

for i in range(7, len(sys.argv)): #10
  f7 = ROOT.TFile.Open(sys.argv[i], 'read')
  hist_num_1pr = f7.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_num_'+pr)
  hist_den_1pr = f7.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/tauPt_den_'+pr)

  hist_mu = f7.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/muPt')
  hist_jet = f7.Get('Hplus2hwAnalysis_fake_350to3000_Run2016/nJet')

  hist_dummy_num_1pr.Add(hist_num_1pr)
  hist_dummy_den_1pr.Add(hist_den_1pr)

  hist_dummy_mu.Add(hist_mu)
  hist_dummy_jet.Add(hist_jet)

  f7.Close()


#add fakes to DY from diboson and TT

#hist_num_DY.Add(hist_num_WZ)
#hist_num_DY.Add(hist_num_ZZ)
hist_num_DY.Add(hist_num_TT)
#hist_num_DY.Add(hist_num_WW)

#hist_den_DY.Add(hist_den_WW)
#hist_den_DY.Add(hist_den_WZ)
#hist_den_DY.Add(hist_den_ZZ)
hist_den_DY.Add(hist_den_TT)


#hist_den_DY.Add(hist_den_g_DY,-1)
#hist_den_DY.Add(hist_den_g_WZ,-1)
#hist_den_DY.Add(hist_den_g_ZZ,-1)
hist_den_DY.Add(hist_den_g_TT,-1)
#hist_den_DY.Add(hist_den_g_WW,-1)

#hist_num_DY.Add(hist_num_g_WW,-1)
#hist_num_DY.Add(hist_num_g_DY,-1)
#hist_num_DY.Add(hist_num_g_WZ,-1)
#hist_num_DY.Add(hist_num_g_ZZ,-1)
hist_num_DY.Add(hist_num_g_TT,-1)

#remove genuine from data using diboson
'''
hist_dummy_num_1pr.Add(hist_num_g_WZ,-1)

hist_dummy_num_1pr.Add(hist_num_g_ZZ,-1)

hist_dummy_num_1pr.Add(hist_num_g_WW,-1)

hist_dummy_den_1pr.Add(hist_den_g_WW,-1)

hist_dummy_den_1pr.Add(hist_den_g_WZ,-1)

hist_dummy_den_1pr.Add(hist_den_g_ZZ,-1)



# what about DY
hist_dummy_num_1pr.Add(hist_num_g_DY,-1)

hist_dummy_den_1pr.Add(hist_den_g_DY,-1)


# what about TT
hist_dummy_num_1pr.Add(hist_num_g_TT,-1)

hist_dummy_den_1pr.Add(hist_den_g_TT,-1)
'''

#add muons from all MC
hist_mu_DY.Add(hist_mu_WZ)
hist_mu_DY.Add(hist_mu_ZZ)
hist_mu_DY.Add(hist_mu_TT)

#add jets
hist_jet_DY.Add(hist_jet_WZ)
hist_jet_DY.Add(hist_jet_ZZ)
hist_jet_DY.Add(hist_jet_TT)

##############################################
##############################################

#plot numerator
canvas_3 = ROOT.TCanvas('canvas_3', '', 500,500)

hist_num_DY.Draw("")
hist_num_DY.SetMarkerStyle(20)
hist_dummy_num_1pr.Draw("Same")

canvas_3.Print('FR/Numerator_DY_data.png')


#plot ratio

#hist_dummy_num_1pr.Divide(hist_dummy_den_1pr)

bins = [20,25,30,35,40,50,60,120]
#bins = [20,40,60,120]

n_data = hist_dummy_num_1pr.Rebin(len(bins)-1,"data_nnew",array.array("d",bins))
d_data = hist_dummy_den_1pr.Rebin(len(bins)-1,"data_dnew",array.array("d",bins))

n_data.Divide(d_data)


#bins = [20,25,30,35,40,50,60,120]
bins = [20,40,60,120]

n = hist_num_DY.Rebin(len(bins)-1,"DY_nnew",array.array("d",bins))
d = hist_den_DY.Rebin(len(bins)-1,"DY_dnew",array.array("d",bins))

n.Divide(d)

canvas = ROOT.TCanvas('canvas', '', 500,500)


n_data.Draw()

n_data.GetXaxis().SetRangeUser(20,180)
n_data.GetYaxis().SetRangeUser(0,0.5)

#hist_num_DY.Divide(hist_den_DY)

#hist_dummy_num_1pr.Draw()

#hist_dummy_num_1pr.GetXaxis().SetRangeUser(20,180)
#hist_dummy_num_1pr.GetYaxis().SetRangeUser(0,0.5)

#hist_num_DY.Draw("Same")
#hist_num_DY.SetMarkerStyle(20)
n.Draw("SAME")
n.SetMarkerStyle(20)

#hist_num_DY.GetXaxis().SetRangeUser(20,140)
#hist_num_DY.GetYaxis().SetRangeUser(0,0.5)

canvas.Print('FR/FR_1pr.png')


#plot denominator
canvas_2 = ROOT.TCanvas('canvas_2', '', 500,500)


hist_den_DY.Draw("")

hist_den_DY.SetMarkerStyle(20)

hist_den_DY.GetYaxis().SetRangeUser(0,26000)

hist_dummy_den_1pr.Draw("Same")

canvas_2.Print('FR/Denominator_DY_data.png')

#plot mu Pt

canvas_4 = ROOT.TCanvas('canvas_4', '', 500,500)

hist_mu_DY.Draw("")

hist_mu_DY.SetMarkerStyle(20)

hist_mu_DY.GetYaxis().SetRangeUser(0,80000)


hist_dummy_mu.Draw("Same")


canvas_4.Print('FR/mu_Pt_DY_data.png')

#plot n jets

canvas_6 = ROOT.TCanvas('canvas_6', '', 500,500)

hist_jet_DY.Draw("")

hist_jet_DY.SetMarkerStyle(20)

hist_jet_DY.GetYaxis().SetRangeUser(0,80000)


hist_dummy_jet.Draw("Same")


canvas_6.Print('FR/Njet_DY_data.png')


f.Close()
f2.Close()
f3.Close()
f4.Close()
f5.Close()
f6.Close()

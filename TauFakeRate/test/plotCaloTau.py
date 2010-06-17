import ROOT

from TauAnalysis.TauIdEfficiency.ntauples.TauNtupleManager import TauNtupleManager
from TauAnalysis.TauIdEfficiency.ntauples.PlotManager import PlotManager

import TauAnalysis.TauIdEfficiency.ntauples.styles as style

# Defintion of input files.
import HiggsAnalysis.TauFakeRate.samples_cache as samples

if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.SetStyle("Plain")


    # Pull out the defintion of the ntuple (this should be improved)
    # Don't ever access this file directly, just use it to parse event content...
#    dummy_file = ROOT.TFile("../data/tauIdEff_ntuple.root")
#    ntuple_manager = TauNtupleManager(dummy_file.Get("Events"), "tauIdEffNtuple")
    ntuple_manager = samples.data.build_ntuple_manager("tauIdEffNtuple")

    # Get the list of collections availabe for our ntuple
    print ntuple_manager

    # Get the shrinking ntuple
    selectedTaus = ntuple_manager.get_ntuple("patCaloTausDijetTagAndProbe")
#        "patPFTausDijetTagAndProbeShrinkingCone")

    # Get list of variables available
    print selectedTaus

    no_selection = selectedTaus.expr('abs($eta) < 2.5')
    my_selection = selectedTaus.expr('abs($eta) < 2.5') & \
                   selectedTaus.expr('$byIsolation > 0.5')

    # Build the plot manager.  The plot manager keeps track of all the samples
    # and ensures they are correctly normalized w.r.t. luminosity.  See 
    # samples.py for available samples.
#    data_sample = samples.data
#    mc_sample = samples.minbias_mc
    data_sample = samples.data_test
    mc_sample = samples.mc_test
   
    plotter = PlotManager()
    # Add each sample we want to plot/compare
    plotter.add_sample(mc_sample, "Minbias MC", **style.MINBIAS_MC_STYLE)
    plotter.add_sample(data_sample, "Data (7 TeV)", **style.DATA_STYLE)
#    plotter.add_sample(samples.qcd_mc, "QCD MC", **style.QCD_MC_STYLE_HIST)

#    plotter.add_sample(mc_sample, "MC", 
#                       fill_color=ROOT.EColor.kBlue-5, draw_option="hist",
#                       line_color=ROOT.EColor.kBlue, fill_style=1)
#
#    plotter.add_sample(data_sample, "Data", marker_size=2,
#                       marker_color=ROOT.EColor.kRed, draw_option="pe")

    # Normalize everything to the data luminosity
    plotter.set_integrated_lumi(data_sample.effective_luminosity())

    # Make some plots
###################################################################################
    canvas = ROOT.TCanvas("canvas_pt", "", 500, 500)

    pt_result = plotter.distribution(
        expression = selectedTaus.expr('$pt'),
        selection  = my_selection,
        binning    = (100, 0, 50),
        x_axis_title = "CaloTau P_{T}[GeV/c]"
    )
    # this should draw a comparison on the canvas, but pt_result
    # now contains some helpful stuff.
    # print "MC average pt: %f" % pt_result['samples']['mc_test']['mean']

    # Add a legend
    pt_result['legend'].make_legend().Draw()
    canvas.SaveAs("caloTau_pt.png")

###################################################################################
    canvas = ROOT.TCanvas("canvas_ptraw", "", 500, 500)
                                                                                             
    ptraw_result = plotter.distribution(
        expression = selectedTaus.expr('$jetPt'),
        selection  = my_selection,
        binning    = (100, 0, 50),
        x_axis_title = "CaloTau P_{T}(raw)[GeV/c]"
    )                                                                                        
    # Add a legend
    ptraw_result['legend'].make_legend().Draw()
    canvas.SaveAs("caloTau_rawpt.png")
  
###################################################################################
    canvas = ROOT.TCanvas("canvas_eta", "", 500, 500)

    eta_result = plotter.distribution(
        expression = selectedTaus.expr('$eta'),
        selection  = selectedTaus.expr('abs($eta) < 5'),
        binning    = (100, -5, 5),
        x_axis_title = "CaloTau eta"
    )
    # Add a legend
    eta_result['legend'].make_legend().Draw()
    canvas.SaveAs("caloTau_eta.png")

###################################################################################                          
    canvas = ROOT.TCanvas("canvas_etaraw", "", 500, 500)

    etaraw_result = plotter.distribution(                                                                  
        expression = selectedTaus.expr('$jetEta'),
        selection  = selectedTaus.expr('abs($jetEta) < 5'),
        binning    = (100, -5, 5),
        x_axis_title = "CaloTau eta(raw)"
    )
    # Add a legend
    etaraw_result['legend'].make_legend().Draw()
    canvas.SaveAs("caloTau_raweta.png") 

###################################################################################

    canvas = ROOT.TCanvas("canvas_phi", "", 500, 500)                       

    phi_result = plotter.distribution(
        expression = selectedTaus.expr('$phi'),
	selection  = my_selection,
        binning    = (100, -3.5, 3.5),
        x_axis_title = "CaloTau phi"
    )
    # Add a legend
    phi_result['legend'].make_legend().Draw()
    canvas.SaveAs("caloTau_phi.png")
###################################################################################                          
                                                                                                             
    canvas = ROOT.TCanvas("canvas_phiraw", "", 500, 500)

    phiraw_result = plotter.distribution(
        expression = selectedTaus.expr('$jetPhi'),
        selection  = my_selection,
        binning    = (100, -3.5, 3.5),
        x_axis_title = "CaloTau phi(raw)"
    )
    # Add a legend
    phiraw_result['legend'].make_legend().Draw()
    canvas.SaveAs("caloTau_rawphi.png")
    
###################################################################################

    canvas = ROOT.TCanvas("canvas_ltrackpt", "", 500, 500)

    ltpt_result = plotter.distribution(
        expression = selectedTaus.expr('$leadTrackPt'),
        selection  = my_selection,
        binning    = (100, 0, 50),
        x_axis_title = "leading track pt [GeV/c]"
    )
    # Add a legend
    ltpt_result['legend'].make_legend().Draw()
    canvas.SaveAs("caloTau_ltrack_pt.png")

###################################################################################

    canvas = ROOT.TCanvas("canvas_nSignalTracks", "", 500, 500)
    canvas.SetLogy()

    nSignalTr_result = plotter.distribution(
        expression = selectedTaus.expr('$numSignalTracks'),
        selection  = no_selection,
        binning    = (10, 0, 10),
        x_axis_title = "Tracks in signal cone"
    )
    # Add a legend
    nSignalTr_result['legend'].make_legend().Draw()
    canvas.SaveAs("caloTau_nSignalTracks.png")
        

###################################################################################

    canvas = ROOT.TCanvas("canvas_nIsolationTracks", "", 500, 500)
    canvas.SetLogy()
    
    nIsolTr_result = plotter.distribution(
        expression = selectedTaus.expr('$numIsolationTracks'),
        selection  = no_selection,
        binning    = (25, 0, 25),
        x_axis_title = "Tracks in isolation cone"
    )
    # Add a legend
    nIsolTr_result['legend'].make_legend().Draw()
    canvas.SaveAs("caloTau_nIsolationTracks.png")

###################################################################################

    canvas = ROOT.TCanvas("canvas_nIsolationTracksPtSum", "", 500, 500)
    canvas.SetLogy()
        
    nIsolTrPtSum_result = plotter.distribution(
        expression = selectedTaus.expr('$ptSumIsolationTracks'),
        selection  = no_selection,
        binning    = (100, 0, 50),
        x_axis_title = "#Sigma P_T of tracks in isolation cone [GeV/c]"
    )
    # Add a legend
    nIsolTrPtSum_result['legend'].make_legend().Draw()
    canvas.SaveAs("caloTau_nIsolationTracksPtSum.png")

###################################################################################

    canvas = ROOT.TCanvas("canvas_nIsolationEcalEtSum", "", 500, 500)
    canvas.SetLogy()
        
    nIsolEcalEtSum_result = plotter.distribution(
        expression = selectedTaus.expr('$etSumIsolationECAL'),
        selection  = no_selection,
        binning    = (100, 0, 50),
        x_axis_title = "#Sigma ECAL Isolation E_T [GeV]"
    )
    # Add a legend
    nIsolEcalEtSum_result['legend'].make_legend().Draw()
    canvas.SaveAs("caloTau_nIsolationEcalEtSum.png")

###################################################################################                                           

    denominator = selectedTaus.expr('abs($jetEta) < 2.5 & $jetPt > 5')
    numerator_byLeadTrackFinding = selectedTaus.expr('$byLeadTrackFinding') & denominator
    numerator_byLeadTrackPtCut   = selectedTaus.expr('$byLeadTrackPtCut') & denominator
    numerator_byIsolation        = selectedTaus.expr('$byIsolation') & denominator
    numerator_againstElectron    = selectedTaus.expr('$againstElectron') & denominator

    canvas = ROOT.TCanvas("canvas_pt_eff_result", "", 500, 500)

    pt_eff_result = plotter.efficiency(
        expression=selectedTaus.expr('$pt'),
        denominator = denominator,
        numerator = numerator_byLeadTrackFinding,
        binning = (20, 0, 100),
        x_axis_title = "Tau P_{T} [GeV/c]",
        y_min = 1e-4, y_max = 5, logy = True,
    )

    # Add a legend
    pt_eff_result['legend'].make_legend().Draw()

    canvas.SaveAs("caloTau_discr_eff_pt.png")


    canvas = ROOT.TCanvas("canvas_eta_eff_result", "", 500, 500)

    eta_eff_result = plotter.efficiency(
        expression=selectedTaus.expr('abs($jetEta)'),
        denominator = denominator,
        numerator = numerator_byLeadTrackFinding,
        binning = (25, 0, 2.5),
        x_axis_title = "Tau |#eta|",
        y_min = 1e-4, y_max = 5, logy = True,  
    )

    # Add a legend
    eta_eff_result['legend'].make_legend().Draw()

    canvas.SaveAs("caloTau_discr_eff_eta.png")


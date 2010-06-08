import ROOT

from TauAnalysis.TauIdEfficiency.ntauples.TauNtupleManager \
        import TauNtupleManager
from TauAnalysis.TauIdEfficiency.ntauples.PlotManager \
        import PlotManager

# Defintion of input files.
import HiggsAnalysis.TauFakeRate.samples as samples

if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.SetStyle("Plain")

    # Pull out the defintion of the ntuple (this should be improved)
    # Don't ever access this file directly, just use it to parse event content...
    dummy_file = ROOT.TFile("../data/tauIdEff_ntuple.root")
    ntuple_manager = TauNtupleManager(dummy_file.Get("Events"), "tauIdEffNtuple")

    # Get the shrinking ntuple
    selectedTaus = ntuple_manager.get_ntuple(
        "patPFTausDijetTagAndProbeShrinkingCone")

    # Build the plot manager.  The plot manager keeps track of all the samples
    # and ensures they are correctly normalized w.r.t. luminosity.  See 
    # samples.py for available samples.
    data_sample = samples.data_test2
    mc_sample = samples.mc_test
   
    plotter = PlotManager()
    # Add each sample we want to plot/compare
    plotter.add_sample(mc_sample, "MC", 
                       fill_color=ROOT.EColor.kBlue-5, draw_option="hist",
                       line_color=ROOT.EColor.kBlue, fill_style=1)

    plotter.add_sample(data_sample, "Data", marker_size=2,
                       marker_color=ROOT.EColor.kRed, draw_option="pe")

    # Normalize everything to the data luminosity
    plotter.set_integrated_lumi(data_sample.effective_luminosity())

    # Make some plots
###################################################################################
    canvas_pt = ROOT.TCanvas("canvas_pt", "", 500, 500)

    pt_result = plotter.distribution(
        expression=selectedTaus.expr('$pt'),
        selection=selectedTaus.expr('abs($eta) < 10'),
        binning = (100, 0, 50),
        x_axis_title = "P_{T}"
    )
    # this should draw a comparison on the canvas, but pt_result
    # now contains some helpful stuff.
    print "MC average pt: %f" % \
            pt_result['samples']['mc_test']['mean']

    canvas_pt.SaveAs("caloTau_pt.png")

###################################################################################

    canvas_eta = ROOT.TCanvas("canvas_eta", "", 500, 500)

    eta_result = plotter.distribution(
        expression=selectedTaus.expr('$eta'),
        selection=selectedTaus.expr('abs($eta) < 5'),
        binning = (100, -5, 5),
        x_axis_title = "eta"
#        expression=selectedTaus.expr('$eta'),
#        selection=selectedTaus.expr('$pt > 5.0'),
#        binning = (100, -5, 5),
#        x_axis_title = "#eta"
    )
    canvas_eta.SaveAs("caloTau_eta.png")

###################################################################################

#    phi_result = plotter.distribution(
#        expression=selectedTaus.expr('$phi'),
#	selection=selectedTaus.expr('abs($eta) < 2.5'),
#        binning = (100, -5, 5),
#        x_axis_title = "phi"
#    )
#    canvas.SaveAs("caloTau_phi.C")


#    denominator = selectedTaus.expr('abs($eta) < 2.5 & $pt > 5')
#    numerator = selectedTaus.expr('$byTaNCfrHalfPercent') & denominator
#
#    pt_eff_result = plotter.efficiency(
#        expression=selectedTaus.expr('$pt'),
#        denominator = denominator,
#        numerator = numerator,
#        binning = (10, 0, 50),
#        x_axis_title = "P_{T}"
#    )
#
#    # Add a legend
#    pt_eff_result['legend'].make_legend().Draw()
#
#    canvas.SaveAs("test_pt_eff.png")
#

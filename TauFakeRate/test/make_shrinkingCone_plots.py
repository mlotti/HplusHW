import ROOT

from TauAnalysis.TauIdEfficiency.ntauples.PlotManager import PlotManager
import TauAnalysis.TauIdEfficiency.ntauples.styles as style

# Defintion of input files.
import samples_cache as samples
import os
import sys

if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)

    if not os.path.isdir('plots'):
        os.mkdir('plots')

    # Build the plot manager.  The plot manager keeps track of all the samples
    # and ensures they are correctly normalized w.r.t. luminosity.  See 
    # samples.py for available samples.
    plotter = PlotManager()

    # Add each sample we want to plot/compare
    # Uncomment to add QCD
    plotter.add_sample(samples.qcd_mc, "QCD MC", **style.QCD_MC_STYLE_HIST)

    plotter.add_sample(samples.minbias_mc, "Minbias MC", **style.MINBIAS_MC_STYLE)

    plotter.add_sample(samples.data, "Data (7 TeV)", **style.DATA_STYLE)


    # Normalize everything to the data luminosity
    plotter.set_integrated_lumi(samples.data.effective_luminosity())

    # Build the ntuple maanger
    ntuple_manager = samples.data.build_ntuple_manager("tauIdEffNtuple")

    # Get the shrinking ntuple
    shrinking_ntuple = ntuple_manager.get_ntuple(
        "patPFTausDijetTagAndProbeShrinkingCone")

    hlt = ntuple_manager.get_ntuple("TriggerResults")

    # Make some plots
    canvas = ROOT.TCanvas("blah", "blah", 500, 500)

    # Plot # different triggers
    trigger_results_expr =  hlt.expr('$hltJet15U')

    trigger_results = plotter.distribution(
        expression=hlt.expr('$hltJet15U'),
        selection=hlt.expr('1'), # no selection
        binning = (5, -2.5, 2.5),
        x_axis_title = "HLT_Jet15U Result",
        y_min = 1, logy=True,
        # Can pass a list of TPaveTexts to draw on the plot
        # CMS preliminary in the upper left is the default
        #labels = [styles.CMS_PRELIMINARY_UPPER_LEFT]  
    )

    trigger_results['legend'].make_legend().Draw()

    canvas.SaveAs("plots/hltJet15U_result.png")
    canvas.SaveAs("plots/hltJet15U_result.pdf")

    # Basic requirement HLT + Probe object
    # N.B. currently disabled, no HLT info in ntuples!
    # base_selection = shrinking_ntuple.expr('$probe > 0.5') & hlt.expr('$hltJet15U > 0.5')
    base_selection = shrinking_ntuple.expr('1')

    # Compare basic distributions
    jetpt_result = plotter.distribution(
        expression=shrinking_ntuple.expr('$jetPt'),
        selection=shrinking_ntuple.expr('abs($jetEta) < 2.5') & base_selection,
        binning = (50, 0, 100),
        x_axis_title = "Jet P_{T} [GeV/c]",
        y_min = 1e-2, logy=True
    )

    # Draw the legend - you can pass NDC xl, yl, xh, yh coords to make_legend(...)
    jetpt_result['legend'].make_legend().Draw()

    canvas.SaveAs("plots/shrinkingCone_jetPt.png")
    canvas.SaveAs("plots/shrinkingCone_jetPt.pdf")

    jeteta_result = plotter.distribution(
        expression=shrinking_ntuple.expr('$jetEta'),
        selection=shrinking_ntuple.expr('abs($jetPt) > 5') & base_selection,
        binning = (50, -2.5, 2.5),
        x_axis_title = "Jet #eta"
    )
    jeteta_result['legend'].make_legend().Draw()

    canvas.SaveAs("plots/shrinkingCone_jetEta.png")
    canvas.SaveAs("plots/shrinkingCone_jetEta.pdf")

    jeteta_result = plotter.distribution(
        expression=shrinking_ntuple.expr('$jetPhi'),
        selection=shrinking_ntuple.expr('abs($jetPt) > 5') & base_selection,
        binning = (50, -3.14, 3.14),
        x_axis_title = "Jet #phi"
    )
    jeteta_result['legend'].make_legend().Draw()

    canvas.SaveAs("plots/shrinkingCone_jetPhi.png")
    canvas.SaveAs("plots/shrinkingCone_jetPhi.pdf")


    ######################################################
    ####      Plot efficiencies                       ####
    ######################################################

    # Change the style of the QCD from filled histogram to dots
    # name mc_qcd is defined in samples.py
    plotter.update_style("mc_qcd", **style.QCD_MC_STYLE_DOTS)



    denominator = shrinking_ntuple.expr(
        'abs($jetEta) < 2.5 & $jetPt > 5') & base_selection
    numerator = shrinking_ntuple.expr('$byTaNCfrHalfPercent') & denominator

    eta_eff_result = plotter.efficiency(
        expression=shrinking_ntuple.expr('abs($jetEta)'),
        denominator = denominator,
        numerator = numerator,
        binning = (25, 0, 2.5),
        x_axis_title = "Jet |#eta|",
        y_min = 1e-4, y_max = 5, logy = True,
    )

    # Add a legend
    eta_eff_result['legend'].make_legend().Draw()

    canvas.SaveAs("plots/shrinkingCone_TaNCHalf_eff_jetEta.png")
    canvas.SaveAs("plots/shrinkingCone_TaNCHalf_eff_jetEta.pdf")

    pt_eff_result = plotter.efficiency(
        expression=shrinking_ntuple.expr('$jetPt'),
        denominator = denominator,
        numerator = numerator,
        binning = (20, 0, 100),
        x_axis_title = "Jet P_{T} [GeV/c]",
        y_min = 1e-4, y_max = 5, logy = True,
    )

    # Add a legend
    pt_eff_result['legend'].make_legend().Draw()

    canvas.SaveAs("plots/shrinkingCone_TaNCHalf_eff_jetPt.png")
    canvas.SaveAs("plots/shrinkingCone_TaNCHalf_eff_jetPt.pdf")


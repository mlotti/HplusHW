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
    ntuple_manager = samples.ztautau_mc.build_ntuple_manager("tauIdEffNtuple")

    # Get the list of collections availabe for our ntuple
    print ntuple_manager

    # Get the shrinking ntuple
    selectedTaus = ntuple_manager.get_ntuple("patCaloTausDijetTagAndProbe")
#        "patPFTausDijetTagAndProbeShrinkingCone")

    # Get list of variables available
    print selectedTaus

    hlt = ntuple_manager.get_ntuple("TriggerResults")
    gen = ntuple_manager.get_ntuple("iterativeCone5GenJets")

    base_selection = selectedTaus.expr('$probe > 0.5') & hlt.expr('$hltJet15U > 0.5')
    eta_selection  = base_selection & selectedTaus.expr('abs($eta) < 2.5')
    my_selection   = eta_selection & selectedTaus.expr('$byIsolation > 0.5')

    # Build the plot manager.  The plot manager keeps track of all the samples
    # and ensures they are correctly normalized w.r.t. luminosity.  See 
    # samples.py for available samples.
    data_sample = samples.data
    mc_sample = samples.minbias_mc
#    data_sample = samples.data_test
#    mc_sample = samples.mc_test
   
    plotter = PlotManager()
    # Add each sample we want to plot/compare
#    plotter.add_sample(mc_sample, "Minbias MC", **style.MINBIAS_MC_STYLE)
#    plotter.add_sample(data_sample, "Data (7 TeV)", **style.DATA_STYLE)
#    plotter.add_sample(samples.qcd_mc, "QCD MC", **style.QCD_MC_STYLE_HIST)
    plotter.add_sample(samples.ztautau_mc, "Ztautau MC", **style.QCD_MC_STYLE_HIST)

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
        expression = selectedTaus.expr('$pt')/gen.expr('$genPt') - 1,
#	expression = gen.expr('$genPt'),
        selection  = my_selection & gen.expr('$genPt > 0'),
        binning    = (100, -5, 5),
        x_axis_title = "CaloTau P_{T}[GeV/c]"
    )
    # this should draw a comparison on the canvas, but pt_result
    # now contains some helpful stuff.
    # print "MC average pt: %f" % pt_result['samples']['mc_test']['mean']

    # Add a legend
    pt_result['legend'].make_legend().Draw()
    canvas.SaveAs("caloTau_ptRes_TCTau.png")

###################################################################################                    
    canvas = ROOT.TCanvas("canvas_pt", "", 500, 500)                                                   
                                                                                                       
    pt_result = plotter.distribution(                                                                  
        expression = selectedTaus.expr('$jetPt')/gen.expr('$genPt') - 1,                                  
        selection  = my_selection & gen.expr('$genPt > 0'),                                            
        binning    = (100, -5, 5),                                                                     
        x_axis_title = "CaloTau P_{T}[GeV/c]"                                                          
    )                                                                                                  
    # this should draw a comparison on the canvas, but pt_result                                       
    # now contains some helpful stuff.                                                                 
    # print "MC average pt: %f" % pt_result['samples']['mc_test']['mean']                              
                                                                                                       
    # Add a legend                                                                                     
    pt_result['legend'].make_legend().Draw()                                                           
    canvas.SaveAs("caloTau_ptRes_JPTTau.png")

###################################################################################                    
    canvas = ROOT.TCanvas("canvas_pt", "", 500, 500)                                                   
                                                                                                       
    pt_result = plotter.distribution(                                                                  
        expression = selectedTaus.expr('$caloJetPt')/gen.expr('$genPt') - 1,                                  
        selection  = my_selection & gen.expr('$genPt > 0'),                                            
        binning    = (100, -5, 5),                                                                     
        x_axis_title = "CaloTau P_{T}[GeV/c]"                                                          
    )                                                                                                  
    # this should draw a comparison on the canvas, but pt_result                                       
    # now contains some helpful stuff.                                                                 
    # print "MC average pt: %f" % pt_result['samples']['mc_test']['mean']                              
                                                                                                       
    # Add a legend                                                                                     
    pt_result['legend'].make_legend().Draw()                                                           
    canvas.SaveAs("caloTau_ptRes_CaloTau.png")

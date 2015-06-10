#!/usr/bin/env python

# Script for plotting generator comparison results
# Example usage: ./plotGeneratorComparison.py light 13

###########################################################################
#
# This script is only intended as an example, please do NOT modify it.
# For example, start from scratch and look here for help, or make a
# copy of it and modify the copy (including removing all unnecessary
# code).
#
###########################################################################

import re
import ROOT
import sys

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

ROOT.gROOT.SetBatch(True)

def main(argv):
    if len(sys.argv) < 3:
        raise Exception("Specify mass range and CM energy as command line parameters")
    if sys.argv[1] not in ["light","heavy"]:
        raise Exception("Invalid mass range command line parameter")
    
    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Construct datasets as stated in the multicrab.cfg of the execution
    # directory. The returned object is of type DatasetManager.

    massrange = sys.argv[1]
    energy = sys.argv[2]
    if massrange == "light":
        datasets = dataset.getDatasetsFromMulticrabCfg(directory = '../../../work/generatorComparison_150526_203239')
    if massrange == "heavy":
        datasets = dataset.getDatasetsFromMulticrabCfg(directory = '../../../work/FINAL2/8T/heavy/generatorComparison_150606_132341')

    datasetlist = datasets.getMCDatasets()
    
    qlist_particle = ["Pt","Phi","Eta"]
    qlist_met = ["Et","Phi"]
    qlist_b = ["Pt","Eta"] 
    if massrange == "light":
        objects = {"Hplus/associatedB" : qlist_particle, "Hplus/hplus" : qlist_particle, "Hplus/associatedT" : qlist_particle, "Hplus/associatedSecondaryT" : qlist_particle, "Hplus/associatedTau" : qlist_particle, "Hplus/associatedOneProngTau" : qlist_particle, "met" : qlist_met}
    if massrange == "heavy":
        objects = {"Hplus/associatedB" : qlist_particle, "Hplus/associatedSecondaryB" : qlist_b, "Hplus/hplus" : qlist_particle, "Hplus/associatedT" : qlist_particle, "Hplus/associatedTau" : qlist_particle, "Hplus/associatedOneProngTau" : qlist_particle, "met" : qlist_met} 
    
    colorlist = [1,2,4,5]
    print "These objects are considered: ", objects.keys()

    object_dict={"met" : "Gen MET", "associatedB" : "associated b", "associatedT" : "associated t","associatedSecondaryB" : "b (from associated t decay)", "associatedSecondaryT" : "t (from t#bar{t}, t#rightarrow bW)",  "hplus" : "H^{#pm}", "associatedTau" : "associated #tau", "associatedOneProngTau" : "associated 1-prong #tau"}
    quantity_dict={'Et' : '(GeV)', "Pt" : "p_{T} (GeV)", "Phi" : "#phi", "Eta" : "#eta"}
    gen_dict = {'PYTHIA6' : 'Pythia 6 (LO)', 'PYTHIA8' : 'Pythia 8', '2HDMII' : 'MG 2HDM type II', '2HDMtypeII' : 'MG 2HDM type II', 'MSSM' :'MG5_aMC@NLO MSSM', 'LowTanb' : 'Low tan#beta', '2HDMtypeII_LO' : 'MG5_aMC@NLO (LO)', '2HDMtypeII_NLO' : 'MG5_aMC@NLO (NLO)'} 

    for obj in objects.keys():
        for quantity in objects[obj]:
            HISTONAME = obj + quantity
            histos = [] 
            for i in range(0,len(datasetlist)):
                name = datasetlist[i].getName()
                histotuple = datasetlist[i].getRootHisto(HISTONAME)
                histo = histotuple[0].Clone()
                if len(datasetlist) > 1:
                    histo.Scale(1/histo.Integral())
                histo.SetLineColor(colorlist[i])
                histo.SetName(gen_dict[name])
                histos.append(histo)

            myParams = {}

            if len(obj.split("/")) > 1:
                obj_name = obj.split("/")[1]
            else:
                obj_name = obj

            xmin = None
            xmax = None
            if quantity == "Phi":
                myParams["moveLegend"] = {"dx": -0.25, "dy": -0.2, "dh": -0.1}
                ymin = 0
                ymax = 0.012
            elif quantity == "Eta":
                myParams["moveLegend"] = {"dx": -0.25, "dy": 0.0, "dh": -0.1}
                myParams["log"] = True
                xmin = -2.5
                xmax = 2.5
                ymin = 0.005
                ymax = 0.05
                if massrange == "heavy":
                    if "associatedB" in obj_name:
                        xmin = -4.0
                        xmax = 4.0
                        ymax = 0.02                        
            else:
                myParams["moveLegend"] = {"dx": -0.25, "dy": 0.0, "dh": -0.1}
                myParams["log"] = True 
                ymin = 0.00005
                ymax = 0.5
                if obj_name == "associatedB":
                    ymin = ymin/5
                if  massrange == "heavy":
                    ymin = ymin*10

            if len(histos) > 1:
                myParams["ratio"] = True
                myParams["opts2"] = {"ymin": 0.0, "ymax":2.0}
                myParams["ylabel"] = "#LT Events / bin #GT, normalized"
                if xmin and xmax:
                    myParams["opts"] = {"xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax}
                else:
                    myParams["opts"] = {"ymin": ymin, "ymax": ymax}
            else: 
                myParams["ylabel"] = "#LT Events / bin #GT"

            myParams["xlabel"] = object_dict[obj_name]+" "+quantity_dict[quantity]

            if len(histos) <= 1:
                plot = plots.PlotBase(histos)
            else:
                default = histos[0]
                compared = histos[1:]
                plot = plots.ComparisonManyPlot(default, compared)
            
            plot.setEnergy(energy)
            tb = histograms.PlotTextBox(xmin=0.75, ymin=None, xmax=0.85, ymax=0.1, size=25, lineheight=0.035)
            if massrange == "light":
                tb.addText("Light H^{+}")
            if massrange == "heavy":
                tb.addText("Heavy H^{+}")
            plot.appendPlotObject(tb)

            histograms.createLegend.setDefaults(textSize = 0.045)

            def customYTitleOffset(p):
                if quantity != "Pt":
                    scale = 1.2
                else:
                    scale = 1
                yaxis = p.getFrame().GetYaxis()                                          
                yaxis.SetTitleOffset(scale*yaxis.GetTitleOffset())

            if len(histos) > 1:
                myParams["customise"] = customYTitleOffset

            plots.drawPlot(plot, obj_name+quantity, **myParams)

if __name__ == "__main__":
    main(sys.argv)

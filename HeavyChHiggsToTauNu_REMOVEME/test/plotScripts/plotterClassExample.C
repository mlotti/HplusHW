//#######################################################################
// -*- ROOT macro-*-
//
// Original Author:  Alexandros Attikis
//         Created:  9 Feb 2010
//       Institute:  UCY
//         e-mail :  attikis@cern.ch
//#######################################################################

{

#include "MyPlotterClass.C"

  /// Declarations
  MyPlotter plotter;
  HPlusStyle(); // TDRStyle();
  
  vector<TString> DatasetsToAdd;
  /// TauData
  DatasetsToAdd.push_back("JetMETTau_Tau_136035-139975_Dec22");
  DatasetsToAdd.push_back("JetMETTau_Tau_140058-141881_Dec22");
  DatasetsToAdd.push_back("BTau_141956-144114_Dec22");
  DatasetsToAdd.push_back("BTau_146428-148058_Dec22");
  DatasetsToAdd.push_back("BTau_148822-149182_Dec22");
  /// MC
  DatasetsToAdd.push_back("QCD");
  DatasetsToAdd.push_back("QCD_Pt30to50");
  DatasetsToAdd.push_back("QCD_Pt50to80");
  DatasetsToAdd.push_back("QCD_Pt80to120");
  DatasetsToAdd.push_back("QCD_Pt120to170");
  DatasetsToAdd.push_back("QCD_Pt170to300");
  DatasetsToAdd.push_back("QCD_Pt300to470");
  DatasetsToAdd.push_back("TTJets");
  DatasetsToAdd.push_back("WJets");

  //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  /// Plotting Options
  //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  /// histos
  const char* multicrab = "~/w0/multicrab_110209_164700/";
  const char* histo       = "signalAnalysisTauSelectionHPSTauBased/TauCand_JetEta";

  plotter.InitializeOnce();
  plotter.AddDatasets(DatasetsToAdd);
  plotter.Initialize("TuneZ2", multicrab, "signalAnalysis", histo); // Tune6DT
  // plotter.SetCustomLumi(36.0);
  plotter.TransparentHistos();
  plotter.Draw("h");
  plotter.CustomizeHisto(10, 1e6, "none", "Events", true);
  plotter.AddHistoLegends("afterTrigger", 0.65, 0.6, 0.85, 0.8); // "none" for no title space
  
}

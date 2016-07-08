//#######################################################################
// -*- C++ -*-
//       File Name:  MyPlotterClass.C
// Original Author:  Alexandros Attikis
//         Created:  09 Feb 2011
//     Description:  Common functions used for TH1
//       Institute:  UCY
//         e-mail :  attikis@cern.ch
//        Comments:  
//#######################################################################

#include "MyPlotterClass.h"

void MyPlotter::InitializeOnce(void){

  /// Initialize variables
  IntegratedLumi = -1.0;
  SuperimposeCounter  = 0;
  CanvasCounter  = 0;
  ColourCounter  = 0;
  GlobalMarkerSize = 1.2;
  x1Leg = 0.65;
  y1Leg = 0.2;
  x2Leg = 0.85;
  y2Leg = 0.4;
  xLegLength = x2Leg-x1Leg;
  yLegLength = y2Leg-y1Leg;  
  TotalTauDataHistoLumi = 0.0;
  TotalJetDataHistoLumi = 0.0;
  bTransparentHistos  = false;
  bEnableHistoMarkers = false;
  GlobalFolder = "";
  InitVariables();
  // InitHistos();
}


void MyPlotter::Initialize(const TString tune, const char* multicrab_dir, const char* folder, const char *histo){

  InitHistos();
  TotalJetDataHistoLumi = 0.0;
  TotalTauDataHistoLumi = 0.0;
  GlobalFolder = folder;
  // histoName = TString(GlobalFolder) + "Counters/counter";
  histoName     = TString(histo);
  fullHistoName = TString(GlobalFolder) + "/" + TString(histo);
  MC_Tune = tune;  
  GetRootFiles(multicrab_dir);
  GetMCXsections();
  GetMCWeights();
  GetHistos(histo);
  // GetHistos(fullHistoName);
}



void MyPlotter::InitVariables(void){

  /// xSections
  TTToHplusBWB_M90_Xsection  = -1.0;
  TTToHplusBWB_M100_Xsection = -1.0;
  TTToHplusBWB_M120_Xsection = -1.0;
  TTToHplusBWB_M140_Xsection = -1.0;
  TTToHplusBWB_M160_Xsection = -1.0;
  QCD_Pt30to50_Xsection   = -1.0;
  QCD_Pt50to80_Xsection   = -1.0;
  QCD_Pt80to120_Xsection  = -1.0;
  QCD_Pt120to170_Xsection = -1.0;
  QCD_Pt170to300_Xsection = -1.0;
  QCD_Pt300to470_Xsection = -1.0;
  TTJets_Xsection = -1.0;
  WJets_Xsection = -1.0;
  WJets_noPU_Xsection = -1.0;

  /// AllEvents
  TTToHplusBWB_M90_AllEvents  = -1.0;
  TTToHplusBWB_M100_AllEvents = -1.0;
  TTToHplusBWB_M120_AllEvents = -1.0;
  TTToHplusBWB_M140_AllEvents = -1.0;
  TTToHplusBWB_M160_AllEvents = -1.0;
  QCD_Pt30to50_AllEvents   = -1.0;
  QCD_Pt50to80_AllEvents   = -1.0;
  QCD_Pt80to120_AllEvents  = -1.0;
  QCD_Pt120to170_AllEvents = -1.0;
  QCD_Pt170to300_AllEvents = -1.0;
  QCD_Pt300to470_AllEvents = -1.0;
  TTJets_AllEvents = -1.0;
  WJets_AllEvents = -1.0;
  WJets_noPU_AllEvents = -1.0;
  
  /// JetData
  bJetMETTau_Jet_136035_141881_Dec22_TFile = false;
  bJetMET_141956_144114_Dec22_TFile = false;
  bJet_146428_148058_Dec22_TFile = false;
  bJet_148822_149294_Dec22_TFile = false;
  /// TauData
  bJetMETTau_Tau_140058_141881_Dec22_TFile = false;
  bJetMETTau_Tau_136035_139975_Dec22_TFile = false;
  bBTau_141956_144114_Dec22_TFile = false;
  bBTau_146428_148058_Dec22_TFile = false;
  bBTau_148822_149182_Dec22_TFile = false;
  /// MC
  bTTToHplusBWB_M90_TFile = false;
  bTTToHplusBWB_M100_TFile = false;
  bTTToHplusBWB_M120_TFile = false;
  bTTToHplusBWB_M140_TFile = false;
  bTTToHplusBWB_M160_TFile = false;
  bQCD_Pt30to50_TFile = false;
  bQCD_Pt50to80_TFile = false;
  bQCD_Pt80to120_TFile = false;
  bQCD_Pt120to170_TFile = false;
  bQCD_Pt170to300_TFile = false;
  bQCD_Pt300to470_TFile = false;
  bTTJets_TFile = false;
  bWJets_TFile = false;
  bWJets_noPU_TFile = false;
  bQCD_TFile = false;
  
  /// JetData
  bJetData = false;
  bJetMETTau_Jet_136035_141881_Dec22 = false;
  bJetMET_141956_144114_Dec22 = false;
  bJet_146428_148058_Dec22 = false;
  bJet_148822_149294_Dec22 = false;
  /// TauData
  bTauData = false;
  bBTau = false;
  bJetMETTau = false;
  bJetMETTau_Tau_140058_141881_Dec22 = false;
  bJetMETTau_Tau_136035_139975_Dec22 = false;
  bBTau_141956_144114_Dec22 = false;
  bBTau_146428_148058_Dec22 = false;
  bBTau_148822_149182_Dec22 = false;
  /// MC
  bMC = false;
  bTTToHplusBWB_M90 = false;
  bTTToHplusBWB_M100 = false;
  bTTToHplusBWB_M120 = false;
  bTTToHplusBWB_M140 = false;
  bTTToHplusBWB_M160 = false;
  bQCD_Pt30to50 = false;
  bQCD_Pt50to80 = false;
  bQCD_Pt80to120 = false;
  bQCD_Pt120to170 = false;
  bQCD_Pt170to300 = false;
  bQCD_Pt300to470 = false;
  bTTJets = false;
  bWJets = false;
  bWJets_noPU = false;
  bQCD = false;
  bOverwriteIntegratedLumi = false;
}



void MyPlotter::InitHistos(void){

  // THStacks
  TauData_THStack = new THStack;
  JetData_THStack = new THStack;
  Bkg_THStack = new THStack;
  MC_THStack = new THStack;

  /// JetData
  JetData_TH1D = new TH1D;
  JetMETTau_Jet_136035_141881_Dec22_TH1D = new TH1D;
  JetMET_141956_144114_Dec22_TH1D = new TH1D;
  Jet_146428_148058_Dec22_TH1D = new TH1D;
  Jet_148822_149294_Dec22_TH1D = new TH1D;
  
  /// TauData
  TauData_TH1D = new TH1D;
  JetMETTau_Tau_140058_141881_Dec22_TH1D = new TH1D;
  JetMETTau_Tau_136035_139975_Dec22_TH1D = new TH1D;
  BTau_141956_144114_Dec22_TH1D = new TH1D;
  BTau_146428_148058_Dec22_TH1D = new TH1D;
  BTau_148822_149182_Dec22_TH1D = new TH1D;
  /// MC
  TTToHplusBWB_M90_TH1D  = new TH1D;
  TTToHplusBWB_M100_TH1D = new TH1D;
  TTToHplusBWB_M120_TH1D = new TH1D;
  TTToHplusBWB_M140_TH1D = new TH1D;
  TTToHplusBWB_M160_TH1D = new TH1D;
  QCD_Pt30to50_TH1D   = new TH1D;
  QCD_Pt50to80_TH1D   = new TH1D;
  QCD_Pt80to120_TH1D  = new TH1D;
  QCD_Pt120to170_TH1D = new TH1D;
  QCD_Pt170to300_TH1D = new TH1D;
  QCD_Pt300to470_TH1D = new TH1D;
  TTJets_TH1D         = new TH1D;
  WJets_TH1D          = new TH1D;
  WJets_noPU_TH1D     = new TH1D;
  BTau_TH1D           = new TH1D;
  JetMETTau_TH1D      = new TH1D;

  dumbieHisto = new TH1D;

}




void MyPlotter::ActivateAllDataAndMC(void){

  /// JetData
  bJetMETTau_Jet_136035_141881_Dec22 = true;
  bJetMET_141956_144114_Dec22 = true;
  bJet_146428_148058_Dec22 = true;
  bJet_148822_149294_Dec22 = true;
  /// TauData
  bJetMETTau_Tau_136035_139975_Dec22 = true;
  bJetMETTau_Tau_140058_141881_Dec22 = true;
  bBTau_141956_144114_Dec22 = true;
  bBTau_146428_148058_Dec22 = true;
  bBTau_148822_149182_Dec22 = true;
  /// MC 
  bTTToHplusBWB_M90 = true;
  bTTToHplusBWB_M100 = true;
  bTTToHplusBWB_M120 = true;
  bTTToHplusBWB_M140 = true;
  bTTToHplusBWB_M160 = true;
  bQCD = true;
  bQCD_Pt30to50 = true;
  bQCD_Pt50to80 = true;
  bQCD_Pt80to120 = true;
  bQCD_Pt120to170 = true;
  bQCD_Pt170to300 = true;
  bQCD_Pt300to470 = true;
  bTTJets = true;
  bWJets = true;
  bWJets_noPU = false;
}


void MyPlotter::ActivateAllData(void){

  /// JetData
  bJetMETTau_Jet_136035_141881_Dec22 = true;
  bJetMET_141956_144114_Dec22 = true;
  bJet_146428_148058_Dec22 = true;
  bJet_148822_149294_Dec22 = true;
  /// TauData
  bJetMETTau_Tau_136035_139975_Dec22 = true;
  bJetMETTau_Tau_140058_141881_Dec22 = true;
  bBTau_141956_144114_Dec22 = true;
  bBTau_146428_148058_Dec22 = true;
  bBTau_148822_149182_Dec22 = true;

}



void MyPlotter::ActivateTauData(void){

  /// TauData
  bJetMETTau_Tau_136035_139975_Dec22 = true;
  bJetMETTau_Tau_140058_141881_Dec22 = true;
  bBTau_141956_144114_Dec22 = true;
  bBTau_146428_148058_Dec22 = true;
  bBTau_148822_149182_Dec22 = true;

}



void MyPlotter::ActivateJetData(void){

  /// JetData
  bJetMETTau_Jet_136035_141881_Dec22 = true;
  bJetMET_141956_144114_Dec22 = true;
  bJet_146428_148058_Dec22 = true;
  bJet_148822_149294_Dec22 = true;

}


void MyPlotter::ActivateAllMC(void){

  /// MC 
  bTTToHplusBWB_M90 = true;
  bTTToHplusBWB_M100 = true;
  bTTToHplusBWB_M120 = true;
  bTTToHplusBWB_M140 = true;
  bTTToHplusBWB_M160 = true;
  bQCD = true;
  bQCD_Pt30to50 = true;
  bQCD_Pt50to80 = true;
  bQCD_Pt80to120 = true;
  bQCD_Pt120to170 = true;
  bQCD_Pt170to300 = true;
  bQCD_Pt300to470 = true;
  bTTJets = true;
  bWJets = true;
  bWJets_noPU = false;
}



void MyPlotter::GetRootFiles(const char* multicrab_dir){
  
  /// JetData
  if(bJetMETTau_Jet_136035_141881_Dec22){
    JetMETTau_Jet_136035_141881_Dec22_TFile = new TFile(TString(multicrab_dir) + "/JetMETTau_Jet_136035-141881_Dec22/res/histograms-JetMETTau_Jet_136035-141881_Dec22.root");
    bJetMETTau_Jet_136035_141881_Dec22_TFile = CheckTFile(JetMETTau_Jet_136035_141881_Dec22_TFile);
  }

  if(bJetMET_141956_144114_Dec22){
    JetMET_141956_144114_Dec22_TFile = new TFile(TString(multicrab_dir) + "/JetMET_141956-144114_Dec22/res/histograms-JetMET_141956-144114_Dec22.root");
    bJetMET_141956_144114_Dec22_TFile = CheckTFile(JetMET_141956_144114_Dec22_TFile);
  }

  if(bJet_146428_148058_Dec22){
    Jet_146428_148058_Dec22_TFile = new TFile(TString(multicrab_dir) + "/Jet_146428-148058_Dec22/res/histograms-Jet_146428-148058_Dec22.root");
    bJet_146428_148058_Dec22_TFile = CheckTFile(Jet_146428_148058_Dec22_TFile);
  }

  if(bJet_148822_149294_Dec22){
    Jet_148822_149294_Dec22_TFile = new TFile(TString(multicrab_dir) + "/Jet_148822-149294_Dec22/res/histograms-Jet_148822-149294_Dec22.root");
    bJet_148822_149294_Dec22_TFile = CheckTFile(Jet_148822_149294_Dec22_TFile);
  }
 
  /// TauData
  if(bJetMETTau_Tau_136035_139975_Dec22){ 
    JetMETTau_Tau_136035_139975_Dec22_TFile  = new TFile(TString(multicrab_dir) + "/JetMETTau_Tau_136035-139975_Dec22/res/histograms-JetMETTau_Tau_136035-139975_Dec22.root");
    bJetMETTau_Tau_136035_139975_Dec22_TFile = CheckTFile(JetMETTau_Tau_136035_139975_Dec22_TFile);
  }
  if(bJetMETTau_Tau_140058_141881_Dec22){

JetMETTau_Tau_140058_141881_Dec22_TFile  = new TFile(TString(multicrab_dir) + "/JetMETTau_Tau_140058-141881_Dec22/res/histograms-JetMETTau_Tau_140058-141881_Dec22.root");
    bJetMETTau_Tau_140058_141881_Dec22_TFile = CheckTFile(JetMETTau_Tau_140058_141881_Dec22_TFile);

  }
  if(bBTau_141956_144114_Dec22){
    BTau_141956_144114_Dec22_TFile  =  new TFile(TString(multicrab_dir) + "/BTau_141956-144114_Dec22/res/histograms-BTau_141956-144114_Dec22.root");
    bBTau_141956_144114_Dec22_TFile = CheckTFile(BTau_141956_144114_Dec22_TFile);
  }
  if(bBTau_146428_148058_Dec22){
    BTau_146428_148058_Dec22_TFile  = new TFile(TString(multicrab_dir) + "/BTau_146428-148058_Dec22/res/histograms-BTau_146428-148058_Dec22.root");
    bBTau_146428_148058_Dec22_TFile = CheckTFile(BTau_146428_148058_Dec22_TFile);
  }
  if(bBTau_148822_149182_Dec22){
    BTau_148822_149182_Dec22_TFile  = new TFile(TString(multicrab_dir) + "/BTau_148822-149182_Dec22/res/histograms-BTau_148822-149182_Dec22.root");
    bBTau_148822_149182_Dec22_TFile = CheckTFile(BTau_148822_149182_Dec22_TFile);
  }
  
  /// MC
  if(bTTToHplusBWB_M90) {
    TTToHplusBWB_M90_TFile  = new TFile(TString(multicrab_dir) + "/TTToHplusBWB_M90_Winter10/res/histograms-TTToHplusBWB_M90_Winter10.root");
    bTTToHplusBWB_M90_TFile = CheckTFile(TTToHplusBWB_M90_TFile);
   }
  if(bTTToHplusBWB_M100){
    TTToHplusBWB_M100_TFile  = new TFile(TString(multicrab_dir) + "/TTToHplusBWB_M100_Winter10/res/histograms-TTToHplusBWB_M100_Winter10.root");
    bTTToHplusBWB_M100_TFile = CheckTFile(TTToHplusBWB_M100_TFile);
  }
  if(bTTToHplusBWB_M120){
    TTToHplusBWB_M120_TFile  = new TFile(TString(multicrab_dir) + "/TTToHplusBWB_M120_Winter10/res/histograms-TTToHplusBWB_M120_Winter10.root");
    bTTToHplusBWB_M120_TFile = CheckTFile(TTToHplusBWB_M120_TFile);
  }
  if(bTTToHplusBWB_M140){
    TTToHplusBWB_M140_TFile  = new TFile(TString(multicrab_dir) + "/TTToHplusBWB_M140_Winter10/res/histograms-TTToHplusBWB_M140_Winter10.root");
    bTTToHplusBWB_M140_TFile = CheckTFile(TTToHplusBWB_M140_TFile);
  }
  if(bTTToHplusBWB_M160){
    TTToHplusBWB_M160_TFile  = new TFile(TString(multicrab_dir) + "/TTToHplusBWB_M160_Winter10/res/histograms-TTToHplusBWB_M160_Winter10.root");
    bTTToHplusBWB_M160_TFile = CheckTFile(TTToHplusBWB_M160_TFile);
  }
  
  if(bQCD_Pt30to50) {
    QCD_Pt30to50_TFile   = new TFile(TString(multicrab_dir) + "/QCD_Pt30to50_"+TString(MC_Tune)+"_Winter10/res/histograms-QCD_Pt30to50_" + TString(MC_Tune) + "_Winter10.root");
    bQCD_Pt30to50_TFile  = CheckTFile(QCD_Pt30to50_TFile);
  }
  if(bQCD_Pt50to80) {
    QCD_Pt50to80_TFile   = new TFile(TString(multicrab_dir) + "/QCD_Pt50to80_"+TString(MC_Tune)+"_Winter10/res/histograms-QCD_Pt50to80_" + TString(MC_Tune) + "_Winter10.root");
    bQCD_Pt50to80_TFile  = CheckTFile(QCD_Pt50to80_TFile);
  }
  if(bQCD_Pt80to120) {
    QCD_Pt80to120_TFile  = new TFile(TString(multicrab_dir) + "/QCD_Pt80to120_"+TString(MC_Tune)+"_Winter10/res/histograms-QCD_Pt80to120_" + TString(MC_Tune) + "_Winter10.root");
    bQCD_Pt80to120_TFile = CheckTFile(QCD_Pt80to120_TFile);
  }
  if(bQCD_Pt120to170) {
    QCD_Pt120to170_TFile  = new TFile(TString(multicrab_dir) + "/QCD_Pt120to170_"+TString(MC_Tune)+"_Winter10/res/histograms-QCD_Pt120to170_" + TString(MC_Tune) + "_Winter10.root");
    bQCD_Pt120to170_TFile = CheckTFile(QCD_Pt120to170_TFile);
  }
  if(bQCD_Pt170to300) {
    QCD_Pt170to300_TFile  = new TFile(TString(multicrab_dir) + "/QCD_Pt170to300_"+TString(MC_Tune)+"_Winter10/res/histograms-QCD_Pt170to300_" + TString(MC_Tune) + "_Winter10.root");
    bQCD_Pt170to300_TFile = CheckTFile(QCD_Pt170to300_TFile);
  }
  if(bQCD_Pt300to470) {
    QCD_Pt300to470_TFile  = new TFile(TString(multicrab_dir) + "/QCD_Pt300to470_"+TString(MC_Tune)+"_Winter10/res/histograms-QCD_Pt300to470_" + TString(MC_Tune) + "_Winter10.root");
    bQCD_Pt300to470_TFile = CheckTFile(QCD_Pt300to470_TFile);
  }
 
  if(bTTJets) {
    TTJets_TFile  = new TFile(TString(multicrab_dir) + "/TTJets_" + TString(MC_Tune) + "_Winter10/res/histograms-TTJets_" + TString(MC_Tune) + "_Winter10.root");
    bTTJets_TFile = CheckTFile(TTJets_TFile);
  }
  if(bWJets) {  
    WJets_TFile  = new TFile(TString(multicrab_dir) + "/WJets_" + TString(MC_Tune) + "_Winter10/res/histograms-WJets_" + TString(MC_Tune) + "_Winter10.root");
    bWJets_TFile = CheckTFile(WJets_TFile);
  }
  else if (bWJets_noPU) {  
    WJets_TFile       = new TFile(TString(multicrab_dir) + "/WJets_"+TString(MC_Tune)+"_Winter10_noPU" + "/res/histograms-TTJets_" + TString(MC_Tune) + "_Winter10.root");
    bWJets_noPU_TFile = CheckTFile(WJets_noPU_TFile);
  }

  /// Make generalised booleans for existence of good files
  bQCD_TFile = bQCD_Pt30to50_TFile || bQCD_Pt50to80_TFile || bQCD_Pt80to120_TFile || bQCD_Pt120to170_TFile || bQCD_Pt170to300_TFile || bQCD_Pt300to470_TFile;
  
  bSignal = bTTToHplusBWB_M90_TFile || bTTToHplusBWB_M100_TFile || bTTToHplusBWB_M120_TFile || bTTToHplusBWB_M140_TFile || bTTToHplusBWB_M160_TFile;

  bMC = bQCD_TFile || bSignal || bWJets_TFile || bWJets_noPU_TFile || bTTJets_TFile;

  bJetData =  bJetMETTau_Jet_136035_141881_Dec22_TFile || bJetMET_141956_144114_Dec22_TFile || bJet_146428_148058_Dec22_TFile || bJet_148822_149294_Dec22_TFile;

  bTauData = bJetMETTau_Tau_136035_139975_Dec22_TFile || bJetMETTau_Tau_140058_141881_Dec22_TFile || bBTau_141956_144114_Dec22_TFile || bBTau_146428_148058_Dec22_TFile || bBTau_148822_149182_Dec22_TFile;
  
}



bool MyPlotter::CheckTFile(TFile* f){
  bool bIsZombie = false; 
  if (f->IsZombie()){
    std::cout << "*** WARNING! TFile \"" << f->GetName() << "\" is a \"Zombie\"" << std::endl;
    bIsZombie = false; 
    // exit (-1);
  }else {
    // std::cout << "*** Opened file: " << f->GetName() << std::endl;
    bIsZombie = true;
  }
  return bIsZombie;
}




float MyPlotter::GetHistoXsection(TFile *f){

  TH1D *histo;
  histo = new TH1D;
  histo = (TH1D*)f->Get("configInfo/configinfo");
  float control = histo->GetBinContent(1);
  float xSection = histo->GetBinContent(2);
  float trueXSection = xSection/control;

  return trueXSection;
}



void MyPlotter::GetMCXsections(void){
 
  if(bTTToHplusBWB_M90_TFile)  TTToHplusBWB_M90_Xsection  = GetHistoXsection( TTToHplusBWB_M90_TFile );
  if(bTTToHplusBWB_M100_TFile) TTToHplusBWB_M100_Xsection = GetHistoXsection( TTToHplusBWB_M100_TFile );
  if(bTTToHplusBWB_M120_TFile) TTToHplusBWB_M120_Xsection = GetHistoXsection( TTToHplusBWB_M120_TFile );
  if(bTTToHplusBWB_M140_TFile) TTToHplusBWB_M140_Xsection = GetHistoXsection( TTToHplusBWB_M140_TFile );
  if(bTTToHplusBWB_M160_TFile) TTToHplusBWB_M160_Xsection = GetHistoXsection( TTToHplusBWB_M160_TFile );
  if(bQCD_Pt30to50_TFile)   QCD_Pt30to50_Xsection   = GetHistoXsection( QCD_Pt30to50_TFile );
  if(bQCD_Pt50to80_TFile)   QCD_Pt50to80_Xsection   = GetHistoXsection( QCD_Pt50to80_TFile );
  if(bQCD_Pt80to120_TFile)  QCD_Pt80to120_Xsection  = GetHistoXsection( QCD_Pt80to120_TFile );
  if(bQCD_Pt120to170_TFile) QCD_Pt120to170_Xsection = GetHistoXsection( QCD_Pt120to170_TFile );
  if(bQCD_Pt170to300_TFile) QCD_Pt170to300_Xsection = GetHistoXsection( QCD_Pt170to300_TFile );
  if(bQCD_Pt300to470_TFile) QCD_Pt300to470_Xsection = GetHistoXsection( QCD_Pt300to470_TFile );
  if(bTTJets_TFile)         TTJets_Xsection         = GetHistoXsection( TTJets_TFile );
  if(bWJets_TFile)          WJets_Xsection          = GetHistoXsection( WJets_TFile );
  if(bWJets_noPU_TFile)     WJets_noPU_Xsection     = GetHistoXsection( WJets_noPU_TFile );

}



void MyPlotter::PrintMCXsections(void){
   
  std::cout << "*** Notification! Printing MC Cross Sections" << std::endl;

  std::cout << "*** TTToHplusBWB_M90_Xsection  = " << TTToHplusBWB_M90_Xsection << " (pb)" << std::endl;
  std::cout << "*** TTToHplusBWB_M100_Xsection = " << TTToHplusBWB_M100_Xsection << " (pb)" << std::endl;
  std::cout << "*** TTToHplusBWB_M120_Xsection = " << TTToHplusBWB_M120_Xsection << " (pb)" << std::endl;
  std::cout << "*** TTToHplusBWB_M140_Xsection = " << TTToHplusBWB_M140_Xsection << " (pb)" << std::endl;
  std::cout << "*** TTToHplusBWB_M160_Xsection = " << TTToHplusBWB_M160_Xsection << " (pb)" << std::endl;
  std::cout << "*** QCD_Pt30to50_Xsection = " << QCD_Pt30to50_Xsection << " (pb)" << std::endl;
  std::cout << "*** QCD_Pt50to80_Xsection = " << QCD_Pt50to80_Xsection << " (pb)" << std::endl;
  std::cout << "*** QCD_Pt80to120_Xsection = " << QCD_Pt80to120_Xsection << " (pb)" << std::endl;
  std::cout << "*** QCD_Pt120to170_Xsection = " << QCD_Pt120to170_Xsection << " (pb)" << std::endl;
  std::cout << "*** QCD_Pt170to300_Xsection = " << QCD_Pt170to300_Xsection << " (pb)" << std::endl;
  std::cout << "*** QCD_Pt300to470_Xsection = " << QCD_Pt300to470_Xsection << " (pb)" << std::endl;
  std::cout << "*** TTJets_Xsection = " << TTJets_Xsection << " (pb)" << std::endl;
  std::cout << "*** WJets_Xsection = " << WJets_Xsection << " (pb)" << std::endl;
  std::cout << "*** WJets_noPU_Xsection = " << WJets_noPU_Xsection << " (pb)" << std::endl;

}



void MyPlotter::PrintActiveDatasets(void){

  /// JetData
  std::cout << "*** bJetMETTau_Jet_136035_141881_Dec22 = " << bJetMETTau_Jet_136035_141881_Dec22 << std::endl;
  std::cout << "*** bJetMET_141956_144114_Dec22 = " << bJetMET_141956_144114_Dec22 << std::endl;
  std::cout << "*** bJet_146428_148058_Dec22 = " << bJet_146428_148058_Dec22 << std::endl;
  std::cout << "*** bJet_148822_149294_Dec22 = " << bJet_148822_149294_Dec22 << std::endl;
  /// TauData  
  std::cout << "*** bJetMETTau_Tau_136035_139975_Dec22 = " << bJetMETTau_Tau_136035_139975_Dec22 << std::endl;
  std::cout << "*** bJetMETTau_Tau_140058_141881_Dec22 = " << bJetMETTau_Tau_140058_141881_Dec22 << std::endl;
  std::cout << "*** bBTau_141956_144114_Dec22 = " << bBTau_141956_144114_Dec22 << std::endl;
  std::cout << "*** bBTau_146428_148058_Dec22 = " << bBTau_146428_148058_Dec22 << std::endl;
  std::cout << "*** bBTau_148822_149182_Dec22 = " << bBTau_148822_149182_Dec22 << std::endl;
  /// MC
  std::cout << "*** bTTToHplusBWB_M90 = " << bTTToHplusBWB_M90 << std::endl;
  std::cout << "*** bTTToHplusBWB_M100 = " << bTTToHplusBWB_M100 << std::endl;
  std::cout << "*** bTTToHplusBWB_M120 = " << bTTToHplusBWB_M120 << std::endl;
  std::cout << "*** bTTToHplusBWB_M140 = " << bTTToHplusBWB_M140 << std::endl;
  std::cout << "*** bTTToHplusBWB_M160 = " << bTTToHplusBWB_M160 << std::endl;
  std::cout << "*** bQCD_Pt30to50 = " << bQCD_Pt30to50 << std::endl;
  std::cout << "*** bQCD_Pt50to80 = " << bQCD_Pt50to80 << std::endl;
  std::cout << "*** bQCD_Pt80to120 = " << bQCD_Pt80to120 << std::endl;
  std::cout << "*** bQCD_Pt120to170 = " << bQCD_Pt120to170 << std::endl;
  std::cout << "*** bQCD_Pt170to300 = " << bQCD_Pt170to300 << std::endl;
  std::cout << "*** bQCD_Pt300to470 = " << bQCD_Pt300to470 << std::endl;
  std::cout << "*** bQCD = " << bQCD << std::endl;

  std::cout << "*** bTTJets = " << bTTJets << std::endl;
  std::cout << "*** bWJets = " << bWJets << std::endl;
  std::cout << "*** bWJets_noPU = " << bWJets_noPU << std::endl;
    
}


float MyPlotter::GetHistoAllEvents(TFile* f){

  float allEvents = -1.0;
  TH1D *h = new TH1D;
  TString hCounter = TString(GlobalFolder) + "Counters/counter";
  h = (TH1D*)f->Get(hCounter);

  if(h != 0){
    if( TString(h->GetXaxis()->GetBinLabel(1)).CompareTo("allEvents") == 0){
      allEvents = h->GetBinContent(1);
    } 
    else if( TString(h->GetXaxis()->GetBinLabel(1)).CompareTo("All events") == 0){
      allEvents = h->GetBinContent(1);
    }
    else{ 
      std::cout << "*** WARNING! Could not find the \"All Events\" counters in  histo " << histoName << " in TFile " << f->GetName() << std::endl;
    }
  } //eof: if(h != 0){
  else{
    std::cout << "*** WARNING! Could not find histo with name " << hCounter << " in TFile " << f->GetName() << std::endl;
    allEvents = 0.0;
  }
  
  // std::cout << "*** allEvents = " << allEvents << std::endl;  
  
  return allEvents;
  
}


void MyPlotter::GetMCWeights(void){
  
  if(bTTToHplusBWB_M90_TFile)  TTToHplusBWB_M90_AllEvents  = GetHistoAllEvents( TTToHplusBWB_M90_TFile );
  if(bTTToHplusBWB_M100_TFile) TTToHplusBWB_M100_AllEvents = GetHistoAllEvents( TTToHplusBWB_M100_TFile );
  if(bTTToHplusBWB_M120_TFile) TTToHplusBWB_M120_AllEvents = GetHistoAllEvents( TTToHplusBWB_M120_TFile );
  if(bTTToHplusBWB_M140_TFile) TTToHplusBWB_M140_AllEvents = GetHistoAllEvents( TTToHplusBWB_M140_TFile );
  if(bTTToHplusBWB_M160_TFile) TTToHplusBWB_M160_AllEvents = GetHistoAllEvents( TTToHplusBWB_M160_TFile );
  if(bQCD_Pt30to50_TFile)   QCD_Pt30to50_AllEvents   = GetHistoAllEvents( QCD_Pt30to50_TFile );
  if(bQCD_Pt50to80_TFile)   QCD_Pt50to80_AllEvents   = GetHistoAllEvents( QCD_Pt50to80_TFile );
  if(bQCD_Pt80to120_TFile)  QCD_Pt80to120_AllEvents  = GetHistoAllEvents( QCD_Pt80to120_TFile );
  if(bQCD_Pt120to170_TFile) QCD_Pt120to170_AllEvents = GetHistoAllEvents( QCD_Pt120to170_TFile );
  if(bQCD_Pt170to300_TFile) QCD_Pt170to300_AllEvents = GetHistoAllEvents( QCD_Pt170to300_TFile );
  if(bQCD_Pt300to470_TFile) QCD_Pt300to470_AllEvents = GetHistoAllEvents( QCD_Pt300to470_TFile );
  if(bTTJets_TFile)         TTJets_AllEvents         = GetHistoAllEvents( TTJets_TFile );
  if(bWJets_TFile)          WJets_AllEvents          = GetHistoAllEvents( WJets_TFile );
  if(bWJets_noPU_TFile)     WJets_noPU_AllEvents     = GetHistoAllEvents( WJets_noPU_TFile );
  
  TTToHplusBWB_M90_NormFactor  = (TTToHplusBWB_M90_Xsection/TTToHplusBWB_M90_AllEvents);
  TTToHplusBWB_M100_NormFactor = (TTToHplusBWB_M100_Xsection/TTToHplusBWB_M100_AllEvents);
  TTToHplusBWB_M120_NormFactor = (TTToHplusBWB_M120_Xsection/TTToHplusBWB_M120_AllEvents);
  TTToHplusBWB_M140_NormFactor = (TTToHplusBWB_M140_Xsection/TTToHplusBWB_M140_AllEvents);
  TTToHplusBWB_M160_NormFactor = (TTToHplusBWB_M160_Xsection/TTToHplusBWB_M160_AllEvents);
  QCD_Pt30to50_NormFactor   = (QCD_Pt30to50_Xsection/QCD_Pt30to50_AllEvents);
  QCD_Pt50to80_NormFactor   = (QCD_Pt50to80_Xsection/QCD_Pt50to80_AllEvents);
  QCD_Pt80to120_NormFactor  = (QCD_Pt80to120_Xsection/QCD_Pt80to120_AllEvents);
  QCD_Pt120to170_NormFactor = (QCD_Pt120to170_Xsection/QCD_Pt120to170_AllEvents);
  QCD_Pt170to300_NormFactor = (QCD_Pt170to300_Xsection/QCD_Pt170to300_AllEvents);
  QCD_Pt300to470_NormFactor = (QCD_Pt300to470_Xsection/QCD_Pt300to470_AllEvents);
  TTJets_NormFactor         = (TTJets_Xsection/TTJets_AllEvents);
  WJets_NormFactor          = (WJets_Xsection/WJets_AllEvents);
  WJets_noPU_NormFactor     = (WJets_noPU_Xsection/WJets_noPU_AllEvents);
  
}


void MyPlotter::PrintMCNormFactors(void){
   
  std::cout << "*** TTToHplusBWB_M90_NormFactor (AllEvts/xSec) = " << TTToHplusBWB_M90_NormFactor << std::endl;
  std::cout << "*** TTToHplusBWB_M100_NormFactor(AllEvts/xSec) = " << TTToHplusBWB_M100_NormFactor << std::endl;
  std::cout << "*** TTToHplusBWB_M120_NormFactor(AllEvts/xSec) = " << TTToHplusBWB_M120_NormFactor << std::endl;
  std::cout << "*** TTToHplusBWB_M140_NormFactor(AllEvts/xSec) = " << TTToHplusBWB_M140_NormFactor << std::endl;
  std::cout << "*** TTToHplusBWB_M160_NormFactor(AllEvts/xSec) = " << TTToHplusBWB_M160_NormFactor << std::endl;
  std::cout << "*** QCD_Pt30to50_NormFactor(AllEvts/xSec) = " << QCD_Pt30to50_NormFactor << std::endl;
  std::cout << "*** QCD_Pt50to80_NormFactor(AllEvts/xSec) = " << QCD_Pt50to80_NormFactor << std::endl;
  std::cout << "*** QCD_Pt80to120_NormFactor(AllEvts/xSec) = " << QCD_Pt80to120_NormFactor << std::endl;
  std::cout << "*** QCD_Pt120to170_NormFactor(AllEvts/xSec) = " << QCD_Pt120to170_NormFactor << std::endl;
  std::cout << "*** QCD_Pt170to300_NormFactor(AllEvts/xSec) = " << QCD_Pt170to300_NormFactor << std::endl;
  std::cout << "*** QCD_Pt300to470_NormFactor(AllEvts/xSec) = " << QCD_Pt300to470_NormFactor << std::endl;
  std::cout << "*** TTJets_NormFactor(AllEvts/xSec) = " << TTJets_NormFactor << std::endl;
  std::cout << "*** WJets_NormFactor(AllEvts/xSec) = " << WJets_NormFactor << std::endl;
  std::cout << "*** WJets_noPU_NormFactor(AllEvts/xSec) = " << WJets_noPU_NormFactor << std::endl;

}


void MyPlotter::GetHistos(const char *histo){

  /// JetData
  if(bJetMETTau_Jet_136035_141881_Dec22_TFile) JetMETTau_Jet_136035_141881_Dec22_TH1D = (TH1D*)JetMETTau_Jet_136035_141881_Dec22_TFile->Get(histoName);
  if(bJetMET_141956_144114_Dec22_TFile) JetMET_141956_144114_Dec22_TH1D = (TH1D*)JetMET_141956_144114_Dec22_TFile->Get(histoName);
  if(bJet_146428_148058_Dec22_TFile) Jet_146428_148058_Dec22_TH1D = (TH1D*)Jet_146428_148058_Dec22_TFile->Get(histoName);
  if(bJet_148822_149294_Dec22_TFile) Jet_148822_149294_Dec22_TH1D = (TH1D*)Jet_148822_149294_Dec22_TFile->Get(histoName);
  /// TauData
  if(bJetMETTau_Tau_140058_141881_Dec22_TFile)JetMETTau_Tau_140058_141881_Dec22_TH1D = (TH1D*)JetMETTau_Tau_140058_141881_Dec22_TFile->Get(histoName);
  if(bJetMETTau_Tau_136035_139975_Dec22_TFile)JetMETTau_Tau_136035_139975_Dec22_TH1D = (TH1D*)JetMETTau_Tau_136035_139975_Dec22_TFile->Get(histoName);

  if(bBTau_141956_144114_Dec22_TFile)BTau_141956_144114_Dec22_TH1D   = (TH1D*)BTau_141956_144114_Dec22_TFile->Get(histoName);
  if(bBTau_146428_148058_Dec22_TFile)BTau_146428_148058_Dec22_TH1D   = (TH1D*)BTau_146428_148058_Dec22_TFile->Get(histoName);
  if(bBTau_148822_149182_Dec22_TFile)BTau_148822_149182_Dec22_TH1D   = (TH1D*)BTau_148822_149182_Dec22_TFile->Get(histoName);
  /// MC 
  if(bTTToHplusBWB_M90_TFile)TTToHplusBWB_M90_TH1D   = (TH1D*)TTToHplusBWB_M90_TFile->Get(histoName);
  if(bTTToHplusBWB_M100_TFile)TTToHplusBWB_M100_TH1D = (TH1D*)TTToHplusBWB_M100_TFile->Get(histoName);
  if(bTTToHplusBWB_M120_TFile)TTToHplusBWB_M120_TH1D = (TH1D*)TTToHplusBWB_M120_TFile->Get(histoName);
  if(bTTToHplusBWB_M140_TFile)TTToHplusBWB_M140_TH1D = (TH1D*)TTToHplusBWB_M140_TFile->Get(histoName);
  if(bTTToHplusBWB_M160_TFile)TTToHplusBWB_M160_TH1D = (TH1D*)TTToHplusBWB_M160_TFile->Get(histoName);
  if(bQCD_Pt30to50_TFile)QCD_Pt30to50_TH1D     = (TH1D*)QCD_Pt30to50_TFile->Get(histoName);
  if(bQCD_Pt50to80_TFile)QCD_Pt50to80_TH1D     = (TH1D*)QCD_Pt50to80_TFile->Get(histoName);
  if(bQCD_Pt80to120_TFile)QCD_Pt80to120_TH1D   = (TH1D*)QCD_Pt80to120_TFile->Get(histoName);
  if(bQCD_Pt120to170_TFile)QCD_Pt120to170_TH1D = (TH1D*)QCD_Pt120to170_TFile->Get(histoName);
  if(bQCD_Pt170to300_TFile)QCD_Pt170to300_TH1D = (TH1D*)QCD_Pt170to300_TFile->Get(histoName);
  if(bQCD_Pt300to470_TFile)QCD_Pt300to470_TH1D = (TH1D*)QCD_Pt300to470_TFile->Get(histoName);
  if(bTTJets_TFile)TTJets_TH1D                 = (TH1D*)TTJets_TFile->Get(histoName);
  if(bWJets_TFile)WJets_TH1D                   = (TH1D*)WJets_TFile->Get(histoName);
  if(bWJets_noPU_TFile)WJets_TH1D              = (TH1D*)WJets_noPU_TFile->Get(histoName);

  /// Check that histograms are indeed there!
  /// JetData
  if(JetMETTau_Jet_136035_141881_Dec22_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << JetMETTau_Jet_136035_141881_Dec22_TFile->GetName() << std::endl;
  if(JetMET_141956_144114_Dec22_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << JetMET_141956_144114_Dec22_TFile->GetName() << std::endl;
  if(Jet_146428_148058_Dec22_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << Jet_146428_148058_Dec22_TFile->GetName() << std::endl;
  if(Jet_148822_149294_Dec22_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << Jet_148822_149294_Dec22_TFile->GetName() << std::endl;
  /// TauData
  if(JetMETTau_Tau_140058_141881_Dec22_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << JetMETTau_Tau_140058_141881_Dec22_TFile->GetName() << std::endl;
  if(JetMETTau_Tau_136035_139975_Dec22_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << JetMETTau_Tau_136035_139975_Dec22_TFile->GetName() << std::endl;
  if(BTau_141956_144114_Dec22_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << BTau_141956_144114_Dec22_TFile->GetName() << std::endl;
  if(BTau_146428_148058_Dec22_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << BTau_146428_148058_Dec22_TFile->GetName() << std::endl;
  if(BTau_148822_149182_Dec22_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << BTau_148822_149182_Dec22_TFile->GetName() << std::endl;
  /// MC
  if(TTToHplusBWB_M90_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << TTToHplusBWB_M90_TFile->GetName() << std::endl;
  if(TTToHplusBWB_M100_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << TTToHplusBWB_M100_TFile->GetName() << std::endl;
  if(TTToHplusBWB_M120_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << TTToHplusBWB_M120_TFile->GetName() << std::endl;
  if(TTToHplusBWB_M140_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << TTToHplusBWB_M140_TFile->GetName() << std::endl;
  if(TTToHplusBWB_M160_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << TTToHplusBWB_M160_TFile->GetName() << std::endl;
  if(QCD_Pt30to50_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << QCD_Pt30to50_TFile->GetName() << std::endl;
  if(QCD_Pt50to80_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << QCD_Pt50to80_TFile->GetName() << std::endl;
  if(QCD_Pt80to120_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << QCD_Pt80to120_TFile->GetName() << std::endl;
  if(QCD_Pt120to170_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << QCD_Pt120to170_TFile->GetName() << std::endl;
  if(QCD_Pt170to300_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << QCD_Pt170to300_TFile->GetName() << std::endl;
  if(QCD_Pt300to470_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << QCD_Pt300to470_TFile->GetName() << std::endl;
  if(TTJets_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << TTJets_TFile->GetName() << std::endl;
  if(WJets_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << WJets_TFile->GetName() << std::endl;
  if(WJets_noPU_TH1D == 0) std::cout << "*** ERROR! No histogram named '" << histo << "' in file '" << WJets_noPU_TFile->GetName() << std::endl;

}


void MyPlotter::RemoveDatasets(std::vector<TString> myDatasetVector){
  
  // std::vector<TString>::iterator it;
  std::vector<TString>::iterator it;
    
  if(myDatasetVector.size() != 0){
    /// Loop over all TStrings in the vector
    for ( it=myDatasetVector.begin(); it < myDatasetVector.end(); it++ ){
      
      // std::cout << "*** Notification! Removing directory " << (*it) << " from the plotting list" << std::endl;
      /// For some strange reason I get an error if I use else if after the first "if" statement
      
      /// JetData
      if((*it).CompareTo("JetMETTau_Jet_136035-141881_Dec22") == 0 ){ bJetMETTau_Jet_136035_141881_Dec22 = false;}
      if((*it).CompareTo("JetMET_141956-144114_Dec22") == 0 ){ bJetMET_141956_144114_Dec22 = false;}
      if((*it).CompareTo("Jet_146428-148058_Dec22") == 0 ){ bJet_146428_148058_Dec22 = false;}
      if((*it).CompareTo("Jet_148822-149294_Dec22") == 0 ){ bJet_148822_149294_Dec22 = false;}
      /// TauData
      if((*it).CompareTo("JetMETTau_Tau_136035-139975_Dec22") == 0 ){bJetMETTau_Tau_136035_139975_Dec22 = false;}
      if((*it).CompareTo("JetMETTau_Tau_140058-141881_Dec22") == 0 ){bJetMETTau_Tau_140058_141881_Dec22 = false;}
      if((*it).CompareTo("BTau_141956-144114_Dec22") == 0 ){bBTau_141956_144114_Dec22 = false;}
      if((*it).CompareTo("BTau_146428-148058_Dec22") == 0 ){bBTau_146428_148058_Dec22 = false;}
      if((*it).CompareTo("BTau_148822-149182_Dec22") == 0 ){bBTau_148822_149182_Dec22 = false;}
      /// MC
      if((*it).CompareTo("TTToHplusBWB_M90") == 0 ){bTTToHplusBWB_M90 = false;}
      if((*it).CompareTo("TTToHplusBWB_M100") == 0 ){bTTToHplusBWB_M100 = false;}
      if((*it).CompareTo("TTToHplusBWB_M120") == 0 ){bTTToHplusBWB_M120 = false;}
      if((*it).CompareTo("TTToHplusBWB_M140") == 0 ){bTTToHplusBWB_M140 = false;}
      if((*it).CompareTo("TTToHplusBWB_M160") == 0 ){bTTToHplusBWB_M160 = false;}
      if((*it).CompareTo("QCD") == 0 ){bQCD = false;}
      if((*it).CompareTo("QCD_Pt30to50") == 0 ){bQCD_Pt30to50 = false;}
      if((*it).CompareTo("QCD_Pt50to80") == 0 ){bQCD_Pt50to80 = false;}
      if((*it).CompareTo("QCD_Pt80to120") == 0 ){bQCD_Pt80to120 = false;}
      if((*it).CompareTo("QCD_Pt120to170") == 0 ){bQCD_Pt120to170 = false;}
      if((*it).CompareTo("QCD_Pt170to300") == 0 ){bQCD_Pt170to300 = false;}
      if((*it).CompareTo("QCD_Pt300to470") == 0 ){bQCD_Pt300to470 = false;}
      if((*it).CompareTo("TTJets") == 0 ){bTTJets = false;}
      if((*it).CompareTo("WJets") == 0 ){bWJets = false;}
      if((*it).CompareTo("WJets_noPU") == 0 ){bWJets_noPU = false;}
      // else{std::cout << "*** WARNING! The directory \""<<(*it)<<"\" does not exist. Please check the input name" << std::endl;}
    } //eof: loop
  }//eof: if(myDatasetVector.sizer() != 0){
  else std::cout << "*** WARNING! The dataset vector passed to the function is empty. Nothing will be done" << std::endl;
  bQCD = bQCD_Pt30to50 || bQCD_Pt50to80 || bQCD_Pt80to120 || bQCD_Pt120to170 || bQCD_Pt170to300 || bQCD_Pt300to470;
}



void MyPlotter::AddDatasets(std::vector<TString> myDatasetVector){
  
  // std::vector<TString>::iterator it;
  std::vector<TString>::iterator it;
    
  if(myDatasetVector.size() != 0){
    /// Loop over all TStrings in the vector
    for ( it=myDatasetVector.begin(); it < myDatasetVector.end(); it++ ){
      
      // std::cout << "*** Notification! Removing directory " << (*it) << " from the plotting list" << std::endl;
      /// For some strange reason I get an error if I use else if after the first "if" statement
      
      /// JetData
      if((*it).CompareTo("JetMETTau_Jet_136035-141881_Dec22") == 0 ){ bJetMETTau_Jet_136035_141881_Dec22 = true;}
      if((*it).CompareTo("JetMET_141956-144114_Dec22") == 0 ){ bJetMET_141956_144114_Dec22 = true;}
      if((*it).CompareTo("Jet_146428-148058_Dec22") == 0 ){ bJet_146428_148058_Dec22 = true;}
      if((*it).CompareTo("Jet_148822-149294_Dec22") == 0 ){ bJet_148822_149294_Dec22 = true;}
      /// TauData
      if((*it).CompareTo("JetMETTau_Tau_136035-139975_Dec22") == 0 ){bJetMETTau_Tau_136035_139975_Dec22 = true;}
      if((*it).CompareTo("JetMETTau_Tau_140058-141881_Dec22") == 0 ){bJetMETTau_Tau_140058_141881_Dec22 = true;}
      if((*it).CompareTo("BTau_141956-144114_Dec22") == 0 ){bBTau_141956_144114_Dec22 = true;}
      if((*it).CompareTo("BTau_146428-148058_Dec22") == 0 ){bBTau_146428_148058_Dec22 = true;}
      if((*it).CompareTo("BTau_148822-149182_Dec22") == 0 ){bBTau_148822_149182_Dec22 = true;}
      /// MC
      if((*it).CompareTo("TTToHplusBWB_M90") == 0 ){bTTToHplusBWB_M90 = true;}
      if((*it).CompareTo("TTToHplusBWB_M100") == 0 ){bTTToHplusBWB_M100 = true;}
      if((*it).CompareTo("TTToHplusBWB_M120") == 0 ){bTTToHplusBWB_M120 = true;}
      if((*it).CompareTo("TTToHplusBWB_M140") == 0 ){bTTToHplusBWB_M140 = true;}
      if((*it).CompareTo("TTToHplusBWB_M160") == 0 ){bTTToHplusBWB_M160 = true;}
      if((*it).CompareTo("QCD") == 0 ){bQCD = true;}
      if((*it).CompareTo("QCD_Pt30to50") == 0 ){bQCD_Pt30to50 = true;}
      if((*it).CompareTo("QCD_Pt50to80") == 0 ){bQCD_Pt50to80 = true;}
      if((*it).CompareTo("QCD_Pt80to120") == 0 ){bQCD_Pt80to120 = true;}
      if((*it).CompareTo("QCD_Pt120to170") == 0 ){bQCD_Pt120to170 = true;}
      if((*it).CompareTo("QCD_Pt170to300") == 0 ){bQCD_Pt170to300 = true;}
      if((*it).CompareTo("QCD_Pt300to470") == 0 ){bQCD_Pt300to470 = true;}
      if((*it).CompareTo("TTJets") == 0 ){bTTJets = true;}
      if((*it).CompareTo("WJets") == 0 ){bWJets = true;}
      if((*it).CompareTo("WJets_noPU") == 0 ){bWJets_noPU = true;}
      // else{std::cout << "*** WARNING! The directory \""<<(*it)<<"\" does not exist. Please check the input name" << std::endl;}
    } //eof: loop
  }//eof: if(myDatasetVector.sizer() != 0){
  else std::cout << "*** WARNING! The dataset vector passed to the function is empty. Nothing will be done" << std::endl;
  bQCD = bQCD_Pt30to50 || bQCD_Pt50to80 || bQCD_Pt80to120 || bQCD_Pt120to170 || bQCD_Pt170to300 || bQCD_Pt300to470;
}



void MyPlotter::Draw(char *options){

  if(!bOverwriteIntegratedLumi){
    GetHistoLuminosities();
    if(bJetData){ IntegratedLumi = TotalJetDataHistoLumi;}
    else if(bTauData){ IntegratedLumi = TotalTauDataHistoLumi;}
    else{ 
      std::cout << "*** WARNING! Could not determine the Integrated Luminosity from the DATA histograms! IntegratedLumi = " << IntegratedLumi << std::endl;
    }
  }
  ApplyMCNormFactors();
  if(bTauData) MergeTauData();
  // std::cout << "bJetData = " << bJetData << std::endl;
  if(bJetData) MergeJetData();
  if(bQCD)  MergeQCD();
  StackMCHistos();
  StackTauDataHistos();
  StackJetDataHistos();
  SetHistoStyles();

  CreateCanvas();
  CreateDumbieHisto();
  dumbieHisto->Draw(); 
  // dumbieHisto->Draw("AXIS"); //crashes!

  if(bMC) MC_THStack->Draw(TString(options) + "sames");
  if(bTauData) TauData_TH1D->Draw("sames");
  if(bJetData) JetData_TH1D->Draw("sames");
  //  Bkg_THStack->Draw("h, sames"); // will not draw the signal MC 

  canvas->Update();
  AddCmsPreliminaryText();
  AddEnergy7TeVText();  
  char myLumi[10];
  sprintf(myLumi,"%.1f",IntegratedLumi);
  AddLuminosityText(myLumi, "pb^{-1}");
  // std::cout << "*** SuperimposeCounter  = " << SuperimposeCounter << std::endl;
  std::cout << "*** Notification! Finished plotting histo with name " << histoName << "\n" << std::endl;
}



void MyPlotter::DrawSuperimposed(char *options, TString legTitle){
  // Suports up to 3 superpositions of datasets sets
  SuperimposeCounter++; 
  if(!bOverwriteIntegratedLumi){
    GetHistoLuminosities();
    if(bJetData){ IntegratedLumi = TotalJetDataHistoLumi;}
    else if(bTauData){ IntegratedLumi = TotalTauDataHistoLumi;}
    else{ 
      std::cout << "*** WARNING! Could not determine the Integrated Luminosity from the DATA histograms! IntegratedLumi = " << IntegratedLumi << std::endl;
    }
  }
  ApplyMCNormFactors();
  if(bTauData) MergeTauData();
  if(bJetData) MergeJetData();
  if(bQCD)  MergeQCD();
  StackMCHistos();
  StackTauDataHistos();
  StackJetDataHistos();
  SetHistoStyles();
  if(bMC) MC_THStack->Draw(TString(options) + "sames");
  if(bTauData) TauData_TH1D->Draw("sames");
  if(bJetData) JetData_TH1D->Draw("sames");
  AddHistoLegends(legTitle, x1Leg-xLegLength, y1Leg, x2Leg-xLegLength, y2Leg);
 
  canvas->Update();
  // std::cout << "*** SuperimposeCounter  = " << SuperimposeCounter << std::endl;
  // std::cout << "*** bEnableHistoMarkers  = " << bEnableHistoMarkers << std::endl;
  std::cout << "*** Notification! Finished plotting histo with name " << histoName << "\n" << std::endl;
}



void MyPlotter::AddHistoWeight(TH1D* histo, float weight){
  if(!bOverwriteIntegratedLumi){
    std::cout << "*** Notification! Applying IntegratedLumi " << IntegratedLumi << " pb^{-1} to histo " << histo->GetName() << std::endl;
    histo->Scale(weight*IntegratedLumi);
  }
  else{
    std::cout << "*** WARNING! Chosen to over-write the IntegratedLumi to " << IntegratedLumi << " pb^{-1} to histo " << histo->GetName() << std::endl;
    histo->Scale(weight*IntegratedLumi);
  }
}



void MyPlotter::ApplyMCNormFactors(void){
  
  if(bTTToHplusBWB_M90_TFile){  AddHistoWeight(TTToHplusBWB_M90_TH1D, TTToHplusBWB_M90_NormFactor);}
  if(bTTToHplusBWB_M100_TFile){ AddHistoWeight(TTToHplusBWB_M100_TH1D, TTToHplusBWB_M100_NormFactor);}
  if(bTTToHplusBWB_M120_TFile){ AddHistoWeight(TTToHplusBWB_M120_TH1D, TTToHplusBWB_M120_NormFactor);}
  if(bTTToHplusBWB_M140_TFile){ AddHistoWeight(TTToHplusBWB_M140_TH1D, TTToHplusBWB_M140_NormFactor);}
  if(bTTToHplusBWB_M160_TFile){ AddHistoWeight(TTToHplusBWB_M160_TH1D, TTToHplusBWB_M160_NormFactor);}
  if(bQCD_Pt30to50_TFile){      AddHistoWeight(QCD_Pt30to50_TH1D, QCD_Pt30to50_NormFactor);}
  if(bQCD_Pt50to80_TFile){      AddHistoWeight(QCD_Pt50to80_TH1D, QCD_Pt50to80_NormFactor);}
  if(bQCD_Pt80to120_TFile){     AddHistoWeight(QCD_Pt80to120_TH1D, QCD_Pt80to120_NormFactor);}
  if(bQCD_Pt120to170_TFile){    AddHistoWeight(QCD_Pt120to170_TH1D, QCD_Pt120to170_NormFactor);}
  if(bQCD_Pt170to300_TFile){    AddHistoWeight(QCD_Pt170to300_TH1D, QCD_Pt170to300_NormFactor);}
  if(bQCD_Pt300to470_TFile){    AddHistoWeight(QCD_Pt300to470_TH1D, QCD_Pt300to470_NormFactor);}
  if(bTTJets_TFile){            AddHistoWeight(TTJets_TH1D, TTJets_NormFactor);}
  if(bWJets_TFile){             AddHistoWeight(WJets_TH1D, WJets_NormFactor);}
  if(bWJets_noPU_TFile){        AddHistoWeight(WJets_noPU_TH1D, WJets_noPU_NormFactor);}

  if( bTTToHplusBWB_M90_TFile || bTTToHplusBWB_M100_TFile || bTTToHplusBWB_M120_TFile || bTTToHplusBWB_M140_TFile || bTTToHplusBWB_M160_TFile || bQCD || bTTJets_TFile || bWJets_TFile || bWJets_noPU_TFile){
    bApplyWeights = true;
    std::cout << "*** Notification! MC Weights applied " << std::endl;
  }
  else{
    // std::cout << "*** Notification! MC Weights FAILED to be applied " << std::endl;
  }

}



void MyPlotter::MergeQCD(void){
  
  if(QCD_Pt30to50_TH1D->GetEntries()>0){
    QCD_TH1D = QCD_Pt30to50_TH1D;
    
    // if(QCD_Pt30to50_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt30to50_TH1D);
    if(QCD_Pt50to80_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt50to80_TH1D);
    if(QCD_Pt80to120_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt80to120_TH1D);
    if(QCD_Pt120to170_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt120to170_TH1D);
    if(QCD_Pt170to300_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt170to300_TH1D);
    if(QCD_Pt300to470_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt300to470_TH1D);
  }
  else if(QCD_Pt50to80_TH1D->GetEntries()>0){
    QCD_TH1D = QCD_Pt50to80_TH1D;
    
    // if(QCD_Pt30to50_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt30to50_TH1D);
    // if(QCD_Pt50to80_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt50to80_TH1D);
    if(QCD_Pt80to120_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt80to120_TH1D);
    if(QCD_Pt120to170_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt120to170_TH1D);
    if(QCD_Pt170to300_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt170to300_TH1D);
    if(QCD_Pt300to470_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt300to470_TH1D);
  }
  else if(QCD_Pt80to120_TH1D->GetEntries()>0){
    QCD_TH1D = QCD_Pt80to120_TH1D;
    
    // if(QCD_Pt30to50_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt30to50_TH1D);
    // if(QCD_Pt50to80_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt50to80_TH1D);
    // if(QCD_Pt80to120_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt80to120_TH1D);
    if(QCD_Pt120to170_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt120to170_TH1D);
    if(QCD_Pt170to300_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt170to300_TH1D);
    if(QCD_Pt300to470_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt300to470_TH1D);
  }
  else if(QCD_Pt120to170_TH1D->GetEntries()>0){
    QCD_TH1D = QCD_Pt120to170_TH1D;
    
    // if(QCD_Pt30to50_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt30to50_TH1D);
    // if(QCD_Pt50to80_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt50to80_TH1D);
    // if(QCD_Pt80to120_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt80to120_TH1D);
    // if(QCD_Pt120to170_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt120to170_TH1D);
    if(QCD_Pt170to300_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt170to300_TH1D);
    if(QCD_Pt300to470_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt300to470_TH1D);
  }
  else if(QCD_Pt170to300_TH1D->GetEntries()>0){
    QCD_TH1D = QCD_Pt170to300_TH1D;
    
    // if(QCD_Pt30to50_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt30to50_TH1D);
    // if(QCD_Pt50to80_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt50to80_TH1D);
    // if(QCD_Pt80to120_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt80to120_TH1D);
    // if(QCD_Pt120to170_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt120to170_TH1D);
    // if(QCD_Pt170to300_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt170to300_TH1D);
    if(QCD_Pt300to470_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt300to470_TH1D);
  }
  else if(QCD_Pt300to470_TH1D->GetEntries()>0){
    QCD_TH1D = QCD_Pt300to470_TH1D;
    
    // if(QCD_Pt30to50_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt30to50_TH1D);
    // if(QCD_Pt50to80_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt50to80_TH1D);
    // if(QCD_Pt80to120_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt80to120_TH1D);
    // if(QCD_Pt120to170_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt120to170_TH1D);
    // if(QCD_Pt170to300_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt170to300_TH1D);
    // if(QCD_Pt300to470_TH1D->GetEntries()>0) QCD_TH1D->Add(QCD_Pt300to470_TH1D);
    
  }else{std::cout << "*** WARNING! All QCD sample histogram entries are zero! QCD samples will not be merged" << std::endl;}
}



void MyPlotter::MergeJetData(void){
  
  
  if(JetMETTau_Jet_136035_141881_Dec22_TH1D->GetEntries() > 0){
    bJetData = true;
    JetData_TH1D = JetMETTau_Jet_136035_141881_Dec22_TH1D;
    if(JetMET_141956_144114_Dec22_TH1D->GetEntries() > 0) JetData_TH1D->Add(JetMET_141956_144114_Dec22_TH1D);
    if(Jet_146428_148058_Dec22_TH1D->GetEntries() > 0) JetData_TH1D->Add(Jet_146428_148058_Dec22_TH1D);
    if(Jet_148822_149294_Dec22_TH1D->GetEntries() > 0) JetData_TH1D->Add(Jet_148822_149294_Dec22_TH1D);
  } 
  else if(JetMET_141956_144114_Dec22_TH1D->GetEntries() > 0){
    bJetData = true;
    JetData_TH1D = JetMET_141956_144114_Dec22_TH1D;
    if(Jet_146428_148058_Dec22_TH1D->GetEntries() > 0) JetData_TH1D->Add(Jet_146428_148058_Dec22_TH1D);
    if(Jet_148822_149294_Dec22_TH1D->GetEntries() > 0) JetData_TH1D->Add(Jet_148822_149294_Dec22_TH1D);
  } 
  else if(Jet_146428_148058_Dec22_TH1D->GetEntries() > 0) {
    bJetData = true;
    JetData_TH1D = Jet_146428_148058_Dec22_TH1D;
    if(Jet_148822_149294_Dec22_TH1D->GetEntries() > 0) JetData_TH1D->Add(Jet_148822_149294_Dec22_TH1D);
  } 
  else if(Jet_148822_149294_Dec22_TH1D->GetEntries() > 0){
    bJetData = true;
    JetData_TH1D = Jet_148822_149294_Dec22_TH1D;
  }
  else{
    std::cout << "*** WARNING! All JetData histograms have zero entries! Skipping JetData Merge" << std::endl;
    bJetData = false;
  }
  
}



void MyPlotter::MergeBTau(void){
  
  if(BTau_141956_144114_Dec22_TH1D->GetEntries() > 0){
    bBTau = true;
    BTau_TH1D = BTau_141956_144114_Dec22_TH1D;
    if(BTau_146428_148058_Dec22_TH1D->GetEntries()>0) BTau_TH1D->Add(BTau_146428_148058_Dec22_TH1D);
    if(BTau_148822_149182_Dec22_TH1D->GetEntries()>0) BTau_TH1D->Add(BTau_148822_149182_Dec22_TH1D);
  }
  else if(BTau_146428_148058_Dec22_TH1D->GetEntries()>0){
    bBTau = true;
    BTau_TH1D = BTau_146428_148058_Dec22_TH1D;
    if(BTau_148822_149182_Dec22_TH1D->GetEntries()>0) BTau_TH1D->Add(BTau_148822_149182_Dec22_TH1D);
  }else if(BTau_148822_149182_Dec22_TH1D->GetEntries()>0){
    bBTau = true;
    BTau_TH1D = BTau_148822_149182_Dec22_TH1D;
  }else{
    std::cout << "*** WARNING! All BTau histograms have zero entries! Skipping BTau Merge" << std::endl;
    bBTau = false;
  }
  bTauData = bBTau || bJetMETTau;
}



void MyPlotter::MergeJetMETTau(void){
  
  if(JetMETTau_Tau_136035_139975_Dec22_TH1D->GetEntries() > 0){
    bJetMETTau = true;
    JetMETTau_TH1D = JetMETTau_Tau_136035_139975_Dec22_TH1D;
    if(JetMETTau_Tau_140058_141881_Dec22_TH1D->GetEntries() > 0)JetMETTau_TH1D->Add(JetMETTau_Tau_140058_141881_Dec22_TH1D);
  }
  else if(JetMETTau_Tau_140058_141881_Dec22_TH1D->GetEntries() > 0){
    bJetMETTau = true;
    JetMETTau_TH1D = JetMETTau_Tau_140058_141881_Dec22_TH1D;
  }else{
    std::cout << "*** WARNING! All JetMETTau histograms have zero entries! Skipping JetMETTau Merge" << std::endl;
    bJetMETTau = false;
  }
}


void MyPlotter::MergeTauData(void){

  MergeBTau();
  MergeJetMETTau();
  if(bBTau && bJetMETTau){
    bTauData = true;
    TauData_TH1D = BTau_TH1D;
    TauData_TH1D->Add(JetMETTau_TH1D);
    // std::cout << "*** Notification! Merged datasets BTau and JetMETTau" << std::endl;
  }
  else if(bBTau && !bJetMETTau){
    bTauData = true;
    TauData_TH1D = BTau_TH1D;
  }
  else if(!bBTau && bJetMETTau){
    bTauData = true;
    TauData_TH1D = JetMETTau_TH1D;
  }
  else{
    std::cout << "*** WARNING! No TauData" << std::endl;
  }
  
}




void MyPlotter::StackMCHistos(void){

  if(bWJets_TFile){
    MC_THStack->Add(WJets_TH1D);
    Bkg_THStack->Add(WJets_TH1D);
    bMC = true;
    std::cout << "*** Notification! Added WJets to the MC THStack" << std::endl;
  }else if(bWJets_noPU_TFile){ /// with PileUp or w/o PileUp but NOT BOTH
    MC_THStack->Add(WJets_noPU_TH1D);
    Bkg_THStack->Add(WJets_noPU_TH1D);
    bMC = true;
    std::cout << "*** Notification! Added WJets_noPU to the MC THStack" << std::endl;
  }

  if(bTTJets_TFile){
    MC_THStack->Add(TTJets_TH1D);
    Bkg_THStack->Add(TTJets_TH1D);
    bMC = true;
    std::cout << "*** Notification! Added TTJets to the MC THStack" << std::endl;
  }

  if(bQCD_TFile && bQCD){
    MC_THStack->Add(QCD_TH1D);
    Bkg_THStack->Add(QCD_TH1D);
    bMC = true;
    std::cout << "*** Notification! Added QCD to the MC THStack" << std::endl;
  }

  if(bSignal){
    if(bTTToHplusBWB_M90_TFile)   MC_THStack->Add(TTToHplusBWB_M90_TH1D);
    else if(bTTToHplusBWB_M100_TFile)  MC_THStack->Add(TTToHplusBWB_M100_TH1D);
    else if(bTTToHplusBWB_M120_TFile)  MC_THStack->Add(TTToHplusBWB_M120_TH1D);
    else if(bTTToHplusBWB_M140_TFile)  MC_THStack->Add(TTToHplusBWB_M140_TH1D);
    else if(bTTToHplusBWB_M160_TFile)  MC_THStack->Add(TTToHplusBWB_M160_TH1D);
    else{
      std::cout << "*** Warning! No Signal MC to add to stack" << std::endl;
    }
    bMC = true;
    std::cout << "*** Notification! Added Signal MC to the MC THStack" << std::endl;
  }

  if(!bMC){
    std::cout << "*** WARNING! No MC histos added to the MC THStack" << std::endl;
  }
  else{
    // std::cout << "*** Notification! MC histos added to the MC THStack" << std::endl;
  }

}



void MyPlotter::StackTauDataHistos(void){

  if(bBTau){
    // std::cout << "*** Notification! Adding BTau to Data Stack" << std::endl;
    TauData_THStack->Add(BTau_TH1D);
  }
  if(bJetMETTau){
    // std::cout << "*** Notification! Adding JetMETTau to Data Stack" << std::endl;
    TauData_THStack->Add(JetMETTau_TH1D);
  }
    
}



void MyPlotter::StackJetDataHistos(void){
  
  
  if(bJetMETTau_Jet_136035_141881_Dec22){
    JetData_THStack->Add(JetMETTau_Jet_136035_141881_Dec22_TH1D);
  }
  if(bJetMET_141956_144114_Dec22){
    JetData_THStack->Add(JetMET_141956_144114_Dec22_TH1D);
  }
  if(bJet_146428_148058_Dec22){
    JetData_THStack->Add(Jet_146428_148058_Dec22_TH1D);
  }
  if(bJet_148822_149294_Dec22){
    JetData_THStack->Add(Jet_148822_149294_Dec22_TH1D);
  }
  
}



void MyPlotter::SetHistoStyles(void){

  if(SuperimposeCounter!=0) bEnableHistoMarkers = true;

  if(bTauData)           SetHistoStyle_TauData();
  if(bJetData)           SetHistoStyle_JetData();
  if(bQCD)               SetHistoStyle_QCD();
  /*
  if(bQCD_Pt30to50)      SetHistoStyle_QCD_Pt30to50();
  if(bQCD_Pt50to80)      SetHistoStyle_QCD_Pt50to80();
  if(bQCD_Pt80to120)     SetHistoStyle_QCD_Pt80to120();
  if(bQCD_Pt120to170)    SetHistoStyle_QCD_Pt120to170();
  if(bQCD_Pt170to300)    SetHistoStyle_QCD_Pt170to300();
  if(bQCD_Pt300to470)    SetHistoStyle_QCD_Pt300to470();
  */
  if(bTTToHplusBWB_M90)  SetHistoStyle_SignalM90();
  if(bTTToHplusBWB_M100) SetHistoStyle_SignalM100();
  if(bTTToHplusBWB_M120) SetHistoStyle_SignalM120();
  if(bTTToHplusBWB_M140) SetHistoStyle_SignalM140();
  if(bTTToHplusBWB_M160) SetHistoStyle_SignalM160();
  if(bTTJets)            SetHistoStyle_TTJets();
  if(bWJets)             SetHistoStyle_WJets();
  if(bWJets_noPU)        SetHistoStyle_WJets_noPU();

}

void MyPlotter::SetHistoStyle_TauData(void){

  Color_t colour = kBlack;
  Style_t marker = kFullCircle;

  if( (SuperimposeCounter==0) || (ColourCounter==0) ){
    colour = kBlack;
    marker = kFullCircle;
  }
  if( (SuperimposeCounter==1) || (ColourCounter==1) ){
    colour = kGray+1;
    marker = kFullCircle;
  } 
  if( (SuperimposeCounter==2) || (ColourCounter==2) ){
    colour = kBlack;
    marker = kOpenCircle;
  }

  if(bJetMETTau_Tau_136035_139975_Dec22){
    JetMETTau_Tau_136035_139975_Dec22_TH1D->SetMarkerColor(colour);
    JetMETTau_Tau_136035_139975_Dec22_TH1D->SetMarkerStyle(marker);
    JetMETTau_Tau_136035_139975_Dec22_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
  if(bBTau_141956_144114_Dec22){
    BTau_141956_144114_Dec22_TH1D->SetMarkerColor(colour);
    BTau_141956_144114_Dec22_TH1D->SetMarkerStyle(marker);
    BTau_141956_144114_Dec22_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
  if(bBTau_146428_148058_Dec22){
    BTau_146428_148058_Dec22_TH1D->SetMarkerColor(colour);
    BTau_146428_148058_Dec22_TH1D->SetMarkerStyle(marker);
    BTau_146428_148058_Dec22_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
  if(bBTau_148822_149182_Dec22){
    BTau_148822_149182_Dec22_TH1D->SetMarkerColor(colour);
    BTau_148822_149182_Dec22_TH1D->SetMarkerStyle(marker);
    BTau_148822_149182_Dec22_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
  if(bBTau){
    BTau_TH1D->SetMarkerColor(colour);
    BTau_TH1D->SetMarkerStyle(marker);
    BTau_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
  if(bTauData){
    TauData_TH1D->SetMarkerColor(colour);
    TauData_TH1D->SetMarkerStyle(marker);
    TauData_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
}



void MyPlotter::SetHistoStyle_JetData(void){

  Color_t colour = kBlack;
  Style_t marker = kFullCircle;
  int lineStyle = 2;
  int lineWidth = 2;
  Color_t lineColour = kBlack;
  
 if( (SuperimposeCounter==0) || (ColourCounter==0) ){
   colour = kBlack;
   marker = kFullCircle;
   lineStyle = 2;
   lineWidth = 2;
   lineColour = kBlack;
 }
 if( (SuperimposeCounter==1) || (ColourCounter==1) ){
    colour = kGray+1;
    marker = kFullCircle;
    lineStyle = 4;
    lineWidth = 4;
    lineColour = kGray+1;
 } 
 if( (SuperimposeCounter==2) || (ColourCounter==2) ){
    colour = kBlack;
    marker = kOpenCircle;
    lineStyle = 6;
    lineWidth = 6;
    lineColour = kBlack;
 }
  
  if(bJetMETTau_Jet_136035_141881_Dec22){
     JetMETTau_Jet_136035_141881_Dec22_TH1D->SetMarkerColor(colour);
     JetMETTau_Jet_136035_141881_Dec22_TH1D->SetMarkerStyle(marker);
     JetMETTau_Jet_136035_141881_Dec22_TH1D->SetMarkerSize(GlobalMarkerSize);
     JetMETTau_Jet_136035_141881_Dec22_TH1D->SetLineColor(colour);
     JetMETTau_Jet_136035_141881_Dec22_TH1D->SetLineStyle(lineStyle);
     JetMETTau_Jet_136035_141881_Dec22_TH1D->SetLineWidth(lineWidth);
  }
  if(bJetMET_141956_144114_Dec22){
    JetMET_141956_144114_Dec22_TH1D->SetMarkerColor(colour);
    JetMET_141956_144114_Dec22_TH1D->SetMarkerStyle(marker);
    JetMET_141956_144114_Dec22_TH1D->SetMarkerSize(GlobalMarkerSize);
    JetMET_141956_144114_Dec22_TH1D->SetLineColor(colour);
    JetMET_141956_144114_Dec22_TH1D->SetLineStyle(lineStyle);
    JetMET_141956_144114_Dec22_TH1D->SetLineWidth(lineWidth);
  }
  if(bJet_146428_148058_Dec22){  
    Jet_146428_148058_Dec22_TH1D->SetMarkerColor(colour);
    Jet_146428_148058_Dec22_TH1D->SetMarkerStyle(marker);
    Jet_146428_148058_Dec22_TH1D->SetMarkerSize(GlobalMarkerSize);
    Jet_146428_148058_Dec22_TH1D->SetLineColor(colour);
    Jet_146428_148058_Dec22_TH1D->SetLineStyle(lineStyle);
    Jet_146428_148058_Dec22_TH1D->SetLineWidth(lineWidth);
  }
  if(bJet_148822_149294_Dec22){
     Jet_148822_149294_Dec22_TH1D->SetMarkerColor(colour);
     Jet_148822_149294_Dec22_TH1D->SetMarkerStyle(marker);
     Jet_148822_149294_Dec22_TH1D->SetMarkerSize(GlobalMarkerSize);
     Jet_148822_149294_Dec22_TH1D->SetLineColor(colour);
     Jet_148822_149294_Dec22_TH1D->SetLineStyle(lineStyle);
     Jet_148822_149294_Dec22_TH1D->SetLineWidth(lineWidth);
  }
  if(bJetData){
    JetData_TH1D->SetMarkerColor(colour);
    JetData_TH1D->SetMarkerStyle(marker);
    JetData_TH1D->SetMarkerSize(GlobalMarkerSize);
    JetData_TH1D->SetLineColor(colour);
    JetData_TH1D->SetLineStyle(lineStyle);
    JetData_TH1D->SetLineWidth(lineWidth);
  }
}



void MyPlotter::SetHistoStyle_SignalM90(void){
  Color_t colour = kRed+1-ColourCounter*(2);
  Style_t marker = kFullStar;
 
  TTToHplusBWB_M90_TH1D->SetFillColor(colour);
  TTToHplusBWB_M90_TH1D->SetLineColor(colour);
  // TTToHplusBWB_M90_TH1D->SetFillStyle(3002);
  if(bEnableHistoMarkers){
    TTToHplusBWB_M90_TH1D->SetMarkerColor(colour);
    TTToHplusBWB_M90_TH1D->SetMarkerStyle(marker);
    TTToHplusBWB_M90_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
}

void MyPlotter::SetHistoStyle_SignalM100(void){
  Color_t colour = kRed-ColourCounter*(2);
  Style_t marker = kFullStar;

  TTToHplusBWB_M100_TH1D->SetFillColor(colour);
  TTToHplusBWB_M100_TH1D->SetLineColor(colour);
  // TTToHplusBWB_M100_TH1D->SetFillStyle(3002);
  if(bEnableHistoMarkers){
    TTToHplusBWB_M100_TH1D->SetMarkerColor(colour);
    TTToHplusBWB_M100_TH1D->SetMarkerStyle(marker);
    TTToHplusBWB_M100_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
}

void MyPlotter::SetHistoStyle_SignalM120(void){
  Color_t colour = kRed-ColourCounter*(2);
  Style_t marker = kFullStar;
  
  TTToHplusBWB_M120_TH1D->SetFillColor(colour);
  TTToHplusBWB_M120_TH1D->SetLineColor(colour);
  // TTToHplusBWB_M120_TH1D->SetFillStyle(3002);
  if(bEnableHistoMarkers){
    TTToHplusBWB_M120_TH1D->SetMarkerColor(colour);
    TTToHplusBWB_M120_TH1D->SetMarkerStyle(marker);
    TTToHplusBWB_M120_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
}

void MyPlotter::SetHistoStyle_SignalM140(void){
  Color_t colour = kMagenta-ColourCounter*(2);
  Style_t marker = kFullStar;

  TTToHplusBWB_M140_TH1D->SetFillColor(colour);
  TTToHplusBWB_M140_TH1D->SetLineColor(colour);
  if(bEnableHistoMarkers){
    TTToHplusBWB_M140_TH1D->SetMarkerColor(colour);
    TTToHplusBWB_M140_TH1D->SetMarkerStyle(marker);
    TTToHplusBWB_M140_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
}

void MyPlotter::SetHistoStyle_SignalM160(void){
  Color_t colour = kCyan-ColourCounter*(2);
  Style_t marker = kFullStar;

  TTToHplusBWB_M160_TH1D->SetFillColor(colour);
  TTToHplusBWB_M160_TH1D->SetLineColor(colour);
  if(bEnableHistoMarkers){
    TTToHplusBWB_M160_TH1D->SetMarkerColor(colour);
    TTToHplusBWB_M160_TH1D->SetMarkerStyle(marker);
    TTToHplusBWB_M160_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
}



void MyPlotter::SetHistoStyle_QCD_Pt30to50(void){
  //  Color_t colour = kYellow+2-ColourCounter*(2);
  Color_t colour = kRed+2-ColourCounter*(2);
  Style_t marker = kFullTriangleUp;
  if(ColourCounter == 2){
    marker = kFullTriangleDown;
    colour = kRed;
  }
  
  QCD_Pt30to50_TH1D->SetFillColor(colour);
  // QCD_Pt30to50_TH1D->SetFillStyle(3002);
  QCD_Pt30to50_TH1D->SetLineColor(colour);
  // QCD_Pt30to50_TH1D->SetLineColor(kBlack);
  QCD_Pt30to50_TH1D->SetLineWidth(2);
  if(bEnableHistoMarkers){
    QCD_Pt30to50_TH1D->SetMarkerColor(colour);
    QCD_Pt30to50_TH1D->SetMarkerStyle(marker);
    QCD_Pt30to50_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
}  

void MyPlotter::SetHistoStyle_QCD_Pt50to80(void){
  // Color_t colour = kYellow+2-ColourCounter*(2);
  Color_t colour = kRed+2-ColourCounter*(2);
  Style_t marker = kFullTriangleUp;
  if(ColourCounter == 2){
    marker = kFullTriangleDown;
    colour = kRed;
  }

  QCD_Pt50to80_TH1D->SetFillColor(colour);
  // QCD_Pt50to80_TH1D->SetFillStyle(3002);
  QCD_Pt50to80_TH1D->SetLineColor(colour);
  // QCD_Pt50to80_TH1D->SetLineColor(kBlack);
  QCD_Pt50to80_TH1D->SetLineWidth(2);
  if(bEnableHistoMarkers){
    QCD_Pt50to80_TH1D->SetMarkerColor(colour);
    QCD_Pt50to80_TH1D->SetMarkerStyle(marker);
    QCD_Pt50to80_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
} 

void MyPlotter::SetHistoStyle_QCD_Pt80to120(void){
  // Color_t colour = kYellow+2-ColourCounter*(2);
  Color_t colour = kRed+2-ColourCounter*(2);
  Style_t marker = kFullTriangleUp;
  if(ColourCounter == 2){
    marker = kFullTriangleDown;
    colour = kRed;
  }

  QCD_Pt80to120_TH1D->SetFillColor(colour);
  // QCD_Pt80to120_TH1D->SetFillStyle(3002);
  QCD_Pt80to120_TH1D->SetLineColor(colour);
  // QCD_Pt80to120_TH1D->SetLineColor(kBlack);
  QCD_Pt80to120_TH1D->SetLineWidth(2);
  if(bEnableHistoMarkers){
    QCD_Pt80to120_TH1D->SetMarkerColor(colour);
    QCD_Pt80to120_TH1D->SetMarkerStyle(marker);
    QCD_Pt80to120_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
} 

void MyPlotter::SetHistoStyle_QCD_Pt120to170(void){
  // Color_t colour = kYellow+2-ColourCounter*(2);
  Color_t colour = kRed+2-ColourCounter*(2);
  Style_t marker = kFullTriangleUp;
  if(ColourCounter == 2){
    marker = kFullTriangleDown;
    colour = kRed;
  }

  QCD_Pt120to170_TH1D->SetFillColor(colour);
  // QCD_Pt120to170_TH1D->SetFillStyle(3002);
  QCD_Pt120to170_TH1D->SetLineColor(colour);
  // QCD_Pt120to170_TH1D->SetLineColor(kBlack);
  QCD_Pt120to170_TH1D->SetLineWidth(2);
  if(bEnableHistoMarkers){
    QCD_Pt120to170_TH1D->SetMarkerColor(colour);
    QCD_Pt120to170_TH1D->SetMarkerStyle(marker);
    QCD_Pt120to170_TH1D->SetMarkerSize(GlobalMarkerSize);
    }
} 

void MyPlotter::SetHistoStyle_QCD_Pt170to300(void){
  // Color_t colour = kYellow+2-ColourCounter*(2);
  Color_t colour = kRed+2-ColourCounter*(2);
  Style_t marker = kFullTriangleUp;
  if(ColourCounter == 2){
    marker = kFullTriangleDown;
    colour = kRed;
  }

  QCD_Pt170to300_TH1D->SetFillColor(colour);
  // QCD_Pt170to300_TH1D->SetFillStyle(3002);
  QCD_Pt170to300_TH1D->SetLineColor(colour);
  // QCD_Pt170to300_TH1D->SetLineColor(kBlack);
  QCD_Pt170to300_TH1D->SetLineWidth(2);
  if(bEnableHistoMarkers){
    QCD_Pt170to300_TH1D->SetMarkerColor(colour);
    QCD_Pt170to300_TH1D->SetMarkerStyle(marker);
    QCD_Pt170to300_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
} 

void MyPlotter::SetHistoStyle_QCD_Pt300to470(void){
  // Color_t colour = kYellow+2-ColourCounter*(2);
  Color_t colour = kRed+2-ColourCounter*(2);
  Style_t marker = kFullTriangleUp;
  if(ColourCounter == 2){
    marker = kFullTriangleDown;
    colour = kRed;
  }

  QCD_Pt300to470_TH1D->SetFillColor(colour);
  // QCD_Pt300to470_TH1D->SetFillStyle(3002);
  QCD_Pt300to470_TH1D->SetLineColor(colour);
  // QCD_Pt300to470_TH1D->SetLineColor(kBlack);
  QCD_Pt300to470_TH1D->SetLineWidth(2);
  if(bEnableHistoMarkers){
    QCD_Pt300to470_TH1D->SetMarkerColor(colour);
    QCD_Pt300to470_TH1D->SetMarkerStyle(marker);
    QCD_Pt300to470_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
} 

void MyPlotter::SetHistoStyle_QCD(void){
  
  Color_t colour = kRed+3;
  Style_t marker = kFullTriangleUp;
  int lineStyle = 2;
  int lineWidth = 2;
 
  if( (SuperimposeCounter==0) || (ColourCounter==0) ){
    colour = kRed+3;
    marker = kFullTriangleUp;
    lineStyle = 4;
    lineWidth = 4;
  
    QCD_TH1D->SetFillColor(colour);
    QCD_TH1D->SetLineColor(colour);
    QCD_TH1D->SetLineWidth(lineWidth);
    if(bTransparentHistos) QCD_TH1D->SetFillStyle(3001);
    if(bEnableHistoMarkers){
      QCD_TH1D->SetMarkerColor(colour);
      QCD_TH1D->SetMarkerStyle(marker);
      QCD_TH1D->SetMarkerSize(GlobalMarkerSize);
      // QCD_TH1D->SetLineColor(colour);
      // QCD_TH1D->SetLineWidth(lineWidth);
    }  
  }
  
  if( (SuperimposeCounter==1) || (ColourCounter==1) ){
    colour = kRed;
    marker = kFullTriangleUp;
    lineStyle = 4;
    lineWidth = 4;
    
    QCD_TH1D->SetMarkerColor(colour);
    QCD_TH1D->SetMarkerStyle(marker);
    QCD_TH1D->SetMarkerSize(GlobalMarkerSize);
    // QCD_TH1D->SetLineColor(colour);
    // QCD_TH1D->SetLineWidth(lineWidth);
  } 
  
  if( (SuperimposeCounter==2) || (ColourCounter==2) ){
    colour = kRed-9;
    marker = kFullTriangleUp;
    lineStyle = 4;
    lineWidth = 4;
    
    QCD_TH1D->SetMarkerColor(colour);
    QCD_TH1D->SetMarkerStyle(marker);
    QCD_TH1D->SetMarkerSize(GlobalMarkerSize);
    // QCD_TH1D->SetLineColor(colour);
    // QCD_TH1D->SetLineWidth(lineWidth);
  }
    
}



void MyPlotter::SetHistoStyle_WJets(void){
  
  Color_t colour = kGreen;
  Style_t marker = kFullTriangleDown;


  if( (SuperimposeCounter==0) || (ColourCounter==0) ){
    
    colour = kGreen+3;
    marker = kFullTriangleDown;
    
    WJets_TH1D->SetFillColor(colour);
    WJets_TH1D->SetLineColor(colour);
    WJets_TH1D->SetLineWidth(4);
    if(bTransparentHistos) WJets_TH1D->SetFillStyle(3002);
    if(bEnableHistoMarkers){
      WJets_TH1D->SetMarkerColor(colour);
      WJets_TH1D->SetMarkerStyle(marker);
      WJets_TH1D->SetMarkerSize(GlobalMarkerSize);
    }
  }
    
  if( (SuperimposeCounter==1) || (ColourCounter==1) ){
    
    Color_t colour = kGreen;
    Style_t marker = kFullTriangleDown;
   
    WJets_TH1D->SetMarkerColor(colour);
    WJets_TH1D->SetMarkerStyle(marker);
    WJets_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
  
  if( (SuperimposeCounter==2) || (ColourCounter==2) ){
    Color_t colour = kGreen-9;
    Style_t marker = kFullTriangleDown;
    
    WJets_TH1D->SetMarkerColor(colour);
    WJets_TH1D->SetMarkerStyle(marker);
    WJets_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
}



void MyPlotter::SetHistoStyle_TTJets(void){
  
  if( (SuperimposeCounter==0) || (ColourCounter==0) ){
    
    Color_t colour = kBlue+3;
    Style_t marker = kFullSquare;
    
    TTJets_TH1D->SetFillColor(colour);
    TTJets_TH1D->SetLineColor(colour);
    TTJets_TH1D->SetLineWidth(4);
    if(bTransparentHistos) TTJets_TH1D->SetFillStyle(3003);
    if(bEnableHistoMarkers){
      TTJets_TH1D->SetMarkerColor(colour);
      TTJets_TH1D->SetMarkerStyle(marker);
      TTJets_TH1D->SetMarkerSize(GlobalMarkerSize);
    }
  }
    
  if( (SuperimposeCounter==1) || (ColourCounter==1) ){
    
    Color_t colour = kCyan;
    Style_t marker = kFullSquare;
    
    TTJets_TH1D->SetMarkerColor(colour);
    TTJets_TH1D->SetMarkerStyle(marker);
    TTJets_TH1D->SetMarkerSize(GlobalMarkerSize);
  } 
  
  if( (SuperimposeCounter==2) || (ColourCounter==2) ){
    Color_t colour = kBlue-9;
    Style_t marker = kFullSquare;
    
    TTJets_TH1D->SetMarkerColor(colour);
    TTJets_TH1D->SetMarkerStyle(marker);
    TTJets_TH1D->SetMarkerSize(GlobalMarkerSize);
  }
}



void MyPlotter::SetHistoStyle_WJets_noPU(void){
  Color_t colour = kOrange+3-ColourCounter*(2);
  //  Style_t marker = kOpenDiamond;
  Style_t marker = 33; // kFullDiamond
  
  WJets_noPU_TH1D->SetFillColor(colour);
  // WJets_TH1D->SetFillStyle(3002);
  WJets_noPU_TH1D->SetLineColor(colour);
  WJets_noPU_TH1D->SetLineWidth(2);
  if(bEnableHistoMarkers){
      WJets_noPU_TH1D->SetMarkerColor(colour);
      WJets_noPU_TH1D->SetMarkerStyle(marker);
      WJets_noPU_TH1D->SetMarkerSize(GlobalMarkerSize);
    }
}



void MyPlotter::CreateCanvas(void){
  
  CanvasCounter++;
  TString cName = histoName;
  char cCounter[100];
  sprintf(cCounter,"%.0i", CanvasCounter); 
  canvas = new TCanvas( TString(cName) + TString(cCounter), TString(cName) + TString(cCounter), 1);
  canvas->cd();
}



void MyPlotter::CreateDumbieHisto(void){
  /// Reset this histogram: contents, errors, etc..
  /// if option "ICE" is specified, resets only Integral, Contents and Errors.
  /// if option "M" is specified, resets also Minimum and Maximum

  if(bJetData)                dumbieHisto = (TH1D*)JetData_TH1D->Clone();
  else if(bTauData)           dumbieHisto = (TH1D*)TauData_TH1D->Clone();
  else if(bQCD_TFile && bQCD) dumbieHisto = (TH1D*)QCD_TH1D->Clone();
  else if(bWJets_TFile)       dumbieHisto = (TH1D*)WJets_TH1D->Clone();
  else if(bWJets_noPU_TFile)  dumbieHisto = (TH1D*)WJets_noPU_TH1D->Clone();
  else if(bTTJets_TFile)      dumbieHisto = (TH1D*)TTJets_TH1D->Clone();
  else{
    std::cout << "*** ERROR! All histograms are empty" << std::endl;
  }
  // dumbieHisto->Reset("ICE");
  // dumbieHisto->Reset();
  // dumbieHisto->GetXaxis()->SetTitleOffset(1.1);
  // dumbieHisto->GetYaxis()->SetTitleOffset(1.3);

}


void MyPlotter::AddCmsPreliminaryText(void){
  TLatex *cmsPrelim = new TLatex();
  cmsPrelim->SetNDC();
  cmsPrelim->DrawLatex(0.72, 0.96, "CMS Preliminary");
}


void MyPlotter::AddEnergy7TeVText(void){
  TLatex *lhcEnergy = new TLatex();
  lhcEnergy->SetNDC();
  lhcEnergy->DrawLatex(0.2, 0.96, "#sqrt{s} = 7 TeV");
}


void MyPlotter::AddLuminosityText(TString lumi, TString unit){
  TLatex *lhcLumi = new TLatex();
  lhcLumi->SetNDC();
  lhcLumi->DrawLatex(0.2, 0.85, "#int L dt = " + TString(lumi) + TString(unit));
}


void MyPlotter::GetJetDataLumis(void){

  /// Jet Data
  if(bJetMETTau_Jet_136035_141881_Dec22_TFile) GetHistoLumi(JetMETTau_Jet_136035_141881_Dec22_TFile);
  if(bJetMET_141956_144114_Dec22_TFile) GetHistoLumi(JetMET_141956_144114_Dec22_TFile);
  if(bJet_146428_148058_Dec22_TFile) GetHistoLumi(Jet_146428_148058_Dec22_TFile);
  if(bJet_148822_149294_Dec22_TFile) GetHistoLumi(Jet_148822_149294_Dec22_TFile);
}



void MyPlotter::GetTauDataLumis(void){

  /// TauData
  if(bJetMETTau_Tau_136035_139975_Dec22_TFile) GetHistoLumi(JetMETTau_Tau_136035_139975_Dec22_TFile);
  if(bJetMETTau_Tau_140058_141881_Dec22_TFile) GetHistoLumi(JetMETTau_Tau_140058_141881_Dec22_TFile);
  if(BTau_141956_144114_Dec22_TFile) GetHistoLumi(BTau_141956_144114_Dec22_TFile);
  if(BTau_146428_148058_Dec22_TFile) GetHistoLumi(BTau_146428_148058_Dec22_TFile);
  if(bBTau_148822_149182_Dec22_TFile) GetHistoLumi(BTau_148822_149182_Dec22_TFile);

}


void MyPlotter::AccumulateTauDataLumi(const float lumi){

  TotalTauDataHistoLumi  = TotalTauDataHistoLumi + lumi;
  // std::cout << "*** TotalHistoLumi = " << TotalHistoLumi << std::endl;
}


void MyPlotter::AccumulateJetDataLumi(const float lumi){

  TotalJetDataHistoLumi = TotalJetDataHistoLumi + lumi;
  // std::cout << "*** TotalHistoLumi = " << TotalHistoLumi << std::endl;
}



void MyPlotter::GetHistoLumi(TFile *f){

  // if( TString(histo->GetXaxis()->GetBinLabel(1)).CompareTo("control") == 0) std::cout << "Found control bin!" << std::endl;
  // if( TString(histo->GetXaxis()->GetBinLabel(2)).CompareTo("luminosity") == 0) std::cout << "Found lumi bin!" << std::endl;

  TH1D *histo;
  histo = new TH1D;

  histo = (TH1D*)f->Get("configInfo/configinfo");

  float control = histo->GetBinContent(1);
  float luminosity = histo->GetBinContent(2);

  float histoLumi = luminosity/control;
  std::cout << "*** Notification! Read luminosity from TFile " << f->GetName() << ". The histoLumi = " << histoLumi << std::endl;
  if(bJetData) AccumulateJetDataLumi(histoLumi);
  else if(bTauData) AccumulateTauDataLumi(histoLumi);

}



void MyPlotter::GetHistoLuminosities(void){
  
  if(bJetData) GetJetDataLumis();
  if(bTauData) GetTauDataLumis();
}



void MyPlotter::AddHistoLegends(TString legTitle){
  
  /// Customize Legened
  myLegend = new TLegend(x1Leg, y1Leg, x2Leg, y2Leg, NULL,"brNDC");    
  if(legTitle.CompareTo("none") != 0 ) myLegend->SetHeader(legTitle);
  myLegend->SetFillColor(kWhite);
  myLegend->SetLineColor(kBlack);
  myLegend->SetBorderSize(1);
  myLegend->SetShadowColor(kWhite);
  myLegend->SetTextSize(0.022);
  myLegend->SetTextFont(62);

  if(bEnableHistoMarkers){
    // std::cout << "*** Notification! Histogram markers are enabled" << std::endl;
    if(bJetData) myLegend->AddEntry(JetData_TH1D, "JetData", "lp" );
    if(bTauData) myLegend->AddEntry(TauData_TH1D, "Data", "lp" );
    if(bTTToHplusBWB_M90_TFile)  myLegend->AddEntry(TTToHplusBWB_M90_TH1D,  "H^{#pm} M= 90 GeVc^{-2}", "p" );
    if(bTTToHplusBWB_M100_TFile) myLegend->AddEntry(TTToHplusBWB_M100_TH1D, "H^{#pm} M= 100 GeVc^{-2}", "p" );
    if(bTTToHplusBWB_M120_TFile) myLegend->AddEntry(TTToHplusBWB_M120_TH1D, "H^{#pm} M= 120 GeVc^{-2}", "p" );
    if(bTTToHplusBWB_M140_TFile) myLegend->AddEntry(TTToHplusBWB_M140_TH1D, "H^{#pm} M= 140 GeVc^{-2}", "p" );
    if(bTTToHplusBWB_M160_TFile) myLegend->AddEntry(TTToHplusBWB_M160_TH1D, "H^{#pm} M= 160 GeVc^{-2}", "p" );
    if(bQCD_TFile && bQCD ) myLegend->AddEntry( QCD_TH1D , "QCD", "p" );
    if(bTTJets_TFile) myLegend->AddEntry( TTJets_TH1D, "t#bar{t}+jets", "p" );
    if(bWJets_TFile) myLegend->AddEntry( WJets_TH1D, "W+jets", "p" );
    if(bWJets_noPU_TFile) myLegend->AddEntry( WJets_noPU_TH1D, "W+jets (no PU)", "p" );
  }
  else{
    // std::cout << "*** Notification! Histogram markers are disabled" << std::endl;
    if(bJetData) myLegend->AddEntry(JetData_TH1D, "JetData", "lp" );
    if(bTauData) myLegend->AddEntry(TauData_TH1D, "Data", "lp" );
    if(bTTToHplusBWB_M90_TFile)  myLegend->AddEntry(TTToHplusBWB_M90_TH1D,  "H^{#pm} M = 90 GeVc^{-2}", "f" );
    if(bTTToHplusBWB_M100_TFile) myLegend->AddEntry(TTToHplusBWB_M100_TH1D, "H^{#pm} M = 100 GeVc^{-2}", "f" );
    if(bTTToHplusBWB_M120_TFile) myLegend->AddEntry(TTToHplusBWB_M120_TH1D, "H^{#pm} M = 120 GeVc^{-2}", "f" );
    if(bTTToHplusBWB_M140_TFile) myLegend->AddEntry(TTToHplusBWB_M140_TH1D, "H^{#pm} M = 140 GeVc^{-2}", "f" );
    if(bTTToHplusBWB_M160_TFile) myLegend->AddEntry(TTToHplusBWB_M160_TH1D, "H^{#pm} M = 160 GeVc^{-2}", "f" );
    if(bQCD_TFile) myLegend->AddEntry( QCD_TH1D , "QCD", "f" );
    if(bTTJets_TFile) myLegend->AddEntry( TTJets_TH1D, "t#bar{t}+jets", "f" );
    if(bWJets_TFile) myLegend->AddEntry( WJets_TH1D, "W+jets", "f" );
    if(bWJets_noPU_TFile) myLegend->AddEntry( WJets_noPU_TH1D, "W+jets (no PU)", "f" );
  }

    myLegend->Draw();
    canvas->Update();
}



void MyPlotter::AddHistoLegends(TString legTitle, float x1, float y1, float x2, float y2){

  /// Overwrite the global Legend positions
  x1Leg = x1;
  y1Leg = y1;
  x2Leg = x2;
  y2Leg = y2;
  xLegLength = x2Leg-x1Leg;
  yLegLength = y2Leg-y1Leg;

  /// Customize Legened
  myLegend = new TLegend(x1Leg, y1Leg, x2Leg, y2Leg, NULL,"brNDC");
  if(legTitle.CompareTo("none") != 0 ) myLegend->SetHeader(legTitle);
  // myLegend->SetFillStyle(3001);
  myLegend->SetFillColor(kWhite);
  myLegend->SetLineColor(kBlack);
  myLegend->SetBorderSize(1);
  myLegend->SetShadowColor(kWhite);
  myLegend->SetTextSize(0.022);
  myLegend->SetTextFont(62);

  if(bEnableHistoMarkers){
    // std::cout << "*** Notification! Histogram markers are enabled" << std::endl;
  
    if(bJetData) myLegend->AddEntry(JetData_TH1D, "JetData", "lp" );
    if(bTauData) myLegend->AddEntry(TauData_TH1D, "Data", "lp" );
    if(bTTToHplusBWB_M90_TFile)  myLegend->AddEntry(TTToHplusBWB_M90_TH1D,  "H^{#pm} M= 90 GeVc^{-2}", "p" );
    if(bTTToHplusBWB_M100_TFile) myLegend->AddEntry(TTToHplusBWB_M100_TH1D, "H^{#pm} M= 100 GeVc^{-2}", "p" );
    if(bTTToHplusBWB_M120_TFile) myLegend->AddEntry(TTToHplusBWB_M120_TH1D, "H^{#pm} M= 120 GeVc^{-2}", "p" );
    if(bTTToHplusBWB_M140_TFile) myLegend->AddEntry(TTToHplusBWB_M140_TH1D, "H^{#pm} M= 140 GeVc^{-2}", "p" );
    if(bTTToHplusBWB_M160_TFile) myLegend->AddEntry(TTToHplusBWB_M160_TH1D, "H^{#pm} M= 160 GeVc^{-2}", "p" );
    if(bQCD_TFile && bQCD ) myLegend->AddEntry( QCD_TH1D , "QCD", "p" );
    if(bTTJets_TFile) myLegend->AddEntry( TTJets_TH1D, "t#bar{t}+jets", "p" );
    if(bWJets_TFile) myLegend->AddEntry( WJets_TH1D, "W+jets", "p" );
    if(bWJets_noPU_TFile) myLegend->AddEntry( WJets_noPU_TH1D, "W+jets (no PU)", "p" );
  }
  else{
    // std::cout << "*** Notification! Histogram markers are disabled" << std::endl;
    
    if(bJetData) myLegend->AddEntry(JetData_TH1D, "JetData", "lp" );
    if(bTauData) myLegend->AddEntry(TauData_TH1D, "Data", "lp" );
    if(bTTToHplusBWB_M90_TFile)  myLegend->AddEntry(TTToHplusBWB_M90_TH1D,  "H^{#pm} M = 90 GeVc^{-2}", "f" );
    if(bTTToHplusBWB_M100_TFile) myLegend->AddEntry(TTToHplusBWB_M100_TH1D, "H^{#pm} M = 100 GeVc^{-2}", "f" );
    if(bTTToHplusBWB_M120_TFile) myLegend->AddEntry(TTToHplusBWB_M120_TH1D, "H^{#pm} M = 120 GeVc^{-2}", "f" );
    if(bTTToHplusBWB_M140_TFile) myLegend->AddEntry(TTToHplusBWB_M140_TH1D, "H^{#pm} M = 140 GeVc^{-2}", "f" );
    if(bTTToHplusBWB_M160_TFile) myLegend->AddEntry(TTToHplusBWB_M160_TH1D, "H^{#pm} M = 160 GeVc^{-2}", "f" );
    if(bQCD_TFile) myLegend->AddEntry( QCD_TH1D , "QCD", "f" );
    if(bTTJets_TFile) myLegend->AddEntry( TTJets_TH1D, "t#bar{t}+jets", "f" );
    if(bWJets_TFile) myLegend->AddEntry( WJets_TH1D, "W+jets", "f" );
    if(bWJets_noPU_TFile) myLegend->AddEntry( WJets_noPU_TH1D, "W+jets (no PU)", "p" );
  }

    myLegend->Draw();
    canvas->Update();
}



void MyPlotter::EnableHistoMarkers(const bool enable){
  bEnableHistoMarkers= enable;
}



void MyPlotter::CustomizeHisto(float xMin, float xMax, float yMin, float yMax, TString xTitle, TString yTitle, bool setLogy){
  
  // gPad->SetLogy(setLogy);
  canvas->SetLogy(setLogy);
  dumbieHisto->GetXaxis()->SetRangeUser(xMin, xMax);
  dumbieHisto->GetYaxis()->SetRangeUser(yMin, yMax);
  if(xTitle.CompareTo("none") !=0) dumbieHisto->GetXaxis()->SetTitle(xTitle);
  if(yTitle.CompareTo("none") !=0) dumbieHisto->GetYaxis()->SetTitle(yTitle);

}


void MyPlotter::CustomizeHisto(float yMin, float yMax, TString xTitle, TString yTitle, bool setLogy){
  
  // gPad->SetLogy(setLogy);
  canvas->SetLogy(setLogy);
  dumbieHisto->GetYaxis()->SetRangeUser(yMin, yMax);
  if(xTitle.CompareTo("none") !=0) dumbieHisto->GetXaxis()->SetTitle(xTitle);
  if(yTitle.CompareTo("none") !=0) dumbieHisto->GetYaxis()->SetTitle(yTitle);

}



void MyPlotter::SaveCanvas(char *fullName){

  canvas->SaveAs(TString(fullName) + ".png");
  canvas->SaveAs(TString(fullName) + ".pdf");
  canvas->SaveAs(TString(fullName) + ".C");
  canvas->SaveAs(TString(fullName) + ".eps");
  canvas->SaveAs(TString(fullName) + ".ps");

}


void MyPlotter::SaveCanvas(void){
  char tmpName[10];
  sprintf(tmpName,"c%.0i", CanvasCounter);

  canvas->SaveAs(TString(tmpName) + ".png");
  canvas->SaveAs(TString(tmpName) + ".pdf");
  canvas->SaveAs(TString(tmpName) + ".C");
  canvas->SaveAs(TString(tmpName) + ".eps");
  canvas->SaveAs(TString(tmpName) + ".ps");

}



void MyPlotter::ChangeHistoColours(void){
  ColourCounter++;
  }


void MyPlotter::TransparentHistos(void){
  bTransparentHistos = true;
  }


void MyPlotter::SetCustomLumi(float newLumi){
  bOverwriteIntegratedLumi = true;
  IntegratedLumi = newLumi;
}


void MyPlotter::SetGlobalMarkerSize(float newGlobalMarkerSize){
  GlobalMarkerSize = newGlobalMarkerSize;
}


void MyPlotter::PrintCfgParameters(void){
  // TDirectory(TString(GlobalFolder)) *myFolder;
  TDirectory *myFolder;
  myFolder = new TDirectory;
  
  // TDirectory() *myFolder;
  // myFolder->SetName(GlobalFolder);
  // std::cout << "myFolder = " << myFolder << std::endl;
  // myFolder->cd();
  // std::cout << " *** Notification! Parameters used were:\n" << parameteSet->GetTitle() << std::endl;
}

//#######################################################################
// -*- C++ -*-
//       File Name:  MyPlotterClass.h
// Original Author:  Alexandros Attikis
//         Created:  09 Feb 2011
//     Description:  Common functions used for TH1
//       Institute:  UCY
//         e-mail :  attikis@cern.ch
//        Comments:  
//#######################################################################

/// System includes
#include <iostream>
#include <vector>

/// ROOT libraries
#include <TH1D.h>
#include <TFile.h>
#include <TString.h>
#include <THStack.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TLatex.h>
#include <TMath.h>
#include <TPad.h>
#include <TVirtualPad.h>


class MyPlotter{

 public:
  /// Variables
  int CanvasCounter; // enables having several canvases with same name but different number
  int SuperimposeCounter;  // Supports up to 3 superpositions of datasets sets
  int ColourCounter; // changes the colour-set
  float GlobalMarkerSize;
  float x1Leg;
  float y1Leg;
  float xLegLength;
  float yLegLength;
  float x2Leg;
  float y2Leg;
  float TotalJetDataHistoLumi;
  float TotalTauDataHistoLumi;
  const char *GlobalFolder;

  /// JetData
  TFile *JetMETTau_Jet_136035_141881_Dec22_TFile;
  TFile *JetMET_141956_144114_Dec22_TFile;
  TFile *Jet_146428_148058_Dec22_TFile;
  TFile *Jet_148822_149294_Dec22_TFile;
  /// TauData
  TFile *JetMETTau_Tau_136035_139975_Dec22_TFile;
  TFile *JetMETTau_Tau_140058_141881_Dec22_TFile;
  TFile *BTau_141956_144114_Dec22_TFile;
  TFile *BTau_146428_148058_Dec22_TFile;
  TFile *BTau_148822_149182_Dec22_TFile;
  /// MC
  TFile *TTToHplusBWB_M90_TFile;
  TFile *TTToHplusBWB_M100_TFile;
  TFile *TTToHplusBWB_M120_TFile;
  TFile *TTToHplusBWB_M140_TFile;
  TFile *TTToHplusBWB_M160_TFile;
  TFile *QCD_Pt30to50_TFile;
  TFile *QCD_Pt50to80_TFile;
  TFile *QCD_Pt80to120_TFile;
  TFile *QCD_Pt120to170_TFile;
  TFile *QCD_Pt170to300_TFile;
  TFile *QCD_Pt300to470_TFile;
  TFile *TTJets_TFile;
  TFile *WJets_TFile;
  TFile *WJets_noPU_TFile;
    
  THStack *Bkg_THStack;
  THStack *MC_THStack;
  THStack *TauData_THStack;
  THStack *JetData_THStack;
  TH1D *dumbieHisto;
  /// JetData
  TH1D *JetMETTau_Jet_136035_141881_Dec22_TH1D;
  TH1D *JetMET_141956_144114_Dec22_TH1D;
  TH1D *Jet_146428_148058_Dec22_TH1D;
  TH1D *Jet_148822_149294_Dec22_TH1D;
  TH1D *JetMETTau_Tau_136035_139975_Dec22_TH1D;
  TH1D *JetMETTau_Tau_140058_141881_Dec22_TH1D;
  /// TauData
  TH1D *BTau_141956_144114_Dec22_TH1D;
  TH1D *BTau_146428_148058_Dec22_TH1D;
  TH1D *BTau_148822_149182_Dec22_TH1D;
  TH1D *TTToHplusBWB_M90_TH1D;
  TH1D *TTToHplusBWB_M100_TH1D;
  TH1D *TTToHplusBWB_M120_TH1D;
  TH1D *TTToHplusBWB_M140_TH1D;
  TH1D *TTToHplusBWB_M160_TH1D;
  // MC
  TH1D *QCD_TH1D;
  TH1D *JetData_TH1D;
  TH1D *TauData_TH1D;
  TH1D *BTau_TH1D;
  TH1D *JetMETTau_TH1D;
  TH1D *QCD_Pt30to50_TH1D;
  TH1D *QCD_Pt50to80_TH1D;
  TH1D *QCD_Pt80to120_TH1D;
  TH1D *QCD_Pt120to170_TH1D;
  TH1D *QCD_Pt170to300_TH1D;
  TH1D *QCD_Pt300to470_TH1D;
  TH1D *TTJets_TH1D;
  TH1D *WJets_TH1D;
  TH1D *WJets_noPU_TH1D;

  TCanvas *canvas;
  TLegend *myLegend;
  TString canvasName;
  TString MC_Tune;
  TString histoName;
  TString fullHistoName;
  float IntegratedLumi;
  
  bool bApplyWeights;
  bool bOverwriteIntegratedLumi;
  bool bEnableHistoMarkers;
  bool bTransparentHistos;

  /// JetData
  bool bJetMETTau_Jet_136035_141881_Dec22_TFile;
  bool bJetMET_141956_144114_Dec22_TFile;
  bool bJet_146428_148058_Dec22_TFile;
  bool bJet_148822_149294_Dec22_TFile;
  /// TauData 
  bool bJetMETTau_Tau_136035_139975_Dec22_TFile;
  bool bJetMETTau_Tau_140058_141881_Dec22_TFile;
  bool bBTau_141956_144114_Dec22_TFile;
  bool bBTau_146428_148058_Dec22_TFile;
  bool bBTau_148822_149182_Dec22_TFile;
  /// MC
  bool bTTToHplusBWB_M90_TFile;
  bool bTTToHplusBWB_M100_TFile;
  bool bTTToHplusBWB_M120_TFile;
  bool bTTToHplusBWB_M140_TFile;
  bool bTTToHplusBWB_M160_TFile;
  bool bQCD_TFile;
  bool bQCD_Pt30to50_TFile;
  bool bQCD_Pt50to80_TFile;
  bool bQCD_Pt80to120_TFile;
  bool bQCD_Pt120to170_TFile;
  bool bQCD_Pt170to300_TFile;
  bool bQCD_Pt300to470_TFile;
  bool bTTJets_TFile;
  bool bWJets_TFile;
  bool bWJets_noPU_TFile;

  bool bTauData;
  bool bJetData;
  bool bSignal;
  bool bMC;
  bool bBTau;
  bool bJetMETTau;
  /// JetData
  bool bJetMETTau_Jet_136035_141881_Dec22;
  bool bJetMET_141956_144114_Dec22;
  bool bJet_146428_148058_Dec22;
  bool bJet_148822_149294_Dec22;
  /// TauData
  bool bJetMETTau_Tau_140058_141881_Dec22;
  bool bJetMETTau_Tau_136035_139975_Dec22;
  bool bBTau_141956_144114_Dec22;
  bool bBTau_146428_148058_Dec22;
  bool bBTau_148822_149182_Dec22;
  /// MC 
  bool bTTToHplusBWB_M90;
  bool bTTToHplusBWB_M100;
  bool bTTToHplusBWB_M120;
  bool bTTToHplusBWB_M140;
  bool bTTToHplusBWB_M160;
  bool bQCD;
  bool bQCD_Pt30to50;
  bool bQCD_Pt50to80;
  bool bQCD_Pt80to120;
  bool bQCD_Pt120to170;
  bool bQCD_Pt170to300;
  bool bQCD_Pt300to470;
  bool bTTJets;
  bool bWJets;
  bool bWJets_noPU;
  
  float TTToHplusBWB_M90_Xsection;
  float TTToHplusBWB_M100_Xsection;
  float TTToHplusBWB_M120_Xsection;
  float TTToHplusBWB_M140_Xsection;
  float TTToHplusBWB_M160_Xsection;
  // float QCD_Xsection;
  float QCD_Pt30to50_Xsection;
  float QCD_Pt50to80_Xsection;
  float QCD_Pt80to120_Xsection;
  float QCD_Pt120to170_Xsection;
  float QCD_Pt170to300_Xsection;
  float QCD_Pt300to470_Xsection;
  float TTJets_Xsection;
  float WJets_Xsection;
  float WJets_noPU_Xsection;

  float TTToHplusBWB_M90_AllEvents;
  float TTToHplusBWB_M100_AllEvents;
  float TTToHplusBWB_M120_AllEvents;
  float TTToHplusBWB_M140_AllEvents;
  float TTToHplusBWB_M160_AllEvents;
  // float QCD_AllEvents;
  float QCD_Pt30to50_AllEvents;
  float QCD_Pt50to80_AllEvents;
  float QCD_Pt80to120_AllEvents;
  float QCD_Pt120to170_AllEvents;
  float QCD_Pt170to300_AllEvents;
  float QCD_Pt300to470_AllEvents;
  float TTJets_AllEvents;
  float WJets_AllEvents;
  float WJets_noPU_AllEvents;

  TString cmssw_x_y_z;
  
  /// Functions
  void InitializeOnce(void);
  void Initialize(const TString tune, const char* multicrab_dir, const char* folder, const char *histo);
  void ActivateAllDataAndMC(void); 
  void ActivateAllData(void); 
  void ActivateTauData(void); 
  void ActivateJetData(void); 
  void ActivateAllMC(void); 
  void PrintActiveDatasets(void); 
  void PrintCfgParameters(void); 
  void PrintMCXsections(void);  
  void PrintMCNormFactors(void); 
  void GetMCWeights(void);
  void RemoveDatasets(std::vector<TString> myDatasetVector);  
  void AddDatasets(std::vector<TString> myDatasetVector);  
  void Draw(char *options);
  void AddHistoLegends(TString legTitle);
  void AddHistoLegends(TString legTitle, float x1, float y1, float x2, float y2);
  void EnableHistoMarkers(const bool enable); 
  void CustomizeHisto(float yMin, float yMax, TString xTitle, TString yTitle, bool setLogy); 
  void CustomizeHisto(float xMin, float xMax, float yMin, float yMax, TString xTitle, TString yTitle, bool setLogy);  
  void DrawSuperimposed(char *options, TString legTitle); 
  void SaveCanvas(void); 
  void SaveCanvas(char *fullName); 
  void ChangeHistoColours(void);  
  void SetGlobalMarkerSize(float newGlobalMarkerSize);
  void TransparentHistos(void);
  void SetCustomLumi(float newLumi);
  // void NormalizeHistosToUnity(void);

 private:
  /// Variables
  float TTToHplusBWB_M90_NormFactor;
  float TTToHplusBWB_M100_NormFactor;
  float TTToHplusBWB_M120_NormFactor;
  float TTToHplusBWB_M140_NormFactor;
  float TTToHplusBWB_M160_NormFactor;
  float QCD_Pt30to50_NormFactor;
  float QCD_Pt50to80_NormFactor;
  float QCD_Pt80to120_NormFactor;
  float QCD_Pt120to170_NormFactor;
  float QCD_Pt170to300_NormFactor;
  float QCD_Pt300to470_NormFactor;
  float TTJets_NormFactor;
  float WJets_NormFactor;
  float WJets_noPU_NormFactor;
  
  /// Functions
  void InitVariables(void); 
  void InitHistos(void); 
  void GetRootFiles(const char* multicrab_dir);  
  bool CheckTFile(TFile* f);  
  float GetHistoXsection(TFile *f); 
  void GetMCXsections(void);   
  float GetHistoAllEvents(TFile* f); 
  void GetHistos(const char *histo); 
  void MergeJetData(void);  
  void MergeTauData(void); 
  void MergeQCD(void); 
  void MergeBTau(void);  
  void MergeJetMETTau(void); 
  void StackMCHistos(void);
  void StackMCHistosDoNotMergeQCD(void);
  void StackTauDataHistos(void); 
  void StackJetDataHistos(void); 
  void ApplyMCNormFactors(void); 
  void AddHistoWeight(TH1D* histo, float weight); 
  void SetHistoStyles(void);  
  void SetHistoStyle_TauData(void);  
  void SetHistoStyle_JetData(void);  
  void SetHistoStyle_SignalM90(void);  
  void SetHistoStyle_SignalM100(void);  
  void SetHistoStyle_SignalM120(void);  
  void SetHistoStyle_SignalM140(void);  
  void SetHistoStyle_SignalM160(void);  
  void SetHistoStyle_QCD(void);  
  void SetHistoStyle_QCD_Pt30to50(void);  
  void SetHistoStyle_QCD_Pt50to80(void);  
  void SetHistoStyle_QCD_Pt80to120(void);  
  void SetHistoStyle_QCD_Pt120to170(void);  
  void SetHistoStyle_QCD_Pt170to300(void);  
  void SetHistoStyle_QCD_Pt300to470(void);  
  void SetHistoStyle_TTJets(void);  
  void SetHistoStyle_WJets(void);  
  void SetHistoStyle_WJets_noPU(void);  
  void CreateCanvas(void);  
  void CreateDumbieHisto(void); 
  void AddCmsPreliminaryText(void); 
  void AddEnergy7TeVText(void); 
  void AddLuminosityText(TString lumi, TString unit); 
  void GetHistoLuminosities(void); 
  void GetTauDataLumis(void); 
  void GetJetDataLumis(void); 
  void GetHistoLumi(TFile *f); 
  void AccumulateTauDataLumi(const float lumi); 
  void AccumulateJetDataLumi(const float lumi); 

};

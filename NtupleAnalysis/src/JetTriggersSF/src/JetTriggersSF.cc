//-*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"


class JetTriggersSF: public BaseSelector {
public:
  explicit JetTriggersSF(const ParameterSet& config, const TH1* skimCounters);
  virtual ~JetTriggersSF();// {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;

  double DeltaEta(double eta1, double eta2);
  double DeltaPhi(double phi1, double phi2);

  double DeltaR(double eta1, double eta2,
                  double phi1, double phi2);

  
private:
  // Input parameters
  const HistogramSettings cfg_PtBinSetting;
  const HistogramSettings cfg_EtaBinSetting;

  // Common plots
  CommonPlots fCommonPlots;
  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cControlTrigger; 
  METFilterSelection fMETFilterSelection;
  Count cVertexSelection;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  TauSelection fTauSelection;
  JetSelection fJetSelection;
  BJetSelection fBJetSelection;
  Count cBTaggingSFCounter;
  METSelection fMETSelection;
  TopologySelection fTopologySelection;
  TopSelection fTopSelection;
  Count cSelected;
  Count cTrigger_1BTag;
  Count cTrigger_2BTag;
  Count cTrigger_OR;
  Count cTrigger_OR_PFJet450;
  
  // Strings to store trigger names
  std::string TriggerName;

  //Histograms 
  WrappedTH1* hdRminJetM;
  //---------------------------------------------------------------------
  //   Denominators  
  //---------------------------------------------------------------------
  //   6thJet Pt,Eta,Phi, ... Event HT,PU,JetMulti,bJetMulti, AllJetCSV
  WrappedTH1* hDen_pt6thJet_RefTrg_OfflineSel;
  WrappedTH1* hDen_eta6thJet_RefTrg_OfflineSel;
  WrappedTH1* hDen_phi6thJet_RefTrg_OfflineSel;
  WrappedTH1* hDen_Ht_RefTrg_OfflineSel;
  WrappedTH1* hDen_pu_RefTrg_OfflineSel;
  WrappedTH1* hDen_nBTagJets_RefTrg_OfflineSel;
  WrappedTH1* hDen_CSV_RefTrg_OfflineSel;
  WrappedTH1* hDen_JetMulti_RefTrg_OfflineSel;
  WrappedTH1* hDen_BJetMulti_RefTrg_OfflineSel;
  //---------------------------------------------------------------------

  //---------------------------------------------------------------------  
  // Numerators, 1-BTag, 2-BTag, OR, OR+Jet450
  //---------------------------------------------------------------------
  // 6th jet pt
  WrappedTH1* hNum_pt6thJet_RefTrg_OfflineSel_Signal1BTag;
  WrappedTH1* hNum_pt6thJet_RefTrg_OfflineSel_Signal2BTag;
  WrappedTH1* hNum_pt6thJet_RefTrg_OfflineSel_SignalOR;
  WrappedTH1* hNum_pt6thJet_RefTrg_OfflineSel_SignalOR_PFJet450;

  // 6th jet eta
  WrappedTH1* hNum_eta6thJet_RefTrg_OfflineSel_Signal1BTag;
  WrappedTH1* hNum_eta6thJet_RefTrg_OfflineSel_Signal2BTag;
  WrappedTH1* hNum_eta6thJet_RefTrg_OfflineSel_SignalOR;
  WrappedTH1* hNum_eta6thJet_RefTrg_OfflineSel_SignalOR_PFJet450;

  // 6th jet phi
  WrappedTH1* hNum_phi6thJet_RefTrg_OfflineSel_Signal1BTag;
  WrappedTH1* hNum_phi6thJet_RefTrg_OfflineSel_Signal2BTag;
  WrappedTH1* hNum_phi6thJet_RefTrg_OfflineSel_SignalOR;
  WrappedTH1* hNum_phi6thJet_RefTrg_OfflineSel_SignalOR_PFJet450;

  //Ht
  WrappedTH1* hNum_Ht_RefTrg_OfflineSel_Signal1BTag;
  WrappedTH1* hNum_Ht_RefTrg_OfflineSel_Signal2BTag;
  WrappedTH1* hNum_Ht_RefTrg_OfflineSel_SignalOR;
  WrappedTH1* hNum_Ht_RefTrg_OfflineSel_SignalOR_PFJet450;

  //PU
  WrappedTH1* hNum_pu_RefTrg_OfflineSel_Signal1BTag;
  WrappedTH1* hNum_pu_RefTrg_OfflineSel_Signal2BTag;
  WrappedTH1* hNum_pu_RefTrg_OfflineSel_SignalOR;
  WrappedTH1* hNum_pu_RefTrg_OfflineSel_SignalOR_PFJet450;

  //B-Jet Multi
  WrappedTH1* hNum_nBTagJets_RefTrg_OfflineSel_Signal1BTag;
  WrappedTH1* hNum_nBTagJets_RefTrg_OfflineSel_Signal2BTag;
  WrappedTH1* hNum_nBTagJets_RefTrg_OfflineSel_SignalOR;
  WrappedTH1* hNum_nBTagJets_RefTrg_OfflineSel_SignalOR_PFJet450;

  //Jet CSV
  WrappedTH1* hNum_CSV_RefTrg_OfflineSel_Signal1BTag;
  WrappedTH1* hNum_CSV_RefTrg_OfflineSel_Signal2BTag;
  WrappedTH1* hNum_CSV_RefTrg_OfflineSel_SignalOR;
  WrappedTH1* hNum_CSV_RefTrg_OfflineSel_SignalOR_PFJet450;

  //Jet Multi
  WrappedTH1* hNum_JetMulti_RefTrg_OfflineSel_Signal1BTag;
  WrappedTH1* hNum_JetMulti_RefTrg_OfflineSel_Signal2BTag;
  WrappedTH1* hNum_JetMulti_RefTrg_OfflineSel_SignalOR;
  WrappedTH1* hNum_JetMulti_RefTrg_OfflineSel_SignalOR_PFJet450;

  //B-Jet Multi
  WrappedTH1* hNum_BJetMulti_RefTrg_OfflineSel_Signal1BTag;
  WrappedTH1* hNum_BJetMulti_RefTrg_OfflineSel_Signal2BTag;
  WrappedTH1* hNum_BJetMulti_RefTrg_OfflineSel_SignalOR;
  WrappedTH1* hNum_BJetMulti_RefTrg_OfflineSel_SignalOR_PFJet450;
  //---------------------------------------------------------------------

  //---------------------------------------------------------------------
  // TrgEfficiency in slices of Ht and the pt of the 6th Jet  
  //---------------------------------------------------------------------
  // In slices of HT
  WrappedTH1* h_Den_pt6thJet_Vs_450ht600_RefTrg_OfflineSel;
  WrappedTH1* h_Den_pt6thJet_Vs_600ht800_RefTrg_OfflineSel;
  WrappedTH1* h_Den_pt6thJet_Vs_800ht1000_RefTrg_OfflineSel;
  WrappedTH1* h_Den_pt6thJet_Vs_1000ht1250_RefTrg_OfflineSel;
  WrappedTH1* h_Den_pt6thJet_Vs_1250ht1500_RefTrg_OfflineSel;
  WrappedTH1* h_Den_pt6thJet_Vs_1500ht2000_RefTrg_OfflineSel;

  WrappedTH1* h_Num_pt6thJet_Vs_450ht600_RefTrg_OfflineSel_1BTag;
  WrappedTH1* h_Num_pt6thJet_Vs_600ht800_RefTrg_OfflineSel_1BTag;
  WrappedTH1* h_Num_pt6thJet_Vs_800ht1000_RefTrg_OfflineSel_1BTag;
  WrappedTH1* h_Num_pt6thJet_Vs_1000ht1250_RefTrg_OfflineSel_1BTag;
  WrappedTH1* h_Num_pt6thJet_Vs_1250ht1500_RefTrg_OfflineSel_1BTag;
  WrappedTH1* h_Num_pt6thJet_Vs_1500ht2000_RefTrg_OfflineSel_1BTag;

  WrappedTH1* h_Num_pt6thJet_Vs_450ht600_RefTrg_OfflineSel_2BTag;
  WrappedTH1* h_Num_pt6thJet_Vs_600ht800_RefTrg_OfflineSel_2BTag;
  WrappedTH1* h_Num_pt6thJet_Vs_800ht1000_RefTrg_OfflineSel_2BTag;
  WrappedTH1* h_Num_pt6thJet_Vs_1000ht1250_RefTrg_OfflineSel_2BTag;
  WrappedTH1* h_Num_pt6thJet_Vs_1250ht1500_RefTrg_OfflineSel_2BTag;
  WrappedTH1* h_Num_pt6thJet_Vs_1500ht2000_RefTrg_OfflineSel_2BTag;

  WrappedTH1* h_Num_pt6thJet_Vs_450ht600_RefTrg_OfflineSel_OR;
  WrappedTH1* h_Num_pt6thJet_Vs_600ht800_RefTrg_OfflineSel_OR;
  WrappedTH1* h_Num_pt6thJet_Vs_800ht1000_RefTrg_OfflineSel_OR;
  WrappedTH1* h_Num_pt6thJet_Vs_1000ht1250_RefTrg_OfflineSel_OR;
  WrappedTH1* h_Num_pt6thJet_Vs_1250ht1500_RefTrg_OfflineSel_OR;
  WrappedTH1* h_Num_pt6thJet_Vs_1500ht2000_RefTrg_OfflineSel_OR;
  
  // In slices of Pt of the 6th Jet
  //WrappedTH1* h_Den_ht_Vs_30pt40_RefTrg_OfflineSel;
  WrappedTH1* h_Den_ht_Vs_40pt50_RefTrg_OfflineSel;
  WrappedTH1* h_Den_ht_Vs_50pt60_RefTrg_OfflineSel;
  WrappedTH1* h_Den_ht_Vs_60pt70_RefTrg_OfflineSel;
  WrappedTH1* h_Den_ht_Vs_70pt90_RefTrg_OfflineSel;
  WrappedTH1* h_Den_ht_Vs_90pt120_RefTrg_OfflineSel;

  //WrappedTH1* h_Num_ht_Vs_30pt40_RefTrg_OfflineSel_1BTag;
  WrappedTH1* h_Num_ht_Vs_40pt50_RefTrg_OfflineSel_1BTag;
  WrappedTH1* h_Num_ht_Vs_50pt60_RefTrg_OfflineSel_1BTag;
  WrappedTH1* h_Num_ht_Vs_60pt70_RefTrg_OfflineSel_1BTag;
  WrappedTH1* h_Num_ht_Vs_70pt90_RefTrg_OfflineSel_1BTag;
  WrappedTH1* h_Num_ht_Vs_90pt120_RefTrg_OfflineSel_1BTag;

  //WrappedTH1* h_Num_ht_Vs_30pt40_RefTrg_OfflineSel_2BTag;
  WrappedTH1* h_Num_ht_Vs_40pt50_RefTrg_OfflineSel_2BTag;
  WrappedTH1* h_Num_ht_Vs_50pt60_RefTrg_OfflineSel_2BTag;
  WrappedTH1* h_Num_ht_Vs_60pt70_RefTrg_OfflineSel_2BTag;
  WrappedTH1* h_Num_ht_Vs_70pt90_RefTrg_OfflineSel_2BTag;
  WrappedTH1* h_Num_ht_Vs_90pt120_RefTrg_OfflineSel_2BTag;

  //WrappedTH1* h_Num_ht_Vs_30pt40_RefTrg_OfflineSel_OR;
  WrappedTH1* h_Num_ht_Vs_40pt50_RefTrg_OfflineSel_OR;
  WrappedTH1* h_Num_ht_Vs_50pt60_RefTrg_OfflineSel_OR;
  WrappedTH1* h_Num_ht_Vs_60pt70_RefTrg_OfflineSel_OR;
  WrappedTH1* h_Num_ht_Vs_70pt90_RefTrg_OfflineSel_OR;
  WrappedTH1* h_Num_ht_Vs_90pt120_RefTrg_OfflineSel_OR;
  //---------------------------------------------------------------------

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(JetTriggersSF);

JetTriggersSF::JetTriggersSF(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_PtBinSetting(config.getParameter<ParameterSet>("CommonPlots.ptBins")),
    cfg_EtaBinSetting(config.getParameter<ParameterSet>("CommonPlots.etaBins")),
    fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kHplus2tbAnalysis, fHistoWrapper), 
    cAllEvents(fEventCounter.addCounter("all events")),
    cControlTrigger(fEventCounter.addCounter("passed cntrl trg")),
    fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cVertexSelection(fEventCounter.addCounter("passed PV")),
    fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fTauSelection(config.getParameter<ParameterSet>("TauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fJetSelection(config.getParameter<ParameterSet>("JetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cBTaggingSFCounter(fEventCounter.addCounter("b tag SF")),
    fMETSelection(config.getParameter<ParameterSet>("METSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fTopologySelection(config.getParameter<ParameterSet>("TopologySelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fTopSelection(config.getParameter<ParameterSet>("TopSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cSelected(fEventCounter.addCounter("Selected Events")),
    cTrigger_1BTag(fEventCounter.addCounter("passed sig 1BTag")),
    cTrigger_2BTag(fEventCounter.addCounter("passed sig 2BTag")),
    cTrigger_OR(fEventCounter.addCounter("passed sig OR")),
    cTrigger_OR_PFJet450(fEventCounter.addCounter("passed sig OR + PFJet450"))
{

}

JetTriggersSF::~JetTriggersSF()
{
}

void JetTriggersSF::book(TDirectory *dir) {

  
  // Book common plots histograms
  fCommonPlots.book(dir, isData());

  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  fMETSelection.bookHistograms(dir);
  fTopologySelection.bookHistograms(dir);
  fTopSelection.bookHistograms(dir);
  
  // Book non-common histograms

  //---------------------------------------------------------------------
  // Binning
  //---------------------------------------------------------------------
  double xbins_pt[25] = {20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 55, 60, 65, 70, 80, 90, 100, 110, 120};
  int nxbins_pt       = 24;
  double xbins_ht[38] = {200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500,  520,  540,  560, 580,  600, 620, 640, 660, 680, 700, 725, 750, 775, 800, 850, 900, 950, 1000, 1100, 1400, 1700, 2000};
  int nxbins_ht       = 37;
  double xbins_b[7]   = {-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 9.5};
  int nxbins_b        = 6;
  double etaMax = 3.0;
  int nxbins_eta = 30;
  double phiMax = 4.0;
  int nxbins_phi = 30;
  //---------------------------------------------------------------------

  hdRminJetM = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hdRminJetM" , "dR", 250, 0, 5);

  //---------------------------------------------------------------------
  //   Denominators  
  //---------------------------------------------------------------------
  hDen_pt6thJet_RefTrg_OfflineSel  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hDen_pt6thJet_RefTrg_OfflineSel", "pt", nxbins_pt, xbins_pt);
  hDen_eta6thJet_RefTrg_OfflineSel = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hDen_eta6thJet_RefTrg_OfflineSel", "eta", nxbins_eta, -1*etaMax , etaMax);
  hDen_phi6thJet_RefTrg_OfflineSel = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hDen_phi6thJet_RefTrg_OfflineSel", "phi", nxbins_phi, -1*phiMax , phiMax);
  hDen_Ht_RefTrg_OfflineSel = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hDen_Ht_RefTrg_OfflineSel", "ht", nxbins_ht, xbins_ht);
  hDen_pu_RefTrg_OfflineSel = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hDen_pu_RefTrg_OfflineSel","pu", 11, 0, 55);
  hDen_nBTagJets_RefTrg_OfflineSel = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hDen_nBTagJets_RefTrg_OfflineSel", "nbtagjets", nxbins_b, xbins_b);
  hDen_CSV_RefTrg_OfflineSel = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hDen_CSV_RefTrg_OfflineSel", "CSV", 20, 0, 1); 
  hDen_JetMulti_RefTrg_OfflineSel = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hDen_JetMulti_RefTrg_OfflineSel", "nJets", 10, 4.5, 14.5);
  hDen_BJetMulti_RefTrg_OfflineSel = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hDen_BJetMulti_RefTrg_OfflineSel", "nBJets", 7, 0.5, 7.5);

  //---------------------------------------------------------------------
  // Numerators
  //---------------------------------------------------------------------
  //6th Jet pt
  hNum_pt6thJet_RefTrg_OfflineSel_Signal1BTag       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_pt6thJet_RefTrg_OfflineSel_Signal1BTag", "pt", nxbins_pt, xbins_pt);
  hNum_pt6thJet_RefTrg_OfflineSel_Signal2BTag       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_pt6thJet_RefTrg_OfflineSel_Signal2BTag", "pt", nxbins_pt, xbins_pt);
  hNum_pt6thJet_RefTrg_OfflineSel_SignalOR          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_pt6thJet_RefTrg_OfflineSel_SignalOR", "pt", nxbins_pt, xbins_pt);
  hNum_pt6thJet_RefTrg_OfflineSel_SignalOR_PFJet450 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_pt6thJet_RefTrg_OfflineSel_SignalOR_PFJet450", "pt", nxbins_pt, xbins_pt);

  //6th Jet eta
  hNum_eta6thJet_RefTrg_OfflineSel_Signal1BTag       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_eta6thJet_RefTrg_OfflineSel_Signal1BTag", "eta", nxbins_eta, -1*etaMax , etaMax);
  hNum_eta6thJet_RefTrg_OfflineSel_Signal2BTag       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_eta6thJet_RefTrg_OfflineSel_Signal2BTag", "eta", nxbins_eta, -1*etaMax , etaMax);
  hNum_eta6thJet_RefTrg_OfflineSel_SignalOR          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_eta6thJet_RefTrg_OfflineSel_SignalOR", "eta", nxbins_eta, -1*etaMax , etaMax);
  hNum_eta6thJet_RefTrg_OfflineSel_SignalOR_PFJet450 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_eta6thJet_RefTrg_OfflineSel_SignalOR_PFJet450", "eta", nxbins_eta, -1*etaMax , etaMax);

  //6th Jet phi
  hNum_phi6thJet_RefTrg_OfflineSel_Signal1BTag       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_phi6thJet_RefTrg_OfflineSel_Signal1BTag", "phi", nxbins_phi, -1*phiMax , phiMax);
  hNum_phi6thJet_RefTrg_OfflineSel_Signal2BTag       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_phi6thJet_RefTrg_OfflineSel_Signal2BTag", "phi", nxbins_phi, -1*phiMax , phiMax);
  hNum_phi6thJet_RefTrg_OfflineSel_SignalOR          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_phi6thJet_RefTrg_OfflineSel_SignalOR", "phi", nxbins_phi, -1*phiMax , phiMax);
  hNum_phi6thJet_RefTrg_OfflineSel_SignalOR_PFJet450 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_phi6thJet_RefTrg_OfflineSel_SignalOR_PFJet450", "phi", nxbins_phi, -1*phiMax , phiMax);

  //HT
  hNum_Ht_RefTrg_OfflineSel_Signal1BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_Ht_RefTrg_OfflineSel_Signal1BTag", "Ht", nxbins_ht, xbins_ht);
  hNum_Ht_RefTrg_OfflineSel_Signal2BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_Ht_RefTrg_OfflineSel_Signal2BTag", "Ht", nxbins_ht, xbins_ht);
  hNum_Ht_RefTrg_OfflineSel_SignalOR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_Ht_RefTrg_OfflineSel_SignalOR", "Ht", nxbins_ht, xbins_ht);
  hNum_Ht_RefTrg_OfflineSel_SignalOR_PFJet450 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_Ht_RefTrg_OfflineSel_SignalOR_PFJet450", "Ht", nxbins_ht, xbins_ht);

  //PU
  hNum_pu_RefTrg_OfflineSel_Signal1BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_pu_RefTrg_OfflineSel_Signal1BTag", "pu", 11, 0, 55);
  hNum_pu_RefTrg_OfflineSel_Signal2BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_pu_RefTrg_OfflineSel_Signal2BTag", "pu", 11, 0, 55);
  hNum_pu_RefTrg_OfflineSel_SignalOR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_pu_RefTrg_OfflineSel_SignalOR","pu", 11, 0, 55);
  hNum_pu_RefTrg_OfflineSel_SignalOR_PFJet450    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_pu_RefTrg_OfflineSel_SignalOR_PFJet450","pu", 11, 0, 55);

  //b-Jet Multi
  hNum_nBTagJets_RefTrg_OfflineSel_Signal1BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_nBTagJets_RefTrg_OfflineSel_Signal1BTag", "nbtagjets", nxbins_b, xbins_b);
  hNum_nBTagJets_RefTrg_OfflineSel_Signal2BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_nBTagJets_RefTrg_OfflineSel_Signal2BTag", "nbtagjets", nxbins_b, xbins_b);
  hNum_nBTagJets_RefTrg_OfflineSel_SignalOR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_nBTagJets_RefTrg_OfflineSel_SignalOR", "nbtagjets", nxbins_b, xbins_b);
  hNum_nBTagJets_RefTrg_OfflineSel_SignalOR_PFJet450 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_nBTagJets_RefTrg_OfflineSel_SignalOR_PFJet450", "nbtagjets", nxbins_b, xbins_b);

   //Jet CSV
  hNum_CSV_RefTrg_OfflineSel_Signal1BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_CSV_RefTrg_OfflineSel_Signal1BTag", "CSV", 20, 0, 1);
  hNum_CSV_RefTrg_OfflineSel_Signal2BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_CSV_RefTrg_OfflineSel_Signal2BTag", "CSV", 20, 0, 1);
  hNum_CSV_RefTrg_OfflineSel_SignalOR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_CSV_RefTrg_OfflineSel_SignalOR"   , "CSV", 20, 0, 1);
  hNum_CSV_RefTrg_OfflineSel_SignalOR_PFJet450    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_CSV_RefTrg_OfflineSel_SignalOR_PFJet450"   , "CSV", 20, 0, 1);

  //Jet Multi
  hNum_JetMulti_RefTrg_OfflineSel_Signal1BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_JetMulti_RefTrg_OfflineSel_Signal1BTag", "nJets", 10, 4.5, 14.5);
  hNum_JetMulti_RefTrg_OfflineSel_Signal2BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_JetMulti_RefTrg_OfflineSel_Signal2BTag", "nJets", 10, 4.5, 14.5);
  hNum_JetMulti_RefTrg_OfflineSel_SignalOR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_JetMulti_RefTrg_OfflineSel_SignalOR"   , "nJets", 10, 4.5, 14.5);
  hNum_JetMulti_RefTrg_OfflineSel_SignalOR_PFJet450    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_JetMulti_RefTrg_OfflineSel_SignalOR_PFJet450"   , "nJets", 10, 4.5, 14.5);

  //b-Jet Multi
  hNum_BJetMulti_RefTrg_OfflineSel_Signal1BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_BJetMulti_RefTrg_OfflineSel_Signal1BTag", "nBJets", 7, 0.5, 7.5);
  hNum_BJetMulti_RefTrg_OfflineSel_Signal2BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_BJetMulti_RefTrg_OfflineSel_Signal2BTag", "nBJets", 7, 0.5, 7.5);
  hNum_BJetMulti_RefTrg_OfflineSel_SignalOR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_BJetMulti_RefTrg_OfflineSel_SignalOR"   , "nBJets", 7, 0.5, 7.5);
  hNum_BJetMulti_RefTrg_OfflineSel_SignalOR_PFJet450    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "hNum_BJetMulti_RefTrg_OfflineSel_SignalOR_PFJet450"   , "nBJets", 7, 0.5, 7.5);
  //---------------------------------------------------------------------

  //---------------------------------------------------------------------
  // In slices of HT and the pt of the 6th Jet
  //---------------------------------------------------------------------
  // in slices of the pt of the 6th jet
  //---------------------------------------------------------------------
  //h_Den_ht_Vs_30pt40_RefTrg_OfflineSel=fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Den_ht_Vs_30pt40_RefTrg_OfflineSel","ht",nxbins_ht, xbins_ht);
  h_Den_ht_Vs_40pt50_RefTrg_OfflineSel=fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Den_ht_Vs_40pt50_RefTrg_OfflineSel","ht",nxbins_ht, xbins_ht);
  h_Den_ht_Vs_50pt60_RefTrg_OfflineSel=fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Den_ht_Vs_50pt60_RefTrg_OfflineSel","ht",nxbins_ht, xbins_ht);
  h_Den_ht_Vs_60pt70_RefTrg_OfflineSel=fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Den_ht_Vs_60pt70_RefTrg_OfflineSel","ht",nxbins_ht, xbins_ht);
  h_Den_ht_Vs_70pt90_RefTrg_OfflineSel=fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Den_ht_Vs_70pt90_RefTrg_OfflineSel","ht",nxbins_ht, xbins_ht);
  h_Den_ht_Vs_90pt120_RefTrg_OfflineSel=fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Den_ht_Vs_90pt120_RefTrg_OfflineSel","ht",nxbins_ht,xbins_ht);
  
  //h_Num_ht_Vs_30pt40_RefTrg_OfflineSel_1BTag= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_30pt40_RefTrg_OfflineSel_1BTag","ht in pt slices", nxbins_ht, xbins_ht);
  h_Num_ht_Vs_40pt50_RefTrg_OfflineSel_1BTag= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_40pt50_RefTrg_OfflineSel_1BTag","ht in pt slices",  nxbins_ht, xbins_ht);
  h_Num_ht_Vs_50pt60_RefTrg_OfflineSel_1BTag= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_50pt60_RefTrg_OfflineSel_1BTag","ht in pt slices", nxbins_ht, xbins_ht);
  h_Num_ht_Vs_60pt70_RefTrg_OfflineSel_1BTag= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_60pt70_RefTrg_OfflineSel_1BTag","ht in pt slices", nxbins_ht, xbins_ht);
  h_Num_ht_Vs_70pt90_RefTrg_OfflineSel_1BTag= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_70pt90_RefTrg_OfflineSel_1BTag","ht in pt slices", nxbins_ht, xbins_ht);
  h_Num_ht_Vs_90pt120_RefTrg_OfflineSel_1BTag= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_90pt120_RefTrg_OfflineSel_1BTag","ht in pt slices", nxbins_ht, xbins_ht);
  
  //h_Num_ht_Vs_30pt40_RefTrg_OfflineSel_2BTag= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_30pt40_RefTrg_OfflineSel_2BTag","ht in pt slices", nxbins_ht, xbins_ht);
  h_Num_ht_Vs_40pt50_RefTrg_OfflineSel_2BTag= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_40pt50_RefTrg_OfflineSel_2BTag","ht in pt slices",  nxbins_ht, xbins_ht);
  h_Num_ht_Vs_50pt60_RefTrg_OfflineSel_2BTag= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_50pt60_RefTrg_OfflineSel_2BTag","ht in pt slices", nxbins_ht, xbins_ht);
  h_Num_ht_Vs_60pt70_RefTrg_OfflineSel_2BTag= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_60pt70_RefTrg_OfflineSel_2BTag","ht in pt slices", nxbins_ht, xbins_ht);
  h_Num_ht_Vs_70pt90_RefTrg_OfflineSel_2BTag= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_70pt90_RefTrg_OfflineSel_2BTag","ht in pt slices", nxbins_ht, xbins_ht);
  h_Num_ht_Vs_90pt120_RefTrg_OfflineSel_2BTag= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_90pt120_RefTrg_OfflineSel_2BTag","ht in pt slices", nxbins_ht, xbins_ht);
  
  //h_Num_ht_Vs_30pt40_RefTrg_OfflineSel_OR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_30pt40_RefTrg_OfflineSel_OR","ht in pt slices", nxbins_ht, xbins_ht);
  h_Num_ht_Vs_40pt50_RefTrg_OfflineSel_OR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_40pt50_RefTrg_OfflineSel_OR","ht in pt slices",  nxbins_ht, xbins_ht);
  h_Num_ht_Vs_50pt60_RefTrg_OfflineSel_OR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_50pt60_RefTrg_OfflineSel_OR","ht in pt slices", nxbins_ht, xbins_ht);
  h_Num_ht_Vs_60pt70_RefTrg_OfflineSel_OR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_60pt70_RefTrg_OfflineSel_OR","ht in pt slices", nxbins_ht, xbins_ht);
  h_Num_ht_Vs_70pt90_RefTrg_OfflineSel_OR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_70pt90_RefTrg_OfflineSel_OR","ht in pt slices", nxbins_ht, xbins_ht);
  h_Num_ht_Vs_90pt120_RefTrg_OfflineSel_OR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,"Num_ht_Vs_90pt120_RefTrg_OfflineSel_OR","ht in pt slices", nxbins_ht, xbins_ht);

  //---------------------------------------------------------------------
  // in slices of ht
  //---------------------------------------------------------------------
  h_Den_pt6thJet_Vs_450ht600_RefTrg_OfflineSel=fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital,dir,"Den_pt6thJet_Vs_450ht600_RefTrg_OfflineSel","pt",nxbins_pt,xbins_pt);
  h_Den_pt6thJet_Vs_600ht800_RefTrg_OfflineSel=fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital,dir,"Den_pt6thJet_Vs_600ht800_RefTrg_OfflineSel","pt",nxbins_pt,xbins_pt);
  h_Den_pt6thJet_Vs_800ht1000_RefTrg_OfflineSel=fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital,dir,"Den_pt6thJet_Vs_800ht1000_RefTrg_OfflineSel","pt",nxbins_pt,xbins_pt);
  h_Den_pt6thJet_Vs_1000ht1250_RefTrg_OfflineSel=fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital,dir,"Den_pt6thJet_Vs_1000ht1250_RefTrg_OfflineSel", "pt", nxbins_pt, xbins_pt);
  h_Den_pt6thJet_Vs_1250ht1500_RefTrg_OfflineSel=fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital,dir,"Den_pt6thJet_Vs_1250ht1500_RefTrg_OfflineSel", "pt", nxbins_pt, xbins_pt);
  h_Den_pt6thJet_Vs_1500ht2000_RefTrg_OfflineSel=fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital,dir,"Den_pt6thJet_Vs_1500ht2000_RefTrg_OfflineSel", "pt", nxbins_pt, xbins_pt);
  
  h_Num_pt6thJet_Vs_450ht600_RefTrg_OfflineSel_1BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_450ht600_RefTrg_OfflineSel_1BTag", "pt", nxbins_pt, xbins_pt);
  h_Num_pt6thJet_Vs_600ht800_RefTrg_OfflineSel_1BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_600ht800_RefTrg_OfflineSel_1BTag", "pt", nxbins_pt, xbins_pt);
  h_Num_pt6thJet_Vs_800ht1000_RefTrg_OfflineSel_1BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_800ht1000_RefTrg_OfflineSel_1BTag", "pt", nxbins_pt, xbins_pt);
  h_Num_pt6thJet_Vs_1000ht1250_RefTrg_OfflineSel_1BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_1000ht1250_RefTrg_OfflineSel_1BTag", "pt",nxbins_pt, xbins_pt);
  h_Num_pt6thJet_Vs_1250ht1500_RefTrg_OfflineSel_1BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_1250ht1500_RefTrg_OfflineSel_1BTag", "pt",nxbins_pt, xbins_pt);
  h_Num_pt6thJet_Vs_1500ht2000_RefTrg_OfflineSel_1BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_1500ht2000_RefTrg_OfflineSel_1BTag", "pt",nxbins_pt, xbins_pt);
  
  h_Num_pt6thJet_Vs_450ht600_RefTrg_OfflineSel_2BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_450ht600_RefTrg_OfflineSel_2BTag", "pt", nxbins_pt, xbins_pt);
  h_Num_pt6thJet_Vs_600ht800_RefTrg_OfflineSel_2BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_600ht800_RefTrg_OfflineSel_2BTag", "pt", nxbins_pt, xbins_pt);
  h_Num_pt6thJet_Vs_800ht1000_RefTrg_OfflineSel_2BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_800ht1000_RefTrg_OfflineSel_2BTag", "pt", nxbins_pt, xbins_pt);
  h_Num_pt6thJet_Vs_1000ht1250_RefTrg_OfflineSel_2BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_1000ht1250_RefTrg_OfflineSel_2BTag", "pt",nxbins_pt, xbins_pt);
  h_Num_pt6thJet_Vs_1250ht1500_RefTrg_OfflineSel_2BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_1250ht1500_RefTrg_OfflineSel_2BTag", "pt",nxbins_pt, xbins_pt);
  h_Num_pt6thJet_Vs_1500ht2000_RefTrg_OfflineSel_2BTag = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_1500ht2000_RefTrg_OfflineSel_2BTag", "pt",nxbins_pt, xbins_pt);
  
  h_Num_pt6thJet_Vs_450ht600_RefTrg_OfflineSel_OR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_450ht600_RefTrg_OfflineSel_OR", "pt", nxbins_pt, xbins_pt);
  h_Num_pt6thJet_Vs_600ht800_RefTrg_OfflineSel_OR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_600ht800_RefTrg_OfflineSel_OR", "pt", nxbins_pt, xbins_pt);
  h_Num_pt6thJet_Vs_800ht1000_RefTrg_OfflineSel_OR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_800ht1000_RefTrg_OfflineSel_OR", "pt", nxbins_pt, xbins_pt);
  h_Num_pt6thJet_Vs_1000ht1250_RefTrg_OfflineSel_OR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_1000ht1250_RefTrg_OfflineSel_OR", "pt",nxbins_pt, xbins_pt);
  h_Num_pt6thJet_Vs_1250ht1500_RefTrg_OfflineSel_OR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_1250ht1500_RefTrg_OfflineSel_OR", "pt",nxbins_pt, xbins_pt);
  h_Num_pt6thJet_Vs_1500ht2000_RefTrg_OfflineSel_OR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Num_pt6thJet_Vs_1500ht2000_RefTrg_OfflineSel_OR", "pt",nxbins_pt, xbins_pt);
  //---------------------------------------------------------------------
  
  return;
}


void JetTriggersSF::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}


void JetTriggersSF::process(Long64_t entry) {

  //====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});

  cAllEvents.increment();

  // ===============================================================================================
  //  1) Apply Reference Trigger
  // ===============================================================================================
  TriggerName = "HLT_IsoMu24";
  bool Passed_HLT_IsoMu24 = fEvent.passHLTDecisionByName(TriggerName);
  if (!Passed_HLT_IsoMu24) return;
  cControlTrigger.increment();
  //================================================================================================   
  
  // ===============================================================================================
  //  2) Offline Selection
  // ===============================================================================================
  // ---------------- MET filters (to remove events with spurious sources of fake MET) -------------
  if (0) std::cout << "=== MET Filter" << std::endl;
  const METFilterSelection::Data metFilterData = fMETFilterSelection.analyze(fEvent);
  if (!metFilterData.passedSelection()) return;
  fCommonPlots.fillControlPlotsAfterMETFilter(fEvent);  

  //  ----------------------------- Primarty Vertex (Check that a PV exists) -----------------------
  if (0) std::cout << "=== Vertices" << std::endl;
  int nVertices = fEvent.vertexInfo().value();
  fCommonPlots.setNvertices(nVertices);
  if (nVertices < 1) return;
  cVertexSelection.increment();
  fCommonPlots.fillControlPlotsAtVertexSelection(fEvent);

  // -------------------------------------- Electron Veto --------------------------------------------
  // Electron veto (Orthogonality)
  if (0) std::cout << "=== Electron veto" << std::endl;
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if (eData.hasIdentifiedElectrons()) return;

  // Tau Veto (HToTauNu Orthogonality)
  if (0) std::cout << "=== Tau-Veto" << std::endl;
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (tauData.hasIdentifiedTaus() ) return;

  // -------------------------------------- Muon Selection --------------------------------------------
  if (0) std::cout << "=== Muon veto/selection" << std::endl;
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if (!muData.hasIdentifiedMuons()) return;
  if (muData.getSelectedMuons().size()>1) return;

  
  // ------------------------------------- Jet Selection -------------------------------------------
  if (0) std::cout << "=== Jet selection" << std::endl;
  const JetSelection::Data jetData = fJetSelection.analyzeWithoutTau(fEvent);
  if (!jetData.passedSelection()) return;

  // ------------------------------------ BJet selection -------------------------------------------
  if (0) std::cout << "=== BJet selection" << std::endl;
  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);
  if (!bjetData.passedSelection()) return;
  //================================================================================================   

  //================================================================================================
  // Measurement dependent offline selection 
  //================================================================================================   
  /*
    The efficiency measurement w.r.t Ht and pt6th jet are measured without applying cuts to these variables.
    The initial selection is loose w.r.t these variables.  
  */
  
  Bool_t isEffvsPT = false;
  Bool_t isEffvsHT = false;

  Double_t pt_6thJet = jetData.getSelectedJets().at(5).pt();
  Double_t pt_7thJet = jetData.getSelectedJets().at(6).pt();

  if(pt_6thJet > 40.0 && pt_7thJet > 30.0) // when measuring Eff w.r.t Ht, standard jet pt cut applied on events. pt cut  [40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 30.0] 
    isEffvsHT= true;
  
  Double_t HT_selJets = jetData.HT(); // when measuring Eff w.r.t pt6thJet, standard Ht cut applied on events. Ht cut 500.0 
  if(HT_selJets >= 500.0)
    isEffvsPT = true;

  Bool_t isEffvsOthers = isEffvsPT and isEffvsHT; // for other variables, standard cut on pt and Ht is applied on the events.
  //================================================================================================   


  
  //================================================================================================   
  // 3)  Mu Isolation from selected jets.  
  //================================================================================================
   Double_t dRMin = 100.0;

   for(Size_t imu =0; imu < muData.getSelectedMuons().size(); imu++)
     {
       Double_t MuEta = muData.getSelectedMuons().at(imu).eta();
       Double_t MuPhi = muData.getSelectedMuons().at(imu).phi();	
       for(Size_t ijet = 0; ijet<jetData.getSelectedJets().size(); ijet++)
	 {
	   Double_t JetEta = jetData.getSelectedJets().at(ijet).eta();
	   Double_t JetPhi = jetData.getSelectedJets().at(ijet).phi();
	   
	   Double_t dRJetMu =  DeltaR(MuEta, JetEta,
				      MuPhi, JetPhi);
	   
	   if(dRJetMu < dRMin)
	     {
	       dRMin = dRJetMu;
	     }
	 }//loop on jets
     }//loop on Mu
   
   hdRminJetM->Fill(dRMin);
   
   if(dRMin < 0.4) // comment these out to run withouf dR cut
     return;
   //================================================================================================  
   
  
  //================================================================================================
  // All cuts passed
  //================================================================================================
  if (0) std::cout << "=== All cuts passed" << std::endl;
  cSelected.increment();



    
  //================================================================================================   
  // 4)  Signal triggers  
  //================================================================================================   
  if (0) std::cout << "=== Trigger" << std::endl;

  // Triggers
  TriggerName = "HLT_PFHT400_SixJet30_DoubleBTagCSV_p056";
  bool Passed_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056 = fEvent.passHLTDecisionByName(TriggerName);
  
  TriggerName = "HLT_PFHT450_SixJet40_BTagCSV_p056";
  bool Passed_HLT_PFHT450_SixJet40_BTagCSV_p056 = fEvent.passHLTDecisionByName(TriggerName);

  TriggerName = "HLT_PFJet450";                                           
  bool Passed_HLT_PFJet450 = fEvent.passHLTDecisionByName(TriggerName);
  
  bool Passed_OR                            = Passed_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056 or Passed_HLT_PFHT450_SixJet40_BTagCSV_p056;
  bool Passed_OR_PFJet450                   = Passed_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056 or Passed_HLT_PFHT450_SixJet40_BTagCSV_p056 or Passed_HLT_PFJet450;

  if (Passed_HLT_PFHT450_SixJet40_BTagCSV_p056)       cTrigger_1BTag.increment();
  if (Passed_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056) cTrigger_2BTag.increment();
  if (Passed_OR)                                      cTrigger_OR.increment();
  if (Passed_OR_PFJet450)                             cTrigger_OR_PFJet450.increment();
  //================================================================================================   

  // ===============================================================================================
  //   Accessing variables to measure Trigger Efficiency
  // ===============================================================================================
  
  double Pt6thJet  = jetData.getSelectedJets().at(5).pt();
  double Eta6thJet  = jetData.getSelectedJets().at(5).eta();
  double Phi6thJet  = jetData.getSelectedJets().at(5).phi();
  double HT        = jetData.HT();
  int    PU        = nVertices;
  int    nBTagJets = bjetData.getNumberOfSelectedBJets();
  int    nJets     = jetData.getSelectedJets().size();
  int    nBJets    = bjetData.getSelectedBJets().size();

  // ===============================================================================================
  // Measurement Trigger Efficiencies
  // ===============================================================================================

  //------------------------------------------
  // Fill Denominator Plots
  //-------------------------------------------
  if(isEffvsPT)
    hDen_pt6thJet_RefTrg_OfflineSel   -> Fill(Pt6thJet);
  if(isEffvsHT)
    hDen_Ht_RefTrg_OfflineSel         -> Fill(HT);
  if(isEffvsOthers){
    hDen_eta6thJet_RefTrg_OfflineSel  -> Fill(Eta6thJet);
    hDen_phi6thJet_RefTrg_OfflineSel  -> Fill(Phi6thJet);
    hDen_pu_RefTrg_OfflineSel         -> Fill(PU);
    hDen_nBTagJets_RefTrg_OfflineSel  -> Fill(nBTagJets);
    hDen_JetMulti_RefTrg_OfflineSel   -> Fill(nJets);
    hDen_BJetMulti_RefTrg_OfflineSel  -> Fill(nBJets);
  }
  //------------------------------------------

  //------------------------------------------
  // Fill Numerator Plots
  //------------------------------------------
  //1-B Tag Trigger 
  //------------------------------------------
  if (Passed_HLT_PFHT450_SixJet40_BTagCSV_p056){
    if(isEffvsPT)
      hNum_pt6thJet_RefTrg_OfflineSel_Signal1BTag  -> Fill(Pt6thJet);
    if(isEffvsHT)
      hNum_Ht_RefTrg_OfflineSel_Signal1BTag        -> Fill(HT);
    if(isEffvsOthers){
      hNum_eta6thJet_RefTrg_OfflineSel_Signal1BTag -> Fill(Eta6thJet);
      hNum_phi6thJet_RefTrg_OfflineSel_Signal1BTag -> Fill(Phi6thJet);
      hNum_pu_RefTrg_OfflineSel_Signal1BTag        -> Fill(PU);
      hNum_nBTagJets_RefTrg_OfflineSel_Signal1BTag -> Fill(nBTagJets);
      hNum_JetMulti_RefTrg_OfflineSel_Signal1BTag  -> Fill(nJets);
      hNum_BJetMulti_RefTrg_OfflineSel_Signal1BTag -> Fill(nBJets);
    }
    
  }
  //------------------------------------------
  //2-B Tag Trigger 
  //------------------------------------------
  if (Passed_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056){
    if(isEffvsPT)
      hNum_pt6thJet_RefTrg_OfflineSel_Signal2BTag  -> Fill(Pt6thJet);
    if(isEffvsHT)
      hNum_Ht_RefTrg_OfflineSel_Signal2BTag        -> Fill(HT);
    if(isEffvsOthers){
      hNum_eta6thJet_RefTrg_OfflineSel_Signal2BTag -> Fill(Eta6thJet);
      hNum_phi6thJet_RefTrg_OfflineSel_Signal2BTag -> Fill(Phi6thJet);
      hNum_pu_RefTrg_OfflineSel_Signal2BTag        -> Fill(PU);
      hNum_nBTagJets_RefTrg_OfflineSel_Signal2BTag -> Fill(nBTagJets);
      hNum_JetMulti_RefTrg_OfflineSel_Signal2BTag  -> Fill(nJets);
      hNum_BJetMulti_RefTrg_OfflineSel_Signal2BTag -> Fill(nBJets);
    }
    
  }
  //------------------------------------------
  //OR Trigger 
  //------------------------------------------
  if (Passed_OR){
    if(isEffvsPT)
      hNum_pt6thJet_RefTrg_OfflineSel_SignalOR   -> Fill(Pt6thJet);
    if(isEffvsHT)
      hNum_Ht_RefTrg_OfflineSel_SignalOR         -> Fill(HT);
    if(isEffvsOthers){
      hNum_eta6thJet_RefTrg_OfflineSel_SignalOR  -> Fill(Eta6thJet);
      hNum_phi6thJet_RefTrg_OfflineSel_SignalOR  -> Fill(Phi6thJet);
      hNum_pu_RefTrg_OfflineSel_SignalOR         -> Fill(PU);
      hNum_nBTagJets_RefTrg_OfflineSel_SignalOR  -> Fill(nBTagJets);
      hNum_JetMulti_RefTrg_OfflineSel_SignalOR   -> Fill(nJets);
      hNum_BJetMulti_RefTrg_OfflineSel_SignalOR  -> Fill(nBJets);
    }
  }
  //------------------------------------------
  //Or + PFJet450 Trigger 
  //------------------------------------------
  if(Passed_OR_PFJet450)
    {
      if(isEffvsPT)
	hNum_pt6thJet_RefTrg_OfflineSel_SignalOR_PFJet450   -> Fill(Pt6thJet);
      if(isEffvsHT)
	hNum_Ht_RefTrg_OfflineSel_SignalOR_PFJet450         -> Fill(HT);
      if(isEffvsOthers){
	hNum_eta6thJet_RefTrg_OfflineSel_SignalOR_PFJet450  -> Fill(Eta6thJet);
	hNum_phi6thJet_RefTrg_OfflineSel_SignalOR_PFJet450  -> Fill(Phi6thJet);
	hNum_pu_RefTrg_OfflineSel_SignalOR_PFJet450         -> Fill(PU);
	hNum_nBTagJets_RefTrg_OfflineSel_SignalOR_PFJet450  -> Fill(nBTagJets);
	hNum_JetMulti_RefTrg_OfflineSel_SignalOR_PFJet450   -> Fill(nJets);
	hNum_BJetMulti_RefTrg_OfflineSel_SignalOR_PFJet450  -> Fill(nBJets);
      }
    }
  //------------------------------------------
  
  
  // ----------------------------------------------------------
  //  Fill Plots with slices in HT and the Pt of the 6th Jet
  // ----------------------------------------------------------
  //Slices of HT
  if(HT>=450 && HT<600)
    {
      if(0) std::cout<<"\n\tHT>=450 && HT<600\t"<<HT<<std::endl;
      
      // Fill Denominator Plots
      h_Den_pt6thJet_Vs_450ht600_RefTrg_OfflineSel  -> Fill(Pt6thJet);
      
      // Fill Numerator Plots
      if (Passed_HLT_PFHT450_SixJet40_BTagCSV_p056){
	h_Num_pt6thJet_Vs_450ht600_RefTrg_OfflineSel_1BTag -> Fill(Pt6thJet);
      }
      if (Passed_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056){
        h_Num_pt6thJet_Vs_450ht600_RefTrg_OfflineSel_2BTag -> Fill(Pt6thJet);
      }
      if (Passed_OR){
	h_Num_pt6thJet_Vs_450ht600_RefTrg_OfflineSel_OR    -> Fill(Pt6thJet);
      } 

    } // end   if(HT>=450 && HT<600)
  
  else if(HT>=600 && HT<800)
    {
      if(0) std::cout<<"\n\tHT>=600 && HT<800\t"<<HT<<std::endl;

      // Fill Denominator Plots
      h_Den_pt6thJet_Vs_600ht800_RefTrg_OfflineSel  -> Fill(Pt6thJet);
      
      // Fill Numerator Plots
      if (Passed_HLT_PFHT450_SixJet40_BTagCSV_p056){
	h_Num_pt6thJet_Vs_600ht800_RefTrg_OfflineSel_1BTag -> Fill(Pt6thJet);
      }
      if (Passed_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056){
        h_Num_pt6thJet_Vs_600ht800_RefTrg_OfflineSel_2BTag -> Fill(Pt6thJet);
      }
      if (Passed_OR){
	h_Num_pt6thJet_Vs_600ht800_RefTrg_OfflineSel_OR    -> Fill(Pt6thJet);
      } 

      
    } // end   if(HT>=600 && HT<800)
  
  else if(HT>=800 && HT<1000)
    {
      if(0) std::cout<<"\n\tHT>=800 && HT<1000\t"<<HT<<std::endl;

      // Fill Denominator Plots
      h_Den_pt6thJet_Vs_800ht1000_RefTrg_OfflineSel  -> Fill(Pt6thJet);
      
      // Fill Numerator Plots
      if (Passed_HLT_PFHT450_SixJet40_BTagCSV_p056){
	h_Num_pt6thJet_Vs_800ht1000_RefTrg_OfflineSel_1BTag -> Fill(Pt6thJet);
      }
      if (Passed_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056){
        h_Num_pt6thJet_Vs_800ht1000_RefTrg_OfflineSel_2BTag -> Fill(Pt6thJet);
      }
      if (Passed_OR){
	h_Num_pt6thJet_Vs_800ht1000_RefTrg_OfflineSel_OR    -> Fill(Pt6thJet);
      } 

    } // end   if(HT>=800 && HT<1000)
  
  else if(HT>=1000 && HT<1250)
    {
      if(0) std::cout<<"\n\tHT>=1000 && HT<1250\t"<<HT<<std::endl;

      // Fill Denominator Plots
      h_Den_pt6thJet_Vs_1000ht1250_RefTrg_OfflineSel  -> Fill(Pt6thJet);
      
      // Fill Numerator Plots
      if (Passed_HLT_PFHT450_SixJet40_BTagCSV_p056){
	h_Num_pt6thJet_Vs_1000ht1250_RefTrg_OfflineSel_1BTag -> Fill(Pt6thJet);
      }
      if (Passed_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056){
        h_Num_pt6thJet_Vs_1000ht1250_RefTrg_OfflineSel_2BTag -> Fill(Pt6thJet);
      }
      if (Passed_OR){
	h_Num_pt6thJet_Vs_1000ht1250_RefTrg_OfflineSel_OR    -> Fill(Pt6thJet);
      } 
      
      
    } // end   if(HT>=1000 && HT<1250)
  
  else if(HT>=1250 && HT<1500)
    {
      if(0) std::cout<<"\n\tHT>=1250 && HT<1500\t"<<HT<<std::endl;
      
      // Fill Denominator Plots
      h_Den_pt6thJet_Vs_1250ht1500_RefTrg_OfflineSel  -> Fill(Pt6thJet);
      
      // Fill Numerator Plots
      if (Passed_HLT_PFHT450_SixJet40_BTagCSV_p056){
	h_Num_pt6thJet_Vs_1250ht1500_RefTrg_OfflineSel_1BTag -> Fill(Pt6thJet);
      }
      if (Passed_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056){
        h_Num_pt6thJet_Vs_1250ht1500_RefTrg_OfflineSel_2BTag -> Fill(Pt6thJet);
      }
      if (Passed_OR){
	h_Num_pt6thJet_Vs_1250ht1500_RefTrg_OfflineSel_OR    -> Fill(Pt6thJet);
      } 
     
      
    } // end   if(HT>=1250 && HT<1500)
  
  else if(HT>=1500 && HT<2000)
    {
      if(0) std::cout<<"\n\tHT>=1500 && HT<2000\t"<<HT<<std::endl;


      // Fill Denominator Plots
      h_Den_pt6thJet_Vs_1500ht2000_RefTrg_OfflineSel  -> Fill(Pt6thJet);
      
      // Fill Numerator Plots
      if (Passed_HLT_PFHT450_SixJet40_BTagCSV_p056){
	h_Num_pt6thJet_Vs_1500ht2000_RefTrg_OfflineSel_1BTag -> Fill(Pt6thJet);
      }
      if (Passed_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056){
        h_Num_pt6thJet_Vs_1500ht2000_RefTrg_OfflineSel_2BTag -> Fill(Pt6thJet);
      }
      if (Passed_OR){
	h_Num_pt6thJet_Vs_1500ht2000_RefTrg_OfflineSel_OR    -> Fill(Pt6thJet);
      }
      
    } // end   if(HT>=1500 && HT<2000)



  if(Pt6thJet>=40 && Pt6thJet<50)
    {
      if(0) std::cout<<"\n\tPt6thJet>=40 && Pt6thJet<50\t"<<Pt6thJet<<std::endl;      
      
      // Fill Denominator Plots
      h_Den_ht_Vs_40pt50_RefTrg_OfflineSel        -> Fill(HT);
      
      // Fill Numerator Plots
      if (Passed_HLT_PFHT450_SixJet40_BTagCSV_p056){
	h_Num_ht_Vs_40pt50_RefTrg_OfflineSel_1BTag       -> Fill(HT);
      }
      if (Passed_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056){
        h_Num_ht_Vs_40pt50_RefTrg_OfflineSel_2BTag       -> Fill(HT);
      }
      if (Passed_OR){
        h_Num_ht_Vs_40pt50_RefTrg_OfflineSel_OR          -> Fill(HT);
      }


    }
  if(Pt6thJet>=50 && Pt6thJet<60)
    {
      if(0) std::cout<<"\n\tPt6thJet>=50 && Pt6thJet<60\t"<<Pt6thJet<<std::endl;      

            
      // Fill Denominator Plots
      h_Den_ht_Vs_50pt60_RefTrg_OfflineSel        -> Fill(HT);
      
      // Fill Numerator Plots
      if (Passed_HLT_PFHT450_SixJet40_BTagCSV_p056){
	h_Num_ht_Vs_50pt60_RefTrg_OfflineSel_1BTag       -> Fill(HT);
      }
      if (Passed_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056){
        h_Num_ht_Vs_50pt60_RefTrg_OfflineSel_2BTag       -> Fill(HT);
      }
      if (Passed_OR){
        h_Num_ht_Vs_50pt60_RefTrg_OfflineSel_OR          -> Fill(HT);
      }



    }
  if(Pt6thJet>=60 && Pt6thJet<70)
    {
      if(0) std::cout<<"\n\tPt6thJet>=60 && Pt6thJet<70\t"<<Pt6thJet<<std::endl;      

                  
      // Fill Denominator Plots
      h_Den_ht_Vs_60pt70_RefTrg_OfflineSel        -> Fill(HT);
      
      // Fill Numerator Plots
      if (Passed_HLT_PFHT450_SixJet40_BTagCSV_p056){
	h_Num_ht_Vs_60pt70_RefTrg_OfflineSel_1BTag       -> Fill(HT);
      }
      if (Passed_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056){
        h_Num_ht_Vs_60pt70_RefTrg_OfflineSel_2BTag       -> Fill(HT);
      }
      if (Passed_OR){
        h_Num_ht_Vs_60pt70_RefTrg_OfflineSel_OR          -> Fill(HT);
      }



    }
  if(Pt6thJet>=70 && Pt6thJet<90)
    {
      if(0) std::cout<<"\n\tPt6thJet>=70 && Pt6thJet<90\t"<<Pt6thJet<<std::endl;      

                  
      // Fill Denominator Plots
      h_Den_ht_Vs_70pt90_RefTrg_OfflineSel        -> Fill(HT);
      
      // Fill Numerator Plots
      if (Passed_HLT_PFHT450_SixJet40_BTagCSV_p056){
	h_Num_ht_Vs_70pt90_RefTrg_OfflineSel_1BTag       -> Fill(HT);
      }
      if (Passed_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056){
        h_Num_ht_Vs_70pt90_RefTrg_OfflineSel_2BTag       -> Fill(HT);
      }
      if (Passed_OR){
        h_Num_ht_Vs_70pt90_RefTrg_OfflineSel_OR          -> Fill(HT);
      }

      
    }
  if(Pt6thJet>=90 && Pt6thJet<120)
    {
      if(0) std::cout<<"\n\tPt6thJet>=90 && Pt6thJet<120\t"<<Pt6thJet<<std::endl;      
                        
      // Fill Denominator Plots
      h_Den_ht_Vs_90pt120_RefTrg_OfflineSel        -> Fill(HT);
      
      // Fill Numerator Plots
      if (Passed_HLT_PFHT450_SixJet40_BTagCSV_p056){
	h_Num_ht_Vs_90pt120_RefTrg_OfflineSel_1BTag       -> Fill(HT);
      }
      if (Passed_HLT_PFHT400_SixJet30_DoubleBTagCSV_p056){
        h_Num_ht_Vs_90pt120_RefTrg_OfflineSel_2BTag       -> Fill(HT);
      }
      if (Passed_OR){
        h_Num_ht_Vs_90pt120_RefTrg_OfflineSel_OR          -> Fill(HT);
      }
  

      }
  //---------------------

  //================================================================================================
  // Finalize
  //================================================================================================
  fEventSaver.save();
}


double JetTriggersSF::DeltaEta(double eta1, double eta2)
{

  // See: https://cmssdt.cern.ch/SDT/doxygen/CMSSW_4_4_2/doc/html/d1/d92/DataFormats_2Math_2interface_2deltaPhi_8h_source.html                                                                                             
  double deltaEta = fabs ( eta1 - eta2 );
  return deltaEta;

}

double JetTriggersSF::DeltaPhi(double phi1, double phi2)
{
  // See: https://cmssdt.cern.ch/SDT/doxygen/CMSSW_4_4_2/doc/html/d1/d92/DataFormats_2Math_2interface_2deltaPhi_8h_source.html                                                                                             
  double PI = 3.14159265;
  double result = phi1 - phi2;
  while (result > PI) result -= 2*PI;
  while (result <= -PI) result += 2*PI;

  return result;
}

double JetTriggersSF::DeltaR(double eta1, double eta2,
                             double phi1, double phi2)
{

  double dEta = DeltaEta(eta1, eta2);
  double dPhi = DeltaPhi(phi1, phi2);
  double dR = TMath::Sqrt(TMath::Power(dEta,2)+TMath::Power(dPhi,2));

  return dR;
}


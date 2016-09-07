// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

// User
#include "Auxiliary/interface/Table.h"
#include "Auxiliary/interface/Tools.h"
#include "Tools/interface/MCTools.h"
#include "Tools/interface/DirectionalCut.h"
#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

// ROOT
#include "TDirectory.h"
#include "Math/VectorUtil.h"

struct PtComparator
{
  bool operator() (const math::XYZTLorentzVector p1, const math::XYZTLorentzVector p2) const { return ( p1.pt() > p2.pt() ); }
};


class Kinematics: public BaseSelector {
public:
  explicit Kinematics(const ParameterSet& config, const TH1* skimCounters);
  virtual ~Kinematics() {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;
   
private:
  // Input parameters
  const double cfg_Verbose;
  const ParameterSet PSet_JetSelection;
  const double cfg_JetPtCut;
  const double cfg_JetEtaCut;
  const DirectionalCut<int> cfg_JetNumberCut;
  const ParameterSet PSet_ElectronSelection;
  const double cfg_ElectronPtCut;
  const double cfg_ElectronEtaCut;
  const DirectionalCut<int> cfg_ElectronNumberCut;
  const ParameterSet PSet_MuonSelection;
  const double cfg_MuonPtCut;
  const double cfg_MuonEtaCut;
  const DirectionalCut<int> cfg_MuonNumberCut;
  const ParameterSet PSet_HtSelection;
  const DirectionalCut<float> cfg_HtCut;
  const HistogramSettings cfg_PtBinSetting;
  const HistogramSettings cfg_EtaBinSetting;
  const HistogramSettings cfg_PhiBinSetting;
  const HistogramSettings cfg_MassBinSetting;
  const HistogramSettings cfg_DeltaEtaBinSetting;
  const HistogramSettings cfg_DeltaPhiBinSetting;
  const HistogramSettings cfg_DeltaRBinSetting;
  
  Tools auxTools;
  
  // Counters
  Count cAllEvents;  
  Count cSubNoPreselections;
  Count cSubPassedLeptonVeto;
  Count cSubPassedJetsCut;
  Count cSubPassedHtCut;
  
  // Event Variables
  WrappedTH1 *h_genMET_Et;
  WrappedTH1 *h_genMET_Phi;
  WrappedTH1 *h_genHT_GenJets;  
  WrappedTH1 *h_SelGenJet_N_NoPreselections;
  WrappedTH1 *h_SelGenJet_N_AfterLeptonVeto;
  WrappedTH1 *h_SelGenJet_N_AfterLeptonVetoNJetsCut;
  WrappedTH1 *h_SelGenJet_N_AfterPreselections;  
  
  // GenParticles: BQuarks
  WrappedTH1 *h_BQuarks_N;
  WrappedTH1 *h_BQuark1_Pt;
  WrappedTH1 *h_BQuark2_Pt;
  WrappedTH1 *h_BQuark3_Pt;
  WrappedTH1 *h_BQuark4_Pt;
  //
  WrappedTH1 *h_BQuark1_Eta;
  WrappedTH1 *h_BQuark2_Eta;
  WrappedTH1 *h_BQuark3_Eta;
  WrappedTH1 *h_BQuark4_Eta;

  // GenParticles: BQuarks pair closest together
  WrappedTH1 *h_BQuarkPair_dRMin_pT;
  WrappedTH1 *h_BQuarkPair_dRMin_dEta;
  WrappedTH1 *h_BQuarkPair_dRMin_dPhi;
  WrappedTH1 *h_BQuarkPair_dRMin_dR;
  WrappedTH1 *h_BQuarkPair_dRMin_Mass;
  WrappedTH2 *h_BQuarkPair_dRMin_Eta1_Vs_Eta2;
  WrappedTH2 *h_BQuarkPair_dRMin_Phi1_Vs_Phi2;
  WrappedTH2 *h_BQuarkPair_dRMin_Pt1_Vs_Pt2;
  WrappedTH2 *h_BQuarkPair_dRMin_dEta_Vs_dPhi;
  WrappedTH1 *h_BQuarkPair_dRMin_jet1_dR;
  WrappedTH1 *h_BQuarkPair_dRMin_jet1_dEta;
  WrappedTH1 *h_BQuarkPair_dRMin_jet1_dPhi;
  WrappedTH1 *h_BQuarkPair_dRMin_jet2_dR;
  WrappedTH1 *h_BQuarkPair_dRMin_jet2_dEta;
  WrappedTH1 *h_BQuarkPair_dRMin_jet2_dPhi;

  // GenParticles: bqq trijet system (H+)
  WrappedTH1 *h_tbWPlus_bqq_Pt;
  WrappedTH1 *h_tbWPlus_bqq_Rap;
  WrappedTH1 *h_tbWPlus_bqq_Mass;
  WrappedTH1 *h_tbWPlus_bqq_dRMax_dR;
  WrappedTH1 *h_tbWPlus_bqq_dRMax_dRap;
  WrappedTH1 *h_tbWPlus_bqq_dRMax_dPhi;
  WrappedTH2 *h_tbWPlus_bqq_dRMax_dRap_Vs_dPhi;

  // GenParticles: bqq trijet system (associated top)
  WrappedTH1 *h_tbWMinus_bqq_Pt;
  WrappedTH1 *h_tbWMinus_bqq_Rap;
  WrappedTH1 *h_tbWMinus_bqq_Mass;
  WrappedTH1 *h_tbWMinus_bqq_dRMax_dR;
  WrappedTH1 *h_tbWMinus_bqq_dRMax_dRap;
  WrappedTH1 *h_tbWMinus_bqq_dRMax_dPhi;
  WrappedTH2 *h_tbWMinus_bqq_dRMax_dRap_Vs_dPhi;

  // GenJets
  WrappedTH1 *h_GenJet1_Pt;
  WrappedTH1 *h_GenJet2_Pt;
  WrappedTH1 *h_GenJet3_Pt;
  WrappedTH1 *h_GenJet4_Pt;
  WrappedTH1 *h_GenJet5_Pt;
  WrappedTH1 *h_GenJet6_Pt;
  //
  WrappedTH1 *h_GenJet1_Eta;
  WrappedTH1 *h_GenJet2_Eta;
  WrappedTH1 *h_GenJet3_Eta;
  WrappedTH1 *h_GenJet4_Eta;
  WrappedTH1 *h_GenJet5_Eta;
  WrappedTH1 *h_GenJet6_Eta;

  // GenJets: Dijet with largest mass
  WrappedTH1 *h_MaxDiJetMass_Pt;
  WrappedTH1 *h_MaxDiJetMass_Eta;
  WrappedTH1 *h_MaxDiJetMass_Rap; 
  WrappedTH1 *h_MaxDiJetMass_Mass;
  WrappedTH1 *h_MaxDiJetMass_dR;
  WrappedTH1 *h_MaxDiJetMass_dRrap;
  WrappedTH1 *h_MaxDiJetMass_dEta;
  WrappedTH1 *h_MaxDiJetMass_dPhi;
  WrappedTH1 *h_MaxDiJetMass_dRap;
  WrappedTH2 *h_MaxDiJetMass_dEta_Vs_dPhi;
  WrappedTH2 *h_MaxDiJetMass_dRap_Vs_dPhi;  

  // Correlations 
  WrappedTH2 *h_BQuark1_BQuark2_dEta_Vs_dPhi;
  WrappedTH2 *h_BQuark1_BQuark3_dEta_Vs_dPhi;
  WrappedTH2 *h_BQuark1_BQuark4_dEta_Vs_dPhi;
  WrappedTH2 *h_BQuark2_BQuark3_dEta_Vs_dPhi;
  WrappedTH2 *h_BQuark2_BQuark4_dEta_Vs_dPhi;
  WrappedTH2 *h_BQuark3_BQuark4_dEta_Vs_dPhi;

  WrappedTH2 *h_Jet1Jet2_dEta_Vs_Jet3Jet4_dEta;
  WrappedTH2 *h_Jet1Jet2_dPhi_Vs_Jet3Jet4_dPhi;  
  WrappedTH2 *h_Jet1Jet2_dEta_Vs_Jet1Jet2_Mass;
  WrappedTH2 *h_Jet3Jet4_dEta_Vs_Jet3Jet4_Mass;

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(Kinematics);

Kinematics::Kinematics(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_Verbose(config.getParameter<bool>("verbose")),
    PSet_JetSelection(config.getParameter<ParameterSet>("JetSelection")),
    cfg_JetPtCut(config.getParameter<float>("JetSelection.jetPtCut")),
    cfg_JetEtaCut(config.getParameter<float>("JetSelection.jetEtaCut")),
    cfg_JetNumberCut(config, "JetSelection.jetNCut"),
    PSet_ElectronSelection(config.getParameter<ParameterSet>("ElectronSelection")),
    cfg_ElectronPtCut(config.getParameter<float>("ElectronSelection.electronPtCut")),  
    cfg_ElectronEtaCut(config.getParameter<float>("ElectronSelection.electronEtaCut")),
    cfg_ElectronNumberCut(config, "ElectronSelection.electronNCut"),
    PSet_MuonSelection(config.getParameter<ParameterSet>("MuonSelection")),
    cfg_MuonPtCut(config.getParameter<float>("MuonSelection.muonPtCut")),
    cfg_MuonEtaCut(config.getParameter<float>("MuonSelection.muonEtaCut")),
    cfg_MuonNumberCut(config, "MuonSelection.muonNCut"),
    PSet_HtSelection(config.getParameter<ParameterSet>("HtSelection")),
    cfg_HtCut(config, "HtSelection.HtCut"),
    cfg_PtBinSetting(config.getParameter<ParameterSet>("CommonPlots.ptBins")),
    cfg_EtaBinSetting(config.getParameter<ParameterSet>("CommonPlots.etaBins")),
    cfg_PhiBinSetting(config.getParameter<ParameterSet>("CommonPlots.phiBins")),
    cfg_MassBinSetting(config.getParameter<ParameterSet>("CommonPlots.invmassBins")),
    cfg_DeltaEtaBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaEtaBins")),
    cfg_DeltaPhiBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaPhiBins")),
    cfg_DeltaRBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaRBins")),
    cAllEvents(fEventCounter.addCounter("All events")),
    cSubNoPreselections(fEventCounter.addSubCounter("Preselections", "All Events")),
    cSubPassedLeptonVeto(fEventCounter.addSubCounter("Preselections", "Lepton Veto")),
    cSubPassedJetsCut(fEventCounter.addSubCounter("Preselections", "Jets Cut")),
    cSubPassedHtCut(fEventCounter.addSubCounter("Preselections","HT Cut"))
{ }

void Kinematics::book(TDirectory *dir) {

  Table cuts("Variable | Jets | Electron | Muon | HT", "Text"); //LaTeX or Text
  cuts.AddRowColumn(0, "Pt (GeV/c)");
  cuts.AddRowColumn(1, "Eta");
  cuts.AddRowColumn(2, "Cut Direction");
  cuts.AddRowColumn(3, "Cut Value");
  //  
  cuts.AddRowColumn(0, auxTools.ToString(cfg_JetPtCut) );
  cuts.AddRowColumn(0, auxTools.ToString(cfg_ElectronPtCut) );
  cuts.AddRowColumn(0, auxTools.ToString(cfg_MuonPtCut) );
  cuts.AddRowColumn(0, "-");
  //
  cuts.AddRowColumn(1, auxTools.ToString(cfg_JetEtaCut) );
  cuts.AddRowColumn(1, auxTools.ToString(cfg_ElectronEtaCut) );
  cuts.AddRowColumn(1, auxTools.ToString(cfg_MuonEtaCut) );
  cuts.AddRowColumn(1, "-");
  //
  cuts.AddRowColumn(2, PSet_JetSelection.getParameter<string>("jetNCutDirection") );
  cuts.AddRowColumn(2, PSet_ElectronSelection.getParameter<string>("electronNCutDirection") );
  cuts.AddRowColumn(2, PSet_MuonSelection.getParameter<string>("muonNCutDirection") );
  cuts.AddRowColumn(2, PSet_HtSelection.getParameter<string>("HtCutDirection") );
  //
  cuts.AddRowColumn(3, auxTools.ToString(PSet_JetSelection.getParameter<int>("jetNCutValue")) );
  cuts.AddRowColumn(3, auxTools.ToString(PSet_ElectronSelection.getParameter<int>("electronNCutValue")) );
  cuts.AddRowColumn(3, auxTools.ToString(PSet_MuonSelection.getParameter<int>("muonNCutValue")) );
  cuts.AddRowColumn(3, PSet_HtSelection.getParameter<string>("HtCutValue") );
  //
  std::cout << "\n" << std::endl;
  cuts.Print();

  
  // Fixed binning
  const int nBinsPt   = cfg_PtBinSetting.bins();
  const double minPt  = cfg_PtBinSetting.min();
  const double maxPt  = cfg_PtBinSetting.max();

  const int nBinsEta  = cfg_EtaBinSetting.bins();
  const double minEta = cfg_EtaBinSetting.min();
  const double maxEta = cfg_EtaBinSetting.max();

  const int nBinsRap  = cfg_EtaBinSetting.bins();
  const double minRap = cfg_EtaBinSetting.min();
  const double maxRap = cfg_EtaBinSetting.max();

  const int nBinsPhi  = cfg_PhiBinSetting.bins();
  const double minPhi = cfg_PhiBinSetting.min();
  const double maxPhi = cfg_PhiBinSetting.max();

  const int nBinsM  = cfg_MassBinSetting.bins();
  const double minM = cfg_MassBinSetting.min();
  const double maxM = cfg_MassBinSetting.max();
  
  const int nBinsdEta  = cfg_DeltaEtaBinSetting.bins();
  const double mindEta = cfg_DeltaEtaBinSetting.min();
  const double maxdEta = cfg_DeltaEtaBinSetting.max();

  const int nBinsdRap  = cfg_DeltaEtaBinSetting.bins();
  const double mindRap = cfg_DeltaEtaBinSetting.min();
  const double maxdRap = cfg_DeltaEtaBinSetting.max();

  const int nBinsdPhi  = cfg_DeltaPhiBinSetting.bins();
  const double mindPhi = cfg_DeltaPhiBinSetting.min();
  const double maxdPhi = cfg_DeltaPhiBinSetting.max();

  const int nBinsdR  = cfg_DeltaRBinSetting.bins();
  const double mindR = cfg_DeltaRBinSetting.min();
  const double maxdR = cfg_DeltaRBinSetting.max();

    
  // Event Variables
  h_genMET_Et         =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genMET_Et"          , ";Gen E_{T}^{miss} (GeV)"       , 60,  0.0,   +300.0);
  h_genMET_Phi        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "genMET_Phi"         , ";Gen E_{T}^{miss} #phi (rads)" , nBinsPhi, minPhi, maxPhi);
  h_genHT_GenJets     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genHT_GenJets"      , ";GenJ H_{T} (GeV)"             ,  75,  0.0, +1500.0);  
  
  // GenParticles: B-quarks
  h_BQuarks_N   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarks_N" , ";N (b-quarks)" , 10, -0.5, +9.5);
  h_BQuark1_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark1_Pt", ";p_{T} (GeV/c)" , nBinsPt, minPt, maxPt);
  h_BQuark2_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark2_Pt", ";p_{T} (GeV/c)" , nBinsPt, minPt, maxPt);
  h_BQuark3_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark3_Pt", ";p_{T} (GeV/c)" , nBinsPt, minPt, maxPt);
  h_BQuark4_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark4_Pt", ";p_{T} (GeV/c)" , nBinsPt, minPt, maxPt);

  h_BQuark1_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark1_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_BQuark2_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark2_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_BQuark3_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark3_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_BQuark4_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark4_Eta", ";#eta", nBinsEta, minEta, maxEta);

  // GenParticles: BQuarks pair closest together
  h_BQuarkPair_dRMin_pT   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_pT"  , ";p_{T} (GeV/c)"     ,  nBinsPt, minPt, maxPt);
  h_BQuarkPair_dRMin_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_dEta", ";#Delta#eta"        ,  nBinsdEta, mindEta, maxdEta);
  h_BQuarkPair_dRMin_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_dPhi", ";#Delta#phi (rads)" ,  nBinsdPhi, mindPhi, maxdPhi);
  h_BQuarkPair_dRMin_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_dR"  , ";#DeltaR"           ,  nBinsdR, mindR, maxdR);
  h_BQuarkPair_dRMin_Mass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_Mass", ";M (GeV/c^{2})"     ,  nBinsM, minM, maxM);
  h_BQuarkPair_dRMin_Eta1_Vs_Eta2 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_Eta1_Vs_Eta2", ";#eta;#eta", nBinsEta, minEta, maxEta, nBinsEta, minEta, maxEta);
  h_BQuarkPair_dRMin_Phi1_Vs_Phi2 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_Phi1_Vs_Phi2", ";#phi;#phi", nBinsPhi, minPhi, maxPhi, nBinsPhi, minPhi, maxPhi);
  h_BQuarkPair_dRMin_Pt1_Vs_Pt2   = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_Pt1_Vs_Pt2"  , ";p_{T} (GeV/c); p_{T} (GeV/c)", nBinsPt, minPt, maxPt, nBinsPt, minPt, maxPt);
  h_BQuarkPair_dRMin_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  //
  h_BQuarkPair_dRMin_jet1_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_jet1_dEta", ";#Delta#eta"        ,  nBinsdEta, mindEta, maxdEta);
  h_BQuarkPair_dRMin_jet1_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_jet1_dPhi", ";#Delta#phi (rads)" ,  nBinsdPhi, mindPhi, maxdPhi);
  h_BQuarkPair_dRMin_jet1_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_jet1_dR"  , ";#DeltaR"           ,  nBinsdR, mindR, maxdR);
  h_BQuarkPair_dRMin_jet2_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_jet2_dEta", ";#Delta#eta"        ,  nBinsdEta, mindEta, maxdEta);
  h_BQuarkPair_dRMin_jet2_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_jet2_dPhi", ";#Delta#phi (rads)" ,  nBinsdPhi, mindPhi, maxdPhi);
  h_BQuarkPair_dRMin_jet2_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_jet2_dR"  , ";#DeltaR"           ,  nBinsdR, mindR, maxdR);

  // GenParticles: bqq trijet system (W+)
  h_tbWPlus_bqq_Pt         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbWPlus_bqq_Pt"   , ";p_{T} (GeV/c)"    ,  nBinsPt, minPt, maxPt);
  h_tbWPlus_bqq_Rap        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbWPlus_bqq_Rap"  , ";#omega"           ,  nBinsRap, minRap, maxRap);
  h_tbWPlus_bqq_Mass       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbWPlus_bqq_Mass" , ";M (GeV/c^{2})"    ,  nBinsM, minM, maxM);
  //
  h_tbWPlus_bqq_dRMax_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbWPlus_bqq_dRMax_dPhi" , ";#Delta#phi (rads)",  nBinsdPhi, mindPhi, maxdPhi);
  h_tbWPlus_bqq_dRMax_dRap = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbWPlus_bqq_dRMax_dRap" , ";#Delta#omega"     ,  nBinsdRap, mindRap, maxdRap);
  h_tbWPlus_bqq_dRMax_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbWPlus_bqq_dRMax_dR"   , ";#DeltaR"          ,  nBinsdR, mindR, maxdR);
  h_tbWPlus_bqq_dRMax_dRap_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "tbWPlus_bqq_dRMax_dRap_Vs_dPhi", ";#Delta#omega;#Delta#phi (rads)", nBinsdRap, mindRap, maxdRap, nBinsdPhi, mindPhi, maxdPhi);

  // GenParticles: bqq trijet system (W-)
  h_tbWMinus_bqq_Pt         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbWMinus_bqq_Pt"   , ";p_{T} (GeV/c^{2})",  nBinsPt, minPt, maxPt);
  h_tbWMinus_bqq_Rap        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbWMinus_bqq_Rap"  , ";#omega"           ,  nBinsRap, minRap, maxRap);
  h_tbWMinus_bqq_Mass       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbWMinus_bqq_Mass" , ";M (GeV/c^{2})"    ,  nBinsM, minM, maxM);
  //
  h_tbWMinus_bqq_dRMax_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbWMinus_bqq_dRMax_dPhi", ";#Delta#phi (rads)",  nBinsdPhi, mindPhi, maxdPhi);
  h_tbWMinus_bqq_dRMax_dRap = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbWMinus_bqq_dRMax_dRap", ";#Delta#omega"     ,  nBinsdRap, mindRap, maxdRap);
  h_tbWMinus_bqq_dRMax_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbWMinus_bqq_dRMax_dR"  , ";#DeltaR"          ,  nBinsdR, mindR, maxdR);  
  h_tbWMinus_bqq_dRMax_dRap_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "tbWMinus_bqq_dRMax_dRap_Vs_dPhi", ";#Delta#omega;#Delta#phi (rads)", nBinsdRap, mindRap, maxdRap, nBinsdPhi, mindPhi, maxdPhi);
  
  // Leading Jets
  h_Jet1Jet2_dEta_Vs_Jet3Jet4_dEta = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "Jet1Jet2_dEta_Vs_Jet3Jet4_dEta", ";#Delta#eta(j_{1},j_{2});#Delta#eta(j_{3},j_{4})", nBinsdEta, mindEta, maxdEta, nBinsdEta, mindEta, maxdEta);

  h_Jet1Jet2_dPhi_Vs_Jet3Jet4_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "Jet1Jet2_dPhi_Vs_Jet3Jet4_dPhi", ";#Delta#phi(j_{1},j_{2}) (rads);#Delta#phi(j_{3},j_{4}) (rads)", nBinsdPhi, mindPhi, maxdPhi, nBinsdPhi, mindPhi, maxdPhi);

  h_Jet1Jet2_dEta_Vs_Jet1Jet2_Mass = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "Jet1Jet2_dEta_Vs_Jet1Jet2_Mass", ";#Delta#eta(j_{1},j_{2});M(j_{1},j_{2}) (GeV/c^{2})", nBinsdEta, mindEta, maxdEta, nBinsM, minM, maxM);

  h_Jet3Jet4_dEta_Vs_Jet3Jet4_Mass = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "Jet3Jet4_dEta_Vs_Jet3Jet4_Mass", ";#Delta#eta(j_{3},j_{4});M(j_{4},j_{4}) (GeV/c^{2})", nBinsdEta, mindEta, maxdEta, nBinsM, minM, maxM);
  
  // GenJets
  h_SelGenJet_N_NoPreselections         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelGenJet_N_NoPreselections"        , ";N (selected jets)" , 16, -0.5, +15.5);
  h_SelGenJet_N_AfterLeptonVeto         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelGenJet_N_AfterLeptonVeto"        , ";N (selected jets)" , 16, -0.5, +15.5);
  h_SelGenJet_N_AfterLeptonVetoNJetsCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelGenJet_N_AfterLeptonVetoNJetsCut", ";N (selected jets)" , 16, -0.5, +15.5);
  h_SelGenJet_N_AfterPreselections      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelGenJet_N_AfterPreselections"     , ";N (selected jets)" , 16, -0.5, +15.5);
  //
  h_GenJet1_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet1_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_GenJet2_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet2_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_GenJet3_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet3_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_GenJet4_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet4_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_GenJet5_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet5_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_GenJet6_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet6_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  //
  h_GenJet1_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet1_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_GenJet2_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet2_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_GenJet3_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet3_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_GenJet4_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet4_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_GenJet5_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet5_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_GenJet6_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet6_Eta", ";#eta", nBinsEta, minEta, maxEta);

  // GenJets: Dijet with largest mass
  h_MaxDiJetMass_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_Pt"   , ";p_{T} (GeV/c)"    , nBinsPt, minPt, maxPt);
  h_MaxDiJetMass_Eta   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_Eta"  , ";#eta"             , nBinsEta, minEta, maxEta);
  h_MaxDiJetMass_Rap   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_Rap"  , ";#omega"           , nBinsRap, minRap, maxRap);
  h_MaxDiJetMass_Mass  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_Mass" , ";M (GeV/c^{2})"    , 50,  0.0, +1000.0);  
  h_MaxDiJetMass_dEta  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_dEta" , ";#Delta#eta"       , nBinsdEta, mindEta, maxdEta);
  h_MaxDiJetMass_dRap  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_dRap" , ";#Delta#omega"     , nBinsdRap, mindRap, maxdRap);
  h_MaxDiJetMass_dPhi  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_dPhi" , ";#Delta#phi"       , nBinsdPhi, mindPhi, maxdPhi);  
  h_MaxDiJetMass_dR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_dR"   , ";#DeltaR"          , nBinsdR, mindR, maxdR);  
  h_MaxDiJetMass_dRrap = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_dRrap", ";#DeltaR_{#omega}" , nBinsdR, mindR, maxdR);  
  h_MaxDiJetMass_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "MaxDiJetMass_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)"  , nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_MaxDiJetMass_dRap_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "MaxDiJetMass_dRap_Vs_dPhi", ";#Delta#omega;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);

  // Correlations
  h_BQuark1_BQuark2_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuark1_BQuark2_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_BQuark1_BQuark3_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuark1_BQuark3_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_BQuark1_BQuark4_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuark1_BQuark4_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_BQuark2_BQuark3_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuark2_BQuark3_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_BQuark2_BQuark4_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuark2_BQuark4_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_BQuark3_BQuark4_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuark3_BQuark4_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);

  return;
}

void Kinematics::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}


void Kinematics::process(Long64_t entry) {

  if ( !fEvent.isMC() ) return;
  
  // Create MCools object
  MCTools mcTools(fEvent);
  
  // Increment Counter
  cAllEvents.increment();
  

  ///////////////////////////////////////////////////////////////////////////
  // GenJets Calculations
  /////////////////////////////////////////////////////////////////////////// 
  std::vector<math::XYZTLorentzVector> selJets_p4;
  int nSelJets   = 0;
  double genJ_HT = 0.0;

  // For-loop: GenJets
  for(GenJet j: fEvent.genjets()) {

    math::XYZTLorentzVector genJ_p4;
    genJ_p4 = j.p4();
    double genJ_pt     = j.pt();
    double genJ_eta    = j.eta();
    // double genJ_pdgId  = j.pdgId();

    // Apply selection cuts
    if (genJ_pt < cfg_JetPtCut) continue;
    if (std::abs(genJ_eta) > cfg_JetEtaCut) continue;
    
    // Do calculations
    nSelJets++;
    selJets_p4.push_back( genJ_p4 );
    genJ_HT += genJ_pt;
  }
 

  ///////////////////////////////////////////////////////////////////////////
  // GenParticles 
  ///////////////////////////////////////////////////////////////////////////
  int nElectrons = 0;
  int nMuons     = 0;

  std::vector<math::XYZTLorentzVector> bQuarks_p4;
  std::vector<math::XYZTLorentzVector> tQuarks_p4;

  math::XYZTLorentzVector tbWPlus_BQuark_p4;
  math::XYZTLorentzVector tbWPlus_Wqq_Quark_p4;
  math::XYZTLorentzVector tbWPlus_Wqq_AntiQuark_p4;
  math::XYZTLorentzVector tbWMinus_BQuark_p4;
  math::XYZTLorentzVector tbWMinus_Wqq_Quark_p4;
  math::XYZTLorentzVector tbWMinus_Wqq_AntiQuark_p4;

  // Define the table
  Table table("Evt | Index | PdgId | Status | Charge | Pt | Eta | Phi | E | Vertex (mm) | Mothers | Daughters", "Text"); //LaTeX or Text
  
  int row = 0;
  // For-loop: GenParticles
  for (size_t genP_index=0; genP_index < fEvent.genparticles().getGenParticles().size(); genP_index++) {

    // Create the genParticles
    genParticle p = fEvent.genparticles().getGenParticles()[genP_index];
    genParticle m;
    genParticle g;

    // Particle properties
    int genP_pdgId       = p.pdgId();
    int genP_status      = p.status();
    
    // Other Particle properties
    double genP_pt       = p.pt();
    double genP_eta      = p.eta();
    double genP_phi      = p.phi();
    double genP_energy   = p.e();
    int genP_charge      = p.charge();
    double genP_vtxX     = p.vtxX()*10; // in mm
    double genP_vtxY     = p.vtxY()*10; // in mm
    double genP_vtxZ     = p.vtxZ()*10; // in mm
    std::vector<short> genP_daughters = p.daughters();
    std::vector<short> genP_mothers   = p.mothers();
    math::XYZTLorentzVector genP_p4;
    genP_p4 = p.p4();


    ///////////////////////////////////////////////////////////////////////////
    // Filtering
    ///////////////////////////////////////////////////////////////////////////
    // if (!p.isPrompt()) continue;
    // if (!p.isPromptDecayed()) continue;
    // if (!p.isPromptFinalState()) continue;
    // if (!p.isDecayedLeptonHadron()) continue;
    // if (!p.isTauDecayProduct()) continue;
    // if (!p.isPromptTauDecayProduct()) continue;
    // if (!p.isDirectTauDecayProduct()) continue;
    // if (!p.isDirectPromptTauDecayProduct()) continue;
    // if (!p.isDirectPromptTauDecayProductFinalState()) continue;
    // if (!p.isDirectHadronDecayProduct()) continue;	
    // if (!p.isDirectHardProcessTauDecayProductFinalState()) continue;
    if (!p.isHardProcess()) continue;
    // if (!p.fromHardProcess()) continue;
    // if (!p.fromHardProcessDecayed()) continue;
    // if (!p.fromHardProcessFinalState()) continue;
    // if (!p.isHardProcessTauDecayProduct()) continue;
    // if (!p.isDirectHardProcessTauDecayProduct()) continue;
    // if (!p.fromHardProcessBeforeFSR()) continue;
    // if (!p.isFirstCopy()) continue;
    // if (!p.isLastCopy()) continue;
    // if (!p.isLastCopyBeforeFSR()) continue;

    // mcTools.PrintGenParticle(44);
    // mcTools.PrintDaughters(44, false);
    // mcTools.PrintDaughters(genP_index, true);
    // TESTING

    // Add table rows
    if (cfg_Verbose)
      {
	table.AddRowColumn(row, auxTools.ToString(entry)           );
	table.AddRowColumn(row, auxTools.ToString(genP_index)      );
	table.AddRowColumn(row, auxTools.ToString(genP_pdgId)      );
	table.AddRowColumn(row, auxTools.ToString(genP_status)     );
	table.AddRowColumn(row, auxTools.ToString(genP_charge)     );
	table.AddRowColumn(row, auxTools.ToString(genP_pt , 3)     );
	table.AddRowColumn(row, auxTools.ToString(genP_eta, 4)     );
	table.AddRowColumn(row, auxTools.ToString(genP_phi, 3)     );
	table.AddRowColumn(row, auxTools.ToString(genP_energy, 3)  );
	table.AddRowColumn(row, "(" + auxTools.ToString(genP_vtxX, 3) + ", " + auxTools.ToString(genP_vtxY, 3)  + ", " + auxTools.ToString(genP_vtxZ, 3) + ")" );
	// table.AddRowColumn(row, auxTools.ToString(genP_d0,  3)     );
	// table.AddRowColumn(row, auxTools.ToString(genP_Lxy, 3)     );
	table.AddRowColumn(row, auxTools.ConvertIntVectorToString(genP_mothers) );
	if (genP_daughters.size() < 6)
	  {
	    table.AddRowColumn(row, auxTools.ConvertIntVectorToString(genP_daughters) );
	  }
	else table.AddRowColumn(row, ".. Too many .." );
	row++;
      }


    // Leptons    
    if( mcTools.IsLepton(p.pdgId() ) )
      {
	
	if ( std::abs(p.pdgId()) == 11)
	  {		      
	    if ( (p.p4().pt() >= cfg_ElectronPtCut) && ( std::abs(p.p4().eta()) <= cfg_ElectronEtaCut) ) nElectrons++;
	  }
	else if ( std::abs(p.pdgId()) == 13)
	  {
	    if ( (p.p4().pt() >= cfg_MuonPtCut) && ( std::abs(p.p4().eta()) <= cfg_MuonEtaCut) ) nMuons++;
	  }
      } // Leptons
   
    
    // Quarks
    if ( mcTools.IsQuark(genP_pdgId) )
      {
	
	// b-quarks
	if(std::abs(genP_pdgId) == 5)
	  {
	    
	    bQuarks_p4.push_back( genP_p4 );
	    
	    if ( mcTools.HasMother(genP_mothers, +6, false) ) tbWPlus_BQuark_p4  = genP_p4;
	    if ( mcTools.HasMother(genP_mothers, -6, false) ) tbWMinus_BQuark_p4 = genP_p4;
	    
	    
	  }// b-quarks
	
	// t-quarks
	if(std::abs(genP_pdgId) == 6)
	  {
	    
	    tQuarks_p4.push_back( genP_p4 );
	    
	  }//t-quarks
	
	
	// W-
	if ( mcTools.HasMother(genP_mothers, -24, false) )
	  {
	    
	    if (genP_pdgId > 0) tbWPlus_Wqq_Quark_p4 = genP_p4;
	    else tbWPlus_Wqq_AntiQuark_p4 = genP_p4;
	    
	  }//W-

	// W+
	if ( mcTools.HasMother(genP_mothers, +24, false) )
	  {

	    if (genP_pdgId > 0) tbWMinus_Wqq_Quark_p4 = genP_p4;
	    else tbWMinus_Wqq_AntiQuark_p4 = genP_p4;
	    
	  }// W+

      }// Quarks

    
  }//for-loop: genParticles
  

  ///////////////////////////////////////////////////////////////////////////
  // Preselection Cuts (python/parameters/hplus2tbAnalysis.py)
  ///////////////////////////////////////////////////////////////////////////
  cSubNoPreselections.increment();
  h_SelGenJet_N_NoPreselections->Fill(nSelJets);

  // Lepton Veto
  if ( !cfg_ElectronNumberCut.passedCut(nElectrons) ) return;
  if ( !cfg_MuonNumberCut.passedCut(nMuons) ) return;
  cSubPassedLeptonVeto.increment();
  h_SelGenJet_N_AfterLeptonVeto->Fill(nSelJets);
  
  // Jet Selection
  if ( !cfg_JetNumberCut.passedCut(selJets_p4.size()) ) return;  
  cSubPassedJetsCut.increment();
  h_SelGenJet_N_AfterLeptonVetoNJetsCut->Fill(nSelJets);
    
  // HT Selection
  if ( !cfg_HtCut.passedCut(genJ_HT) ) return;
  cSubPassedHtCut.increment();
  h_SelGenJet_N_AfterPreselections->Fill(nSelJets);  

  // Print the table with genP info
  if (cfg_Verbose) table.Print();  

  
  //////////////////////////////////////////////////////////////////////////////////////////////////////
  // Basic Variables
  //////////////////////////////////////////////////////////////////////////////////////////////////////
  h_genMET_Et  ->Fill(fEvent.genMET().et()); 
  h_genMET_Phi ->Fill(fEvent.genMET().Phi());
  h_genHT_GenJets->Fill(genJ_HT);

  
  //////////////////////////////////////////////////////////////////////////////////////////////////////
  // GenJets
  //////////////////////////////////////////////////////////////////////////////////////////////////////
  std::vector<math::XYZTLorentzVector> v_dijet_p4;
  std::vector<double> v_dijet_masses;
  std::vector<double> v_dijet_dR;
  std::vector<double> v_dijet_dRrap;
  std::vector<double> v_dijet_dEta;
  std::vector<double> v_dijet_dPhi;
  std::vector<double> v_dijet_dRap;
  
  double maxDijetMass_mass;
  math::XYZTLorentzVector maxDijetMass_p4;
  int maxDijetMass_pos;
  double maxDijetMass_dR;
  double maxDijetMass_dRrap;
  double maxDijetMass_dEta;
  double maxDijetMass_dPhi;
  double maxDijetMass_dRap;
  double maxDijetMass_rapidity;

  int iJet = 0;  
  // For-loop: All selected jets 
  for (size_t i=0; i < selJets_p4.size(); i++)
    {
      iJet++;
      double genJ_Pt  = selJets_p4.at(i).pt();
      double genJ_Eta = selJets_p4.at(i).eta();
      // double genJ_Rap = mcTools.GetRapidity(selJets_p4.at(i));
      
      if (iJet==1)
	{
	  h_GenJet1_Pt -> Fill( genJ_Pt  );
	  h_GenJet1_Eta-> Fill( genJ_Eta );
	}
      else if (iJet==2)
	{
	  h_GenJet2_Pt -> Fill( genJ_Pt  );
	  h_GenJet2_Eta-> Fill( genJ_Eta );
	}
      else if (iJet==3)
	{
	  h_GenJet3_Pt -> Fill( genJ_Pt  );
	  h_GenJet3_Eta-> Fill( genJ_Eta );
	}
      else if (iJet==4)
	{
	  h_GenJet4_Pt -> Fill( genJ_Pt  );
	  h_GenJet4_Eta-> Fill( genJ_Eta );
	}
      else if (iJet==5)
	{
	  h_GenJet5_Pt -> Fill( genJ_Pt  );
	  h_GenJet5_Eta-> Fill( genJ_Eta );
	}
      else if (iJet==6)
	{
	  h_GenJet6_Pt -> Fill( genJ_Pt  );
	  h_GenJet6_Eta-> Fill( genJ_Eta );
	}
      else{}
	
       // For-loop: All selected jets (nested)
       for (size_t j=i+1; j < selJets_p4.size(); j++)
       	{
       	  math::XYZTLorentzVector p4_i = selJets_p4.at(i);
       	  math::XYZTLorentzVector p4_j = selJets_p4.at(j);
       	  math::XYZTLorentzVector p4   = p4_i + p4_j;
       	  double rap_i = mcTools.GetRapidity(p4_i);
       	  double rap_j = mcTools.GetRapidity(p4_j);
       	  double dR    = ROOT::Math::VectorUtil::DeltaR(p4_i, p4_j);
       	  double dRap  = std::fabs(rap_i - rap_j);
       	  double dEta  = std::fabs(p4_i.eta() - p4_j.eta());
       	  double dPhi  = std::fabs(ROOT::Math::VectorUtil::DeltaPhi(p4_i, p4_j));
          
       	  v_dijet_p4.push_back( p4 );
       	  v_dijet_masses.push_back( p4.mass() );
       	  v_dijet_dR.push_back( dR );
       	  v_dijet_dRrap.push_back( sqrt( pow(dRap, 2) + pow(dPhi, 2) ) ); 
       	  v_dijet_dEta.push_back( dEta ); 
       	  v_dijet_dRap.push_back( dRap );
       	  v_dijet_dPhi.push_back( dPhi );

       	}
    }

  //////////////////////////////////////////////////////////////////////////////////////////////////////
  // MaxDiJet: DiJet combination with largest mass
  //////////////////////////////////////////////////////////////////////////////////////////////////////
  if (v_dijet_masses.size() > 0)
    {
      maxDijetMass_pos      = std::max_element(v_dijet_masses.begin(), v_dijet_masses.end()) - v_dijet_masses.begin();
      maxDijetMass_mass     = v_dijet_masses.at(maxDijetMass_pos);
      maxDijetMass_p4       = v_dijet_p4.at(maxDijetMass_pos);
      maxDijetMass_dR       = v_dijet_dR.at(maxDijetMass_pos);
      maxDijetMass_dRrap    = v_dijet_dRrap.at(maxDijetMass_pos);
      maxDijetMass_dEta     = v_dijet_dEta.at(maxDijetMass_pos);
      maxDijetMass_dPhi     = v_dijet_dPhi.at(maxDijetMass_pos);
      maxDijetMass_dRap     = v_dijet_dRap.at(maxDijetMass_pos);
      maxDijetMass_rapidity = mcTools.GetRapidity(maxDijetMass_p4);
    }

  // Fill histos
  h_MaxDiJetMass_Mass ->Fill( maxDijetMass_mass     );
  h_MaxDiJetMass_Pt   ->Fill( maxDijetMass_p4.pt()  );
  h_MaxDiJetMass_Eta  ->Fill( maxDijetMass_p4.eta() );
  h_MaxDiJetMass_Rap  ->Fill( maxDijetMass_rapidity );
  h_MaxDiJetMass_dR   ->Fill( maxDijetMass_dR       );
  h_MaxDiJetMass_dRrap->Fill( maxDijetMass_dRrap    );
  h_MaxDiJetMass_dEta ->Fill( maxDijetMass_dEta     );
  h_MaxDiJetMass_dPhi ->Fill( maxDijetMass_dPhi     );
  h_MaxDiJetMass_dRap ->Fill( maxDijetMass_dRap     );
  h_MaxDiJetMass_dEta_Vs_dPhi->Fill( maxDijetMass_dEta, maxDijetMass_dPhi );
  h_MaxDiJetMass_dRap_Vs_dPhi->Fill( maxDijetMass_dRap, maxDijetMass_dPhi );


  //////////////////////////////////////////////////////////////////////////////////////////////////////
  // GenJet Correlations
  //////////////////////////////////////////////////////////////////////////////////////////////////////  
  // Fill Histos
  if (selJets_p4.size() >= 2)
    {
      double jet1_Eta = selJets_p4.at(0).eta();
      double jet1_Phi = selJets_p4.at(0).phi();
      double jet2_Eta = selJets_p4.at(1).eta();
      double jet2_Phi = selJets_p4.at(1).phi();      
      h_Jet1Jet2_dEta_Vs_Jet1Jet2_Mass ->Fill(std::fabs(jet1_Eta - jet2_Eta), (selJets_p4.at(0) + selJets_p4.at(1)).mass() );

      if (selJets_p4.size() >= 4)
	{
	  double jet3_Eta = selJets_p4.at(2).eta();
	  double jet3_Phi = selJets_p4.at(2).phi();
	  double jet4_Eta = selJets_p4.at(3).eta();
	  double jet4_Phi = selJets_p4.at(3).phi();
	  h_Jet1Jet2_dEta_Vs_Jet3Jet4_dEta ->Fill(std::fabs(jet1_Eta - jet2_Eta), std::fabs(jet3_Eta - jet4_Eta));
	  h_Jet1Jet2_dPhi_Vs_Jet3Jet4_dPhi ->Fill(std::fabs(jet1_Phi - jet2_Phi), std::fabs(jet3_Phi - jet4_Phi));      
	  h_Jet3Jet4_dEta_Vs_Jet3Jet4_Mass ->Fill(std::fabs(jet3_Eta - jet4_Eta), (selJets_p4.at(2) + selJets_p4.at(3)).mass() );
	}     
    }  
    
  //////////////////////////////////////////////////////////////////////////////////////////////////////
  // Trijet system (W+)
  //////////////////////////////////////////////////////////////////////////////////////////////////////
  math::XYZTLorentzVector tbWPlus_bqq_p4 = tbWPlus_BQuark_p4 + tbWPlus_Wqq_Quark_p4 + tbWPlus_Wqq_AntiQuark_p4;

  // Find max separation
  std::vector<math::XYZTLorentzVector> bqq_p4;
  bqq_p4.push_back(tbWPlus_BQuark_p4);
  bqq_p4.push_back(tbWPlus_Wqq_Quark_p4);
  bqq_p4.push_back(tbWPlus_Wqq_AntiQuark_p4);
  double deltaRMax = -1.0;
  int deltaRMax_i  = -1;
  int deltaRMax_j  = -1;
  // For-loop: All p4 of bqq system
  for (size_t i = 0; i < bqq_p4.size(); i++)    
    {
      for (size_t j = i+1; j < bqq_p4.size(); j++)
	{
	  double deltaR = ROOT::Math::VectorUtil::DeltaR(bqq_p4.at(i), bqq_p4.at(j));
	  if (deltaR > deltaRMax)
	    {
	      deltaRMax   = deltaR;
	      deltaRMax_i = i;
	      deltaRMax_j = j;
	    }
	}
    } // For-loop: All p4 of bqq system
  
  // double bqq_dEta = std::fabs(bqq_p4.at(deltaRMax_i).eta() - bqq_p4.at(deltaRMax_j).eta());
  double bqq_dRap = -1.0;
  double bqq_dPhi = -1.0;

  if (deltaRMax_i >= 0 && deltaRMax_j >= 0)
    {
      bqq_dRap = std::fabs(mcTools.GetRapidity(bqq_p4.at(deltaRMax_i) ) - mcTools.GetRapidity(bqq_p4.at(deltaRMax_j) ) );
      bqq_dPhi = std::fabs(ROOT::Math::VectorUtil::DeltaPhi(bqq_p4.at(deltaRMax_i), bqq_p4.at(deltaRMax_j)));
    }
  
  // Fill Histos
  h_tbWPlus_bqq_Pt->Fill( tbWPlus_bqq_p4.pt());
  h_tbWPlus_bqq_Rap->Fill( mcTools.GetRapidity(tbWPlus_bqq_p4) );
  h_tbWPlus_bqq_Mass->Fill( tbWPlus_bqq_p4.mass() );
  h_tbWPlus_bqq_dRMax_dR->Fill( deltaRMax );
  h_tbWPlus_bqq_dRMax_dRap->Fill( bqq_dRap );
  h_tbWPlus_bqq_dRMax_dPhi->Fill( bqq_dPhi );
  h_tbWPlus_bqq_dRMax_dRap_Vs_dPhi->Fill( bqq_dRap, bqq_dPhi );
  
  
  //////////////////////////////////////////////////////////////////////////////////////////////////////
  // Trijet system (W-)
  //////////////////////////////////////////////////////////////////////////////////////////////////////
  math::XYZTLorentzVector tbWMinus_bqq_p4 = tbWMinus_Wqq_Quark_p4 + tbWMinus_Wqq_AntiQuark_p4 + tbWMinus_BQuark_p4;
  
  // Fix max separation (again)
  bqq_p4.clear();
  bqq_p4.push_back(tbWMinus_BQuark_p4);
  bqq_p4.push_back(tbWMinus_Wqq_Quark_p4);
  bqq_p4.push_back(tbWMinus_Wqq_AntiQuark_p4);
  deltaRMax    = -1.0;
  deltaRMax_i  = -1;
  deltaRMax_j  = -1;
  
  // For-loop: All p4 of bqq system
  for (size_t i = 0; i < bqq_p4.size(); i++)    
    {
      for (size_t j = i+1; j < bqq_p4.size(); j++)
	{
	  double deltaR = ROOT::Math::VectorUtil::DeltaR(bqq_p4.at(i), bqq_p4.at(j));
	  if (deltaR > deltaRMax)
	    {
	      deltaRMax   = deltaR;
	      deltaRMax_i = i;
	      deltaRMax_j = j;
	    }
	}
    } // For-loop: All p4 of bqq system
  
  bqq_dRap = std::fabs(mcTools.GetRapidity(bqq_p4.at(deltaRMax_i) ) - mcTools.GetRapidity(bqq_p4.at(deltaRMax_j) ) );
  bqq_dPhi = std::fabs(ROOT::Math::VectorUtil::DeltaPhi(bqq_p4.at(deltaRMax_i), bqq_p4.at(deltaRMax_j)));
  
  // Fill Histos
  h_tbWMinus_bqq_Pt->Fill( tbWMinus_bqq_p4.pt() );
  h_tbWMinus_bqq_Rap->Fill( mcTools.GetRapidity(tbWMinus_bqq_p4) );
  h_tbWMinus_bqq_Mass->Fill( tbWMinus_bqq_p4.mass() );
  h_tbWMinus_bqq_dRMax_dR->Fill( deltaRMax );
  h_tbWMinus_bqq_dRMax_dRap->Fill( bqq_dRap );
  h_tbWMinus_bqq_dRMax_dPhi->Fill( bqq_dPhi );
  h_tbWMinus_bqq_dRMax_dRap_Vs_dPhi ->Fill( bqq_dRap, bqq_dPhi );
  
  //////////////////////////////////////////////////////////////////////////////////////////////////////
  // B-quarks (pT sorted)
  //////////////////////////////////////////////////////////////////////////////////////////////////////
  std::sort( bQuarks_p4.begin(), bQuarks_p4.end(), PtComparator() );  
  double deltaRMin = 999999.9;
  int deltaRMin_i  = -1;
  int deltaRMin_j  = -1;  
  double dEta_1_2  = 999.9;
  double dPhi_1_2  = 999.9;
  double dEta_1_3  = 999.9;
  double dPhi_1_3  = 999.9;
  double dEta_2_3  = 999.9;
  double dPhi_2_3  = 999.9;
  double dEta_1_4  = 999.9;
  double dPhi_1_4  = 999.9;
  double dEta_2_4  = 999.9;
  double dPhi_2_4  = 999.9;
  double dEta_3_4  = 999.9;
  double dPhi_3_4  = 999.9;

  // For-loop: All (pT-sorted) b-quarks (FIXME)
  // for (size_t i = 0; i < bqq_p4.size(); i++)    
  //     {
  // 	for (size_t j = i+1; j < bqq_p4.size(); j++)
  // 	  {

  // Fill histos
  h_BQuarks_N->Fill(bQuarks_p4.size());
  
  // For-loop: All b-quarks
  for (size_t i = 0; i < bQuarks_p4.size(); i++)
    {
      
      if (bQuarks_p4.size() >= 2)
	{
	  dEta_1_2 = std::fabs(bQuarks_p4.at(0).eta() - bQuarks_p4.at(1).eta());
	  dPhi_1_2 = std::fabs(bQuarks_p4.at(0).phi() - bQuarks_p4.at(1).phi());
	}
      
      if (bQuarks_p4.size() >= 3) {
	dEta_1_3 = std::fabs(bQuarks_p4.at(0).eta() - bQuarks_p4.at(2).eta());
	dPhi_1_3 = std::fabs(bQuarks_p4.at(0).phi() - bQuarks_p4.at(2).phi());
	dEta_2_3 = std::fabs(bQuarks_p4.at(1).eta() - bQuarks_p4.at(2).eta());
	dPhi_2_3 = std::fabs(bQuarks_p4.at(1).phi() - bQuarks_p4.at(2).phi());
      }
      
      if (bQuarks_p4.size() >= 4) {
	dEta_1_4 = std::fabs(bQuarks_p4.at(0).eta() - bQuarks_p4.at(3).eta());
	dPhi_1_4 = std::fabs(bQuarks_p4.at(0).phi() - bQuarks_p4.at(3).phi());
	dEta_2_4 = std::fabs(bQuarks_p4.at(1).eta() - bQuarks_p4.at(3).eta());
	dPhi_2_4 = std::fabs(bQuarks_p4.at(1).phi() - bQuarks_p4.at(3).phi());
	dEta_3_4 = std::fabs(bQuarks_p4.at(2).eta() - bQuarks_p4.at(3).eta());
	dPhi_3_4 = std::fabs(bQuarks_p4.at(2).phi() - bQuarks_p4.at(3).phi());
      }
      
      // Fill 1D histos
      if (i==0)
	{
	  h_BQuark1_Pt ->Fill( bQuarks_p4.at(i).pt()  );
	  h_BQuark1_Eta->Fill( bQuarks_p4.at(i).eta() );
	}
      else if (i==1)
	{
	  h_BQuark2_Pt ->Fill( bQuarks_p4.at(i).pt()  );
	  h_BQuark2_Eta->Fill( bQuarks_p4.at(i).eta() );
	}
      else if (i==2)
	{
	  h_BQuark3_Pt ->Fill( bQuarks_p4.at(i).pt()  );
	  h_BQuark3_Eta->Fill( bQuarks_p4.at(i).eta() );
	}
      else if (i==3)
	{
	  h_BQuark4_Pt ->Fill( bQuarks_p4.at(i).pt()  );
	  h_BQuark4_Eta->Fill( bQuarks_p4.at(i).eta() );
	}
      else{}

      // Fill 2D histos      
      if (bQuarks_p4.size() >= 2)
	{
	  h_BQuark1_BQuark2_dEta_Vs_dPhi->Fill( dEta_1_2 , dPhi_1_2 );
	}
      
      if (bQuarks_p4.size() >= 3)
	{
	  h_BQuark1_BQuark3_dEta_Vs_dPhi->Fill( dEta_1_3 , dPhi_1_3 );
	  h_BQuark2_BQuark3_dEta_Vs_dPhi->Fill( dEta_2_3 , dPhi_2_3 );
	}
      
      if (bQuarks_p4.size() >= 4)
	{
	  h_BQuark1_BQuark4_dEta_Vs_dPhi->Fill( dEta_1_4 , dPhi_1_4 );
	  h_BQuark2_BQuark4_dEta_Vs_dPhi->Fill( dEta_2_4 , dPhi_2_4 );
	  h_BQuark3_BQuark4_dEta_Vs_dPhi->Fill( dEta_3_4 , dPhi_3_4 );
	}
          
      // For-Loop (Nested): All b-quarks
      for (size_t j = i+1; j < bQuarks_p4.size(); j++)
	{	  

	  double deltaR = ROOT::Math::VectorUtil::DeltaR(bQuarks_p4.at(i), bQuarks_p4.at(j));
	  
	  if (deltaR < deltaRMin)
	    {
	      deltaRMin = deltaR;
	      deltaRMin_i = i;
	      deltaRMin_j = j;
	    }	  
	}      
    } // For-loop: All b-quarks

  
  //////////////////////////////////////////////////////////////////////////////////////////////////////
  // BquarkPair - Ldg Jets Correlations
  //////////////////////////////////////////////////////////////////////////////////////////////////////
  if (deltaRMin_i>= 0  && deltaRMin_j >= 0)
    {
      math::XYZTLorentzVector bQuarkPair_dRMin_p4 = bQuarks_p4.at(deltaRMin_i) + bQuarks_p4.at(deltaRMin_j);
      double bQuarkPair_dEta = std::fabs(bQuarks_p4.at(deltaRMin_i).eta() - bQuarks_p4.at(deltaRMin_j).eta());
      double bQuarkPair_dPhi = std::fabs(ROOT::Math::VectorUtil::DeltaPhi(bQuarks_p4.at(deltaRMin_i), bQuarks_p4.at(deltaRMin_j)));

      // Fill Histos
      h_BQuarkPair_dRMin_pT   ->Fill( bQuarkPair_dRMin_p4.pt() );
      h_BQuarkPair_dRMin_dEta ->Fill( bQuarkPair_dEta );
      h_BQuarkPair_dRMin_dPhi ->Fill( bQuarkPair_dPhi );
      h_BQuarkPair_dRMin_dR   ->Fill( deltaRMin );
      h_BQuarkPair_dRMin_Mass ->Fill( bQuarkPair_dRMin_p4.mass() );
      h_BQuarkPair_dRMin_Eta1_Vs_Eta2->Fill( bQuarks_p4.at(deltaRMin_i).eta(), bQuarks_p4.at(deltaRMin_j).eta());
      h_BQuarkPair_dRMin_Phi1_Vs_Phi2->Fill( bQuarks_p4.at(deltaRMin_i).phi(), bQuarks_p4.at(deltaRMin_j).phi());
      h_BQuarkPair_dRMin_Pt1_Vs_Pt2  ->Fill(bQuarks_p4.at(deltaRMin_i).pt(), bQuarks_p4.at(deltaRMin_j).pt());
      h_BQuarkPair_dRMin_dEta_Vs_dPhi->Fill( bQuarkPair_dEta, bQuarkPair_dPhi);
 
      // Fill histos
      if (selJets_p4.size() > 0)
	{
	  h_BQuarkPair_dRMin_jet1_dEta ->Fill( std::fabs(bQuarkPair_dRMin_p4.eta() - selJets_p4.at(0).eta()) );
	  h_BQuarkPair_dRMin_jet1_dPhi ->Fill( std::fabs(ROOT::Math::VectorUtil::DeltaPhi(bQuarkPair_dRMin_p4, selJets_p4.at(0) ) ) );
	  h_BQuarkPair_dRMin_jet1_dR   ->Fill( ROOT::Math::VectorUtil::DeltaR(bQuarkPair_dRMin_p4, selJets_p4.at(0) ) );
	}
      
      if (selJets_p4.size() > 1)
	{
	  h_BQuarkPair_dRMin_jet2_dEta ->Fill( std::fabs(bQuarkPair_dRMin_p4.eta() - selJets_p4.at(1).eta()) );
	  h_BQuarkPair_dRMin_jet2_dPhi ->Fill( std::fabs(ROOT::Math::VectorUtil::DeltaPhi(bQuarkPair_dRMin_p4, selJets_p4.at(1) ) ) );
	  h_BQuarkPair_dRMin_jet2_dR   ->Fill( ROOT::Math::VectorUtil::DeltaR(bQuarkPair_dRMin_p4, selJets_p4.at(1) ) );
	}
      
    }
  
  return;
}

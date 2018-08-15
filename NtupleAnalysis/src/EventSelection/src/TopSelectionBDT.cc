// -*- c++ -*-
#include "EventSelection/interface/TopSelectionBDT.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"

#include "Tools/interface/MCTools.h"

#include "Math/VectorUtil.h"

TopSelectionBDT::Data::Data()
:
  bPassedSelection(false),
  bHasTwoTopsAndFreeB(false),
  bPassedBothMVA(false),
  bPassedLdgMVA(false),
  bPassedSubldgMVA(false),
  bHasFreeBJet(false),
  fMVAmax1(-1.0),
  fTrijet1Jet1(),
  fTrijet1Jet2(),
  fTrijet1BJet(),
  fTrijet1Dijet_p4(),
  fTrijet1_p4(), 
  fMVAmax2(-1.0),
  fTrijet2Jet1(),
  fTrijet2Jet2(),
  fTrijet2BJet(),
  fTrijet2Dijet_p4(),
  fTrijet2_p4(),
  fTetrajetBJet(),
  fLdgTetrajet_p4(),
  fSubldgTetrajet_p4(),
  fSelectedTopsJet1(),
  fSelectedTopsJet2(),
  fSelectedTopsBJet(),
  fSelectedTopsMVA(),
  fNotSelectedTopsJet1(),
  fNotSelectedTopsJet2(),
  fNotSelectedTopsBJet(),
  fNotSelectedTopsMVA(),
  fAllTopsJet1(),
  fAllTopsJet2(),
  fAllTopsBJet(),
  fAllTopsMVA(),
  fSelectedCleanedTopsJet1(),
  fSelectedCleanedTopsJet2(),
  fSelectedCleanedTopsBJet(),
  fSelectedCleanedTopsMVA(),
  fAllCleanedTopsJet1(),
  fAllCleanedTopsJet2(),
  fAllCleanedTopsBJet(),
  fAllCleanedTopsMVA(),
  fTopTaggingScaleFactorEventWeight(1.0)
{ }

TopSelectionBDT::Data::~Data() { }


TopSelectionBDT::TopSelectionBDT(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
  : BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
    // Input parameters
    cfg_AnyTopMVACut(config , "AnyTopMVACut"),
    cfg_TopMVACut(config    , "TopMVACut"),
    cfg_TopMassLowCut(config, "TopMassLowCut"),
    cfg_TopMassUppCut(config, "TopMassUppCut"),
    cfg_CSV_bDiscCut(config , "CSV_bDiscCut"),
    // Event counter for passing selection
    cPassedTopSelectionBDT(fEventCounter.addCounter("passed top selection ("+postfix+")")),
    // Sub counters
    cSubAll(fEventCounter.addSubCounter("top selection ("+postfix+")", "All events")),
    cSubPassedBjetsCut(fEventCounter.addSubCounter("top selection ("+postfix+")", "Passed b-jets cut")),
    cSubPassedLdgMVACut(fEventCounter.addSubCounter("top selection ("+postfix+")", "Passed MVA cut (ldg)")),
    cSubPassedSubldgMVACut(fEventCounter.addSubCounter("top selection ("+postfix+")", "Passed MVA cut (subldg)")),
    cSubPassedFreeBjetCut(fEventCounter.addSubCounter("top selection ("+postfix+")", "Passed free b-jet cut")),
    // Top candidates
    cTopsAll(fEventCounter.addSubCounter("top candidates ("+postfix+")", "All candidates")),
    cTopsPassTopMassLowCut(fEventCounter.addSubCounter("top candidates ("+postfix+")", "Passed top mass low cut")),
    cTopsPassTopMassUppCut(fEventCounter.addSubCounter("top candidates ("+postfix+")", "Passed top mass upp cut")),
    cTopsPassBDiscCut(fEventCounter.addSubCounter("top candidates ("+postfix+")", "Passed b-disc cut")),
    cTopsPassBDTCut(fEventCounter.addSubCounter("top candidates ("+postfix+")", "Passed BDT cut")),
    cTopsPassCrossCleanCut(fEventCounter.addSubCounter("top candidates ("+postfix+")", "Passed cross-clean cut")),
    fTopTagSFCalculator(config)
{
  initialize(config);
}

TopSelectionBDT::TopSelectionBDT(const ParameterSet& config)
: BaseSelection(),
  // Input parameters
  cfg_AnyTopMVACut(config , "AnyTopMVACut"), 
  cfg_TopMVACut(config    , "TopMVACut"),
  cfg_TopMassLowCut(config, "TopMassLowCut"),
  cfg_TopMassUppCut(config, "TopMassUppCut"),
  cfg_CSV_bDiscCut(config , "CSV_bDiscCut"),
  // Event counter for passing selection
  cPassedTopSelectionBDT(fEventCounter.addCounter("passed top selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("top selection", "All events")),
  cSubPassedBjetsCut(fEventCounter.addSubCounter("top selection", "Passed b-jets cut")),
  cSubPassedLdgMVACut(fEventCounter.addSubCounter("top selection", "Passed MVA cut (ldg)")),
  cSubPassedSubldgMVACut(fEventCounter.addSubCounter("top selection", "Passed MVA cut (subldg)")),
  cSubPassedFreeBjetCut(fEventCounter.addSubCounter("top selection", "Passed Free Bjet cut")),
  // Top candidates
  cTopsAll(fEventCounter.addSubCounter("top candidates", "All candidates")),
  cTopsPassTopMassLowCut(fEventCounter.addSubCounter("top candidates", "Passed top mass low cut")),
  cTopsPassTopMassUppCut(fEventCounter.addSubCounter("top candidates", "Passed top mass upp cut")),
  cTopsPassBDiscCut(fEventCounter.addSubCounter("top candidates", "Passed b-disc cut")),
  cTopsPassBDTCut(fEventCounter.addSubCounter("top candidates", "Passed BDT cut")),
  cTopsPassCrossCleanCut(fEventCounter.addSubCounter("top candidates", "Passed cross-clean cut")),
  fTopTagSFCalculator(config)
{
  initialize(config);
  bookHistograms(new TDirectory());

}

TopSelectionBDT::~TopSelectionBDT() {
  
  // Histograms
  delete hTopMultiplicity_AllCandidates;
  delete hTopBDT_AllCandidates;
  delete hTopMass_AllCandidates;
  delete hTopPt_AllCandidates;

  delete hTopBDT_SelectedCandidates;
  delete hTopMass_SelectedCandidates;
  delete hTopPt_SelectedCandidates;
  delete hTopMultiplicity_SelectedCandidates;
  delete hTopBDT_SelectedCleanedCandidates;
  delete hTopMass_SelectedCleanedCandidates;
  delete hTopPt_SelectedCleanedCandidates;
  delete hTopMultiplicity_SelectedCleanedCandidates;

  delete hTopBDT_NotSelectedCandidates;
  delete hTopMass_NotSelectedCandidates;
  delete hTopPt_NotSelectedCandidates;
  delete hTopMultiplicity_NotSelectedCandidates;
  delete hTopBDT_AllCleanedCandidates;
  delete hTopMass_AllCleanedCandidates;
  delete hTopPt_AllCleanedCandidates;
  delete hTopMultiplicity_AllCleanedCandidates;

  // Ldg in pt free b-jet
  delete hTetrajetBJetPt;
  delete hTetrajetBJetEta;
  delete hTetrajetBJetBDisc;

  // Tetrajet
  delete hTetrajetPt;
  delete hTetrajetMass;
  delete hTetrajetEta;

  // Leading in pt top
  delete hLdgTrijetPt;
  delete hLdgTrijetMass;
  delete hLdgTrijetJet1Pt;
  delete hLdgTrijetJet1Eta;
  delete hLdgTrijetJet1BDisc;
  delete hLdgTrijetJet2Pt;
  delete hLdgTrijetJet2Eta;
  delete hLdgTrijetJet2BDisc;
  delete hLdgTrijetBJetPt;
  delete hLdgTrijetBJetEta;
  delete hLdgTrijetBJetBDisc;
  delete hLdgTrijetDiJetPt;
  delete hLdgTrijetDiJetEta;
  delete hLdgTrijetDiJetMass;
  delete hLdgTrijetDijetDeltaR;
  delete hLdgTrijetTopMassWMassRatio;
  delete hLdgTrijet_DeltaR_Trijet_TetrajetBjet;
  delete hLdgTrijet_DeltaEta_Trijet_TetrajetBjet;
  delete hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet;
  delete hLdgTrijet_DeltaY_Trijet_TetrajetBjet;
  
  // Sub-Leading in pt top
  delete hSubldgTrijetPt;
  delete hSubldgTrijetMass;
  delete hSubldgTrijetJet1Pt;
  delete hSubldgTrijetJet1Eta;
  delete hSubldgTrijetJet1BDisc;
  delete hSubldgTrijetJet2Pt;
  delete hSubldgTrijetJet2Eta;
  delete hSubldgTrijetJet2BDisc;
  delete hSubldgTrijetBJetPt;
  delete hSubldgTrijetBJetEta;
  delete hSubldgTrijetBJetBDisc;
  delete hSubldgTrijetDiJetPt;
  delete hSubldgTrijetDiJetEta;
  delete hSubldgTrijetDiJetMass;
  delete hSubldgTrijetDijetDeltaR;
  delete hSubldgTrijetTopMassWMassRatio;
  delete hSubldgTrijet_DeltaR_Trijet_TetrajetBjet;
  delete hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet;
  delete hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet;
  delete hSubldgTrijet_DeltaY_Trijet_TetrajetBjet;

  // Histograms (2D)
  delete hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet;
  delete hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet;
  delete hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet;
  delete hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet;

  // TMVA reader
  delete reader;
  
}

void TopSelectionBDT::initialize(const ParameterSet& config) {
  
  // Load TMVA library
  TMVA::Tools::Instance();
    
  // Create the reader
  reader = new TMVA::Reader( "!Color:Silent" );
  
  // Add variables
  reader->AddVariable( "TrijetPtDR",              &TrijetPtDR              );
  reader->AddVariable( "TrijetDijetPtDR",         &TrijetDijetPtDR         );
  reader->AddVariable( "TrijetBjetMass",          &TrijetBjetMass          );
  reader->AddVariable( "TrijetLdgJetBDisc",       &TrijetLdgJetBDisc       );
  reader->AddVariable( "TrijetSubldgJetBDisc",    &TrijetSubldgJetBDisc    );
  reader->AddVariable( "TrijetBJetLdgJetMass",    &TrijetBJetLdgJetMass    );
  reader->AddVariable( "TrijetBJetSubldgJetMass", &TrijetBJetSubldgJetMass );
  reader->AddVariable( "TrijetMass",              &TrijetMass              );
  reader->AddVariable( "TrijetDijetMass",         &TrijetDijetMass         );
  reader->AddVariable( "TrijetBJetBDisc",         &TrijetBJetBDisc         );
  reader->AddVariable( "TrijetSoftDrop_n2",       &TrijetSoftDrop_n2       );
  reader->AddVariable( "TrijetLdgJetCvsL",        &TrijetLdgJetCvsL        );
  reader->AddVariable( "TrijetSubldgJetCvsL",     &TrijetSubldgJetCvsL     );
  reader->AddVariable( "TrijetLdgJetPtD",         &TrijetLdgJetPtD         );
  reader->AddVariable( "TrijetSubldgJetPtD",      &TrijetSubldgJetPtD      );
  reader->AddVariable( "TrijetLdgJetAxis2",       &TrijetLdgJetAxis2       );
  reader->AddVariable( "TrijetSubldgJetAxis2",    &TrijetSubldgJetAxis2    );
  reader->AddVariable( "TrijetLdgJetMult",        &TrijetLdgJetMult        );
  reader->AddVariable( "TrijetSubldgJetMult",     &TrijetSubldgJetMult     );

  // Construct the relative path toe the xml file with the BDT weights
  std::string relPath  = "../../../data/TopTaggerWeights/";
  std::string fileName = config.getParameter<std::string>("WeightFile");
  std::string fullPath = relPath + fileName;
  // std::cout << "Opening BDT weight file " << fullPath << std::endl;
  reader->BookMVA("BTDG method", fullPath);

  return;
}

void TopSelectionBDT::bookHistograms(TDirectory* dir) {

  // Fixed binning  
  const int nPtBins   = 2 * fCommonPlots->getPtBinSettings().bins();
  const double fPtMin = 2 * fCommonPlots->getPtBinSettings().min();
  const double fPtMax = 2 * fCommonPlots->getPtBinSettings().max();

  const int  nEtaBins = fCommonPlots->getEtaBinSettings().bins();
  const float fEtaMin = fCommonPlots->getEtaBinSettings().min();
  const float fEtaMax = fCommonPlots->getEtaBinSettings().max();

  const int nDEtaBins   = fCommonPlots->getDeltaEtaBinSettings().bins();
  const double fDEtaMin = fCommonPlots->getDeltaEtaBinSettings().min();
  const double fDEtaMax = fCommonPlots->getDeltaEtaBinSettings().max();
  
  const int nDPhiBins   = fCommonPlots->getDeltaPhiBinSettings().bins();
  const double fDPhiMin = fCommonPlots->getDeltaPhiBinSettings().min();
  const double fDPhiMax = fCommonPlots->getDeltaPhiBinSettings().max();
  
  const int nDRBins   = fCommonPlots->getDeltaRBinSettings().bins();
  const double fDRMin = fCommonPlots->getDeltaRBinSettings().min();
  const double fDRMax = fCommonPlots->getDeltaRBinSettings().max();

  const int  nBDiscBins = fCommonPlots->getBJetDiscBinSettings().bins();
  const float fBDiscMin = fCommonPlots->getBJetDiscBinSettings().min();
  const float fBDiscMax = fCommonPlots->getBJetDiscBinSettings().max();

  const int nWMassBins  = fCommonPlots->getWMassBinSettings().bins();
  const float fWMassMin = fCommonPlots->getWMassBinSettings().min();
  const float fWMassMax = fCommonPlots->getWMassBinSettings().max();

  const int nTopMassBins  = fCommonPlots->getTopMassBinSettings().bins();
  const float fTopMassMin = fCommonPlots->getTopMassBinSettings().min();
  const float fTopMassMax = fCommonPlots->getTopMassBinSettings().max();

  const int nInvMassBins  = fCommonPlots->getInvMassBinSettings().bins();
  const float fInvMassMin = fCommonPlots->getInvMassBinSettings().min();
  const float fInvMassMax = fCommonPlots->getInvMassBinSettings().max();
  
  // Histograms
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kVital, dir, "topSelectionBDT_"    + sPostfix);

  // All Candidates
  hTopBDT_AllCandidates           = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopBDT_AllCandidates",";top candidate BDT", 40, -1.0, 1.0) ; 
  hTopMass_AllCandidates          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopMass_AllCandidates" ,";top candidate M (GeVc^{-2})", nTopMassBins, fTopMassMin, fTopMassMax);
  hTopPt_AllCandidates            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopPt_AllCandidates", ";top candidate p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTopMultiplicity_AllCandidates  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopMultiplicity_AllCandidates", ";top candidate multiplicity", 400, 0.0, 400.0);

  hTopBDT_SelectedCandidates           = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopBDT_SelectedCandidates",";top candidate BDT", 40, -1.0, 1.0) ; 
  hTopMass_SelectedCandidates          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopMass_SelectedCandidates" ,";top candidate M (GeVc^{-2})", nTopMassBins, fTopMassMin, fTopMassMax);
  hTopPt_SelectedCandidates            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopPt_SelectedCandidates", ";top candidate p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTopMultiplicity_SelectedCandidates  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopMultiplicity_SelectedCandidates", ";top candidate multiplicity", 50, 0.0, 50.0);
  hTopBDT_SelectedCleanedCandidates           = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopBDT_SelectedCleanedCandidates",";top candidate BDT", 40, -1.0, 1.0) ; 
  hTopMass_SelectedCleanedCandidates          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopMass_SelectedCleanedCandidates" ,";top candidate M (GeVc^{-2})", nTopMassBins, fTopMassMin, fTopMassMax);
  hTopPt_SelectedCleanedCandidates            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopPt_SelectedCleanedCandidates", ";top candidate p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTopMultiplicity_SelectedCleanedCandidates  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopMultiplicity_SelectedCleanedCandidates", ";top candidate multiplicity", 10, 0.0, 10.0);

  hTopBDT_NotSelectedCandidates           = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopBDT_NotSelectedCandidates",";top candidate BDT", 40, -1.0, 1.0) ; 
  hTopMass_NotSelectedCandidates          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopMass_NotSelectedCandidates" ,";top candidate M (GeVc^{-2})", nTopMassBins, fTopMassMin, fTopMassMax);
  hTopPt_NotSelectedCandidates            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopPt_NotSelectedCandidates", ";top candidate p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTopMultiplicity_NotSelectedCandidates  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopMultiplicity_NotSelectedCandidates", ";top candidate multiplicity", 50, 0.0, 50.0);
  hTopBDT_AllCleanedCandidates           = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopBDT_AllCleanedCandidates",";top candidate BDT", 40, -1.0, 1.0) ; 
  hTopMass_AllCleanedCandidates          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopMass_AllCleanedCandidates" ,";top candidate M (GeVc^{-2})", nTopMassBins, fTopMassMin, fTopMassMax);
  hTopPt_AllCleanedCandidates            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopPt_AllCleanedCandidates", ";top candidate p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTopMultiplicity_AllCleanedCandidates  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopMultiplicity_AllCleanedCandidates", ";top candidate multiplicity", 10, 0.0, 10.0);

  // Ldg in pt free b-jet
  hTetrajetBJetPt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetPt"   ,";p_{T} (GeV/c)"      , nPtBins     , fPtMin     , fPtMax);
  hTetrajetBJetEta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetEta"  ,";#eta"               , nEtaBins    , fEtaMin    , fEtaMax);
  hTetrajetBJetBDisc  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetBDisc",";b-tag discriminator", nBDiscBins  , fBDiscMin  , fBDiscMax);

  // Tetrajet
  hTetrajetPt         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetPt"  , ";p_{T} (GeV/c)"     , nPtBins     , fPtMin     , fPtMax);
  hTetrajetMass       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetMass", ";M (GeV/c^{2})"     , nInvMassBins, fInvMassMin, fInvMassMax);
  hTetrajetEta        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetEta" , ";#eta"              , nEtaBins    , fEtaMin    , fEtaMax);

  // Leading in pt top
  hLdgTrijetPt          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetPt"       ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hLdgTrijetMass        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetMass"     ,";M (GeV/c^{2})", nTopMassBins, fTopMassMin, fTopMassMax);
  hLdgTrijetJet1Pt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet1Pt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hLdgTrijetJet1Eta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet1Eta"  ,";#eta"         , nEtaBins    , fEtaMin    , fEtaMax);
  hLdgTrijetJet1BDisc   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet1BDisc",";b-tag discr." , nBDiscBins  , fBDiscMin  , fBDiscMax);
  hLdgTrijetJet2Pt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet2Pt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hLdgTrijetJet2Eta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet2Eta"  ,";#eta"         , nEtaBins    , fEtaMin    , fEtaMax);
  hLdgTrijetJet2BDisc   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet2BDisc",";b-tag discr." , nBDiscBins  , fBDiscMin  , fBDiscMax);
  hLdgTrijetBJetPt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetBJetPt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hLdgTrijetBJetEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetBJetEta"  ,";#eta"         , nEtaBins    , fEtaMin    , fEtaMax);
  hLdgTrijetBJetBDisc   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetBJetBDisc",";b-tag discr." , nBDiscBins  , fBDiscMin  , fBDiscMax);
  hLdgTrijetDiJetPt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetDiJetPt"  ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hLdgTrijetDiJetEta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetDiJetEta" ,";#eta"         , nEtaBins    , fEtaMin    , fEtaMax);
  hLdgTrijetDiJetMass   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetDiJetMass",";M (GeV/c^{2})", nWMassBins  , fWMassMin  , fWMassMax);
  hLdgTrijetDijetDeltaR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetDijetDR"  , ";#Delta R(j_{1},j_{2})"  , 2*nDRBins     , fDRMin     , fDRMax);
  hLdgTrijetTopMassWMassRatio    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetTopMassWMassRatio"   ,";R_{32}", 100 , 0.0, 10.0);
  hLdgTrijet_DeltaR_Trijet_TetrajetBjet   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijet_DeltaR_Trijet_TetrajetBjet" , ";#Delta R(top, b_{free})" , nDRBins, fDRMin, fDRMax);
  hLdgTrijet_DeltaEta_Trijet_TetrajetBjet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijet_DeltaEta_Trijet_TetrajetBjet", ";#Delta#eta(top, b_{free})", nDEtaBins, fDEtaMin, fDEtaMax);
  hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijet_DeltaPhi_Trijet_TetrajetBjet", ";#Delta#phi(top, b_{free})", nDPhiBins, fDPhiMin, fDPhiMax);
  hLdgTrijet_DeltaY_Trijet_TetrajetBjet   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijet_DeltaY_Trijet_TetrajetBjet", ";#Delta Y(top, b_{free})", nDRBins, fDRMin, fDRMax);

  // Sub-Leading in pt top
  hSubldgTrijetPt          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetPt"       ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hSubldgTrijetMass        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetMass"     ,";M (GeV/c^{2})", nTopMassBins, fTopMassMin, fTopMassMax);
  hSubldgTrijetJet1Pt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet1Pt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hSubldgTrijetJet1Eta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet1Eta"  ,";#eta"         , nEtaBins    , fEtaMin    , fEtaMax);
  hSubldgTrijetJet1BDisc   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet1BDisc",";b-tag discr." , nBDiscBins  , fBDiscMin  , fBDiscMax);
  hSubldgTrijetJet2Pt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet2Pt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hSubldgTrijetJet2Eta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet2Eta"  ,";#eta"         , nEtaBins    , fEtaMin    , fEtaMax);
  hSubldgTrijetJet2BDisc   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet2BDisc",";b-tag discr." , nBDiscBins  , fBDiscMin  , fBDiscMax);
  hSubldgTrijetBJetPt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetBJetPt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hSubldgTrijetBJetEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetBJetEta"  ,";#eta"         , nEtaBins    , fEtaMin    , fEtaMax);
  hSubldgTrijetBJetBDisc   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetBJetBDisc",";b-tag discr." , nBDiscBins  , fBDiscMin  , fBDiscMax);
  hSubldgTrijetDiJetPt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetDiJetPt"  ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hSubldgTrijetDiJetEta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetDiJetEta" ,";#eta"         , nEtaBins    , fEtaMin    , fEtaMax);
  hSubldgTrijetDiJetMass   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetDiJetMass",";M (GeV/c^{2})", nWMassBins  , fWMassMin  , fWMassMax);
  hSubldgTrijetDijetDeltaR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SbldgTrijetDijetDR"  , ";#Delta R(j_{1},j_{2})"  , nDRBins     , fDRMin     , fDRMax);
  hSubldgTrijetTopMassWMassRatio = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetTopMassWMassRatio",";R_{32}", 100 , 0.0, 10.0);
  hSubldgTrijet_DeltaR_Trijet_TetrajetBjet   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijet_DeltaR_Trijet_TetrajetBjet", ";#Delta R(top, b_{free})", nDRBins, fDRMin, fDRMax);
  hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijet_DeltaEta_Trijet_TetrajetBjet", ";#Delta#eta(top, b_{free})", nDEtaBins, fDEtaMin, fDEtaMax);
  hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijet_DeltaPhi_Trijet_TetrajetBjet", ";#Delta#phi(top, b_{free})", nDPhiBins, fDPhiMin, fDPhiMax);
  hSubldgTrijet_DeltaY_Trijet_TetrajetBjet   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijet_DeltaY_Trijet_TetrajetBjet", ";#Delta Y(top, b_{free})", nDRBins, fDRMin, fDRMax);

  // Histograms (2D) 
  hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet   = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "DeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet", 
											     ";#Delta R (Trijet_{Ldg}, b_{free}^{ldg});#Delta R (Trijet_{Sbldg}, b_{free}^{ldg})", 
											     nDRBins     , fDRMin     , 6., nDRBins     , fDRMin     , 6.);
  hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "DeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet", 
											     ";#Delta #eta (Trijet_{Ldg}, b_{free}^{ldg}) ;#Delta #eta (Trijet_{Sbldg}, b_{free}^{ldg})", 
											     nDEtaBins, fDEtaMin, 6., nDEtaBins, fDEtaMin, 6.);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet", 
											     ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});#Delta #phi (Trijet_{Sbldg}, b_{free}^{ldg})", 
											     nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet   = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "DeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet",
											     ";#Delta Y (Trijet_{Ldg}, b_{free}^{ldg});#Delta Y (Trijet_{Sbldg}, b_{free}^{ldg})", 
											     nDRBins     , fDRMin     , 6., nDRBins     , fDRMin     , 6.);

  fTopTagSFCalculator.bookHistograms(subdir, fHistoWrapper); 
  return;
}

TopSelectionBDT::Data TopSelectionBDT::silentAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  ensureSilentAnalyzeAllowed(event.eventID());

  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, jetData.getSelectedJets(), bjetData.getSelectedBJets());
  enableHistogramsAndCounters();
  return myData;
}

TopSelectionBDT::Data TopSelectionBDT::analyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  ensureAnalyzeAllowed(event.eventID());

  // Ready to analyze
  TopSelectionBDT::Data data = privateAnalyze(event, jetData.getSelectedJets(), bjetData.getSelectedBJets());

  // Send data to CommonPlots
  // if (fCommonPlots != nullptr) fCommonPlots->fillControlPlotsAtTopSelectionBDT(event, data);
  return data;
}

TopSelectionBDT::Data TopSelectionBDT::privateAnalyze(const Event& event, const std::vector<Jet> selectedJets, const std::vector<Jet> selectedBjets) {
  Data output;
  cSubAll.increment();

  // Initialise variables
  output.fJetsUsedAsBJets = selectedBjets;
  
  // Sanity check
  //if (selectedBjets.size() < 3) return output;
  cSubPassedBjetsCut.increment();

  // Only resize if their size exceeds max allowed value
  std::vector<Jet> jets  = selectedJets;
  std::vector<Jet> bjets = selectedBjets;
  
  //================================================================================================  
  // Top Candidates
  //================================================================================================  
  if (0) std::cout << "=== TopSelectionBDT:: Obtaining all top candidates" << std::endl;
  TrijetSelection fAllTops;
  TrijetSelection fSelectedTops;
  TrijetSelection fSelectedCleanedTops;
  TrijetSelection fNotSelectedTops;
  TrijetSelection fAllCleanedTops;

  // For-loop: All b-jets
  // mafor (auto& bjet: jets) // OldTop (Between ~March-June 2018)
  for (auto& bjet: bjets) // NewTop (Testing since 01/06/2018)
    {
      int index1 = 0;

      // For-loop: All jets
      for (auto& jet1: jets)
	{
	  index1++;
	  int index2 = 0;

	  // Skip if jet1 is same as bjet
	  if (areSameJets(jet1, bjet)) continue;

	  // For-loop: All jets
	  for (auto& jet2: jets)
	    {
	      index2++;

	      // Do not consider duplicate compinations
	      if (index2 < index1) continue;

	      // Skip if jet2 is same as jet1, or jet2 same as bjet
	      if (areSameJets(jet2,  jet1) || areSameJets(jet2,  bjet)) continue;
	     
	      // Increment top candidate counter
	      cTopsAll.increment();

	      // Get 4-momentum of top (trijet) and W (dijet)
	      math::XYZTLorentzVector top_p4, w_p4;
	      top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
	      w_p4   = jet1.p4() + jet2.p4();
	      
	      // Skip trijet combinations which do not fulfil the top invariant mass (lower threshold)
	      if (!cfg_TopMassLowCut.passedCut(top_p4.M())) continue;
	      cTopsPassTopMassLowCut.increment();

	      // Skip trijet combinations which do not fulfil the top invariant mass (upper threshold)
	      if (!cfg_TopMassUppCut.passedCut(top_p4.M())) continue;
	      cTopsPassTopMassUppCut.increment();

	      // Skip trijet combinations which do not fulfil bjet_CSV threshold
	      if (!cfg_CSV_bDiscCut.passedCut(bjet.bjetDiscriminator())) continue;
	      cTopsPassBDiscCut.increment();

	      // Calculate variables
	      double dr_sd = ROOT::Math::VectorUtil::DeltaR( jet1.p4(), jet2.p4());
	      double softDrop_n2 = min(jet2.pt(), jet1.pt()) / ( (jet2.pt() + jet1.pt()) * dr_sd * dr_sd);

	      // Calculate our BDT discriminating variables for MVA use
	      TrijetPtDR              = top_p4.Pt() * ROOT::Math::VectorUtil::DeltaR( w_p4  , bjet.p4() );
	      TrijetDijetPtDR         = w_p4.Pt() * ROOT::Math::VectorUtil::DeltaR( jet1.p4() , jet2.p4() );
	      TrijetBjetMass          = bjet.p4().M();
	      TrijetLdgJetBDisc       = jet1.bjetDiscriminator();
	      TrijetSubldgJetBDisc    = jet2.bjetDiscriminator();
	      TrijetBJetLdgJetMass    = (bjet.p4() + jet1.p4()).M();
	      TrijetBJetSubldgJetMass = (bjet.p4() + jet2.p4()).M();
	      TrijetMass              = top_p4.M();
	      TrijetDijetMass         = w_p4.M();
	      TrijetBJetBDisc         = bjet.bjetDiscriminator();
	      TrijetSoftDrop_n2       = softDrop_n2;
	      TrijetLdgJetCvsL        = jet1.pfCombinedCvsLJetTags();
	      TrijetSubldgJetCvsL     = jet2.pfCombinedCvsLJetTags();
	      TrijetLdgJetPtD         = jet1.QGTaggerAK4PFCHSptD();
	      TrijetSubldgJetPtD      = jet2.QGTaggerAK4PFCHSptD();
	      TrijetLdgJetAxis2       = jet1.QGTaggerAK4PFCHSaxis2();
	      TrijetSubldgJetAxis2    = jet2.QGTaggerAK4PFCHSaxis2();
	      TrijetLdgJetMult        = jet1.QGTaggerAK4PFCHSmult();
	      TrijetSubldgJetMult     = jet2.QGTaggerAK4PFCHSmult();

	      // Evaluate the MVA discriminator value
	      float MVAoutput = reader->EvaluateMVA("BTDG method");
	      // std::cout << "MVA = " << MVAoutput << ", Pt = " << top_p4.pt() << ", M = " << TrijetMass << std::endl;

	      // Fill top candidate BDT values
	      hTopBDT_AllCandidates -> Fill(MVAoutput);
	      hTopMass_AllCandidates-> Fill(top_p4.M());
	      hTopPt_AllCandidates  -> Fill(top_p4.pt());

	      // Save top candidates
	      fAllTops.MVA.push_back(MVAoutput);
	      fAllTops.TrijetP4.push_back(top_p4);
	      fAllTops.DijetP4.push_back(w_p4);
	      fAllTops.Jet1.push_back(getLeadingSubleadingJet(jet1, jet2, "leading"));
	      fAllTops.Jet2.push_back(getLeadingSubleadingJet(jet1, jet2, "subleading"));
	      fAllTops.BJet.push_back(bjet);
	      fAllTops.isGenuine.push_back(false);
	      fAllTops.isTagged.push_back(cfg_TopMVACut.passedCut(MVAoutput));

	      // Get top candidates above MVA cut
	      if (cfg_TopMVACut.passedCut(MVAoutput))
		{
		  cTopsPassBDTCut.increment();
		  fSelectedTops.MVA.push_back(MVAoutput);
		  fSelectedTops.TrijetP4.push_back(top_p4);
		  fSelectedTops.DijetP4.push_back(w_p4);
		  fSelectedTops.Jet1.push_back(getLeadingSubleadingJet(jet1, jet2, "leading"));
		  fSelectedTops.Jet2.push_back(getLeadingSubleadingJet(jet1, jet2, "subleading"));
		  fSelectedTops.BJet.push_back(bjet);
		  fSelectedTops.isGenuine.push_back(false);
		  fSelectedTops.isTagged.push_back(true);  // fixme: which MVA cut? ldg, or subldg, or?
		}
	      else
		{
		  // Get top candidates failing MVA cut
		  fNotSelectedTops.MVA.push_back(MVAoutput);
		  fNotSelectedTops.TrijetP4.push_back(top_p4);
		  fNotSelectedTops.DijetP4.push_back(w_p4);
		  fNotSelectedTops.Jet1.push_back(getLeadingSubleadingJet(jet1, jet2, "leading"));
		  fNotSelectedTops.Jet2.push_back(getLeadingSubleadingJet(jet1, jet2, "subleading"));
		  fNotSelectedTops.BJet.push_back(bjet);
		  fNotSelectedTops.isGenuine.push_back(false); // fixme
		  fNotSelectedTops.isTagged.push_back(false); // fixme: which MVA cut? ldg, or subldg, or?
		}
		
	    }// For-loop: All jets
	}// For-loop: All jets
    }// For-loop: All b-jets
  hTopMultiplicity_AllCandidates->Fill(fAllTops.MVA.size());

  //================================================================================================  
  // Sort top candidates in descending MVA values
  //================================================================================================    
  if (0) std::cout << "=== TopSelectionBDT::Sort top candidates in MVA" << std::endl;
  fAllTops         = SortInMVAvalue(fAllTops);
  fSelectedTops    = SortInMVAvalue(fSelectedTops);
  fNotSelectedTops = SortInMVAvalue(fNotSelectedTops);
  
  //Debug: Check cleaned top candidates
  bool printCleanedTops = false;

  if (printCleanedTops)
    {
      std::cout << "\n" << std::endl;
      std::cout<<"Entry: "<<cSubAll.value()<<std::endl;
      std::cout << std::string(10*10, '=') << std::endl;
      std::cout << std::setw(12) << "Jet1 indx "  << std::setw(12) << "Jet2 indx"<< std::setw(12) << "Bjet indx"   << std::setw(12) << "BDT"   << std::setw(12) << "is cleaned"  << std::endl;
      std::cout << std::string(10*10, '=') << std::endl;
    }

  // For-loop: All (MVA sorted) selected tops
  for (size_t i = 0; i < fSelectedTops.MVA.size(); i++)
    {
      // Fill Histos (selected candidates)
      hTopBDT_SelectedCandidates -> Fill(fSelectedTops.MVA.at(i) );
      hTopMass_SelectedCandidates-> Fill(fSelectedTops.TrijetP4.at(i).M());
      hTopPt_SelectedCandidates  -> Fill(fSelectedTops.TrijetP4.at(i).pt());
      
      // Is this top cross-cleaned (b-jet availability check, object sharing with higher BDT value)
      bool isCrossCleaned = TopIsCrossCleaned(i, fSelectedTops, bjets);

      if (printCleanedTops)
	{
	  std::cout << std::setw(12) << fSelectedTops.Jet1.at(i).index() << std::setw(12) << fSelectedTops.Jet2.at(i).index() << std::setw(12) << fSelectedTops.BJet.at(i).index() << std::setw(12) << fSelectedTops.MVA.at(i) << std::setw(12) << isCrossCleaned <<  std::endl;
      
      }
      if (!isCrossCleaned) continue;
      cTopsPassCrossCleanCut.increment();

      // Save the top selected && cross-cleaned top candidate (sorted in MVA)
      fSelectedCleanedTops.Jet1.push_back( fSelectedTops.Jet1.at(i) );
      fSelectedCleanedTops.Jet2.push_back( fSelectedTops.Jet2.at(i) );
      fSelectedCleanedTops.BJet.push_back( fSelectedTops.BJet.at(i) );
      fSelectedCleanedTops.MVA.push_back( fSelectedTops.MVA.at(i) );
      fSelectedCleanedTops.TrijetP4.push_back( fSelectedTops.TrijetP4.at(i) );
      fSelectedCleanedTops.DijetP4.push_back( fSelectedTops.DijetP4.at(i) );
      fSelectedCleanedTops.isGenuine.push_back( fSelectedTops.isGenuine.at(i) ); // fixme: always false, overwite later.
      fSelectedCleanedTops.isTagged.push_back( fSelectedTops.isTagged.at(i) );   // fixme: which MVA cut? ldg, or subldg, or?

      // Fill Histos (selected, cross-cleaned candidates)
      hTopBDT_SelectedCleanedCandidates -> Fill(fSelectedTops.MVA.at(i) );
      hTopMass_SelectedCleanedCandidates-> Fill(fSelectedTops.TrijetP4.at(i).M());
      hTopPt_SelectedCleanedCandidates  -> Fill(fSelectedTops.TrijetP4.at(i).pt());
    }

  // For-loop: All candidates
  for (size_t i = 0; i < fAllTops.MVA.size(); i++)
    {      
      // Is this top cross-cleaned (b-jet availability check, object sharing with higher BDT value)
      bool isCrossCleaned = TopIsCrossCleaned(i, fAllTops, bjets);
      printCleanedTops = false;
      
      if (printCleanedTops){
	if (i==0){
	  std::cout << "\n" << std::endl;
	  std::cout<<"Entry: "<<cSubAll.value()<<std::endl;
	  std::cout << std::string(10*10, '=') << std::endl;
	  std::cout << std::setw(12) << "Jet1 indx "  << std::setw(12) << "Jet2 indx"<< std::setw(12) << "Bjet indx"   << std::setw(12) << "BDT"   << std::setw(12) << "is cleaned"  << std::endl;
	  std::cout << std::string(10*10, '=') << std::endl;	
	}
	std::cout << std::setw(12) << fAllTops.Jet1.at(i).index()      << std::setw(12)   << fAllTops.Jet2.at(i).index()   << std::setw(12)   << fAllTops.BJet.at(i).index()
		  << std::setw(12) << fAllTops.MVA.at(i)               << std::setw(12)   << isCrossCleaned
		  <<  std::endl;
	
      }
      if (!isCrossCleaned) continue;

      // Save the top selected && cross-cleaned top candidate
      fAllCleanedTops.Jet1.push_back( fAllTops.Jet1.at(i) );
      fAllCleanedTops.Jet2.push_back( fAllTops.Jet2.at(i) );
      fAllCleanedTops.BJet.push_back( fAllTops.BJet.at(i) );
      fAllCleanedTops.MVA.push_back( fAllTops.MVA.at(i) );
      fAllCleanedTops.TrijetP4.push_back( fAllTops.TrijetP4.at(i) );
      fAllCleanedTops.DijetP4.push_back( fAllTops.DijetP4.at(i) );
      fAllCleanedTops.isGenuine.push_back( fAllTops.isGenuine.at(i) ); // fixme: always false, overwite later.
      fAllCleanedTops.isTagged.push_back( fAllTops.isTagged.at(i) );   // fixme: which MVA cut? ldg, or subldg, or?

      // Fill Histos (selected, cross-cleaned candidates)
      hTopBDT_AllCleanedCandidates -> Fill(fAllTops.MVA.at(i) );
      hTopMass_AllCleanedCandidates-> Fill(fAllTops.TrijetP4.at(i).M());
      hTopPt_AllCleanedCandidates  -> Fill(fAllTops.TrijetP4.at(i).pt());
    }


  // For-loop: Failed candidates
  for (size_t i = 0; i < fNotSelectedTops.MVA.size(); i++)
    {
      // Fill Histos (selected candidates)
      hTopBDT_NotSelectedCandidates -> Fill(fNotSelectedTops.MVA.at(i) );
      hTopMass_NotSelectedCandidates-> Fill(fNotSelectedTops.TrijetP4.at(i).M());
      hTopPt_NotSelectedCandidates  -> Fill(fNotSelectedTops.TrijetP4.at(i).pt());
    }

  // Fill multiplicities
  hTopMultiplicity_SelectedCandidates->Fill(fSelectedTops.MVA.size());
  hTopMultiplicity_SelectedCleanedCandidates->Fill(fSelectedCleanedTops.MVA.size());
  hTopMultiplicity_NotSelectedCandidates->Fill(fNotSelectedTops.MVA.size());
  hTopMultiplicity_AllCleanedCandidates->Fill(fAllCleanedTops.MVA.size());

  //================================================================================================  
  // Determine the ldg-in-pt free b-jet (tetrajet b-jet)
  //================================================================================================  
  if (0) std::cout << "=== TopSelectionBDT:: Find the tetrajet b-jet" << std::endl;
  Jet tetrajetBjet;
  double tetrajetBjetPt_max = -999.99;
  math::XYZTLorentzVector ldgTetrajet_P4;
  math::XYZTLorentzVector subLdgTetrajet_P4;
  // SelectedTrijets top_ldgInPt    = getLdgOrSubldgTop(fSelectedCleanedTops, "leading");
  // SelectedTrijets top_subLdgInPt = getLdgOrSubldgTop(fSelectedCleanedTops, "subleading");
  SelectedTrijets top_ldgInPt    = getLdgOrSubldgTop(fAllCleanedTops, "leading");
  SelectedTrijets top_subLdgInPt = getLdgOrSubldgTop(fAllCleanedTops, "subleading");

  if (0) std::cout << "=== TopSelectionBDT:: Tetrajet bjet loop" << std::endl;
  // For-loop: All selected b-jets
  for (auto& bjet: bjets)
    {
      // Skip if tetrajet bjet pT is greater that this pt
      if (tetrajetBjetPt_max > bjet.pt()) continue;

      // Check if this bjet is matched with one of the jets assigned to the best TWO tops
      if (isMatchedJet(bjet, fAllCleanedTops, 0) || isMatchedJet(bjet, fAllCleanedTops, 1)) continue;

      // Save variables
      tetrajetBjetPt_max = bjet.pt();
      tetrajetBjet       = bjet;
    }
  if (tetrajetBjetPt_max > 0)
    {
      ldgTetrajet_P4    = top_ldgInPt.TrijetP4    + tetrajetBjet.p4();
      subLdgTetrajet_P4 = top_subLdgInPt.TrijetP4 + tetrajetBjet.p4();
    }


  //================================================================================================
  // Find top decay products
  //================================================================================================
  std::vector<genParticle> GenTops, GenTops_BQuark, GenTops_SubldgQuark, GenTops_LdgQuark;
  std::vector <Jet>        MCtrue_LdgJet, MCtrue_SubldgJet, MCtrue_Bjet, MC_BJets;
  std::vector <double>     dRminB;
  const double twoSigmaDpt = 0.32, dRcut = 0.4;

  if (event.isMC())
    {
    GenTops = GetGenParticles(event.genparticles().getGenParticles(), 6);
    }
  
  // For-loop: All top quarks
  for (auto& top: GenTops){
    std::vector<genParticle> quarks, bquark;
    // For-loop: Top quark daughters (Nested)
    for (size_t i=0; i<top.daughters().size(); i++)
      {
        genParticle dau = event.genparticles().getGenParticles()[top.daughters().at(i)];
        // B-Quark, W-Boson
        if (std::abs(dau.pdgId()) ==  5) bquark.push_back(dau);
	if (std::abs(dau.pdgId()) == 24) quarks = GetWpartons(dau, event);
      }//Top-quark daughters

    // Skip top if b-quark is not found (i.e. top decays to W and c)
    if (bquark.size() < 1) continue;
    // Skip top if at least one W decays leptonically
    if (quarks.size() < 2) continue;

    // Fill vectors for b-quarks, leading and subleading quarks coming from tops
    GenTops_BQuark.push_back(bquark.at(0));
    GenTops_LdgQuark.push_back(getLeadingSubleadingParton(quarks.at(0),    quarks.at(1), "leading"));
    GenTops_SubldgQuark.push_back(getLeadingSubleadingParton(quarks.at(0), quarks.at(1), "subleading"));
  }
  
  // Skip matcing if top does not decay to b
  bool doMatching = (GenTops_BQuark.size() == GenTops.size());	    

  //================================================================================================
  // Find truth-matched top candidates
  //================================================================================================
  if (doMatching)
    {
      // For-loop: All top quarks (for b-jet matching)
      for (size_t i=0; i<GenTops.size(); i++)
        {
          genParticle BQuark = GenTops_BQuark.at(i);
          Jet mcMatched_BJet;
          double dRmin  = 99999.9;

          // For-loop: All selected jets
          for (auto& bjet: jets)
            {
              double dR  = ROOT::Math::VectorUtil::DeltaR( bjet.p4(), BQuark.p4());
              double dPtOverPt = std::abs((bjet.pt() - BQuark.pt())/BQuark.pt());

	      // Find minimum dR
              if (dR > dRmin) continue;

              //Skip if dPtOverPt > twoSigmaDpt/Pt
              if (dPtOverPt > twoSigmaDpt) continue;

              // Store values
              dRmin  = dR;
              mcMatched_BJet = bjet;
            }// For-loop: All selected jets

          // Store match
          dRminB.push_back(dRmin);
          MC_BJets.push_back(mcMatched_BJet);
        }// For-loop: All top quarks    
      
      // For-loop: All top quarks (for dijet matching)
      for (size_t i=0; i<GenTops.size(); i++)
	{
	  genParticle top         = GenTops.at(i);
	  genParticle LdgQuark    = GenTops_LdgQuark.at(i);
	  genParticle SubldgQuark = GenTops_SubldgQuark.at(i);
	  Jet mcMatched_LdgJet, mcMatched_SubldgJet;	  
	  double dR1min, dR2min;
	  dR1min = dR2min = 99999.9;
	  
	  // For-loop: All selected jets
	  for (auto& jet: jets)
	    {
	      bool same = false;
	      
	      // For-loop: All top-quarks (Skip the jets that are matched to bquarks)
	      for (size_t k=0; k<GenTops.size(); k++)
		{
		  if (dRminB.at(k) > dRcut) continue;
		  if (areSameJets(jet,MC_BJets.at(k))) same = true;
		}// For-loop: All top-quarks
	      
	      if (same) continue;

	      // Find dR for the two jets in top-decay dijet
	      double dR1 = ROOT::Math::VectorUtil::DeltaR(jet.p4(), LdgQuark.p4());
	      double dR2 = ROOT::Math::VectorUtil::DeltaR(jet.p4(), SubldgQuark.p4());

	      // Calculate dPtOverPt for each jet in top-decay dijet
	      double dPtOverPt1 = std::abs((jet.pt() - LdgQuark.pt())/LdgQuark.pt());
	      double dPtOverPt2 = std::abs((jet.pt() - SubldgQuark.pt())/SubldgQuark.pt());
	      
	      // Find which of the two is the correct match                                                     
	      if (dR1 < dR2)
		{
		  // Is Jet1 closer in eta-phi AND has smaller pT difference?
		  if (dR1 < dR1min)
		    {
		      if (dPtOverPt1 < twoSigmaDpt)
			{
			  dR1min = dR1;
			  mcMatched_LdgJet = jet;
			}
		    }		  
		  // Is Jet2 closer in eta-phi AND has smaller pT difference?
		  else if (dR2 < dR2min)
		    {
		      if (dPtOverPt2 < twoSigmaDpt)
			{
			  dR2min  = dR2;
			  mcMatched_SubldgJet = jet;
			}
		    }
		}
	      else
		{
		  // Is Jet2 closer in eta-phi AND has smaller pT difference?
		  if (dR2 < dR2min)
		    {
		      if (dPtOverPt2 < twoSigmaDpt)
			{
			  dR2min  = dR2;
			  mcMatched_SubldgJet = jet;
			}
		    }		  
		  // Is Jet2 closer in eta-phi AND has smaller pT difference?
		  else if (dR1 < dR1min)
		    {
		      if  (dPtOverPt1 < twoSigmaDpt)
			{
			  dR1min  = dR1;
			  mcMatched_LdgJet = jet;
			}
		    }
		}
	    }//For-loop: All selected jets
	  
	  // Check if top-tagged object is genuine (fully truth-matched)
	  bool isGenuine = (dR1min<= dRcut && dR2min <= dRcut && dRminB.at(i) <= dRcut);

	  if (isGenuine)
	    {
	      // Store genuine top candidates
	      MCtrue_LdgJet.push_back(mcMatched_LdgJet);
	      MCtrue_SubldgJet.push_back(mcMatched_SubldgJet);
	      MCtrue_Bjet.push_back(MC_BJets.at(i));
	    }
	}
    }

  //================================================================================================
  // Calculate the event top-tagging Scale Factor (SF)
  //================================================================================================
  if (event.isMC())
    {

      // First of all, update the mc-truth info
      for (size_t i = 0; i < fAllCleanedTops.MVA.size(); i++)
	{      
	  bool isFullyMatched = IsGenuineTop(fAllCleanedTops.Jet1.at(i), fAllCleanedTops.Jet2.at(i), fAllCleanedTops.BJet.at(i), MCtrue_LdgJet, MCtrue_SubldgJet, MCtrue_Bjet);
	  fAllCleanedTops.isGenuine.at(i) = isFullyMatched;
	}

      // Calculate and store b-jet scale factor weight and it's uncertainty
      output.fTopTaggingScaleFactorEventWeight = fTopTagSFCalculator.calculateSF(fAllCleanedTops.TrijetP4, fAllCleanedTops.MVA, fAllCleanedTops.isTagged, fAllCleanedTops.isGenuine);
    }

    
  //================================================================================================
  // Fill output data
  //================================================================================================
  if (0) std::cout << "=== TopSelectionBDT:: Fill output" << std::endl;
  bool bPass_LdgMVA     = false;
  bool bPass_SubldgMVA  = false;

  if (fAllCleanedTops.MVA.size() < 1) 
    {
      bPass_LdgMVA    = false;
      bPass_SubldgMVA = false;
    }
  else if (fAllCleanedTops.MVA.size() == 1)
    {
      bPass_LdgMVA    = cfg_TopMVACut.passedCut( fAllCleanedTops.MVA.at(0) );
      bPass_SubldgMVA = false;

      // Leading-in-MVA top
      output.fMVAmax1           = fAllCleanedTops.MVA.at(0);
      output.fTrijet1Jet1       = fAllCleanedTops.Jet1.at(0);
      output.fTrijet1Jet2       = fAllCleanedTops.Jet2.at(0);
      output.fTrijet1BJet       = fAllCleanedTops.BJet.at(0);
      output.fTrijet1Dijet_p4   = fAllCleanedTops.Jet1.at(0).p4() + fAllCleanedTops.Jet2.at(0).p4();
      output.fTrijet1_p4        = fAllCleanedTops.TrijetP4.at(0);      
    }
  else // size > 1
    {
      bPass_LdgMVA     = cfg_TopMVACut.passedCut( fAllCleanedTops.MVA.at(0) );
      bPass_SubldgMVA  = cfg_TopMVACut.passedCut( fAllCleanedTops.MVA.at(1) );

      // Leading-in-MVA top
      output.fMVAmax1           = fAllCleanedTops.MVA.at(0);
      output.fTrijet1Jet1       = fAllCleanedTops.Jet1.at(0);
      output.fTrijet1Jet2       = fAllCleanedTops.Jet2.at(0);
      output.fTrijet1BJet       = fAllCleanedTops.BJet.at(0);
      output.fTrijet1Dijet_p4   = fAllCleanedTops.Jet1.at(0).p4() + fAllCleanedTops.Jet2.at(0).p4();
      output.fTrijet1_p4        = fAllCleanedTops.TrijetP4.at(0);
      // Subleading-in-MVA top
      output.fMVAmax2           = fAllCleanedTops.MVA.at(1);
      output.fTrijet2Jet1       = fAllCleanedTops.Jet1.at(1);
      output.fTrijet2Jet2       = fAllCleanedTops.Jet2.at(1);
      output.fTrijet2BJet       = fAllCleanedTops.BJet.at(1);
      output.fTrijet2Dijet_p4   = fAllCleanedTops.Jet1.at(1).p4() + fAllCleanedTops.Jet2.at(1).p4();
      output.fTrijet2_p4        = fAllCleanedTops.TrijetP4.at(1);
    }

  // Booleans
  bool bPass_FreeBjet   = (tetrajetBjetPt_max > 0);
  bool bPass_BothMVA    = bPass_LdgMVA * bPass_SubldgMVA;
  bool bPass_Selection  = bPass_FreeBjet * bPass_BothMVA;
  bool bPass_AnyTwoTops = false; // at least TWO tops with BDT > -1.0
  if (fAllCleanedTops.MVA.size() > 1) bPass_AnyTwoTops = cfg_AnyTopMVACut.passedCut(fAllCleanedTops.MVA.at(1) );
  
  // Fill in remaining data
  output.bPassedLdgMVA       = bPass_LdgMVA;
  output.bPassedSubldgMVA    = bPass_SubldgMVA;
  output.bPassedBothMVA      = bPass_BothMVA;
  output.bHasFreeBJet        = bPass_FreeBjet;
  output.bPassedSelection    = bPass_Selection;
  output.bHasTwoTopsAndFreeB = bPass_AnyTwoTops * bPass_FreeBjet;
  output.fTetrajetBJet       = tetrajetBjet;
  output.fLdgTetrajet_p4     = ldgTetrajet_P4;
  output.fSubldgTetrajet_p4  = subLdgTetrajet_P4;

  for (size_t i = 0; i < fSelectedTops.MVA.size(); i++)
    {
      output.fSelectedTopsJet1.push_back(fSelectedTops.Jet1.at(i));
      output.fSelectedTopsJet2.push_back(fSelectedTops.Jet2.at(i));
      output.fSelectedTopsBJet.push_back(fSelectedTops.BJet.at(i));
      output.fSelectedTopsMVA.push_back(fSelectedTops.MVA.at(i));
    }

  for (size_t i = 0; i < fNotSelectedTops.MVA.size(); i++)
    {
      output.fNotSelectedTopsJet1.push_back(fNotSelectedTops.Jet1.at(i));
      output.fNotSelectedTopsJet2.push_back(fNotSelectedTops.Jet2.at(i));
      output.fNotSelectedTopsBJet.push_back(fNotSelectedTops.BJet.at(i));
      output.fNotSelectedTopsMVA.push_back(fNotSelectedTops.MVA.at(i));
    }

  for (size_t i = 0; i < fAllTops.MVA.size(); i++)
    {
      output.fAllTopsJet1.push_back(fAllTops.Jet1.at(i));
      output.fAllTopsJet2.push_back(fAllTops.Jet2.at(i));
      output.fAllTopsBJet.push_back(fAllTops.BJet.at(i));
      output.fAllTopsMVA.push_back(fAllTops.MVA.at(i));
    }

  for (size_t i = 0; i < fSelectedCleanedTops.MVA.size(); i++)
    {
      output.fSelectedCleanedTopsJet1.push_back(fSelectedCleanedTops.Jet1.at(i));
      output.fSelectedCleanedTopsJet2.push_back(fSelectedCleanedTops.Jet2.at(i));
      output.fSelectedCleanedTopsBJet.push_back(fSelectedCleanedTops.BJet.at(i));
      output.fSelectedCleanedTopsMVA.push_back(fSelectedCleanedTops.MVA.at(i));
    }

  for (size_t i = 0; i < fAllCleanedTops.MVA.size(); i++)
    {
      output.fAllCleanedTopsJet1.push_back(fAllCleanedTops.Jet1.at(i));
      output.fAllCleanedTopsJet2.push_back(fAllCleanedTops.Jet2.at(i));
      output.fAllCleanedTopsBJet.push_back(fAllCleanedTops.BJet.at(i));
      output.fAllCleanedTopsMVA.push_back(fAllCleanedTops.MVA.at(i));
    }

   //================================================================================================
  // Increment counters
  //================================================================================================
  if (0) std::cout << "=== TopSelectionBDT:: Increment counters" << std::endl;
  if (bPass_LdgMVA) cSubPassedLdgMVACut.increment();
  if (bPass_SubldgMVA) cSubPassedSubldgMVACut.increment();
  if (bPass_Selection) cSubPassedFreeBjetCut.increment();
  if (bPass_Selection) cPassedTopSelectionBDT.increment();
   
  //================================================================================================
  // Fill histograms (only if all selectios passed)
  //================================================================================================
  if (0) std::cout << "=== TopSelectionBDT:: Filling histograms" << std::endl;
  if (!bPass_Selection) return output;

  // Leading in pt top
  double dijetMass = (top_ldgInPt.Jet1.p4() +  top_ldgInPt.Jet2.p4()).M();
  hLdgTrijetPt          -> Fill(top_ldgInPt.TrijetP4.Pt());
  hLdgTrijetMass        -> Fill(top_ldgInPt.TrijetP4.M());
  hLdgTrijetJet1Pt      -> Fill(top_ldgInPt.Jet1.pt());
  hLdgTrijetJet1Eta     -> Fill(top_ldgInPt.Jet1.eta());
  hLdgTrijetJet1BDisc   -> Fill(top_ldgInPt.Jet1.bjetDiscriminator());
  hLdgTrijetJet2Pt      -> Fill(top_ldgInPt.Jet2.pt());
  hLdgTrijetJet2Eta     -> Fill(top_ldgInPt.Jet2.eta());
  hLdgTrijetJet2BDisc   -> Fill(top_ldgInPt.Jet2.bjetDiscriminator());
  hLdgTrijetBJetPt      -> Fill(top_ldgInPt.BJet.pt());
  hLdgTrijetBJetEta     -> Fill(top_ldgInPt.BJet.eta());
  hLdgTrijetBJetBDisc   -> Fill(top_ldgInPt.BJet.bjetDiscriminator());
  hLdgTrijetDiJetPt     -> Fill(top_ldgInPt.DijetP4.Pt());
  hLdgTrijetDiJetEta    -> Fill(top_ldgInPt.DijetP4.Eta());
  hLdgTrijetDiJetMass   -> Fill(top_ldgInPt.DijetP4.M());
  hLdgTrijetTopMassWMassRatio -> Fill(top_ldgInPt.TrijetP4.M()/dijetMass);
  hLdgTrijetDijetDeltaR -> Fill(ROOT::Math::VectorUtil::DeltaR(top_ldgInPt.Jet1.p4(), top_ldgInPt.Jet2.p4()));
  hLdgTrijet_DeltaR_Trijet_TetrajetBjet   -> Fill(ROOT::Math::VectorUtil::DeltaR(top_ldgInPt.TrijetP4, output.fTetrajetBJet.p4()));
  hLdgTrijet_DeltaEta_Trijet_TetrajetBjet -> Fill(std::abs(top_ldgInPt.TrijetP4.Eta() - output.fTetrajetBJet.eta()));
  hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet -> Fill(std::abs(ROOT::Math::VectorUtil::DeltaPhi(top_ldgInPt.TrijetP4, output.fTetrajetBJet.p4())));
  double LdgTrijet_Rapidity    = 0.5*log((top_ldgInPt.TrijetP4.E() + top_ldgInPt.TrijetP4.Pz())/(top_ldgInPt.TrijetP4.E() - top_ldgInPt.TrijetP4.Pz()));
  double TetrajetBjet_Rapidity = 0.5*log((output.fTetrajetBJet.p4().E() + output.fTetrajetBJet.p4().Pz())/(output.fTetrajetBJet.p4().E() - output.fTetrajetBJet.p4().Pz()));
  hLdgTrijet_DeltaY_Trijet_TetrajetBjet   -> Fill(std::abs(LdgTrijet_Rapidity - TetrajetBjet_Rapidity));
  
  // Subleading in pt top
  hSubldgTrijetPt           -> Fill(top_subLdgInPt.TrijetP4.Pt());
  hSubldgTrijetMass         -> Fill(top_subLdgInPt.TrijetP4.M());
  hSubldgTrijetJet1Pt       -> Fill(top_subLdgInPt.Jet1.pt());
  hSubldgTrijetJet1Eta      -> Fill(top_subLdgInPt.Jet1.eta());
  hSubldgTrijetJet1BDisc    -> Fill(top_subLdgInPt.Jet1.bjetDiscriminator());    
  hSubldgTrijetJet2Pt       -> Fill(top_subLdgInPt.Jet2.pt());
  hSubldgTrijetJet2Eta      -> Fill(top_subLdgInPt.Jet2.eta());
  hSubldgTrijetJet2BDisc    -> Fill(top_subLdgInPt.Jet2.bjetDiscriminator());
  hSubldgTrijetBJetPt       -> Fill(top_subLdgInPt.BJet.pt());
  hSubldgTrijetBJetEta      -> Fill(top_subLdgInPt.BJet.eta());
  hSubldgTrijetBJetBDisc    -> Fill(top_subLdgInPt.BJet.bjetDiscriminator());
  hSubldgTrijetDiJetPt      -> Fill(top_subLdgInPt.DijetP4.Pt());
  hSubldgTrijetDiJetEta     -> Fill(top_subLdgInPt.DijetP4.Eta());
  hSubldgTrijetDiJetMass    -> Fill(top_subLdgInPt.DijetP4.M());
  hSubldgTrijetDijetDeltaR  -> Fill(ROOT::Math::VectorUtil::DeltaR(top_subLdgInPt.Jet1.p4(), top_subLdgInPt.Jet2.p4()));
  hSubldgTrijetTopMassWMassRatio -> Fill(top_subLdgInPt.TrijetP4.M()/(top_subLdgInPt.Jet1.p4() + top_subLdgInPt.Jet2.p4()).M());    
  hSubldgTrijetDijetDeltaR -> Fill(ROOT::Math::VectorUtil::DeltaR(top_subLdgInPt.Jet1.p4(), top_subLdgInPt.Jet2.p4()));
  hSubldgTrijet_DeltaR_Trijet_TetrajetBjet   -> Fill(ROOT::Math::VectorUtil::DeltaR(top_subLdgInPt.TrijetP4, output.fTetrajetBJet.p4()));
  hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet -> Fill(std::abs(top_subLdgInPt.TrijetP4.Eta() - output.fTetrajetBJet.eta()));
  hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet -> Fill(std::abs(ROOT::Math::VectorUtil::DeltaPhi(top_subLdgInPt.TrijetP4, output.fTetrajetBJet.p4())));
  double SubldgTrijet_Rapidity = 0.5*log((top_subLdgInPt.TrijetP4.E() + top_subLdgInPt.TrijetP4.Pz())/(top_subLdgInPt.TrijetP4.E() - top_subLdgInPt.TrijetP4.Pz()));
  hSubldgTrijet_DeltaY_Trijet_TetrajetBjet   -> Fill(std::abs(SubldgTrijet_Rapidity - TetrajetBjet_Rapidity));
  
  // Ldg in pt free b-jet
  hTetrajetBJetPt-> Fill(output.fTetrajetBJet.pt());
  hTetrajetBJetEta-> Fill(output.fTetrajetBJet.eta());
  hTetrajetBJetBDisc-> Fill(output.fTetrajetBJet.bjetDiscriminator());

  // Tetrajet 
  hTetrajetPt-> Fill(output.fLdgTetrajet_p4.Pt());
  hTetrajetMass-> Fill(output.fLdgTetrajet_p4.M());
  hTetrajetEta -> Fill(output.fLdgTetrajet_p4.Eta());
  hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet -> Fill(LdgTrijet_Rapidity - TetrajetBjet_Rapidity, SubldgTrijet_Rapidity - TetrajetBjet_Rapidity);
  
  double LdgTrijet_DeltaR = ROOT::Math::VectorUtil::DeltaR(top_ldgInPt.TrijetP4, output.fTetrajetBJet.p4());
  double SubldgTrijet_DeltaR = ROOT::Math::VectorUtil::DeltaR(top_subLdgInPt.TrijetP4, output.fTetrajetBJet.p4());
  hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet -> Fill(LdgTrijet_DeltaR, SubldgTrijet_DeltaR);
  
  double LdgTrijet_DeltaEta = std::abs(top_ldgInPt.TrijetP4.Eta() - output.fTetrajetBJet.eta());
  double SubldgTrijet_DeltaEta = std::abs(top_subLdgInPt.TrijetP4.Eta() - output.fTetrajetBJet.eta());
  hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet -> Fill(LdgTrijet_DeltaEta, SubldgTrijet_DeltaEta);
  
  double LdgTrijet_DeltaPhi = std::abs(ROOT::Math::VectorUtil::DeltaPhi(top_ldgInPt.TrijetP4, output.fTetrajetBJet.p4()));
  double SubldgTrijet_DeltaPhi = std::abs(ROOT::Math::VectorUtil::DeltaPhi(top_subLdgInPt.TrijetP4, output.fTetrajetBJet.p4()));
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet -> Fill(LdgTrijet_DeltaPhi, SubldgTrijet_DeltaPhi);

  return output;
}

bool TopSelectionBDT::areSameJets(const Jet& jet1, const Jet& jet2) {
  float dR = ROOT::Math::VectorUtil::DeltaR(jet1.p4(), jet2.p4());
  float dR_match = 0.1;
  if (dR <= dR_match) return true;
  else return false;
}

bool TopSelectionBDT::isBJet(const Jet& jet, const std::vector<Jet>& bjets) {
  for (auto bjet: bjets)
    {
      if (areSameJets(jet, bjet)) return true;
    }
  return false;
}

Jet TopSelectionBDT::getLeadingSubleadingJet(const Jet& jet0, const Jet& jet1, string selectedJet){
  if (selectedJet != "leading" && selectedJet!="subleading") std::cout<<"WARNING! Unknown option "<<selectedJet<<". Function getLeadingSubleadingJet returns leading Jet"<<std::endl;
  Jet leadingJet, subleadingJet;
  if (jet0.pt() > jet1.pt()){                                                                                                   
    leadingJet    = jet0;                  
    subleadingJet = jet1;      
  }           
  else{                         
    leadingJet    = jet1;                                          
    subleadingJet = jet0;
  }
  if (selectedJet == "subleading") return subleadingJet;
  return leadingJet;
}

genParticle TopSelectionBDT::getLeadingSubleadingParton(const genParticle& quark0, const genParticle& quark1, string selectedParton){
  if (selectedParton != "leading" && selectedParton!="subleading") std::cout<<"WARNING! Unknown option "<<selectedParton<<". Function getLeadingSubleadingParton returns leading Parton"<<std::endl;
  genParticle leadingParton, subleadingParton;
  if (quark0.pt() > quark1.pt()){                                                                                                   
    leadingParton    = quark0;                  
    subleadingParton = quark1;      
  }           
  else{                         
    leadingParton    = quark1;                                          
    subleadingParton = quark0;
  }
  if (selectedParton == "subleading") return subleadingParton;
  return leadingParton;
}


bool TopSelectionBDT::isMatchedJet(const Jet& jet, const TrijetSelection& myTops, const unsigned int index) {
  // Sanity check: If index is bigger than the number of tops that top does not exist => not possible to be matched
  if ( index+1 > myTops.MVA.size()) return false;

  std::vector<Jet> jets;
  jets.push_back(myTops.Jet1.at(index));
  jets.push_back(myTops.Jet2.at(index));
  jets.push_back(myTops.BJet.at(index));
  
  for (auto iJet: jets)
    {
      if (areSameJets(jet, iJet)) return true;
    }
  return false;
}

TrijetSelection TopSelectionBDT::SortInMVAvalue(TrijetSelection TopCand){
  //  Description
  //  Takes as input a collection of Top Candidates and returns the collection sorted in BDT(MVA) value
  size_t size = TopCand.MVA.size();
  if (size < 1) return TopCand;

  for (size_t i=0; i<size-1; i++)
    {
      for  (size_t j=i+1; j<size; j++)
	{
	  Jet Jet1_i   = TopCand.Jet1.at(i);
	  Jet Jet2_i   = TopCand.Jet2.at(i);
	  Jet BJet_i   = TopCand.BJet.at(i);
	  double mva_i = TopCand.MVA.at(i);
	  math::XYZTLorentzVector TrijetP4_i = TopCand.TrijetP4.at(i);
	  math::XYZTLorentzVector DijetP4_i  = TopCand.DijetP4.at(i);
	  bool isGenuine_i = TopCand.isGenuine.at(i);
          bool isTagged_i  = TopCand.isTagged.at(i);

	  Jet Jet1_j   = TopCand.Jet1.at(j);
	  Jet Jet2_j   = TopCand.Jet2.at(j);
	  Jet BJet_j   = TopCand.BJet.at(j);
	  double mva_j = TopCand.MVA.at(j);
	  math::XYZTLorentzVector TrijetP4_j = TopCand.TrijetP4.at(j);
	  math::XYZTLorentzVector DijetP4_j  = TopCand.DijetP4.at(j);
	  bool isGenuine_j = TopCand.isGenuine.at(j);
          bool isTagged_j  = TopCand.isTagged.at(j);

	  if (mva_i >= mva_j) continue;
	  TopCand.Jet1.at(i) = Jet1_j;
	  TopCand.Jet2.at(i) = Jet2_j;
	  TopCand.BJet.at(i) = BJet_j;
	  TopCand.MVA.at(i)  = mva_j;
	  TopCand.TrijetP4.at(i)  = TrijetP4_j;
	  TopCand.DijetP4.at(i)   = DijetP4_j;
	  TopCand.isGenuine.at(i) = isGenuine_j;
          TopCand.isTagged.at(i)  = isTagged_j;

	  TopCand.Jet1.at(j)      = Jet1_i;
	  TopCand.Jet2.at(j)      = Jet2_i;
	  TopCand.BJet.at(j)      = BJet_i;
	  TopCand.MVA.at(j)       = mva_i;
	  TopCand.TrijetP4.at(j)  = TrijetP4_i;
	  TopCand.DijetP4.at(j)   = DijetP4_i;
	  TopCand.isGenuine.at(j) = isGenuine_i;
          TopCand.isTagged.at(j)  = isTagged_i;
	}
    }
  return TopCand;
}

bool TopSelectionBDT::foundFreeBjet(const Jet& trijet1Jet1, const Jet& trijet1Jet2, const Jet& trijet1BJet, const Jet& trijet2Jet1, const Jet& trijet2Jet2, const Jet& trijet2BJet , const std::vector<Jet>& bjets){
  //Description:
  //Returns false if two trijet combinations use all the bjets of the event
  //Used to select the best two top candidates which are not formed by all the bjets off the event
  //One free bjet is required for the tetrajet reconstruction
  int SumTrijet1 = isBJet(trijet1Jet1, bjets) + isBJet(trijet1Jet2, bjets) + isBJet(trijet1BJet, bjets);
  int SumTrijet2 = isBJet(trijet2Jet1, bjets) + isBJet(trijet2Jet2, bjets) + isBJet(trijet2BJet, bjets);
  if ((size_t)(SumTrijet1 + SumTrijet2) != bjets.size()) return true;
  return false;
}

SelectedTrijets TopSelectionBDT::getLdgOrSubldgTop(TrijetSelection myTops, string selectedTrijet){
  //  Description
  //  Takes as input a collection of  selected and cross-cleaned  tops 
  //  Returns the leading/subleading in pt top
  if (selectedTrijet != "leading" && selectedTrijet!="subleading") 
    {
      std::cout<<"WARNING! Unknown option "<< selectedTrijet << ". Function returns leading top"<<std::endl;
    }
  
  // Declarations
  SelectedTrijets top_ldgInPt;
  SelectedTrijets top_subLdgInPt;
 
  // Sanity check: If  the number of tops if less than 2 (1) return the only top (empty object)
  if ( myTops.MVA.size() == 0) return top_ldgInPt;
  if ( myTops.MVA.size() == 1) 
    {
      top_ldgInPt.Jet1      = getLeadingSubleadingJet(myTops.Jet1.at(0), myTops.Jet2.at(0), "leading");
      top_ldgInPt.Jet2      = getLeadingSubleadingJet(myTops.Jet1.at(0), myTops.Jet2.at(0), "subleading");
      top_ldgInPt.BJet      = myTops.BJet.at(0);
      top_ldgInPt.DijetP4   = myTops.DijetP4.at(0);
      top_ldgInPt.TrijetP4  = myTops.TrijetP4.at(0);
      top_ldgInPt.MVA       = myTops.MVA.at(0);
      top_ldgInPt.isGenuine = myTops.isGenuine.at(0);
      top_ldgInPt.isTagged  = myTops.isTagged.at(0);
      return top_ldgInPt;
    }

  // Assuming myTops are selected and cross-cleaned
  if(myTops.TrijetP4.at(0).Pt() > myTops.TrijetP4.at(1).Pt())
    {
      top_ldgInPt.Jet1      = getLeadingSubleadingJet(myTops.Jet1.at(0), myTops.Jet2.at(0), "leading");
      top_ldgInPt.Jet2      = getLeadingSubleadingJet(myTops.Jet1.at(0), myTops.Jet2.at(0), "subleading");
      top_ldgInPt.BJet      = myTops.BJet.at(0);
      top_ldgInPt.DijetP4   = myTops.DijetP4.at(0);
      top_ldgInPt.TrijetP4  = myTops.TrijetP4.at(0);
      top_ldgInPt.MVA       = myTops.MVA.at(0);
      top_ldgInPt.isGenuine = myTops.isGenuine.at(0);
      top_ldgInPt.isTagged  = myTops.isTagged.at(0);

      top_subLdgInPt.Jet1      = getLeadingSubleadingJet(myTops.Jet1.at(1), myTops.Jet2.at(1), "leading");
      top_subLdgInPt.Jet2      = getLeadingSubleadingJet(myTops.Jet1.at(1), myTops.Jet2.at(1), "subleading");
      top_subLdgInPt.BJet      = myTops.BJet.at(1);
      top_subLdgInPt.DijetP4   = myTops.DijetP4.at(1);
      top_subLdgInPt.TrijetP4  = myTops.TrijetP4.at(1);
      top_subLdgInPt.MVA       = myTops.MVA.at(1);
      top_subLdgInPt.isGenuine = myTops.isGenuine.at(1);
      top_subLdgInPt.isTagged  = myTops.isTagged.at(1);

    }
  else  // if(myTops.TrijetP4.at(1).Pt() > myTops.TrijetP4.at(0).Pt())
    {
      top_ldgInPt.Jet1      = getLeadingSubleadingJet(myTops.Jet1.at(1), myTops.Jet2.at(1), "leading");
      top_ldgInPt.Jet2      = getLeadingSubleadingJet(myTops.Jet1.at(1), myTops.Jet2.at(1), "subleading");
      top_ldgInPt.BJet      = myTops.BJet.at(1);
      top_ldgInPt.DijetP4   = myTops.DijetP4.at(1);
      top_ldgInPt.TrijetP4  = myTops.TrijetP4.at(1);
      top_ldgInPt.MVA       = myTops.MVA.at(1);
      top_ldgInPt.isGenuine = myTops.isGenuine.at(1);
      top_ldgInPt.isTagged  = myTops.isTagged.at(1);

      top_subLdgInPt.Jet1      = getLeadingSubleadingJet(myTops.Jet1.at(0), myTops.Jet2.at(0), "leading");
      top_subLdgInPt.Jet2      = getLeadingSubleadingJet(myTops.Jet1.at(0), myTops.Jet2.at(0), "subleading");
      top_subLdgInPt.BJet      = myTops.BJet.at(0);
      top_subLdgInPt.DijetP4   = myTops.DijetP4.at(0);
      top_subLdgInPt.TrijetP4  = myTops.TrijetP4.at(0);
      top_subLdgInPt.MVA       = myTops.MVA.at(0);
      top_subLdgInPt.isGenuine = myTops.isGenuine.at(0);
      top_subLdgInPt.isTagged  = myTops.isTagged.at(0);
    }

  if (selectedTrijet == "subleading") return top_subLdgInPt;
  return top_ldgInPt;
}

SelectedTrijets TopSelectionBDT::GetSelectedTopCandidate(TrijetSelection TopCand, int index){
  SelectedTrijets trijet;
  trijet.Jet1 = TopCand.Jet1.at(index);
  trijet.Jet2 = TopCand.Jet2.at(index);
  trijet.BJet = TopCand.BJet.at(index);
  trijet.MVA  = TopCand.MVA.at(index);
  trijet.TrijetP4  = TopCand.TrijetP4.at(index);
  trijet.DijetP4   = TopCand.DijetP4.at(index);
  trijet.isGenuine = TopCand.isGenuine.at(index);
  trijet.isTagged  = TopCand.isTagged.at(index);
  return trijet;
}

bool TopSelectionBDT::TopIsCrossCleaned(int Index, TrijetSelection TopCand, const std::vector<Jet>& bjets){
  // Description:
  // Used to find the cross-cleaned trijet multiplicity. The function takes as input the index of a trijet and the total trijet collection and returns 
  // False: (a) If the trijet uses all the bjets of the event
  //       (b) If at least one of the subjets of the trijets are used by the trijets with Higher BDT value (Higher BDT value -> smaller index: Trijets sorted in BDT value) 
  // True: If cross-cleaned trijet 
  
  bool jet1IsB = isBJet(TopCand.Jet1.at(Index), bjets);
  bool jet2IsB = isBJet(TopCand.Jet2.at(Index), bjets);
  bool bjetIsB = isBJet(TopCand.BJet.at(Index), bjets);
  if ( (size_t)(jet1IsB + jet2IsB + bjetIsB) ==  bjets.size()) return false;

  if (Index > 0)
    {
      for (size_t i=0; i<(size_t)Index; i++)
	{
	  // Skip top candidates with same jets as Trijets with higher BDDT value
	  bool bMatchedJet1 = isMatchedJet(TopCand.Jet1.at(Index), TopCand, i);
	  bool bMatchedJet2 = isMatchedJet(TopCand.Jet2.at(Index), TopCand, i);
	  bool bMatchedBJet = isMatchedJet(TopCand.BJet.at(Index), TopCand, i);
	  bool sharedJets = bMatchedJet1 || bMatchedJet2 || bMatchedBJet;
	  //if (bMatchedJet1 || bMatchedJet2 || bMatchedBJet) return false;
	  if (sharedJets && TopIsCrossCleaned(i, TopCand, bjets)) return false;
	}
    }
  
  return true;
}

//Get all gen particles by pdgId
vector<genParticle> TopSelectionBDT::GetGenParticles(const vector<genParticle> genParticles, const int pdgId)
{
  std::vector<genParticle> particles;
  // For-loop: All genParticles  
  for (auto& p: genParticles){
    // Find last copy of a given particle
    if (!p.isLastCopy()) continue;
    // Consider only particles
    if (std::abs(p.pdgId()) != pdgId) continue;
    // Save this particle
    particles.push_back(p);
  }
  return particles;
}

//  Get the last copy of a particle.
const genParticle TopSelectionBDT::GetLastCopy(const vector<genParticle> genParticles, const genParticle &p){

  int gen_pdgId = p.pdgId();
  for (size_t i=0; i<p.daughters().size(); i++){
    const genParticle genDau = genParticles[p.daughters().at(i)];
    int genDau_pdgId   = genDau.pdgId();

    if (gen_pdgId == genDau_pdgId)  return GetLastCopy(genParticles, genDau);
  }
  return p;
}


vector<genParticle> TopSelectionBDT::GetWpartons( genParticle daughter, const Event& event){
  vector<genParticle> quarks;

  // Get the last copy
  genParticle W = GetLastCopy(event.genparticles().getGenParticles(), daughter);
  // For-loop: W-boson daughters
  for (size_t idau = 0; idau < W.daughters().size(); idau++)
    {
      // Find the decay products of W-boson
      int Wdau_index   = W.daughters().at(idau);
      genParticle Wdau = event.genparticles().getGenParticles()[Wdau_index];
      // Consider only quarks as decaying products
      if (std::abs(Wdau.pdgId()) > 5) continue;
      // Save daughter
      quarks.push_back(Wdau);
    }//W-boson daughters
  
  return quarks;
}

bool TopSelectionBDT::IsGenuineTop(const Jet& trijetJet1, const Jet& trijetJet2, const Jet& trijetBJet,
				   const std::vector<Jet>& MCtrue_LdgJet,  const std::vector<Jet>& MCtrue_SubldgJet, const std::vector<Jet>& MCtrue_Bjet){
  
  for (size_t k=0; k<MCtrue_Bjet.size(); k++){
    bool same1 = areSameJets(trijetJet1, MCtrue_LdgJet.at(k))       && areSameJets(trijetJet2, MCtrue_SubldgJet.at(k)) && areSameJets(trijetBJet,  MCtrue_Bjet.at(k));
    bool same2 = areSameJets(trijetJet1, MCtrue_SubldgJet.at(k))    && areSameJets(trijetJet2, MCtrue_LdgJet.at(k))    && areSameJets(trijetBJet,  MCtrue_Bjet.at(k));
    if (same1 || same2) return true;
  }
  return false;
}

  

  
  

    
  

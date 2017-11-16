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
  fSubldgTetrajet_p4()
{ }

TopSelectionBDT::Data::~Data() { }


TopSelectionBDT::TopSelectionBDT(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
  : BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
    // Input parameters
    cfg_MVACut(config, "MVACut"),
    cfg_MassCut(config, "MassCut"),
    //    cfg_MVACuts(config.getParameter<std::vector<float>>("MVACuts")),
    cfg_CSV_bDiscCut(config, "CSV_bDiscCut"),
    cfg_NjetsMax(config.getParameter<unsigned int>("NjetsMax")),
    cfg_NBjetsMax(config.getParameter<unsigned int>("NBjetsMax")),
    cfg_ReplaceJetsWithGenJets(config.getParameter<bool>("ReplaceJetsWithGenJets")),
    // Event counter for passing selection
    cPassedTopSelectionBDT(fEventCounter.addCounter("passed top selection ("+postfix+")")),
    // Sub counters
    cSubAll(fEventCounter.addSubCounter("top selection ("+postfix+")", "All events")),
    cSubPassedFreeBjetCut(fEventCounter.addSubCounter("top selection ("+postfix+")", "Passed Free Bjet cut")),
    cSubPassedBDTCut(fEventCounter.addSubCounter("top selection ("+postfix+")", "Passed BDT cut"))
{
  initialize(config);
}

TopSelectionBDT::TopSelectionBDT(const ParameterSet& config)
: BaseSelection(),
  // Input parameters
  cfg_MVACut(config, "MVACut"),
  cfg_MassCut(config, "MassCut"),
  //  cfg_MVACuts(config.getParameter<std::vector<float>>("MVACuts")),
  cfg_CSV_bDiscCut(config, "CSV_bDiscCut"),
  cfg_NjetsMax(config.getParameter<int>("NjetsMax")),
  cfg_NBjetsMax(config.getParameter<int>("NBjetsMax")),
  cfg_ReplaceJetsWithGenJets(config.getParameter<bool>("ReplaceJetsWithGenJets")),  
  // Event counter for passing selection
  cPassedTopSelectionBDT(fEventCounter.addCounter("passed top selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("top selection", "All events")),
  cSubPassedFreeBjetCut(fEventCounter.addSubCounter("top selection", "Passed Free Bjet cut")),
  cSubPassedBDTCut(fEventCounter.addSubCounter("top selection", "Passed BDT cut"))
{
  initialize(config);
  bookHistograms(new TDirectory());

}

TopSelectionBDT::~TopSelectionBDT() {
  
  // Histograms (1D)
  delete hBDTresponse;
  delete hTopCandMass;

  delete hLdgTrijetTopMassWMassRatio;
  delete hSubldgTrijetTopMassWMassRatio;
  delete hTetrajetBJetPt;
  delete hTetrajetBJetEta;
  delete hTetrajetBJetBDisc;
  delete hTetrajetPt;
  delete hTetrajetMass;
  delete hTetrajetEta;
  
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

  delete hTopQuarkPt;
  delete hTopQuarkPt_InTopDirBDT;
  delete hTopQuarkPt_InTopDir;
  delete hTrijetPt_BDT;
  delete hAllTopQuarkPt_InTopDir;
  delete hAllTopQuarkPt_InTopDirBDT;
  delete hAllTopQuarkPt_Matched;
  delete hAllTopQuarkPt_MatchedBDT;

  delete hTopQuarkPt_BDT;

  delete hLdgTrijetFake;
  delete hLdgTrijetFake_BDT;

  delete hBDTmultiplicity;
  delete hTrijetInTopDirNonMatched_Mass;
  delete hTrijetInTopDir_Mass;
  delete hTrijetTopMatched_Mass;
  delete hInTopDirBDTmult;
  delete hMatchedBDTmult;
  delete hEventTrijetPt_BDT;
  delete hEventTrijetPt_InTopDirBDT;

  delete hEventTrijetPt2T_BDT;
  delete hEventTrijetPt2T_MatchedBDT;

  delete hTrijetNotInTopDirPt;
  delete hTrijetNotInTopDirPt_BDT;
  delete hTrijetFakePt;
  delete hTrijetFakePt_BDT;

  delete hDeltaRMinTopTrijet;
  delete hEventTrijetPt2T_Matched;
  delete hAllTopQuarkPt_NotInTopDir;

  delete hEventTrijetPt;
  delete hEventTrijetPt2T;
  
  delete hRealSelectedTopMult;
  delete hTrijetMultiplicity;
  delete hTrijetBDT_Mass;
  delete hTrijetMatched_BDTvalue;
  delete hTrijetNonMatched_BDTvalue;

  delete hNjets;
  delete hDeltaMVAmax_MCtruth_SameObjFakes;
  delete hAbsDeltaMVAmax_MCtruth_SameObjFakes;
  delete hTrijetCountForBDTcuts;
  delete hFakeInTopDirMult;

  delete hDeltaMVAmax_MCtruth_SameObjFakesPassBDT;
  delete hDeltaMVAmin_MCtruth_SameObjFakes;
  delete hDeltaMVAmin_MCtruth_SameObjFakesPassBDT;
  delete hMatchedTrijetMult_JetsGT9;
  delete hMatchedTrijetMult_JetsInc;
  delete hMVAvalue_DeltaMVAgt1;
  delete hMatchedPassBDTmult_SameObjFakes;

  delete hAllTrijetPassBDT_pt;
  delete hAllTrijetPassBDTbPassCSV_pt;
  delete hTrijetPassBDT_bDisc;

  delete hChHiggsBjetPt_TetrajetBjetMatched;
  delete hChHiggsBjetPt_foundTetrajetBjet;
  delete hHiggsBjetPt;
  delete hHiggsBjetPt_LdgBjetMatched;
  delete hLdgBjetPt;
  delete hLdgBjetPt_isLdgFreeBjet;
  delete hTrijetPtMaxMVASameFakeObj_BjetPassCSV;
  delete hTrijetPtMaxMVASameFakeObj;
  delete hNSelectedTrijets;

  delete hTopFromHiggsPt_isLdgMVATrijet;
  delete hTopFromHiggsPt_isSubldgMVATrijet;
  delete hTopFromHiggsPt_isMVATrijet;

  delete hDeltaPtOverPt_TopFromH_LdgMVATrijet;
  delete hDeltaEta_TopFromH_LdgMVATrijet;
  delete hDeltaPhi_TopFromH_LdgMVATrijet;
  delete hDeltaR_TopFromH_LdgMVATrijet;

  delete hDeltaPtOverPt_TopFromH_SubldgMVATrijet;
  delete hDeltaEta_TopFromH_SubldgMVATrijet;
  delete hDeltaPhi_TopFromH_SubldgMVATrijet;
  delete hDeltaR_TopFromH_SubldgMVATrijet;
  
  delete hTopFromHiggsPt;


  delete hChHiggsBjetPt_TetrajetBjetMatched_afterCuts;
  delete hChHiggsBjetPt_foundTetrajetBjet_afterCuts;
  delete hHiggsBjetPt_afterCuts;
  delete hHiggsBjetPt_LdgBjetMatched_afterCuts;
  delete hLdgBjetPt_afterCuts;
  delete hLdgBjetPt_isLdgFreeBjet_afterCuts;

  delete hTopFromHiggsPt_isLdgMVATrijet_afterCuts;
  delete hTopFromHiggsPt_isSubldgMVATrijet_afterCuts;
  delete hTopFromHiggsPt_isMVATrijet_afterCuts;

  delete hDeltaPtOverPt_TopFromH_LdgMVATrijet_afterCuts;
  delete hDeltaEta_TopFromH_LdgMVATrijet_afterCuts;
  delete hDeltaPhi_TopFromH_LdgMVATrijet_afterCuts;
  delete hDeltaR_TopFromH_LdgMVATrijet_afterCuts;

  delete hDeltaPtOverPt_TopFromH_SubldgMVATrijet_afterCuts;
  delete hDeltaEta_TopFromH_SubldgMVATrijet_afterCuts;
  delete hDeltaPhi_TopFromH_SubldgMVATrijet_afterCuts;
  delete hDeltaR_TopFromH_SubldgMVATrijet_afterCuts;

  delete hDeltaCSV_TopFromHBJet_LdgMVATrijetBjet_afterCuts;
  delete hDeltaBDT_TopFromH_LdgMVATrijet_afterCuts;

  delete hDeltaCSV_TopFromHBJet_SubldgMVATrijetBjet_afterCuts;
  delete hDeltaBDT_TopFromH_SubldgMVATrijet_afterCuts;

  delete hDeltaPtOverPt_HiggsBjetPt_TetrajetBjetMatched_afterCuts;
  delete hDeltaEta_HiggsBjetPt_TetrajetBjetMatched_afterCuts;
  delete hDeltaPhi_HiggsBjetPt_TetrajetBjetMatched_afterCuts;
  delete hDeltaR_HiggsBjetPt_TetrajetBjetMatched_afterCuts;
  delete hDeltaCSV_HiggsBjetPt_TetrajetBjetMatched_afterCuts;

  delete hTopFromHiggsPt_afterCuts;

  delete hSelectedTrijetsPt_BjetPassCSVdisc_afterCuts;
  delete hSelectedTrijetsPt_afterCuts;
  delete hTrijetPt_PassBDT_BJetPassCSV;
  delete hTrijetPt_PassBDT;

  // Histograms (2D)
  delete hNjetsVsNTrijets_beforeBDT;
  delete hNjetsVsNTrijets_afterBDT;

  delete hDeltaMVAmaxVsTrijetPassBDTvalue;
  delete hDeltaMVAminVsTrijetPassBDTvalue;
  delete hFakeTrijetMassVsBDTvalue;

  delete hTopFromHiggsPtVSAssocTopPt;
  delete DEta_Trijet1TetrajetBjet_Vs_DEta_Trijet2TetrajetBjet;
  delete DPhi_Trijet1TetrajetBjet_Vs_DPhi_Trijet2TetrajetBjet;
  delete DR_Trijet1TetrajetBjet_Vs_DR_Trijet2TetrajetBjet;
  delete DEta_TopFromHBjetFromH_Vs_DEta_AssocTopBjetFromH;
  delete DPhi_TopFromHBjetFromH_Vs_DPhi_AssocTopBjetFromH;
  delete DR_TopFromHBjetFromH_Vs_DR_AssocTopBjetFromH;
  
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
  // reader->AddVariable( "TrijetLdgJetQGLikelihood",     &TrijetLdgJetQGLikelihood);
  // reader->AddVariable( "TrijetSubldgJetQGLikelihood",  &TrijetSubldgJetQGLikelihood);

  // Read the xml file
  reader->BookMVA("BTDG method", "/uscms_data/d3/skonstan/CMSSW_8_0_28/src/HiggsAnalysis/NtupleAnalysis/src/EventSelection/interface/weights/TMVAClassification_BDTG.weights.xml");
}

void TopSelectionBDT::bookHistograms(TDirectory* dir) {

  // Fixed binning
  
  const int nPtBins       = 2 * fCommonPlots->getPtBinSettings().bins();
  const double fPtMin     = 2 * fCommonPlots->getPtBinSettings().min();
  const double fPtMax     = 2 * fCommonPlots->getPtBinSettings().max();

  const int  nEtaBins     = fCommonPlots->getEtaBinSettings().bins();
  const float fEtaMin     = fCommonPlots->getEtaBinSettings().min();
  const float fEtaMax     = fCommonPlots->getEtaBinSettings().max();

  const int nDEtaBins     = fCommonPlots->getDeltaEtaBinSettings().bins();
  const double fDEtaMin   = fCommonPlots->getDeltaEtaBinSettings().min();
  const double fDEtaMax   = fCommonPlots->getDeltaEtaBinSettings().max();
  
  const int nDPhiBins     = fCommonPlots->getDeltaPhiBinSettings().bins();
  const double fDPhiMin   = fCommonPlots->getDeltaPhiBinSettings().min();
  const double fDPhiMax   = fCommonPlots->getDeltaPhiBinSettings().max();
  
  const int nDRBins       = fCommonPlots->getDeltaRBinSettings().bins();
  const double fDRMin     = fCommonPlots->getDeltaRBinSettings().min();
  const double fDRMax     = fCommonPlots->getDeltaRBinSettings().max();

  const int  nBDiscBins   = fCommonPlots->getBJetDiscBinSettings().bins();
  const float fBDiscMin   = fCommonPlots->getBJetDiscBinSettings().min();
  const float fBDiscMax   = fCommonPlots->getBJetDiscBinSettings().max();

  const int nWMassBins    = fCommonPlots->getWMassBinSettings().bins();
  const float fWMassMin   = fCommonPlots->getWMassBinSettings().min();
  const float fWMassMax   = fCommonPlots->getWMassBinSettings().max();

  const int nTopMassBins  = fCommonPlots->getTopMassBinSettings().bins();
  const float fTopMassMin = fCommonPlots->getTopMassBinSettings().min();
  const float fTopMassMax = fCommonPlots->getTopMassBinSettings().max();

  const int nInvMassBins  = fCommonPlots->getInvMassBinSettings().bins();
  const float fInvMassMin = fCommonPlots->getInvMassBinSettings().min();
  const float fInvMassMax = fCommonPlots->getInvMassBinSettings().max();
  
  // Histograms (1D) 
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kVital, dir, "topbdtSelection_" + sPostfix);
  TDirectory* subdirTH2 = fHistoWrapper.mkdir(HistoLevel::kVital, dir, "topbdtSelectionTH2_" + sPostfix);

  hBDTresponse  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"BDTGresponse",";BDTG response", 40, -1., 1.) ; 
  hTopCandMass  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"TopCandMass" ,";M (GeVc^{-2})", nTopMassBins, fTopMassMin, fTopMassMax);

  hTetrajetBJetPt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetPt"   ,";p_{T} (GeV/c)"      , nPtBins     , fPtMin     , fPtMax);
  hTetrajetBJetEta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetEta"  ,";#eta"               , nEtaBins    , fEtaMin    , fEtaMax);
  hTetrajetBJetBDisc  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetBDisc",";b-tag discriminator", nBDiscBins  , fBDiscMin  , fBDiscMax);
  hTetrajetPt         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetPt"       , ";p_{T} (GeV/c)"     , nPtBins     , fPtMin     , fPtMax);
  hTetrajetMass       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetMass"     , ";M (GeV/c^{2})"     , nInvMassBins, fInvMassMin, fInvMassMax);
  hTetrajetEta        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetEta"      , ";#eta"              , nEtaBins    , fEtaMin    , fEtaMax);

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
  hLdgTrijetDijetDeltaR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetDijetDR"  , ";#Delta R(j_{1},j_{2})"  , nDRBins     , fDRMin     , fDRMax);

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

  hLdgTrijetTopMassWMassRatio    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetTopMassWMassRatio"   ,";R_{32}", 100 , 0.0, 10.0);
  hSubldgTrijetTopMassWMassRatio = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetTopMassWMassRatio",";R_{32}", 100 , 0.0, 10.0);

  hTopQuarkPt                   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopQuarkPt"                 , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTopQuarkPt_InTopDirBDT       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopQuarkPt_InTopDirBDT"      , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTopQuarkPt_InTopDir          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopQuarkPt_InTopDir"         , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetPt_BDT                 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetPt_BDT"               , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hAllTopQuarkPt_InTopDir       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AllTopQuarkPt_InTopDir"      , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTopQuarkPt_BDT               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopQuarkPt_BDT"             , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hAllTopQuarkPt_InTopDirBDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AllTopQuarkPt_InTopDirBDT"   , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hAllTopQuarkPt_Matched     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AllTopQuarkPt_Matched"   , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hAllTopQuarkPt_MatchedBDT  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AllTopQuarkPt_MatchedBDT", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);

  hLdgTrijetFake     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetFake"    ,";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hLdgTrijetFake_BDT = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetFake_BDT",";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);

  hBDTmultiplicity                           = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "BDTmultiplicity",";Trijet pass BDT mult", 50, 0, 50);
  hTrijetInTopDirNonMatched_Mass          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetInTopDirNonMatched_Mass"     ,";M (GeV/c^{2})", nTopMassBins, fTopMassMin, fTopMassMax/2);
  hTrijetInTopDir_Mass            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetInTopDir_Mass"     ,";M (GeV/c^{2})", nTopMassBins, fTopMassMin, fTopMassMax/2);
  hTrijetTopMatched_Mass       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetTopMatched_Mass"     ,";M (GeV/c^{2})", nTopMassBins, fTopMassMin, fTopMassMax/2);
  hInTopDirBDTmult                 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "InTopDirBDTmult",";truth matched Trijet pass BDT mult", 3, 0, 3);
  hMatchedBDTmult              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "MatchedBDTmult",";truth matched Trijet pass BDT mult", 3, 0, 3);
  hEventTrijetPt_BDT              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "EventTrijetPt_BDT"   ,";p_{T} (GeV/c)", 2*nPtBins     , fPtMin     , fPtMax);
  hEventTrijetPt_InTopDirBDT      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "EventTrijetPt_InTopDirBDT"   ,";p_{T} (GeV/c)", 2*nPtBins     , fPtMin     , fPtMax);

  hEventTrijetPt2T_BDT              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "EventTrijetPt2T_BDT"   ,";p_{T} (GeV/c)", 2*nPtBins     , fPtMin     , fPtMax);
  hEventTrijetPt2T_MatchedBDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "EventTrijetPt2T_MatchedBDT"   ,";p_{T} (GeV/c)", 2*nPtBins     , fPtMin     , fPtMax);

  hTrijetNotInTopDirPt        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetNotInTopDirPt"       ,";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetNotInTopDirPt_BDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetNotInTopDirPt_BDT"   ,";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetFakePt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetFakePt"    ,";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetFakePt_BDT = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetFakePt_BDT",";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hDeltaRMinTopTrijet  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "DeltaRMinTopTrijet" , ";#Delta R(top,trijet)", 60    , 0     , 1.5);

  hEventTrijetPt2T_Matched = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "EventTrijetPt2T_Matched", ";p_{T} (GeV/c)", 2*nPtBins   , fPtMin     , fPtMax);
  hAllTopQuarkPt_NotInTopDir   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AllTopQuarkPt_NotInTopDir"  ,";p_{T} (GeV/c)" , nPtBins     , fPtMin     , fPtMax);

  hEventTrijetPt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "EventTrijetPt"   ,";p_{T} (GeV/c)", 2*nPtBins, fPtMin, fPtMax);
  hEventTrijetPt2T  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "EventTrijetPt2T" ,";p_{T} (GeV/c)", 2*nPtBins, fPtMin, fPtMax);

  hRealSelectedTopMult =   fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "RealSelectedTopMult",";Selected truth matched Trijets", 3, 0, 3);

  hTrijetMultiplicity           = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetMultiplicity",";Trijet multiplicity", 670, 0, 670);
  hTrijetBDT_Mass               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetBDT_Mass"    ,";M (GeV/c^{2})", nTopMassBins, fTopMassMin, fTopMassMax);
  hTrijetMatched_BDTvalue    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetMatched_BDTvalue",";BDTG response"   , 40, -1.0, 1.0) ;
  hTrijetNonMatched_BDTvalue = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetNonMatched_BDTvalue",";BDTG response", 40, -1.0, 1.0) ;

  hNjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"JetMultiplicity",";Jet Multiplicity", 8,6,14);
  hDeltaMVAmax_MCtruth_SameObjFakes         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaMVAmax_MCtruth_SameObjFakes",";#Delta BDTG response", 100, -2., 2.) ;
  hAbsDeltaMVAmax_MCtruth_SameObjFakes      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"AbsDeltaMVAmax_MCtruth_SameObjFakes",";#Delta BDTG response", 50, 0, 2.) ;


  hFakeInTopDirMult     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "FakeInTopDirMult",";Fake Trijets in Top Direction mult", 670, 0, 670);;

  hDeltaMVAmax_MCtruth_SameObjFakesPassBDT = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaMVAmax_MCtruth_SameObjFakesPassBDT",";#Delta BDTG response", 100, -2., 2.);
  hDeltaMVAmin_MCtruth_SameObjFakes        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaMVAmin_MCtruth_SameObjFakes",";#Delta BDTG response", 100, -2., 2.) ;
  hDeltaMVAmin_MCtruth_SameObjFakesPassBDT = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaMVAmin_MCtruth_SameObjFakesPassBDT",";#Delta BDTG response", 100, -2., 2.) ;
  hMatchedTrijetMult_JetsGT9               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "MatchedTrijetMult_JetsGT9",";Trijet Multiplicity", 3, 0, 3);
  hMatchedTrijetMult_JetsInc               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "MatchedTrijetMult_JetsInc",";Trijet Multiplicity", 3, 0, 3);
  hMVAvalue_DeltaMVAgt1                    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"MVAvalue_DeltaMVAgt1",";BDTG response", 40, -1., 1.) ;
  hMatchedPassBDTmult_SameObjFakes         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "MatchedPassBDTmult_SameObjFakes",";Selected truth matched Trijets", 3, 0, 3);

  hAllTrijetPassBDT_pt              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AllTrijetPassBDT_pt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hAllTrijetPassBDTbPassCSV_pt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AllTrijetPassBDTbPassCSV_pt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hTrijetPassBDT_bDisc              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetPassBDT_bDisc",";b-tag discr." , nBDiscBins  , fBDiscMin  , fBDiscMax);
  
  hTrijetPtMaxMVASameFakeObj_BjetPassCSV = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetPtMaxMVASameFakeObj_BjetPassCSV"    ,";p_{T} (GeV/c)"      , nPtBins     , fPtMin     , fPtMax);
  hTrijetPtMaxMVASameFakeObj             = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetPtMaxMVASameFakeObj"    ,";p_{T} (GeV/c)"      , nPtBins     , fPtMin     , fPtMax);

  hChHiggsBjetPt_TetrajetBjetMatched     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "ChHiggsBjetPt_TetrajetBjetPt_Matched"    ,";p_{T} (GeV/c)"      , nPtBins*4     , fPtMin , fPtMax*4);
  hChHiggsBjetPt_foundTetrajetBjet       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "ChHiggsBjetPt_foundTetrajetBjet"    ,";p_{T} (GeV/c)"      , nPtBins*4     , fPtMin     , fPtMax*4);

  hHiggsBjetPt                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "HiggsBjetPt"    ,";p_{T} (GeV/c)"      , nPtBins*4     , fPtMin     , fPtMax*4);
  hHiggsBjetPt_LdgBjetMatched = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "HiggsBjetPt_LdgBjetMatched"    ,";p_{T} (GeV/c)"      , nPtBins*4     , fPtMin     , fPtMax*4);
  hLdgBjetPt                  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"LdgBjetPt",";p_{T} (GeVc^{-1})",nPtBins*4     , fPtMin     , fPtMax*4);
  hLdgBjetPt_isLdgFreeBjet    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"LdgBjetPt_isLdgFreeBjet",";p_{T} (GeVc^{-1})",nPtBins*4     , fPtMin     , fPtMax*4);

  hNSelectedTrijets =   fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "NSelectedTrijets",";Number of Selected Trijets", 3, 0, 3);
  hTopFromHiggsPt_isLdgMVATrijet       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"TopFromHiggsPt_isLdgMVATrijet",";p_{T} (GeVc^{-1})",nPtBins*4     , fPtMin     , fPtMax*4);
  hTopFromHiggsPt_isSubldgMVATrijet    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"TopFromHiggsPt_isSubldgMVATrijet",";p_{T} (GeVc^{-1})",nPtBins*4     , fPtMin     , fPtMax*4);
  hTopFromHiggsPt_isMVATrijet          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"TopFromHiggsPt_isMVATrijet",";p_{T} (GeVc^{-1})",nPtBins*4     , fPtMin     , fPtMax*4);

  hDeltaPtOverPt_TopFromH_LdgMVATrijet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaPtOverPt_TopFromH_LdgMVATrijet","#;Delta P_{T}/P_{T}", nPtBins     ,-fPtMax/40.  , fPtMax/40.);
  hDeltaEta_TopFromH_LdgMVATrijet      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaEta_TopFromH_LdgMVATrijet",";#Delta #eta", nDEtaBins, -fDEtaMax/4., fDEtaMax/4.);
  hDeltaPhi_TopFromH_LdgMVATrijet      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaPhi_TopFromH_LdgMVATrijet",";#Delta #phi", 2*nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaR_TopFromH_LdgMVATrijet        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaR_TopFromH_LdgMVATrijet",";#Delta R", nDRBins, fDRMin, fDRMax);

  hDeltaPtOverPt_TopFromH_SubldgMVATrijet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaPtOverPt_TopFromH_SubldgMVATrijet","#;Delta P_{T}/P_{T}", nPtBins     ,-fPtMax/40.  , fPtMax/40.);
  hDeltaEta_TopFromH_SubldgMVATrijet      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaEta_TopFromH_SubldgMVATrijet",";#Delta #eta", nDEtaBins, -fDEtaMax/4., fDEtaMax/4.);
  hDeltaPhi_TopFromH_SubldgMVATrijet      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaPhi_TopFromH_SubldgMVATrijet",";#Delta #phi", 2*nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaR_TopFromH_SubldgMVATrijet        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaR_TopFromH_SubldgMVATrijet",";#Delta R", nDRBins, fDRMin, fDRMax);

  hTopFromHiggsPt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"TopFromHiggsPt",";p_{T} (GeVc^{-1})",nPtBins*4     , fPtMin     , fPtMax*4);


  //===
  hChHiggsBjetPt_TetrajetBjetMatched_afterCuts     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "ChHiggsBjetPt_TetrajetBjetPt_Matched_afterCuts"    ,";p_{T} (GeV/c)"      , nPtBins*4     , fPtMin , fPtMax*4);
  hChHiggsBjetPt_foundTetrajetBjet_afterCuts       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "ChHiggsBjetPt_foundTetrajetBjet_afterCuts"    ,";p_{T} (GeV/c)"      , nPtBins*4     , fPtMin     , fPtMax*4);

  hHiggsBjetPt_afterCuts                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "HiggsBjetPt_afterCuts"    ,";p_{T} (GeV/c)"      , nPtBins*4     , fPtMin     , fPtMax*4);
  hHiggsBjetPt_LdgBjetMatched_afterCuts = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "HiggsBjetPt_LdgBjetMatched_afterCuts"    ,";p_{T} (GeV/c)"      , nPtBins*4     , fPtMin     , fPtMax*4);
  hLdgBjetPt_afterCuts                  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"LdgBjetPt_afterCuts",";p_{T} (GeVc^{-1})",nPtBins*4     , fPtMin     , fPtMax*4);
  hLdgBjetPt_isLdgFreeBjet_afterCuts    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"LdgBjetPt_isLdgFreeBjet_afterCuts",";p_{T} (GeVc^{-1})",nPtBins*4     , fPtMin     , fPtMax*4);

  hTopFromHiggsPt_isLdgMVATrijet_afterCuts       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"TopFromHiggsPt_isLdgMVATrijet_afterCuts",";p_{T} (GeVc^{-1})",nPtBins*4     , fPtMin     , fPtMax*4);
  hTopFromHiggsPt_isSubldgMVATrijet_afterCuts    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"TopFromHiggsPt_isSubldgMVATrijet_afterCuts",";p_{T} (GeVc^{-1})",nPtBins*4     , fPtMin     , fPtMax*4);
  hTopFromHiggsPt_isMVATrijet_afterCuts          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"TopFromHiggsPt_isMVATrijet_afterCuts",";p_{T} (GeVc^{-1})",nPtBins*4     , fPtMin     , fPtMax*4);

  hDeltaPtOverPt_TopFromH_LdgMVATrijet_afterCuts = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaPtOverPt_TopFromH_LdgMVATrijet_afterCuts","#;Delta P_{T}/P_{T}", nPtBins     ,-fPtMax/40.  , fPtMax/40.);
  hDeltaEta_TopFromH_LdgMVATrijet_afterCuts      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaEta_TopFromH_LdgMVATrijet_afterCuts",";#Delta #eta", nDEtaBins, -fDEtaMax/4., fDEtaMax/4.);
  hDeltaPhi_TopFromH_LdgMVATrijet_afterCuts      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaPhi_TopFromH_LdgMVATrijet_afterCuts",";#Delta #phi", 2*nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaR_TopFromH_LdgMVATrijet_afterCuts        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaR_TopFromH_LdgMVATrijet_afterCuts",";#Delta R", nDRBins, fDRMin, fDRMax);

  hDeltaPtOverPt_TopFromH_SubldgMVATrijet_afterCuts = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaPtOverPt_TopFromH_SubldgMVATrijet_afterCuts","#;Delta P_{T}/P_{T}", nPtBins,-fPtMax/40., fPtMax/40.);
  hDeltaEta_TopFromH_SubldgMVATrijet_afterCuts      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaEta_TopFromH_SubldgMVATrijet_afterCuts",";#Delta #eta", nDEtaBins, -fDEtaMax/4., fDEtaMax/4.);
  hDeltaPhi_TopFromH_SubldgMVATrijet_afterCuts      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaPhi_TopFromH_SubldgMVATrijet_afterCuts",";#Delta #phi", 2*nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaR_TopFromH_SubldgMVATrijet_afterCuts        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaR_TopFromH_SubldgMVATrije_afterCuts",";#Delta R", nDRBins, fDRMin, fDRMax);

  hTopFromHiggsPt_afterCuts                         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"TopFromHiggsPt_afterCuts",";p_{T} (GeVc^{-1})",nPtBins*4     , fPtMin     , fPtMax*4);
  hDeltaCSV_TopFromHBJet_LdgMVATrijetBjet_afterCuts = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaCSV_TopFromHBJet_LdgMVATrijetBjet_afterCuts",";#Delta b-tag discr", 100, -2, 2);
  hDeltaBDT_TopFromH_LdgMVATrijet_afterCuts         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaBDT_TopFromH_LdgMVATrijet_afterCuts",";#Delta BDT", 100, -2,2);

  hDeltaCSV_TopFromHBJet_SubldgMVATrijetBjet_afterCuts = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaCSV_TopFromH_SubldgMVATrijet_afterCuts",";#Delta b-tag discr", 100, -2,2);
  hDeltaBDT_TopFromH_SubldgMVATrijet_afterCuts         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaBDT_TopFromH_SubldgMVATrijet_afterCuts",";#Delta BDT", 100, -2,2);

  hDeltaPtOverPt_HiggsBjetPt_TetrajetBjetMatched_afterCuts =fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaPtOverPt_HiggsBjetPt_TetrajetBjetMatched_afterCuts","#;Delta P_{T}/P_{T}", nPtBins, -fPtMax/40., fPtMax/40.);
  hDeltaEta_HiggsBjetPt_TetrajetBjetMatched_afterCuts  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaEta_HiggsBjetPt_TetrajetBjetMatched_afterCuts",";#Delta #eta", nDEtaBins, -fDEtaMax/4., fDEtaMax/4.);
  hDeltaPhi_HiggsBjetPt_TetrajetBjetMatched_afterCuts = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaPhi_HiggsBjetPt_TetrajetBjetMatched_afterCuts",";#Delta #phi", 2*nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaR_HiggsBjetPt_TetrajetBjetMatched_afterCuts   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaR_HiggsBjetPt_TetrajetBjetMatched_afterCuts",";#Delta R", nDRBins, fDRMin, fDRMax);
  hDeltaCSV_HiggsBjetPt_TetrajetBjetMatched_afterCuts = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaCSV_HiggsBjetPt_TetrajetBjetMatched_afterCuts",";#Delta b-tag discr", 100, -2, 2);

  //===
  hSelectedTrijetsPt_BjetPassCSVdisc_afterCuts   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SelectedTrijetsPt_BjetPassCSVdisc_afterCuts", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hSelectedTrijetsPt_afterCuts                   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SelectedTrijetsPt_afterCuts", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetPt_PassBDT_BJetPassCSV                  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetPt_PassBDT_BJetPassCSV", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetPt_PassBDT                              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetPt_PassBDT", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);

  // Histograms (2D) 
  hTrijetCountForBDTcuts           = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "TrijetCountVsBDTcuts",             ";BDT cut value;Trijet multiplicity", 19, -0.95,0.95, 200,0,200);
  hNjetsVsNTrijets_beforeBDT       = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "NjetsVsNTrijets_beforeBDT"  ,      ";Jet Multiplicity;Trijets_beforeBDT multiplicity", 8,6,14, 670, 0, 670);
  hNjetsVsNTrijets_afterBDT        = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "NjetsVsNTrijets_afterBDT"  ,       ";Jet Multiplicity;Trijets_afterBDT multiplicity", 8,6,14, 60, 0, 60);
  hDeltaMVAmaxVsTrijetPassBDTvalue = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "DeltaBDTmaxVsTrijetPassBDTvalue", ";#Delta BDTG_{max} response;BDTG response", 100, -2., 2., 40, -1., 1.) ;
  hDeltaMVAminVsTrijetPassBDTvalue = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "DeltaBDTminVsTrijetPassBDTvalue", ";#Delta BDTG_{min} response;BDTG response", 100, -2., 2., 40, -1., 1.) ;
  hFakeTrijetMassVsBDTvalue        = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "FakeTrijetMassVsBDTvalue",";Fake Trijets M (GeVc^{-2}); BDTG response", nTopMassBins, fTopMassMin, fTopMassMax, 40, -1., 1.);

  hTopFromHiggsPtVSAssocTopPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "TopFromHiggsPtVSAssocTopPt", ";p_{T}^{t^{H}} (GeV/c);p_{T}^{t^{Assoc}} (GeV/c)",nPtBins, fPtMin, fPtMax, nPtBins, fPtMin, fPtMax);

  DEta_Trijet1TetrajetBjet_Vs_DEta_Trijet2TetrajetBjet  = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "DEta_Trijet1TetrajetBjet_Vs_DEta_Trijet2TetrajetBjet",
										     ";#Delta#eta(Trijet^{1BDT},Bjet^{ldg}_{free});#Delta#eta(Trijet^{2BDT},Bjet^{ldg}_{free})", 
										     nDEtaBins, fDEtaMin, fDEtaMax, nDEtaBins, fDEtaMin, fDEtaMax);
  DPhi_Trijet1TetrajetBjet_Vs_DPhi_Trijet2TetrajetBjet  = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "DPhi_Trijet1TetrajetBjet_Vs_DPhi_Trijet2TetrajetBjet",
										     ";#Delta#phi(Trijet^{1BDT},Bjet^{ldg}_{free});#Delta#phi(Trijet^{2BDT},Bjet^{ldg}_{free})", 
										     nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);
  DR_Trijet1TetrajetBjet_Vs_DR_Trijet2TetrajetBjet      = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "DR_Trijet1TetrajetBjet_Vs_DR_Trijet2TetrajetBjet",
										     ";#Delta R(Trijet^{1BDT},Bjet^{ldg}_{free});#Delta R(Trijet^{2BDT},Bjet^{ldg}_{free})",
										     nDRBins, fDRMin, fDRMax, nDRBins, fDRMin, fDRMax);
  DEta_TopFromHBjetFromH_Vs_DEta_AssocTopBjetFromH      = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "DEta_TopFromHBjetFromH_Vs_DEta_AssocTopBjetFromH",
										     ";#Delta#eta(Top^{H},Bjet^{H});#Delta#eta(Top^{Assoc},Bjet^{H})",
										     nDEtaBins, fDEtaMin, fDEtaMax, nDEtaBins, fDEtaMin, fDEtaMax);
  DPhi_TopFromHBjetFromH_Vs_DPhi_AssocTopBjetFromH      = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "DPhi_TopFromHBjetFromH_Vs_DPhi_AssocTopBjetFromH",
                                                                                     ";#Delta#phi(Top^{H},Bjet^{H});#Delta#phi(Top^{Assoc},Bjet^{H})",
										     nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);

  DR_TopFromHBjetFromH_Vs_DR_AssocTopBjetFromH          = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "DR_TopFromHBjetFromH_Vs_DR_AssocTopBjetFromH",
                                                                                     ";#Delta R(Top^{H},Bjet^{H});#Delta R(Top^{Assoc},Bjet^{H})",
										     nDRBins, fDRMin, fDRMax, nDRBins, fDRMin, fDRMax);
  return;
}

TopSelectionBDT::Data TopSelectionBDT::silentAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData, const bool doMatching) {
  ensureSilentAnalyzeAllowed(event.eventID());

  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, jetData.getSelectedJets(), bjetData.getSelectedBJets(), doMatching);
  enableHistogramsAndCounters();
  return myData;
}


TopSelectionBDT::Data TopSelectionBDT::silentAnalyzeWithoutBJets(const Event& event, 
								 const JetSelection::Data& jetData,
								 const BJetSelection::Data& bjetData,
								 bool doMatching,
								 const std::string failedBJetsSortType) {
  ensureSilentAnalyzeAllowed(event.eventID());
  
  // Disable histogram filling and counter
  disableHistogramsAndCounters();  
  
  // Ready to analyze 
  Data data = privateAnalyze(event, jetData.getSelectedJets(), GetBjetsToBeUsedInFit(bjetData, cfg_NBjetsMax, failedBJetsSortType), doMatching);
  
  // Save the failed bjets used in the top fit (only the failed (inverted) bjets)
  data.fFailedBJetsUsedAsBJetsInFit = GetFailedBJetsUsedAsBJetsInFit();

  // Re-enable histogram filling and counter
  enableHistogramsAndCounters();
  return data;
}

TopSelectionBDT::Data TopSelectionBDT::analyzeWithoutBJets(const Event& event, 
							   const JetSelection::Data& jetData,
							   const BJetSelection::Data& bjetData,
							   bool doMatching,
							   const std::string failedBJetsSortType) {
  ensureSilentAnalyzeAllowed(event.eventID());

  // Ready to analyze 
  Data data = privateAnalyze(event, jetData.getSelectedJets(), GetBjetsToBeUsedInFit(bjetData, cfg_NBjetsMax, failedBJetsSortType), doMatching);

  // Save the failed bjets used in the top fit (only the failed (inverted) bjets)
  data.fFailedBJetsUsedAsBJetsInFit = GetFailedBJetsUsedAsBJetsInFit();
  
  // Re-enable histogram filling and counter
  enableHistogramsAndCounters();
  return data;
}


TopSelectionBDT::Data TopSelectionBDT::analyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData, const bool doMatching) {
  ensureAnalyzeAllowed(event.eventID());

  // Ready to analyze
  TopSelectionBDT::Data data = privateAnalyze(event, jetData.getSelectedJets(), bjetData.getSelectedBJets(), doMatching);

  // Send data to CommonPlots
  // if (fCommonPlots != nullptr) fCommonPlots->fillControlPlotsAtTopSelectionBDT(event, data); //fixme
  return data;
}


//alex

//alex

TopSelectionBDT::Data TopSelectionBDT::privateAnalyze(const Event& event, const std::vector<Jet> selectedJets, const std::vector<Jet> selectedBjets, bool doMatching) {
  if (0) std::cout << "=== TopSelectionBDT::privateAnalyze()" << std::endl;
  Data output;
  cSubAll.increment();
  
  // Sanity check
  if (selectedBjets.size() < 3) return output;

  // In order to replace PF Jets with GenJets event must be MC and user must enable the dedicated flag
  bool replaceJets = event.isMC()*cfg_ReplaceJetsWithGenJets; // fixme - not tested

  // Only resize if their size exceeds max allowed value
  std::vector<Jet> jets  = selectedJets;
  std::vector<Jet> bjets = selectedBjets;
  if (jets.size() > cfg_NjetsMax)  jets.resize(cfg_NjetsMax);
  if (bjets.size() > cfg_NBjetsMax) bjets.resize(cfg_NBjetsMax);
  
  if (0) std::cout << "\nnJets = " << jets.size() << ", \033[1;31mnBJets = " << bjets.size() << "\033[0m" << std::endl;
  hNjets -> Fill(jets.size());


  //================================================================================================  
  // MC Matching  
  //================================================================================================

  std::vector<genParticle> GenChargedHiggs;
  std::vector<genParticle> GenChargedHiggs_BQuark;
  std::vector<genParticle> GenTops;
  std::vector<genParticle> GenTops_BQuark;
  std::vector<genParticle> GenTops_SubldgQuark;
  std::vector<genParticle> GenTops_LdgQuark;

  vector <Jet> MCtrue_LdgJet, MCtrue_SubldgJet, MCtrue_Bjet, MC_BJets;
  vector <Jet> MCtrueTopFromH_LdgJet, MCtrueTopFromH_SubldgJet, MCtrueTopFromH_Bjet, MCtrue_ChargedHiggsBjet, MCtrue_TopJets;
  vector <Jet> MCtrueAssocTop_LdgJet, MCtrueAssocTop_SubldgJet, MCtrueAssocTop_Bjet;
  std::vector<bool> FoundTop;

  if (event.isMC()){
    
    int nGenuineTops = 0;
    GenTops = GetGenParticles(event.genparticles().getGenParticles(), 6);
    
    // For-loop: All top quarks
    for (auto& top: GenTops){

      bool FoundBQuark = false;
      std::vector<genParticle> quarks;
      genParticle bquark;
      // For-loop: Top quark daughters (Nested)
      for (size_t i=0; i<top.daughters().size(); i++)
	{
	  
	  int dau_index = top.daughters().at(i);
	  genParticle dau = event.genparticles().getGenParticles()[dau_index];
	  
	  // B-Quark
	  if (std::abs(dau.pdgId()) ==  5)
	    {
	      bquark = dau;
	      FoundBQuark = true;
	    }
	  
	  // W-Boson
	  if (std::abs(dau.pdgId()) == 24)
	    {
	      
	      // Get the last copy
	      genParticle W = GetLastCopy(event.genparticles().getGenParticles(), dau);
	      
	      // For-loop: W-boson daughters
	      for (size_t idau=0; idau<W.daughters().size(); idau++)
		{		
		  // Find the decay products of W-boson
		  int Wdau_index = W.daughters().at(idau);
		  genParticle Wdau = event.genparticles().getGenParticles()[Wdau_index];
		  
		  // Consider only quarks as decaying products
		  if (std::abs(Wdau.pdgId()) > 5) continue;
		  
		  // Save daughter
		  quarks.push_back(Wdau);
		}//W-boson daughters
	    }//W-boson
	}//Top-quark daughters
    
      // Skip top if b-quark is not found (i.e. top decays to W and c)
      if (!FoundBQuark) continue;

      // Skip top if it decays leptonically (the "quarks" vector will be empty causing errors)
      if (quarks.size() < 2) continue;

      // Fill vectors for b-quarks, leading and subleading quarks coming from tops 
      GenTops_BQuark.push_back(bquark);
      
      if (quarks.at(0).pt() > quarks.at(1).pt())
        {
          GenTops_LdgQuark.push_back(quarks.at(0));
          GenTops_SubldgQuark.push_back(quarks.at(1));
        }
      else
        {
          GenTops_LdgQuark.push_back(quarks.at(1));
          GenTops_SubldgQuark.push_back(quarks.at(0));
        }

    } // For-Loop over top quarks
    
    // Debugging
    if(0)
      {
	std::cout << "GenTops_BQuark size      =" << GenTops_BQuark.size()      <<std::endl;
	std::cout << "GenTops_LdgQuark size    =" << GenTops_LdgQuark.size()    <<std::endl;
	std::cout << "GenTops_SubldgQuark size =" << GenTops_SubldgQuark.size() <<std::endl; 
      }

    GenChargedHiggs = GetGenParticles(event.genparticles().getGenParticles(), 37);

    //Match bjet from Higgs 
    // For-loop: All top quarks             
    for (auto& hplus: GenChargedHiggs)
      {
        genParticle bquark;
        // For-loop: Top quark daughters (Nested)                        
	for (size_t i=0; i<hplus.daughters().size(); i++)
          {
            int dau_index = hplus.daughters().at(i);
            genParticle dau = event.genparticles().getGenParticles()[dau_index];
            // B-Quark                                   
	    if (std::abs(dau.pdgId()) ==  5) GenChargedHiggs_BQuark.push_back(dau);
          }
      }
    // Debugging                      
    if(0)
      {
	std::cout<<"GenChargedHiggs        "<<GenChargedHiggs.size()<<std::endl;
	std::cout<<"GenChargedHiggs_BQuark "<<GenChargedHiggs_BQuark.size()<<std::endl;
      }

    // Skip matcing if top does not decay to b
    if (doMatching) doMatching = (GenTops_BQuark.size() == GenTops.size()); 

    // Matching criteria: Quarks-Jets matching with DR and DPt criteria
    if (doMatching)
      {
      
	// ======= B jet matching (Loop over all Jets)
	vector <genParticle> MGen_LdgJet, MGen_SubldgJet, MGen_Bjet;
	vector <double> dRminB;
	Jet firstBjet;

	// For-loop: All top-quarks
	for (size_t i=0; i<GenTops.size(); i++)
	  {
	    genParticle BQuark = GenTops_BQuark.at(i);
	    Jet mcMatched_BJet;
	    double dRmin  = 99999.9;
	    double dPtmin = 99999.9;
	    
	    // For-loop: All selected jets
	    for (auto& bjet: jets)
	      {
		double dR  = ROOT::Math::VectorUtil::DeltaR( bjet.p4(), BQuark.p4());
		double dPt = std::abs(bjet.pt() - BQuark.pt());
		
		// Only consider dR < 0.4
		if (dR > 0.4) continue;
		
		// Find minimum dR
		if (dR > dRmin) continue;
		
		// Find minimum dPt
		if (dPt > dPtmin) continue;
		
		// Store values
		dRmin  = dR;
		dPtmin = dPt;
		mcMatched_BJet = bjet;
	      }// For-loop: selected jets
	    
	    // Store match
	    dRminB.push_back(dRmin);
	    MC_BJets.push_back(mcMatched_BJet);
	    
	  }// For-loop: All top-quarks
	
	
	//======= Dijet matching (Loop over all Jets)

	//======= For-loop: All top-quarks
	for (size_t i=0; i<GenTops.size(); i++)
	  {

	    genParticle top = GenTops.at(i);
	    genParticle LdgQuark    = GenTops_LdgQuark.at(i);
	    genParticle SubldgQuark = GenTops_SubldgQuark.at(i);
	    
	    Jet mcMatched_LdgJet;
	    Jet mcMatched_SubldgJet;
	    
	    double dR1min, dR2min, dPt1min, dPt2min;
	    dR1min = dR2min = dPt1min = dPt2min = 99999.9;
	    
	    // For-loop: All selected jets
	    for (auto& jet: jets)
	      {
		
		// For-loop: All top-quarks
		for (size_t k=0; k<GenTops.size(); k++)
		  {
		    if (dRminB.at(k) < 0.4)
		      {
			// Skip the jets that are matched with bquarks
			if( areSameJets(jet,MC_BJets.at(k))) continue;
		      }
		  }// For-loop: All top-quarks
		
		// Find dR for the two jets in top-decay dijet
		double dR1 = ROOT::Math::VectorUtil::DeltaR(jet.p4(), LdgQuark.p4());
		double dR2 = ROOT::Math::VectorUtil::DeltaR(jet.p4(), SubldgQuark.p4());
		
		// Require both jets to be within dR <= 0.4
		if (std::min(dR1, dR2) > 0.4) continue;
	    
		// Calculate dPt for each jet in top-decay dijet
		double dPt1 = std::abs(jet.pt() - LdgQuark.pt());
		double dPt2 = std::abs(jet.pt() - SubldgQuark.pt());
		
		// Find which of the two is the correct match
		if (dR1 < dR2)
		  {
		    // Is Jet1 closer in eta-phi AND has smaller pT difference?
		    if (dR1 < dR1min && dPt1 < dPt1min)
		      {
			dR1min = dR1;
			dPt1min= dPt1;
			mcMatched_LdgJet = jet;
		      }
		    // Is Jet2 closer in eta-phi AND has smaller pT difference?
		    else if (dR2 <= 0.4 && dR2 < dR2min && dPt2 < dPt2min)
		      {
			dR2min  = dR2;
			dPt2min = dPt2;
			mcMatched_SubldgJet = jet;
		      }
		  }
		else
		  {
		    // Is Jet2 closer in eta-phi AND has smaller pT difference?
		    if (dR2 < dR2min && dPt2 < dPt2min)
		      {
			dR2min  = dR2;
			dPt2min = dPt2;
			mcMatched_SubldgJet = jet;
		      }
		    // Is Jet2 closer in eta-phi AND has smaller pT difference?
		    else if (dR1 <= 0.4 && dR1 < dR1min && dPt1 < dPt1min)
		      {
			dR1min  = dR1;
			dPt1min = dPt1;
			mcMatched_LdgJet = jet;
		      }
		  }
	      }//For-loop: All selected jets
	    
	    // Check if TOP is genuine
	    bool isGenuine = (dR1min<= 0.4 && dR2min <= 0.4 && dRminB.at(i) <= 0.4);

	    if (isGenuine)
	      {
		// Increase the counter of genuine tops            
		nGenuineTops++;                                                                                                         
		MCtrue_LdgJet.push_back(mcMatched_LdgJet);
		MCtrue_SubldgJet.push_back(mcMatched_SubldgJet);
		MCtrue_Bjet.push_back(MC_BJets.at(i));
		MGen_LdgJet.push_back(GenTops_LdgQuark.at(i));
		MGen_SubldgJet.push_back(GenTops_SubldgQuark.at(i));
		MGen_Bjet.push_back(GenTops_BQuark.at(i));
		

		if (HasMother(event, top, 37))
		  {
		    //decay products (jets) of H+ top
		    MCtrueTopFromH_LdgJet.push_back(mcMatched_LdgJet);
		    MCtrueTopFromH_SubldgJet.push_back(mcMatched_SubldgJet);
		    MCtrueTopFromH_Bjet.push_back(MC_BJets.at(i));
		  }
		else
		  {
		    //decay products (jets) of associated top
		    MCtrueAssocTop_LdgJet.push_back(mcMatched_LdgJet);
		    MCtrueAssocTop_SubldgJet.push_back(mcMatched_SubldgJet);
		    MCtrueAssocTop_Bjet.push_back(MC_BJets.at(i));
		  }
	      }// if (isGenuine)
	    
	    // Top quark matched with a trijet
	    FoundTop.push_back(isGenuine);
	  }//For-loop: All top-quarks
        //BJet from Higgs-side                                                                                             
        for (size_t i=0; i<GenChargedHiggs_BQuark.size(); i++)
          {
            double dRmin = 999.999;
            Jet mcMatched_ChargedHiggsBjet;
            for (auto& jet: jets)
              {
                for (auto& topJet: MCtrue_TopJets) if (areSameJets(jet, topJet)) continue;
                double dR_Hb = ROOT::Math::VectorUtil::DeltaR(jet.p4(),GenChargedHiggs_BQuark.at(i).p4());
                if (dR_Hb > 0.4 || dR_Hb > dRmin) continue;
                dRmin = dR_Hb;
                mcMatched_ChargedHiggsBjet = jet;
              }
            if (dRmin <= 0.4) MCtrue_ChargedHiggsBjet.push_back(mcMatched_ChargedHiggsBjet);
          }

      }// if (doMatching){
  }// event.isMC()
  if (0)
    {
      std::cout<<"==="<<std::endl;
      std::cout<<"MCtrueAssocTop_LdgJet.size() "<<MCtrueAssocTop_LdgJet.size()<<std::endl;
      std::cout<<"MCtrueTopFromH_LdgJet.size() "<<MCtrueTopFromH_LdgJet.size()<<std::endl;
    }
  //================================================================================================  
  // Top Candidates
  //================================================================================================  
  // Array with 19 different BDT cut values (later use)
  vector<int> mva;
  vector<float> mvaCut;
  float cut = -0.9;
 
  // For-loop: All BDT cut values
  for (int k=0; k<19; k++)
    {
      mva.push_back(0);
      mvaCut.push_back(cut);
      cut = cut + 0.1;
    }// fixme: convert to vector

  // Definitions
  TrijetSelection TopCand;
  int NpassBDT = 0;  
  int indexb = 0;

  // For-loop: All jets (1)
  for (auto& bjet: jets)
    {
      indexb++;
      int index1 = 0;
      
      // For-loop: All jets (Nested)
      for (auto& jet1: jets)
	{
	  index1++;
	  int index2 = 0;
	  
	  // Skip if jet1 is same as bjet
	  if (areSameJets(jet1, bjet)) continue;

	  // For-loop: All jets (Doubly-Nested)
	  for (auto& jet2: jets)
	    {
	      index2++;

	      // Do not consider duplicate compinations
	      if (index2 < index1) continue;

	      // Skip if jet2 is same as jet1, or jet2 same as bjet
	      if (areSameJets(jet2,  jet1)) continue;
	      if (areSameJets(jet2,  bjet)) continue;
	      
	      // Get 4-momentum of top (trijet) and W (dijet)
	      math::XYZTLorentzVector Trijet_p4, Dijet_p4;
	      Trijet_p4 = bjet.p4() + jet1.p4() + jet2.p4();
	      Dijet_p4  = jet1.p4() + jet2.p4();
	      
	      //	      if(Trijet_p4.M() > 400) continue; //fixme
	      if (!cfg_MassCut.passedCut(Trijet_p4.M())) continue;
	      if (!cfg_CSV_bDiscCut.passedCut(bjet.bjetDiscriminator())) continue;

	      // Calculate variables
	      double dr_sd = ROOT::Math::VectorUtil::DeltaR( jet1.p4(), jet2.p4());
	      double softDrop_n2 = min(jet2.pt(), jet1.pt()) / ( (jet2.pt() + jet1.pt()) * dr_sd * dr_sd);

	      // Calculate our 19 discriminating variables for MVA use
	      TrijetPtDR                  = Trijet_p4.Pt() * ROOT::Math::VectorUtil::DeltaR( Dijet_p4  , bjet.p4() );
	      TrijetDijetPtDR             = Dijet_p4.Pt()  * ROOT::Math::VectorUtil::DeltaR( jet1.p4() , jet2.p4() );
	      TrijetBjetMass              = bjet.p4().M();
	      TrijetLdgJetBDisc           = jet1.bjetDiscriminator();
	      TrijetSubldgJetBDisc        = jet2.bjetDiscriminator();
	      TrijetBJetLdgJetMass        = (bjet.p4() + jet1.p4()).M();
	      TrijetBJetSubldgJetMass     = (bjet.p4() + jet2.p4()).M();
	      TrijetMass                  = Trijet_p4.M();
	      TrijetDijetMass             = Dijet_p4.M();
	      TrijetBJetBDisc             = bjet.bjetDiscriminator();
	      TrijetSoftDrop_n2           = softDrop_n2;
	      TrijetLdgJetCvsL            = jet1.pfCombinedCvsLJetTags();
	      TrijetSubldgJetCvsL         = jet2.pfCombinedCvsLJetTags();
	      TrijetLdgJetPtD             = jet1.QGTaggerAK4PFCHSptD();
	      TrijetSubldgJetPtD          = jet2.QGTaggerAK4PFCHSptD();
	      TrijetLdgJetAxis2           = jet1.QGTaggerAK4PFCHSaxis2();
	      TrijetSubldgJetAxis2        = jet2.QGTaggerAK4PFCHSaxis2();
	      TrijetLdgJetMult            = jet1.QGTaggerAK4PFCHSmult();
	      TrijetSubldgJetMult         = jet2.QGTaggerAK4PFCHSmult();
	      // TrijetLdgJetQGLikelihood    = jet1.QGTaggerAK4PFCHSqgLikelihood();
	      // TrijetSubldgJetQGLikelihood = jet2.QGTaggerAK4PFCHSqgLikelihood();

	      // Evaluate the MVA discriminator value
	      float MVAoutput = reader->EvaluateMVA("BTDG method");

	      // Fill top candidate BDT values
	      hBDTresponse -> Fill(MVAoutput);
	      TopCand.MVA.push_back(MVAoutput);
	      TopCand.TrijetP4.push_back(Trijet_p4);
	      TopCand.DijetP4.push_back(Dijet_p4);
	      TopCand.Jet1.push_back(getLeadingSubleadingJet(jet1,jet2,"leading"));
	      TopCand.Jet2.push_back(getLeadingSubleadingJet(jet1,jet2,"subleading"));
	      TopCand.BJet.push_back(bjet);

	      if (cfg_MVACut.passedCut(MVAoutput))
		{
		  NpassBDT++; 
		  hTrijetBDT_Mass -> Fill(Trijet_p4.M());
		}
	      // Determine top candidate multiplicity after BDT cut
	      for (int m=0; m<19; m++) 
		{
		  if (MVAoutput > mvaCut.at(m)) mva.at(m) ++; 
		}
	    }// For-loop: All jets (Doubly-Nested)
	}// For-loop: All jets (Nested)
    }// For-loop: All jets


  TopCand = SortInMVAvalue(TopCand);

  // Fill Number of trijets passing BDT vs MVA cut value
  for (size_t m=0; m < mvaCut.size(); m++) hTrijetCountForBDTcuts -> Fill(mvaCut.at(m), mva.at(m));
  

  if (0) std::cout<<"Number of Top Candidates: "<<TopCand.MVA.size()<<std::endl;
  // Definitions
  float MVAmax1 = -999.999,  MVAmax2 = -999.999;
  Jet trijet1Jet1, trijet1Jet2, trijet1BJet;
  Jet trijet2Jet1, trijet2Jet2, trijet2BJet;
  math::XYZTLorentzVector trijet1, trijet2;
  Jet leadingTrijetJet1, leadingTrijetJet2, leadingTrijetBJet;
  Jet subleadingTrijetJet1, subleadingTrijetJet2, subleadingTrijetBJet;
  math::XYZTLorentzVector leadingTrijetP4, subleadingTrijetP4, tetrajetP4;
  float leadingTrijetMVA, subleadingTrijetMVA;

  std::vector<int> TrijetSelection_index;  //vector with indices of two tops with highest BDT value

  bool foundTrijet1 = false;
  

  for (size_t i=0; i<TopCand.MVA.size(); i++)
    {
      if ( (size_t)(isBJet(TopCand.Jet1.at(i),bjets) + isBJet(TopCand.Jet2.at(i),bjets) + isBJet(TopCand.BJet.at(i),bjets)) ==  bjets.size()) continue;

      // Store new max
      MVAmax1 = TopCand.MVA.at(i);
      
      // Save top candidate subjetss
      trijet1Jet1 = TopCand.Jet1.at(i);
      trijet1Jet2 = TopCand.Jet2.at(i);
      trijet1BJet = TopCand.BJet.at(i);
      
      // Save top candidate 4-momentum
      trijet1 = TopCand.TrijetP4.at(i);

      foundTrijet1 = true;
      TrijetSelection_index.push_back(i);
      break;
    }
  if (!foundTrijet1) return output;

  for (size_t i=0; i<TopCand.MVA.size(); i++)
    {
      
      bool same0 = areSameJets(trijet1BJet, TopCand.Jet1.at(i)) || areSameJets(trijet1BJet, TopCand.Jet2.at(i)) || areSameJets(trijet1BJet, TopCand.BJet.at(i));
      bool same1 = areSameJets(trijet1Jet1, TopCand.Jet1.at(i)) || areSameJets(trijet1Jet1, TopCand.Jet2.at(i)) || areSameJets(trijet1Jet1, TopCand.BJet.at(i));
      bool same2 = areSameJets(trijet1Jet2, TopCand.Jet1.at(i)) || areSameJets(trijet1Jet2, TopCand.Jet2.at(i)) || areSameJets(trijet1Jet2, TopCand.BJet.at(i));
      // Skip top candidates with same jets as Leading in BDT trijet
      if (same0 || same1 || same2) continue; 
      //Skip if there are no free bjets left
      if (!foundFreeBjet(trijet1Jet1, trijet1Jet2, trijet1BJet, TopCand.Jet1.at(i), TopCand.Jet2.at(i), TopCand.BJet.at(i), bjets)) continue;
      double mvaValue = TopCand.MVA.at(i);
      // Find subleading in BDT value trijet
      if (mvaValue < MVAmax2) continue;
      MVAmax2 = mvaValue;
      // Save top candidate subjets
      trijet2Jet1 = TopCand.Jet1.at(i);
      trijet2Jet2 = TopCand.Jet2.at(i);
      trijet2BJet = TopCand.BJet.at(i);
      // Save top candidate 4-momentum
      trijet2     = TopCand.TrijetP4.at(i);
      TrijetSelection_index.push_back(i);
      break;
    }// For-loop: All top candidates
    


 
  if (MVAmax1 <= -999.999 || MVAmax2 <= -999.999)
    {
      if(MVAmax1 <= -999.999 && MVAmax2 <= -999.999) hNSelectedTrijets -> Fill(0);
      else hNSelectedTrijets -> Fill(1);
      return output;
    }
  else  hNSelectedTrijets -> Fill(2);


  //Return if one or less Top Candidates left
  if (TopCand.MVA.size() < 2) return output;
  
  
  //================================================================================================  
  // Tetrajet candidates
  //================================================================================================  
  bool haveMatchedChargedHiggsBJet    = MCtrue_ChargedHiggsBjet.size() > 0;
  bool haveMatchedTopFromChargedHiggs = MCtrueTopFromH_Bjet.size() > 0;
  bool haveMatchedAssocTop            = MCtrueAssocTop_Bjet.size() > 0;

  Jet tetrajetBjet, LdgBjet;
  double tetrajetBjetPt_max = -999.99;
  Jet mc_ChargedHiggsBJet;
  genParticle genChargedHiggs_BQuark;
  
  if (haveMatchedChargedHiggsBJet)
    {
      mc_ChargedHiggsBJet    = MCtrue_ChargedHiggsBjet.at(0);
      genChargedHiggs_BQuark = GenChargedHiggs_BQuark.at(0);
    }
  
  // Get Leading, Subleading in Pt selected trijet  
  if(trijet1.Pt() > trijet2.Pt())
    {
      leadingTrijetP4 = trijet1;
      leadingTrijetJet1 = getLeadingSubleadingJet(trijet1Jet1,trijet1Jet2,"leading");
      leadingTrijetJet2 = getLeadingSubleadingJet(trijet1Jet1,trijet1Jet2,"subleading");
      leadingTrijetBJet  = trijet1BJet;
      leadingTrijetMVA = MVAmax1;

      subleadingTrijetP4 = trijet2;
      subleadingTrijetJet1 = getLeadingSubleadingJet(trijet2Jet1,trijet2Jet2,"leading");
      subleadingTrijetJet2 = getLeadingSubleadingJet(trijet2Jet1,trijet2Jet2,"subleading");
      subleadingTrijetBJet = trijet2BJet;
      subleadingTrijetMVA = MVAmax2;
    }
  else // if(trijet2.Pt() > trijet1.Pt()) 
    {
      leadingTrijetP4 = trijet2;
      leadingTrijetJet1 = getLeadingSubleadingJet(trijet2Jet1,trijet2Jet2,"leading");
      leadingTrijetJet2 = getLeadingSubleadingJet(trijet2Jet1,trijet2Jet2,"subleading");
      leadingTrijetBJet  = trijet2BJet;
      leadingTrijetMVA = MVAmax2;

      subleadingTrijetP4 = trijet1;
      subleadingTrijetJet1 = getLeadingSubleadingJet(trijet1Jet1,trijet1Jet2,"leading");
      subleadingTrijetJet2 = getLeadingSubleadingJet(trijet1Jet1,trijet1Jet2,"subleading");
      subleadingTrijetBJet = trijet1BJet;
      subleadingTrijetMVA = MVAmax1;
    }
  
  //Leading free bjet 
  double ptBjet_max = -999.999;

  // For-loop: All selected b-jets
  for (auto& bjet: bjets)
    {
      // Store max pt                                                                                                                        
      if (bjet.pt() > ptBjet_max)
        {
          ptBjet_max = bjet.pt();
          LdgBjet = bjet;
        }
      
      // Skip if bjets matched any of the bjets in the two two candidates
      bool same1 = areSameJets(trijet1BJet, bjet) || areSameJets(trijet1Jet1, bjet) || areSameJets(trijet1Jet2, bjet);
      bool same2 = areSameJets(trijet2BJet, bjet) || areSameJets(trijet2Jet1, bjet) || areSameJets(trijet2Jet2, bjet);
      if (same1 || same2) continue;
      
      // Skip if tetrajet bjet pT is greater that this pt
      if (tetrajetBjetPt_max > bjet.pt()) continue;
      
      // Save variables
      tetrajetBjetPt_max = bjet.pt();
      tetrajetBjet       = bjet;
  }
    
  // Fill histograms 
  if (tetrajetBjetPt_max > 0) //fixme - needed?
    { 
      tetrajetP4 = leadingTrijetP4 + tetrajetBjet.p4();
      hLdgBjetPt    -> Fill(ptBjet_max);
    }


  //================================================================================================
  // ldg b-tagging Efficiency (per selected bjet) 
  // ldg selected top  (per selected top)
  //================================================================================================
  
  if (haveMatchedChargedHiggsBJet)
    {
      hHiggsBjetPt -> Fill(mc_ChargedHiggsBJet.pt());
      if (areSameJets(LdgBjet, mc_ChargedHiggsBJet)) hHiggsBjetPt_LdgBjetMatched -> Fill(mc_ChargedHiggsBJet.pt());
      
      if (tetrajetBjetPt_max > 0)
	  {
	    hChHiggsBjetPt_foundTetrajetBjet -> Fill(mc_ChargedHiggsBJet.pt());
	    if (areSameJets(tetrajetBjet, mc_ChargedHiggsBJet)) hChHiggsBjetPt_TetrajetBjetMatched -> Fill(mc_ChargedHiggsBJet.pt());
	    hLdgBjetPt    -> Fill(LdgBjet.pt());
	    if (areSameJets(LdgBjet, tetrajetBjet)) hLdgBjetPt_isLdgFreeBjet -> Fill(LdgBjet.pt());
	  }
    }
  
  if (haveMatchedTopFromChargedHiggs)
    {
      hTopFromHiggsPt -> Fill(MCtrueTopFromH_Bjet.at(0).pt());
      
      bool LdgTopIsTopFromH    = isRealMVATop(leadingTrijetJet1, leadingTrijetJet2, leadingTrijetBJet, MCtrueTopFromH_LdgJet.at(0), MCtrueTopFromH_SubldgJet.at(0), MCtrueTopFromH_Bjet.at(0));
      bool SubldgTopIsTopFromH = isRealMVATop(subleadingTrijetJet1, subleadingTrijetJet2, subleadingTrijetBJet, MCtrueTopFromH_LdgJet.at(0), MCtrueTopFromH_SubldgJet.at(0), MCtrueTopFromH_Bjet.at(0));
      
      if (LdgTopIsTopFromH)                         hTopFromHiggsPt_isLdgMVATrijet    -> Fill(MCtrueTopFromH_Bjet.at(0).pt());
      if (SubldgTopIsTopFromH)                      hTopFromHiggsPt_isSubldgMVATrijet -> Fill(MCtrueTopFromH_Bjet.at(0).pt());
      if (LdgTopIsTopFromH || SubldgTopIsTopFromH)  hTopFromHiggsPt_isMVATrijet       -> Fill (MCtrueTopFromH_Bjet.at(0).pt());
      
      math::XYZTLorentzVector TopFromHiggsP4;
      TopFromHiggsP4 = MCtrueTopFromH_LdgJet.at(0).p4() + MCtrueTopFromH_SubldgJet.at(0).p4() + MCtrueTopFromH_Bjet.at(0).p4();
      
      if (!LdgTopIsTopFromH)
	{
	  hDeltaPtOverPt_TopFromH_LdgMVATrijet -> Fill((TopFromHiggsP4.Pt() - leadingTrijetP4.Pt())/TopFromHiggsP4.Pt());
	  hDeltaEta_TopFromH_LdgMVATrijet      -> Fill(TopFromHiggsP4.Eta() - leadingTrijetP4.Eta());
	  hDeltaPhi_TopFromH_LdgMVATrijet      -> Fill(std::abs(ROOT::Math::VectorUtil::DeltaPhi(TopFromHiggsP4, leadingTrijetP4)));
	  hDeltaR_TopFromH_LdgMVATrijet        -> Fill(ROOT::Math::VectorUtil::DeltaR(TopFromHiggsP4, leadingTrijetP4));
	  
	  hDeltaPtOverPt_TopFromH_SubldgMVATrijet -> Fill((TopFromHiggsP4.Pt() - subleadingTrijetP4.Pt())/TopFromHiggsP4.Pt());
	  hDeltaEta_TopFromH_SubldgMVATrijet      -> Fill(TopFromHiggsP4.Eta() - subleadingTrijetP4.Eta());
	  hDeltaPhi_TopFromH_SubldgMVATrijet      -> Fill(std::abs(ROOT::Math::VectorUtil::DeltaPhi(TopFromHiggsP4, subleadingTrijetP4)));
	  hDeltaR_TopFromH_SubldgMVATrijet        -> Fill(ROOT::Math::VectorUtil::DeltaR(TopFromHiggsP4, subleadingTrijetP4));
	}
    }


  //================================================================================================  
  // Top-tagging Efficiency (per selected top)
  //================================================================================================

  bool passBDT1       = cfg_MVACut.passedCut(MVAmax1);
  bool passBDT2       = cfg_MVACut.passedCut(MVAmax2);
  bool passBDT1or2    = cfg_MVACut.passedCut(max(MVAmax1, MVAmax2));
  bool passBDTboth    = passBDT1*passBDT2;

  // bool passBDT1       = false;
  // bool passBDT2       = false;

  //BDT values of leading, subleading in BDT top candidates
  // unsigned int MVACut_index  = 0;
  // for (size_t i=0; i < TrijetSelection_index.size(); i++)
  //   {
  //     int index = TrijetSelection_index.at(i);
  //     const float mvaCut = cfg_MVACuts.at(MVACut_index);
  //     if (TopCand.MVA.at(index) > mvaCut)
  // 	{
  // 	  if (i==0) passBDT1 = true;
  // 	  if (i==1) passBDT2 = true;
  // 	}
  //     if (MVACut_index  < cfg_MVACuts.size()-1  ) MVACut_index++;

  //   }

  // bool passBDT1or2 = passBDT1 || passBDT2;
  // bool passBDTboth    = passBDT1*passBDT2;

  bool inTopDir1        = false;
  bool inTopDir2        = false;
  bool inTopDir1or2     = false;
  bool realInTopDir1    = false;
  bool realInTopDir2    = false;
  bool realInTopDirBoth = false;
  bool IsInTopDirection = true;
  bool realtop1         = false;
  bool realtop2         = false;
  bool realtopBoth      = false;

  if (event.isMC() && doMatching)
    {
      
      // Definitions
      realInTopDir1   = false;
      realInTopDir2   = false;
      
      // For-loop: All top-quarks
      for (auto& top: GenTops)
	{

	  // Find dR(t, trijet)
	  double dR_t1 = ROOT::Math::VectorUtil::DeltaR(top.p4(), trijet1);
	  double dR_t2 = ROOT::Math::VectorUtil::DeltaR(top.p4(), trijet2);

	  // Is the trijet in top's direction
	  if (dR_t1 < 0.4 ) realInTopDir1 = true; 
	  if (dR_t2 < 0.4 ) realInTopDir2 = true; 

	  // Is the trijet matched?
	  if (min(dR_t1, dR_t2) > 0.4) IsInTopDirection = false;

	  // Define booleans
	  bool inTopDir1    = (dR_t1 < 0.4);
	  bool inTopDir2    = (dR_t2 < 0.4);
	  bool inTopDir1or2 = min(dR_t1, dR_t2) < 0.4;

	  // Fill histograms
	  hTopQuarkPt ->Fill(top.pt());
	  if ( passBDT1*inTopDir1 || passBDT2*inTopDir2 ) hTopQuarkPt_InTopDirBDT->Fill(top.pt());
	  if ( inTopDir1or2 )  hTopQuarkPt_InTopDir->Fill(top.pt());
	  if ( passBDT1or2 )   hTopQuarkPt_BDT->Fill(top.pt());
	}

      if (0) cout << inTopDir1 << inTopDir2 << inTopDir1or2 << endl;

      // Assign booleans
      realInTopDirBoth    = realInTopDir1*realInTopDir2;
      realtop1    = isRealMVATop(trijet1Jet1, trijet1Jet2, trijet1BJet, MCtrue_LdgJet,  MCtrue_SubldgJet, MCtrue_Bjet);  
      realtop2    = isRealMVATop(trijet2Jet1, trijet2Jet2, trijet2BJet, MCtrue_LdgJet,  MCtrue_SubldgJet, MCtrue_Bjet);
      realtopBoth = realtop1*realtop2;

      //================================================================================================  
      // Top-tagging Efficiency (per top candidate)
      //================================================================================================
      vector <int> InTopDir_index, MatchedTop_index;
      
      // For-loop: All top quarks
      for (size_t j=0; j<GenTops.size(); j++)
	{	
	  
	  // Get the genParicle
	  genParticle top;
	  top =GenTops.at(j);

	  // Definitions
	  int inTopDir_index = -1, matchedTop_index = -1;
	  double dR_tmin  = 999.999;
	  bool genuineTop = false; 
	  
	  // For-loop: All top candidates
	  for (size_t i = 0; i < TopCand.MVA.size(); i++)
	    {
	      math::XYZTLorentzVector trijet;
	      trijet = TopCand.TrijetP4.at(i);

	      // Calculate dR(t, trijet)
	      double dR_t = ROOT::Math::VectorUtil::DeltaR(top.p4(), trijet);
	      
	      // Find minimum dR
	      if (dR_t < dR_tmin)
		{
		inTopDir_index = i;
		dR_tmin = dR_t;
		}	
	      
	      // Find index of matched trijets
	      bool isMatched = FoundTop.at(j);
	      bool isOnlyMatched = (MCtrue_Bjet.size() == 1);
	      bool sizesAgree    = (MCtrue_Bjet.size() == GenTops.size());

	      if ( isMatched*isOnlyMatched )
		{

		  bool same1 = areSameJets(TopCand.Jet1.at(i), MCtrue_LdgJet.at(0))    && areSameJets(TopCand.Jet2.at(i), MCtrue_SubldgJet.at(0)) && areSameJets(TopCand.BJet.at(i),  MCtrue_Bjet.at(0));
		  bool same2 = areSameJets(TopCand.Jet1.at(i), MCtrue_SubldgJet.at(0)) && areSameJets(TopCand.Jet2.at(i), MCtrue_LdgJet.at(0))    && areSameJets(TopCand.BJet.at(i),  MCtrue_Bjet.at(0));
		  
		  if (same1 || same2)
		    {
		      genuineTop = true;
		      matchedTop_index = i;
		      MatchedTop_index.push_back(matchedTop_index);
		    }
		}// if ( isMatched*isOnlyMatched )

	      if ( isMatched*sizesAgree )
		{
		  bool same1 = areSameJets(TopCand.Jet1.at(i), MCtrue_LdgJet.at(j))    && areSameJets(TopCand.Jet2.at(i), MCtrue_SubldgJet.at(j)) && areSameJets(TopCand.BJet.at(i),  MCtrue_Bjet.at(j));
		  bool same2 = areSameJets(TopCand.Jet1.at(i), MCtrue_SubldgJet.at(j)) && areSameJets(TopCand.Jet2.at(i), MCtrue_LdgJet.at(j))    && areSameJets(TopCand.BJet.at(i),  MCtrue_Bjet.at(j));
		  if (same1 || same2)
		    {
		      genuineTop = true;
		      matchedTop_index = i;
		      MatchedTop_index.push_back(matchedTop_index);
		    }//if (same1 || same2)

		}//if ( isMatched*sizesAgree )
	    }// For-loop: All top candidates
	
	  // Fill histograms
	  hDeltaRMinTopTrijet -> Fill(dR_tmin);
	  
	  // Find index of trijets In top direction (min DeltaR)
	  if (genuineTop)
	    {
	      hAllTopQuarkPt_Matched-> Fill(top.pt());
	      bool matchedPassedBDT = cfg_MVACut.passedCut(TopCand.MVA.at(matchedTop_index));
	      if ( matchedPassedBDT ) hAllTopQuarkPt_MatchedBDT -> Fill(top.pt());
	    }
      
	  // In Top direction
	  if (dR_tmin < 0.4)
	    {
	      // Save top candidate
	      InTopDir_index.push_back(inTopDir_index);
	      hAllTopQuarkPt_InTopDir -> Fill(top.pt());
	      
	      bool inTopDirPassedBDT = cfg_MVACut.passedCut(TopCand.MVA.at(inTopDir_index));
	      if ( inTopDirPassedBDT ) hAllTopQuarkPt_InTopDirBDT -> Fill(top.pt()); 
	    }// if (dR_tmin < 0.4)
	  else hAllTopQuarkPt_NotInTopDir-> Fill(top.pt()); 

	}// For-loop: All top quarks

      // Definitions
      double leadingFakePt  = -999.999;
      double leadingFakeMVA = -999.999;
      bool real_inTopDir    = false;
      bool realTop          = false;
      int matchedPassBDT    = 0;
      int nTopDirPassBDT    = 0;
      int RealSelectedTop   = 0;
      int fakeInTopDir      = 0;
      
      // For-loop: All top candidates
    for (size_t i = 0; i < TopCand.MVA.size(); i++)
      {

	real_inTopDir = false;
	realTop       = false;
	
	// For-loop: All top candidates in top direction (Nested)
	for (size_t j=0; j<InTopDir_index.size(); j++)
	  {
	    if (i==(size_t) InTopDir_index.at(j)) real_inTopDir = true;
	  }
	
	// For-loop: All top candidates matched (Nested)
	for (size_t j=0; j<MatchedTop_index.size(); j++)
	  {
	    if (i==(size_t) MatchedTop_index.at(j)) realTop = true;      
	  }

	// In Top Direction
	if (real_inTopDir)
	  {
	    hTrijetInTopDir_Mass -> Fill(TopCand.TrijetP4.at(i).M());
	    bool passBDT = cfg_MVACut.passedCut(TopCand.MVA.at(i));
	    if ( passBDT ) nTopDirPassBDT++;
	  }//if (real_inTopDir)
	
	// Genuine Trijet
	if (realTop)
	  {
	    hTrijetTopMatched_Mass  -> Fill(TopCand.TrijetP4.at(i).M());
	    hTrijetMatched_BDTvalue -> Fill(TopCand.MVA.at(i));
	    
	    bool passBDT = cfg_MVACut.passedCut(TopCand.MVA.at(i));
	    if ( passBDT )
	      {
		bool isLdgInBDT1or2 = (TopCand.MVA.at(i) == MVAmax1 || TopCand.MVA.at(i) == MVAmax2);
		matchedPassBDT++;
		if ( isLdgInBDT1or2 ) RealSelectedTop++;
	      }

	  }//if (realTop)

      // Trijets in Top direction AND not genuine
	if (real_inTopDir && !realTop)
	  {
	    hTrijetInTopDirNonMatched_Mass -> Fill(TopCand.TrijetP4.at(i).M());
	    fakeInTopDir++;
	  }
	
      // Trijets NOT in top direction
      if (!real_inTopDir)
	{
	  hTrijetNotInTopDirPt -> Fill (TopCand.TrijetP4.at(i).pt());
	  if (cfg_MVACut.passedCut(TopCand.MVA.at(i))) hTrijetNotInTopDirPt_BDT -> Fill(TopCand.TrijetP4.at(i).pt());
	}

      // Fake trijets
      if (!realTop)
	{
	  hTrijetNonMatched_BDTvalue -> Fill (TopCand.MVA.at(i));
	  hTrijetFakePt              -> Fill (TopCand.TrijetP4.at(i).pt());
	  hFakeTrijetMassVsBDTvalue     -> Fill (TopCand.TrijetP4.at(i).M(),TopCand.MVA.at(i));
	  
	  bool passBDT   = cfg_MVACut.passedCut(TopCand.MVA.at(i));
	  bool isLdgInPt = leadingFakePt < TopCand.TrijetP4.at(i).pt();

	  if ( passBDT ) hTrijetFakePt_BDT-> Fill (TopCand.TrijetP4.at(i).pt());	  
	  if ( isLdgInPt )
	    {
	      leadingFakePt  = TopCand.TrijetP4.at(i).pt();
	      leadingFakeMVA = TopCand.MVA.at(i);
	    }
	  
	}//if (!realTop)
      }// For-loop: All top candidates

    if (leadingFakePt > 0)
      {
	hLdgTrijetFake -> Fill(leadingFakePt);
	if (cfg_MVACut.passedCut(leadingFakeMVA)) hLdgTrijetFake_BDT -> Fill(leadingFakePt);
      }
    
    if (IsInTopDirection) hInTopDirBDTmult -> Fill(nTopDirPassBDT);
    
    bool passBDTboth = cfg_MVACut.passedCut(min(MVAmax1,MVAmax2));   
    if (MatchedTop_index.size() == GenTops.size() && passBDTboth )
      {
      hMatchedBDTmult -> Fill(matchedPassBDT);
      hRealSelectedTopMult -> Fill (RealSelectedTop);
      }
    hFakeInTopDirMult -> Fill (fakeInTopDir);

    //================================================================================================
    // Top-tagging Efficiency (per top candidate) - combinations with same subjets (b-tag assignment)
    //================================================================================================
    int NselectedMatched_sameOdj = 0;

    // For-loop: All top candidates matched
    for (size_t j=0; j<MatchedTop_index.size(); j++)
      {
	
	int matched_index = MatchedTop_index.at(j);
	double MVA_min    = TopCand.MVA.at(matched_index);
	double MVA_max    = TopCand.MVA.at(matched_index), BdiscrMax = TopCand.BJet.at(matched_index).bjetDiscriminator();
	int MVAmax_index  = matched_index;

	//Trijets with Wrong-assignment b-tagged jet -  indices
	vector <int> wrongAssignmentTrijetIndex;                                                                           
	wrongAssignmentTrijetIndex = GetWrongAssignmentTrijetIndex(matched_index,TopCand.Jet1, TopCand.Jet2, TopCand.BJet);
	
	bool selectedMatched_sameOdj = true;
	double DeltaMVA_max = -999.999, absDeltaMVA_max = -999.999, DeltaMVA_min = 999.999;
	
	// For-loop: All wrongly-assigned top candidates (Nested)
	for(size_t k=0; k< wrongAssignmentTrijetIndex.size(); k++)
	  {
	    
	    double DeltaMVAvalue = TopCand.MVA.at(matched_index) - TopCand.MVA.at(wrongAssignmentTrijetIndex.at(k));
	    
	    // Find maximum and minumum MVA value
	    if (TopCand.MVA.at(wrongAssignmentTrijetIndex.at(k)) < MVA_min) MVA_min = TopCand.MVA.at(wrongAssignmentTrijetIndex.at(k));
	    
	    if (TopCand.MVA.at(wrongAssignmentTrijetIndex.at(k)) > MVA_max)
	      {		
		MVA_max   = TopCand.MVA.at(wrongAssignmentTrijetIndex.at(k));
		BdiscrMax = TopCand.BJet.at(wrongAssignmentTrijetIndex.at(k)).bjetDiscriminator();
		MVAmax_index = wrongAssignmentTrijetIndex.at(k);
	      }
	    
	    // Find maximum and minimum DeltaMVA value
	    if ( DeltaMVA_max == -999.999)
	      {
		DeltaMVA_max = DeltaMVAvalue;
		DeltaMVA_min = DeltaMVAvalue;
	      }
	    else if (std::abs(DeltaMVAvalue) > std::abs(DeltaMVA_max)){
	      DeltaMVA_max = DeltaMVAvalue;
	    }
	    else{
	      DeltaMVA_min =  DeltaMVAvalue;
	    }
	    
	    if (std::abs(DeltaMVAvalue) > absDeltaMVA_max) absDeltaMVA_max = std::abs(DeltaMVAvalue);
	    if (DeltaMVAvalue < 0) selectedMatched_sameOdj = false;

	  }// for(size_t k=0; k< wrongAssignmentTrijetIndex.size(); k++)

	// Fill histograms
	hDeltaMVAmax_MCtruth_SameObjFakes    -> Fill(DeltaMVA_max);
	hAbsDeltaMVAmax_MCtruth_SameObjFakes -> Fill(absDeltaMVA_max);
	hDeltaMVAmin_MCtruth_SameObjFakes    -> Fill(DeltaMVA_min);
	hTrijetPtMaxMVASameFakeObj           -> Fill(TopCand.TrijetP4.at(MVAmax_index).Pt());
	if (BdiscrMax > 0.8484) hTrijetPtMaxMVASameFakeObj_BjetPassCSV -> Fill(TopCand.TrijetP4.at(MVAmax_index).Pt());


	// MVA value of matched trijets when DeltaMVA > 1
	if (DeltaMVA_min > 1) hMVAvalue_DeltaMVAgt1 -> Fill(TopCand.MVA.at(matched_index));
	
	if (selectedMatched_sameOdj && BdiscrMax > 0.8484) NselectedMatched_sameOdj++;      

	if (!cfg_MVACut.passedCut(MVA_min)) continue;

	// Fill histograms
	hDeltaMVAmax_MCtruth_SameObjFakesPassBDT -> Fill(DeltaMVA_max);
	hDeltaMVAmin_MCtruth_SameObjFakesPassBDT -> Fill(DeltaMVA_min);
	hDeltaMVAmaxVsTrijetPassBDTvalue         -> Fill(DeltaMVA_max, TopCand.MVA.at(matched_index));
	hDeltaMVAminVsTrijetPassBDTvalue         -> Fill(DeltaMVA_min, TopCand.MVA.at(matched_index));
	
      }// For-loop: All top candidates matched
   

    
    //================================================================================================
    // Fill histograms
    //================================================================================================

    if (MatchedTop_index.size() == GenTops.size())  hMatchedPassBDTmult_SameObjFakes -> Fill(NselectedMatched_sameOdj);
    if  (jets.size() > 9)                           hMatchedTrijetMult_JetsGT9 -> Fill(MCtrue_Bjet.size());
    hMatchedTrijetMult_JetsInc -> Fill(MatchedTop_index.size());
    
    // For-loop: All top candidates passing BDT cut
    for (size_t i = 0; i < TopCand.MVA.size(); i++)
      {
	if (!cfg_MVACut.passedCut(TopCand.MVA.at(i))) continue;
	hAllTrijetPassBDT_pt -> Fill(TopCand.TrijetP4.at(i).Pt());
	hTrijetPassBDT_bDisc -> Fill(TopCand.BJet.at(i).bjetDiscriminator());
	if (TopCand.BJet.at(i).bjetDiscriminator() > 0.8484) hAllTrijetPassBDTbPassCSV_pt -> Fill(TopCand.TrijetP4.at(i).Pt());
      }// For-loop: All top candidates passing BDT cut
    
    }// if (event.isMC() && doMatching)


  // Skip events where no free b-jet is available
  //if (tetrajetBjet.p4().pt() <= 0) return output; // fixme

  //================================================================================================
  // Fill output data  
  //================================================================================================

  output.bPassedSelection   = (cfg_MVACut.passedCut(MVAmax1) && cfg_MVACut.passedCut(MVAmax2) && tetrajetBjetPt_max > 0 );
  output.bHasFreeBJet       = (tetrajetBjetPt_max > 0); 
  output.fMVAmax1           = MVAmax1;
  output.fTrijet1Jet1       = leadingTrijetJet1;
  output.fTrijet1Jet2       = leadingTrijetJet2;
  output.fTrijet1BJet       = leadingTrijetBJet;
  output.fTrijet1Dijet_p4   = leadingTrijetJet1.p4() +  leadingTrijetJet2.p4();
  output.fTrijet1_p4        = leadingTrijetP4;
  output.fMVAmax2           = MVAmax2;
  output.fTrijet2Jet1       = subleadingTrijetJet1;
  output.fTrijet2Jet2       = subleadingTrijetJet2;
  output.fTrijet2BJet       = subleadingTrijetBJet;
  output.fTrijet2Dijet_p4   = subleadingTrijetJet1.p4() +  subleadingTrijetJet2.p4();
  output.fTrijet2_p4        = subleadingTrijetP4;
  output.fTetrajetBJet      = tetrajetBjet; 
  output.fLdgTetrajet_p4    = tetrajetP4;
  output.fSubldgTetrajet_p4 = subleadingTrijetP4 + tetrajetBjet.p4();

  //================================================================================================
  // Fill histograms (Before cuts)
  //================================================================================================
  hTrijetMultiplicity        -> Fill(TopCand.MVA.size());               //Trijet multiplicity
  hNjetsVsNTrijets_beforeBDT -> Fill(jets.size(), TopCand.MVA.size());  //Trijet multiplicity as a function of Jet multiplicity  (Before MVA selection)   <---Constant
  hNjetsVsNTrijets_afterBDT  -> Fill(jets.size(), NpassBDT);            //Trijet multiplicity as a function of Jet multiplicity  (After MVA selection)
  if (cfg_MVACut.passedCut(MVAmax1)) hTrijetPt_BDT ->Fill(trijet1.Pt());
  if (cfg_MVACut.passedCut(MVAmax2)) hTrijetPt_BDT ->Fill(trijet2.Pt());

  // Top-tagging Efficiency (per event)
  if (IsInTopDirection)
    {
      hEventTrijetPt -> Fill(trijet1.Pt()); 
      hEventTrijetPt -> Fill(trijet2.Pt());  
      if (passBDTboth)
	{
	  hEventTrijetPt_BDT -> Fill(trijet1.Pt());
	  hEventTrijetPt_BDT -> Fill(trijet2.Pt());
	  if (realInTopDirBoth)
	    {
	      hEventTrijetPt_InTopDirBDT -> Fill(trijet1.Pt());
	      hEventTrijetPt_InTopDirBDT -> Fill(trijet2.Pt());
	    }//if (realInTopDirBoth)
	}//if (passBDTboth)
    }//if (IsInTopDirection)
  
  // All the top quarks have been matched
  if (MCtrue_Bjet.size() == GenTops.size())
    {
      hEventTrijetPt2T -> Fill(trijet1.Pt());              //Trijet.pt -- Inclusive
      hEventTrijetPt2T -> Fill(trijet2.Pt());              //Trijet.pt -- Inclusive
      if ( realtopBoth )
	{
	  hEventTrijetPt2T_Matched -> Fill(trijet1.Pt()); //Trijet.pt(Matched)  -- Inclusive
	  hEventTrijetPt2T_Matched -> Fill(trijet2.Pt()); //Trijet.pt(Matched)  -- Inclusive
	}
      if ( passBDTboth )
	{
	  hEventTrijetPt2T_BDT -> Fill(trijet1.Pt());        //Trijet.pt(passBDT) -- Inclusive
	  hEventTrijetPt2T_BDT -> Fill(trijet2.Pt());        //Trijet.pt(passBDT) -- Inclusive
	  if ( realtopBoth )
	    {
	      hEventTrijetPt2T_MatchedBDT -> Fill(trijet1.Pt()); //Trijet.pt(passBDT&&Matched) -- Inclusive
	      hEventTrijetPt2T_MatchedBDT -> Fill(trijet2.Pt()); //Trijet.pt(passBDT&&Matched) -- Inclusive
	    }//if ( realtopBoth )
	}//if ( passBDTboth )
    }//if (MCtrue_Bjet.size() == GenTops.size())
  

  // Replace all PF Jet 4-vectors with their matched GenJet 4-vectors
  if (replaceJets) ReplaceJetsWithGenJets(output); //fixme: not tested!!!

  //================================================================================================
  // Apply cuts
  //================================================================================================
  if ( !output.hasFreeBJet() ) return output; 
  cSubPassedFreeBjetCut.increment();

  if ( !passBDTboth ) return output; 
  cSubPassedBDTCut.increment();

  // Passed all top selection cuts
  cPassedTopSelectionBDT.increment();

  //================================================================================================
  // Fill histograms (After cuts)
  //================================================================================================

  hTopCandMass ->Fill(output.fTrijet1_p4.M());
  hTopCandMass ->Fill(output.fTrijet2_p4.M());
  
  
  // Leading top candidate passing BDT  
  double dijetMass = (output.fTrijet1Jet1.p4() +  output.fTrijet1Jet2.p4()).M();
  hLdgTrijetTopMassWMassRatio -> Fill(output.fTrijet1_p4.M()/dijetMass);
  
  hLdgTrijetPt          -> Fill(output.fTrijet1_p4.Pt());
  hLdgTrijetMass        -> Fill(output.fTrijet1_p4.M());
  hLdgTrijetJet1Pt      -> Fill(output.fTrijet1Jet1.pt());
  hLdgTrijetJet1Eta     -> Fill(output.fTrijet1Jet1.eta());
  hLdgTrijetJet1BDisc   -> Fill(output.fTrijet1Jet1.bjetDiscriminator());
  hLdgTrijetJet2Pt      -> Fill(output.fTrijet1Jet2.pt());
  hLdgTrijetJet2Eta     -> Fill(output.fTrijet1Jet2.eta());
  hLdgTrijetJet2BDisc   -> Fill(output.fTrijet1Jet2.bjetDiscriminator());
  hLdgTrijetBJetPt      -> Fill(output.fTrijet1BJet.pt());
  hLdgTrijetBJetEta     -> Fill(output.fTrijet1BJet.eta());
  hLdgTrijetBJetBDisc   -> Fill(output.fTrijet1BJet.bjetDiscriminator());
  hLdgTrijetDiJetPt     -> Fill(output.fTrijet1Dijet_p4.Pt());
  hLdgTrijetDiJetEta    -> Fill(output.fTrijet1Dijet_p4.Eta());
  hLdgTrijetDiJetMass   -> Fill(output.fTrijet1Dijet_p4.M());
  hLdgTrijetDijetDeltaR -> Fill(ROOT::Math::VectorUtil::DeltaR(output.fTrijet1Jet1.p4(), output.fTrijet1Jet2.p4()));
  // Subleading top candidate passing BDT
  hSubldgTrijetTopMassWMassRatio -> Fill(output.fTrijet2_p4.M()/(output.fTrijet2Jet1.p4() + output.fTrijet2Jet2.p4()).M());
  hSubldgTrijetPt           -> Fill(output.fTrijet2_p4.Pt());
  hSubldgTrijetMass         -> Fill(output.fTrijet2_p4.M());
  hSubldgTrijetJet1Pt       -> Fill(output.fTrijet2Jet1.pt());
  hSubldgTrijetJet1Eta      -> Fill(output.fTrijet2Jet1.eta());
  hSubldgTrijetJet1BDisc    -> Fill(output.fTrijet2Jet1.bjetDiscriminator());    
  hSubldgTrijetJet2Pt       -> Fill(output.fTrijet2Jet2.pt());
  hSubldgTrijetJet2Eta      -> Fill(output.fTrijet2Jet2.eta());
  hSubldgTrijetJet2BDisc    -> Fill(output.fTrijet2Jet2.bjetDiscriminator());
  hSubldgTrijetBJetPt       -> Fill(output.fTrijet2BJet.pt());
  hSubldgTrijetBJetEta      -> Fill(output.fTrijet2BJet.eta());
  hSubldgTrijetBJetBDisc    -> Fill(output.fTrijet2BJet.bjetDiscriminator());
  hSubldgTrijetDiJetPt      -> Fill(output.fTrijet2Dijet_p4.Pt());
  hSubldgTrijetDiJetEta     -> Fill(output.fTrijet2Dijet_p4.Eta());
  hSubldgTrijetDiJetMass    -> Fill(output.fTrijet2Dijet_p4.M());
  hSubldgTrijetDijetDeltaR  -> Fill(ROOT::Math::VectorUtil::DeltaR(output.fTrijet2Jet1.p4(), output.fTrijet2Jet2.p4()));

  // Ldg in pt free b-jet
  hTetrajetBJetPt    -> Fill(output.fTetrajetBJet.pt());
  hTetrajetBJetEta   -> Fill(output.fTetrajetBJet.eta());
  hTetrajetBJetBDisc -> Fill(output.fTetrajetBJet.bjetDiscriminator());
  hTetrajetPt        -> Fill(output.fLdgTetrajet_p4.Pt());
  hTetrajetMass      -> Fill(output.fLdgTetrajet_p4.M());
  hTetrajetEta       -> Fill(output.fLdgTetrajet_p4.Eta());


  //Efficiency plots (after all cuts)
  if (output.fTrijet1BJet.bjetDiscriminator() >= 0.8484)  hSelectedTrijetsPt_BjetPassCSVdisc_afterCuts -> Fill(output.fTrijet1_p4.Pt());
  if (output.fTrijet2BJet.bjetDiscriminator() >= 0.8484)  hSelectedTrijetsPt_BjetPassCSVdisc_afterCuts -> Fill(output.fTrijet2_p4.Pt());
  hSelectedTrijetsPt_afterCuts -> Fill(output.fTrijet1_p4.Pt());
  hSelectedTrijetsPt_afterCuts -> Fill(output.fTrijet2_p4.Pt());

  hBDTmultiplicity           -> Fill(NpassBDT);                         //Number of trijets passing MVA selection
  

  //================================================================================================
  //Correlation plots: DeltaEta, DeltaPhi, DeltaR
  //================================================================================================
  double deltaEta1 = output.fTrijet1_p4.Eta() - output.fTetrajetBJet.eta();
  double deltaEta2 = output.fTrijet2_p4.Eta() - output.fTetrajetBJet.eta();
  double deltaPhi1 = ROOT::Math::VectorUtil::DeltaPhi(output.fTrijet1_p4, output.fTetrajetBJet.p4());
  double deltaPhi2 = ROOT::Math::VectorUtil::DeltaPhi(output.fTrijet2_p4, output.fTetrajetBJet.p4());
  double deltaR1   = ROOT::Math::VectorUtil::DeltaR(output.fTrijet1_p4, output.fTetrajetBJet.p4());
  double deltaR2   = ROOT::Math::VectorUtil::DeltaR(output.fTrijet2_p4, output.fTetrajetBJet.p4());

  DEta_Trijet1TetrajetBjet_Vs_DEta_Trijet2TetrajetBjet -> Fill(std::abs(deltaEta1), std::abs(deltaEta2));
  DPhi_Trijet1TetrajetBjet_Vs_DPhi_Trijet2TetrajetBjet -> Fill(std::abs(deltaPhi1), std::abs(deltaPhi2));
  DR_Trijet1TetrajetBjet_Vs_DR_Trijet2TetrajetBjet     -> Fill(deltaR1, deltaR2);
  
  //================================================================================================
  //b-tagged bjet Efficiency (Before applying cut on top candidates with untagged b-jet)
  //================================================================================================
  for (size_t i=0; i<TopCand.MVA.size(); i++)
    {
      math::XYZTLorentzVector Trijet_p4;
      Trijet_p4 = TopCand.TrijetP4.at(i);
      if (!cfg_MVACut.passedCut(TopCand.MVA.at(i))) continue;
      hTrijetPt_PassBDT -> Fill(Trijet_p4.Pt());
      if (TopCand.BJet.at(i).bjetDiscriminator() < 0.8484) continue;
      hTrijetPt_PassBDT_BJetPassCSV -> Fill(Trijet_p4.Pt());
    }
  
  
  //================================================================================================
  // ldg b-tagging Efficiency (per selected bjet)
  // ldg selected top  (per selected top)
  //================================================================================================
  
  if (haveMatchedChargedHiggsBJet)
    {
      hHiggsBjetPt_afterCuts -> Fill(mc_ChargedHiggsBJet.pt());

      if (areSameJets(LdgBjet, mc_ChargedHiggsBJet)) hHiggsBjetPt_LdgBjetMatched_afterCuts -> Fill(mc_ChargedHiggsBJet.pt());
      hChHiggsBjetPt_foundTetrajetBjet_afterCuts -> Fill(mc_ChargedHiggsBJet.pt());

      if (areSameJets(LdgBjet, output.fTetrajetBJet)) hLdgBjetPt_isLdgFreeBjet_afterCuts -> Fill(LdgBjet.pt());      
      hLdgBjetPt_afterCuts    -> Fill(LdgBjet.pt());

      if (areSameJets(output.fTetrajetBJet, mc_ChargedHiggsBJet)){
	hChHiggsBjetPt_TetrajetBjetMatched_afterCuts -> Fill(mc_ChargedHiggsBJet.pt());
      }
      else{
	hDeltaPtOverPt_HiggsBjetPt_TetrajetBjetMatched_afterCuts -> Fill((mc_ChargedHiggsBJet.pt() - output.fTetrajetBJet.pt())/ mc_ChargedHiggsBJet.pt());
	hDeltaEta_HiggsBjetPt_TetrajetBjetMatched_afterCuts      -> Fill( mc_ChargedHiggsBJet.eta() - output.fTetrajetBJet.eta());
	hDeltaPhi_HiggsBjetPt_TetrajetBjetMatched_afterCuts      -> Fill( std::abs(ROOT::Math::VectorUtil::DeltaPhi(mc_ChargedHiggsBJet.p4(), output.fTetrajetBJet.p4())));
	hDeltaR_HiggsBjetPt_TetrajetBjetMatched_afterCuts        -> Fill( ROOT::Math::VectorUtil::DeltaR(mc_ChargedHiggsBJet.p4(), output.fTetrajetBJet.p4()));
	hDeltaCSV_HiggsBjetPt_TetrajetBjetMatched_afterCuts      -> Fill(mc_ChargedHiggsBJet.bjetDiscriminator() - output.fTetrajetBJet.bjetDiscriminator());
	
	//Tagged - Non matched bjet from H
	if (cfg_CSV_bDiscCut.passedCut(mc_ChargedHiggsBJet.bjetDiscriminator()))
	  {
	    //	    hChHiggdBJet_passCSV -> Fill(mc_ChargedHiggsBJet.pt());
	    //      bool  LdgTop_bjet = areSameJets(mc_ChargedHiggsBJet, output.fTrijet1Jet1) || areSameJets(mc_ChargedHiggsBJet, output.fTrijet1Jet2) || areSameJets(mc_ChargedHiggsBJet, output.fTrijet1BJet);
	    //      bool  SubldgTop_bjet = areSameJets(mc_ChargedHiggsBJet, output.fTrijet2Jet1) || areSameJets(mc_ChargedHiggsBJet, output.fTrijet2Jet2) || areSameJets(mc_ChargedHiggsBJet, output.fTrijet2BJet);
	    //	    std::cout<<bjets.at(0).pt()<<std::endl;
	  }
      }
      


    }
  
  if (haveMatchedTopFromChargedHiggs)
    {
      hTopFromHiggsPt_afterCuts -> Fill(MCtrueTopFromH_Bjet.at(0).pt());
      
      bool LdgTopIsTopFromH = isRealMVATop(output.fTrijet1Jet1, output.fTrijet1Jet2, output.fTrijet1BJet, MCtrueTopFromH_LdgJet.at(0), MCtrueTopFromH_SubldgJet.at(0), MCtrueTopFromH_Bjet.at(0));
      bool SubldgTopIsTopFromH = isRealMVATop(output.fTrijet2Jet1, output.fTrijet2Jet2, output.fTrijet2BJet, MCtrueTopFromH_LdgJet.at(0), MCtrueTopFromH_SubldgJet.at(0), MCtrueTopFromH_Bjet.at(0));

      math::XYZTLorentzVector TopFromHiggsP4;
      TopFromHiggsP4 = MCtrueTopFromH_LdgJet.at(0).p4() + MCtrueTopFromH_SubldgJet.at(0).p4() + MCtrueTopFromH_Bjet.at(0).p4();

      if (LdgTopIsTopFromH || SubldgTopIsTopFromH)  hTopFromHiggsPt_isMVATrijet_afterCuts -> Fill (MCtrueTopFromH_Bjet.at(0).pt());

      if (LdgTopIsTopFromH)
	{
	  hTopFromHiggsPt_isLdgMVATrijet_afterCuts    -> Fill(MCtrueTopFromH_Bjet.at(0).pt());
	}
      else
	{
	  hDeltaPtOverPt_TopFromH_LdgMVATrijet_afterCuts -> Fill((TopFromHiggsP4.Pt() - output.fTrijet1_p4.Pt())/TopFromHiggsP4.Pt());
	  hDeltaEta_TopFromH_LdgMVATrijet_afterCuts      -> Fill(TopFromHiggsP4.Eta() - output.fTrijet1_p4.Eta());
	  hDeltaPhi_TopFromH_LdgMVATrijet_afterCuts      -> Fill(std::abs(ROOT::Math::VectorUtil::DeltaPhi(TopFromHiggsP4, output.fTrijet1_p4)));
	  hDeltaR_TopFromH_LdgMVATrijet_afterCuts        -> Fill(ROOT::Math::VectorUtil::DeltaR(TopFromHiggsP4, output.fTrijet1_p4));
	  
	  hDeltaCSV_TopFromHBJet_LdgMVATrijetBjet_afterCuts -> Fill(MCtrueTopFromH_Bjet.at(0).bjetDiscriminator() - output.fTrijet1BJet.bjetDiscriminator());

	  int topFromHiggs_index = getTopFromHiggs(TopCand, MCtrueTopFromH_LdgJet.at(0), MCtrueTopFromH_SubldgJet.at(0), MCtrueTopFromH_Bjet.at(0));
	  if ( topFromHiggs_index != -1 ) hDeltaBDT_TopFromH_LdgMVATrijet_afterCuts -> Fill(TopCand.MVA.at(topFromHiggs_index) - leadingTrijetMVA);
	  else hDeltaBDT_TopFromH_LdgMVATrijet_afterCuts -> Fill(-10.);
	}
      
      if (SubldgTopIsTopFromH) 
	{
	  hTopFromHiggsPt_isSubldgMVATrijet_afterCuts -> Fill(MCtrueTopFromH_Bjet.at(0).pt());
	}
      else
	{
	  hDeltaPtOverPt_TopFromH_SubldgMVATrijet_afterCuts -> Fill((TopFromHiggsP4.Pt() - output.fTrijet1_p4.Pt())/TopFromHiggsP4.Pt());
	  hDeltaEta_TopFromH_SubldgMVATrijet_afterCuts      -> Fill(TopFromHiggsP4.Eta() - output.fTrijet1_p4.Eta());
	  hDeltaPhi_TopFromH_SubldgMVATrijet_afterCuts      -> Fill(std::abs(ROOT::Math::VectorUtil::DeltaPhi(TopFromHiggsP4, output.fTrijet1_p4)));
	  hDeltaR_TopFromH_SubldgMVATrijet_afterCuts        -> Fill(ROOT::Math::VectorUtil::DeltaR(TopFromHiggsP4, output.fTrijet1_p4));

	  hDeltaCSV_TopFromHBJet_SubldgMVATrijetBjet_afterCuts -> Fill(MCtrueTopFromH_Bjet.at(0).bjetDiscriminator() - output.fTrijet2BJet.bjetDiscriminator());

	  int topFromHiggs_index = getTopFromHiggs(TopCand, MCtrueTopFromH_LdgJet.at(0), MCtrueTopFromH_SubldgJet.at(0), MCtrueTopFromH_Bjet.at(0));
	  if ( topFromHiggs_index != -1 ) hDeltaBDT_TopFromH_SubldgMVATrijet_afterCuts -> Fill(TopCand.MVA.at(topFromHiggs_index) - subleadingTrijetMVA);
	  else hDeltaBDT_TopFromH_SubldgMVATrijet_afterCuts -> Fill(-10.);
	}
    }

  if (haveMatchedTopFromChargedHiggs && haveMatchedAssocTop)
    {
      math::XYZTLorentzVector TopFromHiggsP4, AssocTopP4;
      TopFromHiggsP4 = MCtrueTopFromH_LdgJet.at(0).p4() + MCtrueTopFromH_SubldgJet.at(0).p4() + MCtrueTopFromH_Bjet.at(0).p4();
      AssocTopP4     = MCtrueAssocTop_LdgJet.at(0).p4() + MCtrueAssocTop_SubldgJet.at(0).p4() + MCtrueAssocTop_Bjet.at(0).p4();
      hTopFromHiggsPtVSAssocTopPt -> Fill(TopFromHiggsP4.Pt(), AssocTopP4.Pt());

      //===Correlation Plots
      double dEta_Htop_Bjet     = std::abs(TopFromHiggsP4.Eta() - MCtrueTopFromH_Bjet.at(0).eta());
      double dPhi_Htop_Bjet     = std::abs(ROOT::Math::VectorUtil::DeltaPhi(TopFromHiggsP4, MCtrueTopFromH_Bjet.at(0).p4()));
      double dR_Htop_Bjet       = ROOT::Math::VectorUtil::DeltaR(TopFromHiggsP4, MCtrueTopFromH_Bjet.at(0).p4());

      double dEta_AssocTop_Bjet = std::abs(AssocTopP4.Eta() - MCtrueTopFromH_Bjet.at(0).eta());
      double dPhi_AssocTop_Bjet     = std::abs(ROOT::Math::VectorUtil::DeltaPhi(AssocTopP4, MCtrueTopFromH_Bjet.at(0).p4()));
      double dR_AssocTop_Bjet       = ROOT::Math::VectorUtil::DeltaR(AssocTopP4, MCtrueTopFromH_Bjet.at(0).p4());
      
      DEta_TopFromHBjetFromH_Vs_DEta_AssocTopBjetFromH -> Fill(dEta_Htop_Bjet, dEta_AssocTop_Bjet);
      DPhi_TopFromHBjetFromH_Vs_DPhi_AssocTopBjetFromH -> Fill(dPhi_Htop_Bjet, dPhi_AssocTop_Bjet);
      DR_TopFromHBjetFromH_Vs_DR_AssocTopBjetFromH     -> Fill(dR_Htop_Bjet, dR_AssocTop_Bjet);


    }

  return output;

}

void TopSelectionBDT::ReplaceJetsWithGenJets(Data &output){
  // Use only for testing:
  // This was introduced to see the best-case-scenario of this chi-square top fit
  // It replaces, post-fit (hence does not affect chi-sq values) the 4-vectors
  // of PF jets with those of the MC-matched ones (GenJets). It should tell us 
  // how much improvement we expect if we had perfect resolution


  // Declare variables
  math::XYZTLorentzVector trijet1_jet1_p4;
  math::XYZTLorentzVector trijet1_jet2_p4;
  math::XYZTLorentzVector trijet1_bjet_p4;

  math::XYZTLorentzVector trijet2_jet1_p4;
  math::XYZTLorentzVector trijet2_jet2_p4;
  math::XYZTLorentzVector trijet2_bjet_p4;

  math::XYZTLorentzVector tetrajet_bjet_p4;

  // Assign values
  trijet1_jet1_p4 = output.fTrijet1Jet1.p4();
  trijet1_jet2_p4 = output.fTrijet1Jet2.p4();
  trijet1_bjet_p4 = output.fTrijet1BJet.p4();

  trijet2_jet1_p4 = output.fTrijet2Jet1.p4();
  trijet2_jet2_p4 = output.fTrijet2Jet2.p4();
  trijet2_bjet_p4 = output.fTrijet2BJet.p4();

  // Overwrite values
  if (output.fTrijet1Jet1.MCjet() != nullptr )  trijet1_jet1_p4 = output.fTrijet1Jet1.MCjet()->p4();
  if (output.fTrijet1Jet2.MCjet() != nullptr )  trijet1_jet2_p4 = output.fTrijet1Jet2.MCjet()->p4();
  if (output.fTrijet1BJet.MCjet() != nullptr )  trijet1_bjet_p4 = output.fTrijet1BJet.MCjet()->p4();

  if (output.fTrijet2Jet1.MCjet() != nullptr )  trijet2_jet1_p4 = output.fTrijet2Jet1.MCjet()->p4();
  if (output.fTrijet2Jet2.MCjet() != nullptr )  trijet2_jet2_p4 = output.fTrijet2Jet2.MCjet()->p4();
  if (output.fTrijet2BJet.MCjet() != nullptr )  trijet2_bjet_p4 = output.fTrijet2BJet.MCjet()->p4();

  // Assign Trijet-1
  // output.fTrijet1Jet1 = jets.at(j1); // Can't do this MCjet is not an object of type "Jet"
  // output.fTrijet1Jet2 = jets.at(j2); // Can't do this MCjet is not an object of type "Jet"
  // output.fTrijet1BJet = jets.at(b1); // Can't do this MCjet is not an object of type "Jet"
  output.fTrijet1Dijet_p4 = trijet1_jet1_p4 + trijet1_jet2_p4;
  output.fTrijet1_p4      = output.fTrijet1Dijet_p4 + trijet1_bjet_p4;

  // Assign Trijet-2
  // output.fTrijet2Jet1 = jets.at(j3); // Can't do this MCjet is not an object of type "Jet"
  // output.fTrijet2Jet2 = jets.at(j4); // Can't do this MCjet is not an object of type "Jet"
  // output.fTrijet2BJet = jets.at(b2); // Can't do this MCjet is not an object of type "Jet"
  output.fTrijet2Dijet_p4 = trijet2_jet1_p4 + trijet2_jet2_p4;
  output.fTrijet2_p4      = output.fTrijet2Dijet_p4 + trijet2_bjet_p4;

  // DiJets with min/max dR separation
  double dR12 = ROOT::Math::VectorUtil::DeltaR(trijet1_jet1_p4, trijet1_jet2_p4);
  double dR34 = ROOT::Math::VectorUtil::DeltaR(trijet2_jet1_p4, trijet2_jet2_p4);
  if (dR12 < dR34) 
    {
      output.fDijetWithMinDR_p4 = trijet1_jet1_p4 + trijet1_jet2_p4;
      output.fDijetWithMaxDR_p4 = trijet2_jet1_p4 + trijet2_jet2_p4;
    }
  else 
    {
      output.fDijetWithMaxDR_p4 = trijet2_jet1_p4 + trijet2_jet2_p4;
      output.fDijetWithMinDR_p4 = trijet1_jet1_p4 + trijet1_jet2_p4;
    }
      
  // Tetrajet b-jet (for Invariant Mass)
  tetrajet_bjet_p4 = output.getTetrajetBJet().p4();
  if (output.getTetrajetBJet().MCjet() != nullptr ) tetrajet_bjet_p4 = output.getTetrajetBJet().MCjet()->p4();

  // Ldg here means use the LdgTrijet
  output.fLdgTetrajet_p4    = output.getLdgTrijet()    + tetrajet_bjet_p4;
  output.fSubldgTetrajet_p4 = output.getSubldgTrijet() + tetrajet_bjet_p4;

  //std::cout << "output.getLdgTrijet().M() = " << output.getLdgTrijet().M() << std::endl;
  //std::cout << "output.fLdgTetrajet_p4.M() = " << output.fLdgTetrajet_p4.M() << "\n" << std::endl;
  
  return;
}

bool TopSelectionBDT::_getIsGenuineB(bool bIsMC, const std::vector<Jet>& selectedBjets){
  if (!bIsMC) return false;

  // GenuineB=All selected b-jets in the event are genuine (using jet-flavour from MC)
  unsigned int nFakes=0;
  for(const Jet& bjet: selectedBjets)
    {
      // https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideBTagMCTools#Jet_flavour_in_PAT
      bool isFakeB = (abs(bjet.pdgId()) != 5); // For data pdgId==0
      if (isFakeB) nFakes++;
    }
  return (nFakes==0);
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


/*
  Get the last copy of a particle.
*/
const genParticle TopSelectionBDT::GetLastCopy(const std::vector<genParticle> genParticles, const genParticle &p){

  int gen_pdgId = p.pdgId();

  for (size_t i=0; i<p.daughters().size(); i++){

    const genParticle genDau = genParticles[p.daughters().at(i)];
    int genDau_pdgId   = genDau.pdgId();

    if (gen_pdgId == genDau_pdgId)  return GetLastCopy(genParticles, genDau);
  }
  return p;
}


/*
  Get all gen particles by pdgId
*/
std::vector<genParticle> TopSelectionBDT::GetGenParticles(const std::vector<genParticle> genParticles, const int pdgId)
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



//Soti
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

bool TopSelectionBDT::isWsubjet(const Jet& jet , const std::vector<Jet>& jets1 , const std::vector<Jet>& jets2){
  return  (isMatchedJet(jet,jets1)||isMatchedJet(jet,jets2));
}

bool TopSelectionBDT::isMatchedJet(const Jet& jet, const std::vector<Jet>& jets) {
  for (auto Jet: jets)
    {
      if (areSameJets(jet, Jet)) return true;
    }
  return false;
}



bool TopSelectionBDT::isRealMVATop(const Jet& trijetJet1, const Jet& trijetJet2, const Jet& trijetBJet, const std::vector<Jet>& MCtrue_LdgJet,  const std::vector<Jet>& MCtrue_SubldgJet, const std::vector<Jet>& MCtrue_Bjet){
  
  for (size_t k=0; k<MCtrue_Bjet.size(); k++){
    bool same1 = areSameJets(trijetJet1, MCtrue_LdgJet.at(k))       && areSameJets(trijetJet2, MCtrue_SubldgJet.at(k)) && areSameJets(trijetBJet,  MCtrue_Bjet.at(k));
    bool same2 = areSameJets(trijetJet1, MCtrue_SubldgJet.at(k))    && areSameJets(trijetJet2, MCtrue_LdgJet.at(k))    && areSameJets(trijetBJet,  MCtrue_Bjet.at(k));
    if (same1 || same2) return true;
 }
  return false;
}

bool TopSelectionBDT::isRealMVATop(const Jet& trijetJet1, const Jet& trijetJet2, const Jet& trijetBJet, const Jet& MCtrue_LdgJet, const Jet& MCtrue_SubldgJet, const Jet& MCtrue_Bjet){

  bool same1 = areSameJets(trijetJet1, MCtrue_LdgJet)       && areSameJets(trijetJet2, MCtrue_SubldgJet) && areSameJets(trijetBJet,  MCtrue_Bjet);
  bool same2 = areSameJets(trijetJet1, MCtrue_SubldgJet)    && areSameJets(trijetJet2, MCtrue_LdgJet)    && areSameJets(trijetBJet,  MCtrue_Bjet);
  if (same1 || same2) return true;
  return false;

}


int TopSelectionBDT::getTopFromHiggs(TrijetSelection TopCand, const Jet&  MCtrueTopFromH_LdgJet, const Jet& MCtrueTopFromH_SubldgJet, const Jet& MCtrueTopFromH_Bjet){
  size_t size = TopCand.MVA.size();

  if (size < 1) return -1;
  
  for (size_t i=0; i< size; i++)
    {
      if (isRealMVATop(TopCand.Jet1.at(i), TopCand.Jet2.at(i), TopCand.BJet.at(i), MCtrueTopFromH_LdgJet, MCtrueTopFromH_SubldgJet, MCtrueTopFromH_Bjet)) return i;
    }
  
  return -1;
}
  

vector <int> TopSelectionBDT::GetWrongAssignmentTrijetIndex(int matched_index, const std::vector<Jet>& TopCandJet1, const std::vector<Jet>& TopCandJet2, const std::vector<Jet>& TopCandBjet){

  vector <int> WrongAssignmentIndex;
  Jet MCtrue_Jet1 = TopCandJet1.at(matched_index);  
  Jet MCtrue_Jet2 = TopCandJet2.at(matched_index);  
  Jet MCtrue_BJet = TopCandBjet.at(matched_index);  

  for (size_t k=0; k<TopCandBjet.size(); k++){    
    Jet Jet1 = TopCandJet1.at(k);
    Jet Jet2 = TopCandJet2.at(k);
    Jet BJet = TopCandBjet.at(k);

    if (isRealMVATop(Jet1, BJet, Jet2, MCtrue_Jet1, MCtrue_Jet2, MCtrue_BJet) || isRealMVATop(BJet, Jet2, Jet1, MCtrue_Jet1, MCtrue_Jet2, MCtrue_BJet)) WrongAssignmentIndex.push_back(k);
  }

  return WrongAssignmentIndex;
}


TrijetSelection TopSelectionBDT::SortInMVAvalue(TrijetSelection TopCand){
  size_t size = TopCand.MVA.size();

  if (size < 1) return TopCand;

  for (size_t i=0; i<size-1; i++)
    {

      for  (size_t j=i+1; j<size; j++)
	{
	  Jet Jet1_i = TopCand.Jet1.at(i);
	  Jet Jet2_i = TopCand.Jet2.at(i);
	  Jet BJet_i = TopCand.BJet.at(i);
	  double mva_i = TopCand.MVA.at(i);
	  math::XYZTLorentzVector TrijetP4_i = TopCand.TrijetP4.at(i);
	  math::XYZTLorentzVector DijetP4_i = TopCand.DijetP4.at(i);

	  Jet Jet1_j = TopCand.Jet1.at(j);
	  Jet Jet2_j = TopCand.Jet2.at(j);
	  Jet BJet_j = TopCand.BJet.at(j);
	  double mva_j = TopCand.MVA.at(j);
	  math::XYZTLorentzVector TrijetP4_j = TopCand.TrijetP4.at(j);
	  math::XYZTLorentzVector DijetP4_j = TopCand.DijetP4.at(j);

	  if (mva_i >= mva_j) continue;
	  TopCand.Jet1.at(i) = Jet1_j;
	  TopCand.Jet2.at(i) = Jet2_j;
	  TopCand.BJet.at(i) = BJet_j;
	  TopCand.MVA.at(i)  = mva_j;
	  TopCand.TrijetP4.at(i) = TrijetP4_j;
	  TopCand.DijetP4.at(i) = DijetP4_j;

	  TopCand.Jet1.at(j) = Jet1_i;
	  TopCand.Jet2.at(j) = Jet2_i;
	  TopCand.BJet.at(j) = BJet_i;
	  TopCand.MVA.at(j)  = mva_i;
	  TopCand.TrijetP4.at(j) = TrijetP4_i;
	  TopCand.DijetP4.at(j) = DijetP4_i;

	}

    }

  return TopCand;
}


bool TopSelectionBDT::foundFreeBjet(const Jet& trijet1Jet1, const Jet& trijet1Jet2, const Jet& trijet1BJet, const Jet& trijet2Jet1, const Jet& trijet2Jet2, const Jet& trijet2BJet , const std::vector<Jet>& bjets){

  int SumTrijet1 = isBJet(trijet1Jet1, bjets) + isBJet(trijet1Jet2, bjets) + isBJet(trijet1BJet, bjets);
  int SumTrijet2 = isBJet(trijet2Jet1, bjets) + isBJet(trijet2Jet2, bjets) + isBJet(trijet2BJet, bjets);
  
  if ((size_t)(SumTrijet1 + SumTrijet2) != bjets.size()) return true;

  return false;
}


bool TopSelectionBDT::HasMother(const Event& event, const genParticle &p, const int mom_pdgId){
  //  Description: 
  //  Returns true if the particle has a mother with pdgId equal to mom_pdgId.                                                                  
  // Ensure the particle has a mother!                                                                       
  if (p.mothers().size() < 1) return false;

  // For-loop: All mothers                     
  for (size_t iMom = 0; iMom < p.mothers().size(); iMom++)
    {
      
      int mom_index =  p.mothers().at(iMom);
      const genParticle m = event.genparticles().getGenParticles()[mom_index];
      //      const genParticle m = fEvent->genparticles().getGenParticles()[mom_index];
      int motherID = m.pdgId();
      int particleID = p.pdgId();
      if (std::abs(motherID) == mom_pdgId) return true;
      if (std::abs(motherID) == std::abs(particleID)) return HasMother(event, m, mom_pdgId);
      //      else continue;

    }

  return false;
}


const std::vector<Jet> TopSelectionBDT::GetJetsToBeUsedInFit(const JetSelection::Data& jetData,
							     const unsigned int maxNumberOfJets)
{
  // Get the selected jets
  std::vector<Jet> jets = jetData.getSelectedJets();
  
  // Only resize if their size exceeds max allowed value
  if (jets.size() > maxNumberOfJets) jets.resize(maxNumberOfJets);
  return jets;
}


const std::vector<Jet> TopSelectionBDT::GetBjetsToBeUsedInFit(const BJetSelection::Data& bjetData,
							      const unsigned int maxNumberOfBJets, 
							      const std::string jetSortType)
{
  // If there are some bjets use them (depends on cuts)
  std::vector<Jet> bjetsForFit      = bjetData.getSelectedBJets();
  const unsigned int nSelectedBJets = bjetData.getSelectedBJets().size();

  // Append the vector of all failed bjets to the end of the bjets vector
  // Use case: QCD Measurement where we invert at least 1 b-jet => may have less than 3 b-jets available (min for di-top fit and inv mass) 
  if (bjetsForFit.size() < maxNumberOfBJets)
    {      

      std::vector<Jet> failedBJets;
      if (jetSortType.compare("Random") == 0 ) failedBJets = bjetData.getFailedBJetCandsShuffled();
      else if  (jetSortType.compare("AscendingPt") == 0 ) failedBJets = bjetData.getFailedBJetCandsAscendingPt();
      else if  (jetSortType.compare("DescendingPt") == 0 ) failedBJets = bjetData.getFailedBJetCandsDescendingPt();
      else if  (jetSortType.compare("AscendingBDiscriminator") == 0 ) failedBJets = bjetData.getFailedBJetCandsAscendingDiscr();
      else if  (jetSortType.compare("DescendingBDiscriminator") == 0 ) failedBJets = bjetData.getFailedBJetCandsDescendingDiscr();
      else
	{
	  throw hplus::Exception("logic") << "Uknown jet sort type \"" << jetSortType << "\" passed to TopSelection class. "
					  << "Please select one of the following:\n\t\"Random\", \"AscendingPt\", \"DescendingPt\", \"AscendingBDiscriminator\", \"DescendingBDiscriminator\".";
	}

      // Save the failed bjets that will be used to replace bjets in top fit (for studying their properties)
      const unsigned int nFailedBJetsUsedAsBJetsInFit = maxNumberOfBJets - nSelectedBJets;
      myFailedBJetsUsedAsBJetsInFit = failedBJets;
      myFailedBJetsUsedAsBJetsInFit.resize(nFailedBJetsUsedAsBJetsInFit);
      if (0) std::cout << "nFailedBJetsUsedAsBJetsInFit = " << maxNumberOfBJets << " - " << nSelectedBJets << " = " << nFailedBJetsUsedAsBJetsInFit << std::endl;

      // Now insert the customly sorted failed bjet vector to the end of the selected bjets vector
      bjetsForFit.insert(bjetsForFit.end(), failedBJets.begin(), failedBJets.end()); 
    }


  // Truncate the bjets vector to correct size
  if (bjetsForFit.size() > maxNumberOfBJets) bjetsForFit.resize(maxNumberOfBJets);

  // Finally sort by descending pt value (http://en.cppreference.com/w/cpp/algorithm/sort)      
  std::sort(bjetsForFit.begin(), bjetsForFit.end(), [](const Jet& a, const Jet& b){return a.pt() > b.pt();});

  return bjetsForFit;
}

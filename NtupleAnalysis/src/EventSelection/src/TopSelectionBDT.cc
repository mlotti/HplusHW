// -*- c++ -*-
#include "EventSelection/interface/TopSelectionBDT.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
//#include "Framework/interface/makeTH.h"

#include "Math/VectorUtil.h"

TopSelectionBDT::Data::Data()
:
  bPassedSelection(false),
  fTrijet1Jet1(),
  fTrijet1Jet2(),
  fTrijet1BJet(),
  fTrijet1Dijet_p4(),
  fTrijet1_p4(), 
  fTrijet2Jet1(),
  fTrijet2Jet2(),
  fTrijet2BJet(),
  fTrijet2Dijet_p4(),
  fTrijet2_p4(),
  fTetrajetBJet(),
  fTetrajet1_p4(),
  fTetrajet2_p4(),
  fLdgTetrajet_p4(),
  fSubldgTetrajet_p4()
{ }

TopSelectionBDT::Data::~Data() { }


TopSelectionBDT::TopSelectionBDT(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
  : BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
    // Input parameters
    cfg_MVACut(config, "MVACut"),
    cfg_NjetsMaxCut(config, "NjetsMaxCut"),
    cfg_ReplaceJetsWithGenJets(config.getParameter<bool>("ReplaceJetsWithGenJets")),
    // Event counter for passing selection
    cPassedTopSelectionBDT(fEventCounter.addCounter("passed top selection ("+postfix+")")),
    // Sub counters
    cSubAll(fEventCounter.addSubCounter("top selection ("+postfix+")", "All events")),
    cSubPassedBDTCut(fEventCounter.addSubCounter("top selection ("+postfix+")", "Passed BDT cut"))
{
  initialize(config);
  nSelectedBJets = -1;
}

TopSelectionBDT::TopSelectionBDT(const ParameterSet& config)
: BaseSelection(),
  // Input parameters
  cfg_MVACut(config, "MVACut"),
  cfg_NjetsMaxCut(config, "NjetsMaxCut"),
  cfg_ReplaceJetsWithGenJets(config.getParameter<bool>("ReplaceJetsWithGenJets")),  
  // Event counter for passing selection
  cPassedTopSelectionBDT(fEventCounter.addCounter("passed top selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("top selection", "All events")),
  cSubPassedBDTCut(fEventCounter.addSubCounter("top selection", "Passed BDT cut"))
{
  initialize(config);
  bookHistograms(new TDirectory());
}

TopSelectionBDT::~TopSelectionBDT() {
  
  // Histograms (1D)
  delete hBDTresponse;
  delete hTopCandMass;
  //  delete hTetrajetMass;
  delete hSelectedTopPt1;
  delete hSelectedMatchedTopPt1;
  delete hSelectedTopPt2;
  delete hSelectedMatchedTopPt2;
  delete hLdgBjetPt;
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
  delete hTopQuarkPt_MatchedBDT;
  delete hTopQuarkPt_Matched;
  delete hTrijetPt_BDT;
  delete hTrijetMass_NotMatchedBDT;
  delete hAllTopQuarkPt_Matched;
  delete hAllTopQuarkPt_MatchedBDT;
  delete hAllTopQuarkPt_jjbMatched;
  delete hAllTopQuarkPt_jjbMatchedBDT;

  delete hTopQuarkPt_BDT;

  delete hLdgTrijetFake;
  delete hLdgTrijetFake_BDT;
  delete hLdgTrijetFakeJJB;
  delete hLdgTrijetFakeJJB_BDT;

  delete hBDTmultiplicity;
  delete hTrijetTopMatchedNonJJBMatched_Mass;
  delete hTrijetTopMatched_Mass;
  delete hTrijetTopJJBMatched_Mass;
  delete hMatchedBDTmult;
  delete hMatchedjjbBDTmult;
  delete hEventTrijetPt_BDT;
  delete hEventTrijetPt_MatchedBDT;
  delete hEventTrijetPt_MatchedjjbBDT;

  delete hEventTrijetPt2T_BDT;
  delete hEventTrijetPt2T_MatchedjjbBDT;

  delete hTrijetFakePt;
  delete hTrijetFakePt_BDT;
  delete hTrijetFakeJJBPt;
  delete hTrijetFakeJJBPt_BDT;

  delete hDeltaRMinTopTrijet;
  delete hEventTrijetPt2T_Matchedjjb;
  delete hAllTopQuarkPt_NonMatched;
  delete hAllTopQuarkMass_NonMatched;

  delete hEventTrijetPt;
  delete hEventTrijetPt2T;
  
  delete hRealSelectedTopMult;
  delete hTrijetMultiplicity;
  delete hTrijetBDT_Mass;
  delete hTrijetJJBMatched_BDTvalue;
  delete hTrijetJJBNonMatched_BDTvalue;

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
  // Histograms (2D)
  delete hNjetsVsNTrijets_beforeBDT;
  delete hNjetsVsNTrijets_afterBDT;

  delete hDeltaMVAmaxVsTrijetPassBDTvalue;
  delete hDeltaMVAminVsTrijetPassBDTvalue;
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

  // Read the xml file
  reader->BookMVA("BTDG method", "/uscms_data/d3/skonstan/CMSSW_8_0_28/src/HiggsAnalysis/NtupleAnalysis/src/TopReco/work/TMVA_BDT/test/weights/TMVAClassification_BDTG.weights.xml");
}

void TopSelectionBDT::bookHistograms(TDirectory* dir) {

  // Fixed binning
  
  const int nPtBins       = 2 * fCommonPlots->getPtBinSettings().bins();
  const double fPtMin     = 2 * fCommonPlots->getPtBinSettings().min();
  const double fPtMax     = 2 * fCommonPlots->getPtBinSettings().max();

  const int  nEtaBins     = fCommonPlots->getEtaBinSettings().bins();
  const float fEtaMin     = fCommonPlots->getEtaBinSettings().min();
  const float fEtaMax     = fCommonPlots->getEtaBinSettings().max();

  // const int nDEtaBins     = fCommonPlots->getDeltaEtaBinSettings().bins();
  // const double fDEtaMin   = fCommonPlots->getDeltaEtaBinSettings().min();
  // const double fDEtaMax   = fCommonPlots->getDeltaEtaBinSettings().max();

  // const int nDPhiBins     = fCommonPlots->getDeltaPhiBinSettings().bins();
  // const double fDPhiMin   = fCommonPlots->getDeltaPhiBinSettings().min();
  // const double fDPhiMax   = fCommonPlots->getDeltaPhiBinSettings().max();

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
  hBDTresponse       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"BDTGresponse",";BDTG response", 40, -1., 1.) ; 
  hTopCandMass       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"TopCandMass",";M (GeVc^{-2})",nTopMassBins, fTopMassMin, fTopMassMax);
  hTetrajetMass      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"TetrajetMass",";M (GeVc^{-2})",300, 0,3000);
  hSelectedTopPt1            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"SelectedTopPt1",";p_{T} (GeVc^{-1})",100,0.0,1000);
  hSelectedMatchedTopPt1     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"SelectedMatchedTopPt1",";p_{T} (GeVc^{-1})",100,0.0,1000);
  hSelectedTopPt2            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"SelectedTopPt2",";p_{T} (GeVc^{-1})",100,0.0,1000);
  hSelectedMatchedTopPt2     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"SelectedMatchedTopPt2",";p_{T} (GeVc^{-1})",100,0.0,1000);

  hLdgBjetPt            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"LdgBjetPt",";p_{T} (GeVc^{-1})",nPtBins     , fPtMin     , fPtMax);

  hTetrajetBJetPt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetPt"    ,";p_{T} (GeV/c)"      , nPtBins     , fPtMin     , fPtMax);
  hTetrajetBJetEta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetEta"   ,";#eta"               , nEtaBins    , fEtaMin    , fEtaMax);
  hTetrajetBJetBDisc  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetBDisc" ,";b-tag discriminator", nBDiscBins  , fBDiscMin  , fBDiscMax);
  hTetrajetPt         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "TetrajetPt"       , ";p_{T} (GeV/c)"      , nPtBins     , fPtMin     , fPtMax);
  hTetrajetMass       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "TetrajetMass"     , ";M (GeV/c^{2})"      , nInvMassBins, fInvMassMin, fInvMassMax);
  hTetrajetEta        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "TetrajetEta"      , ";#eta"               , nEtaBins    , fEtaMin    , fEtaMax);

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
  hLdgTrijetDijetDeltaR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "LdgTrijetDijetDR"  , ";#Delta R(j_{1},j_{2})"  , nDRBins     , fDRMin     , fDRMax);


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
  hSubldgTrijetDijetDeltaR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "SbldgTrijetDijetDR"  , ";#Delta R(j_{1},j_{2})"  , nDRBins     , fDRMin     , fDRMax);

  hLdgTrijetTopMassWMassRatio      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetTopMassWMassRatio"       ,";R_{32}", 100 , 0.0, 10.0);
  hSubldgTrijetTopMassWMassRatio      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetTopMassWMassRatio"       ,";R_{32}", 100 , 0.0, 10.0);



  hTopQuarkPt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopQuarkPt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hTopQuarkPt_MatchedBDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopQuarkPt_MatchedBDT"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hTopQuarkPt_Matched    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopQuarkPt_Matched"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hTrijetPt_BDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetPt_BDT"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hTrijetMass_NotMatchedBDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetMass_NotMatchedBDT"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hAllTopQuarkPt_Matched    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AllTopQuarkPt_Matched"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hTopQuarkPt_BDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TopQuarkPt_BDT"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hAllTopQuarkPt_MatchedBDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AllTopQuarkPt_MatchedBDT"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hAllTopQuarkPt_jjbMatched    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AllTopQuarkPt_jjbMatched"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hAllTopQuarkPt_jjbMatchedBDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AllTopQuarkPt_jjbMatchedBDT"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);

  hLdgTrijetFake    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetFake"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hLdgTrijetFake_BDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetFake_BDT"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hLdgTrijetFakeJJB    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetFakeJJB"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hLdgTrijetFakeJJB_BDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetFakeJJB_BDT"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);


  hBDTmultiplicity    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "BDTmultiplicity",";Trijet pass BDT mult", 50, 0, 50);
  hTrijetTopMatchedNonJJBMatched_Mass        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetMass_TopMatchedNonJJBMatched"     ,";M (GeV/c^{2})", nTopMassBins, fTopMassMin, fTopMassMax/2);
  hTrijetTopMatched_Mass        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetTopMatched_Mass"     ,";M (GeV/c^{2})", nTopMassBins, fTopMassMin, fTopMassMax/2);
  hTrijetTopJJBMatched_Mass        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetTopJJBMatched_Mass"     ,";M (GeV/c^{2})", nTopMassBins, fTopMassMin, fTopMassMax/2);
  hMatchedBDTmult    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "MatchedBDTmult",";truth matched Trijet pass BDT mult", 3, 0, 3);
  hMatchedjjbBDTmult    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "MatchedjjbBDTmult",";truth matched Trijet pass BDT mult", 3, 0, 3);
  hEventTrijetPt_BDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "EventTrijetPt_BDT"   ,";p_{T} (GeV/c)", 2*nPtBins     , fPtMin     , fPtMax);
  hEventTrijetPt_MatchedBDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "EventTrijetPt_MatchedBDT"   ,";p_{T} (GeV/c)", 2*nPtBins     , fPtMin     , fPtMax);
  hEventTrijetPt_MatchedjjbBDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "EventTrijetPt_MatchedjjbBDT"   ,";p_{T} (GeV/c)", 2*nPtBins     , fPtMin     , fPtMax);

  hEventTrijetPt2T_BDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "EventTrijetPt2T_BDT"   ,";p_{T} (GeV/c)", 2*nPtBins     , fPtMin     , fPtMax);
  hEventTrijetPt2T_MatchedjjbBDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "EventTrijetPt2T_MatchedjjbBDT"   ,";p_{T} (GeV/c)", 2*nPtBins     , fPtMin     , fPtMax);

  hTrijetFakePt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetFakePt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hTrijetFakePt_BDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetFakePt_BDT"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hTrijetFakeJJBPt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetFakeJJBPt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hTrijetFakeJJBPt_BDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetFakeJJBPt_BDT"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hDeltaRMinTopTrijet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "DeltaRMinTopTrijet"  , ";#Delta R(top,trijet)"  , 60    , 0     , 1.5);

  hEventTrijetPt2T_Matchedjjb     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "EventTrijetPt2T_Matchedjjb", ";p_{T} (GeV/c)", 2*nPtBins     , fPtMin     , fPtMax);
  hAllTopQuarkPt_NonMatched       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AllTopQuarkPt_NonMatched"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hAllTopQuarkMass_NonMatched     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AllTopQuarkMass_NonMatched"   ,";M (GeV/c^{2})", nTopMassBins, fTopMassMin, 400);

  hEventTrijetPt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "EventTrijetPt"   ,";p_{T} (GeV/c)", 2*nPtBins     , fPtMin     , fPtMax);
  hEventTrijetPt2T    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "EventTrijetPt2T"   ,";p_{T} (GeV/c)", 2*nPtBins     , fPtMin     , fPtMax);

  hRealSelectedTopMult =   fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "RealSelectedTopMult",";Selected truth matched Trijets", 3, 0, 3);

  hTrijetMultiplicity     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetMultiplicity",";Trijet multiplicity", 670, 0, 670);
  hTrijetBDT_Mass        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetBDT_Mass"     ,";M (GeV/c^{2})", nTopMassBins, fTopMassMin, fTopMassMax);
  hTrijetJJBMatched_BDTvalue       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"TrijetJJBMatched_BDTvalue",";BDTG response", 40, -1., 1.) ;
  hTrijetJJBNonMatched_BDTvalue       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"TrijetJJBNonMatched_BDTvalue",";BDTG response", 40, -1., 1.) ;

  hNjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"JetMultiplicity",";Jet Multiplicity", 8,6,14);
  hDeltaMVAmax_MCtruth_SameObjFakes       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaMVAmax_MCtruth_SameObjFakes",";#Delta BDTG response", 100, -2., 2.) ;
  hAbsDeltaMVAmax_MCtruth_SameObjFakes      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"AbsDeltaMVAmax_MCtruth_SameObjFakes",";#Delta BDTG response", 50, 0, 2.) ;


  hFakeInTopDirMult     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "FakeInTopDirMult",";Fake Trijets in Top Direction mult", 670, 0, 670);;

  hDeltaMVAmax_MCtruth_SameObjFakesPassBDT       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaMVAmax_MCtruth_SameObjFakesPassBDT",";#Delta BDTG response", 100, -2., 2.);
  hDeltaMVAmin_MCtruth_SameObjFakes       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaMVAmin_MCtruth_SameObjFakes",";#Delta BDTG response", 100, -2., 2.) ;
  hDeltaMVAmin_MCtruth_SameObjFakesPassBDT       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"DeltaMVAmin_MCtruth_SameObjFakesPassBDT",";#Delta BDTG response", 100, -2., 2.) ;
  hMatchedTrijetMult_JetsGT9 =   fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "MatchedTrijetMult_JetsGT9",";Trijet Multiplicity", 3, 0, 3);
  hMatchedTrijetMult_JetsInc =   fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "MatchedTrijetMult_JetsInc",";Trijet Multiplicity", 3, 0, 3);
  hMVAvalue_DeltaMVAgt1       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir,"MVAvalue_DeltaMVAgt1",";BDTG response", 40, -1., 1.) ;
  hMatchedPassBDTmult_SameObjFakes       =   fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "MatchedPassBDTmult_SameObjFakes",";Selected truth matched Trijets", 3, 0, 3);

  hAllTrijetPassBDT_pt              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AllTrijetPassBDT_pt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hAllTrijetPassBDTbPassCSV_pt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AllTrijetPassBDTbPassCSV_pt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hTrijetPassBDT_bDisc              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TrijetPassBDT_bDisc",";b-tag discr." , nBDiscBins  , fBDiscMin  , fBDiscMax);
  
  //next
  // Histograms (2D) 
  hTrijetCountForBDTcuts           = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir,"TrijetCountVsBDTcuts",";BDT cut value;Trijet multiplicity", 19, -0.95,0.95, 200,0,200);
  hNjetsVsNTrijets_beforeBDT       = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "NjetsVsNTrijets_beforeBDT"  ,";Jet Multiplicity;Trijets_beforeBDT multiplicity", 8,6,14, 670, 0, 670);
  hNjetsVsNTrijets_afterBDT        = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "NjetsVsNTrijets_afterBDT"  ,";Jet Multiplicity;Trijets_afterBDT multiplicity", 8,6,14, 60, 0, 60);
  hDeltaMVAmaxVsTrijetPassBDTvalue = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "DeltaBDTmaxVsTrijetPassBDTvalue", ";#Delta BDTG_{max} response;BDTG response", 100, -2., 2., 40, -1., 1.) ;
  hDeltaMVAminVsTrijetPassBDTvalue = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "DeltaBDTminVsTrijetPassBDTvalue", ";#Delta BDTG_{min} response;BDTG response", 100, -2., 2., 40, -1., 1.) ;

  return;
}

TopSelectionBDT::Data TopSelectionBDT::silentAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  ensureSilentAnalyzeAllowed(event.eventID());
  nSelectedBJets = bjetData.getSelectedBJets().size();

  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, jetData.getSelectedJets(), bjetData.getSelectedBJets());
  enableHistogramsAndCounters();
  return myData;
}


TopSelectionBDT::Data TopSelectionBDT::analyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  ensureAnalyzeAllowed(event.eventID());
  nSelectedBJets = bjetData.getSelectedBJets().size();

  // Ready to analyze
  TopSelectionBDT::Data data = privateAnalyze(event, jetData.getSelectedJets(), bjetData.getSelectedBJets());

  // Send data to CommonPlots
  // if (fCommonPlots != nullptr) fCommonPlots->fillControlPlotsAtTopSelectionBDT(event, data); //fixme
  return data;
}


TopSelectionBDT::Data TopSelectionBDT::privateAnalyze(const Event& event, const std::vector<Jet> jets, const std::vector<Jet> bjets) {
  Data output;
  cSubAll.increment();
  
  // Sanity check
  if (bjets.size() < 3) return output;

  if (0) std::cout << "\nnJets = " << jets.size() << ", \033[1;31mnBJets = " << bjets.size() << "\033[0m" << std::endl;
  hNjets -> Fill(jets.size());

  // In order to replace PF Jets with GenJets event must be MC and user must enable the dedicated flag
  bool replaceJets = event.isMC()*cfg_ReplaceJetsWithGenJets; // fixme - not tested

  //================================================================================================  
  // MC Matching  
  //================================================================================================
  TrijetSelection mcTrueTrijets;
  bool doMatching = true;
  std::vector<genParticle> GenTops;
  std::vector<genParticle> GenTops_BQuark;
  std::vector<genParticle> GenTops_LdgQuark;
  std::vector<genParticle> GenTops_SubldgQuark;

  vector <Jet> MCtrue_LdgJet, MCtrue_SubldgJet, MCtrue_Bjet, MC_BJets;
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

    // Skip matcing if top does not decay to b
    doMatching = (GenTops_BQuark.size() == GenTops.size()); 

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
	      }// if (isGenuine)
	    
	    // Top quark matched with a trijet
	    FoundTop.push_back(isGenuine);
	  }//For-loop: All top-quarks
      }// if (doMatching){
  }// event.isMC()
  
  //================================================================================================  
  // Top Candidates
  //================================================================================================  
  // Array with 19 different BDT cut values (later use)
  int mva[19];
  float mvaCut[19];
  float cut = -0.9;

  // For-loop: All BDT cut values
  for (int k=0; k<19; k++)
    {
      mva[k] = 0;
      mvaCut[k] = cut;
      cut = cut + 0.1;
    }// fixme: convert to vector

  // Definitions
  vector <double> TopCandMVA;
  vector <Jet> TopCandJet1, TopCandJet2, TopCandBJet;
  vector <math::XYZTLorentzVector> TopCandP4;
  bool isMaxIndex0, isMaxIndex1, isMaxIndex2;
  int indexb = 0;

  // For-loop: All jets (1)
  for (auto& bjet: jets)
    {
      indexb++;
      // Restrict max number of jets considered?
      isMaxIndex0 = !cfg_NjetsMaxCut.passedCut(indexb);
      int index1 = 0;
      
      // For-loop: All jets (Nested)
      for (auto& jet1: jets)
	{
	  index1++;
	  // Restrict max number of jets considered?
	  isMaxIndex1 = !cfg_NjetsMaxCut.passedCut(index1);
	  int index2 = 0;
	  
	  // Skip if jet1 is same as bjet
	  if (areSameJets(jet1, bjet)) continue;

	  // For-loop: All jets (Doubly-Nested)
	  for (auto& jet2: jets)
	    {
	      index2++;
	      // Restrict max number of jets considered?
	      isMaxIndex2 = !cfg_NjetsMaxCut.passedCut(index2);
	      if (isMaxIndex0 || isMaxIndex1 || isMaxIndex2) continue;

	      // Do not consider duplicate compinations
	      if (index2 < index1) continue;

	      // Skip if jet2 is same as jet1, or jet2 same as bjet
	      if (areSameJets(jet2,  jet1)) continue;
	      if (areSameJets(jet2,  bjet)) continue;
	      
	      // Get 4-momentum of top (trijet) and W (dijet)
	      math::XYZTLorentzVector Trijet_p4, Dijet_p4;
	      Trijet_p4 = bjet.p4() + jet1.p4() + jet2.p4();
	      Dijet_p4  = jet1.p4() + jet2.p4();
	      
	      // Calculate variables
	      double dr_sd = ROOT::Math::VectorUtil::DeltaR( jet1.p4(), jet2.p4());
	      double softDrop_n2 = min(jet2.pt(), jet1.pt()) / ( (jet2.pt() + jet1.pt()) * dr_sd * dr_sd);

	      // Calculate our 19 discriminating variables for MVA use
	      TrijetPtDR               = Trijet_p4.Pt() * ROOT::Math::VectorUtil::DeltaR( Dijet_p4  , bjet.p4() );
	      TrijetDijetPtDR          = Dijet_p4.Pt()  * ROOT::Math::VectorUtil::DeltaR( jet1.p4() , jet2.p4() );
	      TrijetBjetMass           = bjet.p4().M();
	      TrijetLdgJetBDisc        = jet1.bjetDiscriminator();
	      TrijetSubldgJetBDisc     = jet2.bjetDiscriminator();
	      TrijetBJetLdgJetMass     = (bjet.p4() + jet1.p4()).M();
	      TrijetBJetSubldgJetMass  = (bjet.p4() + jet2.p4()).M();
	      TrijetMass               = Trijet_p4.M();
	      TrijetDijetMass          = Dijet_p4.M();
	      TrijetBJetBDisc          = bjet.bjetDiscriminator();
	      TrijetSoftDrop_n2        = softDrop_n2;
	      TrijetLdgJetCvsL         = jet1.pfCombinedCvsLJetTags();
	      TrijetSubldgJetCvsL      = jet2.pfCombinedCvsLJetTags();
	      TrijetLdgJetPtD          = jet1.QGTaggerAK4PFCHSptD();
	      TrijetSubldgJetPtD       = jet2.QGTaggerAK4PFCHSptD();
	      TrijetLdgJetAxis2        = jet1.QGTaggerAK4PFCHSaxis2();
	      TrijetSubldgJetAxis2     = jet2.QGTaggerAK4PFCHSaxis2();
	      TrijetLdgJetMult         = jet1.QGTaggerAK4PFCHSmult();
	      TrijetSubldgJetMult      = jet2.QGTaggerAK4PFCHSmult();
	
	      // Evaluate the MVA discriminator value
	      float MVAoutput = reader->EvaluateMVA("BTDG method");

	      // Fill top candidate BDT values
	      hBDTresponse -> Fill(MVAoutput);
	      TopCandMVA.push_back(MVAoutput);
	      TopCandP4.push_back(Trijet_p4);
	      TopCandJet1.push_back(getLeadingSubleadingJet(jet1,jet2,"leading"));
	      TopCandJet2.push_back(getLeadingSubleadingJet(jet1,jet2,"subleading"));
	      TopCandBJet.push_back(bjet);
	      
	      // Determine top candidate multiplicity after BDT cut
	      for (int m=0; m<19; m++) 
		{
		  if (MVAoutput > mvaCut[m]) mva[m] ++; 
		}

	    }// For-loop: All jets (Doubly-Nested)
	}// For-loop: All jets (Nested)
    }// For-loop: All jets

  // Fill Number of trijets passing BDT vs MVA cut value
  for (int m=0; m<19; m++) hTrijetCountForBDTcuts -> Fill(mvaCut[m], mva[m]);

  if (0) std::cout<<"Number of Top Candidates: "<<TopCandMVA.size()<<std::endl;
  // Definitions
  double MVAmax1 = -999.999,  MVAmax2 = -999.999;
  Jet trijet1Jet1, trijet1Jet2, trijet1BJet;
  Jet trijet2Jet1, trijet2Jet2, trijet2BJet;
  math::XYZTLorentzVector trijet1, trijet2;
  Jet leadingTrijetJet1, leadingTrijetJet2, leadingTrijetBJet;
  Jet subleadingTrijetJet1, subleadingTrijetJet2, subleadingTrijetBJet;
  math::XYZTLorentzVector leadingTrijetP4, subleadingTrijetP4, tetrajetP4;
  int passBDT = 0;  

  // For-loop: All top candidates 
  for (size_t i = 0; i < TopCandMVA.size(); i++)
    {
      double mvaValue = TopCandMVA.at(i);

      // Does this top candidate Pass our BDT cut?
      if (cfg_MVACut.passedCut(mvaValue) )
	{ 
	  passBDT ++;
	  hTrijetBDT_Mass -> Fill(TopCandP4.at(i).M());
	}
      
      // Find Leading in BDT value trijet
      if (mvaValue < MVAmax1) continue;

      // Store new max
      MVAmax1 = mvaValue;

      // Save top candidate subjetss
      trijet1Jet1 = TopCandJet1.at(i);
      trijet1Jet2 = TopCandJet2.at(i);
      trijet1BJet = TopCandBJet.at(i);

      // Save top candidate 4-momentum
      trijet1 = TopCandP4.at(i);

    }// For-loop: All top candidates 


  // Find Subleading in BDT value trijet
  if (TopCandMVA.size() > 1)
    {
      // For-loop: All top candidates
      for (size_t i = 0; i < TopCandMVA.size(); i++)
	{
	  bool same0 = areSameJets(trijet1BJet, TopCandJet1.at(i)) || areSameJets(trijet1BJet, TopCandJet2.at(i)) || areSameJets(trijet1BJet, TopCandBJet.at(i));
	  bool same1 = areSameJets(trijet1Jet1, TopCandJet1.at(i)) || areSameJets(trijet1Jet1, TopCandJet2.at(i)) || areSameJets(trijet1Jet1, TopCandBJet.at(i));
	  bool same2 = areSameJets(trijet1Jet2, TopCandJet1.at(i)) || areSameJets(trijet1Jet2, TopCandJet2.at(i)) || areSameJets(trijet1Jet2, TopCandBJet.at(i));

	  // Skip top candidates with same jets as Leading in BDT trijet
	  if (same0 || same1 || same2) continue; 
	  
	  double mvaValue = TopCandMVA.at(i);
	  
	  // Find subleading in BDT value trijet
	  if (mvaValue < MVAmax2) continue;
	  MVAmax2 = mvaValue;

	  // Save top candidate subjets
	  trijet2Jet1 = TopCandJet1.at(i);
	  trijet2Jet2 = TopCandJet2.at(i);
	  trijet2BJet = TopCandBJet.at(i);

	  // Save top candidate 4-momentum
	  trijet2     = TopCandP4.at(i);

	}// For-loop: All top candidates

    }// if (TopCandMVA.size() > 1)


  //================================================================================================  
  // Tetrajet candidates
  //================================================================================================  
  Jet tetrajetBjet;
  double tetrajetBjetPt_max = -999.99;
  
  // Get Leading, Subleading in Pt selected trijet  // fixme: Use Function!
  if(trijet1.Pt() > trijet2.Pt())
    {
      leadingTrijetP4 = trijet1;
      
      if (trijet1Jet1.pt() > trijet1Jet2.pt())
	{
	  leadingTrijetJet1 = trijet1Jet1;
	  leadingTrijetJet2 = trijet1Jet2;
	}
      else
	{
	  leadingTrijetJet1 = trijet1Jet2;
	  leadingTrijetJet2 = trijet1Jet1;
	}
      leadingTrijetBJet  = trijet1BJet;
      subleadingTrijetP4 = trijet2;
      
      if (trijet2Jet1.pt() > trijet2Jet2.pt())
	{
	  subleadingTrijetJet1 = trijet2Jet1;
	  subleadingTrijetJet2 = trijet2Jet2;
	}
      else
	{
	  subleadingTrijetJet1 = trijet2Jet2;
	  subleadingTrijetJet2 = trijet2Jet1;
	}
	subleadingTrijetBJet = trijet2BJet;
    }
  else // if(trijet2.Pt() > trijet1.Pt())
    {
      leadingTrijetP4 = trijet2;
      if (trijet2Jet1.pt() > trijet2Jet2.pt())
	{
	  leadingTrijetJet1 = trijet2Jet1;
	  leadingTrijetJet2 = trijet2Jet2;
	}
      else
	{
	  leadingTrijetJet1 = trijet2Jet2;
	  leadingTrijetJet2 = trijet2Jet1;
	}
      leadingTrijetBJet  = trijet2BJet;
      subleadingTrijetP4 = trijet1;

      if (trijet1Jet1.pt() > trijet1Jet2.pt())
	{
	  subleadingTrijetJet1 = trijet1Jet1;
	  subleadingTrijetJet2 = trijet1Jet2;
	}
      else 
	{
	  subleadingTrijetJet1 = trijet1Jet2;
	  subleadingTrijetJet2 = trijet1Jet1;
	}
      subleadingTrijetBJet = trijet1BJet;
    }

  
  //Leading free bjet 
  double ptBjet_max = -999.999;

  // For-loop: All selected b-jets
  for (auto& bjet: bjets)
    {
      // Store max pt
      if (bjet.pt() > ptBjet_max) ptBjet_max = bjet.pt();
      
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
  // Top-tagging Efficiency (per selected top)
  //================================================================================================
  bool passBDT1       = cfg_MVACut.passedCut(MVAmax1);
  bool passBDT2       = cfg_MVACut.passedCut(MVAmax2);
  bool passBDT1or2    = cfg_MVACut.passedCut(max(MVAmax1, MVAmax2));
  bool passBDTboth    = passBDT1*passBDT2;
  bool inTopDir1      = false;
  bool inTopDir2      = false;
  bool inTopDir1or2   = false;
  bool realtop1       = false;
  bool realtop2       = false;
  bool realtopBoth    = false;
  bool TopMatched     = true;
  bool realtop1qqb    = false;
  bool realtop2qqb    = false;
  bool realtopBothqqb = false;

  if (event.isMC() && doMatching)
    {
      
      // Definitions
      realtop1   = false;
      realtop2   = false;
      
      // For-loop: All top-quarks
      for (auto& top: GenTops)
	{

	  // Find dR(t, trijet)
	  double dR_t1 = ROOT::Math::VectorUtil::DeltaR(top.p4(), trijet1);
	  double dR_t2 = ROOT::Math::VectorUtil::DeltaR(top.p4(), trijet2);

	  // Is the trijet in top's direction
	  if (dR_t1 < 0.4 ) realtop1 = true; 
	  if (dR_t2 < 0.4 ) realtop2 = true; 

	  // Is the trijet matched?
	  if (min(dR_t1, dR_t2) > 0.4) TopMatched = false;

	  // Define booleans
	  bool inTopDir1    = (dR_t1 < 0.4);
	  bool inTopDir2    = (dR_t2 < 0.4);
	  bool inTopDir1or2 = min(dR_t1, dR_t2) < 0.4;

	  // Fill histograms
	  hTopQuarkPt ->Fill(top.pt());
	  if ( passBDT1*inTopDir1 || passBDT2*inTopDir2 ) hTopQuarkPt_MatchedBDT->Fill(top.pt());
	  if ( inTopDir1or2 ) hTopQuarkPt_Matched->Fill(top.pt());
	  if ( passBDT1or2 ) hTopQuarkPt_BDT->Fill(top.pt());
	}

      if (0) cout << inTopDir1 << inTopDir2 << inTopDir1or2 << endl;

      // Assign booleans
      realtopBoth    = realtop1*realtop2;
      realtop1qqb    = isRealMVATop(trijet1Jet1, trijet1Jet2, trijet1BJet, MCtrue_LdgJet,  MCtrue_SubldgJet, MCtrue_Bjet);  
      realtop2qqb    = isRealMVATop(trijet2Jet1, trijet2Jet2, trijet2BJet, MCtrue_LdgJet,  MCtrue_SubldgJet, MCtrue_Bjet);
      realtopBothqqb = realtop1qqb*realtop2qqb;
      
      //================================================================================================  
      // Top-tagging Efficiency (per top candidate)
      //================================================================================================
      vector <int> MatchedTop_index, MatchedJJB_index;
      
      // For-loop: All top quarks
      for (size_t j=0; j<GenTops.size(); j++)
	{	
	  
	  // Get the genParicle
	  genParticle top;
	  top =GenTops.at(j);

	  // Definitions
	  int matchedTop_index = -1, matchedJJB_index = -1;
	  double dR_tmin  = 999.999;
	  bool genuineTop = false; 
	  
	  // For-loop: All top candidates
	  for (size_t i = 0; i < TopCandMVA.size(); i++)
	    {
	      math::XYZTLorentzVector trijet;
	      trijet = TopCandP4.at(i);

	      // Calculate dR(t, trijet)
	      double dR_t = ROOT::Math::VectorUtil::DeltaR(top.p4(), trijet);
	      
	      // Find minimum dR
	      if (dR_t < dR_tmin)
		{
		matchedTop_index = i;
		dR_tmin = dR_t;
		}	
	      
	      // Find index of matched trijets
	      bool isMatched = FoundTop.at(j);
	      bool isOnlyMatched = (MCtrue_Bjet.size() == 1);
	      bool sizesAgree    = (MCtrue_Bjet.size() == GenTops.size());

	      if ( isMatched*isOnlyMatched )
		{

		  bool same1 = areSameJets(TopCandJet1.at(i), MCtrue_LdgJet.at(0))    && areSameJets(TopCandJet2.at(i), MCtrue_SubldgJet.at(0)) && areSameJets(TopCandBJet.at(i),  MCtrue_Bjet.at(0));
		  bool same2 = areSameJets(TopCandJet1.at(i), MCtrue_SubldgJet.at(0)) && areSameJets(TopCandJet2.at(i), MCtrue_LdgJet.at(0))    && areSameJets(TopCandBJet.at(i),  MCtrue_Bjet.at(0));
		  
		  if (same1 || same2)
		    {
		      genuineTop = true;
		      matchedJJB_index = i;
		      MatchedJJB_index.push_back(matchedJJB_index);
		    }
		}// if ( isMatched*isOnlyMatched )

	      if ( isMatched*sizesAgree )
		{
		  bool same1 = areSameJets(TopCandJet1.at(i), MCtrue_LdgJet.at(j))    && areSameJets(TopCandJet2.at(i), MCtrue_SubldgJet.at(j)) && areSameJets(TopCandBJet.at(i),  MCtrue_Bjet.at(j));
		  bool same2 = areSameJets(TopCandJet1.at(i), MCtrue_SubldgJet.at(j)) && areSameJets(TopCandJet2.at(i), MCtrue_LdgJet.at(j))    && areSameJets(TopCandBJet.at(i),  MCtrue_Bjet.at(j));
		  if (same1 || same2)
		    {
		      genuineTop = true;
		      matchedJJB_index = i;
		      MatchedJJB_index.push_back(matchedJJB_index);
		    }//if (same1 || same2)

		}//if ( isMatched*sizesAgree )
	    }// For-loop: All top candidates
	
	  // Fill histograms
	  hDeltaRMinTopTrijet -> Fill(dR_tmin);
	  
	  // Find index of trijets In top direction (min DeltaR)
	  if (genuineTop)
	    {
	      hAllTopQuarkPt_jjbMatched-> Fill(top.pt());
	      bool matchedPassedBDT = cfg_MVACut.passedCut(TopCandMVA.at(matchedJJB_index));
	      if ( matchedPassedBDT ) hAllTopQuarkPt_jjbMatchedBDT -> Fill(top.pt());
	    }
      
	  // In Top direction
	  if (dR_tmin < 0.4)
	    {
	      // Save top candidate
	      MatchedTop_index.push_back(matchedTop_index);
	      hAllTopQuarkPt_Matched -> Fill(top.pt());
	      
	      bool inTopDirPassedBDT = cfg_MVACut.passedCut(TopCandMVA.at(matchedTop_index));
	      if ( inTopDirPassedBDT ) hAllTopQuarkPt_MatchedBDT -> Fill(top.pt());
	    }// if (dR_tmin < 0.4)
	  else hAllTopQuarkPt_NonMatched-> Fill(top.pt());

	}// For-loop: All top quarks

      // Definitions
      double leadingFakePt  = -999.999;
      double leadingFakeMVA = -999.999;
      bool realTop          = false;
      bool realTopJJB       = false;
      int matchedJJBpassBDT = 0;
      int matchedTpassBDT   = 0;
      int RealSelectedTop   = 0;
      int fakeInTopDir      = 0;
      
      // For-loop: All top candidates
    for (size_t i = 0; i < TopCandMVA.size(); i++)
      {

	realTop    = false;
	realTopJJB = false;
	
	// For-loop: All top candidates in top direction (Nested)
	for (size_t j=0; j<MatchedTop_index.size(); j++)
	  {
	    if (i==(size_t) MatchedTop_index.at(j)) realTop = true;
	  }
	
	// For-loop: All top candidates matched (Nested)
	for (size_t j=0; j<MatchedJJB_index.size(); j++)
	  {
	    if (i==(size_t) MatchedJJB_index.at(j)) realTopJJB = true;      
	  }
	
	// In Top Direction
	if (realTop)
	  {
	    hTrijetTopMatched_Mass -> Fill(TopCandP4.at(i).M());
	    bool passBDT = cfg_MVACut.passedCut(TopCandMVA.at(i));
	    if ( passBDT ) matchedTpassBDT++;
	  }//if (realTop)
	
	// Genuine Trijet
	if (realTopJJB)
	  {
	    hTrijetTopJJBMatched_Mass  -> Fill(TopCandP4.at(i).M());
	    hTrijetJJBMatched_BDTvalue -> Fill(TopCandMVA.at(i));
	    
	    bool passBDT = cfg_MVACut.passedCut(TopCandMVA.at(i));
	    if ( passBDT )
	      {
		bool isLdgInBDT1or2 = (TopCandMVA.at(i) == MVAmax1 || TopCandMVA.at(i) == MVAmax2);
		matchedJJBpassBDT++;
		if ( isLdgInBDT1or2 ) RealSelectedTop++;
	      }

	  }//if (realTopJJB)

      // Trijets in Top direction AND not genuine
	if (realTop && !realTopJJB)
	  {
	    hTrijetTopMatchedNonJJBMatched_Mass -> Fill(TopCandP4.at(i).M());
	    fakeInTopDir++;
	  }
	
      // Trijets NOT in top direction
      if (!realTop)
	{
	  hTrijetFakePt -> Fill (TopCandP4.at(i).pt());
	  if (cfg_MVACut.passedCut(TopCandMVA.at(i))) hTrijetFakePt_BDT -> Fill(TopCandP4.at(i).pt());
	}

      // Fake trijets
      if (!realTopJJB)
	{
	  hTrijetJJBNonMatched_BDTvalue -> Fill(TopCandMVA.at(i));
	  hTrijetFakeJJBPt -> Fill (TopCandP4.at(i).pt());

	  bool passBDT   = cfg_MVACut.passedCut(TopCandMVA.at(i));
	  bool isLdgInPt = leadingFakePt < TopCandP4.at(i).pt();

	  if ( passBDT ) hTrijetFakeJJBPt_BDT-> Fill (TopCandP4.at(i).pt());	  
	  if ( isLdgInPt )
	    {
	      leadingFakePt  = TopCandP4.at(i).pt();
	      leadingFakeMVA = TopCandMVA.at(i);
	    }
	  
	}//if (!realTopJJB)
      }// For-loop: All top candidates

    if (leadingFakePt > 0)
      {
	hLdgTrijetFakeJJB -> Fill(leadingFakePt);
	if (cfg_MVACut.passedCut(leadingFakeMVA)) hLdgTrijetFakeJJB_BDT -> Fill(leadingFakePt);
      }
    
    if (TopMatched) hMatchedBDTmult -> Fill(matchedTpassBDT);

    bool passBDTboth = cfg_MVACut.passedCut(min(MVAmax1,MVAmax2));
    if (MatchedJJB_index.size() == GenTops.size() && passBDTboth )
      {
      hMatchedjjbBDTmult -> Fill(matchedJJBpassBDT);
      hRealSelectedTopMult -> Fill (RealSelectedTop);
    }
    hFakeInTopDirMult -> Fill (fakeInTopDir);


    //================================================================================================
    // Top-tagging Efficiency (per top candidate) - combinations with same subjets (b-tag assignment)
    //================================================================================================
    int NselectedMatched_sameOdj = 0;

    // For-loop: All top candidates matched
    for (size_t j=0; j<MatchedJJB_index.size(); j++)
      {
	
	int matched_index = MatchedJJB_index.at(j);
	double MVA_min    = TopCandMVA.at(matched_index);
	double MVA_max    = TopCandMVA.at(matched_index), BdiscrMax = TopCandBJet.at(matched_index).bjetDiscriminator();
	
	vector <int> wrongAssignmentTrijetIndex;                                                                           //Trijets with Wrong-assignment b-tagged jet -  indices
	wrongAssignmentTrijetIndex = GetWrongAssignmentTrijetIndex(matched_index,TopCandJet1, TopCandJet2, TopCandBJet);
	
	bool selectedMatched_sameOdj = true;
	double DeltaMVA_max = -999.999, absDeltaMVA_max = -999.999, DeltaMVA_min = 999.999;
	
	// For-loop: All wrongly-assigned top candidates (Nested)
	for(size_t k=0; k< wrongAssignmentTrijetIndex.size(); k++)
	  {
	    
	    double DeltaMVAvalue = TopCandMVA.at(matched_index) - TopCandMVA.at(wrongAssignmentTrijetIndex.at(k));
	    
	    // Find maximum and mivumum MVA value
	    if (TopCandMVA.at(wrongAssignmentTrijetIndex.at(k)) < MVA_min) MVA_min = TopCandMVA.at(wrongAssignmentTrijetIndex.at(k));
	    
	    if (TopCandMVA.at(wrongAssignmentTrijetIndex.at(k)) > MVA_max)
	      {		
		MVA_max   = TopCandMVA.at(wrongAssignmentTrijetIndex.at(k));
		BdiscrMax = TopCandBJet.at(wrongAssignmentTrijetIndex.at(k)).bjetDiscriminator();
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
	 
	// MVA value of matched trijets when DeltaMVA > 1
	if (DeltaMVA_min > 1) hMVAvalue_DeltaMVAgt1 -> Fill(TopCandMVA.at(matched_index));
	
	if (selectedMatched_sameOdj && BdiscrMax > 0.8484) NselectedMatched_sameOdj++;      

	// fixme
	if (!cfg_MVACut.passedCut(MVA_min)) continue;


	// Fill histograms
	hDeltaMVAmax_MCtruth_SameObjFakesPassBDT -> Fill(DeltaMVA_max);
	hDeltaMVAmin_MCtruth_SameObjFakesPassBDT -> Fill(DeltaMVA_min);
	hDeltaMVAmaxVsTrijetPassBDTvalue         -> Fill(DeltaMVA_max, TopCandMVA.at(matched_index));
	hDeltaMVAminVsTrijetPassBDTvalue         -> Fill(DeltaMVA_min, TopCandMVA.at(matched_index));
	
      }// For-loop: All top candidates matched

    if (MatchedJJB_index.size() == GenTops.size())  hMatchedPassBDTmult_SameObjFakes -> Fill(NselectedMatched_sameOdj);
    if  (jets.size() > 9)                           hMatchedTrijetMult_JetsGT9 -> Fill(MCtrue_Bjet.size());
    hMatchedTrijetMult_JetsInc -> Fill(MatchedJJB_index.size());
  
    // For-loop: All top candidates passing BDT cut
    for (size_t i = 0; i < TopCandMVA.size(); i++)
      {
	if (!cfg_MVACut.passedCut(TopCandMVA.at(i))) continue;
	hAllTrijetPassBDT_pt -> Fill(TopCandP4.at(i).Pt());
	hTrijetPassBDT_bDisc -> Fill(TopCandBJet.at(i).bjetDiscriminator());
	if (TopCandBJet.at(i).bjetDiscriminator() > 0.8484) hAllTrijetPassBDTbPassCSV_pt -> Fill(TopCandP4.at(i).Pt());
      }// For-loop: All top candidates passing BDT cut
    
    }// if (event.isMC() && doMatching)

  // Fill output data  
  output.fTrijet1Jet1     = leadingTrijetJet1;
  output.fTrijet1Jet2     = leadingTrijetJet2;
  output.fTrijet1BJet     = leadingTrijetBJet;
  output.fTrijet1Dijet_p4 = leadingTrijetJet1.p4() +  leadingTrijetJet2.p4();
  output.fTrijet1_p4      = leadingTrijetP4;
  output.fTrijet2Jet1     = subleadingTrijetJet1;
  output.fTrijet2Jet2     = subleadingTrijetJet2;
  output.fTrijet2BJet     = subleadingTrijetBJet;
  output.fTrijet2Dijet_p4 = subleadingTrijetJet1.p4() +  subleadingTrijetJet2.p4();
  output.fTrijet2_p4      = subleadingTrijetP4;
  output.fTetrajetBJet    = tetrajetBjet;
  output.fLdgTetrajet_p4  = tetrajetP4;
  output.bPassedSelection = (cfg_MVACut.passedCut(MVAmax1) && cfg_MVACut.passedCut(MVAmax2) && tetrajetBjetPt_max > 0 );
  
  //================================================================================================
  // Fill histograms (Before cuts)
  //================================================================================================
  hBDTmultiplicity           -> Fill(passBDT);                         //Number of trijets passing MVA selection
  hTrijetMultiplicity        -> Fill(TopCandMVA.size());               //Trijet multiplicity
  hNjetsVsNTrijets_beforeBDT -> Fill(jets.size(), TopCandMVA.size());  //Trijet multiplicity as a function of Jet multiplicity  (Before MVA selection)   <---Constant
  hNjetsVsNTrijets_afterBDT  -> Fill(jets.size(), passBDT);            //Trijet multiplicity as a function of Jet multiplicity  (After MVA selection)
  if (cfg_MVACut.passedCut(MVAmax1)) hTrijetPt_BDT ->Fill(trijet1.Pt());
  if (cfg_MVACut.passedCut(MVAmax2)) hTrijetPt_BDT ->Fill(trijet2.Pt());

  // Top-tagging Efficiency (per event)
  if (TopMatched)
    {
      hEventTrijetPt -> Fill(trijet1.Pt()); 
      hEventTrijetPt -> Fill(trijet2.Pt());  
      if (passBDTboth)
	{
	  hEventTrijetPt_BDT -> Fill(trijet1.Pt());
	  hEventTrijetPt_BDT -> Fill(trijet2.Pt());
	  if (realtopBoth)
	    {
	      hEventTrijetPt_MatchedBDT -> Fill(trijet1.Pt());
	      hEventTrijetPt_MatchedBDT -> Fill(trijet2.Pt());
	    }//if (realtopBoth)
	}//if (passBDTboth)
    }//if (TopMatched)
  
  // All the top quarks have been matched
  if (MCtrue_Bjet.size() == GenTops.size())
    {
      hEventTrijetPt2T -> Fill(trijet1.Pt());              //Trijet.pt -- Inclusive
      hEventTrijetPt2T -> Fill(trijet2.Pt());              //Trijet.pt -- Inclusive
      if ( realtopBothqqb )
	{
	  hEventTrijetPt2T_Matchedjjb -> Fill(trijet1.Pt()); //Trijet.pt(Matched)  -- Inclusive
	  hEventTrijetPt2T_Matchedjjb -> Fill(trijet2.Pt()); //Trijet.pt(Matched)  -- Inclusive
	}
      if ( passBDTboth )
	{
	  hEventTrijetPt2T_BDT -> Fill(trijet1.Pt());        //Trijet.pt(passBDT) -- Inclusive
	  hEventTrijetPt2T_BDT -> Fill(trijet2.Pt());        //Trijet.pt(passBDT) -- Inclusive
	  if ( realtopBothqqb )
	    {
	      hEventTrijetPt2T_MatchedjjbBDT -> Fill(trijet1.Pt()); //Trijet.pt(passBDT&&Matched) -- Inclusive
	      hEventTrijetPt2T_MatchedjjbBDT -> Fill(trijet2.Pt()); //Trijet.pt(passBDT&&Matched) -- Inclusive
	    }//if ( realtopBothqqb )
	}//if ( passBDTboth )
    }//if (MCtrue_Bjet.size() == GenTops.size())
  

  // Replace all PF Jet 4-vectors with their matched GenJet 4-vectors
  if (replaceJets) ReplaceJetsWithGenJets(output); //fixme: not tested!!!

  //================================================================================================
  // Apply cuts
  //================================================================================================
  bool haveFreeBJet = (tetrajetBjetPt_max > 0); 
  if ( !passBDTboth ) return output; 
  if ( !haveFreeBJet ) return output; 
  cSubPassedBDTCut.increment();

  // Passed all top selection cuts
  cPassedTopSelectionBDT.increment();
    
  //================================================================================================
  // Fill histograms (After cuts)
  //================================================================================================
  hTopCandMass ->Fill(trijet1.M());
  hTopCandMass ->Fill(trijet2.M());
  // Leading top candidate passing BDT  
  double dijetMass = (leadingTrijetJet1.p4() +  leadingTrijetJet2.p4()).M();
  hLdgTrijetTopMassWMassRatio -> Fill(leadingTrijetP4.M()/dijetMass);
  hLdgTrijetPt          -> Fill(leadingTrijetP4.Pt());
  hLdgTrijetMass        -> Fill(leadingTrijetP4.M());
  hLdgTrijetJet1Pt      -> Fill(leadingTrijetJet1.pt());
  hLdgTrijetJet1Eta     -> Fill(leadingTrijetJet1.eta());
  hLdgTrijetJet1BDisc   -> Fill(leadingTrijetJet1.bjetDiscriminator());
  hLdgTrijetJet2Pt      -> Fill(leadingTrijetJet2.pt());
  hLdgTrijetJet2Eta     -> Fill(leadingTrijetJet2.eta());
  hLdgTrijetJet2BDisc   -> Fill(leadingTrijetJet2.bjetDiscriminator());
  hLdgTrijetBJetPt      -> Fill(leadingTrijetBJet.pt());
  hLdgTrijetBJetEta     -> Fill(leadingTrijetBJet.eta());
  hLdgTrijetBJetBDisc   -> Fill(leadingTrijetBJet.bjetDiscriminator());
  hLdgTrijetDiJetPt     -> Fill((leadingTrijetJet1.p4() + leadingTrijetJet2.p4()).Pt());
  hLdgTrijetDiJetEta    -> Fill((leadingTrijetJet1.p4() + leadingTrijetJet2.p4()).Eta());
  hLdgTrijetDiJetMass   -> Fill((leadingTrijetJet1.p4() + leadingTrijetJet2.p4()).M());
  hLdgTrijetDijetDeltaR -> Fill(ROOT::Math::VectorUtil::DeltaR(leadingTrijetJet1.p4(), leadingTrijetJet2.p4()));
  // Subleading top candidate passing BDT
  hSubldgTrijetTopMassWMassRatio -> Fill(subleadingTrijetP4.M()/(subleadingTrijetJet1.p4() + subleadingTrijetJet2.p4()).M());
  hSubldgTrijetPt           -> Fill(subleadingTrijetP4.Pt());
  hSubldgTrijetMass         -> Fill(subleadingTrijetP4.M());
  hSubldgTrijetJet1Pt       -> Fill(subleadingTrijetJet1.pt());
  hSubldgTrijetJet1Eta      -> Fill(subleadingTrijetJet1.eta());
  hSubldgTrijetJet1BDisc    -> Fill(subleadingTrijetJet1.bjetDiscriminator());    
  hSubldgTrijetJet2Pt       -> Fill(subleadingTrijetJet2.pt());
  hSubldgTrijetJet2Eta      -> Fill(subleadingTrijetJet2.eta());
  hSubldgTrijetJet2BDisc    -> Fill(subleadingTrijetJet2.bjetDiscriminator());
  hSubldgTrijetBJetPt       -> Fill(subleadingTrijetBJet.pt());
  hSubldgTrijetBJetEta      -> Fill(subleadingTrijetBJet.eta());
  hSubldgTrijetBJetBDisc    -> Fill(subleadingTrijetBJet.bjetDiscriminator());
  hSubldgTrijetDiJetPt      -> Fill((subleadingTrijetJet1.p4() + subleadingTrijetJet2.p4()).Pt());
  hSubldgTrijetDiJetEta     -> Fill((subleadingTrijetJet1.p4() + subleadingTrijetJet2.p4()).Eta());
  hSubldgTrijetDiJetMass    -> Fill((subleadingTrijetJet1.p4() + subleadingTrijetJet2.p4()).M());
  hSubldgTrijetDijetDeltaR  -> Fill(ROOT::Math::VectorUtil::DeltaR(subleadingTrijetJet1.p4(), subleadingTrijetJet2.p4()));
  // Ldg in pt free b-jet
  hTetrajetBJetPt    -> Fill(tetrajetBjet.pt());
  hTetrajetBJetEta   -> Fill(tetrajetBjet.eta());
  hTetrajetBJetBDisc -> Fill(tetrajetBjet.bjetDiscriminator());
  hTetrajetPt        -> Fill(tetrajetP4.Pt());
  hTetrajetMass      -> Fill(tetrajetP4.M());
  hTetrajetEta       -> Fill(tetrajetP4.Eta());

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

  math::XYZTLorentzVector tetrajet1_p4;
  math::XYZTLorentzVector tetrajet2_p4;
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

  // Tetrajet system (for Invariant Mass)  
  tetrajet1_p4 = tetrajet_bjet_p4 + output.fTrijet1_p4;
  tetrajet2_p4 = tetrajet_bjet_p4 + output.fTrijet2_p4;
  output.fTetrajet1_p4 = tetrajet1_p4;
  output.fTetrajet2_p4 = tetrajet2_p4;

  // Ldg here means use the LdgTrijet
  output.fLdgTetrajet_p4    = output.getLdgTrijet()    + tetrajet_bjet_p4;
  output.fSubldgTetrajet_p4 = output.getSubldgTrijet() + tetrajet_bjet_p4;

  // std::cout << "output.getLdgTrijet().M() = " << output.getLdgTrijet().M() << std::endl;
  // std::cout << "output.fLdgTetrajet_p4.M() = " << output.fLdgTetrajet_p4.M() << "\n" << std::endl;
  
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

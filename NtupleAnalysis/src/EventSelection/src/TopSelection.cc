// -*- c++ -*-
#include "EventSelection/interface/TopSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
//#include "Framework/interface/makeTH.h"

#include "Math/VectorUtil.h"

TopSelection::Data::Data()
: bPassedSelection(false),
  fChiSqr(1e9),
  fNumberOfFits(0.0),
  fJetsUsedAsBJetsInFit(),
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

TopSelection::Data::~Data() { }


TopSelection::TopSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
  : BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
    // Input parameters
    cfg_MassW(config.getParameter<float>("MassW")),
    cfg_diJetSigma(config.getParameter<float>("DiJetSigma")),
    cfg_triJetSigma(config.getParameter<float>("TriJetSigma")),
    cfg_dijetWithMaxDR_tetrajetBjet_dR_min(config.getParameter<float>("dijetWithMaxDR_tetrajetBjet_dR_min")),
    cfg_dijetWithMaxDR_tetrajetBjet_dR_slopeCoeff(config.getParameter<float>("dijetWithMaxDR_tetrajetBjet_dR_slopeCoeff")),
    cfg_dijetWithMaxDR_tetrajetBjet_dR_yIntercept(config.getParameter<float>("dijetWithMaxDR_tetrajetBjet_dR_yIntercept")), 
    cfg_dijetWithMaxDR_tetrajetBjet_dPhi_min(config.getParameter<float>("dijetWithMaxDR_tetrajetBjet_dPhi_min")),
    cfg_dijetWithMaxDR_tetrajetBjet_dPhi_slopeCoeff(config.getParameter<float>("dijetWithMaxDR_tetrajetBjet_dPhi_slopeCoeff")),
    cfg_dijetWithMaxDR_tetrajetBjet_dPhi_yIntercept(config.getParameter<float>("dijetWithMaxDR_tetrajetBjet_dPhi_yIntercept")), 
    cfg_ChiSqrCut(config, "ChiSqrCut"),
    cfg_MaxJetsToUseInFit(config.getParameter<int>("MaxJetsToUseInFit")),
    cfg_MaxBJetsToUseInFit(config.getParameter<int>("MaxBJetsToUseInFit")),
    // Event counter for passing selection
    cPassedTopSelection(fEventCounter.addCounter("passed top selection ("+postfix+")")),
    // Sub counters
    cSubAll(fEventCounter.addSubCounter("top selection ("+postfix+")", "All events")),
    cSubPassedChiSqCut(fEventCounter.addSubCounter("top selection ("+postfix+")", "Passed chiSq cut"))
{
  initialize(config);
  nSelectedBJets = -1;
}

TopSelection::TopSelection(const ParameterSet& config)
: BaseSelection(),
  // Input parameters
  cfg_MassW(config.getParameter<float>("MassW")),
  cfg_diJetSigma(config.getParameter<float>("DiJetSigma")),
  cfg_triJetSigma(config.getParameter<float>("TriJetSigma")),
  cfg_dijetWithMaxDR_tetrajetBjet_dR_min(config.getParameter<float>("dijetWithMaxDR_tetrajetBjet_dR_min")),
  cfg_dijetWithMaxDR_tetrajetBjet_dR_slopeCoeff(config.getParameter<float>("dijetWithMaxDR_tetrajetBjet_dR_slopeCoeff")),
  cfg_dijetWithMaxDR_tetrajetBjet_dR_yIntercept(config.getParameter<float>("dijetWithMaxDR_tetrajetBjet_dR_yIntercept")), 
  cfg_dijetWithMaxDR_tetrajetBjet_dPhi_min(config.getParameter<float>("dijetWithMaxDR_tetrajetBjet_dPhi_min")),
  cfg_dijetWithMaxDR_tetrajetBjet_dPhi_slopeCoeff(config.getParameter<float>("dijetWithMaxDR_tetrajetBjet_dPhi_slopeCoeff")),
  cfg_dijetWithMaxDR_tetrajetBjet_dPhi_yIntercept(config.getParameter<float>("dijetWithMaxDR_tetrajetBjet_dPhi_yIntercept")), 
  cfg_ChiSqrCut(config, "ChiSqrCut"),
  cfg_MaxJetsToUseInFit(config.getParameter<int>("MaxJetsToUseInFit")),
  cfg_MaxBJetsToUseInFit(config.getParameter<int>("MaxBJetsToUseInFit")),
  // Event counter for passing selection
  cPassedTopSelection(fEventCounter.addCounter("passed top selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("top selection", "All events")),
  cSubPassedChiSqCut(fEventCounter.addSubCounter("top selection", "Passed a cut"))
{
  initialize(config);
  bookHistograms(new TDirectory());
}

TopSelection::~TopSelection() {
  
  delete hChiSqr;
  delete hNJetsUsedAsBJetsInFit;
  delete hNumberOfFits;
  delete hTetrajetBJetPt;
  delete hTetrajetBJetEta;
  delete hTetrajetBJetBDisc;
  delete hTetrajet1Pt;
  delete hTetrajet1Mass;
  delete hTetrajet1Eta;
  delete hTetrajet2Pt;
  delete hTetrajet2Mass;
  delete hTetrajet2Eta;
  delete hLdgTetrajetPt;
  delete hLdgTetrajetMass;
  delete hLdgTetrajetEta;
  delete hSubldgTetrajetPt;
  delete hSubldgTetrajetMass;
  delete hSubldgTetrajetEta;
  delete hTrijet1Mass;
  delete hTrijet2Mass;
  delete hTrijet1Pt;
  delete hTrijet2Pt;
  delete hTrijet1DijetMass;
  delete hTrijet2DijetMass;
  delete hTrijet1DijetPt;
  delete hTrijet2DijetPt;
  delete hTrijet1DijetDEta;
  delete hTrijet2DijetDEta;
  delete hTrijet1DijetDPhi;
  delete hTrijet2DijetDPhi;
  delete hTrijet1DijetDR;
  delete hTrijet2DijetDR;
  delete hTrijet1DijetBJetDR;
  delete hTrijet2DijetBJetDR;
  delete hTrijet1DijetBJetDPhi;
  delete hTrijet2DijetBJetDPhi;
  delete hTrijet1DijetBJetDEta;
  delete hTrijet2DijetBJetDEta;
  delete hLdgTrijetPt;
  delete hLdgTrijetTopMassWMassRatio;
  delete hLdgTrijetPt_Vs_LdgTrijetDijetPt;
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
  delete hSubldgTrijetPt;
  delete hSubldgTrijetTopMassWMassRatio;
  delete hSubldgTrijetPt_Vs_SubldgTrijetDijetPt;
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

  // Histograms (2D)
  delete hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DPhiVsDPhi;
  delete hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DRVsDR;
  delete hTrijet1MassVsChiSqr;
  delete hTrijet2MassVsChiSqr;
  delete hTrijet1DijetPtVsDijetDR;
  delete hTrijet2DijetPtVsDijetDR;
  
}

void TopSelection::initialize(const ParameterSet& config) {
  
}

void TopSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kVital, dir, "topSelection_" + sPostfix);

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
  hChiSqr                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "ChiSqr", ";#chi^{2}", 1000,  0.0, 1000.0);
  hNJetsUsedAsBJetsInFit = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "NJetsUsedAsBJetsInFit", ";failed b-Jets Multiplicity;Events / %0.f GeV/c^{2}", 15, -0.5, 14.5);
  hNumberOfFits          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "NumberOfFits", ";number of di-top fits;Events / %0.f GeV/c^{2}", 500, 0.0, 500.0);

  hTetrajetBJetPt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetPt"    ,";p_{T} (GeV/c)"      , nPtBins     , fPtMin     , fPtMax);
  hTetrajetBJetEta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetEta"   ,";#eta"               , nEtaBins    , fEtaMin    , fEtaMax);
  hTetrajetBJetBDisc  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetBDisc" ,";b-tag discriminator", nBDiscBins  , fBDiscMin  , fBDiscMax);
  hTetrajet1Pt        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Tetrajet1Pt"       , ";p_{T} (GeV/c)"     , nPtBins     , fPtMin     , fPtMax);
  hTetrajet1Mass      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Tetrajet1Mass"     , ";M (GeV/c^{2})"     , nInvMassBins, fInvMassMin, fInvMassMax);
  hTetrajet1Eta       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Tetrajet1Eta"      , ";#eta"              , nEtaBins    , fEtaMin    , fEtaMax);
  hTetrajet2Pt        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Tetrajet2Pt"       , ";p_{T} (GeV/c)"     , nPtBins     , fPtMin     , fPtMax);
  hTetrajet2Mass      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Tetrajet2Mass"     , ";M (GeV/c^{2})"     , nInvMassBins, fInvMassMin, fInvMassMax);
  hTetrajet2Eta       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Tetrajet2Eta"      , ";#eta"              , nEtaBins    , fEtaMin    , fEtaMax);
  hLdgTetrajetPt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTetrajetPt"     , ";p_{T} (GeV/c)"     , nPtBins     , fPtMin     , fPtMax);
  hLdgTetrajetMass    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTetrajetMass"   , ";M (GeV/c^{2})"     , nInvMassBins, fInvMassMin, fInvMassMax);
  hLdgTetrajetEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTetrajetEta"    , ";#eta"              , nEtaBins    , fEtaMin    , fEtaMax);
  hSubldgTetrajetPt   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTetrajetPt"  , ";p_{T} (GeV/c)"     , nPtBins     , fPtMin     , fPtMax);
  hSubldgTetrajetMass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTetrajetMass", ";M (GeV/c^{2})"     , nInvMassBins, fInvMassMin, fInvMassMax);
  hSubldgTetrajetEta  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTetrajetEta" , ";#eta"              , nEtaBins    , fEtaMin    , fEtaMax);

  hTrijet1Mass      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet1Mass"     , ";M (GeV/c^{2})"          , nTopMassBins, fTopMassMin, fTopMassMax);
  hTrijet2Mass      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet2Mass"     , ";M (GeV/c^{2})"          , nTopMassBins, fTopMassMin, fTopMassMax);
  hTrijet1Pt        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet1Pt"       , ";p_{T} (GeV/c)"          , nPtBins     , fPtMin     , fPtMax);
  hTrijet2Pt        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet2Pt"       , ";p_{T} (GeV/c)"          , nPtBins     , fPtMin     , fPtMax);
  hTrijet1DijetMass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet1DijetMass", ";M (GeV/c^{2})"          , nWMassBins  , fWMassMin  , fWMassMax);
  hTrijet2DijetMass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet2DijetMass", ";M (GeV/c^{2})"          , nWMassBins  , fWMassMin  , fWMassMax);
  hTrijet1DijetPt   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet1DijetPt"  , ";p_{T} (GeV/c)"          , nPtBins     , fPtMin     , fPtMax);
  hTrijet2DijetPt   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet2DijetPt"  , ";p_{T} (GeV/c)"          , nPtBins     , fPtMin     , fPtMax);
  hTrijet1DijetDR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet1DijetDR"  , ";#Delta R(j_{1},j_{2})"  , nDRBins     , fDRMin     , fDRMax);
  hTrijet2DijetDR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet2DijetDR"  , ";#Delta R(j_{1},j_{2})"  , nDRBins     , fDRMin     , fDRMax);
  hTrijet1DijetDPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet1DijetDPhi", ";#Delta#phi(j_{1},j_{2})", nDPhiBins   , fDPhiMin   , fDPhiMax);
  hTrijet2DijetDPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet2DijetDPhi", ";#Delta#phi(j_{1},j_{2})", nDPhiBins   , fDPhiMin   , fDPhiMax);
  hTrijet1DijetDEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet1DijetDEta", ";#Delta#eta(j_{1},j_{2})", nDEtaBins   , fDEtaMin   , fDEtaMax);
  hTrijet2DijetDEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet2DijetDEta", ";#Delta#eta(j_{1},j_{2})", nDEtaBins   , fDEtaMin   , fDEtaMax);

  hTrijet1DijetBJetDEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet1DijetBJetDEta", ";#Delta#eta(jj,bjet)", nDEtaBins, fDEtaMin, fDEtaMax);
  hTrijet2DijetBJetDEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet2DijetBJetDEta", ";#Delta#eta(jj,bjet)", nDEtaBins, fDEtaMin, fDEtaMax);
  hTrijet1DijetBJetDPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet1DijetBJetDPhi", ";#Delta#phi(jj,bjet)", nDPhiBins, fDPhiMin, fDPhiMax);
  hTrijet2DijetBJetDPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet2DijetBJetDPhi", ";#Delta#phi(jj,bjet)", nDPhiBins, fDPhiMin, fDPhiMax);
  hTrijet1DijetBJetDR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet1DijetBJetDR"  , ";#Delta R(jj,bjet)"  , nDRBins  , fDRMin  , fDRMax);
  hTrijet2DijetBJetDR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Trijet2DijetBJetDR"  , ";#Delta R(jj,bjet)"  , nDRBins  , fDRMin  , fDRMax);

  hLdgTrijetPt        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetPt"       ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hLdgTrijetMass      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetMass"     ,";M (GeV/c^{2})", nTopMassBins, fTopMassMin, fTopMassMax);
  hLdgTrijetJet1Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet1Pt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hLdgTrijetJet1Eta   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet1Eta"  ,";#eta"         , nEtaBins    , fEtaMin    , fEtaMax);
  hLdgTrijetJet1BDisc = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet1BDisc",";b-tag discr." , nBDiscBins  , fBDiscMin  , fBDiscMax);
  hLdgTrijetJet2Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet2Pt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hLdgTrijetJet2Eta   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet2Eta"  ,";#eta"         , nEtaBins    , fEtaMin    , fEtaMax);
  hLdgTrijetJet2BDisc = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet2BDisc",";b-tag discr." , nBDiscBins  , fBDiscMin  , fBDiscMax);
  hLdgTrijetBJetPt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetBJetPt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hLdgTrijetBJetEta   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetBJetEta"  ,";#eta"         , nEtaBins    , fEtaMin    , fEtaMax);
  hLdgTrijetBJetBDisc = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetBJetBDisc",";b-tag discr." , nBDiscBins  , fBDiscMin  , fBDiscMax);
  hLdgTrijetDiJetPt   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetDiJetPt"  ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hLdgTrijetDiJetEta  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetDiJetEta" ,";#eta"         , nEtaBins    , fEtaMin    , fEtaMax);
  hLdgTrijetDiJetMass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetDiJetMass",";M (GeV/c^{2})", nWMassBins  , fWMassMin  , fWMassMax);
  hLdgTrijetTopMassWMassRatio      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetTopMassWMassRatio"       ,";R_{32}", 100 , 0.0, 10.0);
  hLdgTrijetPt_Vs_LdgTrijetDijetPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "LdgTrijetPt_Vs_LdgTrijetDijetPt"  ,";p_{T} (GeV/c);p_{T} (GeV/c)",
								nPtBins, fPtMin, fPtMax, nPtBins, fPtMin, fPtMax);

  hSubldgTrijetPt        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetPt"       ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hSubldgTrijetMass      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetMass"     ,";M (GeV/c^{2})", nTopMassBins, fTopMassMin, fTopMassMax);
  hSubldgTrijetJet1Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet1Pt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hSubldgTrijetJet1Eta   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet1Eta"  ,";#eta"         , nEtaBins    , fEtaMin    , fEtaMax);
  hSubldgTrijetJet1BDisc = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet1BDisc",";b-tag discr." , nBDiscBins  , fBDiscMin  , fBDiscMax);
  hSubldgTrijetJet2Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet2Pt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hSubldgTrijetJet2Eta   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet2Eta"  ,";#eta"         , nEtaBins    , fEtaMin    , fEtaMax);
  hSubldgTrijetJet2BDisc = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet2BDisc",";b-tag discr." , nBDiscBins  , fBDiscMin  , fBDiscMax);
  hSubldgTrijetBJetPt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetBJetPt"   ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hSubldgTrijetBJetEta   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetBJetEta"  ,";#eta"         , nEtaBins    , fEtaMin    , fEtaMax);
  hSubldgTrijetBJetBDisc = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetBJetBDisc",";b-tag discr." , nBDiscBins  , fBDiscMin  , fBDiscMax);
  hSubldgTrijetDiJetPt   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetDiJetPt"  ,";p_{T} (GeV/c)", nPtBins     , fPtMin     , fPtMax);
  hSubldgTrijetDiJetEta  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetDiJetEta" ,";#eta"         , nEtaBins    , fEtaMin    , fEtaMax);
  hSubldgTrijetDiJetMass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetDiJetMass",";M (GeV/c^{2})", nWMassBins  , fWMassMin  , fWMassMax);
  hSubldgTrijetTopMassWMassRatio         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetTopMassWMassRatio"       ,";R_{32}", 100 , 0.0, 10.0);
  hSubldgTrijetPt_Vs_SubldgTrijetDijetPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "SubldgTrijetPt_Vs_SubldgTrijetDijetPt",";p_{T} (GeV/c);p_{T} (GeV/c)",
								nPtBins, fPtMin, fPtMax, nPtBins, fPtMin, fPtMax);

  // Histograms (2D) 
  hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DPhiVsDPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, subdir, 
												 "TetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DPhiVsDPhi", ";#Delta#phi (rads); #Delta#phi (rads)", 
												 nDPhiBins, fDPhiMin, fDPhiMax, nDPhiBins, fDPhiMin, fDPhiMax);
  
  hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DRVsDR = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, subdir, 
											     "TetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DRVsDR", ";#DeltaR; #DeltaR", 
											     nDRBins, fDRMin, fDRMax, nDRBins, fDRMin, fDRMax);
  
  hTrijet1MassVsChiSqr     = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, subdir, "Trijet1MassVsChiSqr", ";M (GeV/c^{2}); #chi^{2}", nTopMassBins, fTopMassMin, fTopMassMax, 300, 0.0, 300.0);
  hTrijet2MassVsChiSqr     = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, subdir, "Trijet2MassVsChiSqr", ";M (GeV/c^{2}); #chi^{2}", nTopMassBins, fTopMassMin, fTopMassMax, 300, 0.0, 300.0);
  hTrijet1DijetPtVsDijetDR = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, subdir, "Trijet1DijetPtVsDijetDR", ";p_{T} (GeV/c);#Delta R(j_{1},j_{2}", nPtBins, fPtMin, fPtMax, nDRBins, fDRMin, fDRMax);
  hTrijet2DijetPtVsDijetDR = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, subdir, "Trijet2DijetPtVsDijetDR", ";p_{T} (GeV/c);#Delta R(j_{1},j_{2}", nPtBins, fPtMin, fPtMax, nDRBins, fDRMin, fDRMax);

  return;
}

TopSelection::Data TopSelection::silentAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  ensureSilentAnalyzeAllowed(event.eventID());
  nSelectedBJets = bjetData.getSelectedBJets().size();

  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, GetJetsToBeUsedInFit(jetData, cfg_MaxJetsToUseInFit), GetBjetsToBeUsedInFit(bjetData, cfg_MaxBJetsToUseInFit) );
  enableHistogramsAndCounters();
  return myData;
}

TopSelection::Data TopSelection::silentAnalyzeWithoutBJets(const Event& event, 
							   const JetSelection::Data& jetData,
							   const BJetSelection::Data& bjetData,
							   const unsigned int maxNumberOfBJetsInTopFit) {
  ensureSilentAnalyzeAllowed(event.eventID());
  nSelectedBJets = bjetData.getSelectedBJets().size();

  // Disable histogram filling and counter
  disableHistogramsAndCounters();  
  // Ready to analyze 
  Data data = privateAnalyzeWithoutBJets(event, GetJetsToBeUsedInFit(jetData, cfg_MaxJetsToUseInFit), GetBjetsToBeUsedInFit(bjetData, cfg_MaxBJetsToUseInFit) );
  // Re-enable histogram filling and counter
  enableHistogramsAndCounters();
  return data;
}


TopSelection::Data TopSelection::analyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  ensureAnalyzeAllowed(event.eventID());
  nSelectedBJets = bjetData.getSelectedBJets().size();

  // Ready to analyze
  TopSelection::Data data = privateAnalyze(event, GetJetsToBeUsedInFit(jetData, cfg_MaxJetsToUseInFit), GetBjetsToBeUsedInFit(bjetData, cfg_MaxBJetsToUseInFit) );

  // Send data to CommonPlots
  // if (fCommonPlots != nullptr) fCommonPlots->fillControlPlotsAtTopSelection(event, data); //fixme
  return data;
}

TopSelection::Data TopSelection::analyzeWithoutBJets(const Event& event, 
						     const JetSelection::Data& jetData, 
						     const BJetSelection::Data& bjetData,
						     const unsigned int maxNumberOfBJetsInTopFit) {
  // Used to be different but not identical to analyze!
  ensureAnalyzeAllowed(event.eventID());
  nSelectedBJets = bjetData.getSelectedBJets().size();
 
  // Ready to analyze 
  TopSelection::Data data = privateAnalyze(event, GetJetsToBeUsedInFit(jetData, cfg_MaxJetsToUseInFit), GetBjetsToBeUsedInFit(bjetData, cfg_MaxBJetsToUseInFit) );

  // Send data to CommonPlots
  // if (fCommonPlots != nullptr) fCommonPlots->fillControlPlotsAtTopSelection(event, data); //fixme
  return data;
}

TopSelection::Data TopSelection::privateAnalyze(const Event& event, const std::vector<Jet> jets, const std::vector<Jet> bjets) {
  Data output;
  cSubAll.increment();
  
  // Initialise variables
  output.fJetsUsedAsBJetsInFit = bjets;
  output.bIsGenuineB = _getIsGenuineB(event.isMC(), output.fJetsUsedAsBJetsInFit);

  std::vector<unsigned int> bjet1;
  std::vector<unsigned int> bjet2;
  std::vector<unsigned int> jet1;
  std::vector<unsigned int> jet2;
  std::vector<unsigned int> jet3;
  std::vector<unsigned int> jet4;
  double minChiSqr = 1e9;

  // Sanity check
  if (bjets.size() < 3) return output;

  if (0) std::cout << "\nnJets = " << jets.size() << ", \033[1;31mnBJets = " << bjets.size() << "\033[0m" << std::endl;

  // Get all combinatorics for fit-trials
  GetJetIndicesForChiSqrFit(jets, bjets, jet1, jet2, jet3, jet4, bjet1, bjet2);

  // For-loop: All jet indices
  for (unsigned int index=0; index < jet1.size(); index++, output.fNumberOfFits++)
    {
      // Construct chi-square variable using jets(1-4) and b-jets(1-2)
      unsigned int b1  = bjet1.at(index);
      unsigned int b2  = bjet2.at(index);
      unsigned int j1  = jet1.at(index);
      unsigned int j2  = jet2.at(index);
      unsigned int j3  = jet3.at(index);
      unsigned int j4  = jet4.at(index);
      double chiSqr    = CalculateChiSqrForTrijetSystems(jets.at(j1), jets.at(j2), jets.at(j3), jets.at(j4), jets.at(b1), jets.at(b2));

      // Ensure that this di-top combination leaves 1 bjet for the tetrajet reconstruction. Apply angular cuts?
      const int tetrajetBjet_index = GetTetrajetBjetIndex(bjets, jets.at(b1), jets.at(b2), jets.at(j1), jets.at(j2), jets.at(j3), jets.at(j4));
      if (tetrajetBjet_index < 0) continue;
      Jet tetrajetBjet = bjets.at(tetrajetBjet_index);

      // Find the configuration that minimised chi-squared
      if (chiSqr < minChiSqr) {

	if (0) std::cout << "minChiSqr = " << minChiSqr << std::endl;

	// Assign the chi-squared value
	minChiSqr = chiSqr;       
	output.fChiSqr = minChiSqr;
	// Assign Trijet-1
	output.fTrijet1Jet1 = jets.at(j1);
	output.fTrijet1Jet2 = jets.at(j2);
	output.fTrijet1BJet = jets.at(b1);
	output.fTrijet1Dijet_p4 = output.fTrijet1Jet1.p4() + output.fTrijet1Jet2.p4();
	output.fTrijet1_p4  = output.fTrijet1Dijet_p4 + output.fTrijet1BJet.p4();
	// Assign Trijet-2
	output.fTrijet2Jet1 = jets.at(j3);
	output.fTrijet2Jet2 = jets.at(j4);
	output.fTrijet2BJet = jets.at(b2);
	output.fTrijet2Dijet_p4 = output.fTrijet2Jet1.p4() + output.fTrijet2Jet2.p4();
	output.fTrijet2_p4  = output.fTrijet2Dijet_p4 + output.fTrijet2BJet.p4();
	// DiJets with min/max dR separation
	double dR12 = ROOT::Math::VectorUtil::DeltaR(output.fTrijet1Jet1.p4(), output.fTrijet1Jet2.p4());
	double dR34 = ROOT::Math::VectorUtil::DeltaR(output.fTrijet2Jet1.p4(), output.fTrijet2Jet2.p4());
	if (dR12 < dR34) 
	  {
	  output.fDijetWithMinDR_p4 = output.fTrijet1Jet1.p4() + output.fTrijet1Jet2.p4();
	  output.fDijetWithMaxDR_p4 = output.fTrijet2Jet1.p4() + output.fTrijet2Jet2.p4();
	}
      else 
	{
	  output.fDijetWithMaxDR_p4 = output.fTrijet1Jet1.p4() + output.fTrijet1Jet2.p4();
	  output.fDijetWithMinDR_p4 = output.fTrijet2Jet1.p4() + output.fTrijet2Jet2.p4();
	}
      
	// Tetrajet
	output.fTetrajetBJet = tetrajetBjet;
	output.fTetrajet1_p4 = output.fTetrajetBJet.p4() + output.fTrijet1_p4;
	output.fTetrajet2_p4 = output.fTetrajetBJet.p4() + output.fTrijet2_p4;

	// Ldg here means use the LdgTrijet
	output.fLdgTetrajet_p4    = output.getLdgTrijet()    + output.fTetrajetBJet.p4();
	output.fSubldgTetrajet_p4 = output.getSubldgTrijet() + output.fTetrajetBJet.p4();
		
	/* // Get terrible mass 
	   if (output.fTetrajet1_p4.pt() > output.fTetrajet2_p4.pt()) 
	  {
	    output.fLdgTetrajet_p4    = output.fTetrajet1_p4;
	    output.fSubldgTetrajet_p4 = output.fTetrajet2_p4;
	  }
	else	  
	  {
	    output.fLdgTetrajet_p4    = output.fTetrajet2_p4;
	    output.fSubldgTetrajet_p4 = output.fTetrajet1_p4;
	  }*/
      }
    }
  // Sanity check: Did I get at least 1 successful fit?
  if (minChiSqr == 1e9) return output;

  // Fill Histograms (Before cuts)
  hChiSqr->Fill( output.fChiSqr );
  hNJetsUsedAsBJetsInFit->Fill( output.fJetsUsedAsBJetsInFit.size() - nSelectedBJets );
  hNumberOfFits->Fill( output.fNumberOfFits );
  hTrijet1Mass->Fill(output.fTrijet1_p4.mass());
  hTrijet2Mass->Fill(output.fTrijet2_p4.mass());
  hTrijet1Pt->Fill(output.fTrijet1_p4.pt());
  hTrijet2Pt->Fill(output.fTrijet2_p4.pt());
  hTrijet1DijetMass->Fill( output.fTrijet1Dijet_p4.mass() );
  hTrijet2DijetMass->Fill( output.fTrijet2Dijet_p4.mass() );
  hTrijet1DijetPt->Fill( output.fTrijet1Dijet_p4.pt() );
  hTrijet2DijetPt->Fill( output.fTrijet2Dijet_p4.pt() );
  hTrijet1DijetDEta->Fill( std::abs( output.fTrijet1Jet1.p4().eta() - output.fTrijet1Jet2.p4().eta() ) );
  hTrijet2DijetDEta->Fill( std::abs( output.fTrijet2Jet1.p4().eta() - output.fTrijet2Jet2.p4().eta() ) );
  hTrijet1DijetDPhi->Fill( std::abs( ROOT::Math::VectorUtil::DeltaPhi( output.fTrijet1Jet1.p4(), output.fTrijet1Jet2.p4() ) ) );
  hTrijet2DijetDPhi->Fill( std::abs( ROOT::Math::VectorUtil::DeltaPhi( output.fTrijet2Jet1.p4(), output.fTrijet2Jet2.p4() ) ) );
  hTrijet1DijetDR  ->Fill( ROOT::Math::VectorUtil::DeltaR( output.fTrijet1Jet1.p4(), output.fTrijet1Jet2.p4() ) );
  hTrijet2DijetDR  ->Fill( ROOT::Math::VectorUtil::DeltaR( output.fTrijet2Jet1.p4(), output.fTrijet2Jet2.p4() ) );
  hTrijet1DijetBJetDEta->Fill( std::abs( output.fTrijet1Dijet_p4.eta() - output.fTrijet1BJet.p4().eta() ) );
  hTrijet2DijetBJetDEta->Fill( std::abs( output.fTrijet2Dijet_p4.eta() - output.fTrijet2BJet.p4().eta() ) );
  hTrijet1DijetBJetDPhi->Fill( std::abs( ROOT::Math::VectorUtil::DeltaPhi( output.fTrijet1Dijet_p4, output.fTrijet1BJet.p4() ) ) );
  hTrijet2DijetBJetDPhi->Fill( std::abs( ROOT::Math::VectorUtil::DeltaPhi( output.fTrijet2Dijet_p4, output.fTrijet2BJet.p4() ) ) );
  hTrijet1DijetBJetDR  ->Fill( ROOT::Math::VectorUtil::DeltaR( output.fTrijet1Dijet_p4, output.fTrijet1BJet.p4() ) );
  hTrijet2DijetBJetDR  ->Fill( ROOT::Math::VectorUtil::DeltaR( output.fTrijet2Dijet_p4, output.fTrijet2BJet.p4() ) );

  // Leading/Subleading tops
  hLdgTrijetTopMassWMassRatio->Fill(output.getLdgTrijetTopMassWMassRatio());
  hLdgTrijetPt_Vs_LdgTrijetDijetPt->Fill(output.getLdgTrijet().pt(), output.getLdgTrijetDijet().pt());
  hSubldgTrijetTopMassWMassRatio->Fill(output.getSubldgTrijetTopMassWMassRatio());
  hSubldgTrijetPt_Vs_SubldgTrijetDijetPt->Fill(output.getSubldgTrijet().pt(), output.getSubldgTrijetDijet().pt());

  if (output.fTrijet1_p4.pt() > output.fTrijet2_p4.pt()) 
    {
      // Leading
      hLdgTrijetPt       ->Fill(output.fTrijet1_p4.pt());
      hLdgTrijetMass     ->Fill(output.fTrijet1_p4.mass());
      hLdgTrijetJet1Pt   ->Fill(output.fTrijet1Jet1.pt());
      hLdgTrijetJet1Eta  ->Fill(output.fTrijet1Jet1.eta());
      hLdgTrijetJet1BDisc->Fill(output.fTrijet1Jet1.bjetDiscriminator());
      hLdgTrijetJet2Pt   ->Fill(output.fTrijet1Jet2.pt());
      hLdgTrijetJet2Eta  ->Fill(output.fTrijet1Jet2.eta());
      hLdgTrijetJet2BDisc->Fill(output.fTrijet1Jet2.bjetDiscriminator());
      hLdgTrijetBJetPt   ->Fill(output.fTrijet1BJet.pt());
      hLdgTrijetBJetEta  ->Fill(output.fTrijet1BJet.eta());
      hLdgTrijetBJetBDisc->Fill(output.fTrijet1BJet.bjetDiscriminator());
      hLdgTrijetDiJetPt  ->Fill(output.fTrijet1Dijet_p4.pt());
      hLdgTrijetDiJetEta ->Fill(output.fTrijet1Dijet_p4.eta());
      hLdgTrijetDiJetMass->Fill(output.fTrijet1Dijet_p4.mass());
      // Subleading
      hSubldgTrijetPt       ->Fill(output.fTrijet2_p4.pt());
      hSubldgTrijetMass     ->Fill(output.fTrijet2_p4.mass());
      hSubldgTrijetPt       ->Fill(output.fTrijet2_p4.pt());
      hSubldgTrijetMass     ->Fill(output.fTrijet2_p4.mass());
      hSubldgTrijetJet1Pt   ->Fill(output.fTrijet2Jet1.pt());
      hSubldgTrijetJet1Eta  ->Fill(output.fTrijet2Jet1.eta());
      hSubldgTrijetJet1BDisc->Fill(output.fTrijet2Jet1.bjetDiscriminator());
      hSubldgTrijetJet2Pt   ->Fill(output.fTrijet2Jet2.pt());
      hSubldgTrijetJet2Eta  ->Fill(output.fTrijet2Jet2.eta());
      hSubldgTrijetJet2BDisc->Fill(output.fTrijet2Jet2.bjetDiscriminator());
      hSubldgTrijetBJetPt   ->Fill(output.fTrijet2BJet.pt());
      hSubldgTrijetBJetEta  ->Fill(output.fTrijet2BJet.eta());
      hSubldgTrijetBJetBDisc->Fill(output.fTrijet2BJet.bjetDiscriminator());
      hSubldgTrijetDiJetPt  ->Fill(output.fTrijet2Dijet_p4.pt());
      hSubldgTrijetDiJetEta ->Fill(output.fTrijet2Dijet_p4.eta());
      hSubldgTrijetDiJetMass->Fill(output.fTrijet2Dijet_p4.mass());
    }
  else 
    {
      // Leading
      hLdgTrijetPt       ->Fill(output.fTrijet2_p4.pt());
      hLdgTrijetMass     ->Fill(output.fTrijet2_p4.mass());
      hLdgTrijetJet1Pt   ->Fill(output.fTrijet2Jet1.pt());
      hLdgTrijetJet1Eta  ->Fill(output.fTrijet2Jet1.eta());
      hLdgTrijetJet1BDisc->Fill(output.fTrijet2Jet1.bjetDiscriminator());
      hLdgTrijetJet2Pt   ->Fill(output.fTrijet2Jet2.pt());
      hLdgTrijetJet2Eta  ->Fill(output.fTrijet2Jet2.eta());
      hLdgTrijetJet2BDisc->Fill(output.fTrijet2Jet2.bjetDiscriminator());
      hLdgTrijetBJetPt   ->Fill(output.fTrijet2BJet.pt());
      hLdgTrijetBJetEta  ->Fill(output.fTrijet2BJet.eta());
      hLdgTrijetBJetBDisc->Fill(output.fTrijet2BJet.bjetDiscriminator());
      hLdgTrijetDiJetPt  ->Fill(output.fTrijet2Dijet_p4.pt());
      hLdgTrijetDiJetEta ->Fill(output.fTrijet2Dijet_p4.eta());
      hLdgTrijetDiJetMass->Fill(output.fTrijet2Dijet_p4.mass());
      // Subleading
      hSubldgTrijetPt       ->Fill(output.fTrijet1_p4.pt());
      hSubldgTrijetMass     ->Fill(output.fTrijet1_p4.mass());
      hSubldgTrijetJet1Pt   ->Fill(output.fTrijet1Jet1.pt());
      hSubldgTrijetJet1Eta  ->Fill(output.fTrijet1Jet1.eta());
      hSubldgTrijetJet1BDisc->Fill(output.fTrijet1Jet1.bjetDiscriminator());
      hSubldgTrijetJet2Pt   ->Fill(output.fTrijet1Jet2.pt());
      hSubldgTrijetJet2Eta  ->Fill(output.fTrijet1Jet2.eta());
      hSubldgTrijetJet2BDisc->Fill(output.fTrijet1Jet2.bjetDiscriminator());
      hSubldgTrijetBJetPt   ->Fill(output.fTrijet1BJet.pt());
      hSubldgTrijetBJetEta  ->Fill(output.fTrijet1BJet.eta());
      hSubldgTrijetBJetBDisc->Fill(output.fTrijet1BJet.bjetDiscriminator());
      hSubldgTrijetDiJetPt  ->Fill(output.fTrijet1Dijet_p4.pt());
      hSubldgTrijetDiJetEta ->Fill(output.fTrijet1Dijet_p4.eta());
      hSubldgTrijetDiJetMass->Fill(output.fTrijet1Dijet_p4.mass());
    }

  // Tetrajet
  hTetrajetBJetPt    ->Fill(output.fTetrajetBJet.pt());
  hTetrajetBJetEta   ->Fill(output.fTetrajetBJet.eta());
  hTetrajetBJetBDisc ->Fill(output.fTetrajetBJet.bjetDiscriminator());
  hTetrajet1Pt       ->Fill(output.fTetrajet1_p4.pt());
  hTetrajet1Mass     ->Fill(output.fTetrajet1_p4.mass());
  hTetrajet1Eta      ->Fill(output.fTetrajet1_p4.eta());
  hTetrajet2Pt       ->Fill(output.fTetrajet2_p4.pt());
  hTetrajet2Mass     ->Fill(output.fTetrajet2_p4.mass());
  hTetrajet2Eta      ->Fill(output.fTetrajet2_p4.eta());
  hLdgTetrajetPt     ->Fill(output.fLdgTetrajet_p4.pt());
  hLdgTetrajetMass   ->Fill(output.fLdgTetrajet_p4.mass());
  hLdgTetrajetEta    ->Fill(output.fLdgTetrajet_p4.eta());
  hSubldgTetrajetPt  ->Fill(output.fSubldgTetrajet_p4.pt());
  hSubldgTetrajetMass->Fill(output.fSubldgTetrajet_p4.mass());
  hSubldgTetrajetEta ->Fill(output.fSubldgTetrajet_p4.eta());

  // 2-D histos
  double dRMin   = ROOT::Math::VectorUtil::DeltaR(output.fDijetWithMinDR_p4, output.fTetrajetBJet.p4());
  double dRMax   = ROOT::Math::VectorUtil::DeltaR(output.fDijetWithMaxDR_p4, output.fTetrajetBJet.p4());
  double dPhiMin = std::abs(ROOT::Math::VectorUtil::DeltaPhi(output.fDijetWithMinDR_p4, output.fTetrajetBJet.p4() ));
  double dPhiMax = std::abs(ROOT::Math::VectorUtil::DeltaPhi(output.fDijetWithMaxDR_p4, output.fTetrajetBJet.p4() ));
  hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DPhiVsDPhi->Fill(dPhiMin, dPhiMax); 
  hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DRVsDR->Fill(dRMin, dRMax);

  hTrijet1MassVsChiSqr->Fill( output.fTrijet1_p4.mass(), output.fChiSqr );
  hTrijet2MassVsChiSqr->Fill( output.fTrijet2_p4.mass(), output.fChiSqr );
  hTrijet1DijetPtVsDijetDR->Fill( output.fTrijet1Dijet_p4.pt(), ROOT::Math::VectorUtil::DeltaR(output.fTrijet1Jet1.p4(), output.fTrijet1Jet2.p4() ) );
  hTrijet2DijetPtVsDijetDR->Fill( output.fTrijet2Dijet_p4.pt(), ROOT::Math::VectorUtil::DeltaR(output.fTrijet2Jet1.p4(), output.fTrijet2Jet2.p4() ) );

  // Apply cuts
  if ( !cfg_ChiSqrCut.passedCut(output.fChiSqr) ) return output;
  cSubPassedChiSqCut.increment();

  // Passed all top selection cuts
  output.bPassedSelection = true;
  cPassedTopSelection.increment();
  
  // Return data object
  return output;

}

bool TopSelection::_getIsGenuineB(bool bIsMC, const std::vector<Jet>& selectedBjets){
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

bool TopSelection::areSameJets(const Jet& jet1, const Jet& jet2) {
  float dR = ROOT::Math::VectorUtil::DeltaR(jet1.p4(), jet2.p4());
  float dR_match = 0.1;
  if (dR <= dR_match) return true;
  else return false;
}


bool TopSelection::isBJet(const Jet& jet, const std::vector<Jet>& bjets) {
  for (auto bjet: bjets)
    {
      if (areSameJets(jet, bjet)) return true;
    }
  return false;
}


double TopSelection::CalculateChiSqrForTrijetSystems(const Jet& jet1, 
						     const Jet& jet2,
						     const Jet& jet3, 
						     const Jet& jet4,
						     const Jet& bjet1,
						     const Jet& bjet2) {

  // Known mass of W-boson (default: 80.385)
  const double massW = cfg_MassW;

  // 1-sigma of gaussian fit to the mass of the di-jets system (default: 10.2)
  const double sigmaDijet = cfg_diJetSigma;

  // 1- of the gaussian fitting of the mass difference of the 2 triJet systems (default: 27.2)
  const double sigmaTrijet = cfg_triJetSigma;

  // Calculate the chi-sqruare of the two trijet systems
  double massDijet1  = (jet1.p4() + jet2.p4()).mass();
  double massDijet2  = (jet3.p4() + jet4.p4()).mass();
  double massTrijet1 = (jet1.p4() + jet2.p4() + bjet1.p4()).mass();
  double massTrijet2 = (jet3.p4() + jet4.p4() + bjet2.p4()).mass();

  double a = (massDijet1 - massW)/(sigmaDijet);
  double b = (massDijet2 - massW)/(sigmaDijet); 
  double c = (massTrijet1 - massTrijet2)/(sigmaTrijet);

  // Calculate the chi-squared of the di-top system
  double chiSq = pow(a,2) + pow(b,2) + pow(c,2);

  return chiSq;
}

const std::vector<Jet> TopSelection::GetJetsToBeUsedInFit(const JetSelection::Data& jetData,
                                                          const unsigned int maxNumberOfJets)
{
  // Get the selected jets
  std::vector<Jet> jetsForFit = jetData.getSelectedJets();

  // Only resize if their size exceeds max allowed value
  if (jetsForFit.size() > maxNumberOfJets) jetsForFit.resize(maxNumberOfJets);
  return jetsForFit;
}


const std::vector<Jet> TopSelection::GetBjetsToBeUsedInFit(const BJetSelection::Data& bjetData, const unsigned int maxNumberOfBJets)
{
  // If there are some bjets use them (depends on cuts)
  std::vector<Jet> bjetsForFit = bjetData.getSelectedBJets();

  // Append the vector of all failed bjets (in descending B-discriminator value) to the end of the bjets vector
  // Use case: QCD Measurement where we invert at least 1 b-jet => may have less than 3 b-jets available (min for di-top fit and inv mass) 
  if (bjetsForFit.size() < maxNumberOfBJets)
    {
  bjetsForFit.insert(bjetsForFit.end(), bjetData.getFailedBJetCands().begin(), bjetData.getFailedBJetCands().end()); 
    }

  // Truncate the bjets vector to correct size
  if (bjetsForFit.size() > maxNumberOfBJets) bjetsForFit.resize(maxNumberOfBJets);

  return bjetsForFit;
}
  

const int TopSelection::GetTetrajetBjetIndex(const std::vector<Jet> bjets, 
					     const Jet& bjet1,
					     const Jet& bjet2,
					     const Jet& jet1, 
					     const Jet& jet2,
					     const Jet& jet3, 
					     const Jet& jet4){
  
  int tetrajetBjet_index = -1;
  int counter = -1;
  math::XYZTLorentzVector dijetWithMinDR_p4;
  math::XYZTLorentzVector dijetWithMaxDR_p4;

  // For-loop: All bjets
  for (auto bjet: bjets)
    {
      counter++;

      // Skip the jets used in the di-top fit
      if (areSameJets(bjet, bjet1))  continue;
      if (areSameJets(bjet, bjet2))  continue;
      if (areSameJets(bjet,  jet1))  continue;
      if (areSameJets(bjet,  jet2))  continue;
      if (areSameJets(bjet,  jet3))  continue;
      if (areSameJets(bjet,  jet4))  continue;

      // DiJets with min/max dR separation
      double dR_12 = ROOT::Math::VectorUtil::DeltaR(jet1.p4(), jet2.p4());
      double dR_34 = ROOT::Math::VectorUtil::DeltaR(jet3.p4(), jet4.p4());
      if (dR_12 < dR_34) 
	{
	  dijetWithMinDR_p4 = jet1.p4() + jet2.p4();
	  dijetWithMaxDR_p4 = jet3.p4() + jet4.p4();
	}
      else 
	{
	  dijetWithMinDR_p4 = jet3.p4() + jet4.p4();
	  dijetWithMaxDR_p4 = jet1.p4() + jet2.p4();
	}

      // Apply dR cuts between the tetrajet bjet and the two dijets [y = mx + c: dR(dijetMax, b) = -dR(dijetMin, b) + 4]
      double dR_dijetMin = ROOT::Math::VectorUtil::DeltaR(bjet.p4(), dijetWithMinDR_p4);
      double dR_dijetMax = ROOT::Math::VectorUtil::DeltaR(bjet.p4(), dijetWithMaxDR_p4);
      double dR          = std::min(dR_dijetMax, cfg_dijetWithMaxDR_tetrajetBjet_dR_min);
      double dR_cut      = cfg_dijetWithMaxDR_tetrajetBjet_dR_yIntercept + (cfg_dijetWithMaxDR_tetrajetBjet_dR_slopeCoeff * std::min(dR_dijetMin, cfg_dijetWithMaxDR_tetrajetBjet_dR_min) );
      bool passCut_dR    = ( dR > dR_cut);
      if (!passCut_dR) continue;

      // Apply dPhi cuts between the tetrajet bjet and the two dijets [y = mx + c: dPhi(dijetMax, b) = -dPhi(dijetMin, b) + 3.0]
      double dPhi_dijetMin = std::abs(ROOT::Math::VectorUtil::DeltaPhi(bjet.p4(), dijetWithMinDR_p4)); 
      double dPhi_dijetMax = std::abs(ROOT::Math::VectorUtil::DeltaPhi(bjet.p4(), dijetWithMaxDR_p4));
      double dPhi          = std::min(dPhi_dijetMax, cfg_dijetWithMaxDR_tetrajetBjet_dPhi_min);
      double dPhi_cut      = cfg_dijetWithMaxDR_tetrajetBjet_dPhi_yIntercept + (cfg_dijetWithMaxDR_tetrajetBjet_dPhi_slopeCoeff * std::min(dPhi_dijetMin, cfg_dijetWithMaxDR_tetrajetBjet_dPhi_min) );
      bool passCut_dPhi    = ( dPhi > dPhi_cut);
      if (!passCut_dPhi) continue; 

      // Index assignment 
      if (tetrajetBjet_index == -1) tetrajetBjet_index = counter;
      if (bjet.pt()  >= bjets.at(tetrajetBjet_index).pt() ) tetrajetBjet_index = counter;

    }
 
  return tetrajetBjet_index;
}


void TopSelection::GetJetIndicesForChiSqrFit(const std::vector<Jet> jets, 
					     const std::vector<Jet> bjets,
					     std::vector<unsigned int>& jet1,
					     std::vector<unsigned int>& jet2,
					     std::vector<unsigned int>& jet3,
					     std::vector<unsigned int>& jet4,
					     std::vector<unsigned int>& bjet1,
					     std::vector<unsigned int>& bjet2)
{
  // For a given event with B bjets and J-B jets, the number of combinations should be:
  // N = C(B, 2) x C(J-B, 4)  where C(n, r) = nCr
  // For B=3, J=7 we have N =  6 combinations
  // For B=3, J=8 we have N = 30 combinations

  // Declare variables
  const unsigned int nJets = jets.size();
  // const unsigned int nLightJets = jets.size() - bjets.size();
  
  // Safety measure in the case where there are not enough light-jets
  // (i.e. non-bjets) to have 4 jets in the di-top reconstruction
  // In these cases we might also use more than 2 bjets in the chi-square fit
  // This does not necessarily mean we are using b-jets. These b-tagged jets
  // might be c-flavour jets from W->cs decays.
  // const bool skipBJets = (nLightJets >= 4);

  // std::cout << "=== GetJetIndicesForChiSqrFit()\n\tjets.size() = " << jets.size() << ", bjets.size() = " << bjets.size() << std::endl;

  // For-loop: 6 nested loops to get 4 jets, 2 bjets
  for (unsigned int b1=0; b1 < nJets; b1++){
    // Consider only jets which are b-jets
    if ( !isBJet(jets.at(b1), bjets) ) continue;

    for (unsigned int b2=b1+1; b2 < nJets; b2++){
      // Consider only jets which are b-jets
      if ( !isBJet(jets.at(b2), bjets) ) continue;    

      for (unsigned int j1 = 0; j1 < nJets; j1++){
	// Consider only jets, not b-jets (if possible)
	if ( isBJet(jets.at(j1), bjets) ) continue;
	// Ensure jet is not the same as other used jets
	if (j1 == b1 || j1 == b2) continue;

	for (unsigned int j2=j1+1; j2 < nJets; j2++){
	  // Consider only jets, not b-jets (if possible)
	  if ( isBJet(jets.at(j2), bjets) ) continue;
	  // Ensure jet is not the same as other used jets
	  if (j2 == b1 || j2 == b2) continue;
	  
	  for (unsigned int j3=j2+1; j3 < nJets; j3++){
	    // Consider only jets, not b-jets (if possible)
	    if ( isBJet(jets.at(j3), bjets) ) continue;
	    // Ensure jet is not the same as other used jets
	    if (j3 == b1 || j3 == b2 || j3 == j1 || j3 == j2) continue;

	    for (unsigned int j4=j3+1; j4 < nJets; j4++){
	      // Consider only jets, not b-jets (if possible)
	      if ( isBJet(jets.at(j4), bjets) ) continue;
	      // Ensure jet is not the same as other used jets
	      if (j4 == b1 || j4 == b2 || j4 == j1 || j4 == j2 || j4 == j3) continue;
	      
	      // Save this combination of jets/bjets for di-top reconstruction (4 jets, 2 bjets)
	      bjet1.push_back(b1);
	      bjet2.push_back(b2);
	      jet1.push_back(j1);
	      jet2.push_back(j2);
	      jet3.push_back(j3);
	      jet4.push_back(j4);
	      
	      // Save the same combination but with the b-jet positions swapped 
	      // To account for fact that each b-jet can go with trijet1 or trijet2
	      bjet1.push_back(b2);
	      bjet2.push_back(b1);
	      jet1.push_back(j1);
	      jet2.push_back(j2);
	      jet3.push_back(j3);
	      jet4.push_back(j4);
	    }//j4
	  }//j3
	}//j2
      }//j1
    }//b2
  }//b1

  
  // Sanity check:
  if ( (bjet1.size() != bjet2.size()) || (bjet1.size() != jet1.size()) ||
       (bjet1.size() != jet2.size())  || (bjet1.size() != jet3.size()) ||
       (bjet1.size() != jet4.size()) )
    {
      throw hplus::Exception("logic") << "The jet/bjets vector sizes must be the same!";
    }

  if (0)
    {
      unsigned int combinations = 1;
      for (unsigned int i = 0; i < bjet1.size(); i++, combinations++)
	{
	  std::cout << "  " << jet1.at(i) 
		    << "  " << jet2.at(i)
		    << "  " << jet3.at(i) 
		    << "  " << jet4.at(i)
		    << "  \033[1;31m" << bjet1.at(i)
		    << "  \033[1;31m" << bjet2.at(i)
		    << "\033[0m" << std::endl;
	}
      std::cout << "Combinations = " << combinations << std::endl;
    }

  return;
}

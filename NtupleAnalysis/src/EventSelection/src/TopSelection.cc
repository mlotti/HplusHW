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
  fChiSqr(-1.0),
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
  
  delete hChiSqr_Before;
  delete hChiSqr_After;
  delete hNJetsUsedAsBJetsInFit_Before;
  delete hNJetsUsedAsBJetsInFit_After;
  delete hNumberOfFits_Before;
  delete hNumberOfFits_After;

  delete hTetrajetBJetPt_Before;
  delete hTetrajetBJetEta_Before;
  delete hTetrajetBJetBDisc_Before;
  delete hTetrajetBJetPt_After;
  delete hTetrajetBJetEta_After;
  delete hTetrajetBJetBDisc_After;
  delete hTetrajet1Pt_Before;
  delete hTetrajet1Mass_Before;
  delete hTetrajet1Eta_Before;
  delete hTetrajet1Pt_After;
  delete hTetrajet1Mass_After;
  delete hTetrajet1Eta_After;
  delete hTetrajet2Pt_Before;
  delete hTetrajet2Mass_Before;
  delete hTetrajet2Eta_Before;
  delete hTetrajet2Pt_After;
  delete hTetrajet2Mass_After;
  delete hTetrajet2Eta_After;
  delete hLdgTetrajetPt_Before;
  delete hLdgTetrajetMass_Before;
  delete hLdgTetrajetEta_Before;
  delete hLdgTetrajetPt_After;
  delete hLdgTetrajetMass_After;
  delete hLdgTetrajetEta_After;
  delete hSubldgTetrajetPt_Before;
  delete hSubldgTetrajetMass_Before;
  delete hSubldgTetrajetEta_Before;
  delete hSubldgTetrajetPt_After;
  delete hSubldgTetrajetMass_After;
  delete hSubldgTetrajetEta_After;

  delete hTrijet1Mass_Before;
  delete hTrijet2Mass_Before;
  delete hTrijet1Mass_After;
  delete hTrijet2Mass_After;
  delete hTrijet1Pt_Before;
  delete hTrijet2Pt_Before;
  delete hTrijet1Pt_After;
  delete hTrijet2Pt_After;

  delete hTrijet1DijetMass_Before;
  delete hTrijet2DijetMass_Before;
  delete hTrijet1DijetMass_After;
  delete hTrijet2DijetMass_After;
  delete hTrijet1DijetPt_Before;
  delete hTrijet2DijetPt_Before;
  delete hTrijet1DijetPt_After;
  delete hTrijet2DijetPt_After;
  delete hTrijet1DijetDEta_Before;
  delete hTrijet2DijetDEta_Before;
  delete hTrijet1DijetDEta_After;
  delete hTrijet2DijetDEta_After;
  delete hTrijet1DijetDPhi_Before;
  delete hTrijet2DijetDPhi_Before;
  delete hTrijet1DijetDPhi_After;
  delete hTrijet2DijetDPhi_After;
  delete hTrijet1DijetDR_Before;
  delete hTrijet2DijetDR_Before;
  delete hTrijet1DijetDR_After;
  delete hTrijet2DijetDR_After;

  delete hTrijet1DijetBJetDR_Before;
  delete hTrijet2DijetBJetDR_Before;
  delete hTrijet1DijetBJetDR_After;
  delete hTrijet2DijetBJetDR_After;
  delete hTrijet1DijetBJetDPhi_Before;
  delete hTrijet2DijetBJetDPhi_Before;
  delete hTrijet1DijetBJetDPhi_After;
  delete hTrijet2DijetBJetDPhi_After;
  delete hTrijet1DijetBJetDEta_Before;
  delete hTrijet2DijetBJetDEta_Before;
  delete hTrijet1DijetBJetDEta_After;
  delete hTrijet2DijetBJetDEta_After;

  delete hLdgTrijetPt_Before;
  delete hLdgTrijetPt_After;
  delete hLdgTrijetMass_Before;
  delete hLdgTrijetMass_After;
  delete hLdgTrijetJet1Pt_Before;
  delete hLdgTrijetJet1Pt_After;
  delete hLdgTrijetJet1Eta_Before;
  delete hLdgTrijetJet1Eta_After;
  delete hLdgTrijetJet1BDisc_Before;
  delete hLdgTrijetJet1BDisc_After;
  delete hLdgTrijetJet2Pt_Before;
  delete hLdgTrijetJet2Pt_After;
  delete hLdgTrijetJet2Eta_Before;
  delete hLdgTrijetJet2Eta_After;
  delete hLdgTrijetJet2BDisc_Before;
  delete hLdgTrijetJet2BDisc_After;
  delete hLdgTrijetBJetPt_Before;
  delete hLdgTrijetBJetPt_After;
  delete hLdgTrijetBJetEta_Before;
  delete hLdgTrijetBJetEta_After;
  delete hLdgTrijetBJetBDisc_Before;
  delete hLdgTrijetBJetBDisc_After;
  delete hLdgTrijetDiJetPt_Before;
  delete hLdgTrijetDiJetPt_After;
  delete hLdgTrijetDiJetEta_Before;
  delete hLdgTrijetDiJetEta_After;
  delete hLdgTrijetDiJetMass_Before;
  delete hLdgTrijetDiJetMass_After;

  delete hSubldgTrijetPt_Before;
  delete hSubldgTrijetPt_After;
  delete hSubldgTrijetMass_Before;
  delete hSubldgTrijetMass_After;
  delete hSubldgTrijetJet1Pt_Before;
  delete hSubldgTrijetJet1Pt_After;
  delete hSubldgTrijetJet1Eta_Before;
  delete hSubldgTrijetJet1Eta_After;
  delete hSubldgTrijetJet1BDisc_Before;
  delete hSubldgTrijetJet1BDisc_After;
  delete hSubldgTrijetJet2Pt_Before;
  delete hSubldgTrijetJet2Pt_After;
  delete hSubldgTrijetJet2Eta_Before;
  delete hSubldgTrijetJet2Eta_After;
  delete hSubldgTrijetJet2BDisc_Before;
  delete hSubldgTrijetJet2BDisc_After;
  delete hSubldgTrijetBJetPt_Before;
  delete hSubldgTrijetBJetPt_After;
  delete hSubldgTrijetBJetEta_Before;
  delete hSubldgTrijetBJetEta_After;
  delete hSubldgTrijetBJetBDisc_Before;
  delete hSubldgTrijetBJetBDisc_After;
  delete hSubldgTrijetDiJetPt_Before;
  delete hSubldgTrijetDiJetPt_After;
  delete hSubldgTrijetDiJetEta_Before;
  delete hSubldgTrijetDiJetEta_After;
  delete hSubldgTrijetDiJetMass_Before;
  delete hSubldgTrijetDiJetMass_After;

  // Histograms (2D)
  delete hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DPhiVsDPhi_Before;
  delete hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DPhiVsDPhi_After;
  delete hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DRVsDR_Before;
  delete hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DRVsDR_After;
  delete hTrijet1MassVsChiSqr_Before;
  delete hTrijet2MassVsChiSqr_Before;
  delete hTrijet1MassVsChiSqr_After;
  delete hTrijet2MassVsChiSqr_After;
  delete hTrijet1DijetPtVsDijetDR_Before;
  delete hTrijet2DijetPtVsDijetDR_Before;
  delete hTrijet1DijetPtVsDijetDR_After;
  delete hTrijet2DijetPtVsDijetDR_After;

}

void TopSelection::initialize(const ParameterSet& config) {
  
}

void TopSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kVital, dir, "topSelection_"+sPostfix);

  // Fixed binning
  const int nBinsPt    = 100;
  const double minPt   = 0.0;
  const double maxPt   = 1000.0;
  const int nBinsM     = 150;
  const double minM    = 0.0;
  const double maxM    = 1500.0;
  const int nBinsdEta  = 50;
  const double mindEta = 0.0;
  const double maxdEta = 10.0;
  const int nBinsdPhi  = 32;
  const double mindPhi = 0.0;
  const double maxdPhi = 3.2;
  const int nBinsdR    = 50;
  const double mindR   = 0.0;
  const double maxdR   = 10.0;
  const int  nBinsBDisc= fCommonPlots->getBJetDiscBinSettings().bins();
  const float minBDisc = fCommonPlots->getBJetDiscBinSettings().min();
  const float maxBDisc = fCommonPlots->getBJetDiscBinSettings().max();
  const int  nBinsEta  = fCommonPlots->getEtaBinSettings().bins();
  const float minEta   = fCommonPlots->getEtaBinSettings().min();
  const float maxEta   = fCommonPlots->getEtaBinSettings().max();
  // const int nBinsJets  = fCommonPlots->getNjetsBinSettings().bins();
  // const int minJets    = fCommonPlots->getNjetsBinSettings().min();
  // const int maxJets    = fCommonPlots->getNjetsBinSettings().max();

  // Histograms (1D) 
  hChiSqr_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "ChiSqr_Before", ";#chi^{2}", 1000,  0.0, 1000.0);
  hChiSqr_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "ChiSqr_After" , ";#chi^{2}", 1000,  0.0, 1000.0);
  hNJetsUsedAsBJetsInFit_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "NJetsUsedAsBJetsInFit_Before", ";failed b-Jets Multiplicity;Events / %0.f GeV/c^{2}", 8, -0.5, 7.5);
  hNJetsUsedAsBJetsInFit_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "NJetsUsedAsBJetsInFit_After" , ";failed b-Jets Multiplicity;Events / %0.f GeV/c^{2}", 8, -0.5, 7.5);
  hNumberOfFits_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "NumberOfFits_Before", ";number of di-top fits;Events / %0.f GeV/c^{2}", 500, 0.0, 500.0);
  hNumberOfFits_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "NumberOfFits_After" , ";number of di-top fits;Events / %0.f GeV/c^{2}", 500, 0.0, 500.0);

  hTetrajetBJetPt_Before    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetPt_Before"   ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hTetrajetBJetPt_After     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetPt_After"    ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hTetrajetBJetEta_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetEta_Before"  ,";#eta", nBinsEta, minEta, maxEta);
  hTetrajetBJetEta_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetEta_After"   ,";#eta", nBinsEta, minEta, maxEta);
  hTetrajetBJetBDisc_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetBDisc_Before",";b-tag discriminator",  nBinsBDisc, minBDisc, maxBDisc);
  hTetrajetBJetBDisc_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "TetrajetBJetBDisc_After" ,";b-tag discriminator",  nBinsBDisc, minBDisc, maxBDisc);
  hTetrajet1Pt_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Tetrajet1Pt_Before"  , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hTetrajet1Mass_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Tetrajet1Mass_Before", ";M (GeV/c^{2})", nBinsM*4, minM, maxM*4);
  hTetrajet1Eta_Before  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Tetrajet1Eta_Before"  , ";#eta", nBinsEta, minEta, maxEta);
  hTetrajet1Pt_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Tetrajet1Pt_After"   , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hTetrajet1Mass_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Tetrajet1Mass_After" , ";M (GeV/c^{2})", nBinsM*4, minM, maxM*4);
  hTetrajet1Eta_After   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Tetrajet1Eta_After"   , ";#eta", nBinsEta, minEta, maxEta);
  hTetrajet2Pt_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Tetrajet2Pt_Before"  , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hTetrajet2Mass_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Tetrajet2Mass_Before", ";M (GeV/c^{2})", nBinsM*4, minM, maxM*4);
  hTetrajet2Eta_Before  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Tetrajet2Eta_Before"  , ";#eta", nBinsEta, minEta, maxEta);
  hTetrajet2Pt_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Tetrajet2Pt_After"   , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hTetrajet2Mass_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Tetrajet2Mass_After" , ";M (GeV/c^{2})", nBinsM*4, minM, maxM*4);
  hTetrajet2Eta_After   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Tetrajet2Eta_After"   , ";#eta", nBinsEta, minEta, maxEta);
  hLdgTetrajetPt_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTetrajetPt_Before"  , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hLdgTetrajetMass_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTetrajetMass_Before", ";M (GeV/c^{2})", nBinsM*4, minM, maxM*4);
  hLdgTetrajetEta_Before  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTetrajetEta_Before"  , ";#eta", nBinsEta, minEta, maxEta);
  hLdgTetrajetPt_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTetrajetPt_After"   , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hLdgTetrajetMass_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTetrajetMass_After" , ";M (GeV/c^{2})", nBinsM*4, minM, maxM*4);
  hLdgTetrajetEta_After   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTetrajetEta_After"   , ";#eta", nBinsEta, minEta, maxEta);
  hSubldgTetrajetPt_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTetrajetPt_Before"  , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hSubldgTetrajetMass_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTetrajetMass_Before", ";M (GeV/c^{2})", nBinsM*4, minM, maxM*4);
  hSubldgTetrajetEta_Before  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTetrajetEta_Before"  , ";#eta", nBinsEta, minEta, maxEta);
  hSubldgTetrajetPt_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTetrajetPt_After"   , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hSubldgTetrajetMass_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTetrajetMass_After" , ";M (GeV/c^{2})", nBinsM*4, minM, maxM*4);
  hSubldgTetrajetEta_After   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTetrajetEta_After"   , ";#eta", nBinsEta, minEta, maxEta);

  hTrijet1Mass_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1Mass_Before", ";M (GeV/c^{2})", nBinsM, minM, maxM);
  hTrijet2Mass_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2Mass_Before", ";M (GeV/c^{2})", nBinsM, minM, maxM);
  hTrijet1Mass_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1Mass_After" , ";M (GeV/c^{2})", nBinsM, minM, maxM);
  hTrijet2Mass_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2Mass_After" , ";M (GeV/c^{2})", nBinsM, minM, maxM);
  hTrijet1Pt_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1Pt_Before", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hTrijet2Pt_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2Pt_Before", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hTrijet1Pt_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1Pt_After" , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hTrijet2Pt_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2Pt_After" , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);

  hTrijet1DijetMass_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1DijetMass_Before", ";M (GeV/c^{2})", nBinsM, minM, maxM);
  hTrijet2DijetMass_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2DijetMass_Before", ";M (GeV/c^{2})", nBinsM, minM, maxM);
  hTrijet1DijetMass_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1DijetMass_After" , ";M (GeV/c^{2})", nBinsM, minM, maxM);
  hTrijet2DijetMass_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2DijetMass_After" , ";M (GeV/c^{2})", nBinsM, minM, maxM);
  hTrijet1DijetPt_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1DijetPt_Before"  , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hTrijet2DijetPt_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2DijetPt_Before"  , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hTrijet1DijetPt_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1DijetPt_After"   , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hTrijet2DijetPt_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2DijetPt_After"   , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hTrijet1DijetDR_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1DijetDR_Before"  , ";#Delta R(j_{1},j_{2})"  , nBinsdR  , mindR  , maxdR);
  hTrijet2DijetDR_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2DijetDR_Before"  , ";#Delta R(j_{1},j_{2})"  , nBinsdR  , mindR  , maxdR);
  hTrijet1DijetDR_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1DijetDR_After"   , ";#Delta R(j_{1},j_{2})"  , nBinsdR  , mindR  , maxdR);
  hTrijet2DijetDR_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2DijetDR_After"   , ";#Delta R(j_{1},j_{2})"  , nBinsdR  , mindR  , maxdR);
  hTrijet1DijetDPhi_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1DijetDPhi_Before", ";#Delta#phi(j_{1},j_{2})", nBinsdPhi, mindPhi, maxdPhi);
  hTrijet2DijetDPhi_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2DijetDPhi_Before", ";#Delta#phi(j_{1},j_{2})", nBinsdPhi, mindPhi, maxdPhi);
  hTrijet1DijetDPhi_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1DijetDPhi_After" , ";#Delta#phi(j_{1},j_{2})", nBinsdPhi, mindPhi, maxdPhi);
  hTrijet2DijetDPhi_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2DijetDPhi_After" , ";#Delta#phi(j_{1},j_{2})", nBinsdPhi, mindPhi, maxdPhi);
  hTrijet1DijetDEta_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1DijetDEta_Before", ";#Delta#eta(j_{1},j_{2})", nBinsdEta, mindEta, maxdEta);
  hTrijet2DijetDEta_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2DijetDEta_Before", ";#Delta#eta(j_{1},j_{2})", nBinsdEta, mindEta, maxdEta);
  hTrijet1DijetDEta_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1DijetDEta_After" , ";#Delta#eta(j_{1},j_{2})", nBinsdEta, mindEta, maxdEta);
  hTrijet2DijetDEta_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2DijetDEta_After" , ";#Delta#eta(j_{1},j_{2})", nBinsdEta, mindEta, maxdEta);

  hTrijet1DijetBJetDEta_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1DijetBJetDEta_Before", ";#Delta#eta(jj,bjet)", nBinsdEta, mindEta, maxdEta);
  hTrijet2DijetBJetDEta_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2DijetBJetDEta_Before", ";#Delta#eta(jj,bjet)", nBinsdEta, mindEta, maxdEta);
  hTrijet1DijetBJetDEta_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1DijetBJetDEta_After" , ";#Delta#eta(jj,bjet)", nBinsdEta, mindEta, maxdEta);
  hTrijet2DijetBJetDEta_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2DijetBJetDEta_After" , ";#Delta#eta(jj,bjet)", nBinsdEta, mindEta, maxdEta);
  hTrijet1DijetBJetDPhi_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1DijetBJetDPhi_Before", ";#Delta#phi(jj,bjet)", nBinsdPhi, mindPhi, maxdPhi);
  hTrijet2DijetBJetDPhi_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2DijetBJetDPhi_Before", ";#Delta#phi(jj,bjet)", nBinsdPhi, mindPhi, maxdPhi);
  hTrijet1DijetBJetDPhi_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1DijetBJetDPhi_After" , ";#Delta#phi(jj,bjet)", nBinsdPhi, mindPhi, maxdPhi);
  hTrijet2DijetBJetDPhi_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2DijetBJetDPhi_After" , ";#Delta#phi(jj,bjet)", nBinsdPhi, mindPhi, maxdPhi);
  hTrijet1DijetBJetDR_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1DijetBJetDR_Before"  , ";#Delta R(jj,bjet)"  , nBinsdR  , mindR  , maxdR);
  hTrijet2DijetBJetDR_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2DijetBJetDR_Before"  , ";#Delta R(jj,bjet)"  , nBinsdR  , mindR  , maxdR);
  hTrijet1DijetBJetDR_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet1DijetBJetDR_After"   , ";#Delta R(jj,bjet)"  , nBinsdR  , mindR  , maxdR);
  hTrijet2DijetBJetDR_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Trijet2DijetBJetDR_After"   , ";#Delta R(jj,bjet)"  , nBinsdR  , mindR  , maxdR);

  hLdgTrijetPt_Before        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetPt_Before"       ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hLdgTrijetPt_After         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetPt_After"        ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hLdgTrijetMass_Before      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetMass_Before"     ,";M (GeV/c^{2})", nBinsM, minM, maxM);
  hLdgTrijetMass_After       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetMass_After"      ,";M (GeV/c^{2})", nBinsM, minM, maxM);
  hLdgTrijetJet1Pt_Before    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet1Pt_Before"   ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hLdgTrijetJet1Pt_After     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet1Pt_After"    ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hLdgTrijetJet1Eta_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet1Eta_Before"  ,";#eta", nBinsEta, minEta, maxEta);
  hLdgTrijetJet1Eta_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet1Eta_After"   ,";#eta", nBinsEta, minEta, maxEta);
  hLdgTrijetJet1BDisc_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet1BDisc_Before",";b-tag discriminator",  nBinsBDisc, minBDisc, maxBDisc);
  hLdgTrijetJet1BDisc_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet1BDisc_After" ,";b-tag discriminator",  nBinsBDisc, minBDisc, maxBDisc);
  hLdgTrijetJet2Pt_Before    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet2Pt_Before"   ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hLdgTrijetJet2Pt_After     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet2Pt_After"    ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hLdgTrijetJet2Eta_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet2Eta_Before"  ,";#eta", nBinsEta, minEta, maxEta);
  hLdgTrijetJet2Eta_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet2Eta_After"   ,";#eta", nBinsEta, minEta, maxEta);
  hLdgTrijetJet2BDisc_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet2BDisc_Before",";b-tag discriminator",  nBinsBDisc, minBDisc, maxBDisc);
  hLdgTrijetJet2BDisc_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetJet2BDisc_After" ,";b-tag discriminator",  nBinsBDisc, minBDisc, maxBDisc);
  hLdgTrijetBJetPt_Before    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetBJetPt_Before"   ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hLdgTrijetBJetPt_After     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetBJetPt_After"    ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hLdgTrijetBJetEta_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetBJetEta_Before"  ,";#eta", nBinsEta, minEta, maxEta);
  hLdgTrijetBJetEta_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetBJetEta_After"   ,";#eta", nBinsEta, minEta, maxEta);
  hLdgTrijetBJetBDisc_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetBJetBDisc_Before",";b-tag discriminator",  nBinsBDisc, minBDisc, maxBDisc);
  hLdgTrijetBJetBDisc_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetBJetBDisc_After" ,";b-tag discriminator",  nBinsBDisc, minBDisc, maxBDisc);
  hLdgTrijetDiJetPt_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetDiJetPt_Before"  ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hLdgTrijetDiJetPt_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetDiJetPt_After"   ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hLdgTrijetDiJetEta_Before  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetDiJetEta_Before" ,";#eta", nBinsEta, minEta, maxEta);
  hLdgTrijetDiJetEta_After   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetDiJetEta_After"  ,";#eta", nBinsEta, minEta, maxEta);
  hLdgTrijetDiJetMass_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetDiJetMass_Before",";M (GeV/c^{2})", nBinsM, minM, maxM);
  hLdgTrijetDiJetMass_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LdgTrijetDiJetMass_After" ,";M (GeV/c^{2})", nBinsM, minM, maxM);

  hSubldgTrijetPt_Before        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetPt_Before"       ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hSubldgTrijetPt_After         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetPt_After"        ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hSubldgTrijetMass_Before      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetMass_Before"     ,";M (GeV/c^{2})", nBinsM, minM, maxM);
  hSubldgTrijetMass_After       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetMass_After"      ,";M (GeV/c^{2})", nBinsM, minM, maxM);
  hSubldgTrijetJet1Pt_Before    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet1Pt_Before"   ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hSubldgTrijetJet1Pt_After     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet1Pt_After"    ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hSubldgTrijetJet1Eta_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet1Eta_Before"  ,";#eta", nBinsEta, minEta, maxEta);
  hSubldgTrijetJet1Eta_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet1Eta_After"   ,";#eta", nBinsEta, minEta, maxEta);
  hSubldgTrijetJet1BDisc_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet1BDisc_Before",";b-tag discriminator",  nBinsBDisc, minBDisc, maxBDisc);
  hSubldgTrijetJet1BDisc_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet1BDisc_After" ,";b-tag discriminator",  nBinsBDisc, minBDisc, maxBDisc);
  hSubldgTrijetJet2Pt_Before    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet2Pt_Before"   ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hSubldgTrijetJet2Pt_After     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet2Pt_After"    ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hSubldgTrijetJet2Eta_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet2Eta_Before"  ,";#eta", nBinsEta, minEta, maxEta);
  hSubldgTrijetJet2Eta_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet2Eta_After"   ,";#eta", nBinsEta, minEta, maxEta);
  hSubldgTrijetJet2BDisc_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet2BDisc_Before",";b-tag discriminator",  nBinsBDisc, minBDisc, maxBDisc);
  hSubldgTrijetJet2BDisc_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetJet2BDisc_After" ,";b-tag discriminator",  nBinsBDisc, minBDisc, maxBDisc);
  hSubldgTrijetBJetPt_Before    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetBJetPt_Before"   ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hSubldgTrijetBJetPt_After     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetBJetPt_After"    ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hSubldgTrijetBJetEta_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetBJetEta_Before"  ,";#eta", nBinsEta, minEta, maxEta);
  hSubldgTrijetBJetEta_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetBJetEta_After"   ,";#eta", nBinsEta, minEta, maxEta);
  hSubldgTrijetBJetBDisc_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetBJetBDisc_Before",";b-tag discriminator",  nBinsBDisc, minBDisc, maxBDisc);
  hSubldgTrijetBJetBDisc_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetBJetBDisc_After" ,";b-tag discriminator",  nBinsBDisc, minBDisc, maxBDisc);
  hSubldgTrijetDiJetPt_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetDiJetPt_Before"  ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hSubldgTrijetDiJetPt_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetDiJetPt_After"   ,";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hSubldgTrijetDiJetEta_Before  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetDiJetEta_Before" ,";#eta", nBinsEta, minEta, maxEta);
  hSubldgTrijetDiJetEta_After   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetDiJetEta_After"  ,";#eta", nBinsEta, minEta, maxEta);
  hSubldgTrijetDiJetMass_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetDiJetMass_Before",";M (GeV/c^{2})", nBinsM, minM, maxM);
  hSubldgTrijetDiJetMass_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SubldgTrijetDiJetMass_After" ,";M (GeV/c^{2})", nBinsM, minM, maxM);

  // Histograms (2D) 
  hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DPhiVsDPhi_Before = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "TetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DPhiVsDPhi_Before", ";#Delta#phi (rads); #Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi, nBinsdPhi, mindPhi, maxdPhi);
  hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DPhiVsDPhi_After = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "TetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DPhiVsDPhi_After", ";#Delta#phi (rads); #Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi, nBinsdPhi, mindPhi, maxdPhi);
  hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DRVsDR_Before = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "TetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DRVsDR_Before", ";#DeltaR; #DeltaR", nBinsdR, mindR, maxdR, nBinsdR, mindR, maxdR);
  hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DRVsDR_After = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "TetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DRVsDR_After", ";#DeltaR; #DeltaR", nBinsdR, mindR, maxdR, nBinsdR, mindR, maxdR);
  hTrijet1MassVsChiSqr_Before = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "Trijet1MassVsChiSqr_Before", ";M (GeV/c^{2}); #chi^{2}", nBinsM, minM, maxM, 300, 0.0, 300.0);
  hTrijet2MassVsChiSqr_Before = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "Trijet2MassVsChiSqr_Before", ";M (GeV/c^{2}); #chi^{2}", nBinsM, minM, maxM, 300, 0.0, 300.0);
  hTrijet1MassVsChiSqr_After  = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "Trijet1MassVsChiSqr_After" , ";M (GeV/c^{2}); #chi^{2}", nBinsM, minM, maxM, 300, 0.0, 300.0);
  hTrijet2MassVsChiSqr_After  = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "Trijet2MassVsChiSqr_After" , ";M (GeV/c^{2}); #chi^{2}", nBinsM, minM, maxM, 300, 0.0, 300.0);
  hTrijet1DijetPtVsDijetDR_Before = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "Trijet1DijetPtVsDijetDR_Before", ";p_{T} (GeV/c);#Delta R(j_{1},j_{2}", nBinsPt, minPt, maxPt, nBinsdR, mindR, maxdR);
  hTrijet2DijetPtVsDijetDR_Before = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "Trijet2DijetPtVsDijetDR_Before", ";p_{T} (GeV/c);#Delta R(j_{1},j_{2}", nBinsPt, minPt, maxPt, nBinsdR, mindR, maxdR);
  hTrijet1DijetPtVsDijetDR_After  = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "Trijet1DijetPtVsDijetDR_After" , ";p_{T} (GeV/c);#Delta R(j_{1},j_{2}", nBinsPt, minPt, maxPt, nBinsdR, mindR, maxdR);
  hTrijet2DijetPtVsDijetDR_After  = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "Trijet2DijetPtVsDijetDR_After" , ";p_{T} (GeV/c);#Delta R(j_{1},j_{2}", nBinsPt, minPt, maxPt, nBinsdR, mindR, maxdR);

  return;
}

TopSelection::Data TopSelection::silentAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  ensureSilentAnalyzeAllowed(event.eventID());
  nSelectedBJets = bjetData.getSelectedBJets().size();

  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, jetData.getSelectedJets(), bjetData.getSelectedBJets());
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
  Data data = privateAnalyzeWithoutBJets(event, jetData.getSelectedJets(), GetBjetsToBeUsedInFit(bjetData, maxNumberOfBJetsInTopFit) );
  // Re-enable histogram filling and counter
  enableHistogramsAndCounters();
  return data;
}


TopSelection::Data TopSelection::analyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  ensureAnalyzeAllowed(event.eventID());
  nSelectedBJets = bjetData.getSelectedBJets().size();

  // Ready to analyze
  TopSelection::Data data = privateAnalyze(event, jetData.getSelectedJets(), bjetData.getSelectedBJets());

  // Send data to CommonPlots
  // if (fCommonPlots != nullptr) fCommonPlots->fillControlPlotsAtTopSelection(event, data); //fixme
  return data;
}

TopSelection::Data TopSelection::analyzeWithoutBJets(const Event& event, 
						     const JetSelection::Data& jetData, 
						     const BJetSelection::Data& bjetData,
						     const unsigned int maxNumberOfBJetsInTopFit) {
  ensureAnalyzeAllowed(event.eventID());
  nSelectedBJets = bjetData.getSelectedBJets().size();

  // Ready to analyze
  TopSelection::Data data = privateAnalyze(event, jetData.getSelectedJets(), GetBjetsToBeUsedInFit(bjetData, maxNumberOfBJetsInTopFit) );

  // Send data to CommonPlots
  // if (fCommonPlots != nullptr) fCommonPlots->fillControlPlotsAtTopSelection(event, data);
  return data;
}

TopSelection::Data TopSelection::privateAnalyze(const Event& event, const std::vector<Jet> jets, const std::vector<Jet> bjets) {
  Data output;
  cSubAll.increment();
  
  // Initialise variables
  output.fJetsUsedAsBJetsInFit = bjets;
  std::vector<unsigned int> bjet1;
  std::vector<unsigned int> bjet2;
  std::vector<unsigned int> jet1;
  std::vector<unsigned int> jet2;
  std::vector<unsigned int> jet3;
  std::vector<unsigned int> jet4;
  double minChiSqr = 1e9;

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
	if (output.fTetrajet1_p4.pt() > output.fTetrajet2_p4.pt()) 
	  {
	    output.fLdgTetrajet_p4    = output.fTetrajet1_p4;
	    output.fSubldgTetrajet_p4 = output.fTetrajet2_p4;
	  }
	else	  
	  {
	    output.fLdgTetrajet_p4    = output.fTetrajet2_p4;
	    output.fSubldgTetrajet_p4 = output.fTetrajet1_p4;
	  }
      }
    }
  
  // Sanity check: Did I get at least 1 successful fit?
  if (minChiSqr == 1e9) return output;

  // Fill Histograms (Before cuts)
  hChiSqr_Before->Fill( output.fChiSqr );
  hNJetsUsedAsBJetsInFit_Before->Fill( output.fJetsUsedAsBJetsInFit.size() - nSelectedBJets );
  hNumberOfFits_Before->Fill( output.fNumberOfFits );
  hTrijet1Mass_Before->Fill(output.fTrijet1_p4.mass());
  hTrijet2Mass_Before->Fill(output.fTrijet2_p4.mass());
  hTrijet1Pt_Before->Fill(output.fTrijet1_p4.pt());
  hTrijet2Pt_Before->Fill(output.fTrijet2_p4.pt());
  hTrijet1DijetMass_Before->Fill( output.fTrijet1Dijet_p4.mass() );
  hTrijet2DijetMass_Before->Fill( output.fTrijet2Dijet_p4.mass() );
  hTrijet1DijetPt_Before->Fill( output.fTrijet1Dijet_p4.pt() );
  hTrijet2DijetPt_Before->Fill( output.fTrijet2Dijet_p4.pt() );
  hTrijet1DijetDEta_Before->Fill( std::abs( output.fTrijet1Jet1.p4().eta() - output.fTrijet1Jet2.p4().eta() ) );
  hTrijet2DijetDEta_Before->Fill( std::abs( output.fTrijet2Jet1.p4().eta() - output.fTrijet2Jet2.p4().eta() ) );
  hTrijet1DijetDPhi_Before->Fill( std::abs( ROOT::Math::VectorUtil::DeltaPhi( output.fTrijet1Jet1.p4(), output.fTrijet1Jet2.p4() ) ) );
  hTrijet2DijetDPhi_Before->Fill( std::abs( ROOT::Math::VectorUtil::DeltaPhi( output.fTrijet2Jet1.p4(), output.fTrijet2Jet2.p4() ) ) );
  hTrijet1DijetDR_Before  ->Fill( ROOT::Math::VectorUtil::DeltaR( output.fTrijet1Jet1.p4(), output.fTrijet1Jet2.p4() ) );
  hTrijet2DijetDR_Before  ->Fill( ROOT::Math::VectorUtil::DeltaR( output.fTrijet2Jet1.p4(), output.fTrijet2Jet2.p4() ) );
  hTrijet1DijetBJetDEta_Before->Fill( std::abs( output.fTrijet1Dijet_p4.eta() - output.fTrijet1BJet.p4().eta() ) );
  hTrijet2DijetBJetDEta_Before->Fill( std::abs( output.fTrijet2Dijet_p4.eta() - output.fTrijet2BJet.p4().eta() ) );
  hTrijet1DijetBJetDPhi_Before->Fill( std::abs( ROOT::Math::VectorUtil::DeltaPhi( output.fTrijet1Dijet_p4, output.fTrijet1BJet.p4() ) ) );
  hTrijet2DijetBJetDPhi_Before->Fill( std::abs( ROOT::Math::VectorUtil::DeltaPhi( output.fTrijet2Dijet_p4, output.fTrijet2BJet.p4() ) ) );
  hTrijet1DijetBJetDR_Before  ->Fill( ROOT::Math::VectorUtil::DeltaR( output.fTrijet1Dijet_p4, output.fTrijet1BJet.p4() ) );
  hTrijet2DijetBJetDR_Before  ->Fill( ROOT::Math::VectorUtil::DeltaR( output.fTrijet2Dijet_p4, output.fTrijet2BJet.p4() ) );
  // Leading/Subleading tops
  if (output.fTrijet1_p4.pt() > output.fTrijet2_p4.pt()) 
    {
      // Leading
      hLdgTrijetPt_Before       ->Fill(output.fTrijet1_p4.pt());
      hLdgTrijetMass_Before     ->Fill(output.fTrijet1_p4.mass());
      hLdgTrijetJet1Pt_Before   ->Fill(output.fTrijet1Jet1.pt());
      hLdgTrijetJet1Eta_Before  ->Fill(output.fTrijet1Jet1.eta());
      hLdgTrijetJet1BDisc_Before->Fill(output.fTrijet1Jet1.bjetDiscriminator());
      hLdgTrijetJet2Pt_Before   ->Fill(output.fTrijet1Jet2.pt());
      hLdgTrijetJet2Eta_Before  ->Fill(output.fTrijet1Jet2.eta());
      hLdgTrijetJet2BDisc_Before->Fill(output.fTrijet1Jet2.bjetDiscriminator());
      hLdgTrijetBJetPt_Before   ->Fill(output.fTrijet1BJet.pt());
      hLdgTrijetBJetEta_Before  ->Fill(output.fTrijet1BJet.eta());
      hLdgTrijetBJetBDisc_Before->Fill(output.fTrijet1BJet.bjetDiscriminator());
      hLdgTrijetDiJetPt_Before  ->Fill(output.fTrijet1Dijet_p4.pt());
      hLdgTrijetDiJetEta_Before ->Fill(output.fTrijet1Dijet_p4.eta());
      hLdgTrijetDiJetMass_Before->Fill(output.fTrijet1Dijet_p4.mass());
      // Subleading
      hSubldgTrijetPt_Before       ->Fill(output.fTrijet2_p4.pt());
      hSubldgTrijetMass_Before     ->Fill(output.fTrijet2_p4.mass());
      hSubldgTrijetPt_Before       ->Fill(output.fTrijet2_p4.pt());
      hSubldgTrijetMass_Before     ->Fill(output.fTrijet2_p4.mass());
      hSubldgTrijetJet1Pt_Before   ->Fill(output.fTrijet2Jet1.pt());
      hSubldgTrijetJet1Eta_Before  ->Fill(output.fTrijet2Jet1.eta());
      hSubldgTrijetJet1BDisc_Before->Fill(output.fTrijet2Jet1.bjetDiscriminator());
      hSubldgTrijetJet2Pt_Before   ->Fill(output.fTrijet2Jet2.pt());
      hSubldgTrijetJet2Eta_Before  ->Fill(output.fTrijet2Jet2.eta());
      hSubldgTrijetJet2BDisc_Before->Fill(output.fTrijet2Jet2.bjetDiscriminator());
      hSubldgTrijetBJetPt_Before   ->Fill(output.fTrijet2BJet.pt());
      hSubldgTrijetBJetEta_Before  ->Fill(output.fTrijet2BJet.eta());
      hSubldgTrijetBJetBDisc_Before->Fill(output.fTrijet2BJet.bjetDiscriminator());
      hSubldgTrijetDiJetPt_Before  ->Fill(output.fTrijet2Dijet_p4.pt());
      hSubldgTrijetDiJetEta_Before ->Fill(output.fTrijet2Dijet_p4.eta());
      hSubldgTrijetDiJetMass_Before->Fill(output.fTrijet2Dijet_p4.mass());
    }
  else 
    {
      // Leading
      hLdgTrijetPt_Before       ->Fill(output.fTrijet2_p4.pt());
      hLdgTrijetMass_Before     ->Fill(output.fTrijet2_p4.mass());
      hLdgTrijetJet1Pt_Before   ->Fill(output.fTrijet2Jet1.pt());
      hLdgTrijetJet1Eta_Before  ->Fill(output.fTrijet2Jet1.eta());
      hLdgTrijetJet1BDisc_Before->Fill(output.fTrijet2Jet1.bjetDiscriminator());
      hLdgTrijetJet2Pt_Before   ->Fill(output.fTrijet2Jet2.pt());
      hLdgTrijetJet2Eta_Before  ->Fill(output.fTrijet2Jet2.eta());
      hLdgTrijetJet2BDisc_Before->Fill(output.fTrijet2Jet2.bjetDiscriminator());
      hLdgTrijetBJetPt_Before   ->Fill(output.fTrijet2BJet.pt());
      hLdgTrijetBJetEta_Before  ->Fill(output.fTrijet2BJet.eta());
      hLdgTrijetBJetBDisc_Before->Fill(output.fTrijet2BJet.bjetDiscriminator());
      hLdgTrijetDiJetPt_Before  ->Fill(output.fTrijet2Dijet_p4.pt());
      hLdgTrijetDiJetEta_Before ->Fill(output.fTrijet2Dijet_p4.eta());
      hLdgTrijetDiJetMass_Before->Fill(output.fTrijet2Dijet_p4.mass());
      // Subleading
      hSubldgTrijetPt_Before       ->Fill(output.fTrijet1_p4.pt());
      hSubldgTrijetMass_Before     ->Fill(output.fTrijet1_p4.mass());
      hSubldgTrijetJet1Pt_Before   ->Fill(output.fTrijet1Jet1.pt());
      hSubldgTrijetJet1Eta_Before  ->Fill(output.fTrijet1Jet1.eta());
      hSubldgTrijetJet1BDisc_Before->Fill(output.fTrijet1Jet1.bjetDiscriminator());
      hSubldgTrijetJet2Pt_Before   ->Fill(output.fTrijet1Jet2.pt());
      hSubldgTrijetJet2Eta_Before  ->Fill(output.fTrijet1Jet2.eta());
      hSubldgTrijetJet2BDisc_Before->Fill(output.fTrijet1Jet2.bjetDiscriminator());
      hSubldgTrijetBJetPt_Before   ->Fill(output.fTrijet1BJet.pt());
      hSubldgTrijetBJetEta_Before  ->Fill(output.fTrijet1BJet.eta());
      hSubldgTrijetBJetBDisc_Before->Fill(output.fTrijet1BJet.bjetDiscriminator());
      hSubldgTrijetDiJetPt_Before  ->Fill(output.fTrijet1Dijet_p4.pt());
      hSubldgTrijetDiJetEta_Before ->Fill(output.fTrijet1Dijet_p4.eta());
      hSubldgTrijetDiJetMass_Before->Fill(output.fTrijet1Dijet_p4.mass());
    }

  // Tetrajet
  hTetrajetBJetPt_Before    ->Fill(output.fTetrajetBJet.pt());
  hTetrajetBJetEta_Before   ->Fill(output.fTetrajetBJet.eta());
  hTetrajetBJetBDisc_Before ->Fill(output.fTetrajetBJet.bjetDiscriminator());
  hTetrajet1Pt_Before       ->Fill(output.fTetrajet1_p4.pt());
  hTetrajet1Mass_Before     ->Fill(output.fTetrajet1_p4.mass());
  hTetrajet1Eta_Before      ->Fill(output.fTetrajet1_p4.eta());
  hTetrajet2Pt_Before       ->Fill(output.fTetrajet2_p4.pt());
  hTetrajet2Mass_Before     ->Fill(output.fTetrajet2_p4.mass());
  hTetrajet2Eta_Before      ->Fill(output.fTetrajet2_p4.eta());
  hLdgTetrajetPt_Before     ->Fill(output.fLdgTetrajet_p4.pt());
  hLdgTetrajetMass_Before   ->Fill(output.fLdgTetrajet_p4.mass());
  hLdgTetrajetEta_Before    ->Fill(output.fLdgTetrajet_p4.eta());
  hSubldgTetrajetPt_Before  ->Fill(output.fSubldgTetrajet_p4.pt());
  hSubldgTetrajetMass_Before->Fill(output.fSubldgTetrajet_p4.mass());
  hSubldgTetrajetEta_Before ->Fill(output.fSubldgTetrajet_p4.eta());

  // 2-D histos
  double dRMin   = ROOT::Math::VectorUtil::DeltaR(output.fDijetWithMinDR_p4, output.fTetrajetBJet.p4());
  double dRMax   = ROOT::Math::VectorUtil::DeltaR(output.fDijetWithMaxDR_p4, output.fTetrajetBJet.p4());
  double dPhiMin = std::abs(ROOT::Math::VectorUtil::DeltaPhi(output.fDijetWithMinDR_p4, output.fTetrajetBJet.p4() ));
  double dPhiMax = std::abs(ROOT::Math::VectorUtil::DeltaPhi(output.fDijetWithMaxDR_p4, output.fTetrajetBJet.p4() ));
  hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DPhiVsDPhi_Before->Fill(dPhiMin, dPhiMax); 
  hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DRVsDR_Before->Fill(dRMin, dRMax);

  hTrijet1MassVsChiSqr_Before->Fill( output.fTrijet1_p4.mass(), output.fChiSqr );
  hTrijet2MassVsChiSqr_Before->Fill( output.fTrijet2_p4.mass(), output.fChiSqr );
  hTrijet1DijetPtVsDijetDR_Before->Fill( output.fTrijet1Dijet_p4.pt(), ROOT::Math::VectorUtil::DeltaR(output.fTrijet1Jet1.p4(), output.fTrijet1Jet2.p4() ) );
  hTrijet2DijetPtVsDijetDR_Before->Fill( output.fTrijet2Dijet_p4.pt(), ROOT::Math::VectorUtil::DeltaR(output.fTrijet2Jet1.p4(), output.fTrijet2Jet2.p4() ) );

  // Apply cuts
  if ( !cfg_ChiSqrCut.passedCut(output.fChiSqr) ) return output;
  cSubPassedChiSqCut.increment();


  // Fill Histograms (After cuts)
  hChiSqr_After->Fill( output.fChiSqr );
  hNJetsUsedAsBJetsInFit_After->Fill( output.fJetsUsedAsBJetsInFit.size() - nSelectedBJets );
  hNumberOfFits_After->Fill( output.fNumberOfFits );
  hTrijet1Mass_After->Fill( output.fTrijet1_p4.mass() );
  hTrijet2Mass_After->Fill( output.fTrijet2_p4.mass() );
  hTrijet1Pt_After->Fill( output.fTrijet1_p4.pt() );
  hTrijet2Pt_After->Fill( output.fTrijet2_p4.pt() );
  hTrijet1DijetMass_After->Fill( output.fTrijet1Dijet_p4.mass() );
  hTrijet2DijetMass_After->Fill( output.fTrijet2Dijet_p4.mass() );
  hTrijet1DijetPt_After->Fill( output.fTrijet1Dijet_p4.pt() );
  hTrijet2DijetPt_After->Fill( output.fTrijet2Dijet_p4.pt() );
  hTrijet1DijetDR_After  ->Fill( ROOT::Math::VectorUtil::DeltaR(output.fTrijet1Jet1.p4(), output.fTrijet1Jet2.p4() ) );
  hTrijet2DijetDR_After  ->Fill( ROOT::Math::VectorUtil::DeltaR(output.fTrijet1Jet2.p4(), output.fTrijet2Jet2.p4() ) );
  hTrijet1DijetDPhi_After->Fill( std::abs(ROOT::Math::VectorUtil::DeltaPhi(output.fTrijet1Jet1.p4(), output.fTrijet1Jet2.p4() ) ) );
  hTrijet2DijetDPhi_After->Fill( std::abs(ROOT::Math::VectorUtil::DeltaPhi(output.fTrijet2Jet1.p4(), output.fTrijet2Jet2.p4() ) ) );
  hTrijet1DijetDEta_After->Fill( std::abs(output.fTrijet1Jet1.p4().eta() - output.fTrijet1Jet2.p4().eta() ) );
  hTrijet2DijetDEta_After->Fill( std::abs(output.fTrijet2Jet1.p4().eta() - output.fTrijet2Jet2.p4().eta() ) );
  hTrijet1DijetBJetDEta_After->Fill( std::abs(output.fTrijet1Dijet_p4.eta() - output.fTrijet1BJet.p4().eta() ) );
  hTrijet2DijetBJetDEta_After->Fill( std::abs(output.fTrijet2Dijet_p4.eta() - output.fTrijet2BJet.p4().eta() ) );
  hTrijet1DijetBJetDPhi_After->Fill( std::abs(ROOT::Math::VectorUtil::DeltaPhi(output.fTrijet1Dijet_p4, output.fTrijet1BJet.p4() ) ) );
  hTrijet2DijetBJetDPhi_After->Fill( std::abs(ROOT::Math::VectorUtil::DeltaPhi(output.fTrijet2Dijet_p4, output.fTrijet2BJet.p4() ) ) );
  hTrijet1DijetBJetDR_After  ->Fill( ROOT::Math::VectorUtil::DeltaR(output.fTrijet1Dijet_p4, output.fTrijet1BJet.p4() ) );
  hTrijet2DijetBJetDR_After  ->Fill( ROOT::Math::VectorUtil::DeltaR(output.fTrijet2Dijet_p4, output.fTrijet2BJet.p4() ) );
  // Leading/Subleading tops
  if (output.fTrijet1_p4.pt() > output.fTrijet2_p4.pt()) 
    {
      // Leading
      hLdgTrijetPt_After        ->Fill(output.fTrijet1_p4.pt());
      hLdgTrijetMass_After      ->Fill(output.fTrijet1_p4.mass());
      hLdgTrijetJet1Pt_After    ->Fill(output.fTrijet1Jet1.pt());
      hLdgTrijetJet1Eta_After   ->Fill(output.fTrijet1Jet1.eta());
      hLdgTrijetJet1BDisc_After ->Fill(output.fTrijet1Jet1.bjetDiscriminator());
      hLdgTrijetJet2Pt_After    ->Fill(output.fTrijet1Jet2.pt());
      hLdgTrijetJet2Eta_After   ->Fill(output.fTrijet1Jet2.eta());
      hLdgTrijetJet2BDisc_After ->Fill(output.fTrijet1Jet2.bjetDiscriminator());
      hLdgTrijetBJetPt_After    ->Fill(output.fTrijet1BJet.pt());
      hLdgTrijetBJetEta_After   ->Fill(output.fTrijet1BJet.eta());
      hLdgTrijetBJetBDisc_After ->Fill(output.fTrijet1BJet.bjetDiscriminator());
      hLdgTrijetDiJetPt_After   ->Fill(output.fTrijet1Dijet_p4.pt());
      hLdgTrijetDiJetEta_After  ->Fill(output.fTrijet1Dijet_p4.eta());
      hLdgTrijetDiJetMass_After ->Fill(output.fTrijet1Dijet_p4.mass());
      // Subleading
      hSubldgTrijetJet1Pt_After    ->Fill(output.fTrijet2Jet1.pt());
      hSubldgTrijetJet1Eta_After   ->Fill(output.fTrijet2Jet1.eta());
      hSubldgTrijetJet1BDisc_After ->Fill(output.fTrijet2Jet1.bjetDiscriminator());
      hSubldgTrijetJet2Pt_After    ->Fill(output.fTrijet2Jet2.pt());
      hSubldgTrijetJet2Eta_After   ->Fill(output.fTrijet2Jet2.eta());
      hSubldgTrijetJet2BDisc_After ->Fill(output.fTrijet2Jet2.bjetDiscriminator());
      hSubldgTrijetBJetPt_After    ->Fill(output.fTrijet2BJet.pt());
      hSubldgTrijetBJetEta_After   ->Fill(output.fTrijet2BJet.eta());
      hSubldgTrijetBJetBDisc_After ->Fill(output.fTrijet2BJet.bjetDiscriminator());
      hSubldgTrijetDiJetPt_After   ->Fill(output.fTrijet2Dijet_p4.pt());
      hSubldgTrijetDiJetEta_After  ->Fill(output.fTrijet2Dijet_p4.eta());
      hSubldgTrijetDiJetMass_After ->Fill(output.fTrijet2Dijet_p4.mass());
    }
  else 
    {
      // Leading
      hLdgTrijetPt_After        ->Fill(output.fTrijet2_p4.pt());
      hLdgTrijetMass_After      ->Fill(output.fTrijet2_p4.mass());
      hLdgTrijetJet1Pt_After    ->Fill(output.fTrijet2Jet1.pt());
      hLdgTrijetJet1Eta_After   ->Fill(output.fTrijet2Jet1.eta());
      hLdgTrijetJet1BDisc_After ->Fill(output.fTrijet2Jet1.bjetDiscriminator());
      hLdgTrijetJet2Pt_After    ->Fill(output.fTrijet2Jet2.pt());
      hLdgTrijetJet2Eta_After   ->Fill(output.fTrijet2Jet2.eta());
      hLdgTrijetJet2BDisc_After ->Fill(output.fTrijet2Jet2.bjetDiscriminator());
      hLdgTrijetBJetPt_After    ->Fill(output.fTrijet2BJet.pt());
      hLdgTrijetBJetEta_After   ->Fill(output.fTrijet2BJet.eta());
      hLdgTrijetBJetBDisc_After ->Fill(output.fTrijet2BJet.bjetDiscriminator());
      hLdgTrijetDiJetPt_After   ->Fill(output.fTrijet2Dijet_p4.pt());
      hLdgTrijetDiJetEta_After  ->Fill(output.fTrijet2Dijet_p4.eta());
      hLdgTrijetDiJetMass_After ->Fill(output.fTrijet2Dijet_p4.mass());
      // Subleading
      hSubldgTrijetPt_After        ->Fill(output.fTrijet1_p4.pt());
      hSubldgTrijetMass_After      ->Fill(output.fTrijet1_p4.mass());
      hSubldgTrijetJet1Pt_After    ->Fill(output.fTrijet1Jet1.pt());
      hSubldgTrijetJet1Eta_After   ->Fill(output.fTrijet1Jet1.eta());
      hSubldgTrijetJet1BDisc_After ->Fill(output.fTrijet1Jet1.bjetDiscriminator());
      hSubldgTrijetJet2Pt_After    ->Fill(output.fTrijet1Jet2.pt());
      hSubldgTrijetJet2Eta_After   ->Fill(output.fTrijet1Jet2.eta());
      hSubldgTrijetJet2BDisc_After ->Fill(output.fTrijet1Jet2.bjetDiscriminator());
      hSubldgTrijetBJetPt_After    ->Fill(output.fTrijet1BJet.pt());
      hSubldgTrijetBJetEta_After   ->Fill(output.fTrijet1BJet.eta());
      hSubldgTrijetBJetBDisc_After ->Fill(output.fTrijet1BJet.bjetDiscriminator());
      hSubldgTrijetDiJetPt_After   ->Fill(output.fTrijet1Dijet_p4.pt());
      hSubldgTrijetDiJetEta_After  ->Fill(output.fTrijet1Dijet_p4.eta());
      hSubldgTrijetDiJetMass_After ->Fill(output.fTrijet1Dijet_p4.mass());
    }

  // Tetrajet
  hTetrajetBJetPt_After    ->Fill(output.fTetrajetBJet.pt());
  hTetrajetBJetEta_After   ->Fill(output.fTetrajetBJet.eta());
  hTetrajetBJetBDisc_After ->Fill(output.fTetrajetBJet.bjetDiscriminator());
  hTetrajet1Pt_After       ->Fill(output.fTetrajet1_p4.pt());
  hTetrajet1Mass_After     ->Fill(output.fTetrajet1_p4.mass());
  hTetrajet1Eta_After      ->Fill(output.fTetrajet1_p4.eta());
  hTetrajet2Pt_After       ->Fill(output.fTetrajet2_p4.pt());
  hTetrajet2Mass_After     ->Fill(output.fTetrajet2_p4.mass());
  hTetrajet2Eta_After      ->Fill(output.fTetrajet2_p4.eta());
  hLdgTetrajetPt_After     ->Fill(output.fLdgTetrajet_p4.pt());
  hLdgTetrajetMass_After   ->Fill(output.fLdgTetrajet_p4.mass());
  hLdgTetrajetEta_After    ->Fill(output.fLdgTetrajet_p4.eta());
  hSubldgTetrajetPt_After  ->Fill(output.fSubldgTetrajet_p4.pt());
  hSubldgTetrajetMass_After->Fill(output.fSubldgTetrajet_p4.mass());
  hSubldgTetrajetEta_After ->Fill(output.fSubldgTetrajet_p4.eta());

  // 2-D histos
  hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DPhiVsDPhi_After->Fill(dPhiMin, dPhiMax);
  hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DRVsDR_After->Fill(dRMin, dRMax);
  hTrijet1MassVsChiSqr_After->Fill( output.fTrijet1_p4.mass(), output.fChiSqr );
  hTrijet2MassVsChiSqr_After->Fill( output.fTrijet2_p4.mass(), output.fChiSqr );
  hTrijet1DijetPtVsDijetDR_After->Fill( output.fTrijet1Dijet_p4.pt(), ROOT::Math::VectorUtil::DeltaR(output.fTrijet1Jet1.p4(), output.fTrijet1Jet2.p4() ) );
  hTrijet2DijetPtVsDijetDR_After->Fill( output.fTrijet2Dijet_p4.pt(), ROOT::Math::VectorUtil::DeltaR(output.fTrijet2Jet1.p4(), output.fTrijet2Jet2.p4() ) );

  // Passed all top selection cuts
  output.bPassedSelection = true;
  cPassedTopSelection.increment();
  
  // Return data object
  return output;

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


const std::vector<Jet> TopSelection::GetBjetsToBeUsedInFit(const BJetSelection::Data& bjetData, const unsigned int maxNumberOfBJets)
{
  // If there are some bjets use them
  std::vector<Jet> bjetsForFit = bjetData.getSelectedBJets();

  // Append the vector of all failed bjets (in descending B-discriminator value) to the end of the bjets vector
  bjetsForFit.insert(bjetsForFit.end(), bjetData.getFailedBJetCandsDescendingDiscr().begin(), bjetData.getFailedBJetCandsDescendingDiscr().end()); 

  // Now truncate the bjets vector 
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

  // std::cout << "jets.size() = " << jets.size() << ", bjets.size() = " << bjets.size() << std::endl;

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
      unsigned int combinations = 0;
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

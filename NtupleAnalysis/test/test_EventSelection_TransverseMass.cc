// -*- c++ -*-
#include "catch.hpp"

#include "EventSelection/interface/TauSelection.h"
#include "EventSelection/interface/METSelection.h"
#include "EventSelection/interface/TransverseMass.h"
#include "Framework/interface/EventWeight.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/BranchManager.h"
#include "DataFormat/interface/Event.h"

#include "test_createTree.h"

TEST_CASE("TransverseMass", "[EventSelection]") {
  // Create config for testing
  boost::property_tree::ptree tmp = getMinimalConfig();
  tmp.put("TauSelection.applyTriggerMatching", false);
  tmp.put("TauSelection.triggerMatchingCone", 0.1);
  tmp.put("TauSelection.tauPtCut", 41.0);
  tmp.put("TauSelection.tauEtaCut", 2.1);
  tmp.put("TauSelection.tauLdgTrkPtCut", 10.0);
  tmp.put("TauSelection.prongs", 1);
  tmp.put("TauSelection.rtau", -10.0);
  tmp.put("TauSelection.invertTauIsolation", false);
  tmp.put("TauSelection.againstElectronDiscr", "againstElectronLooseMVA5");
  tmp.put("TauSelection.againstMuonDiscr", "againstMuonTight3");
  tmp.put("TauSelection.isolationDiscr", "byLooseCombinedIsolationDeltaBetaCorr3Hits");
  tmp.put("METSelection.METCutValue", 80.0);
  tmp.put("METSelection.METCutDirection", ">");
  tmp.put("METSelection.METSignificanceCutValue", 0);
  tmp.put("METSelection.METSignificanceCutDirection", ">");
  tmp.put("METSelection.METType", "MET_Type1");
  tmp.put("METSelection.applyPhiCorrections", false);
  ParameterSet pset(tmp, true, true);
  // Create necessary objects for testing
  TDirectory* f = getDirectory("test_TransverseMass");
  CommonPlots* commonPlotsPointer = 0;
  EventWeight weight;
  HistoWrapper histoWrapper(weight, "Debug");
  EventCounter ec(weight);
  TauSelection tausel(pset.getParameter<ParameterSet>("TauSelection"),
                    ec, histoWrapper, commonPlotsPointer, "default");
  METSelection metsel(pset.getParameter<ParameterSet>("METSelection"),
                      ec, histoWrapper, commonPlotsPointer, "test");
  tausel.bookHistograms(f);
  metsel.bookHistograms(f);

  // Setup events for testing
  auto tree = new TTree("Events", "Events");
  unsigned int run;           tree->Branch("run",   &run);
  unsigned int lumi;          tree->Branch("lumi",  &lumi);
  unsigned long long nevent;  tree->Branch("event", &nevent);
  std::vector<float> pt;   tree->Branch("Taus_pt", &pt);
  std::vector<float> eta;  tree->Branch("Taus_eta", &eta);
  std::vector<float> phi;  tree->Branch("Taus_phi", &phi);
  std::vector<float> e;    tree->Branch("Taus_e", &e);
  std::vector<float> mcpt;   tree->Branch("Taus_pt_MCVisibleTau", &mcpt);
  std::vector<float> mceta;  tree->Branch("Taus_eta_MCVisibleTau", &mceta);
  std::vector<float> mcphi;  tree->Branch("Taus_phi_MCVisibleTau", &mcphi);
  std::vector<float> mce;    tree->Branch("Taus_e_MCVisibleTau", &mce);
  std::vector<short> mcPdgId;    tree->Branch("Taus_pdgId", &mcPdgId);
  std::vector<short> pdgOrigin;    tree->Branch("Taus_pdgOrigin", &pdgOrigin);
  std::vector<float> lTrkPt;   tree->Branch("Taus_lChTrkPt", &lTrkPt);
  std::vector<float> lTrkEta;   tree->Branch("Taus_lChTrkEta", &lTrkEta);
  std::vector<int> decayMode;    tree->Branch("Taus_decayMode", &decayMode);
  std::vector<short> nProngs;    tree->Branch("Taus_nProngs", &nProngs);
  std::vector<short> mcProngs;    tree->Branch("Taus_mcNProngs", &mcProngs);
  std::vector<bool> eDiscr;    tree->Branch("Taus_againstElectronLooseMVA5", &eDiscr);
  std::vector<bool> muDiscr;   tree->Branch("Taus_againstMuonTight3", &muDiscr);
  std::vector<bool> isolDiscr; tree->Branch("Taus_byLooseCombinedIsolationDeltaBetaCorr3Hits", &isolDiscr);
  std::vector<bool> dm;        tree->Branch("Taus_decayModeFinding", &dm);
  std::vector<float> trgpt;   tree->Branch("HLTTau_pt", &trgpt);
  std::vector<float> trgeta;  tree->Branch("HLTTau_eta", &trgeta);
  std::vector<float> trgphi;  tree->Branch("HLTTau_phi", &trgphi);
  std::vector<float> trge;    tree->Branch("HLTTau_e", &trge);
  double type1METx;          tree->Branch("MET_Type1_x", &type1METx);
  double type1METy;         tree->Branch("MET_Type1_y", &type1METy);
  double type1METsignif;      tree->Branch("MET_Type1_significance", &type1METsignif);
  short nPU;                    tree->Branch("nGoodOfflineVertices", &nPU);

  run = 1;
  lumi = 1;
  nevent = 1; // no taus
  dm  = std::vector<bool>{true, true, true, true, true, true, true, true};
  eDiscr = std::vector<bool>{true, true, true, true, true, true, true, true};
  muDiscr = std::vector<bool>{true, true, true, true, true, true, true, true};
  isolDiscr = std::vector<bool>{true, true, true, true, true, true, true, true};
  pt  = std::vector<float>{50.f,  20.f,  11.f,  51.f,  75.f,  11.f,  13.f, 90.f};
  eta = std::vector<float>{-2.3f, -2.3f, -1.1f, -1.4f,  0.2f,  0.7f, 3.3f,  3.3f};
  phi = std::vector<float>{-2.9f, -0.5f,  1.f,  -2.3f, -1.7f,  0.3f, 0.8f,  1.1f};
  e   = std::vector<float>{50.f,  20.f,  11.f,  50.f,  75.f,  11.f,  13.f, 90.f};
  mcpt  = std::vector<float>{50.f,  20.f,  11.f,  51.f,  75.f,  11.f,  13.f, 90.f};
  mceta = std::vector<float>{-2.3f, -2.3f, -1.1f, -1.4f,  0.2f,  0.7f, 3.3f,  3.3f};
  mcphi = std::vector<float>{-2.9f, -0.5f,  1.f,  -2.3f, -1.7f,  0.3f, 0.8f,  1.1f};
  mce   = std::vector<float>{50.f,  20.f,  11.f,  50.f,  75.f,  11.f,  13.f, 90.f};
  mcPdgId = std::vector<short>{15,    15,    15,    15,    15,    15,    15,   15};
  pdgOrigin = std::vector<short>{0, 0, 0, 0, 0, 0, 0, 0};
  lTrkPt = std::vector<float>{5.f,  20.f,  11.f,  5.f,  70.f,  11.f,  13.f, 90.f};
  lTrkEta = std::vector<float>{-2.3f, -2.3f, -1.1f, -1.4f, 0.23f, 0.7f, 3.3f, 3.3f};
  decayMode = std::vector<int>{1, 1, 1, 1, 1, 1, 1, 1};
  nProngs = std::vector<short>{1,1,1,1,1,1,1,1};
  mcProngs = std::vector<short>{1,1,1,1,1,1,1,1};
  type1METx = 32.61220;
  type1METy = 83.883512;
  type1METsignif = 10.0;
  nPU = 1;
  tree->Fill();
  nevent = 2; // fail btag discriminator
  type1METx = 91.78106;
  type1METy = -77.30612;
  tree->Fill();
  
  BranchManager mgr;
  mgr.setTree(tree);
  Event event(pset);
  event.setupBranches(mgr);

  SECTION("Algorithm") {
    mgr.setEntry(0);
    TauSelection::Data tauData = tausel.analyze(event);
    METSelection::Data metData = metsel.analyze(event, event.vertexInfo().value());
    REQUIRE( tauData.getSelectedTaus().size() > 0 );
    REQUIRE( metData.passedSelection() == true );
    REQUIRE_NOTHROW( TransverseMass::reconstruct(tauData.getSelectedTau(), metData.getMET()) );
    double m = TransverseMass::reconstruct(tauData.getSelectedTau(), metData.getMET());
    CHECK( m == Approx(163.119) );
    mgr.setEntry(1);
    tauData = tausel.analyze(event);
    metData = metsel.analyze(event, event.vertexInfo().value());
    REQUIRE( tauData.getSelectedTaus().size() > 0 );
    REQUIRE( metData.passedSelection() == true );
    REQUIRE_NOTHROW( TransverseMass::reconstruct(tauData.getSelectedTau(), metData.getMET()) );
    m = TransverseMass::reconstruct(tauData.getSelectedTau(), metData.getMET());
    CHECK( m == Approx(90.965) );
  }
}

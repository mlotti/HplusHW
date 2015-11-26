// -*- c++ -*-
#include "catch.hpp"

#include "EventSelection/interface/AngularCuts.h"
#include "EventSelection/interface/TauSelection.h"
#include "EventSelection/interface/JetSelection.h"
#include "EventSelection/interface/METSelection.h"
#include "Framework/interface/Exception.h"
#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/EventWeight.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/BranchManager.h"
#include "DataFormat/interface/Event.h"

#include "test_createTree.h"

#include <string>
#include <sstream>
#include <iostream>
#include "TFile.h"
#include "TTree.h"

TEST_CASE("AngularCuts", "[EventSelection]") {
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
  tmp.put("JetSelection.jetPtCut", 30.0);
  tmp.put("JetSelection.jetEtaCut", 2.5);
  tmp.put("JetSelection.tauMatchingDeltaR", 0.5);
  tmp.put("JetSelection.numberOfJetsCutValue", 0);
  tmp.put("JetSelection.numberOfJetsCutDirection", "GEQ");
  //tmp.put("JetSelection.jetIDDiscr", "FIXME"); // FIXME
  tmp.put("JetSelection.jetPUIDDiscr", "PUIDloose");
  tmp.put("METSelection.METCutValue", 80.0);
  tmp.put("METSelection.METCutDirection", ">");
  tmp.put("METSelection.METType", "MET_Type1");
  tmp.put("METSelection.applyPhiCorrections", false);
  tmp.put("METSelection.METSignificanceCutValue", 0);
  tmp.put("METSelection.METSignificanceCutDirection", ">");
  tmp.put("AngularCutsCollinear.nConsideredJets", 3);
  tmp.put("AngularCutsCollinear.cutValueJet1", 40.0);
  tmp.put("AngularCutsCollinear.cutValueJet2", 40.0);
  tmp.put("AngularCutsCollinear.enableOptimizationPlots", true);
  tmp.put("AngularCutsBackToBack.nConsideredJets", 3);
  tmp.put("AngularCutsBackToBack.cutValueJet1", 50.0);
  tmp.put("AngularCutsBackToBack.cutValueJet2", 50.0);
  tmp.put("AngularCutsBackToBack.enableOptimizationPlots", true);
  
  // Create necessary objects for testing
  TDirectory* f = getDirectory("test_AngularCuts");
  CommonPlots* commonPlotsPointer = 0;
  EventWeight weight;
  HistoWrapper histoWrapper(weight, "Debug");
  EventCounter ec(weight);
  // Setup events for testing
  auto tree = new TTree("Events", "Events");
  unsigned int run;           tree->Branch("run",   &run);
  unsigned int lumi;          tree->Branch("lumi",  &lumi);
  unsigned long long nevent;  tree->Branch("event", &nevent);
  // Jet
  std::vector<float> jetpt;   tree->Branch("Jets_pt", &jetpt);
  std::vector<float> jeteta;  tree->Branch("Jets_eta", &jeteta);
  std::vector<float> jetphi;  tree->Branch("Jets_phi", &jetphi);
  std::vector<float> jete;    tree->Branch("Jets_e", &jete);
  std::vector<bool> jetID;    tree->Branch("Jets_IDtight", &jetID);
  std::vector<bool> jetPUID;  tree->Branch("Jets_PUIDloose", &jetPUID);
  // Tau
  std::vector<float> pt;   tree->Branch("Taus_pt", &pt);
  std::vector<float> eta;  tree->Branch("Taus_eta", &eta);
  std::vector<float> phi;  tree->Branch("Taus_phi", &phi);
  std::vector<float> e;    tree->Branch("Taus_e", &e);
  std::vector<float> mcpt;   tree->Branch("Taus_pt_MCVisibleTau", &mcpt);
  std::vector<float> mceta;  tree->Branch("Taus_eta_MCVisibleTau", &mceta);
  std::vector<float> mcphi;  tree->Branch("Taus_phi_MCVisibleTau", &mcphi);
  std::vector<float> mce;    tree->Branch("Taus_e_MCVisibleTau", &mce);
  std::vector<short> mcPdgId;    tree->Branch("Taus_pdgId", &mcPdgId);
  std::vector<float> lTrkPt;   tree->Branch("Taus_lChTrkPt", &lTrkPt);
  std::vector<float> lTrkEta;   tree->Branch("Taus_lChTrkEta", &lTrkEta);
  std::vector<int> decayMode;    tree->Branch("Taus_decayMode", &decayMode);
  std::vector<bool> eDiscr;    tree->Branch("Taus_againstElectronLooseMVA5", &eDiscr);
  std::vector<bool> muDiscr;   tree->Branch("Taus_againstMuonTight3", &muDiscr);
  std::vector<bool> isolDiscr; tree->Branch("Taus_byLooseCombinedIsolationDeltaBetaCorr3Hits", &isolDiscr);
  std::vector<bool> dm;        tree->Branch("Taus_decayModeFinding", &dm);
  std::vector<float> trgpt;   tree->Branch("HLTTau_pt", &trgpt);
  std::vector<float> trgeta;  tree->Branch("HLTTau_eta", &trgeta);
  std::vector<float> trgphi;  tree->Branch("HLTTau_phi", &trgphi);
  std::vector<float> trge;    tree->Branch("HLTTau_e", &trge);
  // MET
  double type1METx;           tree->Branch("MET_Type1_x", &type1METx);
  double type1METy;           tree->Branch("MET_Type1_y", &type1METy);
  double type1METsignif;      tree->Branch("MET_Type1_significance", &type1METsignif);
  // Vertices
  run = 1;
  lumi = 1;
  nevent = 1; // 1 jet outside tau
  dm  = std::vector<bool>{true};
  eDiscr = std::vector<bool>{true};
  muDiscr = std::vector<bool>{true};
  isolDiscr = std::vector<bool>{true};
  pt  = std::vector<float>{50.f};
  eta = std::vector<float>{1.2f};
  phi = std::vector<float>{-2.9f};
  e   = std::vector<float>{50.f};
  mcpt  = std::vector<float>{50.f,  20.f,  11.f,  51.f,  75.f,  11.f,  13.f, 90.f};
  mceta = std::vector<float>{-2.3f, -2.3f, -1.1f, -1.4f,  0.2f,  0.7f, 3.3f,  3.3f};
  mcphi = std::vector<float>{-2.9f, -0.5f,  1.f,  -2.3f, -1.7f,  0.3f, 0.8f,  1.1f};
  mce   = std::vector<float>{50.f,  20.f,  11.f,  50.f,  75.f,  11.f,  13.f, 90.f};
  mcPdgId = std::vector<short>{15,    15,    15,    15,    15,    15,    15,   15};
  lTrkPt = std::vector<float>{50.f};
  lTrkEta = std::vector<float>{1.21f};
  decayMode = std::vector<int>{1};
  trgpt  = std::vector<float>{51.f};
  trgeta = std::vector<float>{1.2f};
  trgphi = std::vector<float>{-2.93f};
  trge   = std::vector<float>{51.f};
  jetpt  = std::vector<float>{40.f,  60.f};
  jeteta = std::vector<float>{1.24f, 0.34f};
  jetphi = std::vector<float>{-2.92f, -0.51f};
  jete   = std::vector<float>{40.f,  60.f};
  jetID  = std::vector<bool>{true, true};
  jetPUID = std::vector<bool>{true, true};
  type1METx = 32.61220;
  type1METy = 83.88352; // collinear with tau
  tree->Fill();
  nevent = 2; // 4 jets outside tau, MET not collinear with tau or jet
  jetpt  = std::vector<float>{40.f,  60.f,   130.f,  80.f,  34.f};
  jeteta = std::vector<float>{1.24f, 0.34f,   2.1f, -1.2f,  1.6f};
  jetphi = std::vector<float>{-2.92f, 0.51f,  1.2f,  0.2f,  -2.3f};
  jete   = std::vector<float>{40.f,  60.f,   130.f,  80.f,  34.f};
  jetID  = std::vector<bool>{true, true, true, true, true};
  jetPUID = std::vector<bool>{true, true, true, true, true};
  tree->Fill(); // 4 jets outside tau, MET collinear with jet 2
  nevent = 3;
  type1METx = -87.38623;
  type1METy = -21.53244;
  tree->Fill();// 4 jets outside tau, MET collinear with tau
  nevent = 4;
  type1METx = 39.8002;
  type1METy = 3.99334;
  type1METsignif = 10.0;
  tree->Fill();  
  BranchManager mgr;
  mgr.setTree(tree);
  Event event(ParameterSet(tmp, true, true));
  event.setupBranches(mgr);
  
  SECTION("config") {
    ParameterSet pset1(tmp, true, true);
    // Check effect of nConsideredJets
    REQUIRE_THROWS_AS( AngularCutsCollinear p(pset1.getParameter<ParameterSet>("AngularCutsCollinear"),
                                           ec, histoWrapper, commonPlotsPointer, "test"), hplus::Exception );
    REQUIRE_THROWS_AS( AngularCutsBackToBack p(pset1.getParameter<ParameterSet>("AngularCutsBackToBack"),
                                           ec, histoWrapper, commonPlotsPointer, "test"), hplus::Exception );
    tmp.put("AngularCutsCollinear.cutValueJet3", 40.0);
    tmp.put("AngularCutsBackToBack.cutValueJet3", 50.0);
    ParameterSet pset2(tmp, true, true);
    REQUIRE_NOTHROW( AngularCutsCollinear p(pset2.getParameter<ParameterSet>("AngularCutsCollinear"),
                                           ec, histoWrapper, commonPlotsPointer, "test") );
    REQUIRE_NOTHROW( AngularCutsBackToBack p(pset2.getParameter<ParameterSet>("AngularCutsBackToBack"),
                                           ec, histoWrapper, commonPlotsPointer, "test") );
    // All params exist
    tmp.put("AngularCutsCollinear.cutValueJet4", 40.0);
    tmp.put("AngularCutsBackToBack.cutValueJet4", 50.0);
    ParameterSet pset3(tmp, true, true);
    REQUIRE_NOTHROW( AngularCutsCollinear p(pset3.getParameter<ParameterSet>("AngularCutsCollinear"),
                                           ec, histoWrapper, commonPlotsPointer, "test") );
    REQUIRE_NOTHROW( AngularCutsBackToBack p(pset3.getParameter<ParameterSet>("AngularCutsBackToBack"),
                                           ec, histoWrapper, commonPlotsPointer, "test") );
  }
  tmp.put("AngularCutsCollinear.cutValueJet3", 40.0);
  tmp.put("AngularCutsBackToBack.cutValueJet3", 50.0);
  tmp.put("AngularCutsCollinear.cutValueJet4", 40.0);
  tmp.put("AngularCutsBackToBack.cutValueJet4", 50.0);
  ParameterSet psetdefault(tmp, true, true);
  
  SECTION("Collinear angular cuts") {
    TauSelection tausel(psetdefault.getParameter<ParameterSet>("TauSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    JetSelection jetsel(psetdefault.getParameter<ParameterSet>("JetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    METSelection metsel(psetdefault.getParameter<ParameterSet>("METSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    AngularCutsCollinear collsel(psetdefault.getParameter<ParameterSet>("AngularCutsCollinear"),
                        ec, histoWrapper, commonPlotsPointer, "");
    tausel.bookHistograms(f);
    jetsel.bookHistograms(f);
    metsel.bookHistograms(f);
    collsel.bookHistograms(f);
    mgr.setEntry(0);
    TauSelection::Data tauData = tausel.silentAnalyze(event);
    JetSelection::Data jetData = jetsel.silentAnalyze(event, tauData.getSelectedTau());
    METSelection::Data metData = metsel.silentAnalyze(event, 1);
    AngularCutsCollinear::Data collData = collsel.silentAnalyze(event, tauData.getSelectedTau(), jetData, metData);
    // Delta phi (tau, MET)
    CHECK( collData.getDeltaPhiTauMET() == Approx(125.0873) );
    // Values of first event
    REQUIRE( tauData.hasIdentifiedTaus() == 1 );
    REQUIRE( jetData.getNumberOfSelectedJets() == 1 );
    CHECK( collData.passedSelection() == true );
    for (size_t i = 0; i < 4; ++i) {
      CHECK( collData.passedSelectionOnJet(i) == true );
    }
    CHECK( collData.getDeltaPhiJetMET(0) == Approx(97.9757832536) );
    CHECK( collData.get1DCutVariable(0) == Approx(149.58210) );
    CHECK( collData.getMinimumCutValue() == Approx(149.58210) );
    for (size_t i = 1; i < 4; ++i) {
      CHECK( collData.getDeltaPhiJetMET(i) == -1.0 );
      CHECK( collData.get1DCutVariable(i) == -1.0 );
    }
    // Access items outside vector
    REQUIRE_NOTHROW ( collData.passedSelectionOnJet(4) );
    REQUIRE_NOTHROW ( collData.getDeltaPhiJetMET(4) );
    REQUIRE_NOTHROW ( collData.get1DCutVariable(4) );
    // 4 jets MET not collinear with tau or jet
    mgr.setEntry(1);
    tauData = tausel.silentAnalyze(event);
    jetData = jetsel.silentAnalyze(event, tauData.getSelectedTau());
    metData = metsel.silentAnalyze(event, 1);
    collData = collsel.silentAnalyze(event, tauData.getSelectedTau(), jetData, metData);
    REQUIRE( tauData.hasIdentifiedTaus() == 1 );
    REQUIRE( jetData.getNumberOfSelectedJets() == 4 );
    CHECK( collData.passedSelection() == true );
    for (size_t i = 0; i < 4; ++i) {
      CHECK( collData.passedSelectionOnJet(i) == true );
    }
    // Detailed check on algebra
    CHECK( collData.getDeltaPhiTauMET() == Approx(125.0873) );
    CHECK( collData.getDeltaPhiJetMET(0) == Approx(0.0) );
    CHECK( collData.getDeltaPhiJetMET(1) == Approx(57.296) );
    CHECK( collData.getDeltaPhiJetMET(2) == Approx(39.534) );
    CHECK( collData.getDeltaPhiJetMET(3) == Approx(159.465) );
    CHECK( collData.get1DCutVariable(0) == Approx(219.196) );
    CHECK( collData.get1DCutVariable(1) == Approx(175.223) );
    CHECK( collData.get1DCutVariable(2) == Approx(188.089) );
    CHECK( collData.get1DCutVariable(3) == Approx(126.761) );
    CHECK( collData.getMinimumCutValue() == Approx(126.761) );
    // 4 jets outside tau, MET collinear with jet 2
    mgr.setEntry(2);
    tauData = tausel.silentAnalyze(event);
    jetData = jetsel.silentAnalyze(event, tauData.getSelectedTau());
    metData = metsel.silentAnalyze(event, 1);
    collData = collsel.silentAnalyze(event, tauData.getSelectedTau(), jetData, metData);
    REQUIRE( tauData.hasIdentifiedTaus() == 1 );
    REQUIRE( jetData.getNumberOfSelectedJets() == 4 );
    CHECK( collData.passedSelection() == false );
    CHECK( collData.getDeltaPhiTauMET() == Approx(0.0) );
    CHECK( collData.passedSelectionOnJet(0) == true );
    CHECK( collData.passedSelectionOnJet(1) == false );
    CHECK( collData.passedSelectionOnJet(2) == false );
    CHECK( collData.passedSelectionOnJet(3) == false );
    for (size_t i = 0; i < 4; ++i) {
      CHECK( collData.getDeltaPhiJetMET(i) > 0.0 );
      CHECK( collData.get1DCutVariable(i) > 0.0 );
    }
    // 4 jets outside tau, MET back-to-back with jet 2
    mgr.setEntry(3);
    tauData = tausel.silentAnalyze(event);
    jetData = jetsel.silentAnalyze(event, tauData.getSelectedTau());
    metData = metsel.silentAnalyze(event, 1);
    collData = collsel.silentAnalyze(event, tauData.getSelectedTau(), jetData, metData);
    REQUIRE( tauData.hasIdentifiedTaus() == 1 );
    REQUIRE( jetData.getNumberOfSelectedJets() == 4 );
    CHECK( collData.passedSelection() == true );
    CHECK( collData.getDeltaPhiTauMET() == Approx(171.887) );
    for (size_t i = 0; i < 4; ++i) {
      CHECK( collData.passedSelectionOnJet(i) == true );
      CHECK( collData.getDeltaPhiJetMET(i) > 0.0 );
      CHECK( collData.get1DCutVariable(i) > 0.0 );
    }
  }
  
  SECTION("Back-to-back angular cuts") {
    TauSelection tausel(psetdefault.getParameter<ParameterSet>("TauSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    JetSelection jetsel(psetdefault.getParameter<ParameterSet>("JetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    METSelection metsel(psetdefault.getParameter<ParameterSet>("METSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    AngularCutsBackToBack backtobacksel(psetdefault.getParameter<ParameterSet>("AngularCutsBackToBack"),
                        ec, histoWrapper, commonPlotsPointer, "");
    tausel.bookHistograms(f);
    jetsel.bookHistograms(f);
    metsel.bookHistograms(f);
    backtobacksel.bookHistograms(f);
    mgr.setEntry(0);
    TauSelection::Data tauData = tausel.silentAnalyze(event);
    JetSelection::Data jetData = jetsel.silentAnalyze(event, tauData.getSelectedTau());
    METSelection::Data metData = metsel.silentAnalyze(event, 1);
    AngularCutsBackToBack::Data backtobackData = backtobacksel.silentAnalyze(event, tauData.getSelectedTau(), jetData, metData);
    // Delta phi (tau, MET)
    CHECK( backtobackData.getDeltaPhiTauMET() == Approx(125.0873) );
    // Values of first event
    REQUIRE( tauData.hasIdentifiedTaus() == 1 );
    REQUIRE( jetData.getNumberOfSelectedJets() == 1 );
    CHECK( backtobackData.passedSelection() == true );
    for (size_t i = 0; i < 4; ++i) {
      CHECK( backtobackData.passedSelectionOnJet(i) == true );
    }
    CHECK( backtobackData.getDeltaPhiJetMET(0) == Approx(97.9757832536) );
    CHECK( backtobackData.get1DCutVariable(0) == Approx(112.315) );
    CHECK( backtobackData.getMinimumCutValue() == Approx(112.315) );
    for (size_t i = 1; i < 4; ++i) {
      CHECK( backtobackData.getDeltaPhiJetMET(i) == -1.0 );
      CHECK( backtobackData.get1DCutVariable(i) == -1.0 );
    }
    // Access items outside vector
    REQUIRE_NOTHROW ( backtobackData.passedSelectionOnJet(4) );
    REQUIRE_NOTHROW ( backtobackData.getDeltaPhiJetMET(4) );
    REQUIRE_NOTHROW ( backtobackData.get1DCutVariable(4) );
    // 4 jets MET not collinear with tau or jet
    mgr.setEntry(1);
    tauData = tausel.silentAnalyze(event);
    jetData = jetsel.silentAnalyze(event, tauData.getSelectedTau());
    metData = metsel.silentAnalyze(event, 1);
    backtobackData = backtobacksel.silentAnalyze(event, tauData.getSelectedTau(), jetData, metData);
    REQUIRE( tauData.hasIdentifiedTaus() == 1 );
    REQUIRE( jetData.getNumberOfSelectedJets() == 4 );
    CHECK( backtobackData.passedSelection() == true );
    for (size_t i = 0; i < 4; ++i) {
      CHECK( backtobackData.passedSelectionOnJet(i) == true );
    }
    // Detailed check on algebra
    CHECK( backtobackData.getDeltaPhiTauMET() == Approx(125.0873) );
    CHECK( backtobackData.getDeltaPhiJetMET(0) == Approx(0.0) );
    CHECK( backtobackData.getDeltaPhiJetMET(1) == Approx(57.296) );
    CHECK( backtobackData.getDeltaPhiJetMET(2) == Approx(39.534) );
    CHECK( backtobackData.getDeltaPhiJetMET(3) == Approx(159.465) );
    CHECK( backtobackData.get1DCutVariable(0) == Approx(54.913) );
    CHECK( backtobackData.get1DCutVariable(1) == Approx(79.362) );
    CHECK( backtobackData.get1DCutVariable(2) == Approx(67.664) );
    CHECK( backtobackData.get1DCutVariable(3) == Approx(168.655) );
    CHECK( backtobackData.getMinimumCutValue() == Approx(54.913) );
    // 4 jets outside tau, MET collinear with jet 2
    mgr.setEntry(2);
    tauData = tausel.silentAnalyze(event);
    jetData = jetsel.silentAnalyze(event, tauData.getSelectedTau());
    metData = metsel.silentAnalyze(event, 1);
    backtobackData = backtobacksel.silentAnalyze(event, tauData.getSelectedTau(), jetData, metData);
    REQUIRE( tauData.hasIdentifiedTaus() == 1 );
    REQUIRE( jetData.getNumberOfSelectedJets() == 4 );
    CHECK( backtobackData.passedSelection() == true );
    CHECK( backtobackData.getDeltaPhiTauMET() == Approx(0.0) );
    for (size_t i = 0; i < 4; ++i) {
      CHECK( backtobackData.passedSelectionOnJet(i) == true );
      CHECK( backtobackData.getDeltaPhiJetMET(i) > 0.0 );
      CHECK( backtobackData.get1DCutVariable(i) > 0.0 );
    }
    // 4 jets outside tau, MET back-to-back with jet 2
    mgr.setEntry(3);
    tauData = tausel.silentAnalyze(event);
    jetData = jetsel.silentAnalyze(event, tauData.getSelectedTau());
    metData = metsel.silentAnalyze(event, 1);
    backtobackData = backtobacksel.silentAnalyze(event, tauData.getSelectedTau(), jetData, metData);
    REQUIRE( tauData.hasIdentifiedTaus() == 1 );
    REQUIRE( jetData.getNumberOfSelectedJets() == 4 );
    CHECK( backtobackData.passedSelection() == false );
    CHECK( backtobackData.getDeltaPhiTauMET() == Approx(171.887) );
    CHECK( backtobackData.passedSelectionOnJet(0) == true );
    CHECK( backtobackData.passedSelectionOnJet(1) == false );
    CHECK( backtobackData.passedSelectionOnJet(2) == false );
    CHECK( backtobackData.passedSelectionOnJet(3) == false );
    for (size_t i = 0; i < 4; ++i) {
      CHECK( backtobackData.getDeltaPhiJetMET(i) > 0.0 );
      CHECK( backtobackData.get1DCutVariable(i) > 0.0 );
    }
  }  
    
    //for (size_t i = 0; i < 4; ++i) { std::cout << collData.get1DCutVariable(i) << std::endl; }
    
    
//     backtobacksel.bookHistograms(f);
//     AngularCutsBackToBack backtobacksel(psetdefault.getParameter<ParameterSet>("AngularCutsBackToBack"),
//                         ec, histoWrapper, commonPlotsPointer, "");
//     AngularCutsBackToBack::Data collData = backtobacksel.silentAnalyze(event, tauData, jetData, metData);
    
    

  SECTION("protection for double counting of events") {
    mgr.setEntry(0);
    TauSelection tausel(psetdefault.getParameter<ParameterSet>("TauSelection"),
                        ec, histoWrapper, commonPlotsPointer, "dblcount");
    JetSelection jetsel(psetdefault.getParameter<ParameterSet>("JetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "dblcount");
    METSelection metsel(psetdefault.getParameter<ParameterSet>("METSelection"),
                        ec, histoWrapper, commonPlotsPointer, "dblcount");
    AngularCutsCollinear collsel(psetdefault.getParameter<ParameterSet>("AngularCutsCollinear"),
                        ec, histoWrapper, commonPlotsPointer, "dblcount");
    AngularCutsBackToBack backtobacksel(psetdefault.getParameter<ParameterSet>("AngularCutsBackToBack"),
                         ec, histoWrapper, commonPlotsPointer, "dblcount");
    tausel.bookHistograms(f);
    jetsel.bookHistograms(f);
    metsel.bookHistograms(f);
    collsel.bookHistograms(f);
    backtobacksel.bookHistograms(f);
    mgr.setEntry(0);
    TauSelection::Data tauData = tausel.silentAnalyze(event);
    JetSelection::Data jetData = jetsel.silentAnalyze(event, tauData.getSelectedTau());
    METSelection::Data metData = metsel.silentAnalyze(event, 1);
    // Collinear
    CHECK( ec.getValueByName("passed angular cuts / Collinear (dblcount)") == 0);
    REQUIRE_NOTHROW( AngularCutsCollinear::Data collData = collsel.silentAnalyze(event, tauData.getSelectedTau(), jetData, metData) );
    CHECK( ec.getValueByName("passed angular cuts / Collinear (dblcount)") == 0);
    REQUIRE_NOTHROW( AngularCutsCollinear::Data collData = collsel.analyze(event, tauData.getSelectedTau(), jetData, metData) );
    CHECK( ec.getValueByName("passed angular cuts / Collinear (dblcount)") == 1);
    REQUIRE_THROWS_AS( AngularCutsCollinear::Data collData = collsel.analyze(event, tauData.getSelectedTau(), jetData, metData), hplus::Exception );
    REQUIRE_THROWS_AS( AngularCutsCollinear::Data collData = collsel.silentAnalyze(event, tauData.getSelectedTau(), jetData, metData), hplus::Exception );
    // Back to back
    CHECK( ec.getValueByName("passed angular cuts / BackToBack (dblcount)") == 0);
    REQUIRE_NOTHROW( AngularCutsBackToBack::Data bbData = backtobacksel.silentAnalyze(event, tauData.getSelectedTau(), jetData, metData) );
    CHECK( ec.getValueByName("passed angular cuts / BackToBack (dblcount)") == 0);
    REQUIRE_NOTHROW( AngularCutsBackToBack::Data bbData = backtobacksel.analyze(event, tauData.getSelectedTau(), jetData, metData) );
    CHECK( ec.getValueByName("passed angular cuts / BackToBack (dblcount)") == 1);
    REQUIRE_THROWS_AS( AngularCutsBackToBack::Data bbData = backtobacksel.analyze(event, tauData.getSelectedTau(), jetData, metData), hplus::Exception );
    REQUIRE_THROWS_AS( AngularCutsBackToBack::Data bbData = backtobacksel.silentAnalyze(event, tauData.getSelectedTau(), jetData, metData), hplus::Exception );  }
  ec.setOutput(f);
  ec.serialize();
  closeDirectory(f);
}
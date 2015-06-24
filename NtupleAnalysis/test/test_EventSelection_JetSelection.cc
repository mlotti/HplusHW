// -*- c++ -*-
#include "catch.hpp"

#include "EventSelection/interface/JetSelection.h"
#include "EventSelection/interface/TauSelection.h"
#include "Framework/interface/Exception.h"
#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/EventWeight.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/BranchManager.h"
#include "DataFormat/interface/Event.h"

#include "test_createTree.h"

#include <string>
#include <iostream>
#include "TFile.h"
#include "TTree.h"

TEST_CASE("JetSelection", "[EventSelection]") {
  SECTION("Default (empty) discriminators") {
    boost::property_tree::ptree tmp = getMinimalConfig();
    ParameterSet pset1(tmp, true);
    REQUIRE_NOTHROW(Event event1(pset1));
  }
  SECTION("JetIDDiscr validity") {
    boost::property_tree::ptree tmp = getMinimalConfig();
    tmp.put("JetSelection.jetIDDiscr", "");
    ParameterSet pset1(tmp, true);
    REQUIRE_NOTHROW(Event event1(pset1));
    //tmp.put("JetSelection.jetIDDiscr", "FIXME"); // FIXME
    //ParameterSet pset2(tmp, true);
    //REQUIRE_NOTHROW(Event event2(pset2));
    tmp.put("JetSelection.jetIDDiscr", "dummy");
    ParameterSet pset3(tmp, true);
    REQUIRE_THROWS_AS(Event event3(pset3), hplus::Exception);
  }
  SECTION("JetPUIDDiscr validity") {
    boost::property_tree::ptree tmp = getMinimalConfig();
    tmp.put("JetSelection.jetPUIDDiscr", "");
    ParameterSet pset1(tmp, true);
    REQUIRE_NOTHROW(Event event1(pset1));
    tmp.put("JetSelection.jetPUIDDiscr", "PUIDloose");
    ParameterSet pset2(tmp, true);
    REQUIRE_NOTHROW(Event event2(pset2));
    tmp.put("JetSelection.jetPUIDDiscr", "dummy");
    ParameterSet pset3(tmp, true);
    REQUIRE_THROWS_AS(Event event3(pset3), hplus::Exception);
  }

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
  tmp.put("TauSelection.againstElectronDiscr", "againstElectronTight");
  tmp.put("TauSelection.againstMuonDiscr", "againstMuonMedium");
  tmp.put("TauSelection.isolationDiscr", "byLooseCombinedIsolationDeltaBetaCorr3Hits");
  tmp.put("JetSelection.jetPtCut", 30.0);
  tmp.put("JetSelection.jetEtaCut", 2.5);
  tmp.put("JetSelection.tauMatchingDeltaR", 0.5);
  tmp.put("JetSelection.numberOfJetsCutValue", 3);
  tmp.put("JetSelection.numberOfJetsCutDirection", "GEQ");
  //tmp.put("JetSelection.jetIDDiscr", "FIXME"); // FIXME
  tmp.put("JetSelection.jetPUIDDiscr", "PUIDloose");
  ParameterSet psetDefault(tmp, true);
  // Create necessary objects for testing
  TFile* f = new TFile("test_JetSelection.root", "recreate");
  CommonPlots* commonPlotsPointer = 0;
  EventWeight weight;
  HistoWrapper histoWrapper(weight, "Debug");
  EventCounter ec(weight);
  JetSelection sel1(psetDefault.getParameter<ParameterSet>("JetSelection"),
                    ec, histoWrapper, commonPlotsPointer, "default");
  sel1.bookHistograms(f);
  
  // Setup events for testing
  auto tree = new TTree("Events", "Events");
  unsigned int run;           tree->Branch("run",   &run);
  unsigned int lumi;          tree->Branch("lumi",  &lumi);
  unsigned long long nevent;  tree->Branch("event", &nevent);
  std::vector<float> jetpt;   tree->Branch("Jets_pt", &jetpt);
  std::vector<float> jeteta;  tree->Branch("Jets_eta", &jeteta);
  std::vector<float> jetphi;  tree->Branch("Jets_phi", &jetphi);
  std::vector<float> jete;    tree->Branch("Jets_e", &jete);
  std::vector<bool> jetID;    tree->Branch("Jets_IDtight", &jetID);
  std::vector<bool> jetPUID;  tree->Branch("Jets_PUIDloose", &jetPUID);
  std::vector<float> pt;   tree->Branch("Taus_pt", &pt);
  std::vector<float> eta;  tree->Branch("Taus_eta", &eta);
  std::vector<float> phi;  tree->Branch("Taus_phi", &phi);
  std::vector<float> e;    tree->Branch("Taus_e", &e);
  std::vector<float> lTrkPt;   tree->Branch("Taus_lTrkPt", &lTrkPt);
  std::vector<float> lTrkEta;   tree->Branch("Taus_lTrkEta", &lTrkEta);
  std::vector<int> nProngs;    tree->Branch("Taus_nProngs", &nProngs);
  std::vector<bool> eDiscr;    tree->Branch("Taus_againstElectronTight", &eDiscr);
  std::vector<bool> muDiscr;   tree->Branch("Taus_againstMuonMedium", &muDiscr);
  std::vector<bool> isolDiscr; tree->Branch("Taus_byLooseCombinedIsolationDeltaBetaCorr3Hits", &isolDiscr);
  std::vector<bool> dm;        tree->Branch("Taus_decayModeFinding", &dm);
  std::vector<float> trgpt;   tree->Branch("HLTTau_pt", &trgpt);
  std::vector<float> trgeta;  tree->Branch("HLTTau_eta", &trgeta);
  std::vector<float> trgphi;  tree->Branch("HLTTau_phi", &trgphi);
  std::vector<float> trge;    tree->Branch("HLTTau_e", &trge);

  run = 1;
  lumi = 1;
  nevent = 1; // no taus
  jetpt  = std::vector<float>{40.f,  60.f,   130.f,  12.f,  24.f,  50.f,  70.f,  90.f};
  jeteta = std::vector<float>{-1.24f, 0.34f,   2.6f,  1.2f,  4.5f, -2.1f, -3.2f,  1.2f};
  jetphi = std::vector<float>{-2.92f, -0.51f,  1.2f, -2.1f,  0.1f, -1.9f,  0.1f,  3.0f};
  jete   = std::vector<float>{40.f,  60.f,   130.f,  12.f,  24.f,  50.f,  70.f,  90.f};
  jetID  = std::vector<bool>{true, true, true, true, true, true, true, true};
  jetPUID = std::vector<bool>{true, true, true, true, true, true, true, true};
  tree->Fill();
  nevent = 2; // with taus
  dm  = std::vector<bool>{true, true};
  eDiscr = std::vector<bool>{true, true};
  muDiscr = std::vector<bool>{true, true};
  isolDiscr = std::vector<bool>{true, true};
  pt  = std::vector<float>{50.f,  70.f};
  eta = std::vector<float>{-1.3f, 0.3f};
  phi = std::vector<float>{-2.9f, -0.5f};
  e   = std::vector<float>{50.f,  70.f};
  lTrkPt = std::vector<float>{50.f,  60.f};
  lTrkEta = std::vector<float>{-1.3f, 0.3f};
  nProngs = std::vector<int>{1, 1};
  tree->Fill();
  nevent = 3; // jet ID
  jetID  = std::vector<bool>{true, false, false, false, true, true, false, true};
  tree->Fill();
  nevent = 4; // against e
  jetID = std::vector<bool>{true, true, true, true, true, true, true, true};
  jetPUID  = std::vector<bool>{true, false, false, false, true, true, false, true};
  tree->Fill();
  
  BranchManager mgr;
  mgr.setTree(tree);
  Event event(psetDefault);
  //event.setupBranches(mgr);
  
  SECTION("jet ID discriminator") {
    tmp.put("JetSelection.jetPtCut", 0.0);
    tmp.put("JetSelection.jetEtaCut", 9.0);
    tmp.put("JetSelection.tauMatchingDeltaR", -1.0);
    tmp.put("JetSelection.numberOfJetsCutValue", 0);
    tmp.put("JetSelection.numberOfJetsCutDirection", "GEQ");
    ParameterSet newPset(tmp,true);
    TauSelection tausel(newPset.getParameter<ParameterSet>("TauSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    JetSelection jetsel(newPset.getParameter<ParameterSet>("JetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    tausel.bookHistograms(f);
    jetsel.bookHistograms(f);
    Event event2(newPset);
    event2.setupBranches(mgr);
    mgr.setEntry(1);
    TauSelection::Data tauData = tausel.silentAnalyze(event2);
    JetSelection::Data jetData = jetsel.silentAnalyze(event2, tauData);
    CHECK( jetData.passedSelection() == true );
    CHECK( jetData.getAllJets().size() == 8 );
    CHECK( jetData.getNumberOfSelectedJets() == 8 );
    mgr.setEntry(2);
    tauData = tausel.silentAnalyze(event2);
    jetData = jetsel.silentAnalyze(event2, tauData);
    CHECK( jetData.passedSelection() == true );
    CHECK( jetData.getAllJets().size() == 8 );
    //CHECK( jetData.getNumberOfSelectedJets() == 3 ); // FIXME 
  }
  SECTION("jet PU ID discriminator") {
    tmp.put("JetSelection.jetPtCut", 30.0);
    tmp.put("JetSelection.jetEtaCut", 9.0);
    tmp.put("JetSelection.tauMatchingDeltaR", -1.0);
    tmp.put("JetSelection.numberOfJetsCutValue", 0);
    tmp.put("JetSelection.numberOfJetsCutDirection", "GEQ");
    ParameterSet newPset(tmp,true);
    TauSelection tausel(newPset.getParameter<ParameterSet>("TauSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    JetSelection jetsel(newPset.getParameter<ParameterSet>("JetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    tausel.bookHistograms(f);
    jetsel.bookHistograms(f);
    Event event2(newPset);
    event2.setupBranches(mgr);
    mgr.setEntry(1);
    TauSelection::Data tauData = tausel.silentAnalyze(event2);
    JetSelection::Data jetData = jetsel.silentAnalyze(event2, tauData);
    CHECK( jetData.passedSelection() == true );
    CHECK( jetData.getAllJets().size() == 8 );
    CHECK( jetData.getNumberOfSelectedJets() == 6 );
    mgr.setEntry(3);
    tauData = tausel.silentAnalyze(event2);
    jetData = jetsel.silentAnalyze(event2, tauData);
    CHECK( jetData.passedSelection() == true );
    CHECK( jetData.getAllJets().size() == 4 );
    CHECK( jetData.getNumberOfSelectedJets() == 3 );
  }
  SECTION("jet to tau matching") {
    tmp.put("JetSelection.jetPtCut", 0.0);
    tmp.put("JetSelection.jetEtaCut", 9.0);
    tmp.put("JetSelection.tauMatchingDeltaR", 0.5);
    tmp.put("JetSelection.numberOfJetsCutValue", 0);
    tmp.put("JetSelection.numberOfJetsCutDirection", "GEQ");
    ParameterSet newPset(tmp,true);
    TauSelection tausel(newPset.getParameter<ParameterSet>("TauSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    JetSelection jetsel(newPset.getParameter<ParameterSet>("JetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    tausel.bookHistograms(f);
    jetsel.bookHistograms(f);
    Event event2(newPset);
    event2.setupBranches(mgr);
    mgr.setEntry(1);
    TauSelection::Data tauData = tausel.silentAnalyze(event2);
    JetSelection::Data jetData = jetsel.silentAnalyze(event2, tauData);
    CHECK( jetData.passedSelection() == true );
    CHECK( jetData.getAllJets().size() == 8 );
    CHECK( jetData.getNumberOfSelectedJets() == 7 );
    CHECK( jetData.jetMatchedToTauFound() == true );
    REQUIRE_NOTHROW( jetData.getJetMatchedToTau() );
    CHECK( jetData.getJetMatchedToTau().pt() == 60.0 );
    mgr.setEntry(0);
    tauData = tausel.silentAnalyze(event2);
    jetData = jetsel.silentAnalyze(event2, tauData);
    CHECK( jetData.getNumberOfSelectedJets() == 8 );
    CHECK( jetData.jetMatchedToTauFound() == false );
    REQUIRE_THROWS_AS( jetData.getJetMatchedToTau(), hplus::Exception );
  }
  SECTION("jet pt cut") {
    tmp.put("JetSelection.jetPtCut", 20.0);
    tmp.put("JetSelection.jetEtaCut", 9.0);
    tmp.put("JetSelection.tauMatchingDeltaR", -1.0);
    tmp.put("JetSelection.numberOfJetsCutValue", 0);
    tmp.put("JetSelection.numberOfJetsCutDirection", "GEQ");
    ParameterSet newPset(tmp,true);
    TauSelection tausel(newPset.getParameter<ParameterSet>("TauSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    JetSelection jetsel(newPset.getParameter<ParameterSet>("JetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    tausel.bookHistograms(f);
    jetsel.bookHistograms(f);
    Event event2(newPset);
    event2.setupBranches(mgr);
    mgr.setEntry(1);
    TauSelection::Data tauData = tausel.silentAnalyze(event2);
    JetSelection::Data jetData = jetsel.silentAnalyze(event2, tauData);
    CHECK( jetData.passedSelection() == true );
    CHECK( jetData.getAllJets().size() == 8 );
    CHECK( jetData.getNumberOfSelectedJets() == 7);
  }
  SECTION("jet eta cut") {
    tmp.put("JetSelection.jetPtCut", 0.0);
    tmp.put("JetSelection.jetEtaCut", 2.5);
    tmp.put("JetSelection.tauMatchingDeltaR", -1.0);
    tmp.put("JetSelection.numberOfJetsCutValue", 0);
    tmp.put("JetSelection.numberOfJetsCutDirection", "GEQ");
    ParameterSet newPset(tmp,true);
    TauSelection tausel(newPset.getParameter<ParameterSet>("TauSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    JetSelection jetsel(newPset.getParameter<ParameterSet>("JetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    tausel.bookHistograms(f);
    jetsel.bookHistograms(f);
    Event event2(newPset);
    event2.setupBranches(mgr);
    mgr.setEntry(1);
    TauSelection::Data tauData = tausel.silentAnalyze(event2);
    JetSelection::Data jetData = jetsel.silentAnalyze(event2, tauData);
    CHECK( jetData.passedSelection() == true );
    CHECK( jetData.getAllJets().size() == 8 );
    CHECK( jetData.getNumberOfSelectedJets() == 5);
  }
  SECTION("HT value") {
    tmp.put("JetSelection.jetPtCut", 30.0);
    tmp.put("JetSelection.jetEtaCut", 2.5);
    tmp.put("JetSelection.tauMatchingDeltaR", 0.5);
    tmp.put("JetSelection.numberOfJetsCutValue", 3);
    tmp.put("JetSelection.numberOfJetsCutDirection", "GEQ");
    ParameterSet newPset(tmp,true);
    TauSelection tausel(newPset.getParameter<ParameterSet>("TauSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    JetSelection jetsel(newPset.getParameter<ParameterSet>("JetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    tausel.bookHistograms(f);
    jetsel.bookHistograms(f);
    Event event2(newPset);
    event2.setupBranches(mgr);
    mgr.setEntry(1); // with tau
    TauSelection::Data tauData = tausel.silentAnalyze(event2);
    JetSelection::Data jetData = jetsel.silentAnalyze(event2, tauData);
    CHECK( jetData.getNumberOfSelectedJets() == 3);
    CHECK( jetData.HT() == 250.f );
    mgr.setEntry(0); // no tau
    tauData = tausel.silentAnalyze(event2);
    jetData = jetsel.silentAnalyze(event2, tauData);
    CHECK( jetData.getNumberOfSelectedJets() == 4);
    CHECK( jetData.HT() == 240.f );
  }
  SECTION("jet count 1") {
    tmp.put("JetSelection.jetPtCut", 30.0);
    tmp.put("JetSelection.jetEtaCut", 2.5);
    tmp.put("JetSelection.tauMatchingDeltaR", -1.0);
    tmp.put("JetSelection.numberOfJetsCutValue", 3);
    tmp.put("JetSelection.numberOfJetsCutDirection", "GEQ");
    ParameterSet newPset(tmp,true);
    TauSelection tausel(newPset.getParameter<ParameterSet>("TauSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    JetSelection jetsel(newPset.getParameter<ParameterSet>("JetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    tausel.bookHistograms(f);
    jetsel.bookHistograms(f);
    Event event2(newPset);
    event2.setupBranches(mgr);
    mgr.setEntry(1);
    TauSelection::Data tauData = tausel.silentAnalyze(event2);
    JetSelection::Data jetData = jetsel.silentAnalyze(event2, tauData);
    CHECK( jetData.passedSelection() == true );
  }
  SECTION("jet count 2") {
    tmp.put("JetSelection.jetPtCut", 30.0);
    tmp.put("JetSelection.jetEtaCut", 2.5);
    tmp.put("JetSelection.tauMatchingDeltaR", -1.0);
    tmp.put("JetSelection.numberOfJetsCutValue", 5);
    tmp.put("JetSelection.numberOfJetsCutDirection", "GEQ");
    ParameterSet newPset(tmp,true);
    TauSelection tausel(newPset.getParameter<ParameterSet>("TauSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    JetSelection jetsel(newPset.getParameter<ParameterSet>("JetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    tausel.bookHistograms(f);
    jetsel.bookHistograms(f);
    Event event2(newPset);
    event2.setupBranches(mgr);
    mgr.setEntry(1);
    TauSelection::Data tauData = tausel.silentAnalyze(event2);
    JetSelection::Data jetData = jetsel.silentAnalyze(event2, tauData);
    CHECK( jetData.passedSelection() == false );
  }
 SECTION("jet sorting by pt") {
    tmp.put("JetSelection.jetPtCut", 30.0);
    tmp.put("JetSelection.jetEtaCut", 2.5);
    tmp.put("JetSelection.tauMatchingDeltaR", -1.0);
    tmp.put("JetSelection.numberOfJetsCutValue", 3);
    tmp.put("JetSelection.numberOfJetsCutDirection", "GEQ");
    ParameterSet newPset(tmp,true);
    TauSelection tausel(newPset.getParameter<ParameterSet>("TauSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    JetSelection jetsel(newPset.getParameter<ParameterSet>("JetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    tausel.bookHistograms(f);
    jetsel.bookHistograms(f);
    Event event2(newPset);
    event2.setupBranches(mgr);
    mgr.setEntry(1);
    TauSelection::Data tauData = tausel.silentAnalyze(event2);
    JetSelection::Data jetData = jetsel.silentAnalyze(event2, tauData);
    CHECK( jetData.getNumberOfSelectedJets() == 4 );
    CHECK( jetData.getSelectedJets()[0].pt() == 90.0 );
    CHECK( jetData.getSelectedJets()[1].pt() == 60.0 );
    CHECK( jetData.getSelectedJets()[2].pt() == 50.0 );
    CHECK( jetData.getSelectedJets()[3].pt() == 40.0 );
  }
  SECTION("protection for double counting of events") {
    mgr.setEntry(0); 
    Event event2(psetDefault);
    event2.setupBranches(mgr);
    TauSelection tausel(psetDefault.getParameter<ParameterSet>("TauSelection"),
                        ec, histoWrapper, commonPlotsPointer, "dblcount");
    JetSelection jetsel(psetDefault.getParameter<ParameterSet>("JetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "dblcount");
    tausel.bookHistograms(f);
    jetsel.bookHistograms(f);
    TauSelection::Data tauData = tausel.silentAnalyze(event2);
    CHECK( ec.getValueByName("passed jet selection (dblcount)") == 0);
    REQUIRE_NOTHROW( jetsel.silentAnalyze(event2, tauData) );
    CHECK( ec.getValueByName("passed jet selection (dblcount)") == 0);
    REQUIRE_NOTHROW( jetsel.analyze(event2, tauData) );
    CHECK( ec.getValueByName("passed jet selection (dblcount)") == 1);
    REQUIRE_THROWS_AS( jetsel.analyze(event2, tauData), hplus::Exception );
    REQUIRE_THROWS_AS( jetsel.silentAnalyze(event2, tauData), hplus::Exception );
  }
  
  ec.setOutput(f);
  ec.serialize();
  f->Write();
  f->Close();
}
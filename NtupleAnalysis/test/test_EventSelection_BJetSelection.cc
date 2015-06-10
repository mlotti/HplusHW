// -*- c++ -*-
#include "catch.hpp"

#include "EventSelection/interface/BJetSelection.h"
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

TEST_CASE("BJetSelection", "[EventSelection]") {
  SECTION("Default (empty) discriminators") {
    boost::property_tree::ptree tmp = getMinimalConfig();
    ParameterSet pset1(tmp, true);
    REQUIRE_NOTHROW(Event event1(pset1));
  }
  SECTION("bjet discriminator validity") {
    boost::property_tree::ptree tmp = getMinimalConfig();
    tmp.put("BJetSelection.bjetDiscr", "");
    ParameterSet pset1(tmp, true);
    REQUIRE_NOTHROW(Event event1(pset1));
    tmp.put("BJetSelection.bjetDiscr", "combinedInclusiveSecondaryVertexV2BJetTags");
    ParameterSet pset2(tmp, true);
    REQUIRE_NOTHROW(Event event2(pset2));
    tmp.put("BJetSelection.bjetDiscr", "dummy");
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
  tmp.put("BJetSelection.bjetDiscr", "combinedInclusiveSecondaryVertexV2BJetTags");
  tmp.put("BJetSelection.bjetDiscrWorkingPoint", "Loose");
  tmp.put("BJetSelection.numberOfBJetsCutValue", 1);
  tmp.put("BJetSelection.numberOfBJetsCutDirection", ">=");
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
  std::vector<float> btagCSVv2;tree->Branch("Jets_combinedInclusiveSecondaryVertexV2BJetTags", &btagCSVv2);
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
  btagCSVv2 = std::vector<float>{0.2f, 0.96f, -0.1f, 0.99f, 0.8f, 0.98f, 0.4f, 0.7f};
  jetpt  = std::vector<float>{40.f,  60.f,   130.f,  12.f,  24.f,  50.f,  70.f,  90.f};
  jeteta = std::vector<float>{-1.24f, 0.34f,   2.6f,  1.2f,  4.5f, -2.1f, -3.2f,  1.2f};
  jetphi = std::vector<float>{-2.92f, -0.51f,  1.2f, -2.1f,  0.1f, -1.9f,  0.1f,  3.0f};
  jete   = std::vector<float>{40.f,  60.f,   130.f,  12.f,  24.f,  50.f,  70.f,  90.f};
  jetID  = std::vector<bool>{true, true, true, true, true, true, true, true};
  jetPUID = std::vector<bool>{true, true, true, true, true, true, true, true};
  tree->Fill();
  nevent = 2; // fail btag discriminator
  btagCSVv2 = std::vector<float>{1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f};
  tree->Fill();
  nevent = 3; // pass btag discriminator
  btagCSVv2 = std::vector<float>{0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f};
  tree->Fill();
  
  BranchManager mgr;
  mgr.setTree(tree);
  Event event(psetDefault);
  //event.setupBranches(mgr);
  
  SECTION("discriminator value") {
    tmp.put("BJetSelection.bjetDiscr", "combinedInclusiveSecondaryVertexV2BJetTags");
    tmp.put("BJetSelection.bjetDiscrWorkingPoint", "Loose");
    tmp.put("BJetSelection.numberOfBJetsCutValue", 1);
    tmp.put("BJetSelection.numberOfBJetsCutDirection", ">=");
    tmp.put("BJetSelection2.bjetDiscr", "combinedInclusiveSecondaryVertexV2BJetTags");
    tmp.put("BJetSelection2.bjetDiscrWorkingPoint", "Medium");
    tmp.put("BJetSelection2.numberOfBJetsCutValue", 1);
    tmp.put("BJetSelection2.numberOfBJetsCutDirection", ">=");
    tmp.put("BJetSelection3.bjetDiscr", "combinedInclusiveSecondaryVertexV2BJetTags");
    tmp.put("BJetSelection3.bjetDiscrWorkingPoint", "Tight");
    tmp.put("BJetSelection3.numberOfBJetsCutValue", 1);
    tmp.put("BJetSelection3.numberOfBJetsCutDirection", ">=");
    tmp.put("BJetSelection4.bjetDiscr", "combinedInclusiveSecondaryVertexV2BJetTags");
    tmp.put("BJetSelection4.bjetDiscrWorkingPoint", "dummy");
    tmp.put("BJetSelection4.numberOfBJetsCutValue", 1);
    tmp.put("BJetSelection4.numberOfBJetsCutDirection", ">=");
    tmp.put("BJetSelection5.bjetDiscr", "combinedSecondaryVertexBJetTags");
    tmp.put("BJetSelection5.bjetDiscrWorkingPoint", "Loose");
    tmp.put("BJetSelection5.numberOfBJetsCutValue", 1);
    tmp.put("BJetSelection5.numberOfBJetsCutDirection", ">=");
    ParameterSet newPset(tmp,true);
    // Test loose, medium, tight working points for an implemented algorithm
    REQUIRE_NOTHROW(BJetSelection(newPset.getParameter<ParameterSet>("BJetSelection"),
                          ec, histoWrapper, commonPlotsPointer, "1"));
    REQUIRE_NOTHROW(BJetSelection(newPset.getParameter<ParameterSet>("BJetSelection2"),
                          ec, histoWrapper, commonPlotsPointer, "2"));
    REQUIRE_NOTHROW(BJetSelection(newPset.getParameter<ParameterSet>("BJetSelection3"),
                          ec, histoWrapper, commonPlotsPointer, "3"));
    // Test using invalid working point
    REQUIRE_THROWS_AS(BJetSelection(newPset.getParameter<ParameterSet>("BJetSelection4"),
                          ec, histoWrapper, commonPlotsPointer, "4"), hplus::Exception);
    // Test using discriminator with no implemented working point values
    REQUIRE_THROWS_AS(BJetSelection(newPset.getParameter<ParameterSet>("BJetSelection5"),
                          ec, histoWrapper, commonPlotsPointer, "5"), hplus::Exception);
  }
  SECTION("apply discriminator") {
    tmp.put("BJetSelection.bjetDiscr", "combinedInclusiveSecondaryVertexV2BJetTags");
    tmp.put("BJetSelection.bjetDiscrWorkingPoint", "Tight");
    tmp.put("BJetSelection.numberOfBJetsCutValue", 0);
    tmp.put("BJetSelection.numberOfBJetsCutDirection", ">=");
    ParameterSet newPset(tmp,true);
    TauSelection tausel(newPset.getParameter<ParameterSet>("TauSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    JetSelection jetsel(newPset.getParameter<ParameterSet>("JetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    BJetSelection bjetsel(newPset.getParameter<ParameterSet>("BJetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    tausel.bookHistograms(f);
    jetsel.bookHistograms(f);
    bjetsel.bookHistograms(f);
    Event event2(newPset);
    event2.setupBranches(mgr);
    mgr.setEntry(0);
    TauSelection::Data tauData = tausel.silentAnalyze(event2);
    JetSelection::Data jetData = jetsel.silentAnalyze(event2, tauData);
    BJetSelection::Data bjetData = bjetsel.silentAnalyze(event2, jetData);
    CHECK( bjetData.passedSelection() == true );
    CHECK( bjetData.getNumberOfSelectedBJets() == 2 );
    mgr.setEntry(1);
    tauData = tausel.silentAnalyze(event2);
    jetData = jetsel.silentAnalyze(event2, tauData);
    bjetData = bjetsel.silentAnalyze(event2, jetData);
    CHECK( bjetData.passedSelection() == true );
    CHECK( bjetData.getNumberOfSelectedBJets() == 4 );
  }
  SECTION("apply Nbjets cut") {
    tmp.put("BJetSelection.bjetDiscr", "combinedInclusiveSecondaryVertexV2BJetTags");
    tmp.put("BJetSelection.bjetDiscrWorkingPoint", "Tight");
    tmp.put("BJetSelection.numberOfBJetsCutValue", 2);
    tmp.put("BJetSelection.numberOfBJetsCutDirection", ">=");
    ParameterSet newPset(tmp,true);
    TauSelection tausel(newPset.getParameter<ParameterSet>("TauSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    JetSelection jetsel(newPset.getParameter<ParameterSet>("JetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    BJetSelection bjetsel(newPset.getParameter<ParameterSet>("BJetSelection"),
                        ec, histoWrapper, commonPlotsPointer, "");
    tausel.bookHistograms(f);
    jetsel.bookHistograms(f);
    bjetsel.bookHistograms(f);
    Event event2(newPset);
    event2.setupBranches(mgr);
    mgr.setEntry(0);
    TauSelection::Data tauData = tausel.silentAnalyze(event2);
    JetSelection::Data jetData = jetsel.silentAnalyze(event2, tauData);
    BJetSelection::Data bjetData = bjetsel.silentAnalyze(event2, jetData);
    CHECK( bjetData.passedSelection() == true );
    mgr.setEntry(1);
    tauData = tausel.silentAnalyze(event2);
    jetData = jetsel.silentAnalyze(event2, tauData);
    bjetData = bjetsel.silentAnalyze(event2, jetData);
    CHECK( bjetData.passedSelection() == true );
    mgr.setEntry(2);
    tauData = tausel.silentAnalyze(event2);
    jetData = jetsel.silentAnalyze(event2, tauData);
    bjetData = bjetsel.silentAnalyze(event2, jetData);
    CHECK( bjetData.passedSelection() == false );
  }    
  ec.setOutput(f);
  ec.serialize();
  f->Write();
  f->Close();
}
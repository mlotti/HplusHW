// -*- c++ -*-
#include "catch.hpp"

#include "EventSelection/interface/MuonSelection.h"
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

TEST_CASE("MuonSelection", "[EventSelection]") {
  // Create config for testing
  boost::property_tree::ptree tmp = getMinimalConfig();
  tmp.put("MuonSelection1.muonPtCut", 30.0);
  tmp.put("MuonSelection1.muonEtaCut", 2.0);
  tmp.put("MuonSelection2.muonPtCut", 10.0);
  tmp.put("MuonSelection2.muonEtaCut", 1.0);
  ParameterSet pset(tmp, true);

  // Create necessary objects for testing
  TDirectory* f = getDirectory("test_MuonSelection");
  CommonPlots* commonPlotsPointer = 0;
  EventWeight weight;
  HistoWrapper histoWrapper(weight, "Debug");
  EventCounter ec(weight);
  MuonSelection musel1(pset.getParameter<ParameterSet>("MuonSelection1"),
                          ec, histoWrapper, commonPlotsPointer, "test");
  musel1.bookHistograms(f);
  MuonSelection musel2(pset.getParameter<ParameterSet>("MuonSelection2"),
                          ec, histoWrapper, commonPlotsPointer, "Veto");
  musel2.bookHistograms(f);
  // Setup events for testing
  
  auto tree = new TTree("Events", "Events");
  unsigned int run;           tree->Branch("run",   &run);
  unsigned int lumi;          tree->Branch("lumi",  &lumi);
  unsigned long long nevent;   tree->Branch("event", &nevent);
  std::vector<float> e_pt;   tree->Branch("Muons_pt", &e_pt);
  std::vector<float> e_eta;  tree->Branch("Muons_eta", &e_eta);
  std::vector<float> e_phi;  tree->Branch("Muons_phi", &e_phi);
  std::vector<float> e_e;    tree->Branch("Muons_e", &e_e);
  run = 1;
  lumi = 1;
  nevent = 1;
  e_pt = std::vector<float>{50.f, 20.f, 11.f, 75.f};
  e_eta = std::vector<float>{1.1f, -2.3f, 0.7f, 3.3f};
  e_phi = std::vector<float>{-2.9f, -0.5f, 1.f, 0.3f};
  e_e = std::vector<float>{60.f, 25.f, 40.f, 30.f};
  tree->Fill();
  run = 1;
  lumi = 1;
  nevent = 2;
  e_pt = std::vector<float>{9.f, 30.f, 30.f, 9.f};
  e_eta = std::vector<float>{0.1f, -4.3f, 2.7f, 0.3f};
  e_phi = std::vector<float>{-2.9f, -0.5f, 1.f, 0.3f};
  e_e = std::vector<float>{60.f, 25.f, 40.f, 30.f};
  tree->Fill();  
  BranchManager mgr;
  mgr.setTree(tree);
  Event event(pset);
  event.setupBranches(mgr);
  
  SECTION("Selection") {
    CHECK( ec.contains("passed mu selection (test)"));
    CHECK( ec.contains("passed mu selection (Veto)"));
    // Checks on event 1
    mgr.setEntry(0);
    MuonSelection::Data data = musel1.analyze(event);
    CHECK( data.getSelectedMuons().size() == 1 );
    CHECK( data.getHighestSelectedMuonPt() == 50.f );
    CHECK( data.getHighestSelectedMuonEta() == 1.1f );
    CHECK( data.getHighestSelectedMuonPtBeforePtCut() == 50.f );
    CHECK( ec.getValueByName("passed mu selection (test)") == 1);
    // Check protection for analyzing event only once
    REQUIRE_THROWS_AS(musel1.analyze(event), hplus::Exception);
    REQUIRE_THROWS_AS(musel1.silentAnalyze(event), hplus::Exception);
    // Continue event 1
    data = musel2.analyze(event);
    CHECK( data.getSelectedMuons().size() == 1 );
    CHECK( data.getHighestSelectedMuonPt() == 11.f );
    CHECK( data.getHighestSelectedMuonEta() == 0.7f );
    CHECK( data.getHighestSelectedMuonPtBeforePtCut() == 11.f );
    CHECK( ec.getValueByName("passed mu selection (Veto)") == 0);
    // Checks on event 2
    mgr.setEntry(1);
    data = musel1.analyze(event);
    CHECK( data.getSelectedMuons().size() == 0 );
    CHECK( data.getHighestSelectedMuonPt() < 1.f );
    CHECK( data.getHighestSelectedMuonEta() < 1.f );
    CHECK( data.getHighestSelectedMuonPtBeforePtCut() == 9.f );
    CHECK( ec.getValueByName("passed mu selection (test)") == 1);
    data = musel2.analyze(event);
    CHECK( data.getSelectedMuons().size() == 0 );
    CHECK( data.getHighestSelectedMuonPt() < 1.f );
    CHECK( data.getHighestSelectedMuonEta() < 1.f );
    CHECK( data.getHighestSelectedMuonPtBeforePtCut() == 9.f );
    CHECK( ec.getValueByName("passed mu selection (Veto)") == 1);
  }
  SECTION("protection for double counting of events") {
    mgr.setEntry(0);
    MuonSelection museldbl(pset.getParameter<ParameterSet>("MuonSelection2"),
                           ec, histoWrapper, commonPlotsPointer, "dblcount");
    museldbl.bookHistograms(f);
    CHECK( ec.getValueByName("passed mu selection (dblcount)") == 0);
    REQUIRE_NOTHROW( museldbl.silentAnalyze(event) );
    CHECK( ec.getValueByName("passed mu selection (dblcount)") == 0);
    REQUIRE_NOTHROW( museldbl.analyze(event) );
    CHECK( ec.getValueByName("passed mu selection (dblcount)") == 1);
    REQUIRE_THROWS_AS( museldbl.analyze(event), hplus::Exception );
    REQUIRE_THROWS_AS( museldbl.silentAnalyze(event), hplus::Exception );
  }
  ec.setOutput(f);
  ec.serialize();
  closeDirectory(f);
}
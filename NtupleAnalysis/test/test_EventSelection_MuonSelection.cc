// -*- c++ -*-
#include "catch.hpp"

#include "EventSelection/interface/MuonSelection.h"
#include "Framework/interface/Exception.h"
#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/EventWeight.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/BranchManager.h"
#include "DataFormat/interface/Event.h"

#include <string>
#include <sstream>
#include <iostream>
#include "TFile.h"
#include "TTree.h"

TEST_CASE("MuonSelection", "[EventSelection]") {
  // Create config for testing
  std::stringstream config;
  config << "{" << std::endl;
  config << "  \"MuonSelection1\": {" << std::endl;
  config << "    \"muonPtCut\": 30.0," << std::endl;
  config << "    \"muonEtaCut\": 2.0" << std::endl;
  config << "  }" << std::endl;
  config << "}" << std::endl;
  ParameterSet pset1(config.str());
  config.str("");
  config << "{" << std::endl;
  config << "  \"MuonSelection2\": {" << std::endl;
  config << "    \"muonPtCut\": 10.0," << std::endl;
  config << "    \"muonEtaCut\": 1.0" << std::endl;
  config << "  }" << std::endl;
  config << "}" << std::endl;
  ParameterSet pset2(config.str());
  // Create necessary objects for testing
  TFile* f = new TFile("test_MuonSelection.root", "recreate");
  CommonPlots* commonPlotsPointer = 0;
  EventWeight weight;
  HistoWrapper histoWrapper(weight, "Debug");
  EventCounter ec(weight);
  ec.setOutput(f);
  MuonSelection esel1(pset1.getParameter<ParameterSet>("MuonSelection1"),
                          ec, histoWrapper, commonPlotsPointer, "test");
  esel1.bookHistograms(f);
  MuonSelection esel2(pset2.getParameter<ParameterSet>("MuonSelection2"),
                          ec, histoWrapper, commonPlotsPointer, "Veto");
  esel2.bookHistograms(f);
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
  Event event(ParameterSet("{}", true));
  event.setupBranches(mgr);
  
  SECTION("Selection") {
    CHECK( ec.contains("passed e selection (test)"));
    CHECK( ec.contains("passed e selection (Veto)"));
    // Checks on event 1
    mgr.setEntry(0);
    MuonSelection::Data data = esel1.analyze(event);
    CHECK( data.getSelectedMuons().size() == 1 );
    CHECK( data.getHighestSelectedMuonPt() == 50.f );
    CHECK( data.getHighestSelectedMuonEta() == 1.1f );
    CHECK( data.getHighestSelectedMuonPtBeforePtCut() == 50.f );
    CHECK( ec.getValueByName("passed e selection (test)") == 1);
    // Check protection for analyzing event only once
    REQUIRE_THROWS_AS(esel1.analyze(event), hplus::Exception);
    REQUIRE_THROWS_AS(esel1.silentAnalyze(event), hplus::Exception);
    // Continue event 1
    data = esel2.analyze(event);
    CHECK( data.getSelectedMuons().size() == 1 );
    CHECK( data.getHighestSelectedMuonPt() == 11.f );
    CHECK( data.getHighestSelectedMuonEta() == 0.7f );
    CHECK( data.getHighestSelectedMuonPtBeforePtCut() == 11.f );
    CHECK( ec.getValueByName("passed e selection (Veto)") == 0);
    // Checks on event 2
    mgr.setEntry(1);
    data = esel1.analyze(event);
    CHECK( data.getSelectedMuons().size() == 0 );
    CHECK( data.getHighestSelectedMuonPt() < 1.f );
    CHECK( data.getHighestSelectedMuonEta() < 1.f );
    CHECK( data.getHighestSelectedMuonPtBeforePtCut() == 9.f );
    CHECK( ec.getValueByName("passed e selection (test)") == 1);
    data = esel2.analyze(event);
    CHECK( data.getSelectedMuons().size() == 0 );
    CHECK( data.getHighestSelectedMuonPt() < 1.f );
    CHECK( data.getHighestSelectedMuonEta() < 1.f );
    CHECK( data.getHighestSelectedMuonPtBeforePtCut() == 9.f );
    CHECK( ec.getValueByName("passed e selection (Veto)") == 1);
    // Make sure that silent analysis works
    mgr.setEntry(0);
    data = esel1.silentAnalyze(event);
    TH1* h = dynamic_cast<TH1*>(f->Get("eSelection_test/muonPtPassed"));
    CHECK( h != 0 );
    CHECK( data.getSelectedMuons().size() == 1 );
    CHECK( data.getHighestSelectedMuonPt() == 50.f );
    CHECK( data.getHighestSelectedMuonEta() == 1.1f );
    CHECK( data.getHighestSelectedMuonPtBeforePtCut() == 50.f );
    CHECK( ec.getValueByName("passed e selection (test)") == 1);
    CHECK( h->Integral() == 1.0f );
    data = esel1.analyze(event);
    CHECK( ec.getValueByName("passed e selection (test)") == 2);
    CHECK( h->Integral() == 2.0f );
  }
  f->Write();
  f->Close();
}
// -*- c++ -*-
#include "catch.hpp"

#include "EventSelection/interface/ElectronSelection.h"
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

TEST_CASE("ElectronSelection", "[EventSelection]") {
  // Create config for testing
  boost::property_tree::ptree tmp = getMinimalConfig();
  tmp.put("ElectronSelection1.electronPtCut", 30.0);
  tmp.put("ElectronSelection1.electronEtaCut", 2.0);
  tmp.put("ElectronSelection2.electronPtCut", 10.0);
  tmp.put("ElectronSelection2.electronEtaCut", 1.0);
  ParameterSet pset(tmp, true);
  // Create necessary objects for testing
  TDirectory* f = getDirectory("test_ElectronSelection");
  CommonPlots* commonPlotsPointer = 0;
  EventWeight weight;
  HistoWrapper histoWrapper(weight, "Debug");
  EventCounter ec(weight);
  ElectronSelection esel1(pset.getParameter<ParameterSet>("ElectronSelection1"),
                          ec, histoWrapper, commonPlotsPointer, "test");
  esel1.bookHistograms(f);
  ElectronSelection esel2(pset.getParameter<ParameterSet>("ElectronSelection2"),
                          ec, histoWrapper, commonPlotsPointer, "Veto");
  esel2.bookHistograms(f);
  // Setup events for testing
  
  auto tree = new TTree("Events", "Events");
  unsigned int run;           tree->Branch("run",   &run);
  unsigned int lumi;          tree->Branch("lumi",  &lumi);
  unsigned long long nevent;   tree->Branch("event", &nevent);
  std::vector<float> e_pt;   tree->Branch("Electrons_pt", &e_pt);
  std::vector<float> e_eta;  tree->Branch("Electrons_eta", &e_eta);
  std::vector<float> e_phi;  tree->Branch("Electrons_phi", &e_phi);
  std::vector<float> e_e;    tree->Branch("Electrons_e", &e_e);
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
    CHECK( ec.contains("passed e selection (test)"));
    CHECK( ec.contains("passed e selection (Veto)"));
    // Checks on event 1
    mgr.setEntry(0);
    ElectronSelection::Data data = esel1.analyze(event);
    CHECK( data.getSelectedElectrons().size() == 1 );
    CHECK( data.getHighestSelectedElectronPt() == 50.f );
    CHECK( data.getHighestSelectedElectronEta() == 1.1f );
    CHECK( data.getHighestSelectedElectronPtBeforePtCut() == 50.f );
    CHECK( ec.getValueByName("passed e selection (test)") == 1);
    // Check protection for analyzing event only once
    REQUIRE_THROWS_AS(esel1.analyze(event), hplus::Exception);
    REQUIRE_THROWS_AS(esel1.silentAnalyze(event), hplus::Exception);
    // Continue event 1
    data = esel2.analyze(event);
    CHECK( data.getSelectedElectrons().size() == 1 );
    CHECK( data.getHighestSelectedElectronPt() == 11.f );
    CHECK( data.getHighestSelectedElectronEta() == 0.7f );
    CHECK( data.getHighestSelectedElectronPtBeforePtCut() == 11.f );
    CHECK( ec.getValueByName("passed e selection (Veto)") == 0);
    // Checks on event 2
    mgr.setEntry(1);
    data = esel1.analyze(event);
    CHECK( data.getSelectedElectrons().size() == 0 );
    CHECK( data.getHighestSelectedElectronPt() < 1.f );
    CHECK( data.getHighestSelectedElectronEta() < 1.f );
    CHECK( data.getHighestSelectedElectronPtBeforePtCut() == 9.f );
    CHECK( ec.getValueByName("passed e selection (test)") == 1);
    data = esel2.analyze(event);
    CHECK( data.getSelectedElectrons().size() == 0 );
    CHECK( data.getHighestSelectedElectronPt() < 1.f );
    CHECK( data.getHighestSelectedElectronEta() < 1.f );
    CHECK( data.getHighestSelectedElectronPtBeforePtCut() == 9.f );
    CHECK( ec.getValueByName("passed e selection (Veto)") == 1);
  }

  SECTION("protection for double counting of events") {
    mgr.setEntry(0);
    ElectronSelection eseldbl(pset.getParameter<ParameterSet>("ElectronSelection2"),
                           ec, histoWrapper, commonPlotsPointer, "dblcount");
    eseldbl.bookHistograms(f);
    CHECK( ec.getValueByName("passed e selection (dblcount)") == 0);
    REQUIRE_NOTHROW( eseldbl.silentAnalyze(event) );
    CHECK( ec.getValueByName("passed e selection (dblcount)") == 0);
    REQUIRE_NOTHROW( eseldbl.analyze(event) );
    CHECK( ec.getValueByName("passed e selection (dblcount)") == 1);
    REQUIRE_THROWS_AS( eseldbl.analyze(event), hplus::Exception );
    REQUIRE_THROWS_AS( eseldbl.silentAnalyze(event), hplus::Exception );
  }
  
  ec.setOutput(f);
  ec.serialize();
  closeDirectory(f);
}
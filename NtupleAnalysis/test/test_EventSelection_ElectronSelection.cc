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
  tmp.put("ElectronSelection.electronPtCut", 30.0);
  tmp.put("ElectronSelection.electronEtaCut", 2.0);
  tmp.put("ElectronSelection.electronIsolation", "tight");
  tmp.put("ElectronSelection.electronID", "mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90");
  tmp.put("ElectronSelection2.electronPtCut", 10.0);
  tmp.put("ElectronSelection2.electronEtaCut", 1.0);
  tmp.put("ElectronSelection2.electronIsolation", "veto");
  tmp.put("ElectronSelection2.electronID", "mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90");
  ParameterSet pset(tmp, true);
  // Create necessary objects for testing
  TDirectory* f = getDirectory("test_ElectronSelection");
  CommonPlots* commonPlotsPointer = 0;
  EventWeight weight;
  HistoWrapper histoWrapper(weight, "Debug");
  EventCounter ec(weight);
  ElectronSelection esel1(pset.getParameter<ParameterSet>("ElectronSelection"),
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
  std::vector<float> emc_pt;   tree->Branch("Electrons_ptMCelectron", &emc_pt);
  std::vector<float> emc_eta;  tree->Branch("Electrons_etaMCelectron", &emc_eta);
  std::vector<float> emc_phi;  tree->Branch("Electrons_phiMCelectron", &emc_phi);
  std::vector<float> emc_e;    tree->Branch("Electrons_eMCelectron", &emc_e);
  std::vector<float> e_relIsoDeltaBeta; tree->Branch("Electrons_relIsoDeltaBeta", &e_relIsoDeltaBeta);
  std::vector<bool> e_id; tree->Branch("Electrons_mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90", &e_id);
  run = 1;
  lumi = 1;
  nevent = 1;
  e_pt = std::vector<float>{50.f, 20.f, 11.f, 75.f};
  e_eta = std::vector<float>{1.1f, -2.3f, 0.7f, 3.3f};
  e_phi = std::vector<float>{-2.9f, -0.5f, 1.f, 0.3f};
  e_e = std::vector<float>{60.f, 25.f, 40.f, 30.f};
  emc_pt = std::vector<float>{50.f, 20.f, 11.f, 75.f};
  emc_eta = std::vector<float>{1.1f, -2.3f, 0.7f, 3.3f};
  emc_phi = std::vector<float>{-2.9f, -0.5f, 1.f, 0.3f};
  emc_e = std::vector<float>{60.f, 25.f, 40.f, 30.f};
  e_relIsoDeltaBeta = std::vector<float>{0.1f, 0.1f, 0.1f, 0.1f};
  e_id = std::vector<bool>{true, true, true, true};
  tree->Fill();
  nevent = 2;
  e_pt = std::vector<float>{9.f, 30.f, 30.f, 9.f};
  e_eta = std::vector<float>{0.1f, -4.3f, 2.7f, 0.3f};
  e_phi = std::vector<float>{-2.9f, -0.5f, 1.f, 0.3f};
  e_e = std::vector<float>{60.f, 25.f, 40.f, 30.f};
  e_relIsoDeltaBeta = std::vector<float>{0.1f, 0.1f, 0.1f, 0.1f};
  e_id = std::vector<bool>{true, true, true, true};
  tree->Fill();
  nevent = 3;
  e_pt = std::vector<float>{50.f, 20.f, 11.f, 75.f};
  e_eta = std::vector<float>{1.1f, -2.3f, 0.7f, 3.3f};
  e_phi = std::vector<float>{-2.9f, -0.5f, 1.f, 0.3f};
  e_e = std::vector<float>{60.f, 25.f, 40.f, 30.f};
  e_relIsoDeltaBeta = std::vector<float>{.01f, .05f, .21f, .25f};
  e_id = std::vector<bool>{true, true, true, true};
  tree->Fill();
  nevent = 4;
  e_pt = std::vector<float>{50.f, 20.f, 11.f, 75.f};
  e_eta = std::vector<float>{1.1f, -2.3f, 0.7f, 3.3f};
  e_phi = std::vector<float>{-2.9f, -0.5f, 1.f, 0.3f};
  e_e = std::vector<float>{60.f, 25.f, 40.f, 30.f};
  e_relIsoDeltaBeta = std::vector<float>{0.1f, 0.1f, 0.1f, 0.1f};
  e_id = std::vector<bool>{false, true, false, true};
  tree->Fill();
  BranchManager mgr;
  mgr.setTree(tree);
  Event event(pset);
  event.setupBranches(mgr);
  
  SECTION("Config test") {
    boost::property_tree::ptree testcfg = getMinimalConfig();
    testcfg.put("ElectronSelection.electronPtCut", 30.0);
    testcfg.put("ElectronSelection.electronEtaCut", 2.0);
    testcfg.put("ElectronSelection.electronIsolation", "tight");
    testcfg.put("ElectronSelection.electronID", "mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90");
    REQUIRE_NOTHROW(Event(ParameterSet(testcfg, true)));
  }

  SECTION("Config test2") {
    boost::property_tree::ptree testcfg = getMinimalConfig();
    testcfg.put("ElectronSelection.electronPtCut", 30.0);
    testcfg.put("ElectronSelection.electronEtaCut", 2.0);
    testcfg.put("ElectronSelection.electronIsolation", "tight");
    REQUIRE_NOTHROW(Event(ParameterSet(testcfg, true)));
  }

  SECTION("Faulty config test") {
    boost::property_tree::ptree testcfg = getMinimalConfig();
    testcfg.put("ElectronSelection.electronPtCut", 30.0);
    testcfg.put("ElectronSelection.electronEtaCut", 2.0);
    testcfg.put("ElectronSelection.electronIsolation", "dummy");
    testcfg.put("ElectronSelection.electronID", "notexist");
    REQUIRE_THROWS_AS(Event(ParameterSet(testcfg, true)), hplus::Exception);
    REQUIRE_THROWS_AS(ElectronSelection(ParameterSet(testcfg, true).getParameter<ParameterSet>("ElectronSelection"),
                      ec, histoWrapper, commonPlotsPointer, "test"), hplus::Exception);
  }
  
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
    // Checks on event 3
    mgr.setEntry(2);
    data = esel1.analyze(event);
    CHECK( data.getSelectedElectrons().size() == 1 );
    data = esel2.analyze(event);
    CHECK( data.getSelectedElectrons().size() == 0 );
    // Checks on event 4
    mgr.setEntry(3);
    data = esel1.analyze(event);
    CHECK( data.getSelectedElectrons().size() == 0 );
    data = esel2.analyze(event);
    CHECK( data.getSelectedElectrons().size() == 0 );
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
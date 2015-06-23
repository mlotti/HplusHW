// -*- c++ -*-
#include "catch.hpp"

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

TEST_CASE("METSelection", "[EventSelection]") {
  // Create config for testing
  boost::property_tree::ptree tmp = getMinimalConfig();
  tmp.put("METSelection.METCutValue", 80.0);
  tmp.put("METSelection.METCutDirection", ">");
  tmp.put("METSelection.METType", "type1MET");
  tmp.put("METSelection.applyPhiCorrections", false);
  ParameterSet pset(tmp, true, true);

  // Create necessary objects for testing
  TFile* f = new TFile("test_METSelection.root", "recreate");
  CommonPlots* commonPlotsPointer = 0;
  EventWeight weight;
  HistoWrapper histoWrapper(weight, "Debug");
  EventCounter ec(weight);
  METSelection metsel(pset.getParameter<ParameterSet>("METSelection"),
                      ec, histoWrapper, commonPlotsPointer, "test");
  metsel.bookHistograms(f);
  // Setup events for testing
  auto tree = new TTree("Events", "Events");
  unsigned int run;           tree->Branch("run",   &run);
  unsigned int lumi;          tree->Branch("lumi",  &lumi);
  unsigned long long nevent;  tree->Branch("event", &nevent);
  double type1METet;          tree->Branch("MET_Type1_et", &type1METet);
  double type1METphi;         tree->Branch("MET_Type1_phi", &type1METphi);
  int nPU;                    tree->Branch("nGoodOfflinePV", &nPU);
  run = 1;
  lumi = 1;
  nevent = 1;
  type1METet = 90.0;
  type1METphi = 1.2;
  nPU = 1;
  tree->Fill();
  nevent = 2;
  type1METet = 90.0;
  type1METphi = 2.6;
  nPU = 30;
  tree->Fill();
  nevent = 3;
  type1METet = 40.0;
  type1METphi = -2.6;
  nPU = 30;
  tree->Fill();  
  BranchManager mgr;
  mgr.setTree(tree);
  Event event(pset);
  event.setupBranches(mgr);
  
  SECTION("PV Selection") {
    mgr.setEntry(0);
    CHECK( event.NPU().value() == 1);
    mgr.setEntry(1);
    CHECK( event.NPU().value() == 30);
  }

  SECTION("config") {
    tmp.put("METSelection.METType", "dummy");
    ParameterSet p(tmp, true, true);
    REQUIRE_THROWS_AS( METSelection metsel(p.getParameter<ParameterSet>("METSelection"),
                                           ec, histoWrapper, commonPlotsPointer, "test"), hplus::Exception );
  }
  
  SECTION("MET Selection") {
    mgr.setEntry(0);
    METSelection::Data data = metsel.analyze(event, event.NPU().value());
    CHECK( data.passedSelection() == true );
    CHECK( floatcmp(data.getMET().R(), 90.0) );
    CHECK( floatcmp(data.getMET().Phi(), 1.2) );
    mgr.setEntry(1);
    data = metsel.analyze(event, event.NPU().value());
    CHECK( data.passedSelection() == true );
    CHECK( floatcmp(data.getMET().R(), 90.0) );
    CHECK( floatcmp(data.getMET().Phi(), 2.6) );
    mgr.setEntry(2);
    data = metsel.analyze(event, event.NPU().value());
    CHECK( data.passedSelection() == false );
    CHECK( floatcmp(data.getMET().R(), 40.0) );
    CHECK( floatcmp(data.getMET().Phi(), -2.6) );
  }
  SECTION("protection for double counting of events") {
    mgr.setEntry(0);
    METSelection metsel2(pset.getParameter<ParameterSet>("METSelection"),
                    ec, histoWrapper, commonPlotsPointer, "dblcount");
    metsel2.bookHistograms(f);
    CHECK( ec.getValueByName("passed MET selection (dblcount)") == 0);
    REQUIRE_NOTHROW( metsel2.silentAnalyze(event, event.NPU().value()));
    CHECK( ec.getValueByName("passed MET selection (dblcount)") == 0);
    REQUIRE_NOTHROW( metsel2.analyze(event, event.NPU().value()) );
    CHECK( ec.getValueByName("passed MET selection (dblcount)") == 1);
    REQUIRE_THROWS_AS( metsel2.analyze(event, event.NPU().value()), hplus::Exception );
  }
  ec.setOutput(f);
  ec.serialize();
  f->Write();
  f->Close();
}
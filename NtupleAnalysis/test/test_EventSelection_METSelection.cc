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
#include "TLeaf.h"

TEST_CASE("METSelection", "[EventSelection]") {
  // Create config for testing
  boost::property_tree::ptree tmp = getMinimalConfig();
  tmp.put("METSelection.METCutValue", 80.0);
  tmp.put("METSelection.METCutDirection", ">");
  tmp.put("METSelection.METType", "type1MET");
  tmp.put("METSelection.applyPhiCorrections", false);
  ParameterSet pset(tmp, true, true);

  // Create necessary objects for testing
  TDirectory* f = getDirectory("test_METSelection");
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
  double type1METx;           tree->Branch("MET_Type1_x", &type1METx);
  double type1METy;           tree->Branch("MET_Type1_y", &type1METy);
  short nPU;                  tree->Branch("nGoodOfflineVertices", &nPU);
  
  run = 1;
  lumi = 1;
  nevent = 1;
  type1METx = 32.61220;
  type1METy = 83.88352;
  nPU = 1;
  tree->Fill();
  nevent = 2;
  type1METx = -77.11999;
  type1METy = 46.395123;
  nPU = 30;
  tree->Fill();
  nevent = 3;
  type1METx = -34.27555;
  type1METy = -20.620055;
  nPU = 30;
  tree->Fill();  
  BranchManager mgr;
  mgr.setTree(tree);
  Event event(pset);
  event.setupBranches(mgr);
  TBranch* b = tree->GetBranch("nGoodOfflineVertices");
  tree->GetEvent(0);
  
  SECTION("PV Selection") {
    mgr.setEntry(0);
    CHECK( event.vertexInfo().value() == 1);
    mgr.setEntry(1);
    CHECK( event.vertexInfo().value() == 30);
  }

  SECTION("config") {
    tmp.put("METSelection.METType", "dummy");
    ParameterSet p(tmp, true, true);
    REQUIRE_THROWS_AS( METSelection metsel(p.getParameter<ParameterSet>("METSelection"),
                                           ec, histoWrapper, commonPlotsPointer, "test"), hplus::Exception );
  }
  
  SECTION("MET Selection") {
    mgr.setEntry(0);
    METSelection::Data data = metsel.analyze(event, event.vertexInfo().value());
    CHECK( data.passedSelection() == true );
    CHECK( data.getMET().R() == Approx(90.0) );
    CHECK( data.getMET().Phi() == Approx(1.2) );
    mgr.setEntry(1);
    data = metsel.analyze(event, event.vertexInfo().value());
    CHECK( data.passedSelection() == true );
    CHECK( data.getMET().R() == Approx(90.0) );
    CHECK( data.getMET().Phi() == Approx(2.6) );
    mgr.setEntry(2);
    data = metsel.analyze(event, event.vertexInfo().value());
    CHECK( data.passedSelection() == false );
    CHECK( data.getMET().R() == Approx(40.0) );
    CHECK( data.getMET().Phi() == Approx(-2.6) );
  }
  SECTION("protection for double counting of events") {
    mgr.setEntry(0);
    METSelection metsel2(pset.getParameter<ParameterSet>("METSelection"),
                    ec, histoWrapper, commonPlotsPointer, "dblcount");
    metsel2.bookHistograms(f);
    CHECK( ec.getValueByName("passed MET selection (dblcount)") == 0);
    REQUIRE_NOTHROW( metsel2.silentAnalyze(event, event.vertexInfo().value()));
    CHECK( ec.getValueByName("passed MET selection (dblcount)") == 0);
    REQUIRE_NOTHROW( metsel2.analyze(event, event.vertexInfo().value()) );
    CHECK( ec.getValueByName("passed MET selection (dblcount)") == 1);
    REQUIRE_THROWS_AS( metsel2.analyze(event, event.vertexInfo().value()), hplus::Exception );
  }
  ec.setOutput(f);
  ec.serialize();
  closeDirectory(f);
}
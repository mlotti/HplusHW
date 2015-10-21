#include "catch.hpp"

#include "test_createTree.h"

#include "Framework/interface/BranchManager.h"
#include <Framework/interface/Exception.h>
#include "EventSelection/interface/METFilterSelection.h"
#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/EventWeight.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/BranchManager.h"
#include "DataFormat/interface/Event.h"

#include <algorithm>
#include <vector>
#include <string>

TEST_CASE("METFilterSelection", "[EventSelection]") {
  // Setup events for testing
  boost::property_tree::ptree discrs;
  boost::property_tree::ptree child;
  child.put("", "Flag_CSCTightHaloFilter");
  discrs.push_back(std::make_pair("", child));
  child.put("", "Flag_eeBadScFilter");
  discrs.push_back(std::make_pair("", child));
  child.put("", "Flag_goodVertices");
  discrs.push_back(std::make_pair("", child));
  boost::property_tree::ptree allDiscrs;
  allDiscrs.add_child("METFilter.discriminators", discrs);
  ParameterSet psetDefault(allDiscrs, true, true);

  auto tree = new TTree("Events", "Events");
  unsigned int run;           tree->Branch("run",   &run);
  unsigned int lumi;          tree->Branch("lumi",  &lumi);
  unsigned long long nevent;  tree->Branch("event", &nevent);
  bool d1; tree->Branch("METFilter_Flag_CSCTightHaloFilter", &d1);
  bool d2; tree->Branch("METFilter_Flag_eeBadScFilter", &d2);
  bool d3; tree->Branch("METFilter_Flag_goodVertices", &d3);
  run = 1;
  lumi = 1;
  nevent = 1;
  d1 = false;
  d2 = true;
  d3 = true;
  tree->Fill();
  nevent = 2;
  d1 = true;
  d2 = true;
  d3 = false;
  tree->Fill();
  nevent = 3;
  d1 = true;
  d2 = true;
  d3 = true;
  tree->Fill();

  boost::property_tree::ptree tmp;
  ParameterSet psetEmpty(tmp, true, true);

  // Create necessary objects for testing
  TDirectory* f = getDirectory("test_METFilters");
  CommonPlots* commonPlotsPointer = 0;
  EventWeight weight;
  HistoWrapper histoWrapper(weight, "Debug");
  EventCounter ec(weight);
  BranchManager mgr;
  mgr.setTree(tree);
  Event event(psetDefault);
  event.setupBranches(mgr);

  SECTION("No discriminators") {
    REQUIRE_THROWS_AS( METFilterSelection(psetEmpty, ec, histoWrapper, commonPlotsPointer, "test"), hplus::Exception );
  }
  
  SECTION("Empty list of discriminators") {
    boost::property_tree::ptree tmpchild;
    boost::property_tree::ptree tmp;
    tmp.add_child("METFilter.discriminators", tmpchild);
    ParameterSet pset(tmp, true, true);
    Event eventtmp(pset);
    eventtmp.setupBranches(mgr);
    REQUIRE_NOTHROW( METFilterSelection(pset.getParameter<ParameterSet>("METFilter"), ec, histoWrapper, commonPlotsPointer, "test") );
    METFilterSelection m(pset.getParameter<ParameterSet>("METFilter"), ec, histoWrapper, commonPlotsPointer, "test");
    mgr.setEntry(0);
    METFilterSelection::Data data = m.silentAnalyze(eventtmp);
    CHECK( data.passedSelection() == true );
  }

  SECTION("Discriminator values") {
    REQUIRE_NOTHROW( METFilterSelection(psetDefault.getParameter<ParameterSet>("METFilter"), ec, histoWrapper, commonPlotsPointer, "test") );
    METFilterSelection m(psetDefault.getParameter<ParameterSet>("METFilter"), ec, histoWrapper, commonPlotsPointer, "test");
    mgr.setEntry(0);
    METFilterSelection::Data data = m.analyze(event);
    CHECK( data.passedSelection() == false );
    mgr.setEntry(1);
    data = m.analyze(event);
    CHECK( data.passedSelection() == false );
    mgr.setEntry(2);
    data = m.analyze(event);
    CHECK( data.passedSelection() == true );
  }
  
  SECTION("Protection for double counting of events") {
    mgr.setEntry(2);
    METFilterSelection m(psetDefault.getParameter<ParameterSet>("METFilter"), ec, histoWrapper, commonPlotsPointer, "dblcount");
    CHECK( ec.getValueByName("passed METFilter selection (dblcount)") == 0 );
    REQUIRE_NOTHROW( m.silentAnalyze(event) );
    CHECK( ec.getValueByName("passed METFilter selection (dblcount)") == 0 );
    REQUIRE_NOTHROW( m.analyze(event) );
    CHECK( ec.getValueByName("passed METFilter selection (dblcount)") == 1 );
    REQUIRE_THROWS_AS( m.analyze(event), hplus::Exception );
    REQUIRE_THROWS_AS( m.silentAnalyze(event), hplus::Exception );
    REQUIRE_THROWS_AS( m.analyze(event), hplus::Exception );
  }
}

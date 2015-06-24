#include "catch.hpp"

#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/Exception.h"
#include "DataFormat/interface/Event.h"

#include "test_createTree.h"

#include "TDirectory.h"
#include "TH1.h"

#include <iostream>

TEST_CASE("Event works", "[Framework]") {  
  SECTION("Trigger decision") {
    auto tree = new TTree("Events", "Events");
    unsigned int run;           tree->Branch("run",   &run);
    unsigned int lumi;          tree->Branch("lumi",  &lumi);
    unsigned long long nevent;  tree->Branch("event", &nevent);
    bool trg1;   tree->Branch("HLT_trg1", &trg1);
    bool trg2;   tree->Branch("HLT_trg2_v5", &trg2);
    run = 1;
    lumi = 1;    
    nevent = 1;
    trg1 = false;
    trg2 = false;
    tree->Fill();
    nevent = 2;
    trg1 = true;
    trg2 = true;
    tree->Fill();
    nevent = 3;
    trg1 = false;
    trg2 = true;
    tree->Fill();
    nevent = 4;
    trg1 = true;
    trg2 = false;
    tree->Fill();
    BranchManager mgr;
    mgr.setTree(tree);
    boost::property_tree::ptree tmp = getMinimalConfig();
    Event event(ParameterSet(tmp, true, false));
    event.setupBranches(mgr);
    boost::property_tree::ptree trgs;
    boost::property_tree::ptree child;
    child.put("", "HLT_trg1");
    trgs.push_back(std::make_pair("", child));
    child.put("", "HLT_trg2");
    trgs.push_back(std::make_pair("", child));
    tmp.add_child("Trigger.triggerOR", trgs);
    Event event2(ParameterSet(tmp, true, false));
    event2.setupBranches(mgr);
    
    mgr.setEntry(0);
    REQUIRE_THROWS_AS ( event.configurableTriggerDecision(), hplus::Exception);
    REQUIRE_THROWS_AS ( event.configurableTriggerDecision2(), hplus::Exception);
    CHECK ( event.configurableTriggerIsEmpty() == true );
    CHECK ( event.configurableTrigger2IsEmpty() == true );
    CHECK ( event.passTriggerDecision() == true );
    CHECK ( event2.configurableTriggerIsEmpty() == false );
    CHECK ( event2.configurableTrigger2IsEmpty() == true );
    CHECK ( event2.configurableTriggerDecision() == false );
    REQUIRE_THROWS_AS ( event2.configurableTriggerDecision2(), hplus::Exception);
    CHECK ( event2.passTriggerDecision() == false );
    mgr.setEntry(1);
    REQUIRE_THROWS_AS ( event.configurableTriggerDecision(), hplus::Exception);
    REQUIRE_THROWS_AS ( event.configurableTriggerDecision2(), hplus::Exception);
    CHECK ( event.configurableTriggerIsEmpty() == true );
    CHECK ( event.configurableTrigger2IsEmpty() == true );
    CHECK ( event.passTriggerDecision() == true );
    CHECK ( event2.configurableTriggerDecision() == true );
    REQUIRE_THROWS_AS ( event2.configurableTriggerDecision2(), hplus::Exception);
    CHECK ( event2.configurableTrigger2IsEmpty() == true );
    CHECK ( event2.configurableTriggerIsEmpty() == false );
    CHECK ( event2.passTriggerDecision() == true );
    mgr.setEntry(2);
    CHECK ( event2.configurableTriggerDecision() == true );
    REQUIRE_THROWS_AS ( event2.configurableTriggerDecision2(), hplus::Exception);
    CHECK ( event2.configurableTriggerIsEmpty() == false );
    CHECK ( event2.configurableTrigger2IsEmpty() == true );
    CHECK ( event2.passTriggerDecision() == true );
    mgr.setEntry(3);
    CHECK ( event2.configurableTriggerDecision() == true );
    REQUIRE_THROWS_AS ( event2.configurableTriggerDecision2(), hplus::Exception);
    CHECK ( event2.configurableTriggerIsEmpty() == false );
    CHECK ( event2.configurableTrigger2IsEmpty() == true );
    CHECK ( event2.passTriggerDecision() == true );
  }
}
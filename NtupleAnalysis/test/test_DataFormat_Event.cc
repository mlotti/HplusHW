#include "catch.hpp"

#include "test_createTree.h"

#include "Framework/interface/BranchManager.h"
#include "DataFormat/interface/Event.h"
#include <string>

TEST_CASE("Event", "[DataFormat]") {
  SECTION("Default case") {
    std::unique_ptr<TTree> tree = createRealisticTree();

    BranchManager mgr;
    mgr.setTree(tree.get());
    
    ParameterSet pset(getMinimalConfig(), true);
    Event event(pset);
    event.setupBranches(mgr);

    SECTION("Event") {
      CHECK( event.isMC() == true );
      CHECK( event.isData() == false );

      mgr.setEntry(0);
      CHECK( event.eventID().event() == 1u );
      CHECK( event.eventID().lumi() == 1 );
      CHECK( event.eventID().run() == 1 );

      REQUIRE( event.taus().size() == 4 );
      CHECK( event.taus()[0].pt() == 50.f );
      CHECK( event.taus()[0].eta() == 0.1f );
      CHECK( event.taus()[0].phi() == -2.9f );
      CHECK( event.taus()[0].e() == 60.f );
      CHECK( event.met_Type1().et() == Approx(50.0) );
      CHECK( event.met_Type1().phi() == Approx(0.1) );


      mgr.setEntry(1);
      CHECK( event.eventID().event() == 2u );
      CHECK( event.eventID().lumi() == 1 );
      CHECK( event.eventID().run() == 1 );
      REQUIRE( event.taus().size() == 1 );
      CHECK( event.taus()[0].pt() == 20.f );
      CHECK( event.taus()[0].eta() == 0.9f );
      CHECK( event.taus()[0].phi() == 3.1f );
      CHECK( event.taus()[0].e() == 25.f );
      CHECK( event.met_Type1().et() == Approx(45.0) );
      CHECK( event.met_Type1().phi() == Approx(3.1) );
    }

    SECTION("Non-existent object") {
      mgr.setEntry(0);
      REQUIRE_THROWS_AS( event.jets().size(), std::runtime_error );
    }
  }

  SECTION("Systematic variations") {
    std::unique_ptr<TTree> tree = createRealisticTree();

    BranchManager mgr;
    mgr.setTree(tree.get());

    boost::property_tree::ptree tmp = getMinimalConfig();
    tmp.put("TauSelection.systematicVariation", "systVarTESUp");
    ParameterSet config(tmp, true);

    Event event(config);
    event.setupBranches(mgr);

    SECTION("Event") {
      mgr.setEntry(0);
      CHECK( event.eventID().event() == 1u );
      CHECK( event.eventID().lumi() == 1 );
      CHECK( event.eventID().run() == 1 );

      REQUIRE( event.taus().size() == 4 );
      CHECK( event.taus()[0].pt() == 50.f*1.03f );
      CHECK( event.taus()[0].eta() == 0.1f );
      CHECK( event.taus()[0].phi() == -2.9f );
      CHECK( event.taus()[0].e() == 60.f*1.03f );
      CHECK( event.met_Type1().et() == Approx(60.0) );
      CHECK( event.met_Type1().phi() == Approx(0.7) );


      mgr.setEntry(1);
      CHECK( event.eventID().event() == 2u );
      CHECK( event.eventID().lumi() == 1 );
      CHECK( event.eventID().run() == 1 );
      REQUIRE( event.taus().size() == 1 );
      CHECK( event.taus()[0].pt() == 20.f*1.03f );
      CHECK( event.taus()[0].eta() == 0.9f );
      CHECK( event.taus()[0].phi() == 3.1f );
      CHECK( event.taus()[0].e() == 25.f*1.03f );
      CHECK( event.met_Type1().et() == Approx(30.0) );
      CHECK( event.met_Type1().phi() == Approx(-2.6) );
    }
  }

  SECTION("Multiple systematic variations") {
    boost::property_tree::ptree tmp = getMinimalConfig();
    tmp.put("TauSelection.systematicVariation", "systVarTESUp");
    tmp.put("JetSelection.systematicVariation", "systVarJESUp");
    ParameterSet config(tmp, true);

    REQUIRE_THROWS_AS( Event event(config), std::runtime_error );
  }

  SECTION("Tau configurable discriminators") {
    std::unique_ptr<TTree> tree = createRealisticTree();

    BranchManager mgr;
    mgr.setTree(tree.get());

    boost::property_tree::ptree tmp = getMinimalConfig();

    SECTION("One discriminator") {
      TauCollection fTauCollection;
      boost::property_tree::ptree discrs;
      boost::property_tree::ptree child;
      child.put("", fTauCollection.getIsolationDiscriminatorNames()[0]);
      discrs.push_back(std::make_pair("", child));

      tmp.add_child("TauSelection.discriminators", discrs);

      ParameterSet config(tmp, true);
      Event event(config);
      event.setupBranches(mgr);

      mgr.setEntry(0);
      REQUIRE( event.taus().size() == 4 );
      CHECK( event.taus()[0].configurableDiscriminators() == true );
      CHECK( event.taus()[3].configurableDiscriminators() == false );

      mgr.setEntry(1);
      REQUIRE( event.taus().size() == 1 );
      CHECK( event.taus()[0].configurableDiscriminators() == true );
    }

    SECTION("Three discriminators") {
      TauCollection fTauCollection;
      boost::property_tree::ptree discrs;
      boost::property_tree::ptree child;
      child.put("", fTauCollection.getIsolationDiscriminatorNames()[0]);
      discrs.push_back(std::make_pair("", child));
      child.put("", fTauCollection.getAgainstMuonDiscriminatorNames()[0]);
      discrs.push_back(std::make_pair("", child));
      child.put("", fTauCollection.getAgainstElectronDiscriminatorNames()[0]);
      discrs.push_back(std::make_pair("", child));

      tmp.add_child("TauSelection.discriminators", discrs);

      ParameterSet config(tmp, true);
      Event event(config);
      event.setupBranches(mgr);

      mgr.setEntry(0);
      REQUIRE( event.taus().size() == 4 );
      CHECK( event.taus()[0].configurableDiscriminators() == true );
      CHECK( event.taus()[1].configurableDiscriminators() == false );
      CHECK( event.taus()[3].configurableDiscriminators() == false );

      mgr.setEntry(1);
      REQUIRE( event.taus().size() == 1 );
      CHECK( event.taus()[0].configurableDiscriminators() == false );
    }
  }

  SECTION("Trigger OR") {
    std::unique_ptr<TTree> tree = createRealisticTree();

    BranchManager mgr;
    mgr.setTree(tree.get());

    boost::property_tree::ptree tmp = getMinimalConfig();
    boost::property_tree::ptree trgchild;
    boost::property_tree::ptree child;
    child.put("", "HLT_Trig1");
    trgchild.push_back(std::make_pair("", child));
    child.put("", "HLT_Trig2");
    trgchild.push_back(std::make_pair("", child));
    boost::property_tree::ptree trgOr;
    trgOr.add_child("triggerOR", trgchild);
    tmp.add_child("Trigger",trgOr);
    ParameterSet config(tmp, true);
    Event event(config);
    event.setupBranches(mgr);

    mgr.setEntry(0);
    CHECK( event.configurableTriggerDecision() == true );

    mgr.setEntry(1);
    CHECK( event.configurableTriggerDecision() == true );

    mgr.setEntry(2);
    CHECK( event.configurableTriggerDecision() == false );
  }
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

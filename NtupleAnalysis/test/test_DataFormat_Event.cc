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
      CHECK( event.met_Type1().et() == 50.0 );
      CHECK( event.met_Type1().phi() == 0.1 );


      mgr.setEntry(1);
      CHECK( event.eventID().event() == 2u );
      CHECK( event.eventID().lumi() == 1 );
      CHECK( event.eventID().run() == 1 );
      REQUIRE( event.taus().size() == 1 );
      CHECK( event.taus()[0].pt() == 20.f );
      CHECK( event.taus()[0].eta() == 0.9f );
      CHECK( event.taus()[0].phi() == 3.1f );
      CHECK( event.taus()[0].e() == 25.f );
      CHECK( event.met_Type1().et() == 45 );
      CHECK( event.met_Type1().phi() == 3.1 );
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
      CHECK( event.met_Type1().et() == 60.0 );
      CHECK( event.met_Type1().phi() == 0.7 );


      mgr.setEntry(1);
      CHECK( event.eventID().event() == 2u );
      CHECK( event.eventID().lumi() == 1 );
      CHECK( event.eventID().run() == 1 );
      REQUIRE( event.taus().size() == 1 );
      CHECK( event.taus()[0].pt() == 20.f*1.03f );
      CHECK( event.taus()[0].eta() == 0.9f );
      CHECK( event.taus()[0].phi() == 3.1f );
      CHECK( event.taus()[0].e() == 25.f*1.03f );
      CHECK( event.met_Type1().et() == 30.0 );
      CHECK( event.met_Type1().phi() == -2.6 );
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
      boost::property_tree::ptree discrs;
      boost::property_tree::ptree child;
      child.put("", "discriminator3");
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
      boost::property_tree::ptree discrs;
      boost::property_tree::ptree child;
      child.put("", "discriminator1");
      discrs.push_back(std::make_pair("", child));
      child.put("", "discriminator2");
      discrs.push_back(std::make_pair("", child));
      child.put("", "discriminator3");
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
}

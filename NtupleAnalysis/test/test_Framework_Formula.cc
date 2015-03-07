#include "catch.hpp"

#include "test_createTree.h"

#include "Framework/interface/Formula.h"
#include "Framework/interface/BranchManager.h"
#include "DataFormat/interface/Event.h"

#include <iostream>

TEST_CASE("Formula", "[Framework]") {
  std::unique_ptr<TTree> tree = createRealisticTree();

  FormulaManager mgr;

  SECTION("One variable") {
    Formula formula = mgr.book("event");
    mgr.setupBranch(tree.get());

    tree->LoadTree(0);
    CHECK( static_cast<int>(formula.value()) == 1 );
    CHECK( static_cast<int>(formula.value()) == 1 );
    CHECK( static_cast<int>(formula.value()) == 1 );

    tree->LoadTree(1);
    CHECK( static_cast<int>(formula.value()) == 2 );

    tree->LoadTree(2);
    CHECK( static_cast<int>(formula.value()) == 3 );
  }

  SECTION("Two formulas for the same") {
    Formula f1 = mgr.book("event");
    Formula f2 = mgr.book("event");
    mgr.setupBranch(tree.get());

    tree->LoadTree(0);
    CHECK( static_cast<int>(f1.value()) == 1 );
    CHECK( static_cast<int>(f1.value()) == 1 );
    CHECK( static_cast<int>(f2.value()) == 1 );
    CHECK( static_cast<int>(f2.value()) == 1 );

    tree->LoadTree(1);
    CHECK( static_cast<int>(f1.value()) == 2 );
    CHECK( static_cast<int>(f2.value()) == 2 );

    tree->LoadTree(2);
    CHECK( static_cast<int>(f1.value()) == 3 );
    CHECK( static_cast<int>(f2.value()) == 3 );
  }

  SECTION("Two formulas for different branches") {
    Formula f1 = mgr.book("event");
    Formula f2 = mgr.book("lumi");
    mgr.setupBranch(tree.get());

    tree->LoadTree(0);
    CHECK( static_cast<int>(f1.value()) == 1 );
    CHECK( static_cast<int>(f1.value()) == 1 );
    CHECK( static_cast<int>(f2.value()) == 1 );
    CHECK( static_cast<int>(f2.value()) == 1 );

    tree->LoadTree(1);
    CHECK( static_cast<int>(f1.value()) == 2 );
    CHECK( static_cast<int>(f2.value()) == 1 );

    tree->LoadTree(2);
    CHECK( static_cast<int>(f1.value()) == 3 );
    CHECK( static_cast<int>(f2.value()) == 2 );
  }

  SECTION("Complex formula") {
    Formula formula = mgr.book("event + lumi - run");
    mgr.setupBranch(tree.get());

    tree->LoadTree(0);
    CHECK( static_cast<int>(formula.value()) == 1 );
    CHECK( static_cast<int>(formula.value()) == 1 );
    CHECK( static_cast<int>(formula.value()) == 1 );

    tree->LoadTree(1);
    CHECK( static_cast<int>(formula.value()) == 2 );

    tree->LoadTree(2);
    CHECK( static_cast<int>(formula.value()) == 4 );
  }

  SECTION("Formula to non-existent branch") {
    Formula formula = mgr.book("foobar");
    mgr.setupBranch(tree.get());

    REQUIRE( formula.isValid() == false );

    tree->LoadTree(0);
    REQUIRE_THROWS_AS( formula.value(), std::runtime_error );
  }

  SECTION("Trigger OR formula") {
    Formula trg = mgr.book("HLT_Trig1 || HLT_Trig2 || HLT_Trig3");
    mgr.setupBranch(tree.get());

    tree->LoadTree(0);
    CHECK( trg.value() > 0 );
    CHECK( trg.value() > 0 );

    tree->LoadTree(1);
    CHECK( trg.value() > 0 );

    tree->LoadTree(2);
    CHECK( trg.value() <= 0 );
  }

  SECTION("Trigger OR of non-existent branch") {
    Formula trg = mgr.book("HLT_Trig1 || HLT_Trig_Nonexistent");
    mgr.setupBranch(tree.get());

    tree->LoadTree(0);
    CHECK( trg.value() > 0 );
    CHECK( trg.value() > 0 );

    tree->LoadTree(1);
    CHECK( trg.value() > 0 );

    // This is what we would like to have
    tree->LoadTree(2);
    CHECK( trg.value() <= 0 );
  }


  SECTION("Formula and a branch to the same") {
    Formula formula = mgr.book("event");
    mgr.setupBranch(tree.get());

    Branch<unsigned long long> b_event("event");
    b_event.setupBranch(tree.get());

    tree->LoadTree(0);
    b_event.setEntry(0);
    CHECK( static_cast<int>(formula.value()) == 1 );
    CHECK( b_event.value() == 1);
    CHECK( static_cast<int>(formula.value()) == 1 );
    CHECK( b_event.value() == 1);
    CHECK( static_cast<int>(formula.value()) == 1 );
    CHECK( b_event.value() == 1);

    tree->LoadTree(1);
    b_event.setEntry(1);
    CHECK( static_cast<int>(formula.value()) == 2 );
    CHECK( b_event.value() == 2);

    tree->LoadTree(2);
    b_event.setEntry(2);
    CHECK( static_cast<int>(formula.value()) == 3 );
    CHECK( b_event.value() == 3);
  }

  SECTION("Formula and Event") {
    BranchManager bmgr;
    bmgr.setTree(tree.get());

    Event event;
    event.setupBranches(bmgr);

    Formula formula = mgr.book("event");
    mgr.setupBranch(tree.get());

    tree->LoadTree(0);
    bmgr.setEntry(0);
    CHECK( static_cast<int>(formula.value()) == 1 );
    CHECK( event.eventID().event() == 1u );
    CHECK( static_cast<int>(formula.value()) == 1 );
    CHECK( event.eventID().lumi() == 1 );
    CHECK( static_cast<int>(formula.value()) == 1 );
    CHECK( event.eventID().run() == 1 );
    CHECK( event.taus().size() == 4 );

    tree->LoadTree(1);
    bmgr.setEntry(1);
    CHECK( static_cast<int>(formula.value()) == 2 );
    CHECK( event.eventID().event() == 2);
    CHECK( event.taus().size() == 1 );

    tree->LoadTree(2);
    bmgr.setEntry(2);
    CHECK( static_cast<int>(formula.value()) == 3 );
    CHECK( event.eventID().event() == 3);
    CHECK( event.taus().size() == 2 );
  }

}

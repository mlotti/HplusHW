#include "catch.hpp"

#include "test_createTree.h"

#include "Framework/interface/BranchManager.h"
#include "DataFormat/interface/EventID.h"

TEST_CASE("EventID", "[DataFormat]") {
  std::unique_ptr<TTree> tree = createRealisticTree();

  BranchManager mgr;
  mgr.setTree(tree.get());

  EventID eventID;
  eventID.setupBranches(mgr);

  SECTION("EventID") {
    mgr.setEntry(0);
    CHECK( eventID.event() == 1u );
    CHECK( eventID.lumi() == 1 );
    CHECK( eventID.run() == 1 );

    mgr.setEntry(1);
    CHECK( eventID.event() == 2u );
    CHECK( eventID.lumi() == 1 );
    CHECK( eventID.run() == 1 );

    mgr.setEntry(2);
    CHECK( eventID.event() == 3u );
    CHECK( eventID.lumi() == 2 );
    CHECK( eventID.run() == 1 );
  }
}

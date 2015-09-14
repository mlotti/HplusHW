#include "catch.hpp"

#include "test_createTree.h"

#include "Framework/interface/BranchManager.h"
#include "DataFormat/interface/MET.h"

TEST_CASE("MET", "[DataFormat]") {
  SECTION("Default prefix") {
    std::unique_ptr<TTree> tree = createRealisticTree();

    BranchManager mgr;
    mgr.setTree(tree.get());

    MET met("MET_Type1");
    met.setupBranches(mgr);

    SECTION("MET getters") {
      mgr.setEntry(0);
      CHECK( met.et() == Approx(50.0) );
      CHECK( met.phi() == Approx(0.1) );

      mgr.setEntry(2);
      CHECK( met.et() == Approx(200.0) );
      CHECK( met.phi() == Approx(-2.4) );

      mgr.setEntry(1);
      CHECK( met.et() == Approx(45.0) );
      CHECK( met.phi() == Approx(3.1) );
    }

    SECTION("MET p2 conversions") {
      mgr.setEntry(0);

      auto p2 = met.p2();
      CHECK( p2.x() == Approx(49.75021) );
      CHECK( p2.y() == Approx(4.99167) );
    }
  }

  SECTION("Systematic variations") {
    std::unique_ptr<TTree> tree = createRealisticTree();

    BranchManager mgr;
    mgr.setTree(tree.get());

    MET met("MET_Type1");
    met.setEnergySystematicsVariation("systVarTESUp");
    met.setupBranches(mgr);

    SECTION("MET getters") {
      mgr.setEntry(0);
      CHECK( met.et() == Approx(60.0) );
      CHECK( met.phi() == Approx(0.7) );

      mgr.setEntry(2);
      CHECK( met.et() == Approx(150.0) );
      CHECK( met.phi() == Approx(1.5) );

      mgr.setEntry(1);
      CHECK( met.et() == Approx(30.0) );
      CHECK( met.phi() == Approx(-2.6) );
    }
  }
}

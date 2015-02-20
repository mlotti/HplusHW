#include "catch.hpp"

#include "test_createTree.h"

#include "Framework/interface/BranchManager.h"
#include "DataFormat/interface/Particle.h"

TEST_CASE("Particle", "[DataFormat]") {
  std::unique_ptr<TTree> tree = createRealisticTree();

  BranchManager mgr;
  mgr.setTree(tree.get());

  ParticleCollection<float> coll("Taus");
  coll.setupBranches(mgr);

  SECTION("ParticleCollection") {
    mgr.setEntry(0);
    REQUIRE( coll.size() == 4 );

    mgr.setEntry(1);
    REQUIRE( coll.size() == 1 );

    mgr.setEntry(2);
    REQUIRE( coll.size() == 2 );
  }

  SECTION("Particle getters") {
    mgr.setEntry(0);
    auto p = coll[0];
    CHECK( p.pt()  == 50.f );
    CHECK( p.eta() == 0.1f );
    CHECK( p.phi() == -2.9f );
    CHECK( p.e()   == 60.f );

    p = coll[2];
    CHECK( p.pt()  == 10.f );
    CHECK( p.eta() == 1.7f );
    CHECK( p.phi() == 1.f );
    CHECK( p.e()   == 40.f );

    mgr.setEntry(2);
    p = coll[1];
    CHECK( p.pt()  == 17.f );
    CHECK( p.eta() == 1.5f );
    CHECK( p.phi() == -1.2f );
    CHECK( p.e()   == 20.f );
  }

  SECTION("Particle p4 conversions") {
    mgr.setEntry(2);
    auto p = coll[1];
    auto polarP4 = p.polarP4();
    CHECK( polarP4.pt()  == 17.f );
    CHECK( polarP4.eta() == 1.5f );
    CHECK( polarP4.phi() == -1.2f );
    CHECK( polarP4.e()   == 20.f );

    auto p4 = p.p4();
    CHECK( p4.px() == Approx(6.16008f) );
    CHECK( p4.py() == Approx(-15.84466f) );
    CHECK( p4.pz() == Approx(36.19775f) );
    CHECK( p4.e() == 20.f );
  }
}

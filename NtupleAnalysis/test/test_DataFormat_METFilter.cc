#include "catch.hpp"

#include "test_createTree.h"

#include "Framework/interface/BranchManager.h"
#include <Framework/interface/Exception.h>
#include "DataFormat/interface/METFilter.h"

#include <algorithm>
#include <vector>
#include <string>

TEST_CASE("METFilter", "[DataFormat]") {
  SECTION("Valid discriminators") {
    std::vector<std::string> v = {"CSCTightHaloFilter", "eeBadScFilter", "goodVertices"};
    METFilter dummy;
    REQUIRE_NOTHROW( dummy.checkDiscriminatorValidity(v) );
    for (auto p: v) {
      REQUIRE_NOTHROW( dummy.checkDiscriminatorValidity(p) );
    }
  }

  SECTION("Empty discriminators") {
    METFilter dummy;
    REQUIRE_THROWS_AS( dummy.checkDiscriminatorValidity(std::string()), hplus::Exception );
    std::vector<std::string> v = {};
    REQUIRE_NOTHROW( dummy.checkDiscriminatorValidity(v) );
  }

  SECTION("Invalid discriminator") {
    METFilter dummy;
    REQUIRE_THROWS_AS( dummy.checkDiscriminatorValidity("doesnotexist"), hplus::Exception );
    std::vector<std::string> v = {"doesnotexist"};
    REQUIRE_THROWS_AS( dummy.checkDiscriminatorValidity(v), hplus::Exception );
  }

}

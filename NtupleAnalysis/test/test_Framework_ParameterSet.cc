#include "catch.hpp"

#include "Framework/interface/ParameterSet.h"

TEST_CASE("ParameterSet", "[Framework]") {
  boost::property_tree::ptree config;
  config.put("TauSelection.systematicVariation", "systVarTESUp");
  config.put("TauSelection.ptCut", 40.);
  config.put("TauSelection.minProngs", 3);

  boost::property_tree::ptree discrs;
  boost::property_tree::ptree child;
  child.put("", "discriminator1");
  discrs.push_back(std::make_pair("", child));
  child.put("", "discriminator2");
  discrs.push_back(std::make_pair("", child));
  child.put("", "discriminator3");
  discrs.push_back(std::make_pair("", child));

  config.add_child("TauSelection.discriminators", discrs);

  ParameterSet pset(config);

  SECTION("Scalar types") {
    CHECK( pset.getParameter<int>("TauSelection.minProngs") == 3 );
    CHECK( pset.getParameter<double>("TauSelection.ptCut") == 40. );
    CHECK( pset.getParameter<std::string>("TauSelection.systematicVariation") == "systVarTESUp" );
  }

  SECTION("Non-existing parameters") {
    REQUIRE_THROWS_AS( pset.getParameter<int>("foo"), std::runtime_error);
  }

  SECTION("Type conversions") {
    CHECK( pset.getParameter<std::string>("TauSelection.minProngs") == "3" );
    CHECK( pset.getParameter<double>("TauSelection.minProngs") == 3.0 );
  }

  SECTION("Wrong type") {
    REQUIRE_THROWS_AS( pset.getParameter<int>("TauSelection.systematicVariation"), std::runtime_error );
  }

  SECTION("Optional") {
    boost::optional<int> t1 = pset.getParameterOptional<int>("TauSelection.minProngs");
    REQUIRE( static_cast<bool>(t1) == true );
    CHECK( *t1 == 3 );

    boost::optional<std::string> t2 = pset.getParameterOptional<std::string>("foo");
    CHECK( static_cast<bool>(t2) == false );
  }

}


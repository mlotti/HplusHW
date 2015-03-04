#include "catch.hpp"

#include "Framework/interface/ParameterSet.h"

TEST_CASE("ParameterSet", "[Framework]") {
  SECTION("string argument") {
    std::string config = "{\n";
    config += "  \"TauSelection\": {\n";
    config += "    \"systematicVariation\": \"systVarTESUp\",\n";
    config += "    \"ptCut\": 40.0,\n";
    config += "    \"minProngs\": 3,\n";
    config += "    \"discriminators\": [\n";
    config += "      \"discriminator1\",\n";
    config += "      \"discriminator2\",\n";
    config += "      \"discriminator3\"\n";
    config += "    ],\n";
    config += "    \"intvector\": [\n";
    config += "       1,2,42\n";
    config += "    ],\n";
    config += "    \"floatvector\": [\n";
    config += "       -2.0, 0.5, 3.14159\n";
    config += "    ],\n";
    config += "    \"psetvector\": [\n";
    config += "       {\"foo\": 1},\n";
    config += "       {\"foo\": 2},\n";
    config += "       {\"foo\": 3},\n";
    config += "       {\"foo\": 4}\n";
    config += "    ]\n";
    config += "  }\n";
    config += "}\n";

    ParameterSet pset(config);

    SECTION("Get parameters") {
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

    SECTION("Vector parameters") {
      auto discrs = pset.getParameter<std::vector<std::string> >("TauSelection.discriminators");
      REQUIRE( discrs.size() == 3 );
      CHECK( discrs[0] == "discriminator1" );
      CHECK( discrs[1] == "discriminator2" );
      CHECK( discrs[2] == "discriminator3" );

      auto ints = pset.getParameter<std::vector<int>>("TauSelection.intvector");
      REQUIRE( ints.size() == 3 );
      CHECK( ints[0] == 1 );
      CHECK( ints[1] == 2 );
      CHECK( ints[2] == 42 );

      auto doubles = pset.getParameter<std::vector<double>>("TauSelection.floatvector");
      REQUIRE( doubles.size() == 3 );
      CHECK( doubles[0] == -2.0 );
      CHECK( doubles[1] == 0.5 );
      CHECK( doubles[2] == 3.14159 );
    }

    SECTION("ParameterSet parameters") {
      ParameterSet tau = pset.getParameter<ParameterSet>("TauSelection");

      CHECK( tau.getParameter<int>("minProngs") == 3 );
      CHECK( tau.getParameter<double>("ptCut") == 40. );
      CHECK( tau.getParameter<std::string>("systematicVariation") == "systVarTESUp" );
    }

    SECTION("Vector<ParameterSet> parameters") {
      std::vector<ParameterSet> psets = pset.getParameter<std::vector<ParameterSet> >("TauSelection.psetvector");

      REQUIRE( psets.size() == 4 );
      CHECK( psets[0].getParameter<int>("foo") == 1 );
      CHECK( psets[1].getParameter<int>("foo") == 2 );
      CHECK( psets[2].getParameter<int>("foo") == 3 );
      CHECK( psets[3].getParameter<int>("foo") == 4 );
    }
  }


  SECTION("property_tree argument") {
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

    CHECK( pset.getParameter<int>("TauSelection.minProngs") == 3 );
    CHECK( pset.getParameter<double>("TauSelection.ptCut") == 40. );
    CHECK( pset.getParameter<std::string>("TauSelection.systematicVariation") == "systVarTESUp" );
  }

}


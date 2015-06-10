#include "catch.hpp"

#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/Exception.h"

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

    SECTION("Optional") {
      boost::optional<int> t1 = pset.getParameterOptional<int>("TauSelection.minProngs");
      REQUIRE( static_cast<bool>(t1) == true );
      CHECK( *t1 == 3 );

      boost::optional<std::string> t2 = pset.getParameterOptional<std::string>("foo");
      CHECK( static_cast<bool>(t2) == false );


      boost::optional<std::vector<std::string> > t3 = pset.getParameterOptional<std::vector<std::string > >("TauSelection.discriminators");
      REQUIRE( static_cast<bool>(t3) == true);
      REQUIRE( t3->size() == 3 );
      CHECK( (*t3)[0] == "discriminator1" );
      CHECK( (*t3)[1] == "discriminator2" );
      CHECK( (*t3)[2] == "discriminator3" );

      boost::optional<std::vector<int> > t4 = pset.getParameterOptional<std::vector<int> >("foo");
      CHECK( static_cast<bool>(t4) == false );


      boost::optional<ParameterSet> t5 = pset.getParameterOptional<ParameterSet>("TauSelection");
      REQUIRE( static_cast<bool>(t5) == true );
      CHECK( t5->getParameter<int>("minProngs") == 3);

      boost::optional<ParameterSet> t6 = pset.getParameterOptional<ParameterSet>("foo");
      CHECK( static_cast<bool>(t6) == false );


      boost::optional<std::vector<ParameterSet> > t7 = pset.getParameterOptional<std::vector<ParameterSet> >("TauSelection.psetvector");
      REQUIRE( static_cast<bool>(t7) == true );
      REQUIRE( t7->size() == 4 );
      CHECK( (*t7)[0].getParameter<int>("foo") == 1 );
      CHECK( (*t7)[1].getParameter<int>("foo") == 2 );
      CHECK( (*t7)[2].getParameter<int>("foo") == 3 );
      CHECK( (*t7)[3].getParameter<int>("foo") == 4 );
    }

    SECTION("Default value") {
      CHECK( pset.getParameter<int>("foo", 3) == 3 );
      CHECK( pset.getParameter<double>("foo", 6.5) == 6.5 );
      CHECK( pset.getParameter<int>("foo", 6.5) == 6 );

      auto vec = pset.getParameter<std::vector<int> >("vectest", std::vector<int>{1, 20, 500, 1000});
      REQUIRE( vec.size() == 4 );
      CHECK( vec[0] == 1 );
      CHECK( vec[1] == 20 );
      CHECK( vec[2] == 500 );
      CHECK( vec[3] == 1000 );

      auto ps = pset.getParameter<ParameterSet>("foo", ParameterSet("{\"bar\": 10}"));
      CHECK( ps.getParameter<int>("bar") == 10 );

      auto vecps = pset.getParameter<std::vector<ParameterSet> >("vecpset",
                     std::vector<ParameterSet>{
                       ParameterSet("{\"plop\": 1}"),
                       ParameterSet("{\"plop\": 2}"),
                       ParameterSet("{\"plop\": 3}"),
                       ParameterSet("{\"plop\": 4}"),
                       ParameterSet("{\"plop\": 5}")
                     });
      REQUIRE( vecps.size() == 5 );
      CHECK( vecps[0].getParameter<int>("plop") == 1 );
      CHECK( vecps[1].getParameter<int>("plop") == 2 );
      CHECK( vecps[2].getParameter<int>("plop") == 3 );
      CHECK( vecps[3].getParameter<int>("plop") == 4 );
      CHECK( vecps[4].getParameter<int>("plop") == 5 );
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

  SECTION("Deliver isMC bit") {
    ParameterSet pset("{}");
    REQUIRE_THROWS_AS( pset.isMC(), hplus::Exception );

    pset = ParameterSet("{}", true);
    CHECK( pset.isMC() == true);

    pset = ParameterSet("{}", false);
    CHECK( pset.isMC() == false);
  }
}


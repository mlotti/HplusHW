// -*- c++ -*-
#include "catch.hpp"

#include "Tools/interface/DirectionalCut.h"
#include "Framework/interface/Exception.h"
#include "Framework/interface/ParameterSet.h"

#include "test_createTree.h"

#include <string>
#include <iostream>

TEST_CASE("DirectionalCut", "[Tools]") {
  boost::property_tree::ptree tmp = getMinimalConfig();
  tmp.put("testeq1Value", 3);
  tmp.put("testeq1Direction", "GEQ");
  tmp.put("testeq2Value", 3);
  tmp.put("testeq2Direction", "==");
  tmp.put("testneq1Value", 3);
  tmp.put("testneq1Direction", "NEQ");
  tmp.put("testneq2Value", 3);
  tmp.put("testneq2Direction", "!=");
  tmp.put("testgt1Value", 3);
  tmp.put("testgt1Direction", "GT");
  tmp.put("testgt2Value", 3);
  tmp.put("testgt2Direction", ">");
  tmp.put("testgeq1Value", 3);
  tmp.put("testgeq1Direction", "GEQ");
  tmp.put("testgeq2Value", 3);
  tmp.put("testgeq2Direction", ">=");
  tmp.put("testlt1Value", 3);
  tmp.put("testlt1Direction", "LT");
  tmp.put("testlt2Value", 3);
  tmp.put("testlt2Direction", "<");
  tmp.put("testleq1Value", 3);
  tmp.put("testleq1Direction", "LEQ");
  tmp.put("testleq2Value", 3);
  tmp.put("testleq2Direction", "<=");
  tmp.put("incomplete1Value", 3);
  tmp.put("incomplete2Direction", "EQ");
  tmp.put("unknownValue", 3);
  tmp.put("unknownDirection", "dummy");
  tmp.put("type1Value", 3);
  tmp.put("type1Direction", "EQ");
  tmp.put("type2Value", 3.0);
  tmp.put("type2Direction", "EQ");
  tmp.put("type3Value", -3);
  tmp.put("type3Direction", "EQ");
  tmp.put("type4Value", true);
  tmp.put("type4Direction", "EQ");
  ParameterSet pset(tmp, true);

  SECTION("initialization") {
    REQUIRE_NOTHROW( DirectionalCut<int> d1(pset, "testgeq1") );
    REQUIRE_THROWS_AS( DirectionalCut<int> d1(pset, "unknown"), hplus::Exception);
    REQUIRE_THROWS_AS( DirectionalCut<int> d1(pset, "incomplete1"), std::runtime_error);
    REQUIRE_THROWS_AS( DirectionalCut<int> d1(pset, "incomplete2"), std::runtime_error);
  }
  SECTION("template") {
    DirectionalCut<int> d1(pset, "type1");
    CHECK( d1.passedCut(2) == false );
    CHECK( d1.passedCut(3) == true );
    DirectionalCut<float> d2(pset, "type2");
    CHECK( d2.passedCut(2.0) == false );
    CHECK( d2.passedCut(3.0) == true );
    DirectionalCut<int> d3(pset, "type3");
    CHECK( d3.passedCut(2) == false );
    CHECK( d3.passedCut(-3) == true );
    DirectionalCut<bool> d4(pset, "type4");
    CHECK( d4.passedCut(false) == false );
    CHECK( d4.passedCut(true) == true );
  }
  SECTION("equal to") {
    DirectionalCut<int> d1(pset, "testeq1");
    CHECK( d1.passedCut(2) == false );
    CHECK( d1.passedCut(3) == true );
    DirectionalCut<int> d2(pset, "testeq2");
    CHECK( d2.passedCut(2) == false );
    CHECK( d2.passedCut(3) == true );
  }
  SECTION("not equal to") {
    DirectionalCut<int> d1(pset, "testneq1");
    CHECK( d1.passedCut(3) == false );
    CHECK( d1.passedCut(2) == true );
    DirectionalCut<int> d2(pset, "testneq2");
    CHECK( d2.passedCut(3) == false );
    CHECK( d2.passedCut(2) == true );
  }
  SECTION("greater than") {
    DirectionalCut<int> d1(pset, "testgt1");
    CHECK( d1.passedCut(2) == false );
    CHECK( d1.passedCut(3) == false );
    CHECK( d1.passedCut(4) == true );
    DirectionalCut<int> d2(pset, "testgt2");
    CHECK( d2.passedCut(2) == false );
    CHECK( d2.passedCut(3) == false );
    CHECK( d2.passedCut(4) == true );
  }
  SECTION("greater than or equal to") {
    DirectionalCut<int> d1(pset, "testgeq1");
    CHECK( d1.passedCut(2) == false );
    CHECK( d1.passedCut(3) == true );
    CHECK( d1.passedCut(4) == true );
    DirectionalCut<int> d2(pset, "testgeq2");
    CHECK( d2.passedCut(2) == false );
    CHECK( d2.passedCut(3) == true );
    CHECK( d2.passedCut(4) == true );
  }
  SECTION("less than") {
    DirectionalCut<int> d1(pset, "testlt1");
    CHECK( d1.passedCut(4) == false );
    CHECK( d1.passedCut(3) == false );
    CHECK( d1.passedCut(2) == true );
    DirectionalCut<int> d2(pset, "testlt2");
    CHECK( d2.passedCut(4) == false );
    CHECK( d2.passedCut(3) == false );
    CHECK( d2.passedCut(2) == true );
  }
  SECTION("less than or equal to") {
    DirectionalCut<int> d1(pset, "testleq1");
    CHECK( d1.passedCut(4) == false );
    CHECK( d1.passedCut(3) == true );
    CHECK( d1.passedCut(2) == true );
    DirectionalCut<int> d2(pset, "testleq2");
    CHECK( d2.passedCut(4) == false );
    CHECK( d2.passedCut(3) == true );
    CHECK( d2.passedCut(2) == true );
  }
  
}
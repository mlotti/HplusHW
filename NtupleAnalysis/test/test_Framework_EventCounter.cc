#include "catch.hpp"

#include "Framework/interface/EventWeight.h"
#include "Framework/interface/EventCounter.h"

#include "TDirectory.h"
#include "TH1.h"

#include <iostream>

TEST_CASE("EventCounter works", "[Framework]") {
  EventWeight weight;
  EventCounter ec(weight);

  SECTION("Serialization of empty EventCounter") {
    TDirectory dir("rootdir", "rootdir");
    ec.setOutput(&dir);
    ec.serialize();
    REQUIRE( dir.Get("counters") );
    REQUIRE( dir.Get("counters/weighted") );
    TH1 *h = nullptr;
    dir.GetObject("counters/counter", h);
    CHECK( !h );
    dir.GetObject("counters/weighted/counter", h);
    CHECK( !h );
  }

  Count c1 = ec.addCounter("count1");
  Count c2 = ec.addCounter("count2");
  Count c3 = ec.addCounter("count3");

  SECTION("Serialization") {
    TDirectory dir("rootdir", "rootdir");
    ec.setOutput(&dir);
    ec.serialize();
    TH1 *h = nullptr;
    dir.GetObject("counters/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetXaxis()->GetBinLabel(1) == std::string("count1") );
    CHECK( h->GetXaxis()->GetBinLabel(2) == std::string("count2") );
    CHECK( h->GetXaxis()->GetBinLabel(3) == std::string("count3") );
    CHECK( h->GetBinContent(0) == 0 );
    CHECK( h->GetBinContent(1) == 0 );
    CHECK( h->GetBinContent(2) == 0 );
    CHECK( h->GetBinContent(3) == 0 );
    CHECK( h->GetBinContent(4) == 0 );

    dir.GetObject("counters/weighted/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetXaxis()->GetBinLabel(1) == std::string("count1") );
    CHECK( h->GetXaxis()->GetBinLabel(2) == std::string("count2") );
    CHECK( h->GetXaxis()->GetBinLabel(3) == std::string("count3") );
    CHECK( h->GetBinContent(0) == 0 );
    CHECK( h->GetBinContent(1) == 0 );
    CHECK( h->GetBinContent(2) == 0 );
    CHECK( h->GetBinContent(3) == 0 );
    CHECK( h->GetBinContent(4) == 0 );

    REQUIRE_THROWS_AS( ec.addCounter("count4"), std::logic_error );
  }

  SECTION("Single count") {
    c1.increment();
    c1.increment();
    c1.increment();
    c1.increment();

    TDirectory dir("rootdir", "rootdir");
    ec.setOutput(&dir);
    ec.serialize();
    TH1 *h = nullptr;
    dir.GetObject("counters/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetBinContent(0) == 0 );
    CHECK( h->GetBinContent(1) == 4 );
    CHECK( h->GetBinContent(2) == 0 );
    CHECK( h->GetBinContent(3) == 0 );
    CHECK( h->GetBinContent(4) == 0 );

    dir.GetObject("counters/weighted/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetBinContent(0) == 0 );
    CHECK( h->GetBinContent(1) == 4 );
    CHECK( h->GetBinContent(2) == 0 );
    CHECK( h->GetBinContent(3) == 0 );
    CHECK( h->GetBinContent(4) == 0 );
  }

  SECTION("Many counts") {
    c1.increment();
    c2.increment();

    c1.increment();
    c2.increment();
    c3.increment();

    c1.increment();
    c2.increment();

    c1.increment();

    TDirectory dir("rootdir", "rootdir");
    ec.setOutput(&dir);
    ec.serialize();
    TH1 *h = nullptr;
    dir.GetObject("counters/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetBinContent(0) == 0 );
    CHECK( h->GetBinContent(1) == 4 );
    CHECK( h->GetBinContent(2) == 3 );
    CHECK( h->GetBinContent(3) == 1 );
    CHECK( h->GetBinContent(4) == 0 );

    dir.GetObject("counters/weighted/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetBinContent(0) == 0 );
    CHECK( h->GetBinContent(1) == 4 );
    CHECK( h->GetBinContent(2) == 3 );
    CHECK( h->GetBinContent(3) == 1 );
    CHECK( h->GetBinContent(4) == 0 );
  }

  SECTION("Weighted counts") {
    c1.increment();
    c2.increment();

    c1.increment();
    c2.increment();
    weight.multiplyWeight(0.5);
    c3.increment();

    weight.beginEvent();
    c1.increment();
    weight.multiplyWeight(0.5);
    c2.increment();

    weight.beginEvent();
    c1.increment();
    weight.multiplyWeight(0.25);
    c2.increment();
    weight.multiplyWeight(2);
    c3.increment();

    TDirectory dir("rootdir", "rootdir");
    ec.setOutput(&dir);
    ec.serialize();
    TH1 *h = nullptr;
    dir.GetObject("counters/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetBinContent(0) == 0 );
    CHECK( h->GetBinContent(1) == 4 );
    CHECK( h->GetBinContent(2) == 4 );
    CHECK( h->GetBinContent(3) == 2 );
    CHECK( h->GetBinContent(4) == 0 );

    dir.GetObject("counters/weighted/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetBinContent(0) == 0 );
    CHECK( h->GetBinContent(1) == 4 );
    CHECK( h->GetBinContent(2) == 2.75 );
    CHECK( h->GetBinContent(3) == 1.0 );
    CHECK( h->GetBinContent(4) == 0 );
  }


  Count sub1 = ec.addSubCounter("sub", "count1");
  Count sub2 = ec.addSubCounter("sub", "count2");
  Count suc1 = ec.addSubCounter("suc", "count1");
  Count suc2 = ec.addSubCounter("suc", "count2");
  Count suc3 = ec.addSubCounter("suc", "count3");

  SECTION("Serialization of subcounters") {
    TDirectory dir("rootdir", "rootdir");
    ec.setOutput(&dir);
    ec.serialize();
    TH1 *h = nullptr;
    dir.GetObject("counters/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );

    dir.GetObject("counters/weighted/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );

    dir.GetObject("counters/sub", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 2 );
    CHECK( h->GetXaxis()->GetBinLabel(1) == std::string("count1") );
    CHECK( h->GetXaxis()->GetBinLabel(2) == std::string("count2") );
    CHECK( h->GetBinContent(0) == 0 );
    CHECK( h->GetBinContent(1) == 0 );
    CHECK( h->GetBinContent(2) == 0 );
    CHECK( h->GetBinContent(3) == 0 );

    dir.GetObject("counters/suc", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetXaxis()->GetBinLabel(1) == std::string("count1") );
    CHECK( h->GetXaxis()->GetBinLabel(2) == std::string("count2") );
    CHECK( h->GetXaxis()->GetBinLabel(3) == std::string("count3") );
    CHECK( h->GetBinContent(0) == 0 );
    CHECK( h->GetBinContent(1) == 0 );
    CHECK( h->GetBinContent(2) == 0 );
    CHECK( h->GetBinContent(3) == 0 );
    CHECK( h->GetBinContent(4) == 0 );
  }

  SECTION("Counts of subcounters with weights") {
    c1.increment();
    c2.increment();
    sub1.increment();

    c1.increment();
    c2.increment();
    sub1.increment();
    sub2.increment();
    weight.multiplyWeight(0.5);
    c3.increment();
    suc1.increment();
    suc2.increment();

    weight.beginEvent();
    c1.increment();
    weight.multiplyWeight(0.5);
    c2.increment();
    sub1.increment();

    weight.beginEvent();
    c1.increment();
    weight.multiplyWeight(0.25);
    c2.increment();
    sub1.increment();
    weight.multiplyWeight(2);
    c3.increment();
    suc1.increment();
    suc2.increment();
    suc3.increment();

    TDirectory dir("rootdir", "rootdir");
    ec.setOutput(&dir);
    ec.serialize();
    TH1 *h = nullptr;
    dir.GetObject("counters/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetBinContent(0) == 0 );
    CHECK( h->GetBinContent(1) == 4 );
    CHECK( h->GetBinContent(2) == 4 );
    CHECK( h->GetBinContent(3) == 2 );
    CHECK( h->GetBinContent(4) == 0 );

    dir.GetObject("counters/weighted/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetBinContent(0) == 0 );
    CHECK( h->GetBinContent(1) == 4 );
    CHECK( h->GetBinContent(2) == 2.75 );
    CHECK( h->GetBinContent(3) == 1.0 );
    CHECK( h->GetBinContent(4) == 0 );

    dir.GetObject("counters/sub", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 2 );
    CHECK( h->GetBinContent(0) == 0 );
    CHECK( h->GetBinContent(1) == 4 );
    CHECK( h->GetBinContent(2) == 1 );
    CHECK( h->GetBinContent(3) == 0 );

    dir.GetObject("counters/weighted/sub", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 2 );
    CHECK( h->GetBinContent(0) == 0 );
    CHECK( h->GetBinContent(1) == 2.75 );
    CHECK( h->GetBinContent(2) == 1 );
    CHECK( h->GetBinContent(3) == 0 );


    dir.GetObject("counters/suc", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetBinContent(0) == 0 );
    CHECK( h->GetBinContent(1) == 2 );
    CHECK( h->GetBinContent(2) == 2 );
    CHECK( h->GetBinContent(3) == 1 );
    CHECK( h->GetBinContent(4) == 0 );

    dir.GetObject("counters/weighted/suc", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetBinContent(0) == 0 );
    CHECK( h->GetBinContent(1) == 1 );
    CHECK( h->GetBinContent(2) == 1 );
    CHECK( h->GetBinContent(3) == 0.5 );
    CHECK( h->GetBinContent(4) == 0 );

  }
}

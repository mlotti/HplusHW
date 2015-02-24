#include "catch.hpp"

#include "Framework/interface/EventWeight.h"
#include "Framework/interface/HistoWrapper.h"

TEST_CASE("HistoWrapper works", "[Framework]") {
  EventWeight weight;
  HistoWrapper wrapper(weight, "Vital");

  SECTION("Initialization") {
    CHECK( wrapper.getWeight() == 1.0 );
    CHECK( wrapper.isEnabled() );
    CHECK( wrapper.isActive(HistoLevel::kSystematics) );
    CHECK( wrapper.isActive(HistoLevel::kVital) );
    CHECK( !wrapper.isActive(HistoLevel::kInformative) );
    CHECK( !wrapper.isActive(HistoLevel::kDebug) );
  }

  SECTION("1D histograms") {
    TDirectory dir("rootdir", "rootdir");

    WrappedTH1 *th1 = wrapper.makeTH<TH1F>(HistoLevel::kVital, &dir, "name", "title", 100, 0, 100);
    REQUIRE( th1 );
    REQUIRE( th1->isActive() );
    REQUIRE( th1->getHisto() );
    CHECK( std::string(th1->getHisto()->GetName()) == "name" );
    CHECK( std::string(th1->getHisto()->GetTitle()) == "title" );
    CHECK( th1->getHisto()->GetNbinsX() == 100 );
    TAxis *axis = th1->GetXaxis();
    REQUIRE( axis );
    CHECK( axis->GetBinLowEdge(axis->GetFirst()) == 0 );
    CHECK( axis->GetBinUpEdge(axis->GetLast()) == 100 );

    TH1 *tmp = nullptr;
    dir.GetObject("name", tmp);
    CHECK( tmp );
    CHECK( tmp == th1->getHisto() );

    th1->Fill(10);
    CHECK( th1->getHisto()->GetBinContent(10) == 0);
    CHECK( th1->getHisto()->GetBinContent(11) == 1);
    CHECK( th1->getHisto()->GetBinContent(12) == 0);

    th1->Fill(12, 0.5);
    CHECK( th1->getHisto()->GetBinContent(10) == 0);
    CHECK( th1->getHisto()->GetBinContent(11) == 1);
    CHECK( th1->getHisto()->GetBinContent(12) == 0);
    CHECK( th1->getHisto()->GetBinContent(13) == 0.5);
    CHECK( th1->getHisto()->GetBinContent(14) == 0);
  }

  SECTION("2D histograms") {
    TDirectory dir("rootdir", "rootdir");
    WrappedTH2 *th2 = wrapper.makeTH<TH2F>(HistoLevel::kVital, &dir, "name", "title", 100,0,100, 20,-5,5);
    REQUIRE( th2 );
    REQUIRE( th2->isActive() );
    REQUIRE( th2->getHisto() );
    CHECK( std::string(th2->getHisto()->GetName()) == "name" );
    CHECK( std::string(th2->getHisto()->GetTitle()) == "title" );
    CHECK( th2->getHisto()->GetNbinsX() == 100 );
    TAxis *axis = th2->GetXaxis();
    REQUIRE( axis );
    CHECK( axis->GetBinLowEdge(axis->GetFirst()) == 0 );
    CHECK( axis->GetBinUpEdge(axis->GetLast()) == 100 );

    CHECK( th2->getHisto()->GetNbinsY() == 20 );
    axis = th2->getHisto()->GetYaxis();
    CHECK( axis->GetBinLowEdge(axis->GetFirst()) == -5 );
    CHECK( axis->GetBinUpEdge(axis->GetLast()) == 5 );

    TH2 *tmp = nullptr;
    dir.GetObject("name", tmp);
    CHECK( tmp );
    CHECK( tmp == th2->getHisto() );
  }

  SECTION("3D histograms") {
    TDirectory dir("rootdir", "rootdir");
    WrappedTH3 *th3 = wrapper.makeTH<TH3F>(HistoLevel::kVital, &dir, "name", "title", 100,0,100, 20,-5,5, 50,-100,-50);
    REQUIRE( th3 );
    REQUIRE( th3->isActive() );
    REQUIRE( th3->getHisto() );
    CHECK( std::string(th3->getHisto()->GetName()) == "name" );
    CHECK( std::string(th3->getHisto()->GetTitle()) == "title" );
    CHECK( th3->getHisto()->GetNbinsX() == 100 );
    TAxis *axis = th3->GetXaxis();
    REQUIRE( axis );
    CHECK( axis->GetBinLowEdge(axis->GetFirst()) == 0 );
    CHECK( axis->GetBinUpEdge(axis->GetLast()) == 100 );

    CHECK( th3->getHisto()->GetNbinsY() == 20 );
    axis = th3->getHisto()->GetYaxis();
    CHECK( axis->GetBinLowEdge(axis->GetFirst()) == -5 );
    CHECK( axis->GetBinUpEdge(axis->GetLast()) == 5 );

    CHECK( th3->getHisto()->GetNbinsZ() == 50 );
    axis = th3->getHisto()->GetZaxis();
    CHECK( axis->GetBinLowEdge(axis->GetFirst()) == -100 );
    CHECK( axis->GetBinUpEdge(axis->GetLast()) == -50 );

    TH3 *tmp = nullptr;
    dir.GetObject("name", tmp);
    CHECK( tmp );
    CHECK( tmp == th3->getHisto() );
  }

  SECTION("UnfoldedFactorisationHisto") {
    TDirectory dir("rootdir", "rootdir");
    WrappedUnfoldedFactorisationHisto *th2 = wrapper.makeTH<TH2F>(10, HistoLevel::kVital, &dir, "name", "title", 100,0,100);
    REQUIRE( th2 );
    REQUIRE( th2->isActive() );
    REQUIRE( th2->getHisto() );
    CHECK( std::string(th2->getHisto()->GetName()) == "name" );
    CHECK( std::string(th2->getHisto()->GetTitle()) == "title" );
    CHECK( th2->getHisto()->GetNbinsX() == 100 );
    TAxis *axis = th2->GetXaxis();
    REQUIRE( axis );
    CHECK( axis->GetBinLowEdge(axis->GetFirst()) == 0 );
    CHECK( axis->GetBinUpEdge(axis->GetLast()) == 100 );

    CHECK( th2->getHisto()->GetNbinsY() == 10 );
    axis = th2->getHisto()->GetYaxis();
    CHECK( axis->GetBinLowEdge(axis->GetFirst()) == 0 );
    CHECK( axis->GetBinUpEdge(axis->GetLast()) == 10 );

    TH2 *tmp = nullptr;
    dir.GetObject("name", tmp);
    CHECK( tmp );
    CHECK( tmp == th2->getHisto() );
  }

  SECTION("Histo levels") {
    TDirectory dir("rootdir", "rootdir");
    WrappedTH1 *th1 = wrapper.makeTH<TH1F>(HistoLevel::kDebug, &dir, "debug", "title", 100, 0, 100);
    REQUIRE( th1 );
    CHECK( !th1->isActive() );
    CHECK( th1->getHisto() == nullptr );

    th1 = wrapper.makeTH<TH1F>(HistoLevel::kInformative, &dir, "informative", "title", 100, 0, 100);
    REQUIRE( th1 );
    CHECK( !th1->isActive() );
    CHECK( th1->getHisto() == nullptr );

    th1 = wrapper.makeTH<TH1F>(HistoLevel::kVital, &dir, "vital", "title", 100, 0, 100);
    REQUIRE( th1 );
    CHECK( th1->isActive() );
    CHECK( th1->getHisto() );

    th1 = wrapper.makeTH<TH1F>(HistoLevel::kSystematics, &dir, "systematics", "title", 100, 0, 100);
    REQUIRE( th1 );
    CHECK( th1->isActive() );
    CHECK( th1->getHisto() );
  }
}

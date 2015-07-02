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

    th2->Fill(50, 2);
    CHECK( th2->getHisto()->GetBinContent(50, 14) == 0 );
    CHECK( th2->getHisto()->GetBinContent(50, 15) == 0 );
    CHECK( th2->getHisto()->GetBinContent(50, 16) == 0 );
    CHECK( th2->getHisto()->GetBinContent(51, 14) == 0 );
    CHECK( th2->getHisto()->GetBinContent(51, 15) == 1 );
    CHECK( th2->getHisto()->GetBinContent(51, 16) == 0 );
    CHECK( th2->getHisto()->GetBinContent(52, 14) == 0 );
    CHECK( th2->getHisto()->GetBinContent(52, 15) == 0 );
    CHECK( th2->getHisto()->GetBinContent(52, 16) == 0 );
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

    th3->Fill(50, 1.2, -75);
    CHECK( th3->getHisto()->GetBinContent(51, 12, 25) == 0 );
    CHECK( th3->getHisto()->GetBinContent(51, 12, 26) == 0 );
    CHECK( th3->getHisto()->GetBinContent(51, 12, 27) == 0 );
    CHECK( th3->getHisto()->GetBinContent(51, 13, 25) == 0 );
    CHECK( th3->getHisto()->GetBinContent(51, 13, 26) == 1 );
    CHECK( th3->getHisto()->GetBinContent(51, 13, 27) == 0 );
    CHECK( th3->getHisto()->GetBinContent(51, 14, 25) == 0 );
    CHECK( th3->getHisto()->GetBinContent(51, 14, 26) == 0 );
    CHECK( th3->getHisto()->GetBinContent(51, 14, 27) == 0 );
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

  SECTION("1D triplet histograms") {
    TDirectory dir("rootdir", "rootdir");
    TDirectory fakedir("fakedir", "fakedir");
    TDirectory truedir("truedir", "truedir");
    std::vector<TDirectory*> dirs = { &dir, &fakedir, &truedir };

    WrappedTH1Triplet *th1 = wrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, dirs, "name", "title", 100, 0, 100);
    REQUIRE( th1 );
    REQUIRE( th1->isActive() );
    REQUIRE( th1->getInclusiveHisto() );
    REQUIRE( th1->getTrueHisto() );
    REQUIRE( th1->getFalseHisto() );
    CHECK( std::string(th1->getInclusiveHisto()->GetName()) == "name" );
    CHECK( std::string(th1->getInclusiveHisto()->GetTitle()) == "title" );
    CHECK( th1->getInclusiveHisto()->GetNbinsX() == 100 );
    CHECK( std::string(th1->getTrueHisto()->GetName()) == "name" );
    CHECK( std::string(th1->getTrueHisto()->GetTitle()) == "title" );
    CHECK( th1->getTrueHisto()->GetNbinsX() == 100 );
    CHECK( std::string(th1->getFalseHisto()->GetName()) == "name" );
    CHECK( std::string(th1->getFalseHisto()->GetTitle()) == "title" );
    CHECK( th1->getFalseHisto()->GetNbinsX() == 100 );

    th1->Fill(true, 11);
    th1->Fill(false, 12, 0.5);
    CHECK( th1->getInclusiveHisto()->GetBinContent(10) == 0 );
    CHECK( th1->getInclusiveHisto()->GetBinContent(11) == 1 );
    CHECK( th1->getInclusiveHisto()->GetBinContent(12) == Approx(0.5) );
    CHECK( th1->getInclusiveHisto()->GetBinContent(13) == 0 );
    CHECK( th1->getTrueHisto()->GetBinContent(10) == 0 );
    CHECK( th1->getTrueHisto()->GetBinContent(11) == 1 );
    CHECK( th1->getTrueHisto()->GetBinContent(12) == 0 );
    CHECK( th1->getTrueHisto()->GetBinContent(13) == 0 );
    CHECK( th1->getFalseHisto()->GetBinContent(10) == 0 );
    CHECK( th1->getFalseHisto()->GetBinContent(11) == 0 );
    CHECK( th1->getFalseHisto()->GetBinContent(12) == Approx(0.5) );
    CHECK( th1->getFalseHisto()->GetBinContent(13) == 0 );

    WrappedTH1Triplet *th1prime = wrapper.makeTHTriplet<TH1F>(false, HistoLevel::kVital, dirs, "name", "title", 100, 0, 100);
    REQUIRE( th1prime );
    REQUIRE( th1prime->isActive() );
    REQUIRE( th1prime->getInclusiveHisto() );
    REQUIRE( th1prime->getTrueHisto() == nullptr );
    REQUIRE( th1prime->getFalseHisto() );
    th1->Fill(true, 11);
    th1->Fill(false, 12, 0.5);
    CHECK( th1prime->getInclusiveHisto()->GetBinContent(10) == 0 );
    CHECK( th1prime->getInclusiveHisto()->GetBinContent(11) == 1 );
    CHECK( th1prime->getInclusiveHisto()->GetBinContent(12) == Approx(0.5) );
    CHECK( th1prime->getInclusiveHisto()->GetBinContent(13) == 0 );
    CHECK( th1prime->getFalseHisto()->GetBinContent(10) == 0 );
    CHECK( th1prime->getFalseHisto()->GetBinContent(11) == 0 );
    CHECK( th1prime->getFalseHisto()->GetBinContent(12) == Approx(0.5) );
    CHECK( th1prime->getFalseHisto()->GetBinContent(13) == 0 );
    
  }
  
}

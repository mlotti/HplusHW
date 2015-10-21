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
    std::vector<TDirectory*> dirs3 = { &dir, &fakedir, &truedir };
    std::vector<TDirectory*> dirs2 = { &dir, &fakedir };

    WrappedTH1Triplet *th1 = wrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, dirs3, "nametr1", "title", 100, 0, 100);
    REQUIRE( th1 != nullptr );
    REQUIRE( th1->isActive() == true );
    REQUIRE( th1->getInclusiveHisto() != nullptr );
    REQUIRE( th1->getTrueHisto() != nullptr );
    REQUIRE( th1->getFalseHisto() != nullptr );
    CHECK( std::string(th1->getInclusiveHisto()->GetName()) == "nametr1" );
    CHECK( std::string(th1->getInclusiveHisto()->GetTitle()) == "title" );
    CHECK( th1->getInclusiveHisto()->GetNbinsX() == 100 );
    CHECK( std::string(th1->getTrueHisto()->GetName()) == "nametr1" );
    CHECK( std::string(th1->getTrueHisto()->GetTitle()) == "title" );
    CHECK( th1->getTrueHisto()->GetNbinsX() == 100 );
    CHECK( std::string(th1->getFalseHisto()->GetName()) == "nametr1" );
    CHECK( std::string(th1->getFalseHisto()->GetTitle()) == "title" );
    CHECK( th1->getFalseHisto()->GetNbinsX() == 100 );

    th1->Fill(true, 10);
    th1->Fill(false, 11, 0.5);
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

    WrappedTH1Triplet *th1prime = wrapper.makeTHTriplet<TH1F>(false, HistoLevel::kVital, dirs2, "nametr1p", "title", 100, 0, 100);
    REQUIRE( th1prime != nullptr );
    REQUIRE( th1prime->isActive() == true );
    REQUIRE( th1prime->getInclusiveHisto() != nullptr );
    REQUIRE( th1prime->getTrueHisto() == nullptr );
    REQUIRE( th1prime->getFalseHisto() != nullptr );
    th1prime->Fill(true, 10);
    th1prime->Fill(false, 11, 0.5);
    CHECK( th1prime->getInclusiveHisto()->GetBinContent(10) == 0 );
    CHECK( th1prime->getInclusiveHisto()->GetBinContent(11) == 1 );
    CHECK( th1prime->getInclusiveHisto()->GetBinContent(12) == Approx(0.5) );
    CHECK( th1prime->getInclusiveHisto()->GetBinContent(13) == 0 );
    CHECK( th1prime->getFalseHisto()->GetBinContent(10) == 0 );
    CHECK( th1prime->getFalseHisto()->GetBinContent(11) == 0 );
    CHECK( th1prime->getFalseHisto()->GetBinContent(12) == Approx(0.5) );
    CHECK( th1prime->getFalseHisto()->GetBinContent(13) == 0 );
  }

  SECTION("2D triplet histograms") {
    TDirectory dir("rootdir", "rootdir");
    TDirectory fakedir("fakedir", "fakedir");
    TDirectory truedir("truedir", "truedir");
    std::vector<TDirectory*> dirs3 = { &dir, &fakedir, &truedir };
    std::vector<TDirectory*> dirs2 = { &dir, &fakedir };

    WrappedTH2Triplet *th2 = wrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, dirs3, "nametr2", "title", 100, 0, 100, 100, 0, 100);
    REQUIRE( th2 != nullptr );
    REQUIRE( th2->isActive() == true );
    REQUIRE( th2->getInclusiveHisto() != nullptr );
    REQUIRE( th2->getTrueHisto() != nullptr );
    REQUIRE( th2->getFalseHisto() != nullptr );
    CHECK( std::string(th2->getInclusiveHisto()->GetName()) == "nametr2" );
    CHECK( std::string(th2->getInclusiveHisto()->GetTitle()) == "title" );
    CHECK( th2->getInclusiveHisto()->GetNbinsX() == 100 );
    CHECK( th2->getInclusiveHisto()->GetNbinsY() == 100 );
    CHECK( std::string(th2->getTrueHisto()->GetName()) == "nametr2" );
    CHECK( std::string(th2->getTrueHisto()->GetTitle()) == "title" );
    CHECK( th2->getTrueHisto()->GetNbinsX() == 100 );
    CHECK( th2->getTrueHisto()->GetNbinsY() == 100 );
    CHECK( std::string(th2->getFalseHisto()->GetName()) == "nametr2" );
    CHECK( std::string(th2->getFalseHisto()->GetTitle()) == "title" );
    CHECK( th2->getFalseHisto()->GetNbinsX() == 100 );
    CHECK( th2->getFalseHisto()->GetNbinsY() == 100 );

    th2->Fill(true, 10, 4);
    th2->Fill(false, 11, 5, 0.5);
    CHECK( th2->getInclusiveHisto()->GetBinContent(10,4) == 0 );
    CHECK( th2->getInclusiveHisto()->GetBinContent(11,5) == 1 );
    CHECK( th2->getInclusiveHisto()->GetBinContent(12,6) == Approx(0.5) );
    CHECK( th2->getInclusiveHisto()->GetBinContent(13,7) == 0 );
    CHECK( th2->getTrueHisto()->GetBinContent(10,4) == 0 );
    CHECK( th2->getTrueHisto()->GetBinContent(11,5) == 1 );
    CHECK( th2->getTrueHisto()->GetBinContent(12,6) == 0 );
    CHECK( th2->getTrueHisto()->GetBinContent(13,7) == 0 );
    CHECK( th2->getFalseHisto()->GetBinContent(10,4) == 0 );
    CHECK( th2->getFalseHisto()->GetBinContent(11,5) == 0 );
    CHECK( th2->getFalseHisto()->GetBinContent(12,6) == Approx(0.5) );
    CHECK( th2->getFalseHisto()->GetBinContent(13,7) == 0 );

    WrappedTH2Triplet *th2prime = wrapper.makeTHTriplet<TH2F>(false, HistoLevel::kVital, dirs2, "nametr2p", "title", 100, 0, 100, 100, 0, 100);
    REQUIRE( th2prime != nullptr );
    REQUIRE( th2prime->isActive() == true );
    REQUIRE( th2prime->getInclusiveHisto() != nullptr );
    REQUIRE( th2prime->getTrueHisto() == nullptr );
    REQUIRE( th2prime->getFalseHisto() != nullptr );
    th2prime->Fill(true, 10, 4);
    th2prime->Fill(false, 11,5, 0.5);
    CHECK( th2prime->getInclusiveHisto()->GetBinContent(10,4) == 0 );
    CHECK( th2prime->getInclusiveHisto()->GetBinContent(11,5) == 1 );
    CHECK( th2prime->getInclusiveHisto()->GetBinContent(12,6) == Approx(0.5) );
    CHECK( th2prime->getInclusiveHisto()->GetBinContent(13,7) == 0 );
    CHECK( th2prime->getFalseHisto()->GetBinContent(10,4) == 0 );
    CHECK( th2prime->getFalseHisto()->GetBinContent(11,5) == 0 );
    CHECK( th2prime->getFalseHisto()->GetBinContent(12,6) == Approx(0.5) );
    CHECK( th2prime->getFalseHisto()->GetBinContent(13,7) == 0 );
  }

  SECTION("3D triplet histograms") {
    TDirectory dir("rootdir", "rootdir");
    TDirectory fakedir("fakedir", "fakedir");
    TDirectory truedir("truedir", "truedir");
    std::vector<TDirectory*> dirs3 = { &dir, &fakedir, &truedir };
    std::vector<TDirectory*> dirs2 = { &dir, &fakedir };

    WrappedTH3Triplet *th3 = wrapper.makeTHTriplet<TH3F>(true, HistoLevel::kVital, dirs3, "nametr3", "title", 100, 0, 100, 10, 0, 10, 10, 0, 10);
    REQUIRE( th3 != nullptr );
    REQUIRE( th3->isActive() == true );
    REQUIRE( th3->getInclusiveHisto() != nullptr );
    REQUIRE( th3->getTrueHisto() != nullptr );
    REQUIRE( th3->getFalseHisto() != nullptr );
    CHECK( std::string(th3->getInclusiveHisto()->GetName()) == "nametr3" );
    CHECK( std::string(th3->getInclusiveHisto()->GetTitle()) == "title" );
    CHECK( th3->getInclusiveHisto()->GetNbinsX() == 100 );
    CHECK( th3->getInclusiveHisto()->GetNbinsY() == 10 );
    CHECK( th3->getInclusiveHisto()->GetNbinsZ() == 10 );
    CHECK( std::string(th3->getTrueHisto()->GetName()) == "nametr3" );
    CHECK( std::string(th3->getTrueHisto()->GetTitle()) == "title" );
    CHECK( th3->getTrueHisto()->GetNbinsX() == 100 );
    CHECK( th3->getTrueHisto()->GetNbinsY() == 10 );
    CHECK( th3->getTrueHisto()->GetNbinsZ() == 10 );
    CHECK( std::string(th3->getFalseHisto()->GetName()) == "nametr3" );
    CHECK( std::string(th3->getFalseHisto()->GetTitle()) == "title" );
    CHECK( th3->getFalseHisto()->GetNbinsX() == 100 );
    CHECK( th3->getFalseHisto()->GetNbinsY() == 10 );
    CHECK( th3->getFalseHisto()->GetNbinsZ() == 10 );

    th3->Fill(true, 10, 4, 3);
    th3->Fill(false, 11, 5, 4, 0.5);
    CHECK( th3->getInclusiveHisto()->GetBinContent(10,4,3) == 0 );
    CHECK( th3->getInclusiveHisto()->GetBinContent(11,5,4) == 1 );
    CHECK( th3->getInclusiveHisto()->GetBinContent(12,6,5) == Approx(0.5) );
    CHECK( th3->getInclusiveHisto()->GetBinContent(13,7,6) == 0 );
    CHECK( th3->getTrueHisto()->GetBinContent(10,4,3) == 0 );
    CHECK( th3->getTrueHisto()->GetBinContent(11,5,4) == 1 );
    CHECK( th3->getTrueHisto()->GetBinContent(12,6,5) == 0 );
    CHECK( th3->getTrueHisto()->GetBinContent(13,7,6) == 0 );
    CHECK( th3->getFalseHisto()->GetBinContent(10,4,3) == 0 );
    CHECK( th3->getFalseHisto()->GetBinContent(11,5,4) == 0 );
    CHECK( th3->getFalseHisto()->GetBinContent(12,6,5) == Approx(0.5) );
    CHECK( th3->getFalseHisto()->GetBinContent(13,7,6) == 0 );

    WrappedTH3Triplet *th3prime = wrapper.makeTHTriplet<TH3F>(false, HistoLevel::kVital, dirs2, "nametr3p", "title", 100, 0, 100, 10, 0, 10, 10, 0, 10);
    REQUIRE( th3prime != nullptr );
    REQUIRE( th3prime->isActive() == true );
    REQUIRE( th3prime->getInclusiveHisto() != nullptr );
    REQUIRE( th3prime->getTrueHisto() == nullptr );
    REQUIRE( th3prime->getFalseHisto() != nullptr );
    th3prime->Fill(true, 10, 4, 3);
    th3prime->Fill(false, 11, 5, 4, 0.5);
    CHECK( th3prime->getInclusiveHisto()->GetBinContent(10,4,3) == 0 );
    CHECK( th3prime->getInclusiveHisto()->GetBinContent(11,5,4) == 1 );
    CHECK( th3prime->getInclusiveHisto()->GetBinContent(12,6,5) == Approx(0.5) );
    CHECK( th3prime->getInclusiveHisto()->GetBinContent(13,7,6) == 0 );
    CHECK( th3prime->getFalseHisto()->GetBinContent(10,4,3) == 0 );
    CHECK( th3prime->getFalseHisto()->GetBinContent(11,5,4) == 0 );
    CHECK( th3prime->getFalseHisto()->GetBinContent(12,6,5) == Approx(0.5) );
    CHECK( th3prime->getFalseHisto()->GetBinContent(13,7,6) == 0 );
  }

  SECTION("Event weight") {
    weight.beginEvent();
    CHECK( wrapper.getWeight() == 1.0 );
    weight.multiplyWeight(0.5);
    CHECK( wrapper.getWeight() == Approx(0.5) );
    weight.multiplyWeight(0.3);
    CHECK( wrapper.getWeight() == Approx(0.15) );
    
    TDirectory dir("rootdir", "rootdir");
    // WrappedTH1
    WrappedTH1 *th1 = wrapper.makeTH<TH1F>(HistoLevel::kVital, &dir, "name", "title", 100, 0, 100);
    REQUIRE( th1 );
    REQUIRE( th1->isActive() );
    REQUIRE( th1->getHisto() );
    th1->Fill(10);
    CHECK( th1->getHisto()->GetBinContent(11) == Approx(0.15) );
    
    // WrappedTH2
    WrappedTH2 *th2 = wrapper.makeTH<TH2F>(HistoLevel::kVital, &dir, "name", "title", 100,0,100, 20,-5,5);
    REQUIRE( th2 );
    REQUIRE( th2->isActive() );
    REQUIRE( th2->getHisto() );
    th2->Fill(50, 2);
    CHECK( th2->getHisto()->GetBinContent(51, 15) == Approx(0.15) );
    
    // WrappedTH3
    WrappedTH3 *th3 = wrapper.makeTH<TH3F>(HistoLevel::kVital, &dir, "name", "title", 100,0,100, 20,-5,5, 50,-100,-50);
    REQUIRE( th3 );
    REQUIRE( th3->isActive() );
    REQUIRE( th3->getHisto() );
    th3->Fill(50, 1.2, -75);
    CHECK( th3->getHisto()->GetBinContent(51, 13, 26) == Approx(0.15) );

    // WrappedUnfoldedFactorisationHisto
    WrappedUnfoldedFactorisationHisto *tw2 = wrapper.makeTH<TH2F>(10, HistoLevel::kVital, &dir, "name", "title", 100,0,100);
    REQUIRE( tw2 );
    REQUIRE( tw2->isActive() );
    REQUIRE( tw2->getHisto() );
    // omit test
    
    // WrappedTH1Triplet
    TDirectory fakedir("fakedir", "fakedir");
    TDirectory truedir("truedir", "truedir");
    std::vector<TDirectory*> dirs3 = { &dir, &fakedir, &truedir };

    WrappedTH1Triplet *tt1 = wrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, dirs3, "nametr1", "title", 100, 0, 100);
    REQUIRE( tt1 != nullptr );
    REQUIRE( tt1->isActive() == true );
    REQUIRE( tt1->getInclusiveHisto() != nullptr );
    REQUIRE( tt1->getTrueHisto() != nullptr );
    REQUIRE( tt1->getFalseHisto() != nullptr );
    tt1->Fill(true, 10);
    tt1->Fill(false, 11);
    CHECK( tt1->getInclusiveHisto()->GetBinContent(11) == Approx(0.15) );
    CHECK( tt1->getInclusiveHisto()->GetBinContent(12) == Approx(0.15) );
    CHECK( tt1->getTrueHisto()->GetBinContent(11) == Approx(0.15) );
    CHECK( tt1->getTrueHisto()->GetBinContent(12) == 0 );
    CHECK( tt1->getFalseHisto()->GetBinContent(11) == 0 );
    CHECK( tt1->getFalseHisto()->GetBinContent(12) == Approx(0.15) );

    // WrappedTH2Triplet
    WrappedTH2Triplet *tt2 = wrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, dirs3, "nametr2", "title", 100, 0, 100, 20,-5,5);
    REQUIRE( tt2 != nullptr );
    REQUIRE( tt2->isActive() == true );
    REQUIRE( tt2->getInclusiveHisto() != nullptr );
    REQUIRE( tt2->getTrueHisto() != nullptr );
    REQUIRE( tt2->getFalseHisto() != nullptr );
    tt2->Fill(true, 10, 2);
    tt2->Fill(false, 11, 2);
    CHECK( tt2->getInclusiveHisto()->GetBinContent(11,15) == Approx(0.15) );
    CHECK( tt2->getInclusiveHisto()->GetBinContent(12,15) == Approx(0.15) );
    CHECK( tt2->getTrueHisto()->GetBinContent(11,15) == Approx(0.15) );
    CHECK( tt2->getTrueHisto()->GetBinContent(12,15) == 0 );
    CHECK( tt2->getFalseHisto()->GetBinContent(11,15) == 0 );
    CHECK( tt2->getFalseHisto()->GetBinContent(12,15) == Approx(0.15) );    

    // WrappedTH3Triplet
    WrappedTH3Triplet *tt3 = wrapper.makeTHTriplet<TH3F>(true, HistoLevel::kVital, dirs3, "nametr3", "title", 100, 0, 100, 20,-5,5, 50,-100,-50);
    REQUIRE( tt3 != nullptr );
    REQUIRE( tt3->isActive() == true );
    REQUIRE( tt3->getInclusiveHisto() != nullptr );
    REQUIRE( tt3->getTrueHisto() != nullptr );
    REQUIRE( tt3->getFalseHisto() != nullptr );
    tt3->Fill(true, 10, 2, -75);
    tt3->Fill(false, 11, 2, -75);
    CHECK( tt3->getInclusiveHisto()->GetBinContent(11,15,26) == Approx(0.15) );
    CHECK( tt3->getInclusiveHisto()->GetBinContent(12,15,26) == Approx(0.15) );
    CHECK( tt3->getTrueHisto()->GetBinContent(11,15,26) == Approx(0.15) );
    CHECK( tt3->getTrueHisto()->GetBinContent(12,15,26) == 0 );
    CHECK( tt3->getFalseHisto()->GetBinContent(11,15,26) == 0 );
    CHECK( tt3->getFalseHisto()->GetBinContent(12,15,26) == Approx(0.15) );    

  }
    
  
}

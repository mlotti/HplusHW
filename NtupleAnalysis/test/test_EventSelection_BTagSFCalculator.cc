#include "catch.hpp"
#include "test_createTree.h"

#include "EventSelection/interface/BTagSFCalculator.h"
#include "Framework/interface/Exception.h"
#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/BranchManager.h"
#include "DataFormat/interface/Jet.h"
#include "Framework/interface/HistoWrapper.h"

#include <iostream>
#include "TDirectory.h"

TEST_CASE("BTagSFCalculator works", "[EventSelection]") {
  SECTION("BTagSFInputItem") {
    // Constant item, test basic functionality
    BTagSFInputItem item1(30., 50., 0.987);
    CHECK( item1.matchesPtRange(20.) == false );
    CHECK( item1.matchesPtRange(40.) == true );
    CHECK( item1.matchesPtRange(60.) == false );
    CHECK( item1.isGreaterThanPtRange(20.) == false );
    CHECK( item1.isGreaterThanPtRange(40.) == false );
    CHECK( item1.isGreaterThanPtRange(60.) == true );
    REQUIRE_THROWS_AS( item1.getValueByPt(20.), hplus::Exception );
    CHECK( item1.getValueByPt(40.) == 0.987f );
    REQUIRE_THROWS_AS( item1.getValueByPt(60.), hplus::Exception );
    item1.setAsOverflowBinPt();
    CHECK( item1.matchesPtRange(20.) == false );
    CHECK( item1.matchesPtRange(40.) == true );
    CHECK( item1.matchesPtRange(60.) == true );
    CHECK( item1.getPtMax() == 50 );
    REQUIRE_THROWS_AS( item1.getValueByPt(20.), hplus::Exception );
    CHECK( item1.getValueByPt(40.) == 0.987f );
    CHECK( item1.getValueByPt(60.) == 0.987f );
    // Function object, test values
    BTagSFInputItem item2(30., 50., "0.01*x+0.123");
    REQUIRE_THROWS_AS( item2.getValueByPt(20.), hplus::Exception );
    CHECK( item2.getValueByPt(40.) == 0.523f );
    REQUIRE_THROWS_AS( item2.getValueByPt(60.), hplus::Exception );
    item2.setAsOverflowBinPt();
    REQUIRE_THROWS_AS( item2.getValueByPt(20.), hplus::Exception );
    CHECK( item2.getValueByPt(40.) == 0.523f );
    REQUIRE_NOTHROW( item2.getValueByPt(60.) );
    CHECK( item2.getValueByPt(60.) == 0.723f );
  }
  
  EventWeight weight;
  HistoWrapper histoWrapper(weight, "Debug");
  TDirectory dir("rootdir", "rootdir");
  // Create dummy events for testing
  auto tree = std::unique_ptr<TTree>(new TTree("Events", "Events"));
  std::vector<float> pt; tree->Branch("Jets_pt", &pt);
  std::vector<float> eta; tree->Branch("Jets_eta", &eta);
  std::vector<float> phi; tree->Branch("Jets_phi", &phi);
  std::vector<float> e; tree->Branch("Jets_e", &e);
  std::vector<short> pdgId; tree->Branch("Jets_pdgId", &pdgId);
  std::vector<short> partonFlavour; tree->Branch("Jets_partonFlavour", &partonFlavour);
  std::vector<short> hadronFlavour; tree->Branch("Jets_hadronFlavour", &hadronFlavour);
  std::vector<float> bdiscr; tree->Branch("Jets_pfCombinedInclusiveSecondaryVertexV2BJetTags", &bdiscr);
  // Event 1: 4 jets, b->b / c->not b / uds->not b / g->not b
  pt = std::vector<float>{34.f, 35.f, 36.f, 37.f};
  pdgId = std::vector<short>{5, 4, 3, 21};
  partonFlavour = std::vector<short>{5, 4, 3, 21};
  hadronFlavour = std::vector<short>{5, 4, 3, 21};
  bdiscr = std::vector<float>{1.f, 0.f, 0.f, 0.f};
  tree->Fill();
  
  // Create event tree
  BranchManager mgr;
  mgr.setTree(tree.get());
  JetCollection coll;
  coll.setBJetDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags");
  coll.setupBranches(mgr);
  
  // Create config for testing
  boost::property_tree::ptree tmp = getMinimalConfig();
  tmp.put("bjetDiscr", "pfCombinedInclusiveSecondaryVertexV2BJetTags");
  tmp.put("bjetDiscrWorkingPoint", "Loose");
  tmp.put("numberOfBJetsCutValue", 1);
  tmp.put("numberOfBJetsCutDirection", ">=");
  //ParameterSet psetDefault(tmp, true, false);
  
  SECTION("No input given") {
    ParameterSet psetDefault(tmp, true, false);
    REQUIRE_NOTHROW( BTagSFCalculator p(psetDefault) );
    BTagSFCalculator p(psetDefault);
    mgr.setEntry(0);
    REQUIRE( coll.size() == 4 );
    std::vector<Jet> jets = coll.toVector();
    REQUIRE( jets.size() == 4 );
    std::vector<Jet> bjets = { jets[0] };
    // SF should be 1.0 in case there is no input
    CHECK( p.calculateSF(jets, bjets) == 1.0f );
  }

  // Add config fragments for btag efficiency and SF
  boost::property_tree::ptree effPset;
  boost::property_tree::ptree effList;
  effPset.put("jetFlavor", "B");
  effPset.put("ptMin", 30);
  effPset.put("ptMax", 50);
  effPset.put("eff", 0.456);
  effList.push_back(std::make_pair("", effPset));
  effPset.put("jetFlavor", "B");
  effPset.put("ptMin", 50);
  effPset.put("ptMax", 70);
  effPset.put("eff", 0.678);
  effList.push_back(std::make_pair("", effPset));
  effPset.put("jetFlavor", "B");
  effPset.put("ptMin", 70);
  effPset.put("ptMax", 500);
  effPset.put("eff", 0.987);
  effList.push_back(std::make_pair("", effPset));
  effPset.put("jetFlavor", "C");
  effPset.put("ptMin", 30);
  effPset.put("ptMax", 50);
  effPset.put("eff", 0.123);
  effList.push_back(std::make_pair("", effPset));
  effPset.put("jetFlavor", "C");
  effPset.put("ptMin", 50);
  effPset.put("ptMax", 500);
  effPset.put("eff", 0.156);
  effList.push_back(std::make_pair("", effPset));
  effPset.put("jetFlavor", "Light");
  effPset.put("ptMin", 30);
  effPset.put("ptMax", 50);
  effPset.put("eff", 0.098);
  effList.push_back(std::make_pair("", effPset));
  effPset.put("jetFlavor", "G");
  effPset.put("ptMin", 30);
  effPset.put("ptMax", 50);
  effPset.put("eff", 0.075);
  effList.push_back(std::make_pair("", effPset));
  tmp.add_child("btagEfficiency", effList);
  boost::property_tree::ptree sfPset;
  boost::property_tree::ptree sfList;
  sfPset.put("jetFlavor", 0); // 0 = b jet
  sfPset.put("ptMin", 30);
  sfPset.put("ptMax", 50);
  sfPset.put("formula", "0.91+0.01*x");
  sfList.push_back(std::make_pair("", sfPset));
  sfPset.put("jetFlavor", 0); // 0 = b jet
  sfPset.put("ptMin", 50);
  sfPset.put("ptMax", 70);
  sfPset.put("formula", "0.85+0.01*x");
  sfList.push_back(std::make_pair("", sfPset));
  sfPset.put("jetFlavor", 1); // 1 = c jet
  sfPset.put("ptMin", 30);
  sfPset.put("ptMax", 500);
  sfPset.put("formula", "0.87+0.01*x");
  sfList.push_back(std::make_pair("", sfPset));
  sfPset.put("jetFlavor", 2); // 2 = uds jet
  sfPset.put("ptMin", 30);
  sfPset.put("ptMax", 50);
  sfPset.put("formula", "1.07+0.01*x");
  sfList.push_back(std::make_pair("", sfPset));
  sfPset.put("jetFlavor", 2); // 2 = uds jet
  sfPset.put("ptMin", 50);
  sfPset.put("ptMax", 70);
  sfPset.put("formula", "1.02+0.01*x");
  sfList.push_back(std::make_pair("", sfPset));
  tmp.add_child("btagSF", sfList);

  SECTION("SF calculation") {
    ParameterSet psetDefault(tmp, true, false);
    //psetDefault.debug();
    //REQUIRE_NOTHROW( BTagSFCalculator p(psetDefault) );
    BTagSFCalculator p(psetDefault);
    p.bookHistograms(&dir, histoWrapper);
    mgr.setEntry(0);
    REQUIRE( coll.size() == 4 );
    std::vector<Jet> jets = coll.toVector();
    REQUIRE( jets.size() == 4 );
    std::vector<Jet> bjets = { jets[0] };
    // Check correct reading of config
    REQUIRE( p.sizeOfEfficiencyList(BTagSFCalculator::kBJet) == 3 );
    REQUIRE( p.sizeOfEfficiencyList(BTagSFCalculator::kCJet) == 2 );
    REQUIRE( p.sizeOfEfficiencyList(BTagSFCalculator::kGJet) == 1 );
    REQUIRE( p.sizeOfEfficiencyList(BTagSFCalculator::kUDSJet) == 1 );
    REQUIRE( p.sizeOfSFList(BTagSFCalculator::kBJet) == 2 );
    REQUIRE( p.sizeOfSFList(BTagSFCalculator::kCJet) == 1 );
    REQUIRE( p.sizeOfSFList(BTagSFCalculator::kGJet) == 2 );
    REQUIRE( p.sizeOfSFList(BTagSFCalculator::kUDSJet) == 2 );
    // Check individual SF values
    std::vector<Jet> jnull =  { };
    std::vector<Jet> j1 =  { jets[0] };
    std::vector<Jet> b1 = { jets[0] };
    CHECK( p.calculateSF(j1, jnull) == Approx((1.0-0.456*(0.91+0.01*34.))/(1.0-0.456)) ); // b->not b
    CHECK( p.calculateSF(j1, b1) == Approx(0.91+0.01*34.) ); // b->b
    std::vector<Jet> j2 =  { jets[1] };
    std::vector<Jet> b2 = { jets[1] };
    CHECK( p.calculateSF(j2, jnull) == Approx((1.0-0.123*(0.87+0.01*35.))/(1.0-0.123)) ); // c->not b
    CHECK( p.calculateSF(j2, b2) == Approx(0.87+0.01*35.) ); // c->b
    std::vector<Jet> j3 =  { jets[2] };
    std::vector<Jet> b3 = { jets[2] };
    CHECK( p.calculateSF(j3, jnull) == Approx((1.0-0.098*(1.07+0.01*36.))/(1.0-0.098)) ); // uds->not b
    CHECK( p.calculateSF(j3, b3) == Approx(1.07+0.01*36.) ); // uds->b
    std::vector<Jet> j4 =  { jets[3] };
    std::vector<Jet> b4 = { jets[3] };
    CHECK( p.calculateSF(j4, jnull) == Approx((1.0-0.075*(1.07+0.01*37.))/(1.0-0.075)) ); // g->not b
    CHECK( p.calculateSF(j4, b4) == Approx(1.07+0.01*37.) ); // g->b
    // Check combined SF values
    CHECK( p.calculateSF(jets, bjets) == Approx((0.91+0.01*34.) * (1.0-0.123*(0.87+0.01*35.))/(1.0-0.123) * (1.0-0.098*(1.07+0.01*36.))/(1.0-0.098) * (1.0-0.075*(1.07+0.01*37.))/(1.0-0.075)));
  }
}

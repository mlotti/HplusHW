#include "catch.hpp"
#include "test_createTree.h"

#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/Exception.h"
#include "Framework/interface/HistoSplitter.h"
#include "Framework/interface/HistoWrapper.h"
#include "boost/property_tree/json_parser.hpp"

#include "TH1F.h"


// class HistoSplitterDummy : public HistoSplitter {
// public:
//   HistoSplitterDummy(const ParameterSet& config, HistoWrapper& histoWrapper)
//   : HistoSplitter(config, histoWrapper) { }
//   ~HistoSplitterDummy() { }
//   
//   friend HistoSplitterTester;
// };
// 
class HistoSplitterTester : public HistoSplitter {
public:
  HistoSplitterTester(const ParameterSet& config, HistoWrapper& histoWrapper)
  : HistoSplitter(config, histoWrapper) { }
  ~HistoSplitterTester() { }
  
  void checkIndexValidity() const { HistoSplitter::checkIndexValidity(); }
  size_t getShapeBinIndex() const { return HistoSplitter::getShapeBinIndex(); }
  std::vector<size_t> obtainIndicesFromUnfoldedIndex(size_t unfoldedIndex) const { return HistoSplitter::obtainIndicesFromUnfoldedIndex(unfoldedIndex); }
};


TEST_CASE("HistoSplitter", "[Framework]") {
  SECTION("HistoSplitterItem input validity") {
    std::string tmp = "{\n";
    tmp += "  \"missingInput1\": {\n";
    tmp += "    \"label\": \"dummy\"\n";
    tmp += "  },\n";
    tmp += "  \"missingInput2\": {\n";
    tmp += "    \"binLowEdges\": [5.0]\n";
    tmp += "  },\n";
    tmp += "  \"missingInput3\": {\n";
    tmp += "    \"label\": \"dummy\",\n";
    tmp += "    \"binLowEdges\": [5.0]\n";
    tmp += "  },\n";
    tmp += "  \"invalidInput1\": {\n";
    tmp += "    \"label\": \"dummy\",\n";
    tmp += "    \"binLowEdges\": [1.0, 5.0, 3.0, 6.0]\n";
    tmp += "  },\n";
    tmp += "  \"invalidInput2\": {\n";
    tmp += "    \"label\": \"\",\n";
    tmp += "    \"binLowEdges\": [5.0]\n";
    tmp += "  }\n";
    tmp += "}\n";
    ParameterSet pset(tmp, true);
    REQUIRE_THROWS_AS( HistoSplitterItem(pset.getParameter<ParameterSet>("missingInput1")), hplus::Exception );
    REQUIRE_THROWS_AS( HistoSplitterItem(pset.getParameter<ParameterSet>("missingInput2")), hplus::Exception );
    // Absolute value parameter is optional
    REQUIRE_NOTHROW( HistoSplitterItem(pset.getParameter<ParameterSet>("missingInput3")) );
    REQUIRE_THROWS_AS( HistoSplitterItem(pset.getParameter<ParameterSet>("invalidInput1")), hplus::Exception );
    REQUIRE_THROWS_AS( HistoSplitterItem(pset.getParameter<ParameterSet>("invalidInput2")), hplus::Exception );
  }
   
  SECTION("HistoSplitterItem getters") {
    std::string tmp = "{\n";
    tmp += "  \"input1\": {\n";
    tmp += "    \"label\": \"dummy1\",\n";
    tmp += "    \"binLowEdges\": [5.0, 10.0, 15.0, 20.0],\n";
    tmp += "    \"useAbsoluteValues\": true\n";
    tmp += "  },\n";
    tmp += "  \"input2\": {\n";
    tmp += "    \"label\": \"dummy2\",\n";
    tmp += "    \"binLowEdges\": [5, 10, 15, 20]\n";
    tmp += "  },\n";
    tmp += "  \"input3\": {\n";
    tmp += "    \"label\": \"dummy3\",\n";
    tmp += "    \"binLowEdges\": [5.0, 10.0, 15.0, 20.0],\n";
    tmp += "    \"useAbsoluteValues\": false\n";
    tmp += "  },\n";
    tmp += "  \"input4\": {\n";
    tmp += "    \"label\": \"dummy4\",\n";
    tmp += "    \"binLowEdges\": [5, 10, 15, 20],\n";
    tmp += "    \"useAbsoluteValues\": true\n";
    tmp += "  }\n";
    tmp += "}\n";
    ParameterSet pset(tmp, true);
    HistoSplitterItem item1 = pset.getParameter<ParameterSet>("input1");
    HistoSplitterItem item2 = pset.getParameter<ParameterSet>("input2");
    HistoSplitterItem item3 = pset.getParameter<ParameterSet>("input3");
    HistoSplitterItem item4 = pset.getParameter<ParameterSet>("input4");
    // Label
    CHECK( item1.getLabel() == "dummy1" );
    CHECK( item2.getLabel() == "dummy2" );
    // Bin count
    CHECK( item1.getBinCount() == 5 );
    CHECK( item2.getBinCount() == 5 );
    CHECK( item3.getBinCount() == 5 );
    CHECK( item4.getBinCount() == 5 );
    // Bin index for int test value
    CHECK( item2.getBinIndex(-12) == 0 );
    CHECK( item2.getBinIndex(1) == 0 );
    CHECK( item2.getBinIndex(5) == 1 );
    CHECK( item2.getBinIndex(9) == 1 );
    CHECK( item2.getBinIndex(10) == 2 );
    CHECK( item2.getBinIndex(15) == 3 );
    CHECK( item2.getBinIndex(20) == 4 );
    CHECK( item2.getBinIndex(2000000) == 4 );
    // Bin index for float test value
    CHECK( item3.getBinIndex(-12.0) == 0 );
    CHECK( item3.getBinIndex(1.0) == 0 );
    CHECK( item3.getBinIndex(5.01) == 1 );
    CHECK( item3.getBinIndex(9.99) == 1 );
    CHECK( item3.getBinIndex(10.01) == 2 );
    CHECK( item3.getBinIndex(15.01) == 3 );
    CHECK( item3.getBinIndex(20.01) == 4 );
    CHECK( item3.getBinIndex(2000000.0) == 4 );
    // Absolute values
    CHECK( item1.getBinIndex(-12.0) == 2 );
    CHECK( item2.getBinIndex(-12) == 0 );
    CHECK( item3.getBinIndex(-12.0) == 0 );
    CHECK( item4.getBinIndex(-12) == 2 );
    // Bin labels
    CHECK( item1.getBinDescription(0) == "abs(dummy1)<5" );
    CHECK( item1.getBinDescription(1) == "abs(dummy1)=5..10" );
    CHECK( item1.getBinDescription(4) == "abs(dummy1)>20" );
    REQUIRE_THROWS_AS( item1.getBinDescription(5), hplus::Exception );
    CHECK( item2.getBinDescription(0) == "dummy2<5" );
    CHECK( item2.getBinDescription(1) == "dummy2=5..10" );
    CHECK( item2.getBinDescription(4) == "dummy2>20" );
    REQUIRE_THROWS_AS( item2.getBinDescription(5), hplus::Exception );
  }

  TDirectory* f = getDirectory("test_HistoSplitter");
  TDirectory* fTrue = f->mkdir("trueHistograms");
  TDirectory* fFalse = f->mkdir("falseHistograms");
  std::vector<TDirectory*> fTripletDirs = {f,fFalse,fTrue};
  
  EventWeight weight;
  HistoWrapper histoWrapper(weight, "Debug");

  SECTION("HistoSplitter / no splitting") {
    ParameterSet pset("{}", true);
    HistoSplitterTester test(pset, histoWrapper);
    // Check SplittedBinInfo histogram
    test.bookHistograms(f);
    REQUIRE( f->Get("SplittedBinInfo") > 0 );
    TH1F* h = dynamic_cast<TH1F*>(f->Get("SplittedBinInfo"));
    CHECK( h->GetNbinsX() == 1 );
    CHECK( h->GetBinContent(1) == 1 );
    h->SetName("SplittedBinInfo_nosplitting");
    h->SetTitle("SplittedBinInfo_nosplitting");
    // Check safety for preventing double counting
    REQUIRE_THROWS_AS( test.checkIndexValidity(), hplus::Exception );
    REQUIRE_NOTHROW( test.setFactorisationBinForEvent() );
    REQUIRE_NOTHROW( test.checkIndexValidity() );
    test.initialize();
    REQUIRE_THROWS_AS( test.checkIndexValidity(), hplus::Exception );
    // Check unfolded bin index
    test.setFactorisationBinForEvent();
    REQUIRE( test.getShapeBinIndex() == 0 );
    // Check indexing
    std::vector<size_t> v = test.obtainIndicesFromUnfoldedIndex(0);
    CHECK( v.size() == 0 );
    // Check 1D histogram
    HistoSplitter::SplittedTH1s h1;
    test.createShapeHistogram<TH1F>(HistoLevel::kDebug, f, h1, "0_test1D", "0_test1D", 10, 0., 400.);
    CHECK( h1.size() == 1 );
    test.fillShapeHistogram(h1, 205.0);
    test.fillShapeHistogram(h1, 105.0, 2.34);
    CHECK( h1[0]->getHisto()->GetBinContent(6) == Approx(1.000));
    CHECK( h1[0]->getHisto()->GetBinContent(3) == Approx(2.34));
    // Check 2D histogram
    HistoSplitter::SplittedTH2s h2;
    test.createShapeHistogram<TH2F>(HistoLevel::kDebug, f, h2, "0_test2D", "0_test2D", 10, 0., 400., 20, 0., 40.);
    CHECK( h2.size() == 1 );
    test.fillShapeHistogram(h2, 205.0, 3.0);
    test.fillShapeHistogram(h2, 105.0, 15.0, 2.34);
    CHECK( h2[0]->getHisto()->GetBinContent(6,2) == Approx(1.000));
    CHECK( h2[0]->getHisto()->GetBinContent(3,8) == Approx(2.34));
    // Check WrappedUnfoldedFactorisationHisto
    WrappedUnfoldedFactorisationHisto* hf;
    test.createShapeHistogram(HistoLevel::kDebug, f, hf, "0_testHF", "0_testHF", 10, 0., 400.);
    CHECK( hf->getHisto()->GetNbinsX() == 10 );
    CHECK( hf->getHisto()->GetNbinsY() == 1 );
    test.fillShapeHistogram(hf, 205.0);
    test.fillShapeHistogram(hf, 105.0, 2.34);
    CHECK( hf->getHisto()->GetBinContent(6,1) == Approx(1.000));
    CHECK( hf->getHisto()->GetBinContent(3,1) == Approx(2.34));
    // Check 1D triplet histogram
    
    HistoSplitter::SplittedTripletTH1s h1t;
    test.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kDebug, fTripletDirs, h1t, "0_test1Dtriplet", "0_test1Dtriplet", 10, 0., 400.);
    CHECK( h1t.size() == 1 );
    test.fillShapeHistogramTriplet(h1t, false, 205.0);
    test.fillShapeHistogramTriplet(h1t, true, 105.0, 2.34);
    CHECK( h1t[0]->getInclusiveHisto()->GetBinContent(6) == Approx(1.000));
    CHECK( h1t[0]->getInclusiveHisto()->GetBinContent(3) == Approx(2.34));
    CHECK( h1t[0]->getFalseHisto()->GetBinContent(6) == Approx(1.000));
    CHECK( h1t[0]->getFalseHisto()->GetBinContent(3) == Approx(0.0));
    CHECK( h1t[0]->getTrueHisto()->GetBinContent(6) == Approx(0.0));
    CHECK( h1t[0]->getTrueHisto()->GetBinContent(3) == Approx(2.34));

    HistoSplitter::SplittedTripletTH2s h2t;
    test.createShapeHistogramTriplet<TH2F>(true, HistoLevel::kDebug, fTripletDirs, h2t, "0_test2Dtriplet", "0_test2Dtriplet", 10, 0., 400., 10, 0., 100.);
    CHECK( h2t.size() == 1 );
    test.fillShapeHistogramTriplet(h2t, false, 205.0, 4.0);
    test.fillShapeHistogramTriplet(h2t, false, 205.0, 4.0, 2.34);

    HistoSplitter::SplittedTripletTH3s h3t;
    test.createShapeHistogramTriplet<TH3F>(true, HistoLevel::kDebug, fTripletDirs, h3t, "0_test3Dtriplet", "0_test3Dtriplet", 10, 0., 400., 10, 0., 100., 10, 0., 100.);
    CHECK( h3t.size() == 1 );
    test.fillShapeHistogramTriplet(h3t, false, 205.0, 4.0, 2.0);
    test.fillShapeHistogramTriplet(h3t, false, 205.0, 4.0, 2.0, 2.34);
    
  }

  SECTION("HistoSplitter / splitting as function of 1 variable") {
    std::string tmp = "{\n";
    tmp += "  \"histogramSplitting\": [\n";
    tmp += "    {\n";
    tmp += "      \"label\": \"taupt\",\n";
    tmp += "      \"binLowEdges\": [5.0, 10.0, 15.0, 20.0],\n";
    tmp += "      \"useAbsoluteValues\": false\n";
    tmp += "    }\n";
    tmp += "  ]\n";
    tmp += "}\n";
    ParameterSet pset(tmp, true);
    HistoSplitterTester test(pset, histoWrapper);
    // Check SplittedBinInfo histogram
    test.bookHistograms(f);
    REQUIRE( f->Get("SplittedBinInfo") > 0 );
    TH1F* h = dynamic_cast<TH1F*>(f->Get("SplittedBinInfo"));
    CHECK( h->GetNbinsX() == 2 );
    CHECK( h->GetBinContent(1) == 1 );
    CHECK( h->GetBinContent(2) == 5 );
    h->SetName("SplittedBinInfo_1Dsplitting");
    h->SetTitle("SplittedBinInfo_1Dsplitting");
    // Check safety for preventing double counting
    REQUIRE_THROWS_AS( test.checkIndexValidity(), hplus::Exception );
    REQUIRE_THROWS_AS( test.setFactorisationBinForEvent(), hplus::Exception );
    test.initialize();
    REQUIRE_THROWS_AS( test.checkIndexValidity(), hplus::Exception );
    // Check unfolded bin index
    REQUIRE_NOTHROW( test.setFactorisationBinForEvent({11.0}) );
    REQUIRE( test.getShapeBinIndex() == 2 );
    // Check indexing
    std::vector<size_t> v = test.obtainIndicesFromUnfoldedIndex(2);
    CHECK( v.size() == 1 );
    CHECK( v[0] == 2 );
    // Check 1D histogram
    HistoSplitter::SplittedTH1s h1;
    test.createShapeHistogram<TH1F>(HistoLevel::kDebug, f, h1, "1_test1D", "1_test1D", 10, 0., 400.);
    CHECK( h1.size() == 6 );
    test.fillShapeHistogram(h1, 205.0);
    test.fillShapeHistogram(h1, 105.0, 2.34);
    CHECK( h1[2]->getHisto()->GetBinContent(6) == Approx(1.000));
    CHECK( h1[2]->getHisto()->GetBinContent(3) == Approx(2.34));
    CHECK( h1[5]->getHisto()->GetBinContent(6) == Approx(1.000));
    CHECK( h1[5]->getHisto()->GetBinContent(3) == Approx(2.34));
    // Check 2D histogram
    HistoSplitter::SplittedTH2s h2;
    test.createShapeHistogram<TH2F>(HistoLevel::kDebug, f, h2, "1_test2D", "1_test2D", 10, 0., 400., 20, 0., 40.);
    CHECK( h2.size() == 6 );
    test.fillShapeHistogram(h2, 205.0, 3.0);
    test.fillShapeHistogram(h2, 105.0, 15.0, 2.34);
    CHECK( h2[2]->getHisto()->GetBinContent(6,2) == Approx(1.000));
    CHECK( h2[2]->getHisto()->GetBinContent(3,8) == Approx(2.34));
    CHECK( h2[5]->getHisto()->GetBinContent(6,2) == Approx(1.000));
    CHECK( h2[5]->getHisto()->GetBinContent(3,8) == Approx(2.34));
    // Check WrappedUnfoldedFactorisationHisto
    WrappedUnfoldedFactorisationHisto* hf;
    test.createShapeHistogram(HistoLevel::kDebug, f, hf, "1_testHF", "1_testHF", 10, 0., 400.);
    CHECK( hf->getHisto()->GetNbinsX() == 10 );
    CHECK( hf->getHisto()->GetNbinsY() == 5 );
    test.fillShapeHistogram(hf, 205.0);
    test.fillShapeHistogram(hf, 105.0, 2.34);
    CHECK( hf->getHisto()->GetBinContent(6,3) == Approx(1.000));
    CHECK( hf->getHisto()->GetBinContent(3,3) == Approx(2.34));
  }
  
  SECTION("HistoSplitter / splitting as function of 2 variables") {
    std::string tmp = "{\n";
    tmp += "  \"histogramSplitting\": [\n";
    tmp += "    {\n";
    tmp += "      \"label\": \"taupt\",\n";
    tmp += "      \"binLowEdges\": [5.0, 10.0, 15.0, 20.0],\n";
    tmp += "      \"useAbsoluteValues\": false\n";
    tmp += "    },\n";
    tmp += "    {\n";
    tmp += "      \"label\": \"taueta\",\n";
    tmp += "      \"binLowEdges\": [1.5],\n";
    tmp += "      \"useAbsoluteValues\": true\n";
    tmp += "    }\n";
    tmp += "  ]\n";
    tmp += "}\n";
    ParameterSet pset(tmp, true);
    HistoSplitterTester test(pset, histoWrapper);
    // Check SplittedBinInfo histogram
    test.bookHistograms(f);
    REQUIRE( f->Get("SplittedBinInfo") > 0 );
    TH1F* h = dynamic_cast<TH1F*>(f->Get("SplittedBinInfo"));
    CHECK( h->GetNbinsX() == 3 );
    CHECK( h->GetBinContent(1) == 1 );
    CHECK( h->GetBinContent(2) == 5 );
    CHECK( h->GetBinContent(3) == 2 );
    h->SetName("SplittedBinInfo_2Dsplitting");
    h->SetTitle("SplittedBinInfo_2Dsplitting");
    // Check safety for preventing double counting
    REQUIRE_THROWS_AS( test.checkIndexValidity(), hplus::Exception );
    REQUIRE_THROWS_AS( test.setFactorisationBinForEvent(), hplus::Exception );
    test.initialize();
    REQUIRE_THROWS_AS( test.checkIndexValidity(), hplus::Exception );
    // Check unfolded bin index
    REQUIRE_NOTHROW( test.setFactorisationBinForEvent({11.0, -2.0}) );
    REQUIRE( test.getShapeBinIndex() == 7 ); // 2+5
    // Check indexing
    std::vector<size_t> v = test.obtainIndicesFromUnfoldedIndex(7);
    CHECK( v.size() == 2 );
    CHECK( v[0] == 2 );
    CHECK( v[1] == 1 );
    // Check 1D histogram
    HistoSplitter::SplittedTH1s h1;
    test.createShapeHistogram<TH1F>(HistoLevel::kDebug, f, h1, "2_test1D", "2_test1D", 10, 0., 400.);
    CHECK( h1.size() == 11 );
    test.fillShapeHistogram(h1, 205.0);
    test.fillShapeHistogram(h1, 105.0, 2.34);
    CHECK( h1[7]->getHisto()->GetBinContent(6) == Approx(1.000));
    CHECK( h1[7]->getHisto()->GetBinContent(3) == Approx(2.34));
    CHECK( h1[10]->getHisto()->GetBinContent(6) == Approx(1.000));
    CHECK( h1[10]->getHisto()->GetBinContent(3) == Approx(2.34));
    // Check 2D histogram
    HistoSplitter::SplittedTH2s h2;
    test.createShapeHistogram<TH2F>(HistoLevel::kDebug, f, h2, "2_test2D", "2_test2D", 10, 0., 400., 20, 0., 40.);
    CHECK( h2.size() == 11 );
    test.fillShapeHistogram(h2, 205.0, 3.0);
    test.fillShapeHistogram(h2, 105.0, 15.0, 2.34);
    CHECK( h2[7]->getHisto()->GetBinContent(6,2) == Approx(1.000));
    CHECK( h2[7]->getHisto()->GetBinContent(3,8) == Approx(2.34));
    CHECK( h2[10]->getHisto()->GetBinContent(6,2) == Approx(1.000));
    CHECK( h2[10]->getHisto()->GetBinContent(3,8) == Approx(2.34));
    // Check WrappedUnfoldedFactorisationHisto
    WrappedUnfoldedFactorisationHisto* hf;
    test.createShapeHistogram(HistoLevel::kDebug, f, hf, "2_testHF", "2_testHF", 10, 0., 400.);
    hf->getHisto()->SetDirectory(f);
    CHECK( hf->getHisto()->GetNbinsX() == 10 );
    CHECK( hf->getHisto()->GetNbinsY() == 10 );
    test.fillShapeHistogram(hf, 205.0);
    test.fillShapeHistogram(hf, 105.0, 2.34);
    CHECK( hf->getHisto()->GetBinContent(6,8) == Approx(1.000));
    CHECK( hf->getHisto()->GetBinContent(3,8) == Approx(2.34));
  }
  closeDirectory(f);
}

#include "catch.hpp"

#include "test_createTree.h"

#include "Framework/interface/SelectorImpl.h"
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/BranchManager.h"

#include "TDirectory.h"
#include "TH1F.h"

namespace {
  class SelectorTestSelectorImplEmpty: public BaseSelector {
  public:
    explicit SelectorTestSelectorImplEmpty(const boost::property_tree::ptree& config):
      BaseSelector(config) {}
    virtual ~SelectorTestSelectorImplEmpty() {}

    virtual void book(TDirectory *dir) override {}
    virtual void setupBranches(BranchManager& branchManager) override {}
    virtual void process(Long64_t entry) override {}
  };

  class SelectorTestSelectorImpl: public BaseSelector {
  public:
    explicit SelectorTestSelectorImpl(const boost::property_tree::ptree& config):
      BaseSelector(config),
      mode(config.get<int>("mode")),
      b_event(nullptr), b_num1(nullptr),
      c1(fEventCounter.addCounter("all")),
      c2(fEventCounter.addCounter("selected")),
      c3(fEventCounter.addCounter("weighted")),
      histo1(nullptr), histo2(nullptr), histo3(nullptr)
    {}
    virtual ~SelectorTestSelectorImpl() {}

    virtual void book(TDirectory *dir) override {
      histo1 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "histo1", "histo1", 10, 0, 10);
      histo2 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "histo2", "histo2", 100, 0, 100);
      histo3 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "histo3", "histo3", 100, 0, 100);
    }
    virtual void setupBranches(BranchManager& branchManager) override {
      branchManager.book("event", &b_event);
      branchManager.book("num1", &b_num1);
    }
    virtual void process(Long64_t entry) override {
      c1.increment();
      histo1->Fill(b_event->value());

      if(mode != 0 && b_event->value() % 2 == 0)
        return;
      c2.increment();

      for(int value: b_num1->value()) {
        histo2->Fill(value);
      }

      fEventWeight.multiplyWeight(0.5);
      c3.increment();

      for(int value: b_num1->value()) {
        histo3->Fill(value, fEventWeight.getWeight());
      }
    }

    const int mode;

    Branch<int> *b_event;
    Branch<std::vector<int> > *b_num1;

    Count c1;
    Count c2;
    Count c3;

    WrappedTH1 *histo1;
    WrappedTH1 *histo2;
    WrappedTH1 *histo3;
  };

}

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(SelectorTestSelectorImplEmpty);
REGISTER_SELECTOR(SelectorTestSelectorImpl);

TEST_CASE("SelectorImpl works", "[Framework]") {
  std::unique_ptr<TTree> tree = createSimpleTree();
  TDirectory dir("rootdir", "rootdir");
  SelectorImpl tselector(&dir, tree->GetEntries(), true, "{}");
  tselector.setPrintStatus(false);

  SECTION("Single empty selector") {
    tselector.addSelector("test", "SelectorTestSelectorImplEmpty", "{}");
    tree->Process(&tselector);
    REQUIRE( dir.Get("test") );
    REQUIRE( dir.Get("test/counters") );
    REQUIRE( dir.Get("test/counters/weighted") );
    CHECK( !dir.Get("test/counters/counter") );
    CHECK( !dir.Get("test/counters/weighted/counter") );
    TNamed *config = nullptr;
    dir.GetObject("test/config", config);
    REQUIRE( config );
    CHECK( config->GetTitle() == std::string("{}") );
  }

  SECTION("Two selectors with same name are not allowed") {
    tselector.addSelector("test", "SelectorTestSelectorImplEmpty", "{}");
    REQUIRE_THROWS_AS( tselector.addSelector("test", "SelectorTestSelectorImplEmpty", "{}"), std::logic_error );
  }

  SECTION("Two selectors doing some work") {
    tselector.addSelector("test", "SelectorTestSelectorImpl", "{\"mode\": 0}");
    tselector.addSelector("test2", "SelectorTestSelectorImpl", "{\"mode\": 1}");

    TNamed *config = nullptr;
    dir.GetObject("test/config", config);
    REQUIRE( config );
    CHECK( config->GetTitle() == std::string("{\"mode\": 0}") );
    dir.GetObject("test2/config", config);
    REQUIRE( config );
    CHECK( config->GetTitle() == std::string("{\"mode\": 1}") );

    tree->Process(&tselector);
    TH1 *h = nullptr;
    dir.GetObject("test/counters/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetBinContent(1) == 3 );
    CHECK( h->GetBinContent(2) == 3 );
    CHECK( h->GetBinContent(3) == 3 );

    dir.GetObject("test/counters/weighted/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetBinContent(1) == 3 );
    CHECK( h->GetBinContent(2) == 3 );
    CHECK( h->GetBinContent(3) == 1.5 );

    dir.GetObject("test/histo1", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 10 );
    CHECK( h->GetEntries() == 3 );
    CHECK( h->GetBinContent(1) == 0 );
    CHECK( h->GetBinContent(2) == 1 );
    CHECK( h->GetBinContent(3) == 1 );
    CHECK( h->GetBinContent(4) == 1 );
    CHECK( h->GetBinContent(5) == 0 );

    dir.GetObject("test/histo2", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 100 );
    REQUIRE( h->GetEntries() == 9 );
    CHECK( h->GetBinContent(0) == 1 );
    CHECK( h->GetBinContent(1) == 1 );
    CHECK( h->GetBinContent(2) == 1 );
    CHECK( h->GetBinContent(3) == 1 );
    CHECK( h->GetBinContent(4) == 1 );
    CHECK( h->GetBinContent(5) == 1 );
    CHECK( h->GetBinContent(6) == 0 );
    CHECK( h->GetBinContent(10) == 0 );
    CHECK( h->GetBinContent(11) == 1 );
    CHECK( h->GetBinContent(12) == 0 );
    CHECK( h->GetBinContent(100) == 0 );
    CHECK( h->GetBinContent(101) == 2 );

    dir.GetObject("test/histo3", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 100 );
    REQUIRE( h->GetEntries() == 9 );
    CHECK( h->GetBinContent(0) == 0.5 );
    CHECK( h->GetBinContent(1) == 0.5 );
    CHECK( h->GetBinContent(2) == 0.5 );
    CHECK( h->GetBinContent(3) == 0.5 );
    CHECK( h->GetBinContent(4) == 0.5 );
    CHECK( h->GetBinContent(5) == 0.5 );
    CHECK( h->GetBinContent(6) == 0 );
    CHECK( h->GetBinContent(10) == 0 );
    CHECK( h->GetBinContent(11) == 0.5 );
    CHECK( h->GetBinContent(12) == 0 );
    CHECK( h->GetBinContent(100) == 0 );
    CHECK( h->GetBinContent(101) == 1 );

    dir.GetObject("test2/counters/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetBinContent(1) == 3 );
    CHECK( h->GetBinContent(2) == 2 );
    CHECK( h->GetBinContent(3) == 2 );

    dir.GetObject("test2/counters/weighted/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 3 );
    CHECK( h->GetBinContent(1) == 3 );
    CHECK( h->GetBinContent(2) == 2 );
    CHECK( h->GetBinContent(3) == 1 );

    dir.GetObject("test2/histo1", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 10 );
    CHECK( h->GetEntries() == 3 );
    CHECK( h->GetBinContent(1) == 0 );
    CHECK( h->GetBinContent(2) == 1 );
    CHECK( h->GetBinContent(3) == 1 );
    CHECK( h->GetBinContent(4) == 1 );
    CHECK( h->GetBinContent(5) == 0 );

    dir.GetObject("test2/histo2", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 100 );
    CHECK( h->GetEntries() == 8 );
    CHECK( h->GetBinContent(0) == 1 );
    CHECK( h->GetBinContent(1) == 1 );
    CHECK( h->GetBinContent(2) == 1 );
    CHECK( h->GetBinContent(3) == 1 );
    CHECK( h->GetBinContent(4) == 1 );
    CHECK( h->GetBinContent(5) == 0 );
    CHECK( h->GetBinContent(6) == 0 );
    CHECK( h->GetBinContent(10) == 0 );
    CHECK( h->GetBinContent(11) == 1 );
    CHECK( h->GetBinContent(12) == 0 );
    CHECK( h->GetBinContent(100) == 0 );
    CHECK( h->GetBinContent(101) == 2 );

    dir.GetObject("test2/histo3", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 100 );
    CHECK( h->GetEntries() == 8 );
    CHECK( h->GetBinContent(0) == 0.5 );
    CHECK( h->GetBinContent(1) == 0.5 );
    CHECK( h->GetBinContent(2) == 0.5 );
    CHECK( h->GetBinContent(3) == 0.5 );
    CHECK( h->GetBinContent(4) == 0.5 );
    CHECK( h->GetBinContent(5) == 0 );
    CHECK( h->GetBinContent(6) == 0 );
    CHECK( h->GetBinContent(10) == 0 );
    CHECK( h->GetBinContent(11) == 0.5 );
    CHECK( h->GetBinContent(12) == 0 );
    CHECK( h->GetBinContent(100) == 0 );
    CHECK( h->GetBinContent(101) == 1 );
  }
}

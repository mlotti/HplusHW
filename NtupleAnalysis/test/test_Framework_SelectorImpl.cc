#include "catch.hpp"

#include "test_createTree.h"

#include "Framework/interface/SelectorImpl.h"
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/BranchManager.h"
#include "Framework/interface/Exception.h"

#include "TDirectory.h"
#include "TH1F.h"

namespace {
  class SelectorTestSelectorImplEmpty: public BaseSelector {
  public:
    explicit SelectorTestSelectorImplEmpty(const ParameterSet& config, const TH1* skimCounters=nullptr):
      BaseSelector(config) {}
    virtual ~SelectorTestSelectorImplEmpty() {}

    virtual void book(TDirectory *dir) override {}
    virtual void setupBranches(BranchManager& branchManager) override {}
    virtual void process(Long64_t entry) override {}
  };

  class SelectorTestSelectorImpl: public BaseSelector {
  public:
    explicit SelectorTestSelectorImpl(const ParameterSet& config, const TH1* skimCounters=nullptr):
      BaseSelector(config),
      mode(config.getParameter<int>("mode")),
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
      fEvent.setupBranches(branchManager);
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

    const Branch<unsigned long long> *b_event;
    const Branch<std::vector<int> > *b_num1;

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
  SelectorImpl tselector;
  TList inputList;
  tselector.SetInputList(&inputList); // takes pointer to input list
  inputList.Add(new SelectorImplParams(tree->GetEntries(), true, "{}", false));

  SECTION("Single empty selector") {
    inputList.Add(new TNamed("analyzer_test", "SelectorTestSelectorImplEmpty:{}"));
    tree->Process(&tselector);
    TList *output = tselector.GetOutputList();
    REQUIRE( output );
    TObject *tmp = output->FindObject("test");
    REQUIRE( tmp );
    TDirectory *dir = dynamic_cast<TDirectory *>(tmp);
    REQUIRE( dir );
    REQUIRE( dir->Get("counters") );
    REQUIRE( dir->Get("counters/weighted") );
    CHECK( dir->Get("counters/counter") );
    CHECK( dir->Get("counters/weighted/counter") );
    TNamed *config = nullptr;
    dir->GetObject("config", config);
    REQUIRE( config );
    CHECK( config->GetTitle() == std::string("{}") );
  }

  SECTION("Two selectors with same name are not allowed") {
    inputList.Add(new TNamed("analyzer_test", "SelectorTestSelectorImplEmpty:{}"));
    inputList.Add(new TNamed("analyzer_test", "SelectorTestSelectorImplEmpty:{}"));

    REQUIRE_THROWS_AS( tree->Process(&tselector), hplus::Exception );
  }

  SECTION("Two selectors doing some work") {
    inputList.Add(new TNamed("analyzer_test", "SelectorTestSelectorImpl:{\"mode\": 0}"));
    inputList.Add(new TNamed("analyzer_test2", "SelectorTestSelectorImpl:{\"mode\": 1}"));

    tree->Process(&tselector);

    TList *output = tselector.GetOutputList();
    REQUIRE( output );
    TObject *tmp = output->FindObject("test");
    REQUIRE( tmp );
    TDirectory *dir = dynamic_cast<TDirectory *>(tmp);
    REQUIRE( dir );
    TNamed *config = nullptr;
    dir->GetObject("config", config);
    REQUIRE( config );
    CHECK( config->GetTitle() == std::string("{\"mode\": 0}") );

    tmp = output->FindObject("test2");
    REQUIRE( tmp );
    TDirectory *dir2 = dynamic_cast<TDirectory *>(tmp);
    REQUIRE( dir2 );
    dir2->GetObject("config", config);
    REQUIRE( config );
    CHECK( config->GetTitle() == std::string("{\"mode\": 1}") );

    TH1 *h = nullptr;
    dir->GetObject("counters/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 8 );
    CHECK( h->GetBinContent(6) == 3 );
    CHECK( h->GetBinContent(7) == 3 );
    CHECK( h->GetBinContent(8) == 3 );

    dir->GetObject("counters/weighted/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 8 );
    CHECK( h->GetBinContent(6) == 3 );
    CHECK( h->GetBinContent(7) == 3 );
    CHECK( h->GetBinContent(8) == 1.5 );

    dir->GetObject("histo1", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 10 );
    CHECK( h->GetEntries() == 3 );
    CHECK( h->GetBinContent(1) == 0 );
    CHECK( h->GetBinContent(2) == 1 );
    CHECK( h->GetBinContent(3) == 1 );
    CHECK( h->GetBinContent(4) == 1 );
    CHECK( h->GetBinContent(5) == 0 );

    dir->GetObject("histo2", h);
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

    dir->GetObject("histo3", h);
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

    dir2->GetObject("counters/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 8 );
    CHECK( h->GetBinContent(6) == 3 );
    CHECK( h->GetBinContent(7) == 2 );
    CHECK( h->GetBinContent(8) == 2 );

    dir2->GetObject("counters/weighted/counter", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 8 );
    CHECK( h->GetBinContent(6) == 3 );
    CHECK( h->GetBinContent(7) == 2 );
    CHECK( h->GetBinContent(8) == 1 );

    dir2->GetObject("histo1", h);
    REQUIRE( h );
    REQUIRE( h->GetNbinsX() == 10 );
    CHECK( h->GetEntries() == 3 );
    CHECK( h->GetBinContent(1) == 0 );
    CHECK( h->GetBinContent(2) == 1 );
    CHECK( h->GetBinContent(3) == 1 );
    CHECK( h->GetBinContent(4) == 1 );
    CHECK( h->GetBinContent(5) == 0 );

    dir2->GetObject("histo2", h);
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

    dir2->GetObject("histo3", h);
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

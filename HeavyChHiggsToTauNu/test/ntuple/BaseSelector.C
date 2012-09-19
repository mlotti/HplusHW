#include "BaseSelector.h"

#include <TSelector.h>
#include <TStopwatch.h>
#include <TH1F.h>
#include <TDirectory.h>

#include<iostream>
#include<iomanip>
#include<stdexcept>

// EventCounter
EventCounter::Count::Count(EventCounter& ec, size_t index):
  fEventCounter(ec), fIndex(index) {}
EventCounter::Count::~Count() {}

EventCounter::EventCounter(): fWeight(1), counter(0), weightedCounter(0) {}
EventCounter::~EventCounter() {}
EventCounter::Count EventCounter::addCounter(const std::string& name) {
  if(counter)
    throw std::logic_error("May not addCounter() after setOutput()");

  size_t index = labels.size();
  labels.push_back(name);
  values.push_back(0);
  weights.push_back(0);
  weightsSquared.push_back(0);
  return Count(*this, index);
}
void EventCounter::incrementCount(size_t countIndex) {
  values[countIndex] += 1;
  // FIXME: weights...
  weights[countIndex] += fWeight;
  weightsSquared[countIndex] += (fWeight*fWeight);
}
void EventCounter::setOutput(TDirectory *dir) {
  TDirectory *subdir = dir->mkdir("counters");
  subdir->cd();
  counter = new TH1F("counter", "counter", labels.size(), 0, labels.size());
  subdir = subdir->mkdir("weighted");
  subdir->cd();
  weightedCounter = new TH1F("counter", "Weighted counter", labels.size(), 0, labels.size());

  for(size_t i=0; i<labels.size(); ++i) {
    counter->GetXaxis()->SetBinLabel(i+1, labels[i].c_str());
    weightedCounter->GetXaxis()->SetBinLabel(i+1, labels[i].c_str());
  }
}
void EventCounter::serialize() {
  for(size_t i=0; i<labels.size(); ++i) {
    size_t bin = i+1;
    counter->SetBinContent(bin, values[i]);
    weightedCounter->SetBinContent(bin, weights[i]);
    weightedCounter->SetBinError(bin, weightsSquared[i]);
  }
}

// BaseSelector
BaseSelector::BaseSelector() {}
BaseSelector::~BaseSelector() {}

void BaseSelector::setOutput(TDirectory *dir) {
}
void BaseSelector::setupBranches(TTree *tree) {
}

bool BaseSelector::process(Long64_t entry) {
  return true;
}


// TSelector Implementation
class SelectorImp: public TSelector {
public:

  //SelectorImp(TTree * /*tree*/ =0);
  SelectorImp(Long64_t entries);
  SelectorImp(Long64_t entries, BaseSelector *selector);
  virtual ~SelectorImp();
  Int_t   Version() const;
  void    Begin(TTree *tree);
  void    SlaveBegin(TTree *tree);
  void    Init(TTree *tree);
  Bool_t  Notify();
  Bool_t  Process(Long64_t entry);
  void    SlaveTerminate();
  void    Terminate();

  ClassDef(SelectorImp,0);

  void setOutput(TDirectory *dir);

private:
  void printStatus();
  void resetStatus();

  Long64_t                  fEntries;      //! Number of entries in the tree
  Long64_t                  fProcessed;    //! Number of processed entries

  TTree                    *fChain;   //!pointer to the analyzed TTree or TChain
  BaseSelector *fSelector;

  TStopwatch                 fStopwatch;
  Long64_t fPrintStep;
  double fPrintLastTime;
  int fPrintAdaptCount;
};

ClassImp(SelectorImp)

SelectorImp::SelectorImp(Long64_t entries):
  fEntries(entries), fProcessed(0),
  fChain(0), fSelector(new BaseSelector()),
  fPrintStep(20000), fPrintLastTime(0), fPrintAdaptCount(0)
{}

SelectorImp::SelectorImp(Long64_t entries, BaseSelector *selector):
  fEntries(entries), fProcessed(0),
  fChain(0), fSelector(selector),
  fPrintStep(20000), fPrintLastTime(0), fPrintAdaptCount(0)
{}

SelectorImp::~SelectorImp() {
  delete fSelector;
}

Int_t SelectorImp::Version() const {
  return 2;
}

void SelectorImp::Init(TTree *tree) {
  // The Init() function is called when the selector needs to initialize
  // a new tree or chain. Typically here the branch addresses and branch
  // pointers of the tree will be set.
  // It is normally not necessary to make changes to the generated
  // code, but the routine can be extended by the user if needed.
  // Init() will be called many times when running on PROOF
  // (once per file to be processed).

  // Set branch addresses and branch pointers
  if (!tree) return;
  fChain = tree;
  //fChain->SetMakeClass(1);

  // Set up variable and cut branches for the new TTree
  fSelector->setupBranches(tree);
}


Bool_t SelectorImp::Notify() {
  // The Notify() function is called when a new file is opened. This
  // can be either for a new TTree in a TChain or when when a new TTree
  // is started when using PROOF. It is normally not necessary to make changes
  // to the generated code, but the routine can be extended by the
  // user if needed. The return value is currently not used.

  return kTRUE;
}


void SelectorImp::Begin(TTree * /*tree*/) {
  // The Begin() function is called at the start of the query.
  // When running with PROOF Begin() is only called on the client.
  // The tree argument is deprecated (on PROOF 0 is passed).
}

void SelectorImp::SlaveBegin(TTree * /*tree*/) {
  // The SlaveBegin() function is called after the Begin() function.
  // When running with PROOF SlaveBegin() is called on each slave server.
  // The tree argument is deprecated (on PROOF 0 is passed).
}

Bool_t SelectorImp::Process(Long64_t entry) {
  // The Process() function is called for each entry in the tree (or possibly
  // keyed object in the case of PROOF) to be processed. The entry argument
  // specifies which entry in the currently loaded tree is to be processed.
  // It can be passed to either SelectorImp::GetEntry() or TBranch::GetEntry()
  // to read either all or the required parts of the data. When processing
  // keyed objects with PROOF, the object is already loaded and is available
  // via the fObject pointer.
  //
  // This function should contain the "body" of the analysis. It can contain
  // simple or elaborate selection criteria, run algorithms on the data
  // of the event and typically fill histograms.
  //
  // The processing can be stopped by calling Abort().
  //
  // Use fStatus to set the return value of TTree::Process().
  //
  // The return value is currently not used.

  printStatus();
  ++fProcessed;

  bool ret = fSelector->process(entry);
  fStatus = ret;

  return kTRUE;
}

void SelectorImp::SlaveTerminate() {
  // The SlaveTerminate() function is called after all entries or objects
  // have been processed. When running with PROOF SlaveTerminate() is called
  // on each slave server.

  resetStatus();
}

void SelectorImp::Terminate() {
  // The Terminate() function is the last function to be called during
  // a query. It always runs on the client, it can be used to present
  // the results graphically or save the results to file.

  fSelector->terminate();
}

void SelectorImp::setOutput(TDirectory *dir) {
  fSelector->setOutputExt(dir);
}

void SelectorImp::printStatus() {
  if (fProcessed % fPrintStep == 0) {
    double myFraction = static_cast<double>(fProcessed) / static_cast<double>(fEntries);
    std::cout << "\rProcessing ... ";
    
    if (fProcessed == 0) { 
      fStopwatch.Start();
      fPrintLastTime = fStopwatch.RealTime();
      fStopwatch.Continue();
    }
    else {
      // Calculate the time estimate (realTime = totalIime * percent)
      double myRealTime = fStopwatch.RealTime();
      fStopwatch.Continue();

      // adjust the step
      if((myRealTime - fPrintLastTime) < 0.5) {
        fPrintAdaptCount += 1;
        if(fPrintAdaptCount > 2) {
          fPrintStep *= 10; 
          fPrintAdaptCount = 0;
        }
      }
      else if((myRealTime - fPrintLastTime) > 5)
        fPrintStep /= 10;
      fPrintLastTime = myRealTime;

      double myTimeEstimate = myRealTime / myFraction - myRealTime;
      int myHours = static_cast<int>(myTimeEstimate / 3600);
      myTimeEstimate -= static_cast<double>(myHours * 3600);
      int myMinutes = static_cast<int>(myTimeEstimate / 60);
      myTimeEstimate -= static_cast<double>(myMinutes * 60);
      int mySeconds = static_cast<int>(myTimeEstimate);
      std::cout << "estimated time: ";
      if (myHours) {
        std::cout << std::setw(2) << std::setfill('0') << myHours << ":";
      }
      std::cout << std::setw(2) << std::setfill('0') << myMinutes << ":"
                << std::setw(2) << std::setfill('0') << mySeconds << " ";
    }
    std::cout << " (" << std::setprecision(4) << myFraction * 100.0 << " %)   " << std::flush;
  }
}

void SelectorImp::resetStatus() {
  fStopwatch.Stop();
  std::cout << "\rDataset processed (" << fProcessed << " entries). ";
  fStopwatch.Print();
  fPrintStep = 20000;
}

#include "Framework/interface/SelectorImpl.h"
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/BranchManager.h"
#include "Framework/interface/SelectorFactory.h"
#include "Framework/interface/EventSaver.h"

#include "TTree.h"
#include "TFile.h"

#include "boost/property_tree/json_parser.hpp"

#include <iostream>
#include <iomanip>
#include <stdexcept>
#include <sstream>

ClassImp(SelectorImpl)

SelectorImpl::SelectorImpl(TDirectory *outputDir, Long64_t entries, bool isMC, const std::string& options):
  fEntries(entries), fProcessed(0),
  fOutputDir(outputDir), fChain(nullptr),
  fPrintStep(20000), fPrintLastTime(0), fPrintAdaptCount(0), fPrintStatus(true), fIsMC(isMC)
{
  fBranchManager = new BranchManager();

  boost::property_tree::ptree tree;
  std::stringstream ss(options);
  boost::property_tree::read_json(ss, tree);
  fEventSaver = new EventSaver(tree, fOutputDir);
}

SelectorImpl::~SelectorImpl() {
  for(auto& nameSelector: fSelectors)
    delete nameSelector.second;
  delete fBranchManager;
  delete fEventSaver;
}

Int_t SelectorImpl::Version() const {
  return 2;
}

void SelectorImpl::Init(TTree *tree) {
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
  fBranchManager->setTree(tree);
  for(auto& nameSelector: fSelectors)
    nameSelector.second->setupBranches(*fBranchManager);
}


Bool_t SelectorImpl::Notify() {
  // The Notify() function is called when a new file is opened. This
  // can be either for a new TTree in a TChain or when when a new TTree
  // is started when using PROOF. It is normally not necessary to make changes
  // to the generated code, but the routine can be extended by the
  // user if needed. The return value is currently not used.

  auto file = fChain->GetCurrentFile();
  if(fPrintStatus && file)
    std::cout << "Processing file " << file->GetName() << std::endl;

  fEventSaver->beginTree(fChain);

  return kTRUE;
}


void SelectorImpl::Begin(TTree * /*tree*/) {
  // The Begin() function is called at the start of the query.
  // When running with PROOF Begin() is only called on the client.
  // The tree argument is deprecated (on PROOF 0 is passed).
}

void SelectorImpl::SlaveBegin(TTree * /*tree*/) {
  // The SlaveBegin() function is called after the Begin() function.
  // When running with PROOF SlaveBegin() is called on each slave server.
  // The tree argument is deprecated (on PROOF 0 is passed).
}

Bool_t SelectorImpl::Process(Long64_t entry) {
  // The Process() function is called for each entry in the tree (or possibly
  // keyed object in the case of PROOF) to be processed. The entry argument
  // specifies which entry in the currently loaded tree is to be processed.
  // It can be passed to either SelectorImpl::GetEntry() or TBranch::GetEntry()
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

  fEventSaver->beginEvent();
  fBranchManager->setEntry(entry);
  for(auto& nameSelector: fSelectors) {
    //std::cout << "Selector " << nameSelector.first << std::endl;
    nameSelector.second->processInternal(entry);
  }
  fEventSaver->endEvent(entry);

  return kTRUE;
}

void SelectorImpl::SlaveTerminate() {
  // The SlaveTerminate() function is called after all entries or objects
  // have been processed. When running with PROOF SlaveTerminate() is called
  // on each slave server.

  resetStatus();
}

void SelectorImpl::Terminate() {
  // The Terminate() function is the last function to be called during
  // a query. It always runs on the client, it can be used to present
  // the results graphically or save the results to file.

  for(auto& nameSelector: fSelectors) {
    nameSelector.second->terminate();
  }

  fEventSaver->terminate();
}

void SelectorImpl::setPrintStatus(bool status) {
  fPrintStatus = status;
}

void SelectorImpl::addSelector(const std::string& name, const std::string& className, const std::string& config) {
  auto found = std::find_if(fSelectors.begin(), fSelectors.end(), [&](const std::pair<std::string, BaseSelector *>& a) {
      return a.first == name;
    });
  if(found != fSelectors.end())
    throw std::logic_error("Selector with name "+name+" already exists");

  auto selector = SelectorFactory::create(className, config);
  selector->setMCStatus(fIsMC);
  selector->setEventSaver(fEventSaver);
  TDirectory *subdir = fOutputDir->mkdir(name.c_str());
  subdir->cd();
  TNamed *saveConfig = new TNamed("config", config.c_str());
  subdir->Append(saveConfig);
  selector->setOutput(subdir);
  fSelectors.push_back(std::make_pair(name, selector.release()));
}

void SelectorImpl::printStatus() {
  if(!fPrintStatus) return;

  if (fProcessed % fPrintStep == 0) {
    double myFraction = static_cast<double>(fProcessed) / static_cast<double>(fEntries);
    std::cout << "\rProcessing ... ";
    
    Long64_t bytes = 0;
    double timeDiff = 1;
    if (fProcessed == 0) {
      fReadLastTime = TFile::GetFileBytesRead();
      fStopwatch.Start();
      fPrintLastTime = fStopwatch.RealTime();
      fStopwatch.Continue();
    }
    else {
      // Calculate the time estimate (realTime = totalIime * percent)
      double myRealTime = fStopwatch.RealTime();
      fStopwatch.Continue();
      Long64_t readBytes = TFile::GetFileBytesRead();
      bytes = readBytes - fReadLastTime;
      fReadLastTime = readBytes;

      // adjust the step
      timeDiff = myRealTime - fPrintLastTime;
      if(timeDiff < 0.5) {
        fPrintAdaptCount += 1;
        if(fPrintAdaptCount > 2) {
          fPrintStep *= 10; 
          fPrintAdaptCount = 0;
        }
      }
      else if(timeDiff > 5)
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
    std::cout << " (" << std::setprecision(4) << myFraction * 100.0 << " %) at "
              << std::setprecision(3) << (bytes/timeDiff/1024/1024) << " MB/s"
              << "       " // to clear
              << std::flush;
  }
}

void SelectorImpl::resetStatus() {
  if(!fPrintStatus) return;

  fStopwatch.Stop();
  std::cout << "\rDataset processed (" << fProcessed << " entries). ";
  //fStopwatch.Print();
  fPrintStep = 20000;
}

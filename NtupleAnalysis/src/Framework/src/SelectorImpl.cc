#include "Framework/interface/SelectorImpl.h"
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/BranchManager.h"
#include "Framework/interface/SelectorFactory.h"
#include "Framework/interface/EventSaver.h"

#include "TTree.h"
#include "TFile.h"
#include "TProofOutputFile.h"
#include "TIterator.h"

#include "boost/property_tree/json_parser.hpp"

#include <iostream>
#include <iomanip>
#include <stdexcept>
#include <sstream>
#include <unordered_set>

ClassImp(SelectorImplParams)

ClassImp(SelectorImpl)

SelectorImplParams::~SelectorImplParams() {}
const char *SelectorImplParams::GetName() const {
  return "PARAMS";
}

SelectorImpl::SelectorImpl():
  fEntries(-1), fProcessed(0),
  fBranchManager(nullptr), fEventSaver(nullptr),
  fChain(nullptr),
  fProofFile(nullptr), fOutputFile(nullptr),
  fPrintStep(20000), fPrintLastTime(0), fPrintAdaptCount(0), fPrintStatus(false)
{}

SelectorImpl::~SelectorImpl() {
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
  for(BaseSelector *selector: fSelectors)
    selector->setupBranches(*fBranchManager);
}


Bool_t SelectorImpl::Notify() {
  // The Notify() function is called when a new file is opened. This
  // can be either for a new TTree in a TChain or when when a new TTree
  // is started when using PROOF. It is normally not necessary to make changes
  // to the generated code, but the routine can be extended by the
  // user if needed. The return value is currently not used.

  /*
  auto file = fChain->GetCurrentFile();
  if(fPrintStatus && file)
    std::cout << "Processing file " << file->GetName() << std::endl;
  */

  fEventSaver->beginTree(fChain);

  return kTRUE;
}


void SelectorImpl::Begin(TTree * /*tree*/) {
  // The Begin() function is called at the start of the query.
  // When running with PROOF Begin() is only called on the client.
  // The tree argument is deprecated (on PROOF 0 is passed).

  // Check already here that we don't have two analyzers with same names
  // Why here and not SlaveBegin? Because we want the exception thrown in PROOF master

  if(!fInput)
    throw std::runtime_error("No input list to SelectorImpl!");

  if(!dynamic_cast<const SelectorImplParams *>(fInput->FindObject("PARAMS"))) {
    throw std::logic_error("No SelectorImplParams with name PARAMS in the input list");
  }

  std::unordered_set<std::string> analyzerNames;
  TIter next(fInput);
  while(const TObject *obj = next()) {
    if(std::strncmp(obj->GetName(), "analyzer_", 9) == 0) {
      std::string name(obj->GetName());
      name = name.substr(9);
      if(analyzerNames.find(name) != analyzerNames.end())
        throw std::logic_error("Analyzer with name "+name+" already exists");
      analyzerNames.insert(name);
    }
  }
}

void SelectorImpl::SlaveBegin(TTree * /*tree*/) {
  // The SlaveBegin() function is called after the Begin() function.
  // When running with PROOF SlaveBegin() is called on each slave server.
  // The tree argument is deprecated (on PROOF 0 is passed).

  // Pick parameters
  const SelectorImplParams *params = dynamic_cast<const SelectorImplParams *>(fInput->FindObject("PARAMS"));
  fEntries = params->entries();
  fPrintStatus = params->printStatus();

  // Use TProofOutputFile if requested (for PROOF)
  const TNamed *out = dynamic_cast<const TNamed *>(fInput->FindObject("PROOF_OUTPUTFILE_LOCATION"));
  if(out) {
    fProofFile = new TProofOutputFile("histograms.root", "M");
    fProofFile->SetOutputFileName(out->GetTitle());
    fOutputFile = fProofFile->OpenFile("RECREATE");
    fOutputFile->cd();
    fPrintStatus = false;
  }
  else {
    // Use regular file if requested (non-PROOF running)
    out = dynamic_cast<const TNamed *>(fInput->FindObject("OUTPUTFILE_LOCATION"));
    if(out) {
      fOutputFile = TFile::Open(out->GetTitle(), "RECREATE");
      fOutputFile->cd();
    }
  }
  // Otherwise use the fOutput list (unit tests)

  fBranchManager = new BranchManager();

  ParameterSet options(params->options());
  fEventSaver = new EventSaver(options, fOutput);

  TDirectory::AddDirectory(kFALSE);
  TH1::AddDirectory(kFALSE);
  TIter next(fInput);
  while(const TObject *obj = next()) {
    if(std::strncmp(obj->GetName(), "analyzer_", 9) == 0) {
      const TNamed *nm = dynamic_cast<const TNamed *>(obj);
      std::string name(nm->GetName());
      name = name.substr(9);
      std::string title(nm->GetTitle());
      std::string::size_type pos = title.find(":");
      std::string className = title.substr(0, pos);
      std::string config = title.substr(pos+1);

      auto selector = SelectorFactory::create(className, config);
      selector->setMCStatus(params->isMC());
      selector->setEventSaver(fEventSaver);
      TDirectory *subdir = nullptr;
      if(fOutputFile) {
        subdir = fOutputFile->mkdir(name.c_str());
      }
      else {
        subdir = new TDirectory(name.c_str(), name.c_str());
        fOutput->Add(subdir);
      }
      TNamed *saveConfig = new TNamed("config", config.c_str());
      subdir->Append(saveConfig);
      selector->setOutput(subdir);
      fSelectors.push_back(selector.release());
    }
  }
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
  for(BaseSelector *selector: fSelectors) {
    selector->processInternal(entry);
  }
  fEventSaver->endEvent(entry);

  return kTRUE;
}

void SelectorImpl::SlaveTerminate() {
  // The SlaveTerminate() function is called after all entries or objects
  // have been processed. When running with PROOF SlaveTerminate() is called
  // on each slave server.

  resetStatus();

  for(BaseSelector *selector: fSelectors) {
    delete selector;
  }
  fSelectors.clear();

  fEventSaver->terminate();

  delete fEventSaver;
  delete fBranchManager;

  if(fOutputFile) {
    fOutputFile->Write();
    fOutputFile->Close();
    if(fProofFile) {
      fOutput->Add(fProofFile);
    }
  }
  fOutputFile = nullptr;
  fProofFile = nullptr;
}

void SelectorImpl::Terminate() {
  // The Terminate() function is the last function to be called during
  // a query. It always runs on the client, it can be used to present
  // the results graphically or save the results to file.

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
  std::cout << "\rDataset processed (" << fProcessed << " entries). " << std::endl;
  //fStopwatch.Print();
  fPrintStep = 20000;
}

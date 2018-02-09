// -*- c++ -*-
#ifndef Framework_SelectorImpl_h
#define Framework_SelectorImpl_h

#include "Framework/interface/Exception.h"
#include <boost_1_57_0/boost/concept_check.hpp>

#include "TSelector.h"
#include "TStopwatch.h"
#include "TProofServ.h"

#include <string>
#include <vector>

class TDirectory;
class TFile;
class TProofOutputFile;

class BaseSelector;
class BranchManager;
class EventSaver;

class TH1;

class SelectorImplParams: public TObject {
public:
  SelectorImplParams(): fOptions("{}"), fEntries(-1), fIsMC(false), fPrintStatus(false) { }
  SelectorImplParams(Long64_t entries, bool isMC, const std::string& options, bool printStatus):
    fOptions(options), fEntries(entries), fIsMC(isMC), fPrintStatus(printStatus)
  { }
  virtual ~SelectorImplParams();

  virtual const char *GetName() const;

  const std::string& options() const { return fOptions; }
  Long64_t entries() const { return fEntries; }
  bool isMC() const { return fIsMC; }
  bool printStatus() const { return fPrintStatus; }

  ClassDef(SelectorImplParams, 0);

private:
  std::string fOptions;
  Long64_t fEntries;
  bool fIsMC;
  bool fPrintStatus;
};

// TSelector Implementation
class SelectorImpl: public TSelector {
public:

  //SelectorImpl(TTree * /*tree*/ =0);
  SelectorImpl();
  virtual ~SelectorImpl();

  Int_t   Version() const;
  void    Begin(TTree *tree);
  void    SlaveBegin(TTree *tree);
  void    Init(TTree *tree);
  Bool_t  Notify();
  Bool_t  Process(Long64_t entry);
  void    SlaveTerminate();
  void    Terminate();

  ClassDef(SelectorImpl,0);

private:
  SelectorImpl(const SelectorImpl&); // not implemented, not using =delete because of CINT dictionaries

  void printStatus();
  void resetStatus();

  Long64_t                  fEntries;      //! Number of entries in the tree
  Long64_t                  fProcessed;    //! Number of processed entries

  BranchManager *fBranchManager;
  EventSaver *fEventSaver;

  TTree                    *fChain;   //!pointer to the analyzed TTree or TChain

  std::vector<BaseSelector *> fSelectors;

  TProofOutputFile *fProofFile;
  TFile *fOutputFile;

  TStopwatch                 fStopwatch;
  Long64_t fPrintStep;
  Long64_t fReadLastTime;
  double fPrintLastTime;
  int fPrintAdaptCount;
  bool fPrintStatus;

  // Input parameters
  TString fOptionString;
  bool bIsMC;
  
  TH1 *hSkimCounters;
  TH1 *hPUdata;
  TH1 *hPUdataUp;
  TH1 *hPUdataDown;
  TH1 *hPUmc;
  bool bIsttbar;
  bool bIsIntermediateNN;
};

#endif

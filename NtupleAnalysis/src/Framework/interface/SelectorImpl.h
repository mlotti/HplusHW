// -*- c++ -*-
#ifndef Framework_SelectorImpl_h
#define Framework_SelectorImpl_h

#include "TSelector.h"
#include "TStopwatch.h"

#include <string>
#include <vector>
#include <utility>

class TDirectory;

class BaseSelector;
class BranchManager;
class EventSaver;

// TSelector Implementation
class SelectorImpl: public TSelector {
public:

  //SelectorImpl(TTree * /*tree*/ =0);
  SelectorImpl(TDirectory *outputDir, Long64_t entries, bool isMC, const std::string& options);
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

  void setPrintStatus(bool status);

  void addSelector(const std::string& name, const std::string& className, const std::string& config);

private:
  void printStatus();
  void resetStatus();

  Long64_t                  fEntries;      //! Number of entries in the tree
  Long64_t                  fProcessed;    //! Number of processed entries

  BranchManager *fBranchManager;
  EventSaver *fEventSaver;

  TDirectory               *fOutputDir;
  TTree                    *fChain;   //!pointer to the analyzed TTree or TChain
  std::vector<std::pair<std::string, BaseSelector *> > fSelectors;

  TStopwatch                 fStopwatch;
  Long64_t fPrintStep;
  Long64_t fReadLastTime;
  double fPrintLastTime;
  int fPrintAdaptCount;
  bool fPrintStatus;
  bool fIsMC;
};

#endif

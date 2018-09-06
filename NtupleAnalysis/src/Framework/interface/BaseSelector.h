// -*- c++ -*-
#ifndef Framework_BaseSelector_h
#define Framework_BaseSelector_h

#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/EventWeight.h"
#include "Framework/interface/EventCounter.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/EventSaver.h"

#include "DataFormat/interface/Event.h"

#include "Tools/interface/PileupWeight.h"

#include "Rtypes.h"
#include "TBranch.h"
#include "TTree.h"

#include <string>
#include <vector>
#include <algorithm>

class TTree;
class TDirectory;
class TH1;

class BranchManager;

/// Selector base class
class BaseSelector {
public:
  explicit BaseSelector(const ParameterSet& config, const TH1* skimCounters=nullptr);
  virtual ~BaseSelector();

  void setEventSaver(EventSaver *saver) { fEventSaver.setSaver(saver); }

  void setOutput(TDirectory *dir) {
    fEventCounter.setOutput(dir);
    bookInternal(dir);
    book(dir);
  }

  /// Processes internally event before process method is called
  void processInternal(Long64_t entry);

  /// Sets skim counters
  void setSkimCounters(TH1* hSkimCounters);
  
  /// Sets pileup weights
  void setPileUpWeights(TH1* hPUdata,TH1* hPUdataUp, TH1* hPUdataDown, TH1* hPUmc){
    if (iPileupWeightVariation == 1) {
      fPileupWeight.calculateWeights(hPUdataUp,hPUmc);
//      std::cout << "BaseSelector.h is now calculating weights with up variation, iPileupWeightVariation=" << iPileupWeightVariation << std::endl; // debug print
    } else if (iPileupWeightVariation == -1) {
//      std::cout << "BaseSelector.h is now calculating weights with down variation, iPileupWeightVariation=" << iPileupWeightVariation << std::endl; // debug print
      fPileupWeight.calculateWeights(hPUdataDown,hPUmc);
    } else {
//      std::cout << "BaseSelector.h is now calculating weights with nominal variation, iPileupWeightVariation=" << iPileupWeightVariation << std::endl; // debug print
      fPileupWeight.calculateWeights(hPUdata,hPUmc);
    }
  }
  
  /// Sets tflag for ttbar
  void setIsttbar(bool status) { bIsttbar = status; }

  /// Sets tflag for intermediate NoNeutral sample
  void setIsIntermediateNN(bool status) { bIsIntermediateNN = status; }

  /// Book internal histograms
  void bookInternal(TDirectory *dir);
   
  // Implement these
  virtual void book(TDirectory *dir) = 0;
  virtual void setupBranches(BranchManager& branchManager) = 0;
  virtual void process(Long64_t entry) = 0;

protected:
  bool isMC() const { return fIsMC; }
  bool isData() const { return !isMC(); }
  bool isttbar() const { return bIsttbar; }
  bool isIntermediateNN() const { return bIsIntermediateNN; }

  Event fEvent;
  EventWeight fEventWeight;
  EventCounter fEventCounter;
  HistoWrapper fHistoWrapper;
  EventSaverClient fEventSaver;
  PileupWeight fPileupWeight;

private:
  std::vector<Count> processSkimCounters(const TH1* skimCounters);
  
  std::vector<Count> cSkimCounters;
  Count cBaseAllEvents;
  Count cPileupWeighted;
  Count cPrescaled;
  Count cTopPtReweighted;
  Count cExclusiveSamplesWeighted;

  bool bIsttbar;
  bool bIsIntermediateNN;
  float fIntSF;
  int iTopPtVariation;
  int iPileupWeightVariation;
  const bool fIsMC;
    
  // Internal histograms
  WrappedTH1* hNvtxBeforeVtxReweighting;
  WrappedTH1* hNvtxAfterVtxReweighting;
};

#endif

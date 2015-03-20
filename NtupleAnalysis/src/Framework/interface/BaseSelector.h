// -*- c++ -*-
#ifndef Framework_BaseSelector_h
#define Framework_BaseSelector_h

#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/EventWeight.h"
#include "Framework/interface/EventCounter.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/EventSaver.h"
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
  explicit BaseSelector(const ParameterSet& config);
  virtual ~BaseSelector();

  void setEventSaver(EventSaver *saver) { fEventSaver.setSaver(saver); }

  void setOutput(TDirectory *dir) {
    fEventCounter.setOutput(dir);
    book(dir);
  }

  void processInternal(Long64_t entry) {
    fEventWeight.beginEvent();
    if(pileUpWeightPath && pileUpWeightData && pileUpWeightMC)
      fPileupWeight.set(*pileUpWeightPath,*pileUpWeightData,*pileUpWeightMC,this->isData());
    process(entry);
  }

  // Implement these
  virtual void book(TDirectory *dir) = 0;
  virtual void setupBranches(BranchManager& branchManager) = 0;
  virtual void process(Long64_t entry) = 0;

protected:
  bool isMC() const { return fIsMC; }
  bool isData() const { return !isMC(); }

  EventWeight fEventWeight;
  EventCounter fEventCounter;
  HistoWrapper fHistoWrapper;
  EventSaverClient fEventSaver;
  PileupWeight fPileupWeight;

private:
  const bool fIsMC;

  boost::optional<std::string> pileUpWeightPath;
  boost::optional<std::string> pileUpWeightData;
  boost::optional<std::string> pileUpWeightMC;
};

#endif

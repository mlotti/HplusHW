// -*- c++ -*-
#ifndef Framework_BaseSelector_h
#define Framework_BaseSelector_h

#include "Framework/interface/EventWeight.h"
#include "Framework/interface/EventCounter.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/EventSaver.h"

#include "Rtypes.h"
#include "TBranch.h"
#include "TTree.h"

#include "boost/property_tree/ptree.hpp"

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
  explicit BaseSelector(const boost::property_tree::ptree& config);
  virtual ~BaseSelector();

  void setMCStatus(bool isMC_) { fIsMC = isMC_; }
  void setEventSaver(EventSaver *saver) { fEventSaver.setSaver(saver); }

  void setOutput(TDirectory *dir) {
    fEventCounter.setOutput(dir);
    book(dir);
  }

  void processInternal(Long64_t entry) {
    fEventWeight.beginEvent();
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

private:
  bool fIsMC;
};

#endif

// -*- c++ -*-
#include "EventSelection/interface/BaseSelection.h"
#include "DataFormat/interface/EventID.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/EventCounter.h"
#include "EventSelection/interface/CommonPlots.h"
#include "Framework/interface/type.h"
#include "Framework/interface/Exception.h"
#include "Framework/interface/EventWeight.h"
#include "TDirectory.h"

BaseSelection::BaseSelection(EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: fLocalDummyEventWeight(nullptr),
  fLocalDummyEventCounter(nullptr),
  fLocalDummyHistoWrapper(nullptr),
  fEventCounter(eventCounter),
  fHistoWrapper(histoWrapper),
  fCommonPlots(commonPlots),
  sPostfix(postfix),
  fEventNumber(0),
  fLumiNumber(0),
  fRunNumber(0)
{}

BaseSelection::BaseSelection() 
: fLocalDummyEventWeight(new EventWeight()),
  fLocalDummyEventCounter(new EventCounter(*fLocalDummyEventWeight)),
  fLocalDummyHistoWrapper(new HistoWrapper(*fLocalDummyEventWeight, "Never")),
  fEventCounter(*fLocalDummyEventCounter), // Dummy EventCounter with dummy event weight
  fHistoWrapper(*fLocalDummyHistoWrapper), // Dummy HistoWrapper with dummy event weight
  fCommonPlots(nullptr),
  sPostfix(""),
  fEventNumber(0),
  fLumiNumber(0),
  fRunNumber(0)
{}

BaseSelection::~BaseSelection() {
  if (fLocalDummyHistoWrapper != nullptr)
    delete fLocalDummyHistoWrapper;
  if (fLocalDummyEventCounter != nullptr)
    delete fLocalDummyEventCounter;
  if (fLocalDummyEventWeight != nullptr)
    delete fLocalDummyEventWeight;
}

void BaseSelection::ensureAnalyzeAllowed(const EventID& iEventID) {
  if(fEventNumber == iEventID.event() &&
     fLumiNumber == iEventID.lumi() &&
     fRunNumber == iEventID.run()) {
    std::string demangled = type(this);
    throw hplus::Exception("LogicError") << "Called " << demangled << "::analyze() after it has already been called in event " 
                           << fEventNumber << ":" << fLumiNumber << ":" << fRunNumber << ". This is not allowed. (exception from BaseSelection::ensureAnalyzeAllowed())";
  }
  fEventNumber = iEventID.event();
  fLumiNumber = iEventID.lumi();
  fRunNumber = iEventID.run();
}

void BaseSelection::ensureSilentAnalyzeAllowed(const EventID& iEventID) const {
  if(fEventNumber == iEventID.event() &&
     fLumiNumber == iEventID.lumi() &&
     fRunNumber == iEventID.run()) {
    std::string demangled = type(this);
    throw hplus::Exception("LogicError") << "Called " << demangled << "::silentAnalyze() after " << demangled << "::analyze() has already been called in event " 
                                       << fEventNumber << ":" << fLumiNumber << ":" << fRunNumber << ". This is not allowed. (exception from BaseSelection::ensureSilentAnalyzeAllowed())";
  }
}

void BaseSelection::bookHistograms(TDirectory* dir) {
  
}

void BaseSelection::disableHistogramsAndCounters() {
  fHistoWrapper.enable(false);
  fEventCounter.enable(false);  
}

void BaseSelection::enableHistogramsAndCounters() {
  fHistoWrapper.enable(true);
  fEventCounter.enable(true);
}

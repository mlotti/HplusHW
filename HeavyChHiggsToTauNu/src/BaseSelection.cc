#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/Utilities/interface/TypeDemangler.h"

namespace HPlus {
  BaseSelection::BaseSelection(EventCounter& eventCounter, HistoWrapper& histoWrapper): fEventCounter(eventCounter), fHistoWrapper(histoWrapper) {}
  BaseSelection::~BaseSelection() {}

  void BaseSelection::ensureAnalyzeAllowed(const edm::Event& iEvent) {
    if(fEventNumber == iEvent.id().event() && fLumiNumber == iEvent.id().luminosityBlock() && fRunNumber == iEvent.id().run()) {
      std::string demangled;
      edm::typeDemangle(typeid(*this).name(), demangled);
      throw cms::Exception("LogicError") << "Called " << demangled << "::analyze() after it has already been called in event " 
                                         << fEventNumber << ":" << fLumiNumber << ":" << fRunNumber << ". This is not allowed. (exception from BaseSelection::ensureAnalyzeAllowed())" << std::endl;
    }
    fEventNumber = iEvent.id().event();
    fLumiNumber = iEvent.id().luminosityBlock();
    fRunNumber = iEvent.id().run();
  }
  void BaseSelection::ensureSilentAnalyzeAllowed(const edm::Event& iEvent) const {
    if(fEventNumber == iEvent.id().event() && fLumiNumber == iEvent.id().luminosityBlock() && fRunNumber == iEvent.id().run()) {
      std::string demangled;
      edm::typeDemangle(typeid(*this).name(), demangled);
      throw cms::Exception("LogicError") << "Called " << demangled << "::silentAnalyze() after " << demangled << "::analyze() has already been called in event " 
                                         << fEventNumber << ":" << fLumiNumber << ":" << fRunNumber << ". This is not allowed. (exception from BaseSelection::ensureSilentAnalyzeAllowed())" << std::endl;
    }
  }
}

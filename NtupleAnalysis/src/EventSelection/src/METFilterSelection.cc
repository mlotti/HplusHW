// -*- c++ -*-
#include "EventSelection/interface/METFilterSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
//#include "Framework/interface/makeTH.h"

METFilterSelection::Data::Data() 
: bPassedSelection(false) { }

METFilterSelection::Data::~Data() { }

METFilterSelection::METFilterSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  sDiscriminators(config.getParameter<std::vector<std::string>>("discriminators")),
  // Event counter for passing selection
  cPassedMETFilterSelection(eventCounter.addCounter("passed METFilter selection ("+postfix+")"))
{
  // Check discriminator validity
  METFilter dummy;
  dummy.checkDiscriminatorValidity(sDiscriminators);
  // Create sub counters
  for (auto p: sDiscriminators) {
    cSubPassedFilter.push_back(eventCounter.addSubCounter("METFilter selection ("+postfix+")", "Passed "+p) );
  }
}

METFilterSelection::~METFilterSelection() { }

void METFilterSelection::bookHistograms(TDirectory* dir) {
  
}

METFilterSelection::Data METFilterSelection::silentAnalyze(const Event& event) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event);
  enableHistogramsAndCounters();
  return myData;
}

METFilterSelection::Data METFilterSelection::analyze(const Event& event) {
  ensureAnalyzeAllowed(event.eventID());
  METFilterSelection::Data data = privateAnalyze(event);
  // Return data
  return data;
}

METFilterSelection::Data METFilterSelection::privateAnalyze(const Event& iEvent) {
  Data output;
  
  //=== Populate lookup table
  if (!iIndexLUT.size()) {
    for (auto p: sDiscriminators) {
      bool foundStatus = false;
      for (size_t i = 0; i < iEvent.metFilter().getDiscriminatorNames().size(); ++i) {
        if (p == iEvent.metFilter().getDiscriminatorNames()[i]) {
          iIndexLUT.push_back(i);
          foundStatus = true;
        }
      }
      if (!foundStatus) {
        enableHistogramsAndCounters(); // for unit tests
        throw hplus::Exception("config") << "METFilters: could not find requested filter '" << p << "'!";
      }
    }
    if (sDiscriminators.size() != iIndexLUT.size()) {
      enableHistogramsAndCounters(); // for unit tests
      throw hplus::Exception("assert") << "Lookup table size mismatch (size=" 
        << iIndexLUT.size() << ", should be " << sDiscriminators.size() << ")!";
    }
  }
  
  //=== Apply cuts
  output.bPassedSelection = true;
  size_t i = 0;
  while (i < iIndexLUT.size() && output.bPassedSelection) {
    if (iEvent.metFilter().getDiscriminatorValues()[iIndexLUT[i]]()) {
      cSubPassedFilter[i].increment();
    } else {
      output.bPassedSelection = false;
    }
    ++i;
  }
  
  //=== Passed MET filter selection
  if (output.bPassedSelection) {
    cPassedMETFilterSelection.increment();
  }
  
  // Return data object
  return output;
}

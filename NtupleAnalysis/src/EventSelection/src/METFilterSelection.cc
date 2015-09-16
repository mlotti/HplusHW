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
  // Event counter for passing selection
  cSubAll(eventCounter.addSubCounter("METFilter selection ("+postfix+")", "All events")),
  cPassedMETFilterSelection(eventCounter.addCounter("passed METFilter selection ("+postfix+")"))
{
  // Create sub counters
  for (auto p: config.getParameter<std::vector<std::string>>("discriminators")) {
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
  cSubAll.increment();

  //=== Apply cuts
  output.bPassedSelection = true;
  size_t i = 0;
  while (i < iEvent.metFilter().getConfigurableDiscriminatorValues().size() && output.bPassedSelection) {
    if (iEvent.metFilter().getConfigurableDiscriminatorValues()[i]) {
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

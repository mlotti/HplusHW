// -*- c++ -*-
#include "EventSelection/interface/METSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
//#include "Framework/interface/makeTH.h"

METSelection::Data::Data() 
: bPassedSelection(false) { }

METSelection::Data::~Data() { }

const math::XYVectorD& METSelection::Data::getMET() const {
  if (fSelectedMET.size() == 0) {
    throw hplus::Exception("assert") << "No MET stored into result container!";
  }
  return fSelectedMET[0];
}

METSelection::METSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  fMETCut(config, "METCut"),
  bApplyPhiCorrections(config.getParameter<bool>("applyPhiCorrections")),
  // Event counter for passing selection
  cPassedMETSelection(eventCounter.addCounter("passed MET selection ("+postfix+")"))
{
  std::string sType = config.getParameter<std::string>("METType");
  if (sType == "GenMET")
    fMETType = kGenMET;
  else if (sType == "L1MET")
    fMETType = kL1MET;
  else if (sType == "CaloMET")
    fMETType = kCaloMET;
  else if (sType == "type1MET")
    fMETType = kType1MET;
  else {
    throw hplus::Exception("config") << "Invalide MET 'type' chosen in config! Options are: GenMET, L1MET, CaloMET, type1MET";
  }
}

METSelection::~METSelection() { }

void METSelection::bookHistograms(TDirectory* dir) {
  //TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "metSelection_"+sPostfix);
}

METSelection::Data METSelection::silentAnalyze(const Event& event, int nVertices) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, nVertices);
  enableHistogramsAndCounters();
  return myData;
}

METSelection::Data METSelection::analyze(const Event& event, int nVertices) {
  ensureAnalyzeAllowed(event.eventID());
  METSelection::Data data = privateAnalyze(event, nVertices);
  // Send data to CommonPlots
  if (fCommonPlots != nullptr)
    fCommonPlots->fillControlPlotsAtMETSelection(event, data);
  // Return data
  return data;
}

METSelection::Data METSelection::privateAnalyze(const Event& iEvent, int nVertices) {
  Data output;
  // Obtain MET p2 object
  if (fMETType == kGenMET)
    output.fSelectedMET.push_back(iEvent.genMET().p2());
  else if (fMETType == kL1MET)
    output.fSelectedMET.push_back(iEvent.L1met().p2());
  else if (fMETType == kCaloMET)
    output.fSelectedMET.push_back(iEvent.calomet().p2());
  else if (fMETType == kType1MET)
    output.fSelectedMET.push_back(iEvent.met_Type1().p2());
  
  //=== Apply phi corrections // FIXME: not implemented
  
  //=== Apply cut on MET
  if (!fMETCut.passedCut(output.getMET().R()))
    return output;
  
  //=== Passed MET selection
  output.bPassedSelection = true;
  cPassedMETSelection.increment();
  
  // Return data object
  return output;
}

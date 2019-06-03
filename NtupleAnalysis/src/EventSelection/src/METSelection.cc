// -*- c++ -*-
#include "EventSelection/interface/METSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
//#include "Framework/interface/makeTH.h"

METSelection::Data::Data() 
: bPassedSelection(false),
  fMETSignificance(-1.0),
  fMETTriggerSF(0.0)
{ }

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
  fMETSignificanceCut(config, "METSignificanceCut"),
  bApplyPhiCorrections(config.getParameter<bool>("applyPhiCorrections")),
  // MET trigger SF
  fMETTriggerSFReader(config.getParameterOptional<ParameterSet>("metTriggerSF")),
  // Event counter for passing selection
  cPassedMETSelection(fEventCounter.addCounter("passed MET selection ("+postfix+")"))
{
  initialize(config);
}

METSelection::METSelection(const ParameterSet& config)
: BaseSelection(),
  fMETCut(config, "METCut"),
  fMETSignificanceCut(config, "METSignificanceCut"),
  bApplyPhiCorrections(config.getParameter<bool>("applyPhiCorrections")),
  // MET trigger SF
  fMETTriggerSFReader(config.getParameterOptional<ParameterSet>("metTriggerSF")),
  // Event counter for passing selection
  cPassedMETSelection(fEventCounter.addCounter("passed MET selection"))
{
  initialize(config);
  bookHistograms(new TDirectory());
}

METSelection::~METSelection() { }

void METSelection::initialize(const ParameterSet& config) {
  std::string sType = config.getParameter<std::string>("METType");
  if (sType == "GenMET")
    fMETType = kGenMET;
  else if (sType == "L1MET")
    fMETType = kL1MET;
  else if (sType == "HLTMET")
    fMETType = kHLTMET;
  else if (sType == "CaloMET")
    fMETType = kCaloMET;
  else if (sType == "MET_Type1")
    fMETType = kType1MET;
  else if (sType == "MET_Type1_NoHF")
    fMETType = kType1MET_noHF;
  else if (sType == "MET_Puppi")
    fMETType = kPuppiMET;
  else {
    throw hplus::Exception("config") << "Invalid MET 'type' chosen in config! Options are: MET_Type1, MET_Type1_NoHF, MET_Puppi, GenMET, L1MET, HLTMET, CaloMET";
  }
}

void METSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "metSelection_"+sPostfix);
  hMet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "Met", "Met", 100, 0, 1000);


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
//   if (fMETType == kGenMET)
//     output.fSelectedMET.push_back(iEvent.genMET().p2());
//   else if (fMETType == kL1MET)
//     output.fSelectedMET.push_back(iEvent.L1met().p2());
//   else if (fMETType == kCaloMET)
//     output.fSelectedMET.push_back(iEvent.calomet().p2());
//   else if (fMETType == kType1MET)
//     output.fSelectedMET.push_back(iEvent.met_Type1().p2());
  output.fSelectedMET.push_back(iEvent.met().p2());
  output.fMETSignificance = iEvent.met().significance();
  
  //=== Apply phi corrections // FIXME: not implemented
  
  // Set tau trigger SF value to data object
  double metValue = output.getMET().R();
  if (iEvent.isMC()) {
//    output.fMETTriggerSF = fMETTriggerSFReader.getScaleFactorValue(metValue);
  } 
  hMet->Fill(metValue);
  
  //=== Apply cut on MET
  if (!fMETCut.passedCut(metValue))
    return output;
  
  //=== Apply cut on MET significance
  if (!fMETSignificanceCut.passedCut(iEvent.met().significance()))
    return output;
  
  //=== Passed MET selection
  output.bPassedSelection = true;
  cPassedMETSelection.increment();  
 
  // Return data object
  return output;
}

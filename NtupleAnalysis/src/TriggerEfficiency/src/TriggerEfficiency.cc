#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "DataFormat/interface/Event.h"

#include "TH1F.h"
#include "TDirectory.h"

#include "TriggerEfficiency/interface/TauLegSelection.h"
#include "TriggerEfficiency/interface/METLegSelection.h"


class TriggerEfficiency: public BaseSelector {
public:
  explicit TriggerEfficiency(const ParameterSet& config, const TH1* skimCounters);
  virtual ~TriggerEfficiency();

  virtual void book(TDirectory *dir) override;
  virtual void setupBranches(BranchManager& branchManager) override;
  virtual void process(Long64_t entry) override;

private:
  std::string fName;

  const std::string fOfflineSelection;
  std::vector<int> fbinning;
  std::string fxLabel;
  std::string fyLabel;
  /*
  std::string fdataera;
  float flumi;
  int frunMin;
  int frunMax;
  std::string fsample1;
  std::string fsample2;
  std::vector<std::string> fcontrolTriggers1;
  std::vector<std::string> fcontrolTriggers2;
  std::vector<std::string> fsignalTriggers1;
  std::vector<std::string> fsignalTriggers2;
  */
  ParameterSet fcontrolTriggers;

  TrgBaseSelection* selection;

  Count cAllEvents;
  Count cRunRange;
  Count cSelection;
  Count cCtrlTrigger;
  Count cSignalTrigger;

  WrappedTH1 *hNum;
  WrappedTH1 *hDen;
  WrappedTH1 *hNeg;

  WrappedTH1 *hNumEta;
  WrappedTH1 *hDenEta;

  WrappedTH1 *hNumPhi;
  WrappedTH1 *hDenPhi;

  WrappedTH1 *hNumPU;
  WrappedTH1 *hDenPU;

  WrappedTH1 *hNumMCMatch;
  WrappedTH1 *hDenMCMatch;

  WrappedTH1 *hPull;
  WrappedTH1 *hSub;
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(TriggerEfficiency);

TriggerEfficiency::TriggerEfficiency(const ParameterSet& config, const TH1* skimCounters):
  BaseSelector(config, skimCounters),
  fName(config.getParameter<std::string>("name")),
  fOfflineSelection(config.getParameter<std::string>("offlineSelection")),
  fbinning(config.getParameter<std::vector<int>>("binning")),
  fxLabel(config.getParameter<std::string>("xLabel")),
  fyLabel(config.getParameter<std::string>("yLabel")),          
  /*
  fdataera(config.getParameter<std::string>("dataera")),
  flumi(config.getParameter<float>("lumi")),
  frunMin(config.getParameter<int>("runMin")),
  frunMax(config.getParameter<int>("runMax")),
  fsample1(config.getParameter<std::string>("sample1")),
  fsample2(config.getParameter<std::string>("sample2")),
  fcontrolTriggers1(config.getParameter<std::vector<std::string>>("controlTriggers1")),
  fcontrolTriggers2(config.getParameter<std::vector<std::string>>("controlTriggers2")),
  fsignalTriggers1(config.getParameter<std::vector<std::string>>("signalTriggers1")),
  fsignalTriggers2(config.getParameter<std::vector<std::string>>("signalTriggers2")),
  */

  fcontrolTriggers(config.getParameter<ParameterSet>("Trigger")),                                                                       

  cAllEvents(fEventCounter.addCounter("All events")),
  cRunRange(fEventCounter.addCounter("RunRange")),
  cSelection(fEventCounter.addCounter("OfflineSelection")),
  cCtrlTrigger(fEventCounter.addCounter("CtrlTrigger")),
  cSignalTrigger(fEventCounter.addCounter("SignalTrigger"))
{
  std::cout << "    Analyzer " << fName << ", offline selection " << fOfflineSelection << std::endl;
  std::vector<std::string> ctrltriggers = fcontrolTriggers.getParameter<std::vector<std::string>>("triggerOR");
  for(std::vector<std::string>::const_iterator i = ctrltriggers.begin(); i != ctrltriggers.end(); ++i)
  std::cout << "        CtrlTrigger    " <<  *i << std::endl;
  std::vector<std::string> signaltriggers = fcontrolTriggers.getParameter<std::vector<std::string>>("triggerOR2");
  for(std::vector<std::string>::const_iterator i = signaltriggers.begin(); i != signaltriggers.end(); ++i)
  std::cout << "        SignalTrigger  " <<  *i << std::endl;
  if(fOfflineSelection == "taulegSelection") selection = new TauLegSelection(config,fEventCounter,fHistoWrapper);
  if(fOfflineSelection == "metlegSelection") selection = new METLegSelection(config,fEventCounter,fHistoWrapper);
}

TriggerEfficiency::~TriggerEfficiency(){
  std::cout << std::endl;
  std::cout << "    Analyzer " << fName << std::endl;
  std::cout << "    All events    " << cAllEvents.value() << std::endl;
  std::cout << "    Run range     " << cRunRange.value() << std::endl;
  std::cout << "    CtrlTrigger   " << cCtrlTrigger.value() << std::endl;
  selection->print();
  std::cout << "    OfflSelection " << cSelection.value() << std::endl;
  std::cout << "    SignalTrigger " << cSignalTrigger.value() << std::endl;
}

void TriggerEfficiency::book(TDirectory *dir) {

  Double_t* xbins;
  xbins = new Double_t[fbinning.size()];
  for(size_t i = 0; i < fbinning.size(); ++i){
    xbins[i] = fbinning[i];
  }

  hNum = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Numerator", "Numerator", fbinning.size()-1, xbins);
  hNum->GetXaxis()->SetTitle(fxLabel.c_str());

  hDen = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Denominator", "Denominator", fbinning.size()-1, xbins);  
  hDen->GetXaxis()->SetTitle(fxLabel.c_str());

  hNeg = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "NegativeWeight", "NegativeWeight", fbinning.size()-1, xbins);
  hNeg->GetXaxis()->SetTitle(fxLabel.c_str());

  hNumEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "NumeratorEta", "NumeratorEta", 7,-2.1, 2.1);
  hNumEta->GetXaxis()->SetTitle(fxLabel.c_str());

  hDenEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DenominatorEta", "DenominatorEta", 7,-2.1, 2.1);
  hDenEta->GetXaxis()->SetTitle(fxLabel.c_str());

  hNumPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "NumeratorPhi", "NumeratorPhi", 7,-3.14, 3.14);
  hNumPhi->GetXaxis()->SetTitle(fxLabel.c_str());

  hDenPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DenominatorPhi", "DenominatorPhi", 7,-3.14, 3.14);
  hDenPhi->GetXaxis()->SetTitle(fxLabel.c_str());

  hNumPU = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "NumeratorPU", "NumeratorPU", 7, 5, 40.);
  hNumPU->GetXaxis()->SetTitle("nVtx");

  hDenPU = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DenominatorPU", "DenominatorPU", 7, 5, 40.);
  hDenPU->GetXaxis()->SetTitle("nVtx");

  hNumMCMatch = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "NumeratorMCMatch", "NumeratorMCMatch", fbinning.size()-1, xbins);
  hNumMCMatch->GetXaxis()->SetTitle(fxLabel.c_str());

  hDenMCMatch = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DenominatorMCMatch", "DenominatorMCMatch", fbinning.size()-1, xbins);
  hDenMCMatch->GetXaxis()->SetTitle(fxLabel.c_str());

  hPull = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Pull", "Pull", 10, -1., 1.);
  hSub  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Sub", "Sub", 10, -50, 50);

  selection->bookHistograms(dir);
}

void TriggerEfficiency::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void TriggerEfficiency::process(Long64_t entry) {

  cAllEvents.increment();

  if(!selection->passedRunRange(fEvent,this->isData())) return;
  cRunRange.increment();

  if(!selection->passedCtrlTtrigger(fEvent)) return;
  cCtrlTrigger.increment();

  if(selection->offlineSelection(fEvent)){
    cSelection.increment();

    double xvariable = selection->xVariable();
    hDen->Fill(xvariable);
    if(selection->mcMatch()) hDenMCMatch->Fill(xvariable);
    if(fEventWeight.getWeight() < 0) hNeg->Fill(xvariable,1);
    if(selection->onlineSelection(fEvent)) {
      hNum->Fill(xvariable);
      hPull->Fill(selection->pull());
      hSub->Fill(selection->sub());
      if(selection->mcMatch()) hNumMCMatch->Fill(xvariable);
      cSignalTrigger.increment();
    }
  }
  if(selection->offlineSelection(fEvent,eta)){ // eff vs eta
    double xvariable = selection->xVariable();
    hDenEta->Fill(xvariable);
    if(selection->onlineSelection(fEvent)) {
      hNumEta->Fill(xvariable);
    }
  }
  if(selection->offlineSelection(fEvent,phi)){ // eff vs phi
    double xvariable = selection->xVariable();
    hDenPhi->Fill(xvariable);
    if(selection->onlineSelection(fEvent)) {
      hNumPhi->Fill(xvariable);
    }
  }
  if(selection->offlineSelection(fEvent,pu)){ // eff vs nVtx
    double xvariable = selection->xVariable();
    hDenPU->Fill(xvariable);
    if(selection->onlineSelection(fEvent)) {
      hNumPU->Fill(xvariable);
    }
  }
}

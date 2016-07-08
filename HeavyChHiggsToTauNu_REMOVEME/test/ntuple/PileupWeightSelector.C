#include "BaseSelector.h"
#include "Branches.h"

#include "TDirectory.h"
#include "TH1F.h"
#include "TF1.h"

#include<iostream>
#include<vector>
#include<string>

class PileupWeightSelector: public BaseSelector {
public:
  PileupWeightSelector(const TH1 *weights, const TH1 *weightsUp, const TH1 *weightsDown);
  PileupWeightSelector(const TH1 *weights, const TH1 *weightsUp, const TH1 *weightsDown,
                       const std::vector<std::string>& topPtNames,
                       const std::vector<std::string>& topPtFormulasAllHadr,
                       const std::vector<std::string>& topPtFormulasSemiLep,
                       const std::vector<std::string>& topPtFormulasDiLep);
  ~PileupWeightSelector();

  void setOutput(TDirectory *dir);
  void setupBranches(BranchManager& branchManager);
  bool process(Long64_t entry);

private:
  Branch<float> *fTrueNumInteractions;
  Branch<float> *fTopPt;
  Branch<float> *fTopBarPt;
  Branch<int> *fTopNumLeptons;

  const TH1 *fWeights;
  const TH1 *fWeightsUp;
  const TH1 *fWeightsDown;

  const std::vector<std::string> fTopPtNames;
  const std::vector<TF1> fTopPtFormulasAllHadr;
  const std::vector<TF1> fTopPtFormulasSemiLep;
  const std::vector<TF1> fTopPtFormulasDiLep;

  TH1 *hEvents;
  TH1 *hEventsUp;
  TH1 *hEventsDown;

  struct TopPtHistos {
    TH1 *hEventsTopPtOnly;
    TH1 *hEventsTopPtOnlyUp;
    TH1 *hEventsTopPtOnlyDown;

    TH1 *hEventsTopPt;
    TH1 *hEventsTopPtUp;
    TH1 *hEventsTopPtDown;

    TH1 *hEventsUpTopPt;
    TH1 *hEventsUpTopPtUp;
    TH1 *hEventsUpTopPtDown;

    TH1 *hEventsDownTopPt;
    TH1 *hEventsDownTopPtUp;
    TH1 *hEventsDownTopPtDown;
  };
  std::vector<TopPtHistos> fTopPtHistos;

};

PileupWeightSelector::PileupWeightSelector(const TH1 *weights, const TH1 *weightsUp, const TH1 *weightsDown):
  fWeights(weights),
  fWeightsUp(weightsUp),
  fWeightsDown(weightsDown)
{}

namespace {
  std::vector<TF1> convert(const std::vector<std::string>& names, const std::string& postfix, const std::vector<std::string>& formulas) {
    std::vector<TF1> ret;
    ret.reserve(formulas.size());
    for(size_t i=0; i<formulas.size(); ++i)
      ret.push_back(TF1((names[i]+postfix).c_str(), formulas[i].c_str()));
    return ret;
  }

  TH1D *makeTH(const char *name) {
    return new TH1D(name, name, 1, 0, 1);
  }

  void increase(TH1 *histo, double weight) {
    histo->SetBinContent(1, histo->GetBinContent(1)+weight);
  }
}

PileupWeightSelector::PileupWeightSelector(const TH1 *weights, const TH1 *weightsUp, const TH1 *weightsDown,
                                           const std::vector<std::string>& topPtNames,
                                           const std::vector<std::string>& topPtFormulasAllHadr,
                                           const std::vector<std::string>& topPtFormulasSemiLep,
                                           const std::vector<std::string>& topPtFormulasDiLep):
  fWeights(weights),
  fWeightsUp(weightsUp),
  fWeightsDown(weightsDown),
  fTopPtNames(topPtNames),
  fTopPtFormulasAllHadr(convert(topPtNames, "AllHadr", topPtFormulasAllHadr)),
  fTopPtFormulasSemiLep(convert(topPtNames, "SemiLep", topPtFormulasSemiLep)),
  fTopPtFormulasDiLep(convert(topPtNames, "DiLep", topPtFormulasDiLep))
{
  fTopPtHistos.reserve(fTopPtNames.size());
}

PileupWeightSelector::~PileupWeightSelector() {}

void PileupWeightSelector::setOutput(TDirectory *dir) {
  if(dir)
    dir->cd();

  hEvents = makeTH("events");
  hEventsUp = makeTH("eventsUp");
  hEventsDown = makeTH("eventsDown");

  for(size_t i=0; i<fTopPtNames.size(); ++i) {
    fTopPtHistos[i].hEventsTopPtOnly = makeTH(("events_topPtOnly_"+fTopPtNames[i]).c_str());
    fTopPtHistos[i].hEventsTopPtOnlyUp = makeTH(("events_topPtOnlyUp_"+fTopPtNames[i]).c_str());
    fTopPtHistos[i].hEventsTopPtOnlyDown = makeTH(("events_topPtOnlyDown_"+fTopPtNames[i]).c_str());

    fTopPtHistos[i].hEventsTopPt = makeTH(("events_topPt_"+fTopPtNames[i]).c_str());
    fTopPtHistos[i].hEventsTopPtUp = makeTH(("events_topPtUp_"+fTopPtNames[i]).c_str());
    fTopPtHistos[i].hEventsTopPtDown = makeTH(("events_topPtDown_"+fTopPtNames[i]).c_str());

    fTopPtHistos[i].hEventsUpTopPt = makeTH(("eventsUp_topPt_"+fTopPtNames[i]).c_str());
    fTopPtHistos[i].hEventsUpTopPtUp = makeTH(("eventsUp_topPtUp_"+fTopPtNames[i]).c_str());
    fTopPtHistos[i].hEventsUpTopPtDown = makeTH(("eventsUp_topPtDown_"+fTopPtNames[i]).c_str());

    fTopPtHistos[i].hEventsDownTopPt = makeTH(("eventsDown_topPt_"+fTopPtNames[i]).c_str());
    fTopPtHistos[i].hEventsDownTopPtUp = makeTH(("eventsDown_topPtUp_"+fTopPtNames[i]).c_str());
    fTopPtHistos[i].hEventsDownTopPtDown = makeTH(("eventsDown_topPtDown_"+fTopPtNames[i]).c_str());
  }
}

void PileupWeightSelector::setupBranches(BranchManager& branchManager) {
  branchManager.book("TrueNumInteractions", &fTrueNumInteractions);
  if(!fTopPtNames.empty()) {
    branchManager.book("TopPt", &fTopPt);
    branchManager.book("TopBarPt", &fTopBarPt);
    branchManager.book("TopEventClass", &fTopNumLeptons);
  }
}

bool PileupWeightSelector::process(Long64_t entry) {
  // PU nominal
  Int_t bin = fWeights->FindFixBin(fTrueNumInteractions->value());
  double weight = fWeights->GetBinContent(bin);
  increase(hEvents, weight);

  // PU up
  bin = fWeightsUp->FindFixBin(fTrueNumInteractions->value());
  double weightUp = fWeightsUp->GetBinContent(bin);
  increase(hEventsUp, weightUp);

  // PU down
  bin = fWeightsDown->FindFixBin(fTrueNumInteractions->value());
  double weightDown = fWeightsDown->GetBinContent(bin);
  increase(hEventsDown, weightDown);

  int numLeptons = -1;
  if(!fTopPtNames.empty())
    numLeptons = fTopNumLeptons->value();

  for(size_t i=0; i<fTopPtNames.size(); ++i) {
    double topPtWeight = 1.0;
    switch(numLeptons) {
    case 0: topPtWeight = fTopPtFormulasAllHadr[i].Eval(fTopPt->value()) * fTopPtFormulasAllHadr[i].Eval(fTopBarPt->value()); break;
    case 1: topPtWeight = fTopPtFormulasSemiLep[i].Eval(fTopPt->value()) * fTopPtFormulasSemiLep[i].Eval(fTopBarPt->value()); break;
    case 2: topPtWeight = fTopPtFormulasDiLep[i].Eval(fTopPt->value())   * fTopPtFormulasDiLep[i].Eval(fTopBarPt->value()); break;
    default: std::cout << "Number of leptons " << numLeptons << std::endl;
    }
    double topPtWeightDown = 1.0;
    double topPtWeightUp = topPtWeight*topPtWeight;

    increase(fTopPtHistos[i].hEventsTopPtOnly,     topPtWeight);
    increase(fTopPtHistos[i].hEventsTopPtOnlyUp,   topPtWeightUp);
    increase(fTopPtHistos[i].hEventsTopPtOnlyDown, topPtWeightDown);

    increase(fTopPtHistos[i].hEventsTopPt,     weight*topPtWeight);
    increase(fTopPtHistos[i].hEventsTopPtUp,   weight*topPtWeightUp);
    increase(fTopPtHistos[i].hEventsTopPtDown, weight*topPtWeightDown);

    increase(fTopPtHistos[i].hEventsUpTopPt,     weightUp*topPtWeight);
    increase(fTopPtHistos[i].hEventsUpTopPtUp,   weightUp*topPtWeightUp);
    increase(fTopPtHistos[i].hEventsUpTopPtDown, weightUp*topPtWeightDown);

    increase(fTopPtHistos[i].hEventsDownTopPt,     weightDown*topPtWeight);
    increase(fTopPtHistos[i].hEventsDownTopPtUp,   weightDown*topPtWeightUp);
    increase(fTopPtHistos[i].hEventsDownTopPtDown, weightDown*topPtWeightDown);
  }

  return true;
}

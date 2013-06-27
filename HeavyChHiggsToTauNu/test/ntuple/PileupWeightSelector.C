#include "BaseSelector.h"
#include "Branches.h"

#include "TDirectory.h"
#include "TH1F.h"

#include<iostream>

class PileupWeightSelector: public BaseSelector {
public:
  PileupWeightSelector(const TH1 *weights, const TH1 *weightsUp, const TH1 *weightsDown);
  ~PileupWeightSelector();

  void setOutput(TDirectory *dir);
  void setupBranches(BranchManager& branchManager);
  bool process(Long64_t entry);

private:
  Branch<float> *fTrueNumInteractions;

  const TH1 *fWeights;
  const TH1 *fWeightsUp;
  const TH1 *fWeightsDown;

  TH1 *hEvents;
  TH1 *hEventsUp;
  TH1 *hEventsDown;
};

PileupWeightSelector::PileupWeightSelector(const TH1 *weights, const TH1 *weightsUp, const TH1 *weightsDown):
  fWeights(weights),
  fWeightsUp(weightsUp),
  fWeightsDown(weightsDown)
{}

PileupWeightSelector::~PileupWeightSelector() {}

void PileupWeightSelector::setOutput(TDirectory *dir) {
  if(dir)
    dir->cd();

  hEvents = new TH1D("events", "events", 1, 0, 1);
  hEventsUp = new TH1D("eventsUp", "eventsUp", 1, 0, 1);
  hEventsDown = new TH1D("eventsDown", "eventsUp", 1, 0, 1);
}

void PileupWeightSelector::setupBranches(BranchManager& branchManager) {
  branchManager.book("TrueNumInteractions", fTrueNumInteractions);
}

bool PileupWeightSelector::process(Long64_t entry) {
  fTrueNumInteractions.setEntry(entry);

  Int_t bin = fWeights->FindFixBin(fTrueNumInteractions->value());
  double weight = fWeights->GetBinContent(bin);
  hEvents->SetBinContent(1, hEvents->GetBinContent(1)+weight);

  bin = fWeightsUp->FindFixBin(fTrueNumInteractions->value());
  weight = fWeightsUp->GetBinContent(bin);
  hEventsUp->SetBinContent(1, hEventsUp->GetBinContent(1)+weight);

  bin = fWeightsDown->FindFixBin(fTrueNumInteractions->value());
  weight = fWeightsDown->GetBinContent(bin);
  hEventsDown->SetBinContent(1, hEventsDown->GetBinContent(1)+weight);

  return true;
}

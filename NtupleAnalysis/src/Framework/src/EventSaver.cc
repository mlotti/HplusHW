#include "Framework/interface/EventSaver.h"

#include "TList.h"
#include "TEntryList.h"
#include "TTree.h"

#include "boost/optional.hpp"

#include <ostream>

namespace {
  bool isEnabled(const ParameterSet& config, std::string parameter = "EventSaver.enabled") {
    boost::optional<bool> enabled = config.getParameterOptional<bool>(parameter);
    return enabled && *enabled;
  }
}

EventSaver::EventSaver(const ParameterSet& config, TList *outputList, std::string pOUT):
  fEnabled(isEnabled(config)),
  fSave(false),
  fPickEvents(isEnabled(config,"EventSaver.pickEvents")),
  fEntryList(nullptr)
{
  if(!fEnabled) return;

  if(fPickEvents) {
    if(pOUT[pOUT.length()-1] != '/') pOUT += "/";
    fPickEventsFile = pOUT + config.getParameter<std::string>("EventSaver.pickEventsFile","pickEvents.txt");
  }
  fEntryList = new TEntryList("entrylist", "List of selected entries");
  outputList->Add(fEntryList);
}

EventSaver::~EventSaver() {}

void EventSaver::beginTree(TTree *tree) {
  if(!fEnabled) return;
  fEntryList->SetTree(tree);
  fTree = tree;
}

void EventSaver::endEvent(Long64_t entry) {
  if(!fEnabled) return;
  if(!fSave) return;

  fEntryList->Enter(entry);
}

void EventSaver::terminate() {
  if(fEntryList)
    fEntryList->OptimizeStorage();

  if(fEntryList && fPickEvents){

    unsigned long long event;
    unsigned int run,lumi;

    fTree->SetBranchAddress("event",&event);
    fTree->SetBranchAddress("run",&run);
    fTree->SetBranchAddress("lumi",&lumi);

    int N = fEntryList->GetN();
    if(N > 0) {
      std::ofstream fOUT(fPickEventsFile);
      for(int i = 0; i < N; ++i){
	if(i == 0 || i == N-1 || (i+1)%10 == 0) std::cout << "\rWriting pickEvents " << i+1 << " (" << 100*float(i)/N << "%)  ";
	long entry = fEntryList->GetEntry(i);
	fTree->GetEntry(entry);
	fOUT << run << ":" << lumi << ":" << event << std::endl;
      }
      fOUT.close();
      std::cout << "...saved in " << fPickEventsFile << std::endl;
    }
    else
      std::cout << "PickEvents enabled, but no events passed selection. " << std::endl;
  }
}

#include "Framework/interface/EventSaver.h"

#include "TList.h"
#include "TEntryList.h"

#include "boost/optional.hpp"

namespace {
  bool isEnabled(const ParameterSet& config) {
    boost::optional<bool> enabled = config.getParameterOptional<bool>("EventSaver.enabled");
    return enabled && *enabled;
  }
}

EventSaver::EventSaver(const ParameterSet& config, TList *outputList):
  fEnabled(isEnabled(config)),
  fSave(false),
  fEntryList(nullptr)
{
  if(!fEnabled) return;

  fEntryList = new TEntryList("entrylist", "List of selected entries");
  outputList->Add(fEntryList);
}

EventSaver::~EventSaver() {}

void EventSaver::beginTree(const TTree *tree) {
  if(!fEnabled) return;
  fEntryList->SetTree(tree);
}

void EventSaver::endEvent(Long64_t entry) {
  if(!fEnabled) return;
  if(!fSave) return;

  fEntryList->Enter(entry);
}

void EventSaver::terminate() {
  if(fEntryList)
    fEntryList->OptimizeStorage();
}

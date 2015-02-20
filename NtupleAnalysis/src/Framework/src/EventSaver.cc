#include "Framework/interface/EventSaver.h"

#include "TDirectory.h"
#include "TFile.h"
#include "TEntryList.h"

#include "boost/optional.hpp"

namespace {
  bool isEnabled(const boost::property_tree::ptree& config) {
    boost::optional<bool> enabled = config.get_optional<bool>("EventSaver.enabled");
    return enabled && *enabled;
  }
}

EventSaver::EventSaver(const boost::property_tree::ptree& config, TDirectory *histoOutputDir):
  fEnabled(isEnabled(config)),
  fSave(false),
  fOutput(nullptr),
  fOutputFile(nullptr),
  fEntryList(nullptr)
{
  if(!fEnabled) return;

  TFile *outputFile = histoOutputDir->GetFile();

  if(!outputFile) {
    fOutput = histoOutputDir;
  }
  else {
    std::string fname = outputFile->GetName();
    fname.replace(fname.rfind(".root"), 5, "-entrylist.root");
    fOutputFile = TFile::Open(fname.c_str(), "RECREATE");
    fOutput = fOutputFile;
  }

  fOutput->cd();
  fEntryList = new TEntryList("entrylist", "List of selected entries");
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
  if(fOutputFile) {
    fOutputFile->Write();
    fOutputFile->Close();
    delete fOutputFile;
  }
}

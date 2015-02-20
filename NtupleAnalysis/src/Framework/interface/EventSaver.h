#ifndef Framework_EventSaver_h
#define Framework_EventSaver_h

#include "Rtypes.h"

#include "boost/property_tree/ptree.hpp"

class TDirectory;
class TEntryList;
class TTree;
class TFile;

class EventSaver {
public:
  explicit EventSaver(const boost::property_tree::ptree& config, TDirectory *histoOutputDir);
  ~EventSaver();

  void beginTree(const TTree *tree);
  void beginEvent() { fSave = false; }
  void endEvent(Long64_t entry);

  void save() { fSave = true; }

  void terminate();

private:
  const bool fEnabled;
  bool fSave;

  TDirectory *fOutput;
  TFile *fOutputFile;
  TEntryList *fEntryList;
};

class EventSaverClient {
public:
  EventSaverClient() {}
  ~EventSaverClient() {}

  void setSaver(EventSaver *saver) { fSaver = saver; }

  void save() { fSaver->save(); }

private:
  EventSaver *fSaver;
};

#endif

#ifndef Framework_EventSaver_h
#define Framework_EventSaver_h

#include "Framework/interface/ParameterSet.h"

#include "Rtypes.h"

class TDirectory;
class TEntryList;
class TTree;
class TList;
class TTree;

class EventSaver {
public:
  EventSaver(const ParameterSet& config, TList *outputList, std::string);
  ~EventSaver();

  void beginTree(TTree *tree);
  void beginEvent() { fSave = false; }
  void endEvent(Long64_t entry);

  void save() { fSave = true; }

  void terminate();

private:
  const bool fEnabled;
  bool fSave;
  bool fPickEvents;
  std::string fPickEventsFile;

  TEntryList *fEntryList;

  TTree* fTree;
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

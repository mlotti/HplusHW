#ifndef Framework_EventSaver_h
#define Framework_EventSaver_h

#include "Rtypes.h"

#include "boost/property_tree/ptree.hpp"

class TDirectory;
class TEntryList;
class TTree;
class TList;

class EventSaver {
public:
  EventSaver(const boost::property_tree::ptree& config, TList *outputList);
  ~EventSaver();

  void beginTree(const TTree *tree);
  void beginEvent() { fSave = false; }
  void endEvent(Long64_t entry);

  void save() { fSave = true; }

  void terminate();

private:
  const bool fEnabled;
  bool fSave;

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

#include "catch.hpp"

#include "test_createTree.h"

#include "Framework/interface/EventSaver.h"

#include "TDirectory.h"
#include "TEntryList.h"


TEST_CASE("EventSaver", "[Framework]") {
  std::unique_ptr<TTree> tree = createRealisticTree();

  boost::property_tree::ptree config;
  config.put("EventSaver.enabled", true);

  TDirectory dir("rootdir", "rootdir");

  EventSaver eventSaver(config, &dir);
  EventSaverClient saver;
  saver.setSaver(&eventSaver);

  eventSaver.beginTree(tree.get());

  eventSaver.beginEvent();
  saver.save();
  eventSaver.endEvent(0);

  eventSaver.beginEvent();
  eventSaver.endEvent(1);

  eventSaver.beginEvent();
  saver.save();
  saver.save();
  saver.save();
  eventSaver.endEvent(2);

  eventSaver.terminate();

  SECTION("Results") {
    TEntryList *entrylist = nullptr;
    dir.GetObject("entrylist", entrylist);
    REQUIRE( entrylist );
    REQUIRE( entrylist->GetN() == 2);
    CHECK( entrylist->Next() == 0 );
    CHECK( entrylist->Next() == 2 );
  }

}

#include "catch.hpp"

#include "test_createTree.h"

#include "Framework/interface/EventSaver.h"

#include "TDirectory.h"
#include "TEntryList.h"


TEST_CASE("EventSaver", "[Framework]") {
  std::unique_ptr<TTree> tree = createRealisticTree();

  boost::property_tree::ptree config;
  config.put("EventSaver.enabled", true);

  TList list;

  EventSaver eventSaver(config, &list);
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
    TObject *obj = list.FindObject("entrylist");
    REQUIRE( obj );
    TEntryList *entrylist = dynamic_cast<TEntryList *>(obj);
    REQUIRE( entrylist );
    REQUIRE( entrylist->GetN() == 2);
    CHECK( entrylist->Next() == 0 );
    CHECK( entrylist->Next() == 2 );
  }

}

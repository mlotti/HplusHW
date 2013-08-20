#include "HiggsAnalysis/HPlusRootFileDumper/interface/CounterItem.h"

namespace HPlusAnalysis {

CounterItem::CounterItem(std::string name, bool topLevelCounter)
  : fName(name),
  fIsTopLevelCounter(topLevelCounter) {
  reset();
}

CounterItem::~CounterItem() { 

}

}

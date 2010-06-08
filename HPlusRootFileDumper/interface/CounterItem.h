#ifndef HPLUSANALYSISCOUNTERITEM_H
#define HPLUSANALYSISCOUNTERITEM_H

#include <string>

namespace HPlusAnalysis {

/**
Object containing the information of one counted property

	@author Lauri Wendland
*/
class CounterItem {
 public:
  CounterItem(std::string name, bool topLevelCounter);
  ~CounterItem();

  void reset() { fValue = 0; }
  void increment(int value) { fValue += value; }
  
  std::string getName() const { return fName; }
  int getValue() const { return fValue; }
  bool isTopLevelCounter() const { return fIsTopLevelCounter; }
  
 private:
  std::string fName;
  int fValue;
  bool fIsTopLevelCounter;
};

}

#endif

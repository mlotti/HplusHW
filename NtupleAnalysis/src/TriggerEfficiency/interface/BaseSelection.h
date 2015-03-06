#ifndef TriggerEfficiency_BaseSelection_h
#define TriggerEfficiency_BaseSelection_h

#include "DataFormat/interface/Event.h"

class BaseSelection {
 public:
  BaseSelection(){}
  ~BaseSelection(){}

  virtual bool offlineSelection(const Event&) = 0;
  virtual bool onlineSelection(const Event&) = 0;

  double xVariable() { return xvariable;}

 protected:

  bool passedCtrlTtrigger(const Event&);

  double xvariable;
};

bool BaseSelection::passedCtrlTtrigger(const Event& fEvent){
  return true;
}
#endif

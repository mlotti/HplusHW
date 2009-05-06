#ifndef MYROOTTREE_H
#define MYROOTTREE_H
//#include "Utilities/Configuration/interface/Architecture.h"

#include "TROOT.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEvent.h"

class MyRootTree : public TObject {
public:
  MyRootTree(const char *fileName=0);
  virtual ~MyRootTree();

  void fillTree(MyEvent* event);
  void setAcceptance(string,double);

private:
  TH1F* eventInfo;
  TTree* rootTree;
  MyEvent* myEvent;
  TFile* rootFile;

  int    IBG,
         RUN;
  double CNOR,
         cross_section;

  map<string,double> acceptances;
  vector<string>     names;
}; 
#endif 

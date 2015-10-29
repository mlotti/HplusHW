#include "EventSelection/interface/CommonPlotsHelper.h"
#include "DataFormat/interface/Tau.h"

//===== Tau source plot
CommonPlotsHelper::CommonPlotsHelper()
: tauSourceBinLabels({"All",            // 0
                      "src:unknown",    // 1
                      "src:real tau",   // 2
                      "src:e->tau",     // 3
                      "src:mu->tau",    // 4
                      "src:jet->tau",   // 5
                      "partons:g->tau", // 6
                      "partons:uds->tau",// 7
                      "partons:c->tau", // 8
                      "partons:b->tau", // 9
                      "1pr:real tau",   // 10
                      "1pr:fake tau",   // 11
                      "2pr:real tau",   // 12
                      "2pr:fake tau",   // 13
                      "3pr:real tau",   // 14
                      "3pr:fake tau",   // 15            
                      "1pr0pi:real tau",// 16
                      "1pr0pi:fake tau",// 17
                      "1pr1pi:real tau",// 18
                      "1pr1pi:fake tau",// 19
                      "1pr2pi:real tau",// 20
                      "1pr2pi:fake tau",// 21
                      "2pr0pi:real tau",// 22
                      "2pr0pi:fake tau",// 23
                      "2pr1pi:real tau",// 24
                      "2pr1pi:fake tau",// 25
                      "3pr0pi:real tau",// 26
                      "3pr0pi:fake tau",// 27
                      "3pr>0pi:real tau",// 28
                      "3pr>0pi:fake tau",// 29
                      "origin:H+->tau", // 30
                      "origin:W->tau",  // 31
                      "origin:Z->tau",  // 32
                      "origin:other->tau",// 33
                      "origin:unknown->tau"// 34
})
{ }

std::vector<int> CommonPlotsHelper::getTauSourceData(bool isRealData, const Tau& tau) const {
  std::vector<int> result;
  if (isRealData) {
    // Accessors work only for MC taus
    return result;
  }
  // Control
  result.push_back(0);
  // Source
  if (tau.isUnknownTauDecay()) result.push_back(1);
  if (tau.isGenuineTau())      result.push_back(2);
  if (tau.isElectronToTau())   result.push_back(3);
  if (tau.isMuonToTau())       result.push_back(4);
  if (tau.isJetToTau())        result.push_back(5);
  // Partons
  if (tau.isGluonToTau()) result.push_back(6);
  if (tau.isQuarkToTau(1) || tau.isQuarkToTau(2) || tau.isQuarkToTau(3)) result.push_back(7);
  if (tau.isQuarkToTau(4)) result.push_back(8);
  if (tau.isQuarkToTau(5)) result.push_back(9);
  // 1 prong inclusive
  if (tau.nProngs() == 1 && tau.isGenuineTau()) result.push_back(10);
  if (tau.nProngs() == 1 && tau.isFakeTau())    result.push_back(11);
  // 2 prong inclusive
  if (tau.nProngs() == 2 && tau.isGenuineTau()) result.push_back(12);
  if (tau.nProngs() == 2 && tau.isFakeTau())    result.push_back(13);
  // 3 prong inclusive
  if (tau.nProngs() == 3 && tau.isGenuineTau()) result.push_back(14);
  if (tau.nProngs() == 3 && tau.isFakeTau())    result.push_back(15);
  // 1 prong exclusive
  if (tau.decayMode() == 0 && tau.isGenuineTau()) result.push_back(16);
  if (tau.decayMode() == 0 && tau.isFakeTau())    result.push_back(17);
  if (tau.decayMode() == 1 && tau.isGenuineTau()) result.push_back(18);
  if (tau.decayMode() == 1 && tau.isFakeTau())    result.push_back(19);
  if (tau.decayMode() == 2 && tau.isGenuineTau()) result.push_back(20);
  if (tau.decayMode() == 2 && tau.isFakeTau())    result.push_back(21);
  // 2 prong exclusive
  if (tau.decayMode() == 5 && tau.isGenuineTau()) result.push_back(22);
  if (tau.decayMode() == 5 && tau.isFakeTau())    result.push_back(23);
  if (tau.decayMode() == 6 && tau.isGenuineTau()) result.push_back(24);
  if (tau.decayMode() == 6 && tau.isFakeTau())    result.push_back(25);
  // 3 prong exclusive
  if (tau.decayMode() == 10 && tau.isGenuineTau()) result.push_back(26);
  if (tau.decayMode() == 10 && tau.isFakeTau())    result.push_back(27);
  if (tau.decayMode() == 11 && tau.isGenuineTau()) result.push_back(28);
  if (tau.decayMode() == 11 && tau.isFakeTau())    result.push_back(29);
  // Origin
  if (tau.isFromHplusDecay() && tau.isGenuineTau())  result.push_back(30);
  if (tau.isFromWDecay() && tau.isGenuineTau())      result.push_back(31);
  if (tau.isFromZDecay() && tau.isGenuineTau())      result.push_back(32);
  if (tau.isFromOtherSource() && tau.isGenuineTau()) result.push_back(33);
  if (tau.isFromUnknownSource() && tau.isGenuineTau()) result.push_back(34);
  
  return result;
}


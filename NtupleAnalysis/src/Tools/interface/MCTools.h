// -*- c++ -*-                                
#ifndef Tools_MCTools_h
#define Tools_MCTools_h

// System
#include <cmath>
#include <iomanip>
#include <string>
#include <vector>

// User
#include "DataFormat/interface/Event.h"
#include "Auxiliary/interface/Tools.h"

// ROOT
#include "TLorentzVector.h"
#include "Math/VectorUtil.h"

using namespace std;
typedef Particle<ParticleCollection<double> > genParticle;

class MCTools {
  
public:
  MCTools(Event &fEvt);
  ~MCTools();
  TLorentzVector GetVisibleP4(const unsigned int genP_index);
  bool IsNeutrino(const int pdgId);
  bool RecursivelyLookForMotherId(const int genP_index, int wantedMom_pdgId, const bool bAbsoluteMomId);
  double GetD0Mag(const int genP_index,	const int mom_Index, bool wrtPV=true);
  double GetLxy(const int genP_index,	bool wrtPV=true);
  double GetVertexX(void){return fEvent->vertexInfo().pvX();}
  double GetVertexY(void){return fEvent->vertexInfo().pvY();}
  double GetVertexZ(void){return fEvent->vertexInfo().pvZ();}
  int GetLdgDaughter(const int genP_index);
  std::vector<int> GetDaughters(const int my_index, const int my_id, bool bSkipSelf);
  void PrintDaughtersRecursively(const int genP_index);
  void _PrintDaughtersRecursively(const int genP_index, Table &table);
  void PrintGenParticle(const int genP_index, bool bPrintHeaders=true);
private:
  Event *fEvent;
  Tools auxTools;

  
};

#endif


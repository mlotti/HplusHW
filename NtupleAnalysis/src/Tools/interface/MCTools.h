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
#include "DataFormat/interface/Particle.h"
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
  TLorentzVector GetVisibleP4(const int genP_index);
  bool HasDaughter(const int genP_index, const int pdgId, bool bAllDaughters, bool bApplyAbs);
  bool HasMother(const int genP_index, int wantedMom_pdgId, const bool bAbsoluteMomId);
  bool IsChargedLepton(const int pdgId);
  bool IsLepton(const int pdgId);
  bool IsNeutrino(const int pdgId);
  bool IsQuark(const int pdgId);
  double GetD0Mag(const int genP_index, bool wrtPV=true);
  double GetLxy(const int genP_index,	bool wrtPV=true);
  double GetVertexX(void){return fEvent->vertexInfo().pvX();}
  double GetVertexY(void){return fEvent->vertexInfo().pvY();}
  double GetVertexZ(void){return fEvent->vertexInfo().pvZ();}
  int GetFinalSelf(const int genP_index);
  int GetLdgDaughter(const int genP_index);
  std::vector<int> GetAllDaughters(const int genP_index, bool bGetIds);
  std::vector<int> GetDaughters(const int my_index, bool bReturnIds=false);
  void PrintDaughters(const int genP_index, bool bPrintIds=false);
  void PrintGenParticle(const int genP_index, bool bPrintHeaders=true);
  void _GetAllDaughters(const int genP_index, vector<int> &genP_allDaughters, bool bGetIds);
  void _PrintDaughters(const int iDau_index, int &cLevel, int &row, Table &table, bool bPrintIds=false);
private:
  Event *fEvent;
  Tools auxTools;

  
};

#endif


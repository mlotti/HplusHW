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
#include "Math/LorentzVector.h"
#include "Math/VectorUtil.h"
#include "Math/Point3D.h"

using namespace std;
typedef Particle<ParticleCollection<double> > genParticle;

class MCTools {
  
public:
  MCTools(Event &fEvt);
  ~MCTools();
  ROOT::Math::XYZPoint GetPV(void);     // in mm
  ROOT::Math::XYZPoint GetVertex(void); // in mm
  double DeltaPhi(const double phi1, const double phi2);
  double DeltaAbs(const double val1, const double val2);
  double GetD0Mag(const int genP_index, bool wrtPV=true);
  double GetRapidity(const math::XYZTLorentzVector p4);
  double GetLxy(const int genP_index,	bool wrtPV=true);
  int GetFinalSelf(const int genP_index);
  int GetLdgDaughter(const int genP_index);
  std::vector<int> GetDaughters(const int my_index, bool bReturnIds=false);
  std::vector<int> GetAllDaughters(const int genP_index, bool bGetIds);
  void _GetAllDaughters(const int genP_index, vector<int> &genP_allDaughters, bool bGetIds);
   TLorentzVector GetVisibleP4(const int genP_index);
  bool HasDaughter(const int genP_index, const int pdgId, bool bAllDaughters, bool bApplyAbs);
  bool HasMother(std::vector<short> genP_mothers, int wantedMom_pdgId, const bool bAbsoluteMomId);
  bool IsChargedLepton(const int pdgId);
  bool IsLepton(const int pdgId);
  bool IsNeutrino(const int pdgId);
  bool IsQuark(const int pdgId);
  void PrintGenParticle(const int genP_index, bool bPrintHeaders=true);
  void PrintDaughters(const int genP_index, bool bPrintIds=false);
  void _PrintDaughters(const int iDau_index, int &cLevel, int &row, Table &table, bool bPrintIds=false);
private:
  Event *fEvent;
  Tools auxTools;

  
};

#endif


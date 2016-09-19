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

  bool IsChargedLepton(const int pdgId);
  bool IsLepton(const int pdgId);
  bool IsNeutrino(const int pdgId);
  bool IsQuark(const int pdgId);
  double DeltaAbs(const double val1, const double val2);
  double DeltaPhi(const double phi1, const double phi2);
  double GetD0(const genParticle &genP, const genParticle &mother, const genParticle &daughter, ROOT::Math::XYZPoint vtx);
  double GetLxy(const genParticle &genP, const genParticle &mother, const genParticle &daughter, ROOT::Math::XYZPoint vtx);
  double GetRapidity(const math::XYZTLorentzVector p4);
  void PrintGenParticle(const genParticle &genP, bool bPrintHeaders=true);
  void PrintGenDaughters(const genParticle &genP);
  bool HasMother(const genParticle &p, const int mom_pdgId);

private:
  Event *fEvent;
  Tools auxTools;

  void _PrintGenDaughters(const genParticle &genP, int &iRow, Table &table, int shiftLevel);
  
};

#endif

